from datetime import date, datetime, timezone

from sqlmodel.ext.asyncio.session import AsyncSession

from app.exceptions.base import ResourceNotFoundError
from app.models.certification import Certification
from app.models.education import Education
from app.models.experience import Experience
from app.models.project import Project
from app.models.skill import Skill
from app.services.activity import ActivityService
from app.repositories.cv import (
    CertificationRepository,
    EducationRepository,
    ExperienceRepository,
    ProjectRepository,
    SkillRepository,
)


class CVServiceBase:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.activities = ActivityService(session)

    async def _commit(self) -> None:
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise


class EducationService(CVServiceBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = EducationRepository(session)

    async def list(self, user_id: int):
        return await self.repo.list_for_user(user_id)

    async def create(self, user_id: int, *, institution: str, qualification: str, field_of_study: str, start_date: date | None, end_date: date | None, description: str) -> Education:
        item = Education(user_id=user_id, institution=institution.strip(), qualification=qualification.strip(), field_of_study=field_of_study.strip(), start_date=start_date, end_date=end_date, description=description.strip())
        await self.repo.add(item)
        await self.activities.record(user_id, "cv.create", "Added education record.")
        await self._commit()
        await self.session.refresh(item)
        return item

    async def update(self, user_id: int, item_id: int, **data) -> Education:
        item = await self.repo.get_by_id_for_user(item_id, user_id)
        if item is None:
            raise ResourceNotFoundError("Education record not found.")
        for key, value in data.items():
            setattr(item, key, value.strip() if isinstance(value, str) else value)
        item.updated_at = datetime.now(timezone.utc)
        await self.activities.record(user_id, "cv.update", "Updated education record.")
        await self._commit()
        await self.session.refresh(item)
        return item

    async def delete(self, user_id: int, item_id: int) -> None:
        item = await self.repo.get_by_id_for_user(item_id, user_id)
        if item is None:
            raise ResourceNotFoundError("Education record not found.")
        await self.repo.delete(item)
        await self.activities.record(user_id, "cv.delete", "Deleted education record.")
        await self._commit()


class ExperienceService(CVServiceBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = ExperienceRepository(session)

    async def list(self, user_id: int):
        return await self.repo.list_for_user(user_id)

    async def create(self, user_id: int, *, job_title: str, company: str, location: str, start_date: date | None, end_date: date | None, description: str, is_current: bool) -> Experience:
        item = Experience(user_id=user_id, job_title=job_title.strip(), company=company.strip(), location=location.strip(), start_date=start_date, end_date=None if is_current else end_date, description=description.strip(), is_current=is_current)
        await self.repo.add(item)
        await self.activities.record(user_id, "cv.create", "Added work experience record.")
        await self._commit()
        await self.session.refresh(item)
        return item

    async def update(self, user_id: int, item_id: int, **data) -> Experience:
        item = await self.repo.get_by_id_for_user(item_id, user_id)
        if item is None:
            raise ResourceNotFoundError("Work experience record not found.")
        if data.get("is_current"):
            data["end_date"] = None
        for key, value in data.items():
            setattr(item, key, value.strip() if isinstance(value, str) else value)
        item.updated_at = datetime.now(timezone.utc)
        await self.activities.record(user_id, "cv.update", "Updated work experience record.")
        await self._commit()
        await self.session.refresh(item)
        return item

    async def delete(self, user_id: int, item_id: int) -> None:
        item = await self.repo.get_by_id_for_user(item_id, user_id)
        if item is None:
            raise ResourceNotFoundError("Work experience record not found.")
        await self.repo.delete(item)
        await self.activities.record(user_id, "cv.delete", "Deleted work experience record.")
        await self._commit()


class SkillService(CVServiceBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = SkillRepository(session)

    async def list(self, user_id: int):
        return await self.repo.list_for_user(user_id)

    async def create(self, user_id: int, *, name: str, proficiency: str) -> Skill:
        item = Skill(user_id=user_id, name=name.strip(), proficiency=proficiency.strip())
        await self.repo.add(item)
        await self.activities.record(user_id, "cv.create", "Added skill.")
        await self._commit()
        await self.session.refresh(item)
        return item

    async def update(self, user_id: int, item_id: int, *, name: str, proficiency: str) -> Skill:
        item = await self.repo.get_by_id_for_user(item_id, user_id)
        if item is None:
            raise ResourceNotFoundError("Skill not found.")
        item.name = name.strip()
        item.proficiency = proficiency.strip()
        item.updated_at = datetime.now(timezone.utc)
        await self.activities.record(user_id, "cv.update", "Updated skill.")
        await self._commit()
        await self.session.refresh(item)
        return item

    async def delete(self, user_id: int, item_id: int) -> None:
        item = await self.repo.get_by_id_for_user(item_id, user_id)
        if item is None:
            raise ResourceNotFoundError("Skill not found.")
        await self.repo.delete(item)
        await self.activities.record(user_id, "cv.delete", "Deleted skill.")
        await self._commit()


class CertificationService(CVServiceBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = CertificationRepository(session)

    async def list(self, user_id: int):
        return await self.repo.list_for_user(user_id)

    async def create(self, user_id: int, *, name: str, issuer: str, issue_date: date | None, expiry_date: date | None, credential_reference: str) -> Certification:
        item = Certification(user_id=user_id, name=name.strip(), issuer=issuer.strip(), issue_date=issue_date, expiry_date=expiry_date, credential_reference=credential_reference.strip())
        await self.repo.add(item)
        await self.activities.record(user_id, "cv.create", "Added certification.")
        await self._commit()
        await self.session.refresh(item)
        return item

    async def update(self, user_id: int, item_id: int, **data) -> Certification:
        item = await self.repo.get_by_id_for_user(item_id, user_id)
        if item is None:
            raise ResourceNotFoundError("Certification not found.")
        for key, value in data.items():
            setattr(item, key, value.strip() if isinstance(value, str) else value)
        item.updated_at = datetime.now(timezone.utc)
        await self.activities.record(user_id, "cv.update", "Updated certification.")
        await self._commit()
        await self.session.refresh(item)
        return item

    async def delete(self, user_id: int, item_id: int) -> None:
        item = await self.repo.get_by_id_for_user(item_id, user_id)
        if item is None:
            raise ResourceNotFoundError("Certification not found.")
        await self.repo.delete(item)
        await self.activities.record(user_id, "cv.delete", "Deleted certification.")
        await self._commit()


class ProjectService(CVServiceBase):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = ProjectRepository(session)

    async def list(self, user_id: int):
        return await self.repo.list_for_user(user_id)

    async def create(self, user_id: int, *, title: str, description: str, role: str, technologies: str, project_date: date | None, project_url: str) -> Project:
        item = Project(user_id=user_id, title=title.strip(), description=description.strip(), role=role.strip(), technologies=technologies.strip(), project_date=project_date, project_url=project_url.strip())
        await self.repo.add(item)
        await self.activities.record(user_id, "cv.create", "Added project.")
        await self._commit()
        await self.session.refresh(item)
        return item

    async def update(self, user_id: int, item_id: int, **data) -> Project:
        item = await self.repo.get_by_id_for_user(item_id, user_id)
        if item is None:
            raise ResourceNotFoundError("Project not found.")
        for key, value in data.items():
            setattr(item, key, value.strip() if isinstance(value, str) else value)
        item.updated_at = datetime.now(timezone.utc)
        await self.activities.record(user_id, "cv.update", "Updated project.")
        await self._commit()
        await self.session.refresh(item)
        return item

    async def delete(self, user_id: int, item_id: int) -> None:
        item = await self.repo.get_by_id_for_user(item_id, user_id)
        if item is None:
            raise ResourceNotFoundError("Project not found.")
        await self.repo.delete(item)
        await self.activities.record(user_id, "cv.delete", "Deleted project.")
        await self._commit()
