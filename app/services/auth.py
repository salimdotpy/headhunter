from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import hash_password, verify_password
from app.exceptions.auth import AuthenticationError
from app.exceptions.users import ResourceAlreadyExistsError
from app.models.user import User
from app.repositories.user import UserRepository


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)

    async def register(
        self,
        email: str,
        password: str,
    ) -> User:
        existing_user = await self.users.get_by_email(email)

        if existing_user is not None:
            raise ResourceAlreadyExistsError(
                "A user with this email already exists."
            )

        user = User(
            email=email,
            password_hash=hash_password(password),
        )

        await self.users.add(user)

        try:
            await self.session.commit()
            await self.session.refresh(user)
        except Exception:
            await self.session.rollback()
            raise

        return user

    async def authenticate(
        self,
        email: str,
        password: str,
    ) -> User:
        user = await self.users.get_by_email(email)

        if user is None:
            raise AuthenticationError("Invalid email or password.")

        if not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid email or password.")

        if not user.is_active:
            raise AuthenticationError("This account is inactive.")

        return user