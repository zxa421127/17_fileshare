from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(
        String,
        unique=True,
        index=True
    )

    email = Column(
        String
    )

    status = Column(
        String,
        default="active"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    roles = relationship(
        "Role",
        secondary="user_roles"
    )



class UserSecurity(Base):

    __tablename__ = "user_security"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    password_hash = Column(
        String
    )

    failed_count = Column(
        Integer,
        default=0
    )

    last_login = Column(
        DateTime,
        nullable=True
    )



class FileObject(Base):

    __tablename__ = "files"

    id = Column(
        Integer,
        primary_key=True
    )

    original_name = Column(
        String
    )

    object_name = Column(
        String
    )

    content_type = Column(
        String
    )

    size = Column(
        Integer
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    status = Column(
        String,
        default="active"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



class Role(Base):

    __tablename__ = "roles"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String,
        unique=True
    )



class Permission(Base):

    __tablename__ = "permissions"

    id = Column(
        Integer,
        primary_key=True
    )

    code = Column(
        String,
        unique=True
    )



class UserRole(Base):

    __tablename__ = "user_roles"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    role_id = Column(
        Integer,
        ForeignKey("roles.id")
    )



class FilePermission(Base):

    __tablename__ = "file_permissions"

    id = Column(
        Integer,
        primary_key=True
    )

    file_id = Column(
        Integer,
        ForeignKey("files.id")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    permission = Column(
        String,
        default="read"
    )
