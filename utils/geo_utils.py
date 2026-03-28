"""Geographic utility functions for location normalization."""

from geopy.geocoders import Nominatim
from schemas.geo import GeoLocation

geolocator = Nominatim(user_agent="aditusai")


def normalize_location(location: str) -> GeoLocation:
    """Normalize a location string into structured geographic data.

    Args:
        location: Raw location string (e.g., "San Francisco, CA").

    Returns:
        GeoLocation with normalized city, state, country, and country code.

    Raises:
        ValueError: If the location cannot be geocoded.
    """
    result = geolocator.geocode(location, addressdetails=True)

    if not result:
        raise ValueError(f"Could not normalize location: '{location}'")

    address = result.raw["address"]

    return GeoLocation(
        city=address.get("city") or address.get("town") or address.get("village"),
        state=address.get("state"),
        country=address.get("country"),
        country_code=address.get("country_code", "").upper() or None,
    )
