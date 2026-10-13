# SFU CS Course Planner

SFU CS Course Planner is a student-led open-source project maintained by the Simon Fraser University Open Source Development Club (SFU OS DEV).

This repository currently provides a **minimal starter codebase** for contributors to build on.

## Project overview

The long-term goal is a full-stack web application to help SFU Computing Science students plan schedules, verify prerequisites, track degree progress, and explore course availability.

### Starter functionality implemented in this repository

- React + TypeScript + Vite frontend starter
- FastAPI backend starter
- `GET /health` backend endpoint
- Frontend health status indicator connected to backend
- PostgreSQL local development service via Docker Compose
- Basic backend and frontend tests
- GitHub Actions CI workflow

### Planned features (not implemented yet)

- Student account management
- Interactive course planner
- Prerequisite checker
- Degree progress tracking
- SFU course availability integration

## Tech stack

- Frontend: React + TypeScript + Vite
- Backend: Python + FastAPI
- Database: PostgreSQL
- ORM/DB access: SQLAlchemy
- Dev environment: Docker Compose
- CI: GitHub Actions
- Testing: pytest (backend), Vitest (frontend)

## Repository structure

```text
sfu-cs-course-planner/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── ...
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   └── ...
├── docs/
│   ├── architecture.md
│   └── setup.md
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
├── .env.example
├── .gitignore
├── compose.yaml
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

## Prerequisites

- Git
- Node.js 20+
- Python 3.12+
- Docker + Docker Compose

## Local setup

1. Clone your fork and enter the repository.
2. Copy environment variables:

   ```bash
   cp .env.example .env
   ```

3. Start PostgreSQL:

   ```bash
   docker compose up -d db
   ```

4. Run backend:

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```

5. Run frontend in a new terminal:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

6. Stop services when done:

   ```bash
   docker compose down
   ```

## Running tests

Backend:

```bash
cd backend
pytest
```

Frontend:

```bash
cd frontend
npm test
npm run build
```

## Contribution workflow

See [CONTRIBUTING.md](./CONTRIBUTING.md) for full details.

## Project roadmap

- Expand API route modules beyond health checks
- Add course and prerequisite domain models
- Add planner workflows and degree requirement logic
- Integrate SFU course data sources
- Improve UI/UX and testing coverage

## Maintainers

Maintained by SFU OS DEV student contributors.
