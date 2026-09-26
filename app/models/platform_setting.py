from datetime import datetime, timezone
from sqlmodel import Field, SQLModel

class PlatformSetting(SQLModel, table=True):
    __tablename__ = "platform_settings"
    id: int | None = Field(default=None, primary_key=True)
    setting_key: str = Field(max_length=100, unique=True, index=True)
    setting_value: str = Field(default="", max_length=2000)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
