from typing import TypeVar

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.certification import Certification
from app.models.education import Education
from app.models.experience import Experience
from app.models.project import Project
from app.models.skill import Skill

ModelType = TypeVar("ModelType", bound=SQLModel)


class UserOwnedRepository:
    model: type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id_for_user(self, item_id: int, user_id: int) -> ModelType | None:
        statement = select(self.model).where(
            self.model.id == item_id,
            self.model.user_id == user_id,
        )
        result = await self.session.exec(statement)
        return result.first()

    async def list_for_user(self, user_id: int) -> list[ModelType]:
        statement = select(self.model).where(self.model.user_id == user_id).order_by(self.model.id.desc())
        result = await self.session.exec(statement)
        return list(result.all())

    async def add(self, item: ModelType) -> ModelType:
        self.session.add(item)
        return item

    async def delete(self, item: ModelType) -> None:
        await self.session.delete(item)


class EducationRepository(UserOwnedRepository):
    model = Education


class ExperienceRepository(UserOwnedRepository):
    model = Experience


class SkillRepository(UserOwnedRepository):
    model = Skill


class CertificationRepository(UserOwnedRepository):
    model = Certification


class ProjectRepository(UserOwnedRepository):
    model = Project
