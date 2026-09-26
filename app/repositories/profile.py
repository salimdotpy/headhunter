from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.profile import Profile
from app.repositories.base import BaseRepository


class ProfileRepository(BaseRepository[Profile]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Profile)

    async def get_by_id(self, profile_id: int) -> Profile | None:
        return await self.session.get(Profile, profile_id)

    async def get_by_user_id(self, user_id: int) -> Profile | None:
        statement = select(Profile).where(Profile.user_id == user_id)
        result = await self.session.exec(statement)
        return result.first()

    async def add(self, profile: Profile) -> Profile:
        self.session.add(profile)
        return profile
