from fastapi import APIRouter

from app.routers.auth import router as auth_router
from app.routers.admin import router as admin_router
from app.routers.certifications import router as certifications_router
from app.routers.dashboard import router as dashboard_router
from app.routers.documents import router as documents_router
from app.routers.education import router as education_router
from app.routers.experience import router as experience_router
from app.routers.portfolio import router as portfolio_router
from app.routers.profile import router as profile_router
from app.routers.projects import router as projects_router
from app.routers.skills import router as skills_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(admin_router)
router.include_router(dashboard_router)
router.include_router(documents_router)
router.include_router(profile_router)
router.include_router(portfolio_router)
router.include_router(education_router)
router.include_router(experience_router)
router.include_router(skills_router)
router.include_router(certifications_router)
router.include_router(projects_router)
