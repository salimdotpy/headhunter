from app.exceptions.base import HeadhunterException


class PortfolioSlugAlreadyExistsError(HeadhunterException):
    """Raised when a portfolio slug is already in use."""
