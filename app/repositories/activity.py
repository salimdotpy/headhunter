from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.activity import Activity


class ActivityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_recent_for_user(self, user_id: int, limit: int = 8) -> list[Activity]:
        statement = (
            select(Activity)
            .where(Activity.user_id == user_id)
            .order_by(Activity.created_at.desc())
            .limit(limit)
        )
        result = await self.session.exec(statement)
        return list(result.all())

    async def add(self, activity: Activity) -> Activity:
        self.session.add(activity)
        return activity
