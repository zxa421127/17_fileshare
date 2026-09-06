"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-09-06
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "user_security",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("failed_count", sa.Integer(), nullable=False),
        sa.Column("mfa_enabled", sa.Boolean(), nullable=False),
    )
    op.create_index("ix_user_security_user_id", "user_security", ["user_id"], unique=True)

    op.create_table(
        "verification_codes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("target", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("code_hash", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
    )

    op.create_table(
        "files",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("original_name", sa.String(), nullable=False),
        sa.Column("object_name", sa.String(), nullable=False),
        sa.Column("content_type", sa.String(), nullable=False),
        sa.Column("size", sa.BigInteger(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_files_object_name", "files", ["object_name"], unique=True)
    op.create_index("ix_files_owner_id", "files", ["owner_id"], unique=False)
    op.create_index("ix_files_status", "files", ["status"], unique=False)


def downgrade():
    op.drop_index("ix_files_status", table_name="files")
    op.drop_index("ix_files_owner_id", table_name="files")
    op.drop_index("ix_files_object_name", table_name="files")
    op.drop_table("files")
    op.drop_table("verification_codes")
    op.drop_index("ix_user_security_user_id", table_name="user_security")
    op.drop_table("user_security")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")
