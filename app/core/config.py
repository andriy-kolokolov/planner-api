import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DB_URL = os.getenv("DB_URL")

    class Config:
        env_file = ".env"

settings = Settings()