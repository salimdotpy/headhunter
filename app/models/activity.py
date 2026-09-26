from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Activity(SQLModel, table=True):
    __tablename__ = "activities"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    action: str = Field(max_length=100)
    description: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
