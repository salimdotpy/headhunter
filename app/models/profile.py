from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Profile(SQLModel, table=True):
    __tablename__ = "profiles"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True, index=True)

    full_name: str = Field(default="", max_length=150)
    professional_title: str = Field(default="", max_length=200)
    summary: str = Field(default="", max_length=5000)

    phone: str = Field(default="", max_length=30)
    show_email: bool = Field(default=False)
    show_phone: bool = Field(default=False)

    location: str = Field(default="", max_length=200)
    show_location: bool = Field(default=False)

    website_url: str = Field(default="", max_length=500)
    show_website: bool = Field(default=False)

    linkedin_url: str = Field(default="", max_length=500)
    show_linkedin: bool = Field(default=False)

    github_url: str = Field(default="", max_length=500)
    show_github: bool = Field(default=False)

    profile_photo_path: str | None = Field(default=None, max_length=500)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
