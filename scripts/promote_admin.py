import asyncio
import sys
from app.core.database import async_session_factory
from app.repositories.user import UserRepository

async def main(email: str) -> None:
    async with async_session_factory() as session:
        user = await UserRepository(session).get_by_email(email.strip().lower())
        if user is None:
            raise SystemExit("User not found.")
        user.role = "admin"
        await session.commit()
        print(f"Admin role granted to {user.email}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/promote_admin.py user@example.com")
    asyncio.run(main(sys.argv[1]))
