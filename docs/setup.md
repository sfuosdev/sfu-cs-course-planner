# Local Setup Guide

This guide assumes basic Git, Node.js, Python, and Docker familiarity.

## Prerequisites

- Git
- Node.js 20+
- Python 3.12+
- Docker + Docker Compose

## 1) Clone and configure

```bash
git clone <your-fork-url>
cd sfu-cs-course-planner
cp .env.example .env
```

## 2) Start PostgreSQL

```bash
docker compose up -d db
```

Stop it when done:

```bash
docker compose down
```

## 3) Run backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 4) Run frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

## 5) Run tests

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
