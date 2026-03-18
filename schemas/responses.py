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
