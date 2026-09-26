from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.activity import Activity
from app.models.certification import Certification
from app.models.education import Education
from app.models.experience import Experience
from app.models.document import Document
from app.models.project import Project
from app.models.skill import Skill
from app.repositories.activity import ActivityRepository
from app.repositories.document import DocumentRepository
from app.repositories.portfolio import PortfolioRepository
from app.repositories.profile import ProfileRepository


class DashboardService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.profiles = ProfileRepository(session)
        self.portfolios = PortfolioRepository(session)
        self.documents = DocumentRepository(session)
        self.activities = ActivityRepository(session)

    async def _count(self, model: type, user_id: int) -> int:
        statement = select(func.count()).select_from(model).where(model.user_id == user_id)
        result = await self.session.exec(statement)
        return int(result.one())

    async def get_dashboard(self, user_id: int) -> dict:
        profile = await self.profiles.get_by_user_id(user_id)
        portfolio = await self.portfolios.get_by_user_id(user_id)

        counts = {
            "education": await self._count(Education, user_id),
            "experience": await self._count(Experience, user_id),
            "skills": await self._count(Skill, user_id),
            "certifications": await self._count(Certification, user_id),
            "projects": await self._count(Project, user_id),
            "documents": await self._count(Document, user_id),
        }

        completion_items = [
            bool(profile and profile.full_name.strip()),
            bool(profile and profile.professional_title.strip()),
            bool(profile and profile.summary.strip()),
            bool(profile and profile.profile_photo_path),
            counts["education"] > 0,
            counts["experience"] > 0,
            counts["skills"] > 0,
            counts["certifications"] > 0,
            counts["projects"] > 0,
        ]
        completed = sum(completion_items)
        completion_percent = round(completed / len(completion_items) * 100)

        return {
            "profile": profile,
            "portfolio": portfolio,
            "counts": counts,
            "completion_percent": completion_percent,
            "recent_activity": await self.activities.list_recent_for_user(user_id),
        }
