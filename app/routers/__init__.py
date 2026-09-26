from fastapi import APIRouter

from app.routers.auth import router as auth_router
from app.routers.dashboard import router as dashboard_router
from app.routers.portfolio import router as portfolio_router
from app.routers.profile import router as profile_router


router = APIRouter()

router.include_router(auth_router)
router.include_router(dashboard_router)
router.include_router(profile_router)
router.include_router(portfolio_router)
