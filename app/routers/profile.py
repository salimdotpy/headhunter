from pydantic import ValidationError
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from app.core.csrf import validate_csrf_token
from app.core.dependencies import get_current_user
from app.core.flash import flash
from app.core.templates import templates
from app.models.user import User
from app.schemas.profile import ProfileUpdateRequest
from app.services.profile import ProfileService
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session


router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


@router.get("/edit")
async def edit_profile(
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    profile = await ProfileService(session).get_by_user_id(current_user.id)
    return templates.TemplateResponse(
        request=request,
        name="profile/edit.html",
        context={
            "current_user": current_user,
            "profile": profile,
        },
    )


@router.post("/edit")
async def update_profile(
    request: Request,
    full_name: str = Form(...),
    professional_title: str = Form(""),
    summary: str = Form(""),
    phone: str = Form(""),
    show_email: bool = Form(False),
    show_phone: bool = Form(False),
    location: str = Form(""),
    show_location: bool = Form(False),
    website_url: str = Form(""),
    show_website: bool = Form(False),
    linkedin_url: str = Form(""),
    show_linkedin: bool = Form(False),
    github_url: str = Form(""),
    show_github: bool = Form(False),
    csrf_token: str = Form(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    validate_csrf_token(request, csrf_token)

    try:
        data = ProfileUpdateRequest(
            full_name=full_name,
            professional_title=professional_title,
            summary=summary,
            phone=phone,
            show_email=show_email,
            show_phone=show_phone,
            location=location,
            show_location=show_location,
            website_url=website_url or None,
            show_website=show_website,
            linkedin_url=linkedin_url or None,
            show_linkedin=show_linkedin,
            github_url=github_url or None,
            show_github=show_github,
        )
    except ValidationError:
        flash(
            request,
            "Please check your profile information and try again.",
            "error",
        )
        return RedirectResponse(url="/profile/edit", status_code=303)

    profile = await ProfileService(session).update(
        current_user.id,
        full_name=data.full_name,
        professional_title=data.professional_title,
        summary=data.summary,
        phone=data.phone,
        show_email=data.show_email,
        show_phone=data.show_phone,
        location=data.location,
        show_location=data.show_location,
        website_url=str(data.website_url) if data.website_url else "",
        show_website=data.show_website,
        linkedin_url=str(data.linkedin_url) if data.linkedin_url else "",
        show_linkedin=data.show_linkedin,
        github_url=str(data.github_url) if data.github_url else "",
        show_github=data.show_github,
    )

    flash(request, "Your profile has been updated.", "success")
    return RedirectResponse(url="/profile/edit", status_code=303)
