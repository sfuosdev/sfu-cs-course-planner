from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import select

from app.config import settings
from app.models import User, UserSession

EMAIL = "student@sfu.ca"
PASSWORD = "correct horse battery"
USERNAME = "Test user"


def register(client, email=EMAIL, password=PASSWORD, username=USERNAME):
    return client.post(
        "/api/auth/register",
        json={"email": email, "password": password, "username": username},
    )


def login(client, email=EMAIL, password=PASSWORD):
    return client.post("/api/auth/login", json={"email": email, "password": password})


# ---------- Register ----------

def test_register_creates_account_and_signs_in(client):
    response = register(client)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == EMAIL
    assert set(body) == {"id", "email", "username", "createdAt"}
    assert client.get("/api/auth/me").json()["email"] == EMAIL


def test_register_never_returns_or_stores_the_plain_password(client, session_factory):
    response = register(client)

    assert PASSWORD not in response.text
    with session_factory() as db:
        user = db.scalar(select(User))
        assert user.password_hash != PASSWORD


def test_register_sets_a_locked_down_session_cookie(client):
    response = register(client)

    cookie = response.headers["set-cookie"].lower()
    assert f"{settings.session_cookie_name}=" in cookie
    assert "httponly" in cookie
    assert "samesite=lax" in cookie
    assert "path=/" in cookie
    assert f"max-age={settings.session_ttl_days * 86400}" in cookie


def test_register_stores_email_in_lowercase(client, session_factory):
    register(client, email="Student@SFU.ca")

    with session_factory() as db:
        assert db.scalar(select(User.email)) == EMAIL


def test_register_duplicate_email_returns_409_ignoring_case(client, make_client):
    register(client)

    response = register(make_client(), email="STUDENT@sfu.ca")

    assert response.status_code == 409
    assert "set-cookie" not in response.headers


def test_register_rejects_short_password(client):
    assert register(client, password="short").status_code == 422


def test_register_rejects_invalid_email(client):
    assert register(client, email="not-an-email").status_code == 422


# ---------- Username ----------

def test_register_returns_and_stores_username(client, session_factory):
    assert register(client).json()["username"] == USERNAME

    with session_factory() as db:
        assert db.scalar(select(User.username)) == USERNAME


def test_me_and_login_return_username(client, make_client):
    register(client)

    assert client.get("/api/auth/me").json()["username"] == USERNAME
    assert login(make_client()).json()["username"] == USERNAME


def test_register_trims_username(client):
    assert register(client, username="  Test user  ").json()["username"] == USERNAME


def test_register_without_username_returns_422(client):
    response = client.post("/api/auth/register", json={"email": EMAIL, "password": PASSWORD})

    assert response.status_code == 422


@pytest.mark.parametrize("username", ["", "   ", "x" * 51])
def test_register_rejects_invalid_username(client, username):
    assert register(client, username=username).status_code == 422


def test_register_accepts_50_character_username(client):
    assert register(client, username="x" * 50).status_code == 201


def test_two_users_can_share_a_username(client, make_client):
    register(client)

    assert register(make_client(), email="other@sfu.ca").status_code == 201


# ---------- Login ----------

def test_login_signs_in_and_sets_cookie(client, make_client):
    register(client)
    other_browser = make_client()

    response = login(other_browser)

    assert response.status_code == 200
    assert response.json()["email"] == EMAIL
    assert "httponly" in response.headers["set-cookie"].lower()
    assert other_browser.get("/api/auth/me").status_code == 200


def test_login_ignores_email_case(client, make_client):
    register(client)

    assert login(make_client(), email="STUDENT@SFU.CA").status_code == 200


def test_login_wrong_password_and_unknown_email_look_the_same(client, make_client):
    register(client)

    wrong_password = login(make_client(), password="wrong password")
    unknown_email = login(make_client(), email="nobody@sfu.ca")

    assert wrong_password.status_code == unknown_email.status_code == 401
    assert wrong_password.json() == unknown_email.json()
    assert "set-cookie" not in wrong_password.headers
    assert "set-cookie" not in unknown_email.headers


def test_each_login_gets_a_fresh_session_token(client, make_client):
    register(client)
    first, second = make_client(), make_client()
    login(first)
    login(second)

    assert first.cookies[settings.session_cookie_name] != second.cookies[settings.session_cookie_name]


# ---------- Current user ----------

def test_me_requires_sign_in(client):
    response = client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_me_rejects_a_made_up_cookie(client):
    client.cookies.set(settings.session_cookie_name, "made-up-token")

    assert client.get("/api/auth/me").status_code == 401


def test_me_rejects_an_expired_session(client, session_factory):
    register(client)
    with session_factory() as db:
        row = db.scalar(select(UserSession))
        row.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)
        db.commit()

    assert client.get("/api/auth/me").status_code == 401


# ---------- Logout ----------

def test_logout_ends_the_session_and_clears_the_cookie(client):
    register(client)

    response = client.post("/api/auth/logout")

    assert response.status_code == 204
    assert response.content == b""
    assert f"{settings.session_cookie_name}=" in response.headers["set-cookie"]
    assert client.get("/api/auth/me").status_code == 401


def test_logout_invalidates_the_token_on_the_server(client, make_client):
    register(client)
    stolen_token = client.cookies[settings.session_cookie_name]

    client.post("/api/auth/logout")

    replay = make_client()
    replay.cookies.set(settings.session_cookie_name, stolen_token)
    assert replay.get("/api/auth/me").status_code == 401


def test_logout_only_ends_this_browsers_session(client, make_client):
    register(client)
    other_browser = make_client()
    login(other_browser)

    client.post("/api/auth/logout")

    assert other_browser.get("/api/auth/me").status_code == 200


def test_logout_when_not_signed_in_is_fine(client):
    assert client.post("/api/auth/logout").status_code == 204
