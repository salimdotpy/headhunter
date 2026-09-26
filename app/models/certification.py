from datetime import date, datetime, timezone

from sqlmodel import Field, SQLModel


class Certification(SQLModel, table=True):
    __tablename__ = "certifications"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field(max_length=200)
    issuer: str = Field(max_length=200)
    issue_date: date | None = None
    expiry_date: date | None = None
    credential_reference: str = Field(default="", max_length=200)
    certificate_path: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
