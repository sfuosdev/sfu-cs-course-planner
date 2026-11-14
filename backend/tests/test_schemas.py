"""Tests for the API contracts in app/schemas/.

Each test builds model objects by hand (no database needed), passes them through a
schema, and checks the result matches docs/api-contracts.md.

Run from backend/:  python -m pytest
"""
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.models import (
    Course,
    Plan,
    PlanCourse,
    Prerequisite,
    ProgramRequirement,
    ProgramRequirementCourse,
    Term,
)

from app.schemas import (
    CourseResponse,
    CourseSummary,
    PlanCourseCreate,
    PlanCourseRead,
    PlanCourseUpdate,
    PlanCreate,
    PlanDetailResponse,
    PlanResponse,
    PlanUpdate,
    ProgramRequirementResponse,
    TermRead,
)

# ---------- Fixtures: sample model objects reused by several tests ----------
# A fixture is a function pytest runs for you; any test that lists its name as a
# parameter gets the return value.

@pytest.fixture
def cmpt125():
    return Course(id=3, course_code="CMPT 125", title="Intro CS II", credits=3)


@pytest.fixture
def cmpt225(cmpt125):
    course = Course(
        id=12,
        course_code="CMPT 225",
        title="Data Structures and Programming",
        credits=3,
        description="Intro to data structures.",
        degree_level="UGRD",
        designation="Quantitative",
        prerequisites_text="CMPT 125",
        corequisites_text=None,
    )
    course.prerequisites = [Prerequisite(id=1, group_number=1, required_course=cmpt125)]
    return course


@pytest.fixture
def plan(cmpt225):
    now = datetime(2026, 1, 15, 18, 30, tzinfo=timezone.utc)
    plan = Plan(id=7, name="Graduate in 4 years", version=1, created_at=now, updated_at=now)
    plan.plan_courses = [PlanCourse(id=41, term_code=1257, course=cmpt225)]
    return plan


# ---------- Response schemas: model -> schema -> JSON ----------
# model_dump(mode="json", by_alias=True) produces exactly what FastAPI will send.

def test_course_summary_json(cmpt225):
    data = CourseSummary.model_validate(cmpt225).model_dump(mode="json", by_alias=True)

    assert data == {
        "id": 12,
        "courseCode": "CMPT 225",
        "title": "Data Structures and Programming",
        "credits": 3,
    }


def test_course_response_includes_nested_prerequisites(cmpt225):
    data = CourseResponse.model_validate(cmpt225).model_dump(mode="json", by_alias=True)

    assert data["prerequisitesText"] == "CMPT 125"
    assert data["corequisitesText"] is None
    assert data["prerequisites"] == [
        {
            "groupNumber": 1,
            "requiredCourse": {"id": 3, "courseCode": "CMPT 125", "title": "Intro CS II", "credits": 3},
        }
    ]


def test_course_response_hides_internal_fields(cmpt225):
    data = CourseResponse.model_validate(cmpt225).model_dump(by_alias=True)

    assert "lastSyncedAt" not in data


def test_term_read():
    term = Term(code=1257, year=2025, season="Fall")

    assert TermRead.model_validate(term).model_dump() == {"code": 1257, "year": 2025, "season": "Fall"}


def test_plan_response_has_no_courses_or_user(plan):
    data = PlanResponse.model_validate(plan).model_dump(mode="json", by_alias=True)

    assert data["createdAt"] == "2026-01-15T18:30:00Z"  # datetimes become ISO strings
    assert "planCourses" not in data
    assert "userId" not in data


def test_plan_detail_includes_courses(plan):
    data = PlanDetailResponse.model_validate(plan).model_dump(mode="json", by_alias=True)

    assert data["planCourses"] == [
        {
            "id": 41,
            "termCode": 1257,
            "course": {"id": 12, "courseCode": "CMPT 225", "title": "Data Structures and Programming", "credits": 3},
        }
    ]


def test_plan_course_read(plan):
    data = PlanCourseRead.model_validate(plan.plan_courses[0]).model_dump(by_alias=True)

    assert data["id"] == 41
    assert data["termCode"] == 1257


def test_program_requirement_allows_missing_minimums(cmpt225):
    requirement = ProgramRequirement(
        id=1, program_code="CMPT-MAJOR", name="Core", min_courses=1, min_credits=None
    )
    requirement.courses = [ProgramRequirementCourse(course=cmpt225)]

    data = ProgramRequirementResponse.model_validate(requirement).model_dump(by_alias=True)

    assert data["programCode"] == "CMPT-MAJOR"
    assert data["minCredits"] is None
    assert data["courses"][0]["course"]["courseCode"] == "CMPT 225"


# ---------- Request schemas: good input is accepted, bad input is rejected ----------

def test_plan_create_accepts_valid_name():
    assert PlanCreate(name="My plan").name == "My plan"


# parametrize runs the same test once per value in the list
@pytest.mark.parametrize("bad_name", ["", "x" * 256])
def test_plan_create_rejects_bad_name(bad_name):
    with pytest.raises(ValidationError):
        PlanCreate(name=bad_name)


def test_plan_update_requires_name():
    with pytest.raises(ValidationError):
        PlanUpdate()


def test_plan_course_create_from_frontend_json():
    # This is the JSON the frontend sends (camelCase), see api-contracts.md
    body = PlanCourseCreate.model_validate({"courseId": 12, "termCode": 1257})

    assert body.course_id == 12
    assert body.term_code == 1257


def test_plan_course_create_requires_term():
    with pytest.raises(ValidationError):
        PlanCourseCreate.model_validate({"courseId": 12})


def test_plan_course_update_rejects_wrong_type():
    with pytest.raises(ValidationError):
        PlanCourseUpdate.model_validate({"termCode": "fall"})

def test_missing_credits_become_zero():
    assert Course(course_code="CMPT 999", title="X", credits=None).credits == 0
