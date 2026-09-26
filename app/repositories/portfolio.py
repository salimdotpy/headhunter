from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.portfolio import Portfolio
from app.repositories.base import BaseRepository


class PortfolioRepository(BaseRepository[Portfolio]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Portfolio)

    async def get_by_id(self, portfolio_id: int) -> Portfolio | None:
        return await self.session.get(Portfolio, portfolio_id)

    async def get_by_user_id(self, user_id: int) -> Portfolio | None:
        statement = select(Portfolio).where(Portfolio.user_id == user_id)
        result = await self.session.exec(statement)
        return result.first()

    async def get_by_slug(self, slug: str) -> Portfolio | None:
        statement = select(Portfolio).where(Portfolio.slug == slug)
        result = await self.session.exec(statement)
        return result.first()

    async def slug_exists(self, slug: str) -> bool:
        return await self.get_by_slug(slug) is not None

    async def add(self, portfolio: Portfolio) -> Portfolio:
        self.session.add(portfolio)
        return portfolio
