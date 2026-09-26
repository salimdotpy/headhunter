from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.activity import Activity
from app.repositories.activity import ActivityRepository


class ActivityService:
    def __init__(self, session: AsyncSession):
        self.repository = ActivityRepository(session)

    async def record(self, user_id: int, action: str, description: str) -> Activity:
        activity = Activity(user_id=user_id, action=action, description=description)
        await self.repository.add(activity)
        return activity
