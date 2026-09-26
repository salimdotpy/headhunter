from datetime import date

from pydantic import AnyHttpUrl, BaseModel, Field, model_validator


class EducationRequest(BaseModel):
    institution: str = Field(min_length=1, max_length=200)
    qualification: str = Field(min_length=1, max_length=200)
    field_of_study: str = Field(default="", max_length=200)
    start_date: date | None = None
    end_date: date | None = None
    description: str = Field(default="", max_length=5000)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("End date cannot be before start date.")
        return self


class ExperienceRequest(BaseModel):
    job_title: str = Field(min_length=1, max_length=200)
    company: str = Field(min_length=1, max_length=200)
    location: str = Field(default="", max_length=200)
    start_date: date | None = None
    end_date: date | None = None
    description: str = Field(default="", max_length=5000)
    is_current: bool = False

    @model_validator(mode="after")
    def validate_dates(self):
        if self.is_current:
            self.end_date = None
        elif self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("End date cannot be before start date.")
        return self


class SkillRequest(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    proficiency: str = Field(default="", max_length=50)


class CertificationRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    issuer: str = Field(min_length=1, max_length=200)
    issue_date: date | None = None
    expiry_date: date | None = None
    credential_reference: str = Field(default="", max_length=200)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.issue_date and self.expiry_date and self.expiry_date < self.issue_date:
            raise ValueError("Expiry date cannot be before issue date.")
        return self


class ProjectRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=5000)
    role: str = Field(default="", max_length=200)
    technologies: str = Field(default="", max_length=1000)
    project_date: date | None = None
    project_url: AnyHttpUrl | None = None
