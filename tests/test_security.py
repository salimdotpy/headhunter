from app.core.security import hash_password, verify_password


def test_password_hash_round_trip():
    password = "StrongPass123!"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("WrongPass123!", hashed)
