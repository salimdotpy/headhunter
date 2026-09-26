import re
import unicodedata
from datetime import datetime, timezone

from sqlmodel.ext.asyncio.session import AsyncSession

from app.exceptions.base import ResourceNotFoundError
from app.exceptions.portfolio import PortfolioSlugAlreadyExistsError
from app.models.portfolio import Portfolio
from app.repositories.portfolio import PortfolioRepository


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return slug or "portfolio"


class PortfolioService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.portfolios = PortfolioRepository(session)

    async def get_by_user_id(self, user_id: int) -> Portfolio:
        portfolio = await self.portfolios.get_by_user_id(user_id)
        if portfolio is None:
            raise ResourceNotFoundError("Portfolio not found.")
        return portfolio

    async def generate_unique_slug(self, base_value: str) -> str:
        base_slug = slugify(base_value)[:90].rstrip("-")
        candidate = base_slug or "portfolio"
        counter = 2

        while await self.portfolios.slug_exists(candidate):
            suffix = f"-{counter}"
            candidate = f"{base_slug[:100 - len(suffix)]}{suffix}"
            counter += 1

        return candidate

    async def update_slug(self, user_id: int, slug: str) -> Portfolio:
        portfolio = await self.get_by_user_id(user_id)
        normalized_slug = slug.strip().lower()

        existing = await self.portfolios.get_by_slug(normalized_slug)
        if existing is not None and existing.id != portfolio.id:
            raise PortfolioSlugAlreadyExistsError(
                "That portfolio URL is already in use."
            )

        portfolio.slug = normalized_slug
        portfolio.updated_at = datetime.now(timezone.utc)

        try:
            await self.session.commit()
            await self.session.refresh(portfolio)
        except Exception:
            await self.session.rollback()
            raise

        return portfolio
