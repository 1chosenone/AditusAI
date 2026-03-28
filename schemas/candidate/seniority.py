"""Pydantic schemas for seniority-related models."""

from pydantic import BaseModel
from enums import SeniorityLevel


class CandidateSenioritySchema(BaseModel):
    """Schema for seniority information.

    Attributes:
        level: Seniority level enum value.
        years_of_experience: Total years of experience.
    """

    level: SeniorityLevel | None = None
    years_of_experience: float | None = None

    model_config = {"from_attributes": True}
