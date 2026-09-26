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
from app.schemas.cv import ProjectRequest
from app.services.cv import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("")
async def projects_page(request: Request, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    records = await ProjectService(session).list(current_user.id)
    return templates.TemplateResponse(request=request, name="projects/index.html", context={"current_user": current_user, "records": records})

@router.get("/new")
async def projects_new(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="projects/form.html", context={"current_user": current_user, "record": None, "action": "/projects/new"})

@router.post("/new")
async def projects_create(request: Request, title: str = Form(...), description: str = Form(""), role: str = Form(""), technologies: str = Form(""), project_date: date | None = Form(None), project_url: str = Form(""), csrf_token: str = Form(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    try:
        data = ProjectRequest(title=title, description=description, role=role, technologies=technologies, project_date=project_date, project_url=project_url or None)
    except ValidationError:
        flash(request, "Please check the project information and try again.", "error")
        return RedirectResponse("/projects/new", status_code=303)
    payload = data.model_dump()
    payload["project_url"] = str(data.project_url) if data.project_url else ""
    await ProjectService(session).create(current_user.id, **payload)
    flash(request, "Project added successfully.", "success")
    return RedirectResponse("/projects", status_code=303)

@router.get("/{item_id}/edit")
async def projects_edit(request: Request, item_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    record = await ProjectService(session).repo.get_by_id_for_user(item_id, current_user.id)
    if record is None:
        raise ResourceNotFoundError("Project not found.")
    return templates.TemplateResponse(request=request, name="projects/form.html", context={"current_user": current_user, "record": record, "action": f"/projects/{item_id}/edit"})

@router.post("/{item_id}/edit")
async def projects_update(request: Request, item_id: int, title: str = Form(...), description: str = Form(""), role: str = Form(""), technologies: str = Form(""), project_date: date | None = Form(None), project_url: str = Form(""), csrf_token: str = Form(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    try:
        data = ProjectRequest(title=title, description=description, role=role, technologies=technologies, project_date=project_date, project_url=project_url or None)
    except ValidationError:
        flash(request, "Please check the project information and try again.", "error")
        return RedirectResponse(f"/projects/{item_id}/edit", status_code=303)
    payload = data.model_dump()
    payload["project_url"] = str(data.project_url) if data.project_url else ""
    await ProjectService(session).update(current_user.id, item_id, **payload)
    flash(request, "Project updated successfully.", "success")
    return RedirectResponse("/projects", status_code=303)

@router.post("/{item_id}/delete")
async def projects_delete(request: Request, item_id: int, csrf_token: str = Form(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    await ProjectService(session).delete(current_user.id, item_id)
    flash(request, "Project deleted.", "success")
    return RedirectResponse("/projects", status_code=303)
