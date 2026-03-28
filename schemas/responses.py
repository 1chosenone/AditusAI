"""Pydantic schemas for API response models."""

from typing import Any
from pydantic import BaseModel
from .candidate import (
    CandidateExperienceSchema,
    CandidateQualificationSchema,
    CandidateLanguageSchema,
    CandidateSenioritySchema,
    CandidateSkillSchema,
)


class APIResponse(BaseModel):
    """Standard API response format.

    Attributes:
        status: Response status (e.g., "success", "error").
        message: Human-readable message describing the response.
    """

    status: str
    message: str


class CandidateResponse(BaseModel):
    """Response schema for candidate data.

    Attributes:
        candidate_id: Unique identifier of the candidate.
        first_name: Candidate's first name.
        last_name: Candidate's last name.
        email: Candidate's email address.
        city: Candidate's city of residence.
        region: Candidate's region/state.
        country: Candidate's country.
        bio: Short career biography.
        github_url: URL to GitHub profile.
        linkedin_url: URL to LinkedIn profile.
    """

    candidate_id: int
    first_name: str
    last_name: str
    email: str | None
    city: str | None
    region: str | None
    country: str | None
    bio: str | None
    github_url: str | None
    linkedin_url: str | None
    experiences: list[CandidateExperienceSchema] | None
    qualifications: list[CandidateQualificationSchema] | None
    languages: list[CandidateLanguageSchema] | None
    seniority: CandidateSenioritySchema | None
    skills: list[CandidateSkillSchema] | None

    model_config = {"from_attributes": True}


class JobResponse(BaseModel):
    """Response schema for job creation.

    Attributes:
        job_id: Unique identifier for the background job.
    """

    job_id: str


class JobStatusResponse(BaseModel):
    """Response schema for job status.

    Attributes:
        id: Unique identifier of the job.
        status: Current status of the job (e.g., "pending", "completed", "failed").
        result: Result data if job completed successfully.
        error: Error message if job failed.
    """

    id: str
    status: str
    result: Any
    error: str | None
