from pydantic import BaseModel

class Location(BaseModel):
    name: str
    latitude: float
    longitude: float
    country: str | None = None
    admin1: str | None = None

class GeocodeResponse(BaseModel):
    results: list[Location]