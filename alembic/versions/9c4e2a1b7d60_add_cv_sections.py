"""add cv sections

Revision ID: 9c4e2a1b7d60
Revises: 8d2c7f1a9b30
Create Date: 2026-09-26 20:55:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

revision: str = "9c4e2a1b7d60"
down_revision: Union[str, Sequence[str], None] = "8d2c7f1a9b30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "education",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("institution", sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column("qualification", sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column("field_of_study", sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(length=5000), nullable=False),
        sa.Column("created_at", sqlmodel.sql.sqltypes.UTCDateTime(), nullable=False),
        sa.Column("updated_at", sqlmodel.sql.sqltypes.UTCDateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_education_user_id", "education", ["user_id"], unique=False)

    op.create_table(
        "work_experience",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("job_title", sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column("company", sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column("location", sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(length=5000), nullable=False),
        sa.Column("is_current", sa.Boolean(), nullable=False),
        sa.Column("created_at", sqlmodel.sql.sqltypes.UTCDateTime(), nullable=False),
        sa.Column("updated_at", sqlmodel.sql.sqltypes.UTCDateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_work_experience_user_id", "work_experience", ["user_id"], unique=False)

    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=150), nullable=False),
        sa.Column("proficiency", sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
        sa.Column("created_at", sqlmodel.sql.sqltypes.UTCDateTime(), nullable=False),
        sa.Column("updated_at", sqlmodel.sql.sqltypes.UTCDateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_skills_user_id", "skills", ["user_id"], unique=False)

    op.create_table(
        "certifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column("issuer", sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column("issue_date", sa.Date(), nullable=True),
        sa.Column("expiry_date", sa.Date(), nullable=True),
        sa.Column("credential_reference", sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column("certificate_path", sqlmodel.sql.sqltypes.AutoString(length=500), nullable=True),
        sa.Column("created_at", sqlmodel.sql.sqltypes.UTCDateTime(), nullable=False),
        sa.Column("updated_at", sqlmodel.sql.sqltypes.UTCDateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_certifications_user_id", "certifications", ["user_id"], unique=False)

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(length=5000), nullable=False),
        sa.Column("role", sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column("technologies", sqlmodel.sql.sqltypes.AutoString(length=1000), nullable=False),
        sa.Column("project_date", sa.Date(), nullable=True),
        sa.Column("project_url", sqlmodel.sql.sqltypes.AutoString(length=500), nullable=False),
        sa.Column("image_path", sqlmodel.sql.sqltypes.AutoString(length=500), nullable=True),
        sa.Column("created_at", sqlmodel.sql.sqltypes.UTCDateTime(), nullable=False),
        sa.Column("updated_at", sqlmodel.sql.sqltypes.UTCDateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_projects_user_id", "projects", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_projects_user_id", table_name="projects")
    op.drop_table("projects")
    op.drop_index("ix_certifications_user_id", table_name="certifications")
    op.drop_table("certifications")
    op.drop_index("ix_skills_user_id", table_name="skills")
    op.drop_table("skills")
    op.drop_index("ix_work_experience_user_id", table_name="work_experience")
    op.drop_table("work_experience")
    op.drop_index("ix_education_user_id", table_name="education")
    op.drop_table("education")
