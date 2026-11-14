# Local Setup

> The frontend scaffold is available. The backend, database and Docker setup
> will be documented as issues #10, #11 and #35 are completed.

## Prerequisites

- Git
- Node.js and npm
- Python 3
- Docker Desktop or Docker Engine with Docker Compose

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
