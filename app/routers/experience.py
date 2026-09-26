from datetime import date
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.csrf import validate_csrf_token
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.flash import flash
from app.core.templates import templates
from app.exceptions.base import ResourceNotFoundError
from app.models.user import User
from app.schemas.cv import ExperienceRequest
from app.services.cv import ExperienceService

router = APIRouter(prefix="/experience", tags=["Experience"])

@router.get("")
async def experience_page(request: Request, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    records = await ExperienceService(session).list(current_user.id)
    return templates.TemplateResponse(request=request, name="experience/index.html", context={"current_user": current_user, "records": records})

@router.get("/new")
async def experience_new(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="experience/form.html", context={"current_user": current_user, "record": None, "action": "/experience/new"})

@router.post("/new")
async def experience_create(request: Request, job_title: str = Form(...), company: str = Form(...), location: str = Form(""), start_date: date | None = Form(None), end_date: date | None = Form(None), description: str = Form(""), is_current: bool = Form(False), csrf_token: str = Form(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    try:
        data = ExperienceRequest(job_title=job_title, company=company, location=location, start_date=start_date, end_date=end_date, description=description, is_current=is_current)
    except ValidationError:
        flash(request, "Please check the work experience information and try again.", "error")
        return RedirectResponse("/experience/new", status_code=303)
    await ExperienceService(session).create(current_user.id, **data.model_dump())
    flash(request, "Work experience added successfully.", "success")
    return RedirectResponse("/experience", status_code=303)

@router.get("/{item_id}/edit")
async def experience_edit(request: Request, item_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    record = await ExperienceService(session).repo.get_by_id_for_user(item_id, current_user.id)
    if record is None:
        raise ResourceNotFoundError("Work experience record not found.")
    return templates.TemplateResponse(request=request, name="experience/form.html", context={"current_user": current_user, "record": record, "action": f"/experience/{item_id}/edit"})

@router.post("/{item_id}/edit")
async def experience_update(request: Request, item_id: int, job_title: str = Form(...), company: str = Form(...), location: str = Form(""), start_date: date | None = Form(None), end_date: date | None = Form(None), description: str = Form(""), is_current: bool = Form(False), csrf_token: str = Form(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    try:
        data = ExperienceRequest(job_title=job_title, company=company, location=location, start_date=start_date, end_date=end_date, description=description, is_current=is_current)
    except ValidationError:
        flash(request, "Please check the work experience information and try again.", "error")
        return RedirectResponse(f"/experience/{item_id}/edit", status_code=303)
    await ExperienceService(session).update(current_user.id, item_id, **data.model_dump())
    flash(request, "Work experience updated successfully.", "success")
    return RedirectResponse("/experience", status_code=303)

@router.post("/{item_id}/delete")
async def experience_delete(request: Request, item_id: int, csrf_token: str = Form(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    await ExperienceService(session).delete(current_user.id, item_id)
    flash(request, "Work experience deleted.", "success")
    return RedirectResponse("/experience", status_code=303)
