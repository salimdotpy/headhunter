from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.csrf import validate_csrf_token
from app.core.database import get_session
from app.core.dependencies import get_current_admin
from app.core.flash import flash
from app.core.templates import templates
from app.models.user import User
from app.services.admin import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("")
async def admin_dashboard(request: Request, admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)):
    data = await AdminService(session).dashboard()
    return templates.TemplateResponse(request=request, name="admin/dashboard.html", context={"admin": admin, **data})

@router.get("/users")
async def admin_users(request: Request, search: str = "", status: str = "", admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)):
    users = await AdminService(session).users(search, status)
    return templates.TemplateResponse(request=request, name="admin/users.html", context={"admin": admin, "users": users, "search": search, "status": status})

@router.post("/users/{user_id}/status")
async def admin_user_status(request: Request, user_id: int, is_active: bool = Form(...), csrf_token: str = Form(...), admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    try:
        await AdminService(session).set_user_status(user_id, is_active, admin.id)
        flash(request, "Account status updated.", "success")
    except ValueError as exc:
        flash(request, str(exc), "error")
    return RedirectResponse("/admin/users", status_code=303)

@router.get("/portfolios")
async def admin_portfolios(request: Request, admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)):
    portfolios = await AdminService(session).portfolios()
    return templates.TemplateResponse(request=request, name="admin/portfolios.html", context={"admin": admin, "portfolios": portfolios})

@router.get("/activity")
async def admin_activity(request: Request, admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)):
    activities = await AdminService(session).activities()
    return templates.TemplateResponse(request=request, name="admin/activity.html", context={"admin": admin, "activities": activities})

@router.get("/content")
async def admin_content(request: Request, admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)):
    content = await AdminService(session).content()
    return templates.TemplateResponse(request=request, name="admin/content.html", context={"admin": admin, "content": content, "record": None})

@router.get("/content/new")
async def admin_content_new(request: Request, admin: User = Depends(get_current_admin)):
    return templates.TemplateResponse(request=request, name="admin/content_form.html", context={"admin": admin, "record": None, "action": "/admin/content/new"})

@router.post("/content/new")
async def admin_content_create(request: Request, key: str = Form(...), title: str = Form(""), body: str = Form(""), is_published: bool = Form(False), csrf_token: str = Form(...), admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    await AdminService(session).save_content(None, key, title, body, is_published)
    flash(request, "Website content saved.", "success")
    return RedirectResponse("/admin/content", status_code=303)

@router.get("/content/{content_id}/edit")
async def admin_content_edit(request: Request, content_id: int, admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)):
    record = await AdminService(session).repo.get_content(content_id)
    if record is None:
        return RedirectResponse("/admin/content", status_code=303)
    return templates.TemplateResponse(request=request, name="admin/content_form.html", context={"admin": admin, "record": record, "action": f"/admin/content/{content_id}/edit"})

@router.post("/content/{content_id}/edit")
async def admin_content_update(request: Request, content_id: int, key: str = Form(...), title: str = Form(""), body: str = Form(""), is_published: bool = Form(False), csrf_token: str = Form(...), admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    await AdminService(session).save_content(content_id, key, title, body, is_published)
    flash(request, "Website content updated.", "success")
    return RedirectResponse("/admin/content", status_code=303)

@router.get("/settings")
async def admin_settings(request: Request, admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)):
    settings = await AdminService(session).settings()
    return templates.TemplateResponse(request=request, name="admin/settings.html", context={"admin": admin, "settings": settings})

@router.post("/settings")
async def admin_setting_create(request: Request, key: str = Form(...), value: str = Form(""), csrf_token: str = Form(...), admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    await AdminService(session).save_setting(None, key, value)
    flash(request, "Setting saved.", "success")
    return RedirectResponse("/admin/settings", status_code=303)

@router.post("/settings/{setting_id}")
async def admin_setting_update(request: Request, setting_id: int, key: str = Form(...), value: str = Form(""), csrf_token: str = Form(...), admin: User = Depends(get_current_admin), session: AsyncSession = Depends(get_session)):
    validate_csrf_token(request, csrf_token)
    await AdminService(session).save_setting(setting_id, key, value)
    flash(request, "Setting updated.", "success")
    return RedirectResponse("/admin/settings", status_code=303)
