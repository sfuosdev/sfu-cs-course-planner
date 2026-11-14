# Architecture

> This describes the planned design. Most of it isn't built yet.

## Components

| Component | Technology              | Responsibility                                      |
| --------- | ----------------------- | --------------------------------------------------- |
| Frontend  | React, TypeScript, Vite | User interface and course planning interactions     |
| Backend   | Python, FastAPI         | REST API, business logic and data processing        |
| Database  | PostgreSQL, SQLAlchemy  | Application data, user information and course plans |
| Adminer   | Adminer                 | Browser-based inspection of the local database      |

## How they connect

React frontend -> REST API -> FastAPI backend -> SQLAlchemy -> PostgreSQL

## Course data

`docs/sfucourses-api.json` is a Swagger 2.0 description of the sfucourses API
(`api.sfucourses.com`), an unofficial API not affiliated with SFU. The backend
integration in `backend/app/services/sfu_courses.py` retrieves outlines and parsed
prerequisite trees, and exposes normalized course data through `GET /courses`.
Descriptions are returned as plain text. The provider URL and request timeout can be
set with `SFU_COURSES_API_BASE_URL` and `SFU_COURSES_API_TIMEOUT_SECONDS`.

## Repository layout

- `frontend/src/`: `components/`, `pages/` and `services/`
- `backend/app/`: `api/`, `models/`, `schemas/` and `services/`
- `backend/tests/`: backend tests
- `docs/`: project documentation
