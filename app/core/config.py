# app/core/config.py
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn, validator
from functools import lru_cache


class Settings(BaseSettings):
    # app
    APP_ENV: str = Field(default="production")

    # Security
    ACCESS_TOKEN_SECRET_KEY: str = Field(default="", min_length=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    ACCESS_TOKEN_ALGORITHM: str = Field(default="HS256")
    API_SECRET_KEY: str = Field(description="API secret key value", default="")
    API_SECRET_HEADER_NAME: str = Field(default="X-API-Secret", description="Header name for API secret")

    # Database
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=None, ge=1, le=65535)
    DB_USER: str = Field(default="")
    DB_PASSWORD: str = Field(default="")
    DB_NAME: str = Field(default="")
    DB_URL: str = Field(default="")

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="forbid"
    )


@lru_cache()
def get_settings() -> Settings:
    """Cache settings instance"""
    return Settings()


# Global instance (optional, but use get_settings() is preferred)
app_settings = get_settings()
