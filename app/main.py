from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.services.nominatim import nominatim_service
from app.api.routes import weather
from app.config import settings
from app.core.limiter import limiter
from app.services.open_meteo import open_meteo_service

app = FastAPI(title="Storm Track API", version="0.1.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET"],
)

app.include_router(weather.router)


@app.on_event("shutdown")
async def shutdown():
    await open_meteo_service.close()
    await nominatim_service.close()


@app.get("/health")
async def health():
    return {"status": "ok"}