# Architecture — Strategy B (structured context: AGENTS.md + file summaries)

<!-- Produced with AGENTS.md and one-line file summaries provided as context.
     Compare with A and C in docs/architecture.md. -->

**What the app does.** Course-built Task Tracker (Modules 1–5): FastAPI CRUD
API over an in-memory dict store (ADR-001; SQLite planned later), with a
no-framework Kanban frontend served separately on port 5500. Not production
software: no auth, no database, no deployment (per AGENTS.md).

**Data model.** `Task`: id UUID string; title (required, trimmed, ≤200);
description (unbounded string — flagged in docs/security-review.md SR-2);
status exactly `ToDo`/`InProgress`/`Done` with **no transition rules**;
priority `Low`/`Medium`/`High`; assignee (nullable, unbounded); due_date
(nullable ISO date, past allowed); tags (trimmed, deduped, ≤10×30 chars);
created_at/updated_at UTC. All request models `extra="forbid"`.

**Request flow (create a task).** Modal submit in `frontend/index.html` →
client trims title (blocks blank before any request) → `POST /tasks` →
CORSMiddleware (allowlist: localhost/127.0.0.1:5500) → `TaskCreate`
validators (`_validate_title`, `_validate_tags`) → `storage.add_task()` →
201 `TaskResponse` → frontend `loadTasks()` refetch → `renderBoard()` sorts
High→Medium→Low per status column.

**Key files.** `app/main.py` — routes + `_is_overdue` + query filters
(`?overdue=`, `?tag=`); `app/models.py` — all validation; `app/storage.py` —
`TaskStorage` singleton + `clear_tasks()` test helper; `app/config.py` —
dotenv (`APP_ENV`, `PORT`); `frontend/index.html` — board, 4 UI states,
drag-drop with rollback, modal; `tests/` — 26 tests, two files;
`.github/workflows/ci.yml` — Python 3.11, `pytest -v`; `Dockerfile` —
multi-stage, non-root `app` user.

**Conventions.** Validation lives only in models; PATCH treats `null` as
"not provided" (so assignee/due_date cannot be cleared; `tags: []` can);
unknown ids → 404 with detail "Task not found"; overdue = due before today
AND not Done (server-side for the filter, client-side for the pill);
frontend inserts all user text via `textContent`.

**Not confirmed from provided context.** Local Python is 3.10 per AGENTS.md
— venv contents not re-inspected here; Docker runtime behavior unverified on
this machine (see docs/module4/docker-verification.md).
