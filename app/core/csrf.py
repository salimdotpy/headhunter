import secrets

from fastapi import Request

from app.exceptions.auth import AuthenticationError


CSRF_SESSION_KEY = "_csrf_token"


def get_csrf_token(request: Request) -> str:
    token = request.session.get(CSRF_SESSION_KEY)

    if token is None:
        token = secrets.token_urlsafe(32)
        request.session[CSRF_SESSION_KEY] = token

    return token


def validate_csrf_token(
    request: Request,
    submitted_token: str,
) -> None:
    expected_token = request.session.get(CSRF_SESSION_KEY)

    if (
        expected_token is None
        or not submitted_token
        or not secrets.compare_digest(
            expected_token,
            submitted_token,
        )
    ):
        raise AuthenticationError("Invalid CSRF token.")