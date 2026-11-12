"""HTTP client for the sfucourses course outline API."""

from html.parser import HTMLParser
from typing import Any

import httpx

from ..schemas.course import Course


class SFUCoursesError(Exception):
    """Base error for failures while retrieving SFU course data."""


class SFUCoursesTimeoutError(SFUCoursesError):
    """The upstream API did not respond before the configured timeout."""


class SFUCoursesAPIError(SFUCoursesError):
    """The upstream API returned an error or an invalid response."""


class _TextExtractor(HTMLParser):
    """Extract readable text from descriptions that contain markup."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def _plain_text(value: Any) -> str:
    if not isinstance(value, str) or not value:
        return ""
    parser = _TextExtractor()
    parser.feed(value)
    return " ".join(" ".join(parser.parts).split())


class SFUCoursesClient:
    """Fetch and normalize course outlines from api.sfucourses.com."""

    def __init__(
        self,
        base_url: str = "https://api.sfucourses.com/v1/rest",
        timeout_seconds: float = 10.0,
        *,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")
        self._base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            timeout=httpx.Timeout(timeout_seconds),
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "SFUCoursesClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _get_json(self, path: str, params: dict[str, str]) -> Any:
        try:
            response = self._client.get(f"{self._base_url}/{path}", params=params)
        except httpx.TimeoutException as exc:
            raise SFUCoursesTimeoutError("The SFU course API request timed out") from exc
        except httpx.HTTPError as exc:
            raise SFUCoursesAPIError("Could not reach the SFU course API") from exc

        if response.status_code == 404 and path == "prerequisites":
            return {}
        if response.is_error:
            raise SFUCoursesAPIError(
                f"The SFU course API returned HTTP {response.status_code}"
            )
        try:
            return response.json()
        except ValueError as exc:
            raise SFUCoursesAPIError("The SFU course API returned invalid JSON") from exc

    def get_courses(
        self, dept: str | None = None, number: str | None = None
    ) -> list[Course]:
        """Retrieve outlines, descriptions, and parsed prerequisite trees."""
        params = {
            key: value
            for key, value in {"dept": dept, "number": number}.items()
            if value
        }
        params["prereqs"] = "true"
        outlines = self._get_json("outlines", params)
        if not isinstance(outlines, list):
            raise SFUCoursesAPIError("The SFU course API returned an invalid outlines payload")

        prerequisite_map = self._get_json("prerequisites", params)
        if not isinstance(prerequisite_map, dict):
            raise SFUCoursesAPIError("The SFU course API returned an invalid prerequisites payload")

        courses: list[Course] = []
        for outline in outlines:
            if not isinstance(outline, dict):
                raise SFUCoursesAPIError("The SFU course API returned an invalid course outline")
            course_dept = str(outline.get("dept", ""))
            course_number = str(outline.get("number", ""))
            if not course_dept or not course_number or not outline.get("title"):
                raise SFUCoursesAPIError("The SFU course API returned an incomplete course outline")
            code = f"{course_dept} {course_number}"
            courses.append(
                Course(
                    dept=course_dept,
                    number=course_number,
                    title=str(outline["title"]),
                    units=_string_or_none(outline.get("units")),
                    description=_plain_text(outline.get("description")),
                    prerequisites=_plain_text(outline.get("prerequisites")),
                    prerequisite_tree=prerequisite_map.get(code),
                    corequisites=_plain_text(outline.get("corequisites")),
                    offerings=outline.get("offerings") or [],
                )
            )
        return courses


def _string_or_none(value: Any) -> str | None:
    return None if value is None else str(value)
