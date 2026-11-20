import pytest
from sqlalchemy import select

from app.models import Plan, PlanCourse, Course

PASSWORD = "correct horse battery"


def sign_up(client, email):
    response = client.post(
        "/api/auth/register",
        json={"email": email, "password": PASSWORD, "username": "Test user"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_plan(client, name="Graduate in 4 years", **extra):
    response = client.post("/api/plans", json={"name": name, **extra})
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def alice(client):
    sign_up(client, "alice@sfu.ca")
    return client


@pytest.fixture
def bob(make_client, alice):
    bob_client = make_client()
    sign_up(bob_client, "bob@sfu.ca")
    return bob_client


# ---------- Signed out ----------

@pytest.mark.parametrize(
    "method, path, body",
    [
        ("GET", "/api/plans", None),
        ("POST", "/api/plans", {"name": "Plan"}),
        ("GET", "/api/plans/1", None),
        ("PATCH", "/api/plans/1", {"name": "Plan", "version": 1}),
        ("DELETE", "/api/plans/1", None),
    ],
)
def test_plan_routes_require_sign_in(client, method, path, body):
    response = client.request(method, path, json=body)

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_plan_routes_reject_a_signed_out_session(client):
    sign_up(client, "alice@sfu.ca")
    client.post("/api/auth/logout")

    assert client.get("/api/plans").status_code == 401


# ---------- Own plans ----------

def test_new_plan_belongs_to_the_signed_in_user(alice, session_factory):
    user_id = alice.get("/api/auth/me").json()["id"]

    plan = create_plan(alice, startTermCode=1257)

    assert plan["name"] == "Graduate in 4 years"
    assert plan["version"] == 1
    assert plan["startTermCode"] == 1257
    assert plan["planCourses"] == []
    with session_factory() as db:
        assert db.get(Plan, plan["id"]).user_id == user_id


def test_create_plan_cannot_be_assigned_to_another_user(alice, session_factory):
    plan = alice.post("/api/plans", json={"name": "Plan", "userId": 999, "user_id": 999}).json()

    with session_factory() as db:
        assert db.get(Plan, plan["id"]).user_id == alice.get("/api/auth/me").json()["id"]


def test_create_plan_validates_name(alice):
    assert alice.post("/api/plans", json={"name": ""}).status_code == 422
    assert alice.post("/api/plans", json={"name": "x" * 256}).status_code == 422
    assert alice.post("/api/plans", json={}).status_code == 422


def test_list_and_get_own_plans(alice):
    first = create_plan(alice, "First")
    second = create_plan(alice, "Second")

    listed = alice.get("/api/plans").json()
    assert [p["name"] for p in listed] == ["First", "Second"]
    assert "planCourses" not in listed[0]
    assert alice.get(f"/api/plans/{first['id']}").json()["name"] == "First"
    assert alice.get(f"/api/plans/{second['id']}").json()["name"] == "Second"


def test_get_plan_includes_its_courses(alice, session_factory):
    plan = create_plan(alice)
    with session_factory() as db:
        course = Course(title="Data Structures", course_code="CMPT 225", credits=3,
                        dept="CMPT", number="225")
        db.add(course)
        db.flush()
        db.add(PlanCourse(plan_id=plan["id"], course_id=course.id, year=1, season="fall"))
        db.commit()

    courses = alice.get(f"/api/plans/{plan['id']}").json()["planCourses"]

    assert len(courses) == 1
    assert courses[0]["course"]["courseCode"] == "CMPT 225"
    assert (courses[0]["year"], courses[0]["season"]) == (1, "fall")


def test_missing_plan_is_404(alice):
    assert alice.get("/api/plans/12345").status_code == 404


def test_update_plan_renames_and_bumps_version(alice):
    plan = create_plan(alice, startTermCode=1257)

    response = alice.patch(f"/api/plans/{plan['id']}", json={"name": "New name", "version": 1})

    assert response.status_code == 200
    body = response.json()
    assert (body["name"], body["version"]) == ("New name", 2)
    assert body["startTermCode"] == 1257  # left out of the request, so unchanged
    assert alice.get(f"/api/plans/{plan['id']}").json()["version"] == 2


def test_update_plan_can_clear_the_start_term(alice):
    plan = create_plan(alice, startTermCode=1257)

    body = alice.patch(
        f"/api/plans/{plan['id']}",
        json={"name": plan["name"], "version": 1, "startTermCode": None},
    ).json()

    assert body["startTermCode"] is None


def test_update_plan_with_stale_version_is_409(alice):
    plan = create_plan(alice)
    alice.patch(f"/api/plans/{plan['id']}", json={"name": "Edit one", "version": 1})

    response = alice.patch(f"/api/plans/{plan['id']}", json={"name": "Edit two", "version": 1})

    assert response.status_code == 409
    assert alice.get(f"/api/plans/{plan['id']}").json()["name"] == "Edit one"


def test_delete_plan_removes_it_and_its_courses(alice, session_factory):
    plan = create_plan(alice)
    with session_factory() as db:
        course = Course(title="Data Structures", course_code="CMPT 225", credits=3,
                        dept="CMPT", number="225")
        db.add(course)
        db.flush()
        db.add(PlanCourse(plan_id=plan["id"], course_id=course.id, year=1, season="fall"))
        db.commit()

    response = alice.delete(f"/api/plans/{plan['id']}")

    assert response.status_code == 204
    assert alice.get(f"/api/plans/{plan['id']}").status_code == 404
    with session_factory() as db:
        assert db.scalar(select(PlanCourse)) is None


# ---------- Someone else's plans ----------

def test_plan_list_only_shows_the_signed_in_users_plans(alice, bob):
    create_plan(alice, "Alice plan")
    create_plan(bob, "Bob plan")

    assert [p["name"] for p in alice.get("/api/plans").json()] == ["Alice plan"]
    assert [p["name"] for p in bob.get("/api/plans").json()] == ["Bob plan"]


def test_cannot_read_another_users_plan(alice, bob):
    plan = create_plan(alice)

    response = bob.get(f"/api/plans/{plan['id']}")

    assert response.status_code == 404
    assert response.json() == alice.get("/api/plans/99999").json()  # same as a missing plan


def test_cannot_update_another_users_plan(alice, bob):
    plan = create_plan(alice, "Alice plan")

    response = bob.patch(f"/api/plans/{plan['id']}", json={"name": "Hijacked", "version": 1})

    assert response.status_code == 404
    unchanged = alice.get(f"/api/plans/{plan['id']}").json()
    assert (unchanged["name"], unchanged["version"]) == ("Alice plan", 1)


def test_cannot_delete_another_users_plan(alice, bob):
    plan = create_plan(alice)

    assert bob.delete(f"/api/plans/{plan['id']}").status_code == 404
    assert alice.get(f"/api/plans/{plan['id']}").status_code == 200
