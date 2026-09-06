import argparse

from app.auth.password import hash_password
from app.database.database import Base, SessionLocal, engine
from app.database.models import User, UserSecurity


def upsert_admin(username: str, password: str, email: str | None = None):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            user = User(username=username, email=email, status="active")
            db.add(user)
            db.flush()
        else:
            user.email = email or user.email
            user.status = "active"

        security_row = db.query(UserSecurity).filter(UserSecurity.user_id == user.id).first()
        if security_row is None:
            security_row = UserSecurity(user_id=user.id)
            db.add(security_row)

        security_row.password_hash = hash_password(password)
        security_row.failed_count = 0
        db.commit()
        print(f"Admin user ready: {username}")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create or update a local administrator account")
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--email")
    args = parser.parse_args()
    upsert_admin(args.username, args.password, args.email)
