import re
import unicodedata
from datetime import datetime, timezone

from sqlmodel.ext.asyncio.session import AsyncSession

from app.exceptions.base import ResourceNotFoundError
from app.exceptions.portfolio import PortfolioSlugAlreadyExistsError
from app.models.portfolio import Portfolio
from app.repositories.cv import (
    CertificationRepository,
    EducationRepository,
    ExperienceRepository,
    ProjectRepository,
    SkillRepository,
)
from app.repositories.document import DocumentRepository
from app.repositories.portfolio import PortfolioRepository
from app.repositories.profile import ProfileRepository
from app.repositories.user import UserRepository


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return slug or "portfolio"


class PortfolioService:
    PUBLIC_DOCUMENT_CATEGORIES = {
        "certificate",
        "project_document",
        "professional_credential",
        "portfolio_file",
    }

    def __init__(self, session: AsyncSession):
        self.session = session
        self.portfolios = PortfolioRepository(session)
        self.profiles = ProfileRepository(session)
        self.users = UserRepository(session)
        self.education = EducationRepository(session)
        self.experience = ExperienceRepository(session)
        self.skills = SkillRepository(session)
        self.certifications = CertificationRepository(session)
        self.projects = ProjectRepository(session)
        self.documents = DocumentRepository(session)

    async def get_by_user_id(self, user_id: int) -> Portfolio:
        portfolio = await self.portfolios.get_by_user_id(user_id)
        if portfolio is None:
            raise ResourceNotFoundError("Portfolio not found.")
        return portfolio

    async def generate_unique_slug(self, base_value: str) -> str:
        base_slug = slugify(base_value)[:90].rstrip("-")
        candidate = base_slug or "portfolio"
        counter = 2

        while await self.portfolios.slug_exists(candidate):
            suffix = f"-{counter}"
            candidate = f"{base_slug[:100 - len(suffix)]}{suffix}"
            counter += 1

        return candidate

    async def update_slug(self, user_id: int, slug: str) -> Portfolio:
        portfolio = await self.get_by_user_id(user_id)
        normalized_slug = slug.strip().lower()

        existing = await self.portfolios.get_by_slug(normalized_slug)
        if existing is not None and existing.id != portfolio.id:
            raise PortfolioSlugAlreadyExistsError(
                "That portfolio URL is already in use."
            )

        portfolio.slug = normalized_slug
        portfolio.updated_at = datetime.now(timezone.utc)

        try:
            await self.session.commit()
            await self.session.refresh(portfolio)
        except Exception:
            await self.session.rollback()
            raise

        return portfolio

    async def set_published(self, user_id: int, published: bool) -> Portfolio:
        portfolio = await self.get_by_user_id(user_id)
        portfolio.is_published = published
        portfolio.updated_at = datetime.now(timezone.utc)

        try:
            await self.session.commit()
            await self.session.refresh(portfolio)
        except Exception:
            await self.session.rollback()
            raise

        return portfolio

    async def get_preview(self, user_id: int) -> dict:
        portfolio = await self.get_by_user_id(user_id)
        return await self._build_portfolio_data(portfolio, include_private=True)

    async def get_public_by_slug(self, slug: str) -> dict:
        portfolio = await self.portfolios.get_by_slug(slug.strip().lower())
        if portfolio is None or not portfolio.is_published:
            raise ResourceNotFoundError("Portfolio not found.")

        user = await self.users.get_by_id(portfolio.user_id)
        if user is None or not user.is_active:
            raise ResourceNotFoundError("Portfolio not found.")

        return await self._build_portfolio_data(portfolio, include_private=False)

    async def get_preview_photo(self, user_id: int):
        portfolio = await self.get_by_user_id(user_id)
        profile = await self.profiles.get_by_user_id(user_id)
        if profile is None or not profile.profile_photo_path:
            raise ResourceNotFoundError("Photo not found.")
        return profile.profile_photo_path

    async def get_public_photo(self, slug: str):
        portfolio = await self.portfolios.get_by_slug(slug.strip().lower())
        if portfolio is None or not portfolio.is_published:
            raise ResourceNotFoundError("Photo not found.")
        user = await self.users.get_by_id(portfolio.user_id)
        if user is None or not user.is_active:
            raise ResourceNotFoundError("Photo not found.")
        profile = await self.profiles.get_by_user_id(portfolio.user_id)
        if profile is None or not profile.profile_photo_path:
            raise ResourceNotFoundError("Photo not found.")
        return profile.profile_photo_path

    async def get_public_document(self, slug: str, document_id: int):
        portfolio = await self.portfolios.get_by_slug(slug.strip().lower())
        if portfolio is None or not portfolio.is_published:
            raise ResourceNotFoundError("Document not found.")

        user = await self.users.get_by_id(portfolio.user_id)
        if user is None or not user.is_active:
            raise ResourceNotFoundError("Document not found.")

        document = await self.documents.get_by_id_for_user(document_id, portfolio.user_id)
        if document is None or document.category not in self.PUBLIC_DOCUMENT_CATEGORIES:
            raise ResourceNotFoundError("Document not found.")

        return document

    async def _build_portfolio_data(
        self,
        portfolio: Portfolio,
        *,
        include_private: bool,
    ) -> dict:
        user = await self.users.get_by_id(portfolio.user_id)
        profile = await self.profiles.get_by_user_id(portfolio.user_id)

        if user is None or profile is None:
            raise ResourceNotFoundError("Portfolio data is incomplete.")

        education = await self.education.list_for_user(portfolio.user_id)
        experience = await self.experience.list_for_user(portfolio.user_id)
        skills = await self.skills.list_for_user(portfolio.user_id)
        certifications = await self.certifications.list_for_user(portfolio.user_id)
        projects = await self.projects.list_for_user(portfolio.user_id)
        documents = await self.documents.list_for_user(portfolio.user_id)

        contacts = [
            ("Email", user.email, include_private or profile.show_email),
            ("Phone", profile.phone, include_private or profile.show_phone),
            ("Location", profile.location, include_private or profile.show_location),
            ("Website", profile.website_url, include_private or profile.show_website),
            ("LinkedIn", profile.linkedin_url, include_private or profile.show_linkedin),
            ("GitHub", profile.github_url, include_private or profile.show_github),
        ]

        public_profile = {
            "full_name": profile.full_name,
            "professional_title": profile.professional_title,
            "summary": profile.summary,
            "profile_photo_path": profile.profile_photo_path,
            "contacts": contacts,
        }

        public_documents = (
            documents
            if include_private
            else [
                document
                for document in documents
                if document.category in self.PUBLIC_DOCUMENT_CATEGORIES
            ]
        )

        return {
            "portfolio": portfolio,
            "user": user,
            "profile": public_profile,
            "education": education,
            "experience": experience,
            "skills": skills,
            "certifications": certifications,
            "projects": projects,
            "documents": public_documents,
            "include_private": include_private,
            "photo_url": (
                f"/portfolio/preview/photo"
                if include_private and profile.profile_photo_path
                else f"/portfolio/{portfolio.slug}/photo"
                if profile.profile_photo_path
                else None
            ),
        }
