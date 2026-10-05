from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    environment: str = "development"
    secret_key: str = "change-this-in-production"
    database_url: str = "sqlite:///./pocketsmart.db"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    session_cookie: str = "pocketsmart_session"
    session_max_age: int = 86400
    max_image_mb: int = 5
    cors_origins: str = "http://127.0.0.1:8000,http://localhost:8000"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    @property
    def cors_origin_list(self): return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

@lru_cache
def get_settings(): return Settings()
