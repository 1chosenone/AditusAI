"""Geographic location schemas."""

from pydantic import BaseModel


class GeoLocation(BaseModel):
    """Schema representing a geographic location.

    Attributes:
        city: Name of the city.
        state: Name of the state or region.
        country: Name of the country.
        country_code: ISO country code (e.g., "US", "CA"), if available.
    """

    city: str
    state: str
    country: str
    country_code: str | None
