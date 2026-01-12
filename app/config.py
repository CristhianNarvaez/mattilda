import os
from functools import lru_cache


class Settings:
    PROJECT_NAME: str = "Mattilda Backend Test"
    API_V1_PREFIX: str = "/api/v1"

    # Default to SQLite for local dev; overriden in docker-compose for Postgres
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./app.db",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
