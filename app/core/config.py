from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str
    DATABASE_URL: str = "sqlite:///./legaltogo.db"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "https://your-lovable-app.lovable.app"]
    PRODUCT_PRICE_CENTS: int = 19900  # $199
    REDIS_URL: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"

settings = Settings()
