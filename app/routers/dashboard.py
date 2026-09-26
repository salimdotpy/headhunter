from pathlib import Path

from fastapi import APIRouter, Depends, Request

from app.core.dependencies import get_current_user
from app.core.templates import templates
from app.models.user import User


router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard")
async def dashboard(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        request=request,
        name="dashboard/index.html",
        context={
            "current_user": current_user,
        },
    )