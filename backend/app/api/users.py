from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import (
    User,
    UserSecurity,
    Role,
    UserRole
)
from app.schemas.users import (
    UserCreate,
    UserResponse,
    RoleAssign
)
from app.auth.password import hash_password


router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)


@router.get(
    "",
    response_model=list[UserResponse]
)
def list_users(
    db: Session = Depends(get_db)
):

    return db.query(User).all()



@router.post(
    "",
    response_model=UserResponse
)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db)
):

    exists = (
        db.query(User)
        .filter(
            User.username == data.username
        )
        .first()
    )

    if exists:
        raise HTTPException(
            400,
            "username exists"
        )


    user = User(
        username=data.username,
        email=data.email,
        status="active"
    )

    db.add(user)
    db.flush()


    security = UserSecurity(
        user_id=user.id,
        password_hash=hash_password(
            data.password
        )
    )

    db.add(security)

    db.commit()
    db.refresh(user)

    return user



@router.post(
    "/{user_id}/roles"
)
def assign_role(
    user_id:int,
    data:RoleAssign,
    db:Session=Depends(get_db)
):

    user = db.query(User).filter(
        User.id==user_id
    ).first()

    if not user:
        raise HTTPException(
            404,
            "user not found"
        )


    role = db.query(Role).filter(
        Role.name==data.role
    ).first()


    if not role:
        role = Role(
            name=data.role
        )

        db.add(role)
        db.flush()


    relation = UserRole(
        user_id=user.id,
        role_id=role.id
    )

    db.add(relation)
    db.commit()


    return {
        "message":"role assigned",
        "user_id":user_id,
        "role":data.role
    }
