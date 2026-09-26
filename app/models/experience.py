from datetime import date, datetime, timezone

from sqlmodel import Field, SQLModel


class Experience(SQLModel, table=True):
    __tablename__ = "work_experience"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    job_title: str = Field(max_length=200)
    company: str = Field(max_length=200)
    location: str = Field(default="", max_length=200)
    start_date: date | None = None
    end_date: date | None = None
    description: str = Field(default="", max_length=5000)
    is_current: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
