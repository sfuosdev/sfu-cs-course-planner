"""Fixture-based integration tests for the upstream course data client."""

import json
from pathlib import Path

import httpx
import pytest

from backend.app.services.sfu_courses import (
    SFUCoursesAPIError,
    SFUCoursesClient,
    SFUCoursesTimeoutError,
)

FIXTURES = Path(__file__).parent / "fixtures"


def _fixture(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_fetches_and_normalizes_outlines_and_prerequisite_trees() -> None:
    fixtures = {
        "/v1/rest/outlines": _fixture("course_outlines.json"),
        "/v1/rest/prerequisites": _fixture("prerequisites.json"),
    }

    def respond(request: httpx.Request) -> httpx.Response:
        assert request.url.params["dept"] == "CMPT"
        assert request.url.params["number"] == "225"
        return httpx.Response(200, json=fixtures[request.url.path])

    with SFUCoursesClient(transport=httpx.MockTransport(respond)) as client:
        courses = client.get_courses(dept="CMPT", number="225")

    assert len(courses) == 1
    course = courses[0]
    assert course.description == "Introduction to data structures and algorithms."
    assert course.prerequisites == "CMPT 125 and MACM 101."
    assert course.prerequisite_tree is not None
    assert course.prerequisite_tree.type == "and"
    assert [node.id for node in course.prerequisite_tree.children] == [
        "CMPT 125",
        "MACM 101",
    ]
    assert course.offerings[0].term == "Fall 2026"


def test_upstream_http_failure_raises_api_error() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(503))
    with SFUCoursesClient(transport=transport) as client:
        with pytest.raises(SFUCoursesAPIError, match="HTTP 503"):
            client.get_courses(dept="CMPT", number="225")


def test_upstream_timeout_raises_timeout_error() -> None:
    def timeout(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out", request=request)

    with SFUCoursesClient(transport=httpx.MockTransport(timeout)) as client:
        with pytest.raises(SFUCoursesTimeoutError):
            client.get_courses(dept="CMPT", number="225")
