from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)

    async def create_user(self, user: User) -> User:
        await self.users.add(user)

        await self.session.commit()
        await self.session.refresh(user)

        return user