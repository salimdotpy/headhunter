from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.exceptions.auth import AuthenticationError
from app.models.user import User
from app.repositories.user import UserRepository


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> User:
    user_id = request.session.get("user_id")

    if user_id is None:
        raise AuthenticationError("Authentication required.")

    user_repository = UserRepository(session)

    user = await user_repository.get_by_id(user_id)

    if user is None or not user.is_active:
        request.session.clear()
        raise AuthenticationError("Authentication required.")

    return user