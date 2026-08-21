# Comments Feature Plan — Module 5 (Part 5.4)

Planning exercise only — **no implementation**. Comment shape (given):
`id` (UUID), `task_id`, `author` (1–100 chars), `body` (1–2000 chars),
`created_at` (server UTC).

---

## Plan 1 — Generic (no repo knowledge)

**Data Model:** A `Comment` model/table with the five fields; FK to tasks;
ORM entity or Pydantic schema pair (Create/Response).
**API Routes:** `POST /tasks/{task_id}/comments` (201), `GET /tasks/{task_id}/comments`,
`DELETE /comments/{comment_id}` (204). 404 for unknown task/comment; 422 for
blank author/body.
**Tests:** create/list/delete happy paths; blank body 422; unknown task 404.
**Frontend:** a comments section in whatever task-detail view exists; a count
badge on task cards.
**Migration:** add a comments table/collection; backfill not needed.
**Assumptions this plan makes:** there is a database with migrations; there
is a task-detail page; test framework unknown; file layout unknown; auth
unknown.

## Plan 2 — Repo-grounded (files read: AGENTS.md, app/models.py, app/main.py, app/storage.py, tests/, frontend/index.html)

**1. Data Model** — In `app/models.py`, following the existing pattern:
`CommentCreate` (author, body; `extra="forbid"`; trim/length validators in
the style of `_validate_title`) and `CommentResponse` (adds id, task_id,
created_at). No ORM — this repo has none.

**2. API Routes** — In `app/main.py`, nested under tasks like the existing
routes: `POST /tasks/{task_id}/comments` → 201/404/422;
`GET /tasks/{task_id}/comments` → 200 list (empty list, not 404, for a task
with no comments — matches `GET /tasks` returning `[]`);
`DELETE /tasks/{task_id}/comments/{comment_id}` → 204/404. Reuse the
`HTTPException(404, "…not found")` phrasing already used for tasks.

**3. Storage** — In `app/storage.py`: comments stored per-task, either a
`comments: list` inside each task dict or a parallel
`_comments: dict[str, list]` keyed by task_id. **Deleting a task must delete
its comments** — the existing `delete()` needs a companion change.

**4. Tests** — New `tests/test_comments.py` using the existing pattern
(module-level `TestClient`, autouse `clean_storage` fixture, `create_task`
helper): `test_add_comment_returns_201`, `test_add_comment_blank_body_422`,
`test_add_comment_unknown_task_404`, `test_list_comments_empty_for_new_task`,
`test_delete_comment_then_list_excludes_it`,
`test_comments_removed_when_task_deleted`.

**5. Frontend** — `frontend/index.html` has **no task-detail page** — the
natural home is a comments section inside the existing edit modal (fetch on
open, add via textarea + button, count shown on the card meta row). All text
must go through `textContent` like existing rendering.

**6. Migration notes** — In-memory store resets on restart, so no data
migration; but `TaskResponse` has `extra="forbid"` — if comments are embedded
in the task dict, `TaskResponse(**task_data)` **breaks** unless the field is
added or comments live in the separate dict (safer).

**Open Questions:** (1) Do comments belong on `TaskResponse` (embedded) or
only behind `GET .../comments` (separate)? Separate avoids the forbid-break.
(2) Should comment deletion require anything (no auth exists)? (3) Does the
modal fetch comments lazily or should `GET /tasks` return counts?
(4) Cap comments per task (cf. security review SR-3 unbounded growth)?

---

## Critique (5.4C)

| Section | Label | Evidence | Minimal correction |
|---|---|---|---|
| Generic: Data Model | Needs-Resequencing | Assumes ORM/DB — repo has a plain dict store. | Point at `app/storage.py` singleton pattern. |
| Generic: Routes | Right (shape) / Missing (conventions) | Paths are sensible, but `DELETE /comments/{id}` breaks this repo's task-nested convention. | Nest under `/tasks/{task_id}/…`. |
| Generic: Frontend | Missing | Assumes a task-detail page that does not exist. | Use the edit modal in `frontend/index.html`. |
| Repo-grounded: Data Model | Right | Mirrors `_validate_title` pattern, `extra="forbid"`. | — |
| Repo-grounded: Storage | Right | Catches the cascade-delete and the `TaskResponse` forbid-break — the two real traps. | — |
| Repo-grounded: Tests | Right | Names match the existing fixture style exactly. | — |

**Biggest difference:** the generic plan is correct about HTTP and wrong
about this codebase (DB, detail page, route shape); the repo-grounded plan
caught the two things that would actually break (`extra="forbid"` on
embedded comments, orphaned comments on task delete).
**Plan I would hand a teammate:** the repo-grounded one — every claim cites a
real file and its risks are this repo's risks.
**Where generic chat is enough:** naming/shaping API conventions or
brainstorming test categories before any code exists.
