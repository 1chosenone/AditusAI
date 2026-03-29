"""Query schemas for job search optimization and parsing."""

from pydantic import BaseModel, Field
from .geo import GeoLocation


class ParsedQuery(BaseModel):
    """Schema for parsed or optimized job search query terms.

    Attributes:
        terms: List of refined job search terms extracted from raw input
            or inferred from candidate skills.
    """

    terms: list[str] = Field(description="List of optimized job search terms")


class JobSearchQuery(BaseModel):
    """Schema for a complete job search query.

    Attributes:
        terms: Parsed or optimized search terms.
        location: Geographic location for the search.
        max_results_per_source: Maximum results to fetch from each platform.
    """

    terms: list[str]
    location: GeoLocation
    max_results_per_source: int
