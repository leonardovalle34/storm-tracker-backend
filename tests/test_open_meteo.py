import asyncio
import os
import unittest

import httpx

# Settings() reads these at import time; the transport below never hits the network.
os.environ.setdefault("OPEN_METEO_BASE_URL", "https://api.open-meteo.com/v1")
os.environ.setdefault("OPEN_METEO_MARINE_URL", "https://marine-api.open-meteo.com/v1")
os.environ.setdefault("NOMINATIM_URL", "https://nominatim.openstreetmap.org/search")
os.environ.setdefault("NOMINATIM_USER_AGENT", "storm-track-tests")

from app.services.open_meteo import OpenMeteoService  # noqa: E402


def capture_forecast_params() -> dict[str, list[str]]:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"ok": True})

    async def run() -> dict:
        service = OpenMeteoService()
        service._client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        try:
            return await service.get_forecast(-23.96, -46.33)
        finally:
            await service.close()

    assert asyncio.run(run()) == {"ok": True}
    params = seen[0].url.params
    return {key: params[key].split(",") for key in ("hourly", "daily", "current")}


class GetForecastParamsTest(unittest.TestCase):
    def test_hourly_requests_weather_code_and_is_day(self) -> None:
        hourly = capture_forecast_params()["hourly"]
        self.assertIn("weather_code", hourly)
        self.assertIn("is_day", hourly)

    def test_keeps_every_existing_variable(self) -> None:
        params = capture_forecast_params()
        for var in ("temperature_2m", "precipitation", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"):
            self.assertIn(var, params["hourly"])
        for var in (
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "uv_index_max",
            "sunrise",
            "sunset",
            "apparent_temperature_max",
        ):
            self.assertIn(var, params["daily"])
        self.assertEqual(params["current"], ["temperature_2m", "weather_code", "wind_speed_10m"])


if __name__ == "__main__":
    unittest.main()
