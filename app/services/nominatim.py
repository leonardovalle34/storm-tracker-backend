import httpx
from app.config import settings

class NominatimService:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=10.0, headers={"User-Agent" : settings.NOMINATIM_USER_AGENT})

    async def geocode(self, name:str , limit:int = 8) -> list[dict]:
        response = await self._client.get(
            settings.NOMINATIM_URL,
            params={
                "q": name,
                "format": "json",
                "limit": limit,
                "addressdetails": 1,
            },
        )
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        await self._client.aclose()

nominatim_service = NominatimService()