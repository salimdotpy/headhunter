from datetime import datetime, timezone
from sqlmodel import Field, SQLModel

class WebsiteContent(SQLModel, table=True):
    __tablename__ = "website_content"
    id: int | None = Field(default=None, primary_key=True)
    content_key: str = Field(max_length=100, unique=True, index=True)
    title: str = Field(default="", max_length=200)
    body: str = Field(default="", max_length=10000)
    is_published: bool = Field(default=True)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
