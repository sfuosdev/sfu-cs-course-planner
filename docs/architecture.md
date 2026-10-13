# Architecture Overview

SFU CS Course Planner is organized as a monorepo with a React frontend and a FastAPI backend.

## Components

- **Frontend (`frontend/`)**: React + TypeScript + Vite client application.
- **Backend (`backend/`)**: FastAPI API service with SQLAlchemy database configuration.
- **Database (`compose.yaml`)**: PostgreSQL service for local development.

## Request flow

1. The frontend calls the backend health endpoint (`GET /health`) to verify API availability.
2. FastAPI handles requests through structured API routes.
3. SQLAlchemy is configured for PostgreSQL using environment variables.

## Current starter scope

Implemented now:

- Basic frontend shell and backend status check.
- Basic FastAPI app with CORS and `/health` endpoint.
- Local PostgreSQL service via Docker Compose.

Planned later:

- Course planning logic
- Prerequisite validation
- Degree progress tracking
- SFU data integrations
