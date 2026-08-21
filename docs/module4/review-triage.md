# AI Review + Triage — Module 4 (Parts 4.5)

Review target: diff of `mid-course-project`/`module-4` work against `main`
(Modules 1–3 baseline). Review produced by Claude Code, then each comment
triaged **Useful / Noise / Wrong** against the actual files.

## Review comments (R1 output)

| # | Location | Severity | Category | Issue | Evidence |
|---|---|---|---|---|---|
| 1 | `frontend/index.html` `isOverdue()` | medium | correctness | Frontend computes "today" in UTC (`new Date().toISOString().slice(0,10)`) while the backend uses server-local `date.today()` — near midnight (or far from UTC) the red Overdue pill and the `?overdue=true` filter can disagree. | Compare `isOverdue()` in frontend vs `_is_overdue()` in `app/main.py`. |
| 2 | `tests/test_midcourse_features.py` top | low | test | `YESTERDAY`/`TOMORROW` are computed at import time; a run that crosses midnight between import and request could flip overdue assertions. | Module-level constants vs per-test computation. |
| 3 | `frontend/index.html` card rendering | high (claimed) | correctness | "Task text is inserted into the DOM unescaped — XSS risk." | See triage: claim is false. |
| 4 | `app/storage.py` `clear_tasks()` | low | maintainability | Test helper reaches into the private `_store._tasks` attribute. | `_store._tasks.clear()` at module level. |
| 5 | `app/models.py` `TaskUpdate` | medium | correctness | PATCH treats `null` as "not provided", so `assignee` and `due_date` can never be cleared once set (`tags` can, via `[]`). | `storage.update()` only applies non-None fields. |
| 6 | `.github/workflows/ci.yml` vs local venv | low | CI | CI pins Python 3.11 but the local venv is 3.10.10 — a version-specific behavior could pass in one and fail in the other. | `python --version` → 3.10.10; workflow → `"3.11"`. |
| 7 | `Dockerfile` | low | docs | Image copies only `app/` — the container serves the API, not the Kanban frontend; a reader may expect the board at :8000. | `COPY app/ app/`; frontend excluded via `.dockerignore`. |

## Triage (R2 output)

| # | Bucket | Reason (verified against code) | Action |
|---|---|---|---|
| 1 | **Useful** | Confirmed mismatch: UTC vs server-local date. Real but low-impact for a learning project. | Accepted as known limitation; noted in mini-ADR. Fix candidate: build the local date string from `getFullYear/getMonth/getDate` instead of `toISOString`. |
| 2 | **Noise** | Technically true, astronomically unlikely in a <2s suite; fixing adds complexity for no practical gain. | No action. |
| 3 | **Wrong** | All task/tag text is inserted via `createElement` + `textContent` — `innerHTML` is never used for user data. The comment pattern-matched "user text into DOM" without reading the insertion method. | No action. Kept as the required example of a Wrong AI review comment. |
| 4 | **Noise** | Private-attribute access is contained to one documented test helper in the same package. | No action. |
| 5 | **Useful** (already handled) | Real limitation, deliberately accepted and documented in `docs/midcourse/mini-adr.md` (would require changing the Module 2 PATCH contract). | Keep documented; revisit only if a "clear field" user story appears. |
| 6 | **Useful** (accepted risk) | Version skew is real; the course mandates 3.11 in CI/Docker. Local 3.10 is documented in CLAUDE.md. | Documented. Optional: upgrade local venv to 3.11. |
| 7 | **Useful** | Reader confusion is plausible. | Addressed: README "Run with Docker" section states the container serves the API only. |

**Summary:** 4 Useful (1 fixed-by-documentation, 2 accepted+documented, 1 addressed in README), 2 Noise, 1 Wrong. The Wrong comment (#3) is the canonical case from the lecture: fluent, severe-sounding, and refuted by reading two lines of the actual insertion code.
