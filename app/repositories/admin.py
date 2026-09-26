from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.user import User
from app.models.portfolio import Portfolio
from app.models.document import Document
from app.models.activity import Activity
from app.models.website_content import WebsiteContent
from app.models.platform_setting import PlatformSetting

class AdminRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_users(self, search: str = "", status: str = "") -> list[User]:
        statement = select(User).order_by(User.created_at.desc())
        if search:
            term = f"%{search.strip()}%"
            statement = statement.where(User.email.like(term))
        if status == "active":
            statement = statement.where(User.is_active == True)
        elif status == "inactive":
            statement = statement.where(User.is_active == False)
        result = await self.session.exec(statement)
        return list(result.all())

    async def get_user(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def list_portfolios(self) -> list[Portfolio]:
        result = await self.session.exec(select(Portfolio).order_by(Portfolio.updated_at.desc()))
        return list(result.all())

    async def list_activities(self, limit: int = 100) -> list[Activity]:
        result = await self.session.exec(select(Activity).order_by(Activity.created_at.desc()).limit(limit))
        return list(result.all())

    async def list_content(self) -> list[WebsiteContent]:
        result = await self.session.exec(select(WebsiteContent).order_by(WebsiteContent.content_key))
        return list(result.all())

    async def get_content(self, content_id: int) -> WebsiteContent | None:
        return await self.session.get(WebsiteContent, content_id)

    async def add_content(self, item: WebsiteContent) -> None:
        self.session.add(item)

    async def list_settings(self) -> list[PlatformSetting]:
        result = await self.session.exec(select(PlatformSetting).order_by(PlatformSetting.setting_key))
        return list(result.all())

    async def get_setting(self, setting_id: int) -> PlatformSetting | None:
        return await self.session.get(PlatformSetting, setting_id)

    async def add_setting(self, item: PlatformSetting) -> None:
        self.session.add(item)
