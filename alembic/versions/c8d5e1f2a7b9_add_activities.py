"""add activities

Revision ID: c8d5e1f2a7b9
Revises: b7e1f3c2d4a5
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

revision: str = "c8d5e1f2a7b9"
down_revision: Union[str, None] = "b7e1f3c2d4a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("action", sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_activities_user_id"), "activities", ["user_id"], unique=False)
    op.create_index(op.f("ix_activities_created_at"), "activities", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_activities_created_at"), table_name="activities")
    op.drop_index(op.f("ix_activities_user_id"), table_name="activities")
    op.drop_table("activities")
