# Task Tracker

## Project overview

A learning project: a REST API for tracking tasks (Python/FastAPI, in-memory
store per ADR-001) with a vanilla HTML/CSS/JavaScript Kanban board frontend.
Built incrementally across course Modules 1–4: API + validation (M1–M2),
Kanban frontend (M3), feature extensions on branch `mid-course-project`
(due dates + overdue filter, tags), and CI/Docker/documentation hardening (M4).

API endpoints: `GET /health`, `POST /tasks` (201), `GET /tasks`
(`?overdue=true|false`, `?tag=<value>`), `GET /tasks/{id}`,
`PATCH /tasks/{id}`, `DELETE /tasks/{id}` (204). Unknown ids → 404,
validation errors → 422.

## Prerequisites

- Python 3.10+ locally (CI and Docker use Python 3.11)
- pip
- Docker Desktop (only for the container workflow)

## Local setup

```bash
python -m venv venv
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt

# Windows PowerShell:
Copy-Item .env.example .env
# Linux/macOS:
cp .env.example .env
```

## Run the app locally

```bash
uvicorn app.main:app --reload --port 8000
```

Check it: `curl http://127.0.0.1:8000/health` → `{"status":"ok", ...}`.
Swagger UI: http://127.0.0.1:8000/docs

### Run the frontend (Kanban board)

The board lives in `frontend/index.html` and calls the API at
`http://localhost:8000`. Serve it on port 5500 (the CORS allowlist covers
`http://localhost:5500` and `http://127.0.0.1:5500`; opening via `file://`
is blocked):

```bash
python -m http.server 5500
# then open http://localhost:5500/frontend/index.html
```

Board features: three status columns, priority sorting (High → Medium → Low),
loading/empty/error/ready states, drag-and-drop with PATCH + rollback,
create/edit modal with validation and 422 display, due/overdue pills with an
"Overdue only" filter, and tag chips with click-to-filter.

## Run tests

```bash
pytest -v
```

26 tests: `tests/test_tasks.py` (core CRUD/validation) and
`tests/test_midcourse_features.py` (due dates, overdue filter, tags).

## Run with Docker

The container serves the **API only** (the frontend is served separately as
above). Multi-stage build, `python:3.11-slim`, runs as non-root user `app`:

```bash
docker build -t task-tracker:dev .
docker run -d --name tt-dev -p 8000:8000 task-tracker:dev
curl http://localhost:8000/health
docker exec tt-dev whoami   # expected: app
docker rm -f tt-dev
```

Verification checklist and security log: `docs/module4/docker-verification.md`.

## CI workflow

`.github/workflows/ci.yml` runs on every push and pull request: checkout →
Python 3.11 (pinned) → `pip install -r requirements.txt` → `pytest -v`.
There is deliberately no `continue-on-error`, `|| true`, or `--exit-zero` —
a failing test fails the run. Green→red→green proof: `docs/module4/ci-evidence.md`.
Design rationale: [docs/decisions/ci-workflow-design.md](docs/decisions/ci-workflow-design.md).

## Project structure

```
app/
  main.py       # FastAPI app, CORS, all routes, overdue filter logic
  models.py     # Pydantic models + ALL validation rules
  storage.py    # In-memory dict store (module-level singleton)
  config.py     # Env config via python-dotenv
frontend/
  index.html    # Kanban board (vanilla HTML/CSS/JS, single file)
tests/
  test_tasks.py                 # Core API tests (12)
  test_midcourse_features.py    # Due dates + tags tests (14)
docs/
  midcourse/    # Mid-course project deliverables
  module4/      # Module 4 evidence logs (review triage, claim-vs-reality, CI, Docker)
  decisions/    # Technical decision notes (CI design, comments feature plan)
  security-review.md / governance-worksheet.md / ai-playbook.md   # Module 5
  architecture.md (+ architecture-A/B/C.md)                       # Module 5 context experiment
.github/workflows/ci.yml
Dockerfile / .dockerignore
CLAUDE.md       # Project memory for Claude Code sessions
```

## Conventions and current limitations

- Status values are exactly `ToDo`, `InProgress`, `Done` — **no transition
  restrictions are implemented**; any status may move to any other.
- Storage is in-memory by design: all tasks are lost on restart. SQLite is
  planned for a later module. Not thread-safe; no auth; not production-ready.
- PATCH semantics: omitted/`null` fields are not updated — so `assignee` and
  `due_date` cannot be cleared once set; `tags` can be cleared with `[]`.
- Overdue = `due_date < today AND status != Done`, computed server-side for
  the filter and client-side for the card pill (may briefly disagree around
  midnight across timezones).
- Tag filtering is exact and case-sensitive.

## Decision notes

- [CI workflow design](docs/decisions/ci-workflow-design.md)
- [Mid-course mini-ADR: due dates + tags](docs/midcourse/mini-adr.md)
- [Comments feature plan (Module 5, plan-only)](docs/decisions/comments-feature-plan.md)
- [Security review](docs/security-review.md) · [Architecture](docs/architecture.md) · [AI playbook](docs/ai-playbook.md)
