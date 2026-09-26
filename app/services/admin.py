from datetime import datetime, timezone
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.exceptions.base import ResourceNotFoundError
from app.models.activity import Activity
from app.models.document import Document
from app.models.portfolio import Portfolio
from app.models.platform_setting import PlatformSetting
from app.models.user import User
from app.models.website_content import WebsiteContent
from app.repositories.admin import AdminRepository

class AdminService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = AdminRepository(session)

    async def _count(self, model, condition=None) -> int:
        statement = select(func.count()).select_from(model)
        if condition is not None:
            statement = statement.where(condition)
        result = await self.session.exec(statement)
        return int(result.one())

    async def dashboard(self) -> dict:
        return {
            "total_users": await self._count(User),
            "active_users": await self._count(User, User.is_active == True),
            "published_portfolios": await self._count(Portfolio, Portfolio.is_published == True),
            "uploaded_documents": await self._count(Document),
            "recent_activity": await self.repo.list_activities(12),
        }

    async def users(self, search: str = "", status: str = ""):
        return await self.repo.list_users(search, status)

    async def set_user_status(self, user_id: int, is_active: bool, admin_user_id: int) -> User:
        user = await self.repo.get_user(user_id)
        if user is None:
            raise ResourceNotFoundError("User not found.")
        if user.id == admin_user_id and not is_active:
            raise ValueError("An administrator cannot deactivate their own account.")
        user.is_active = is_active
        user.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def portfolios(self):
        return await self.repo.list_portfolios()

    async def activities(self):
        return await self.repo.list_activities(100)

    async def content(self):
        return await self.repo.list_content()

    async def save_content(self, content_id: int | None, key: str, title: str, body: str, published: bool) -> WebsiteContent:
        item = await self.repo.get_content(content_id) if content_id else None
        if item is None:
            item = WebsiteContent(content_key=key.strip().lower(), title=title.strip(), body=body.strip(), is_published=published)
            await self.repo.add_content(item)
        else:
            item.content_key = key.strip().lower()
            item.title = title.strip()
            item.body = body.strip()
            item.is_published = published
            item.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def settings(self):
        return await self.repo.list_settings()

    async def save_setting(self, setting_id: int | None, key: str, value: str) -> PlatformSetting:
        item = await self.repo.get_setting(setting_id) if setting_id else None
        if item is None:
            item = PlatformSetting(setting_key=key.strip().lower(), setting_value=value.strip())
            await self.repo.add_setting(item)
        else:
            item.setting_key = key.strip().lower()
            item.setting_value = value.strip()
            item.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(item)
        return item
