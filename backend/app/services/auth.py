"""Account creation, password login and server-side session helpers."""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.models import User, UserSession
from app.services.passwords import hash_password, verify_password

# Checked against when a login email is unknown, so a failed login takes about as
# long whether or not the account exists.
_DUMMY_PASSWORD_HASH = hash_password("not-a-real-password")


class EmailAlreadyRegisteredError(Exception):
    """Raised when registering an email that already has an account."""


def normalize_email(email: str) -> str:
    """Emails are stored trimmed and lowercase, so lookups ignore case."""
    return email.strip().lower()


def hash_token(token: str) -> str:
    """Session tokens are high-entropy random strings, so a fast hash is enough."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _as_utc(value: datetime) -> datetime:
    # SQLite returns naive datetimes; PostgreSQL returns aware ones.
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)


def create_user(db: Session, email: str, password: str, username: str) -> User:
    normalized = normalize_email(email)
    if db.scalar(select(User.id).where(User.email == normalized)) is not None:
        raise EmailAlreadyRegisteredError(normalized)

    user = User(email=normalized, username=username, password_hash=hash_password(password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:  # two sign-ups for the same email raced
        db.rollback()
        raise EmailAlreadyRegisteredError(normalized) from exc
    return user


def authenticate(db: Session, email: str, password: str) -> User | None:
    """Return the user if the email and password match, otherwise None."""
    user = db.scalar(select(User).where(User.email == normalize_email(email)))
    if user is None:
        verify_password(password, _DUMMY_PASSWORD_HASH)
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def create_session(db: Session, user: User) -> str:
    """Start a session and return the raw token to give to the browser."""
    db.execute(delete(UserSession).where(UserSession.expires_at <= _utcnow()))

    token = secrets.token_urlsafe(32)
    db.add(
        UserSession(
            user_id=user.id,
            token_hash=hash_token(token),
            expires_at=_utcnow() + timedelta(days=settings.session_ttl_days),
        )
    )
    db.commit()
    return token


def get_user_by_session_token(db: Session, token: str) -> User | None:
    """Return the user a live session token belongs to, or None."""
    row = db.scalar(select(UserSession).where(UserSession.token_hash == hash_token(token)))
    if row is None:
        return None
    if _as_utc(row.expires_at) <= _utcnow():
        db.delete(row)
        db.commit()
        return None
    return db.get(User, row.user_id)


def delete_session(db: Session, token: str) -> None:
    """End a session. Does nothing if the token is unknown."""
    db.execute(delete(UserSession).where(UserSession.token_hash == hash_token(token)))
    db.commit()
