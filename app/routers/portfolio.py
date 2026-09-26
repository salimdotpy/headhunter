from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import BASE_DIR
from app.core.csrf import validate_csrf_token
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.flash import flash
from app.core.templates import templates
from app.exceptions.base import ResourceNotFoundError
from app.exceptions.portfolio import PortfolioSlugAlreadyExistsError
from app.models.user import User
from app.schemas.portfolio import PortfolioSlugUpdateRequest
from app.services.portfolio import PortfolioService

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


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
        context={"current_user": current_user, "portfolio": portfolio},
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
        flash(request, "Portfolio URLs may contain only lowercase letters, numbers, and hyphens.", "error")
        return RedirectResponse(url="/portfolio/settings", status_code=303)

    try:
        await PortfolioService(session).update_slug(current_user.id, data.slug)
    except PortfolioSlugAlreadyExistsError:
        flash(request, "That portfolio URL is already in use.", "error")
        return RedirectResponse(url="/portfolio/settings", status_code=303)

    flash(request, "Your portfolio URL has been updated.", "success")
    return RedirectResponse(url="/portfolio/settings", status_code=303)


@router.get("/preview")
async def portfolio_preview(
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    data = await PortfolioService(session).get_preview(current_user.id)
    return templates.TemplateResponse(
        request=request,
        name="portfolio/preview.html",
        context=data | {"is_preview": True},
    )


@router.post("/publish")
async def publish_portfolio(
    request: Request,
    csrf_token: str = Form(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    validate_csrf_token(request, csrf_token)
    await PortfolioService(session).set_published(current_user.id, True)
    flash(request, "Your portfolio has been published.", "success")
    return RedirectResponse(url="/portfolio/settings", status_code=303)


@router.post("/unpublish")
async def unpublish_portfolio(
    request: Request,
    csrf_token: str = Form(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    validate_csrf_token(request, csrf_token)
    await PortfolioService(session).set_published(current_user.id, False)
    flash(request, "Your portfolio is no longer public.", "success")
    return RedirectResponse(url="/portfolio/settings", status_code=303)


@router.get("/preview/photo")
async def preview_photo(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        relative_path = await PortfolioService(session).get_preview_photo(current_user.id)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Photo not found.") from exc
    path = BASE_DIR.parent / relative_path
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Photo not found.")
    return FileResponse(path)


@router.get("/{slug}/photo")
async def public_photo(
    slug: str,
    session: AsyncSession = Depends(get_session),
):
    try:
        relative_path = await PortfolioService(session).get_public_photo(slug)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Photo not found.") from exc
    path = BASE_DIR.parent / relative_path
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Photo not found.")
    return FileResponse(path)


@router.get("/{slug}/documents/{document_id}")
async def public_document(
    slug: str,
    document_id: int,
    session: AsyncSession = Depends(get_session),
):
    try:
        document = await PortfolioService(session).get_public_document(slug, document_id)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Document not found.") from exc

    path = BASE_DIR.parent / document.file_path
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Document not found.")

    return FileResponse(
        path=path,
        media_type=document.mime_type,
        filename=document.original_filename,
    )


@router.get("/{slug}")
async def public_portfolio(
    request: Request,
    slug: str,
    session: AsyncSession = Depends(get_session),
):
    try:
        data = await PortfolioService(session).get_public_by_slug(slug)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Portfolio not found.") from exc

    return templates.TemplateResponse(
        request=request,
        name="portfolio/public.html",
        context=data | {"is_preview": False},
    )
