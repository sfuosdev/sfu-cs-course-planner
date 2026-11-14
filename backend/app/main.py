"""FastAPI application entry point."""

from fastapi import FastAPI

from .api.health import router as health_router
from .config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description="Backend API for the SFU CS Course Planner.",
)

app.include_router(health_router)
