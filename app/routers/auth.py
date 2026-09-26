from pydantic import ValidationError
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.csrf import validate_csrf_token
from app.core.database import get_session
from app.core.flash import flash
from app.core.templates import templates
from app.exceptions.auth import AuthenticationError
from app.exceptions.users import ResourceAlreadyExistsError
from app.schemas.auth import RegisterRequest
from app.services.auth import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/register.html",
    )


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
    )


@router.post("/register")
async def register(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    csrf_token: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    validate_csrf_token(request, csrf_token)

    try:
        data = RegisterRequest(
            full_name=full_name,
            email=email.strip().lower(),
            password=password,
            confirm_password=confirm_password,
        )
    except ValidationError as exc:
        message = "Please check your registration details."
        if any(
            "Passwords do not match." in error.get("msg", "")
            for error in exc.errors()
        ):
            message = "Passwords do not match."

        flash(request, message, "error")
        return RedirectResponse(
            url="/auth/register",
            status_code=303,
        )

    auth_service = AuthService(session)

    try:
        user = await auth_service.register(
            full_name=data.full_name,
            email=data.email,
            password=data.password,
        )
    except ResourceAlreadyExistsError:
        flash(
            request,
            "An account with that email already exists.",
            "error",
        )
        return RedirectResponse(
            url="/auth/register",
            status_code=303,
        )

    request.session["user_id"] = user.id

    flash(
        request,
        "Your account has been created successfully.",
        "success",
    )

    return RedirectResponse(
        url="/dashboard",
        status_code=303,
    )


@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    csrf_token: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    validate_csrf_token(request, csrf_token)
    auth_service = AuthService(session)

    try:
        user = await auth_service.authenticate(
            email=email.strip().lower(),
            password=password,
        )
    except AuthenticationError:
        flash(
            request,
            "Invalid email or password.",
            "error",
        )
        return RedirectResponse(
            url="/auth/login",
            status_code=303,
        )

    request.session["user_id"] = user.id

    flash(
        request,
        "Welcome back.",
        "success",
    )

    return RedirectResponse(
        url="/dashboard",
        status_code=303,
    )


@router.post("/logout")
async def logout(
    request: Request,
    csrf_token: str = Form(...),
):
    validate_csrf_token(request, csrf_token)
    request.session.clear()

    flash(
        request,
        "You have been logged out.",
        "success",
    )

    return RedirectResponse(
        url="/auth/login",
        status_code=303,
    )
