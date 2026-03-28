"""Query schemas for job search optimization and parsing."""

from pydantic import BaseModel, Field


class ParsedQuery(BaseModel):
    """Schema for parsed or optimized job search query terms.

    Attributes:
        terms: List of refined job search terms extracted from raw input
            or inferred from candidate skills.
    """

    terms: list[str] = Field(description="List of optimized job search terms")
