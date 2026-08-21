# Task Tracker

A learning project: a REST API for tracking tasks, built with Python and
FastAPI, plus a vanilla HTML/CSS/JavaScript Kanban board frontend
(Module 3). Per ADR-001, the implementation uses an in-memory
dictionary store, with a planned migration path to SQLite in a later
module.

API endpoints: `GET /health`, `POST /tasks`, `GET /tasks`,
`GET /tasks/{id}`, `PATCH /tasks/{id}`, `DELETE /tasks/{id}`.

## Requirements

- Python 3.10+
- pip

## Setup

1. Clone or copy this project, then from the project root create and
   activate a virtual environment:

   **Linux/macOS:**
```bash
   python3 -m venv venv
   source venv/bin/activate
```

   **Windows PowerShell:**
```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
   pip install -r requirements.txt
```

3. Create your local environment file from the example:

   **Linux/macOS:**
```bash
   cp .env.example .env
```

   **Windows PowerShell:**
```powershell
   Copy-Item .env.example .env
```

## Run

From the project root:

```bash
uvicorn app.main:app --reload --port 8000
```

The `--reload` flag restarts the server automatically on code changes
(development only).

## Test the health endpoint

```bash
curl http://127.0.0.1:8000/health
```

Expected response shape:

```json
{
  "status": "ok",
  "timestamp": "2026-08-14T12:34:56.789012+00:00"
}
```

## Run the frontend (Module 3 Kanban board)

The board lives in `frontend/index.html` and calls the API at
`http://localhost:8000`. Serve it on port 5500 (the backend's CORS
allowlist covers `http://localhost:5500` and `http://127.0.0.1:5500`):

- **VS Code Live Server:** right-click `frontend/index.html` → *Open with
  Live Server* (default port 5500), or
- **Python:** from the project root run `python -m http.server 5500`,
  then open http://localhost:5500/frontend/index.html

Start the backend first (`uvicorn app.main:app --reload --port 8000`),
otherwise the board shows its error state with a Retry button.

Board features: three status columns (To Do / In Progress / Done), cards
sorted High → Medium → Low, loading/empty/error/ready states,
drag-and-drop that PATCHes the backend with rollback on failure, and a
create/edit modal with title validation and server 422 handling.

## Run the tests

```bash
pytest tests/test_tasks.py -q
```

Covers `POST /tasks`, `GET /tasks`, `PATCH /tasks/{id}` (validation,
partial updates, 404s), and `DELETE /tasks/{id}`.

## API documentation (Swagger UI)

With the server running, open:

http://127.0.0.1:8000/docs