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
from app.schemas.cv import SkillRequest
from app.services.cv import SkillService

router = APIRouter(prefix="/skills", tags=["Skills"])

@router.get("")
async def skills_page(request: Request, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    records = await SkillService(session).list(current_user.id)
    return templates.TemplateResponse(request=request, name="skills/index.html", context={"current_user": current_user, "records": records})

@router.get("/new")
async def skills_new(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="skills/form.html", context={"current_user": current_user, "record": None, "action": "/skills/new"})

@router.post("/new")
async def skills_create(request: Request, name: str = Form(...), proficiency: str = Form(""), csrf_token: str = Form(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    try:
        data = SkillRequest(name=name, proficiency=proficiency)
    except ValidationError:
        flash(request, "Please check the skill information and try again.", "error")
        return RedirectResponse("/skills/new", status_code=303)
    await SkillService(session).create(current_user.id, **data.model_dump())
    flash(request, "Skill added successfully.", "success")
    return RedirectResponse("/skills", status_code=303)

@router.get("/{item_id}/edit")
async def skills_edit(request: Request, item_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    record = await SkillService(session).repo.get_by_id_for_user(item_id, current_user.id)
    if record is None:
        raise ResourceNotFoundError("Skill not found.")
    return templates.TemplateResponse(request=request, name="skills/form.html", context={"current_user": current_user, "record": record, "action": f"/skills/{item_id}/edit"})

@router.post("/{item_id}/edit")
async def skills_update(request: Request, item_id: int, name: str = Form(...), proficiency: str = Form(""), csrf_token: str = Form(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    try:
        data = SkillRequest(name=name, proficiency=proficiency)
    except ValidationError:
        flash(request, "Please check the skill information and try again.", "error")
        return RedirectResponse(f"/skills/{item_id}/edit", status_code=303)
    await SkillService(session).update(current_user.id, item_id, **data.model_dump())
    flash(request, "Skill updated successfully.", "success")
    return RedirectResponse("/skills", status_code=303)

@router.post("/{item_id}/delete")
async def skills_delete(request: Request, item_id: int, csrf_token: str = Form(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    await SkillService(session).delete(current_user.id, item_id)
    flash(request, "Skill deleted.", "success")
    return RedirectResponse("/skills", status_code=303)
