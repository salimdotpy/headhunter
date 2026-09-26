from sqlmodel.ext.asyncio.session import AsyncSession

from app.exceptions.base import ResourceNotFoundError
from app.models.document import Document
from app.repositories.document import DocumentRepository
from app.repositories.cv import CertificationRepository, ProjectRepository
from app.services.file import delete_stored_file, save_upload
from app.services.activity import ActivityService


class DocumentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = DocumentRepository(session)
        self.certifications = CertificationRepository(session)
        self.projects = ProjectRepository(session)
        self.activities = ActivityService(session)

    async def list(self, user_id: int) -> list[Document]:
        return await self.repo.list_for_user(user_id)

    async def get(self, user_id: int, document_id: int) -> Document:
        document = await self.repo.get_by_id_for_user(document_id, user_id)
        if document is None:
            raise ResourceNotFoundError("Document not found.")
        return document

    async def create(
        self,
        user_id: int,
        upload,
        *,
        category: str,
        certification_id: int | None = None,
        project_id: int | None = None,
    ) -> Document:
        if certification_id is not None:
            certification = await self.certifications.get_by_id_for_user(certification_id, user_id)
            if certification is None:
                raise ResourceNotFoundError("Certification not found.")

        if project_id is not None:
            project = await self.projects.get_by_id_for_user(project_id, user_id)
            if project is None:
                raise ResourceNotFoundError("Project not found.")

        (
            original_filename,
            stored_filename,
            file_size,
            relative_path,
        ) = await save_upload(upload, category)

        document = Document(
            user_id=user_id,
            certification_id=certification_id,
            project_id=project_id,
            category=category,
            original_filename=original_filename,
            stored_filename=stored_filename,
            file_path=relative_path,
            mime_type=upload.content_type or "application/octet-stream",
            file_size=file_size,
        )
        await self.repo.add(document)
        await self.activities.record(user_id, "document.upload", f"Uploaded {original_filename}.")
        try:
            await self.session.commit()
            await self.session.refresh(document)
        except Exception:
            await self.session.rollback()
            delete_stored_file(relative_path)
            raise
        return document

    async def delete(self, user_id: int, document_id: int) -> None:
        document = await self.get(user_id, document_id)
        relative_path = document.file_path
        await self.repo.delete(document)
        await self.activities.record(user_id, "document.delete", f"Deleted {document.original_filename}.")
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        delete_stored_file(relative_path)
