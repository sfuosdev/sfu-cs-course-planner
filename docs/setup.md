# Local Setup

This guide covers the FastAPI backend and the React frontend. Database and
Docker setup will be documented as issues #11 and #35 are completed.

## Prerequisites

- Git
- Python 3.12 (the version used by CI)

The frontend uses Vite, which requires Node.js 20.19+ or 22.12+, and npm.

## Get the code

1. Fork https://github.com/sfuosdev/sfu-cs-course-planner on GitHub.
2. Clone your fork and add the official repository as `upstream`:

   ```bash
   git clone https://github.com/YOUR_USERNAME/sfu-cs-course-planner.git
   cd sfu-cs-course-planner
   git remote add upstream https://github.com/sfuosdev/sfu-cs-course-planner.git
   git remote -v
   ```

## Set up and run the backend

Create and activate a virtual environment from the repository root, then install
the backend dependencies:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r backend/requirements.txt
```

Copy `.env.example` to `.env` in the repository root to override the defaults.
The app reads `APP_NAME`, `APP_VERSION`, `APP_ENV`, and `DEBUG` from that file or
from the process environment.

Start the development server from the `backend` directory:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

The API is available at <http://127.0.0.1:8000>. The liveness endpoint is
`/health`; interactive Swagger documentation is at `/docs`, ReDoc is at
`/redoc`, and the OpenAPI schema is at `/openapi.json`.

## Run backend tests

From the repository root:

```bash
python -m pytest backend/tests -q
```

## Run the frontend

From the repository root:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite (usually `http://localhost:5173`). To create
and preview a production build, run `npm run build` and then `npm run preview`
from `frontend/`.

## Run the backend tests

From the repository root, create a virtual environment and install the backend
dependencies (first time only):

```bash
cd backend
python -m venv .venv
```

Activate it:

- Windows (PowerShell): `.venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Then install and run the tests:

```bash
pip install -r requirements.txt
python -m pytest
```

Run the tests from `backend/` so Python can find the `app` package. The tests don't
need a database.
