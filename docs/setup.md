# Local Setup

This guide covers the FastAPI backend, the PostgreSQL database and the React
frontend. The quickest way to run everything is with Docker; see
[Run everything with Docker](#run-everything-with-docker). To run the backend
and frontend directly on your machine instead, follow the sections after it.

## Prerequisites

- Git
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

That's all you need for the Docker setup. To run the backend and frontend
without Docker, you also need:

- Python 3.12 (the version used by CI)
- Node.js 20.19+ or 22.12+, and npm (required by Vite)

## Get the code

1. Fork https://github.com/sfuosdev/sfu-cs-course-planner on GitHub.
2. Clone your fork and add the official repository as `upstream`:

   ```bash
   git clone https://github.com/YOUR_USERNAME/sfu-cs-course-planner.git
   cd sfu-cs-course-planner
   git remote add upstream https://github.com/sfuosdev/sfu-cs-course-planner.git
   git remote -v
   ```

## Run everything with Docker

Docker Compose runs the whole app in containers, so you don't need to install
Python, Node.js or PostgreSQL yourself. Make sure Docker Desktop is running
before you start.

### Start the app

From the repository root:

```bash
docker compose up --build
```

The first run takes a few minutes while Docker downloads images and installs
dependencies. This starts four containers:

| Service    | URL                          | What it is                  |
| ---------- | ---------------------------- | --------------------------- |
| `frontend` | <http://localhost:5173>      | React app (Vite dev server) |
| `backend`  | <http://localhost:8000/docs> | FastAPI with Swagger docs   |
| `db`       | `localhost:5432`             | PostgreSQL 16               |
| `adminer`  | <http://localhost:8080>      | Database browser            |

The backend waits until PostgreSQL is ready before it starts. Check that it can
reach the database at <http://localhost:8000/health/db>, which should return
`{"database":"ok"}`.

The `backend` and `frontend` folders are mounted into their containers, so the
servers reload when you save a file. You don't need to rebuild after code
changes.

### Set up the database in Docker

The first time you start the app, the database is empty. In a second terminal,
from the repository root, create the tables and load data:

```bash
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.import_courses --dept MACM MATH STAT CMPT

```

`docker compose exec backend` runs a command inside the running backend
container. Any command in this guide that runs from the `backend` directory
also works this way, for example `docker compose exec backend python -m app.seed`.
Run `alembic upgrade head` again whenever you pull changes that add new
migrations.

### Everyday commands

From the repository root:

| Command                          | What it does                                     |
| -------------------------------- | ------------------------------------------------ |
| `docker compose up -d`           | Start all containers in the background           |
| `docker compose ps`              | List running containers                          |
| `docker compose logs -f backend` | Follow a container's logs (press Ctrl+C to stop) |
| `docker compose down`            | Stop and remove the containers; data is kept     |
| `docker compose up --build`      | Rebuild images, then start                       |

Rebuild with `--build` after a change to `backend/requirements.txt`,
`frontend/package.json`, or either `Dockerfile`. Dependencies are installed
when the image is built, so these changes need a rebuild.

### Troubleshooting

- **`port is already allocated`**: another program is already using that
  port, often a backend or PostgreSQL you started outside Docker. Stop it and
  try again.
- **The backend can't connect to the database**: inside a container,
  `localhost` means the container itself. The backend reaches PostgreSQL at
  `db:5432`, which `compose.yml` already sets through `DATABASE_URL`.
- **Start over with an empty database**: `docker compose down -v` deletes all
  database data. Then run `docker compose up -d` and repeat
  [Set up the database](#set-up-the-database).

## Set up and run the backend

Create a virtual environment in the `backend` directory, activate it and install
the backend dependencies:

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run the server, migrations and the seed script from `backend/` with this
environment active, so Python can find the `app` package. Tests are the
exception; see [Run backend tests](#run-backend-tests).

Copy `.env.example` to `.env` in the repository root to override the defaults.
The app reads `APP_NAME`, `APP_VERSION`, `APP_ENV`, `DEBUG`, `DATABASE_URL`,
`SFU_COURSES_API_BASE_URL`, `SFU_COURSES_API_TIMEOUT_SECONDS`, `SESSION_TTL_DAYS`,
`SESSION_COOKIE_NAME` and `SESSION_COOKIE_SECURE` from that file
or from the process environment. The session settings control sign-in cookies; the
defaults work for local development. When `APP_ENV` isn't `development`, the cookie
is marked `Secure` and browsers only send it over HTTPS. The `/courses` endpoint accepts optional `dept`
and `number` query parameters and returns course outline data from sfucourses.
Upstream errors return 502 and upstream timeouts return 504.

Start the development server from the `backend` directory:

```bash
python -m uvicorn app.main:app --reload
```

The API is available at <http://127.0.0.1:8000>. The liveness endpoint is
`/health`, and `/health/db` checks the database connection. Interactive Swagger
documentation is at `/docs`, ReDoc is at `/redoc`, and the OpenAPI schema is at
`/openapi.json`.

## Set up the database

The backend stores its data in PostgreSQL 16, which runs locally in Docker. Make
sure Docker Desktop is running before you start.

### Start PostgreSQL

From the repository root:

```bash
docker compose up -d
```

This starts two containers: `db` (PostgreSQL on port 5432) and `adminer` (a
database browser on port 8080). Check that both are running with
`docker compose ps`. Data is kept in a Docker volume, so it survives
`docker compose stop` and restarts.

The default connection settings match `compose.yml`, so you don't need a `.env`
file:

```
DATABASE_URL="postgresql+psycopg://planner:planner@localhost:5432/course_planner"
```

### Create the tables

Tables are created by [Alembic](https://alembic.sqlalchemy.org/) migrations in
`backend/alembic/versions/`. From the `backend` directory:

```bash
alembic upgrade head
```

Run this again whenever you pull changes that add new migrations.

### Load sample data

From the `backend` directory:

```bash
python -m app.seed
```

This adds a few terms, a few CMPT courses and a prerequisite, so you have data to
develop against. It skips rows that already exist, so it is safe to run more than
once. To load real courses, see [Import course data](#import-course-data).

### Import course data

From the `backend` directory, with the database running and migrated:

```bash
python -m app.import_courses --dept CMPT
```

This fetches every course in a department from the sfucourses API and saves it
to the `courses` and `prerequisites` tables. `--dept` defaults to `CMPT`. When it
finishes it prints how many courses it created and updated, and how many
prerequisite rows it saved:

```
ImportStats(created=135, updated=0, prerequisites=101)
```

The import is safe to run again. It updates existing courses instead of adding
duplicates and rebuilds each course's prerequisites, so a second run on unchanged
data prints `created=0` and leaves the row counts the same. If anything fails,
the whole import is rolled back.

A prerequisite is only linked if the required course is already in the database.
To link prerequisites from other departments (for example `MACM 101` for
`CMPT 225`), import those departments too and then import `CMPT` again:

```bash
python -m app.import_courses --dept MACM
python -m app.import_courses --dept MATH
python -m app.import_courses --dept CMPT
```

### Browse the database

Open <http://localhost:8080> and log in to Adminer with:

| Field    | Value            |
| -------- | ---------------- |
| System   | `PostgreSQL`     |
| Server   | `db`             |
| Username | `planner`        |
| Password | `planner`        |
| Database | `course_planner` |

Click a table in the sidebar to see its rows, or use **SQL command** to run a
query. Adminer's row counts show `?` for PostgreSQL; open the table to see its
data.

### Change the schema

Models live in `backend/app/models/`. After changing a model, from the `backend`
directory:

1. Generate a migration:

   ```bash
   alembic revision --autogenerate -m "describe your change"
   ```

2. Read the new file in `backend/alembic/versions/` and check it does what you
   expect. Autogenerate can miss or misread some changes.
3. Apply it:

   ```bash
   alembic upgrade head
   ```

4. Commit the migration file together with the model change.

New models must be imported in `backend/app/models/__init__.py`, or Alembic
won't see them.

### Reset the database

To delete all data and start again, from the repository root:

```bash
docker compose down -v
docker compose up -d
```

Then repeat [Create the tables](#create-the-tables) and
[Load sample data](#load-sample-data). The `-v` flag deletes the data volume, so
only use it when you want an empty database. Use `docker compose stop` to stop
the database and keep its data.

## Run backend tests

From the repository root, with the backend virtual environment active (this is
how CI runs them):

```bash
python -m pytest backend/tests -q
```

The tests don't need a database; they use an in-memory SQLite database.

### Try sign-in locally

After `alembic upgrade head` (the `user_sessions` table was added for sign-in), open
<http://localhost:8000/docs> and use the `auth` endpoints: register, then call
`GET /api/auth/me`. Swagger UI keeps the session cookie, so the `plans` endpoints
work afterwards. Or with curl:

```bash
curl -c cookies.txt -H "Content-Type: application/json" \
  -d '{"email":"me@sfu.ca","password":"correct horse battery","username":"Me"}' \
  http://localhost:8000/api/auth/register
curl -b cookies.txt http://localhost:8000/api/plans
```

## Run the frontend

From the repository root:

```bash
cd frontend
npm install
npm run dev
```

The dev server forwards every request starting with `/api` to the backend at
`http://localhost:8000` (see `frontend/vite.config.ts`), so start the backend
first. To use a different backend, set `API_PROXY_TARGET`. Docker Compose sets it
to `http://backend:8000`.

Open the local URL printed by Vite (usually `http://localhost:5173`). To create
and preview a production build, run `npm run build` and then `npm run preview`
from `frontend/`.
