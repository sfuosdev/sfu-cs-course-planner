"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"], summary="Check API health")
def health_check() -> dict[str, str]:
    """Return a simple liveness response."""
    return {"status": "ok"}
