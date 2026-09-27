import pytest
from pydantic import ValidationError

from app.schemas.auth import PasswordChangeRequest, PasswordResetConfirmRequest, RegisterRequest


def test_registration_requires_matching_passwords():
    with pytest.raises(ValidationError):
        RegisterRequest(
            full_name="Jane Doe",
            email="jane@example.com",
            password="StrongPass123!",
            confirm_password="DifferentPass123!",
        )


def test_password_change_requires_matching_passwords():
    with pytest.raises(ValidationError):
        PasswordChangeRequest(
            current_password="OldPass123!",
            new_password="NewPass123!",
            confirm_password="DifferentPass123!",
        )


def test_password_reset_requires_matching_passwords():
    with pytest.raises(ValidationError):
        PasswordResetConfirmRequest(
            token="a" * 48,
            new_password="NewPass123!",
            confirm_password="DifferentPass123!",
        )
