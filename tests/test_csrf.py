from types import SimpleNamespace

import pytest

from app.core.csrf import get_csrf_token, validate_csrf_token
from app.exceptions.auth import AuthenticationError


def test_csrf_token_is_stable_for_session():
    request = SimpleNamespace(session={})
    first = get_csrf_token(request)
    second = get_csrf_token(request)
    assert first == second


def test_csrf_rejects_invalid_token():
    request = SimpleNamespace(session={"_csrf_token": "expected"})
    with pytest.raises(AuthenticationError):
        validate_csrf_token(request, "wrong")
