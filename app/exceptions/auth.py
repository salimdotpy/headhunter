from app.exceptions.base import HeadhunterException


class AuthenticationError(HeadhunterException):
    """Raised when authentication fails."""