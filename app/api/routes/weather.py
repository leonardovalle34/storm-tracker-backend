from fastapi import APIRouter, HTTPException, Request
from datetime import date as date_cls
from app.services.astronomy import astronomy_service
from app.config import settings
from app.core.limiter import limiter
from app.services.open_meteo import open_meteo_service
from app.services.nominatim import nominatim_service

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/geocode")
@limiter.limit(settings.rate_limit_default)
async def geocode(request: Request, name: str):
    try:
        """return await open_meteo_service.geocode(name)"""
        return await nominatim_service.geocode(name)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.get("/forecast")
@limiter.limit(settings.rate_limit_default)
async def forecast(request: Request, lat: float, lon: float):
    try:
        return await open_meteo_service.get_forecast(lat, lon)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.get("/marine")
@limiter.limit(settings.rate_limit_default)
async def marine(request: Request, lat: float, lon: float):
    try:
        return await open_meteo_service.get_marine(lat, lon)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

@router.get("/moon-phase")
@limiter.limit(settings.rate_limit_default)
async def moon_phase(request: Request, target_date: str | None = None):
    try:
        parsed = date_cls.fromisoformat(target_date) if target_date else None
    except ValueError:
        raise HTTPException(status_code=400, detail="target_date deve estar no formato YYYY-MM-DD")
    return astronomy_service.get_moon_phase(parsed)