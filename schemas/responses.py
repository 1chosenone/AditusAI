"""Pydantic schemas for API response models."""

from pydantic import BaseModel


class APIResponse(BaseModel):
    """Standard API response format.

    Attributes:
        status: Response status (e.g., "success", "error").
        message: Human-readable message describing the response.
    """

    status: str
    message: str


class CandidateResponse(BaseModel):
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

    model_config = {"from_attributes": True}
