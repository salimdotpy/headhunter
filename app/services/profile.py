from datetime import datetime, timezone

from sqlmodel.ext.asyncio.session import AsyncSession

from app.exceptions.base import ResourceNotFoundError
from app.models.profile import Profile
from app.repositories.profile import ProfileRepository


class ProfileService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.profiles = ProfileRepository(session)

    async def get_by_user_id(self, user_id: int) -> Profile:
        profile = await self.profiles.get_by_user_id(user_id)
        if profile is None:
            raise ResourceNotFoundError("Profile not found.")
        return profile

    async def update(
        self,
        user_id: int,
        *,
        full_name: str,
        professional_title: str,
        summary: str,
        phone: str,
        show_email: bool,
        show_phone: bool,
        location: str,
        show_location: bool,
        website_url: str,
        show_website: bool,
        linkedin_url: str,
        show_linkedin: bool,
        github_url: str,
        show_github: bool,
    ) -> Profile:
        profile = await self.get_by_user_id(user_id)

        profile.full_name = full_name.strip()
        profile.professional_title = professional_title.strip()
        profile.summary = summary.strip()
        profile.phone = phone.strip()
        profile.show_email = show_email
        profile.show_phone = show_phone
        profile.location = location.strip()
        profile.show_location = show_location
        profile.website_url = website_url.strip()
        profile.show_website = show_website
        profile.linkedin_url = linkedin_url.strip()
        profile.show_linkedin = show_linkedin
        profile.github_url = github_url.strip()
        profile.show_github = show_github
        profile.updated_at = datetime.now(timezone.utc)

        try:
            await self.session.commit()
            await self.session.refresh(profile)
        except Exception:
            await self.session.rollback()
            raise

        return profile
