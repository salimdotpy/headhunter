from pydantic import BaseModel, Field


class PortfolioSlugUpdateRequest(BaseModel):
    slug: str = Field(min_length=3, max_length=100, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
