from pydantic import BaseSettings
from typing import Optional
import logging
from logging.config import dictConfig
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        },
    }
}

dictConfig(LOG_CONFIG)
logger = logging.getLogger("app")

class Settings(BaseSettings):
    PROJECT_NAME: str = "Real Estate CRM"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: Optional[str] = None
    
    REDIS_URL: str = "redis://redis:6379/0"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Generate database URL if not set
if not settings.DATABASE_URL:
    settings.DATABASE_URL = (
        f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"
    )