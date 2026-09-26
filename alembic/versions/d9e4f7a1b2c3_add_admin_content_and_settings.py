"""add admin content and settings

Revision ID: d9e4f7a1b2c3
Revises: c8d5e1f2a7b9
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel

revision: str = "d9e4f7a1b2c3"
down_revision: Union[str, None] = "c8d5e1f2a7b9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "website_content",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content_key", sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column("body", sqlmodel.sql.sqltypes.AutoString(length=10000), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("content_key"),
    )
    op.create_index(op.f("ix_website_content_content_key"), "website_content", ["content_key"], unique=True)
    op.create_table(
        "platform_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("setting_key", sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column("setting_value", sqlmodel.sql.sqltypes.AutoString(length=2000), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("setting_key"),
    )
    op.create_index(op.f("ix_platform_settings_setting_key"), "platform_settings", ["setting_key"], unique=True)

def downgrade() -> None:
    op.drop_index(op.f("ix_platform_settings_setting_key"), table_name="platform_settings")
    op.drop_table("platform_settings")
    op.drop_index(op.f("ix_website_content_content_key"), table_name="website_content")
    op.drop_table("website_content")
