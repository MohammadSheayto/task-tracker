# Architecture — Strategy C (targeted context: app/main.py, app/models.py, app/storage.py only)

<!-- Produced strictly from the three anchor files. Anything else is marked
     "not visible from the files I read". Compare in docs/architecture.md. -->

**What the app does.** A FastAPI REST API for tasks: health check plus CRUD
under `/tasks`, with query filters for overdue and tag. Storage is an
in-memory dictionary; docstrings reference ADR-001 and a planned SQLite
migration.

**Data model.** `Task` (via `TaskCreate`/`TaskUpdate`/`TaskResponse`):
id UUID string, title (trimmed, ≤200, required), description, status enum
(`ToDo`/`InProgress`/`Done`), priority enum (`Low`/`Medium`/`High`),
assignee (nullable), due_date (nullable `date`), tags (validated list:
trimmed, blank→error, deduped, ≤10×30), created_at/updated_at (UTC).
All three request/response models set `extra="forbid"`.

**Request flow (create a task).** `POST /tasks` → `TaskCreate` validation
(422 on failure) → `storage.add_task()` → `TaskStorage.create()` builds the
dict with UUID + UTC timestamps → returns `TaskResponse`, route status 201.

**Key files.** `app/main.py` — app object, CORS allowlist (:5500 origins),
six routes, `_is_overdue()`; `app/models.py` — enums, validators
(`_validate_title`, `_validate_tags`), models; `app/storage.py` —
`TaskStorage` class, module singleton `_store`, public CRUD functions,
`clear_tasks()` marked "intended for test isolation".
Other files: **not visible from the files I read.**

**Conventions.** Validation only in models; storage returns `None`/`False`
for missing ids, routes raise 404 "Task not found"; PATCH updates only
non-`None` fields (`updated_at` always refreshed); overdue = due date before
`date.today()` AND status != Done.

**Not visible from the files I read.** Frontend behavior and UI states; test
count and style; CI pipeline; Docker setup; Python version; how the frontend
handles CORS or errors; whether `clear_tasks()` is used anywhere.

**What this targeted strategy likely missed.** Everything operational (CI,
Docker, tests) and every frontend/backend interaction — e.g. it cannot state
who computes overdue on the client, or that the modal blocks blank titles
before the request.
