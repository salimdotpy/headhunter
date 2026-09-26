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
from app.schemas.cv import EducationRequest
from app.services.cv import EducationService

router = APIRouter(prefix="/education", tags=["Education"])

@router.get("")
async def education_page(request: Request, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    records = await EducationService(session).list(current_user.id)
    return templates.TemplateResponse(request=request, name="education/index.html", context={"current_user": current_user, "records": records})

@router.get("/new")
async def education_new(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="education/form.html", context={"current_user": current_user, "record": None, "action": "/education/new"})

@router.post("/new")
async def education_create(request: Request, institution: str = Form(...), qualification: str = Form(...), field_of_study: str = Form(""), start_date: date | None = Form(None), end_date: date | None = Form(None), description: str = Form(""), csrf_token: str = Form(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    try:
        data = EducationRequest(institution=institution, qualification=qualification, field_of_study=field_of_study, start_date=start_date, end_date=end_date, description=description)
    except ValidationError:
        flash(request, "Please check the education information and try again.", "error")
        return RedirectResponse("/education/new", status_code=303)
    await EducationService(session).create(current_user.id, **data.model_dump())
    flash(request, "Education added successfully.", "success")
    return RedirectResponse("/education", status_code=303)

@router.get("/{item_id}/edit")
async def education_edit(request: Request, item_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    record = await EducationService(session).repo.get_by_id_for_user(item_id, current_user.id)
    if record is None:
        raise ResourceNotFoundError("Education record not found.")
    return templates.TemplateResponse(request=request, name="education/form.html", context={"current_user": current_user, "record": record, "action": f"/education/{item_id}/edit"})

@router.post("/{item_id}/edit")
async def education_update(request: Request, item_id: int, institution: str = Form(...), qualification: str = Form(...), field_of_study: str = Form(""), start_date: date | None = Form(None), end_date: date | None = Form(None), description: str = Form(""), csrf_token: str = Form(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    try:
        data = EducationRequest(institution=institution, qualification=qualification, field_of_study=field_of_study, start_date=start_date, end_date=end_date, description=description)
    except ValidationError:
        flash(request, "Please check the education information and try again.", "error")
        return RedirectResponse(f"/education/{item_id}/edit", status_code=303)
    try:
        await EducationService(session).update(current_user.id, item_id, **data.model_dump())
    except ResourceNotFoundError:
        raise
    flash(request, "Education updated successfully.", "success")
    return RedirectResponse("/education", status_code=303)

@router.post("/{item_id}/delete")
async def education_delete(request: Request, item_id: int, csrf_token: str = Form(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    await EducationService(session).delete(current_user.id, item_id)
    flash(request, "Education record deleted.", "success")
    return RedirectResponse("/education", status_code=303)
