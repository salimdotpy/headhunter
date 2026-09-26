from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Portfolio(SQLModel, table=True):
    __tablename__ = "portfolios"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True, index=True)
    slug: str = Field(max_length=100, unique=True, index=True)
    is_published: bool = Field(default=False)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
