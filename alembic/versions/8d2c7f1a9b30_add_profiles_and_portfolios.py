"""add profiles and portfolios

Revision ID: 8d2c7f1a9b30
Revises: 456f0abd91f2
Create Date: 2026-09-26 20:45:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


revision: str = "8d2c7f1a9b30"
down_revision: Union[str, Sequence[str], None] = "456f0abd91f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "full_name",
            sqlmodel.sql.sqltypes.AutoString(length=150),
            nullable=False,
        ),
        sa.Column(
            "professional_title",
            sqlmodel.sql.sqltypes.AutoString(length=200),
            nullable=False,
        ),
        sa.Column(
            "summary",
            sqlmodel.sql.sqltypes.AutoString(length=5000),
            nullable=False,
        ),
        sa.Column(
            "phone",
            sqlmodel.sql.sqltypes.AutoString(length=30),
            nullable=False,
        ),
        sa.Column("show_email", sa.Boolean(), nullable=False),
        sa.Column("show_phone", sa.Boolean(), nullable=False),
        sa.Column(
            "location",
            sqlmodel.sql.sqltypes.AutoString(length=200),
            nullable=False,
        ),
        sa.Column("show_location", sa.Boolean(), nullable=False),
        sa.Column(
            "website_url",
            sqlmodel.sql.sqltypes.AutoString(length=500),
            nullable=False,
        ),
        sa.Column("show_website", sa.Boolean(), nullable=False),
        sa.Column(
            "linkedin_url",
            sqlmodel.sql.sqltypes.AutoString(length=500),
            nullable=False,
        ),
        sa.Column("show_linkedin", sa.Boolean(), nullable=False),
        sa.Column(
            "github_url",
            sqlmodel.sql.sqltypes.AutoString(length=500),
            nullable=False,
        ),
        sa.Column("show_github", sa.Boolean(), nullable=False),
        sa.Column(
            "profile_photo_path",
            sqlmodel.sql.sqltypes.AutoString(length=500),
            nullable=True,
        ),
        sa.Column("created_at", sqlmodel.sql.sqltypes.UTCDateTime(), nullable=False),
        sa.Column("updated_at", sqlmodel.sql.sqltypes.UTCDateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_profiles_user_id"),
        "profiles",
        ["user_id"],
        unique=True,
    )

    op.create_table(
        "portfolios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "slug",
            sqlmodel.sql.sqltypes.AutoString(length=100),
            nullable=False,
        ),
        sa.Column("is_published", sa.Boolean(), nullable=False),
        sa.Column("created_at", sqlmodel.sql.sqltypes.UTCDateTime(), nullable=False),
        sa.Column("updated_at", sqlmodel.sql.sqltypes.UTCDateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_portfolios_user_id"),
        "portfolios",
        ["user_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_portfolios_slug"),
        "portfolios",
        ["slug"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_portfolios_slug"), table_name="portfolios")
    op.drop_index(op.f("ix_portfolios_user_id"), table_name="portfolios")
    op.drop_table("portfolios")

    op.drop_index(op.f("ix_profiles_user_id"), table_name="profiles")
    op.drop_table("profiles")
