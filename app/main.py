
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles # Import StaticFiles

from app.core.config import get_settings, BASE_DIR
from app.exceptions.handler import authentication_exception_handler, authorization_exception_handler
from app.exceptions.auth import AuthenticationError
from app.exceptions.base import AuthorizationError
from app.core.templates import templates
from app.routers import router



settings = get_settings()

app = FastAPI(
    title="Headhunter",
    description=(
        "CV Portfolio Creation, Management, "
        "Presentation and Sharing System"
    ),
    version="0.1.0",
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie="headhunter_session",
    max_age=60 * 60 * 24,
    same_site="lax",
    https_only=settings.app_env == "production",
)

app.add_exception_handler(
    AuthenticationError,
    authentication_exception_handler,
)
app.add_exception_handler(
    AuthorizationError,
    authorization_exception_handler,
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(router)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"title": "Headhunter"},
    )

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={"title": "About — Headhunter"},
    )
