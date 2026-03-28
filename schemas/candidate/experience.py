"""Pydantic schemas for experience-related models."""

from pydantic import BaseModel
from enums import JobTypeEnum, IndustryEnum


class CandidateExperienceSchema(BaseModel):
    """Represents a candidate's work experience.

    Attributes:
        company_name: Name of the company.
        job_title: Title of the position.
        job_type: Type of employment.
        industry: Industry sector of the experience.
        description: Description of responsibilities and achievements.
        city: City where the job was located.
        region: Region (province, state, etc.) where the job was located.
        country: Country where the job was located.
        start_year: Year the position started.
        start_month: Month the position started (None if not specified).
        end_year: Year the position ended (None if current).
        end_month: Month the position ended (None if not specified).
    """

    company_name: str
    job_title: str
    job_type: JobTypeEnum | None = None
    industry: IndustryEnum | None = None
    description: str | None = None
    city: str | None = None
    region: str | None = None
    country: str | None = None
    start_year: int
    start_month: int | None
    end_year: int | None = None
    end_month: int | None

    model_config = {"from_attributes": True}
