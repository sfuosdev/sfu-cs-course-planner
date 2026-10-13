from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "SFU CS Course Planner API")
    frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://course_planner:course_planner@localhost:5432/course_planner",
    )


settings = Settings()
