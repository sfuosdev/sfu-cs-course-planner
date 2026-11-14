"""Application settings loaded from environment variables and the root .env file."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "SFU CS Course Planner API"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = False
    sfu_courses_api_base_url: str = "https://api.sfucourses.com/v1/rest"
    sfu_courses_api_timeout_seconds: float = 10.0

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
