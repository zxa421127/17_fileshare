from datetime import datetime, timezone

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String

from .database import Base


def utc_now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String)
    phone = Column(String)
    status = Column(String, default="active", nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class UserSecurity(Base):
    __tablename__ = "user_security"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    failed_count = Column(Integer, default=0, nullable=False)
    mfa_enabled = Column(Boolean, default=False, nullable=False)


class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id = Column(Integer, primary_key=True)
    target = Column(String, nullable=False)
    type = Column(String, nullable=False)
    code_hash = Column(String, nullable=False)
    status = Column(String, default="unused", nullable=False)


class FileObject(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    original_name = Column(String, nullable=False)
    object_name = Column(String, unique=True, nullable=False, index=True)
    content_type = Column(String, nullable=False, default="application/octet-stream")
    size = Column(BigInteger, nullable=False)
    owner_id = Column(Integer, nullable=False, index=True)
    status = Column(String, nullable=False, default="active", index=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
