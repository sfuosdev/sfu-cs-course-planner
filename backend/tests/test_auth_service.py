from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import func, select

from app.models import User, UserSession
from app.services.auth import (
    EmailAlreadyRegisteredError,
    authenticate,
    create_session,
    create_user,
    delete_session,
    get_user_by_session_token,
    hash_token,
    normalize_email,
)

PASSWORD = "correct horse battery"
USERNAME = "Test user"


def session_count(db):
    return db.scalar(select(func.count()).select_from(UserSession))


# ---------- Accounts ----------

def test_normalize_email_trims_and_lowercases():
    assert normalize_email("  Student@SFU.ca ") == "student@sfu.ca"


def test_create_user_stores_a_hash_not_the_password(db):
    user = create_user(db, "Student@SFU.ca", PASSWORD, USERNAME)

    assert user.email == "student@sfu.ca"
    assert user.username == USERNAME
    assert user.password_hash != PASSWORD
    assert PASSWORD not in user.password_hash


def test_create_user_rejects_duplicate_email_ignoring_case(db):
    create_user(db, "student@sfu.ca", PASSWORD, USERNAME)

    with pytest.raises(EmailAlreadyRegisteredError):
        create_user(db, "STUDENT@sfu.ca", "another password", USERNAME)


# ---------- Login ----------

def test_authenticate_accepts_correct_password(db):
    user = create_user(db, "student@sfu.ca", PASSWORD, USERNAME)

    assert authenticate(db, "Student@sfu.ca", PASSWORD).id == user.id


def test_authenticate_rejects_wrong_password(db):
    create_user(db, "student@sfu.ca", PASSWORD, USERNAME)

    assert authenticate(db, "student@sfu.ca", "wrong password") is None


def test_authenticate_rejects_unknown_email(db):
    assert authenticate(db, "nobody@sfu.ca", PASSWORD) is None


# ---------- Sessions ----------

def test_session_token_resolves_to_its_user(db):
    user = create_user(db, "student@sfu.ca", PASSWORD, USERNAME)
    token = create_session(db, user)

    assert get_user_by_session_token(db, token).id == user.id


def test_only_a_hash_of_the_token_is_stored(db):
    user = create_user(db, "student@sfu.ca", PASSWORD, USERNAME)
    token = create_session(db, user)

    row = db.scalar(select(UserSession))
    assert row.token_hash == hash_token(token)
    assert token not in row.token_hash


def test_each_session_gets_a_different_token(db):
    user = create_user(db, "student@sfu.ca", PASSWORD, USERNAME)

    assert create_session(db, user) != create_session(db, user)


def test_unknown_token_has_no_user(db):
    assert get_user_by_session_token(db, "not-a-real-token") is None


def test_expired_session_is_rejected_and_removed(db):
    user = create_user(db, "student@sfu.ca", PASSWORD, USERNAME)
    token = create_session(db, user)
    row = db.scalar(select(UserSession))
    row.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    db.commit()

    assert get_user_by_session_token(db, token) is None
    assert session_count(db) == 0


def test_delete_session_ends_only_that_session(db):
    user = create_user(db, "student@sfu.ca", PASSWORD, USERNAME)
    first = create_session(db, user)
    second = create_session(db, user)

    delete_session(db, first)

    assert get_user_by_session_token(db, first) is None
    assert get_user_by_session_token(db, second).id == user.id


def test_delete_session_ignores_unknown_token(db):
    delete_session(db, "not-a-real-token")


def test_creating_a_session_clears_expired_ones(db):
    user = create_user(db, "student@sfu.ca", PASSWORD, USERNAME)
    create_session(db, user)
    old = db.scalar(select(UserSession))
    old.expires_at = datetime.now(timezone.utc) - timedelta(days=1)
    db.commit()

    create_session(db, user)

    assert session_count(db) == 1
    assert db.scalar(select(User.id)) == user.id
