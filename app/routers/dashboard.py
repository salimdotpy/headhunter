from fastapi import APIRouter, Depends, Request

from app.core.dependencies import get_current_user
from app.core.templates import templates
from app.models.user import User
from app.services.dashboard import DashboardService
from app.core.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession


router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard")
async def dashboard(
    request: Request,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    data = await DashboardService(session).get_dashboard(current_user.id)
    return templates.TemplateResponse(
        request=request,
        name="dashboard/index.html",
        context={"current_user": current_user, **data},
    )
