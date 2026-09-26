from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.document import Document


class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_for_user(self, user_id: int) -> list[Document]:
        statement = (
            select(Document)
            .where(Document.user_id == user_id)
            .order_by(Document.created_at.desc())
        )
        result = await self.session.exec(statement)
        return list(result.all())

    async def get_by_id_for_user(self, document_id: int, user_id: int) -> Document | None:
        statement = select(Document).where(
            Document.id == document_id,
            Document.user_id == user_id,
        )
        result = await self.session.exec(statement)
        return result.first()

    async def add(self, document: Document) -> Document:
        self.session.add(document)
        return document

    async def delete(self, document: Document) -> None:
        await self.session.delete(document)
