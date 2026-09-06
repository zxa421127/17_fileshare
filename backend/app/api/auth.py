from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.jwt import create_token, decode_token
from app.auth.password import verify_password
from app.database.database import get_db
from app.database.models import User, UserSecurity
from app.schemas.auth import CurrentUserResponse, LoginRequest, LoginResponse


router = APIRouter(prefix="/api/auth", tags=["auth"])
bearer_scheme = HTTPBearer(auto_error=False)


@router.get("/status")
def auth_status():
    return {
        "auth": "ready",
        "methods": [
            "password",
            "email_code",
            "wechat",
            "sms_switch",
        ],
    }


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    security_row = db.query(UserSecurity).filter(UserSecurity.user_id == user.id).first()
    if not security_row or not verify_password(payload.password, security_row.password_hash):
        if security_row:
            security_row.failed_count = (security_row.failed_count or 0) + 1
            db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if security_row.failed_count:
        security_row.failed_count = 0
        db.commit()

    return LoginResponse(access_token=create_token(user.id))


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    try:
        payload = decode_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unavailable",
        )
    return user


@router.get("/me", response_model=CurrentUserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user
