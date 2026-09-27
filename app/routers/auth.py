from pydantic import ValidationError
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.csrf import validate_csrf_token
from app.core.database import get_session
from app.core.dependencies import get_current_user
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
    request.session["role"] = user.role

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
    request.session["role"] = user.role

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


@router.get("/forgot-password")
async def forgot_password_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/forgot_password.html",
    )


@router.post("/forgot-password")
async def forgot_password(
    request: Request,
    email: str = Form(...),
    csrf_token: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    validate_csrf_token(request, csrf_token)
    from app.services.password_reset import PasswordResetService
    await PasswordResetService(session).request_reset(email.strip().lower())
    flash(
        request,
        "If an active account uses that email, password reset instructions have been sent.",
        "success",
    )
    return RedirectResponse("/auth/login", status_code=303)


@router.get("/reset-password")
async def reset_password_page(request: Request, token: str = ""):
    return templates.TemplateResponse(
        request=request,
        name="auth/reset_password.html",
        context={"token": token},
    )


@router.post("/reset-password")
async def reset_password(
    request: Request,
    token: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    csrf_token: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    validate_csrf_token(request, csrf_token)
    try:
        from app.schemas.auth import PasswordResetConfirmRequest
        data = PasswordResetConfirmRequest(
            token=token,
            new_password=new_password,
            confirm_password=confirm_password,
        )
        from app.services.password_reset import PasswordResetService
        await PasswordResetService(session).reset_password(data.token, data.new_password)
    except ValidationError:
        flash(request, "Please check the password fields.", "error")
        return RedirectResponse(f"/auth/reset-password?token={token}", status_code=303)
    except AuthenticationError as exc:
        flash(request, str(exc), "error")
        return RedirectResponse("/auth/forgot-password", status_code=303)

    request.session.clear()
    flash(request, "Your password has been reset. Please sign in.", "success")
    return RedirectResponse("/auth/login", status_code=303)


@router.get("/change-password")
async def change_password_page(
    request: Request,
    current_user=Depends(get_current_user),
):
    return templates.TemplateResponse(
        request=request,
        name="auth/change_password.html",
        context={"current_user": current_user},
    )


@router.post("/change-password")
async def change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    csrf_token: str = Form(...),
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    validate_csrf_token(request, csrf_token)
    try:
        from app.schemas.auth import PasswordChangeRequest
        data = PasswordChangeRequest(
            current_password=current_password,
            new_password=new_password,
            confirm_password=confirm_password,
        )
        from app.services.password_reset import PasswordChangeService
        await PasswordChangeService(session).change_password(
            current_user.id, data.current_password, data.new_password
        )
    except ValidationError:
        flash(request, "Please check the password fields.", "error")
        return RedirectResponse("/auth/change-password", status_code=303)
    except AuthenticationError as exc:
        flash(request, str(exc), "error")
        return RedirectResponse("/auth/change-password", status_code=303)

    request.session.clear()
    flash(request, "Your password has been changed. Please sign in again.", "success")
    return RedirectResponse("/auth/login", status_code=303)
