from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: str
    BACKEND_URL: str  # ← .env の BACKEND_URL と対応
    FRONTEND_URL: str
    class Config:
        env_file = ".env"

settings = Settings()


