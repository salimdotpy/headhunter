class HeadhunterException(Exception):
    """Base exception for the Headhunter application."""


class ResourceNotFoundError(HeadhunterException):
    """Raised when a requested resource does not exist."""


class AuthorizationError(HeadhunterException):
    """Raised when a user is not authorized."""


class FileValidationError(HeadhunterException):
    """Raised when an uploaded file fails validation."""