from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.csrf import validate_csrf_token
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.flash import flash
from app.core.config import BASE_DIR
from app.core.templates import templates
from app.exceptions.base import FileValidationError, ResourceNotFoundError
from app.models.user import User
from app.services.document import DocumentService
from app.services.file import ALLOWED_CATEGORIES

router = APIRouter(prefix="/documents", tags=["Documents"])


def _category_label(category: str) -> str:
    return category.replace("_", " ").title()


@router.get("")
async def documents_page(
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    records = await DocumentService(session).list(current_user.id)
    return templates.TemplateResponse(
        request=request,
        name="documents/index.html",
        context={
            "current_user": current_user,
            "records": records,
            "category_labels": {c: _category_label(c) for c in ALLOWED_CATEGORIES},
        },
    )


@router.get("/new")
async def documents_new(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        request=request,
        name="documents/form.html",
        context={
            "current_user": current_user,
            "categories": [(c, _category_label(c)) for c in sorted(ALLOWED_CATEGORIES)],
        },
    )


@router.post("/new")
async def documents_create(
    request: Request,
    category: str = Form(...),
    upload: UploadFile = File(...),
    certification_id: int | None = Form(None),
    project_id: int | None = Form(None),
    csrf_token: str = Form(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    validate_csrf_token(request, csrf_token)
    try:
        await DocumentService(session).create(
            current_user.id,
            upload,
            category=category,
            certification_id=certification_id,
            project_id=project_id,
        )
    except (FileValidationError, ResourceNotFoundError) as exc:
        flash(request, str(exc), "error")
        return RedirectResponse("/documents/new", status_code=303)
    flash(request, "Document uploaded successfully.", "success")
    return RedirectResponse("/documents", status_code=303)


@router.get("/{document_id}/download")
async def documents_download(
    document_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    document = await DocumentService(session).get(current_user.id, document_id)
    target = (BASE_DIR.parent / document.file_path).resolve()
    root = (BASE_DIR.parent / "uploads").resolve()
    if root not in target.parents or not target.is_file():
        raise ResourceNotFoundError("Document file not found.")
    return FileResponse(
        target,
        media_type=document.mime_type,
        filename=document.original_filename,
    )


@router.post("/{document_id}/delete")
async def documents_delete(
    request: Request,
    document_id: int,
    csrf_token: str = Form(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    validate_csrf_token(request, csrf_token)
    try:
        await DocumentService(session).delete(current_user.id, document_id)
    except ResourceNotFoundError:
        flash(request, "Document not found.", "error")
        return RedirectResponse("/documents", status_code=303)
    flash(request, "Document deleted.", "success")
    return RedirectResponse("/documents", status_code=303)
