from fastapi import Request
from fastapi.responses import RedirectResponse

from app.core.flash import flash
from app.exceptions.auth import AuthenticationError


async def authentication_exception_handler(
    request: Request,
    exc: AuthenticationError,
):
    flash(
        request,
        "Please sign in to continue.",
        "warning",
    )

    return RedirectResponse(
        url="/auth/login",
        status_code=303,
    )

from app.exceptions.base import AuthorizationError

async def authorization_exception_handler(request: Request, exc: AuthorizationError):
    flash(request, "You do not have permission to access that page.", "error")
    return RedirectResponse(url="/dashboard", status_code=303)
