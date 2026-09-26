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
from app.schemas.cv import CertificationRequest
from app.services.cv import CertificationService

router = APIRouter(prefix="/certifications", tags=["Certifications"])

@router.get("")
async def certifications_page(request: Request, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    records = await CertificationService(session).list(current_user.id)
    return templates.TemplateResponse(request=request, name="certifications/index.html", context={"current_user": current_user, "records": records})

@router.get("/new")
async def certifications_new(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="certifications/form.html", context={"current_user": current_user, "record": None, "action": "/certifications/new"})

@router.post("/new")
async def certifications_create(request: Request, name: str = Form(...), issuer: str = Form(...), issue_date: date | None = Form(None), expiry_date: date | None = Form(None), credential_reference: str = Form(""), csrf_token: str = Form(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    try:
        data = CertificationRequest(name=name, issuer=issuer, issue_date=issue_date, expiry_date=expiry_date, credential_reference=credential_reference)
    except ValidationError:
        flash(request, "Please check the certification information and try again.", "error")
        return RedirectResponse("/certifications/new", status_code=303)
    await CertificationService(session).create(current_user.id, **data.model_dump())
    flash(request, "Certification added successfully.", "success")
    return RedirectResponse("/certifications", status_code=303)

@router.get("/{item_id}/edit")
async def certifications_edit(request: Request, item_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    record = await CertificationService(session).repo.get_by_id_for_user(item_id, current_user.id)
    if record is None:
        raise ResourceNotFoundError("Certification not found.")
    return templates.TemplateResponse(request=request, name="certifications/form.html", context={"current_user": current_user, "record": record, "action": f"/certifications/{item_id}/edit"})

@router.post("/{item_id}/edit")
async def certifications_update(request: Request, item_id: int, name: str = Form(...), issuer: str = Form(...), issue_date: date | None = Form(None), expiry_date: date | None = Form(None), credential_reference: str = Form(""), csrf_token: str = Form(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    try:
        data = CertificationRequest(name=name, issuer=issuer, issue_date=issue_date, expiry_date=expiry_date, credential_reference=credential_reference)
    except ValidationError:
        flash(request, "Please check the certification information and try again.", "error")
        return RedirectResponse(f"/certifications/{item_id}/edit", status_code=303)
    await CertificationService(session).update(current_user.id, item_id, **data.model_dump())
    flash(request, "Certification updated successfully.", "success")
    return RedirectResponse("/certifications", status_code=303)

@router.post("/{item_id}/delete")
async def certifications_delete(request: Request, item_id: int, csrf_token: str = Form(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    await CertificationService(session).delete(current_user.id, item_id)
    flash(request, "Certification deleted.", "success")
    return RedirectResponse("/certifications", status_code=303)
