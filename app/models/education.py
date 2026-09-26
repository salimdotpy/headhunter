from datetime import date, datetime, timezone

from sqlmodel import Field, SQLModel


class Education(SQLModel, table=True):
    __tablename__ = "education"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    institution: str = Field(max_length=200)
    qualification: str = Field(max_length=200)
    field_of_study: str = Field(default="", max_length=200)
    start_date: date | None = None
    end_date: date | None = None
    description: str = Field(default="", max_length=5000)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
