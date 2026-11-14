"""Course search endpoints backed by the SFU course data service."""

from fastapi import APIRouter, HTTPException, Query

from ..config import settings
from ..schemas.course import Course
from ..services.sfu_courses import (
    SFUCoursesAPIError,
    SFUCoursesClient,
    SFUCoursesTimeoutError,
)

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[Course], summary="Search course outlines")
def get_courses(
    dept: str | None = Query(default=None, min_length=2, max_length=8),
    number: str | None = Query(default=None, min_length=1, max_length=8),
) -> list[Course]:
    """Return course outlines, optionally filtered by department and number."""
    try:
        with SFUCoursesClient(
            base_url=settings.sfu_courses_api_base_url,
            timeout_seconds=settings.sfu_courses_api_timeout_seconds,
        ) as client:
            return client.get_courses(dept=dept, number=number)
    except SFUCoursesTimeoutError as exc:
        raise HTTPException(status_code=504, detail="Course data provider timed out") from exc
    except SFUCoursesAPIError as exc:
        raise HTTPException(status_code=502, detail="Course data provider request failed") from exc
