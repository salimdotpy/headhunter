from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    certification_id: int | None = Field(default=None, foreign_key="certifications.id", index=True)
    project_id: int | None = Field(default=None, foreign_key="projects.id", index=True)
    category: str = Field(max_length=40, index=True)
    original_filename: str = Field(max_length=255)
    stored_filename: str = Field(max_length=255, unique=True)
    file_path: str = Field(max_length=500)
    mime_type: str = Field(max_length=100)
    file_size: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
