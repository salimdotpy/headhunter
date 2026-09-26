from datetime import date, datetime, timezone

from sqlmodel import Field, SQLModel


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=5000)
    role: str = Field(default="", max_length=200)
    technologies: str = Field(default="", max_length=1000)
    project_date: date | None = None
    project_url: str = Field(default="", max_length=500)
    image_path: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
