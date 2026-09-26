from app.exceptions.base import HeadhunterException


class ResourceAlreadyExistsError(HeadhunterException):
    """Raised when a resource already exists."""