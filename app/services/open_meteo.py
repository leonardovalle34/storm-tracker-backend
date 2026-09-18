import httpx
from app.config import settings

class OpenMeteoService:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=10.0)

    async def get_forecast(self, lat: float, lon: float, days: int = 16) -> dict:
        response = await self._client.get(
            f"{settings.open_meteo_base_url}/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "hourly":"temperature_2m,precipitation,wind_speed_10m,wind_direction_10m",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                "timezone": "America/Sao_Paulo",
                "forecast_days": days,
            },
        )
        response.raise_for_status()
        return response.json()

    async def get_marine(self,lat: float, lon: float, days: int = 7) -> dict:
        response = await self._client.get(
            f"{settings.open_meteo_marine_url}/marine",
            params={
                "latitude": lat,
                "longitude": lon,
                "hourly": "wave_height,swell_wave_height,swell_wave_direction,swell_wave_period",
                "timezone": "America/Sao_Paulo",
                "forecast_days": days,
                "models":"best_match"
            },
        )
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        await self._client.aclose()


open_meteo_service = OpenMeteoService()