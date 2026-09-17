from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    open_meteo_base_url: str
    open_meteo_geocoding_url: str
    open_meteo_marine_url: str
    cors_origins: list[str] = ["*"]
    rate_limit_default: str = "30/minute"
    NOMINATIM_URL: str
    NOMINATIM_USER_AGENT: str

    class Config:
        env_file = ".env"

settings = Settings()