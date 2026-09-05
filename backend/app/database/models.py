from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)
    phone = Column(String)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)


class UserSecurity(Base):
    __tablename__ = "user_security"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    password_hash = Column(String)
    failed_count = Column(Integer, default=0)
    mfa_enabled = Column(Boolean, default=False)


class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id = Column(Integer, primary_key=True)
    target = Column(String)
    type = Column(String)
    code_hash = Column(String)
    status = Column(String, default="unused")
