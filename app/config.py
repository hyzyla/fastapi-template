from pydantic import BaseSettings, Field


class Config(BaseSettings):
    APP_TITLE: str = Field("fastapi-template")
    ENVIRONMENT: str = Field(...)
    BASE_API_PATH: str = Field("/api")
    SENTRY_DSN: str | None = Field(None)
    DATABASE_URL: str = Field(None)


config = Config()
