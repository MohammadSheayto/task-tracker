# Architecture — Strategy A (minimal context)

<!-- Produced from the minimal task description only, with free repo
     inspection allowed. Compare with B and C in docs/architecture.md. -->

**What the app does.** Task Tracker: a FastAPI REST API for creating,
listing, updating, and deleting tasks, with a single-page Kanban board
frontend. Data lives in an in-memory store and is lost on restart.

**Data model.** One entity, `Task`: id (UUID string), title, description,
status (`ToDo`/`InProgress`/`Done`), priority (`Low`/`Medium`/`High`),
assignee (nullable), due_date (nullable ISO date), tags (list of strings),
created_at/updated_at (UTC).

**Request flow (create a task).** Browser modal → `POST /tasks` with JSON →
CORS middleware admits the :5500 origin → Pydantic validates `TaskCreate`
(422 on bad title/tags/date/unknown fields) → `storage.add_task()` writes to
the module-level dict store → `TaskResponse` returned with 201 → frontend
refetches `GET /tasks` and re-renders.

**Key files.** `app/main.py` (routes, CORS, overdue filter), `app/models.py`
(validation), `app/storage.py` (dict store), `app/config.py` (env),
`frontend/index.html` (entire UI), `tests/test_tasks.py` +
`tests/test_midcourse_features.py`, `.github/workflows/ci.yml`, `Dockerfile`.

**Conventions.** All validation in Pydantic models (`extra="forbid"`);
storage returns `None`/`False` for missing ids and routes convert that to
404; frontend renders exclusively via `textContent`; filters are query
params; tests use one shared TestClient with a store-clearing fixture.

**Assumptions / risk of generic filler.** Written with full repo access, so
facts are grounded; the risk in this strategy is that nothing forced the
draft to distinguish repo fact from FastAPI convention — e.g. the 422
behavior claims would read identically for any FastAPI app.
