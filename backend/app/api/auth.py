"""Account registration, login and logout endpoints."""

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.config import settings
from app.db import get_db
from app.models import User
from app.schemas.auth import LoginRequest, RegisterRequest, UserResponse
from app.schemas.course_responses import ErrorResponse
from app.services.auth import (
    EmailAlreadyRegisteredError,
    authenticate,
    create_session,
    create_user,
    delete_session,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        max_age=settings.session_ttl_days * 24 * 60 * 60,
        path="/",
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
    )


def _clear_session_cookie(response: Response) -> None:
    response.delete_cookie(
        key=settings.session_cookie_name,
        path="/",
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
    )


@router.post(
    "/register",
    status_code=201,
    response_model=UserResponse,
    responses={409: {"model": ErrorResponse}},
    summary="Create an account and sign in",
)
def register(
    payload: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> User:
    try:
        user = create_user(db, payload.email, payload.password, payload.username)
    except EmailAlreadyRegisteredError as exc:
        raise HTTPException(
            status_code=409, detail="An account with this email already exists"
        ) from exc

    _set_session_cookie(response, create_session(db, user))
    return user


@router.post(
    "/login",
    response_model=UserResponse,
    responses={401: {"model": ErrorResponse}},
    summary="Sign in with email and password",
)
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> User:
    user = authenticate(db, payload.email, payload.password)
    if user is None:
        # Same message whether the email or the password was wrong.
        raise HTTPException(status_code=401, detail="Invalid email or password")

    _set_session_cookie(response, create_session(db, user))
    return user


@router.post("/logout", status_code=204, summary="Sign out")
def logout(
    response: Response,
    session_token: str | None = Cookie(default=None, alias=settings.session_cookie_name),
    db: Session = Depends(get_db),
) -> None:
    """End the current session. Safe to call when not signed in."""
    if session_token:
        delete_session(db, session_token)
    _clear_session_cookie(response)


@router.get(
    "/me",
    response_model=UserResponse,
    responses={401: {"model": ErrorResponse}},
    summary="Get the signed-in user",
)
def read_current_user(user: User = Depends(get_current_user)) -> User:
    return user
