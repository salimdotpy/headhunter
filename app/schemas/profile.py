from pydantic import AnyHttpUrl, BaseModel, Field


class ProfileUpdateRequest(BaseModel):
    full_name: str = Field(min_length=1, max_length=150)
    professional_title: str = Field(default="", max_length=200)
    summary: str = Field(default="", max_length=5000)

    phone: str = Field(default="", max_length=30)
    show_email: bool = False
    show_phone: bool = False

    location: str = Field(default="", max_length=200)
    show_location: bool = False

    website_url: AnyHttpUrl | None = None
    show_website: bool = False

    linkedin_url: AnyHttpUrl | None = None
    show_linkedin: bool = False

    github_url: AnyHttpUrl | None = None
    show_github: bool = False
