from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    open_meteo_base_url: str
    open_meteo_marine_url: str
    nominatim_url: str
    nominatim_user_agent: str
    cors_origins: list[str] = ["*"]
    rate_limit_default: str = "30/minute"

    class Config:
        env_file = ".env"


settings = Settings()