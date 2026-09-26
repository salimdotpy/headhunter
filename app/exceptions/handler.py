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