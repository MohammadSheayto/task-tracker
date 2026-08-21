# Prompt Log — Mid-Course Project

> Reconstructed from the actual Claude Code (VS Code) session on 2026-08-21.
> **Review before submitting** and adjust wording so it reflects how you would phrase these prompts yourself.

Tool used: Claude Code (agentic AI assistant) inside VS Code, working directly on the repository.

## Weak prompt → stronger prompt (required example)

**Weak:** "add due dates to tasks"

**Problem:** No file anchors, no validation rules, no decision on where overdue is computed, no scope limits — the assistant is free to invent a date format, reject past dates, or rewrite working files.

**Stronger (what was actually used, condensed):**
> Extend the Task Tracker with an optional `due_date` (`YYYY-MM-DD`) on create and update. Backend: add the field to TaskCreate/TaskUpdate/TaskResponse in app/models.py and to the store in app/storage.py; add `GET /tasks?overdue=true|false` where overdue means due date before today AND status is not Done. Invalid dates must return 422. Do not add dependencies, do not change other routes, do not break the existing 12 tests. Then add pytest tests following tests/test_tasks.py's fixture pattern, then the frontend (modal date field, due/overdue pill, "Overdue only" toggle) — one layer at a time, running pytest between layers.

## Feature 1: Due dates + overdue filter

**P1 — Plan before code.** Pasted the project brief and asked for a scoped plan and feature choice with the constraint "small enough to finish end-to-end with tests".
*AI returned:* Feature choice (due dates + tags), layer-by-layer plan (models → storage → route → tests → frontend), branch + baseline first.
*Decision:* **Accepted.** Baseline recorded before any change: `12 passed`.

**P2 — Backend implementation (stronger prompt above).**
*AI returned:* `Optional[date]` field on all three models, storage wiring, `_is_overdue()` helper + query param in `app/main.py`.
*Decision:* **Accepted with one correction** — the first overdue draft did not exclude `Done` tasks; corrected to `status != Done` and a test for the Done case was added (see user-stories.md).

**P3 — Tests.** "Write pytest tests for due dates using the existing TestClient + clean-storage fixture pattern: valid date, default null, invalid format 422, PATCH update, overdue=true returns only overdue (including the Done exclusion), overdue=false excludes overdue."
*AI returned:* 6 tests in `tests/test_midcourse_features.py` using relative `YESTERDAY`/`TOMORROW` constants so tests don't rot.
*Decision:* **Accepted.** Result: `18 passed`.

**P4 — Frontend integration.** "Add the date field to the modal, a due/overdue pill on cards, and an 'Overdue only' toggle that refetches via the query param. Preserve the Module 3 behavior contract: sorting, four UI states, drag-and-drop rollback, modal validation. Focused diff only."
*AI returned:* Focused edits (filter bar, `buildTasksUrl()`, pill rendering with `textContent`).
*Decision:* **Accepted.**

## Feature 2: Tags / labels

**P5 — Backend with explicit validation rules.** "Add `tags: list[str]` — trim each tag, reject blank values with 422, dedupe preserving order, max 10 tags, max 30 chars each; `GET /tasks?tag=x` exact match. Same files and constraints as Feature 1."
*AI returned:* Shared `_validate_tags()` helper used by both create and update models, storage wiring, query param.
*Decision:* **Accepted with one correction** — the draft normalization silently dropped blank tags; changed to raise 422 (see mini-adr.md).

**P6 — Tests.** "One test per rule: trim+dedupe, default empty list, blank tag 422, >10 tags 422, PATCH replaces list, tags preserved after unrelated PATCH, filter by tag, unknown tag returns 200 + []."
*AI returned:* 8 tests in the same file/pattern.
*Decision:* **Accepted.** Result: `26 passed`.

**P7 — Frontend.** "Comma-separated tags input in the modal (pre-filled on edit, `[]` clears), clickable chips on cards that set the tag filter, active-filter chip with × to clear. Escape all tag text. Focused diff."
*AI returned:* `parseTagsInput()`, chip rendering via `createElement`/`textContent`, filter slot.
*Decision:* **Accepted.**

## Refactor + verification prompts

**P8 — Break Tests.** "Prove two tests by deliberate source breakage: invert the overdue comparison, and revert blank-tag rejection to silent skip. Capture the failing output, restore, re-run."
*AI returned / result:* Exactly the expected tests failed in each break (see verification.md), source restored, `26 passed` again.
*Decision:* **Accepted** — both tests demonstrably catch the bug they claim to catch.

**P9 — Focused refactor.** "Extract the duplicated title validator in app/models.py into one `_validate_title` helper. Behavior must not change; re-run the full suite."
*AI returned:* Shared helper mirroring the `_validate_tags` pattern.
*Decision:* **Accepted.** `26 passed` before and after.
