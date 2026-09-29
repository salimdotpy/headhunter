import logging

from fastapi import Request
from fastapi.responses import RedirectResponse, HTMLResponse

from app.core.flash import flash
from app.core.templates import templates
from app.exceptions.auth import AuthenticationError
from app.exceptions.base import AuthorizationError


logger = logging.getLogger(__name__)

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


async def authorization_exception_handler(request: Request, exc: AuthorizationError):
    flash(request, "You do not have permission to access that page.", "error")
    return RedirectResponse(url="/dashboard", status_code=303)


async def internal_server_error_handler(
    request: Request,
    exc: Exception,
) -> HTMLResponse:
    logger.exception(
        "Unhandled application error on %s %s",
        request.method,
        request.url.path,
        exc_info=exc,
    )

    return templates.TemplateResponse(
        request=request,
        name="errors/500.html",
        context={
            "title": "Something went wrong — Headhunter",
        },
        status_code=500,
    )