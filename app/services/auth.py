import re
import unicodedata

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import hash_password, verify_password
from app.exceptions.auth import AuthenticationError
from app.exceptions.users import ResourceAlreadyExistsError
from app.models.portfolio import Portfolio
from app.models.profile import Profile
from app.models.user import User
from app.repositories.portfolio import PortfolioRepository
from app.repositories.profile import ProfileRepository
from app.repositories.user import UserRepository


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return slug or "portfolio"


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)
        self.profiles = ProfileRepository(session)
        self.portfolios = PortfolioRepository(session)

    async def _unique_portfolio_slug(self, full_name: str) -> str:
        base_slug = slugify(full_name)[:90].rstrip("-")
        candidate = base_slug or "portfolio"
        counter = 2

        while await self.portfolios.slug_exists(candidate):
            suffix = f"-{counter}"
            candidate = f"{base_slug[:100 - len(suffix)]}{suffix}"
            counter += 1

        return candidate

    async def register(
        self,
        *,
        full_name: str,
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

        try:
            await self.users.add(user)
            await self.session.flush()

            if user.id is None:
                raise RuntimeError("User ID was not generated.")

            profile = Profile(
                user_id=user.id,
                full_name=full_name.strip(),
            )

            portfolio = Portfolio(
                user_id=user.id,
                slug=await self._unique_portfolio_slug(full_name),
            )

            await self.profiles.add(profile)
            await self.portfolios.add(portfolio)

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
