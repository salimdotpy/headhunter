from datetime import datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.password_reset import PasswordResetToken
from app.repositories.base import BaseRepository


class PasswordResetRepository(BaseRepository[PasswordResetToken]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, PasswordResetToken)

    async def add(self, token: PasswordResetToken) -> PasswordResetToken:
        self.session.add(token)
        return token

    async def get_valid(self, token_hash: str, now: datetime) -> PasswordResetToken | None:
        statement = select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > now,
        )
        result = await self.session.exec(statement)
        return result.first()

    async def invalidate_for_user(self, user_id: int, now: datetime) -> None:
        statement = select(PasswordResetToken).where(
            PasswordResetToken.user_id == user_id,
            PasswordResetToken.used_at.is_(None),
        )
        result = await self.session.exec(statement)
        for token in result.all():
            token.used_at = now
