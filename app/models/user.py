from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True,)
    email: str = Field(index=True, unique=True, max_length=255,)
    password_hash: str = Field(max_length=255,)
    role: str = Field(default="user", max_length=20,)
    is_active: bool = Field(default=True,)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),)