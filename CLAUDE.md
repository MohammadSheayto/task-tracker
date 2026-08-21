# CLAUDE.md — Task Tracker

Project memory for Claude Code sessions in this repository. Facts below are
verified against the source files cited; do not assume typical-FastAPI behavior
that is not listed here.

## Tech stack

- Python 3.10 in the local `venv/` (CI and Docker use Python 3.11 — see notes)
- FastAPI 0.115.0, Pydantic v2 (2.9.2), Uvicorn 0.30.6 (`requirements.txt`)
- pytest 8.3.2 + httpx 0.27.2 (TestClient) for tests
- Vanilla HTML/CSS/JavaScript frontend in `frontend/index.html` — no framework, no build step

## Commands

- Run the app: `uvicorn app.main:app --reload --port 8000`
- Run tests: `pytest -v` (26 tests; quick form: `pytest tests -q`)
- Serve the frontend: `python -m http.server 5500`, then open
  `http://localhost:5500/frontend/index.html`

## Architecture

- `app/main.py` — FastAPI app, CORS middleware, all routes:
  `GET /health`, `POST /tasks` (201), `GET /tasks` (supports `?overdue=` and
  `?tag=` query filters), `GET /tasks/{id}`, `PATCH /tasks/{id}`,
  `DELETE /tasks/{id}` (204). Unknown ids → 404.
- `app/models.py` — Pydantic models and ALL validation rules
  (`TaskCreate`, `TaskUpdate`, `TaskResponse`, `TaskStatus`, `TaskPriority`,
  `_validate_title`, `_validate_tags`).
- `app/storage.py` — in-memory dict store (`TaskStorage`), module-level
  singleton, CRUD functions. Data is lost on restart by design (ADR-001);
  SQLite is planned for a later module.
- `app/config.py` — env config via python-dotenv (`APP_ENV`, `PORT`).
- `frontend/index.html` — Kanban board: 3 status columns, priority sorting,
  4 UI states (loading/ready/empty/error), HTML5 drag-and-drop with optimistic
  update + rollback, create/edit modal, overdue filter, tag chips/filter.
- `tests/test_tasks.py` (12) and `tests/test_midcourse_features.py` (14).

## Business rules (as implemented — verified in app/models.py)

- Status values are exactly: `ToDo`, `InProgress`, `Done`.
  **No transition restrictions are implemented** — any status may change to
  any other status. Do not invent transition rules.
- Priority values are exactly: `Low`, `Medium`, `High`. Display order on the
  board is High → Medium → Low.
- Title: required, trimmed, non-blank, max 200 chars → otherwise 422.
- Tags: trimmed, blank values rejected (422), deduped preserving order,
  max 10 tags, max 30 chars each. `GET /tasks?tag=x` is exact, case-sensitive.
- `due_date`: optional ISO `YYYY-MM-DD`; invalid format → 422. Past dates are
  allowed. Overdue = `due_date < today AND status != Done` (`_is_overdue` in
  app/main.py).
- All request models use `extra="forbid"` → unknown fields return 422.
- PATCH semantics: a field set to `null`/omitted is NOT updated. Consequence:
  `assignee` and `due_date` cannot be cleared once set; `tags` CAN be cleared
  by sending `[]`. This is a documented, deliberate limitation.

## UI states and CORS

- The board has four explicit states: loading, ready, empty (columns stay
  visible with count 0), error (with Retry).
- CORS allowlist in app/main.py: `http://localhost:5500` and
  `http://127.0.0.1:5500` only. Opening the frontend via `file://` will be
  blocked — serve it on port 5500.

## Do-not rules

- Do not add authentication, a database, or deployment steps without asking.
- Do not add frameworks, build tools, or new dependencies without asking.
- Do not invent status transition rules or validation the code does not have.
- Do not weaken tests to make them pass; fix the source or ask.
- Do not commit `.env` or secrets; `.env.example` is the template.
- Show diffs before applying large or multi-file edits.
