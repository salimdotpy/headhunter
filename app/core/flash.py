from typing import Literal

from fastapi import Request
from app.core.csrf import get_csrf_token


FlashCategory = Literal[
    "info",
    "success",
    "warning",
    "error",
]


def flash(
    request: Request,
    message: str,
    category: FlashCategory = "info",
) -> None:
    request.session.setdefault("_flashes", []).append(
        {
            "message": message,
            "category": category,
        }
    )


def get_flashed_messages(request: Request) -> list[dict[str, str]]:
    return request.session.pop("_flashes", [])


def flash_context(request: Request) -> dict[str, list[dict[str, str]]]:
    return {
        "flashes": get_flashed_messages(request),
        "csrf_token": get_csrf_token(request),
    }