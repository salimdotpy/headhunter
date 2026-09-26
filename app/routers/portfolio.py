from pydantic import ValidationError
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from app.core.csrf import validate_csrf_token
from app.core.dependencies import get_current_user
from app.core.flash import flash
from app.core.templates import templates
from app.models.user import User
from app.schemas.portfolio import PortfolioSlugUpdateRequest
from app.services.portfolio import PortfolioService
from app.exceptions.portfolio import PortfolioSlugAlreadyExistsError
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session


router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"],
)


@router.get("/settings")
async def portfolio_settings(
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    portfolio = await PortfolioService(session).get_by_user_id(current_user.id)
    return templates.TemplateResponse(
        request=request,
        name="portfolio/settings.html",
        context={
            "current_user": current_user,
            "portfolio": portfolio,
        },
    )


@router.post("/settings")
async def update_portfolio_settings(
    request: Request,
    slug: str = Form(...),
    csrf_token: str = Form(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    validate_csrf_token(request, csrf_token)

    try:
        data = PortfolioSlugUpdateRequest(slug=slug)
    except ValidationError:
        flash(
            request,
            "Portfolio URLs may contain only lowercase letters, numbers, and hyphens.",
            "error",
        )
        return RedirectResponse(url="/portfolio/settings", status_code=303)

    try:
        await PortfolioService(session).update_slug(
            current_user.id,
            data.slug,
        )
    except PortfolioSlugAlreadyExistsError:
        flash(request, "That portfolio URL is already in use.", "error")
        return RedirectResponse(url="/portfolio/settings", status_code=303)

    flash(request, "Your portfolio URL has been updated.", "success")
    return RedirectResponse(url="/portfolio/settings", status_code=303)
