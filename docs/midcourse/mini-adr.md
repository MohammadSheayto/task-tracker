# Mini-ADR — Due Dates + Overdue Filter, and Tags

**Status:** Accepted · **Date:** 2026-08-21 · **Branch:** `mid-course-project`

## Context

Extend the Modules 1–3 Task Tracker (FastAPI + in-memory store + vanilla JS Kanban board) with two scoped, end-to-end features. Constraints: no new dependencies, no framework, no persistence changes, keep the Module 2 validation style (`extra="forbid"`, field validators, 422 on bad input).

## Decision — Feature 1: Due dates + overdue filter

- `due_date` is an **optional `date` field** on `TaskCreate`/`TaskUpdate`/`TaskResponse`. Pydantic's ISO-date parsing provides format validation for free (bad input → 422), so no custom validator was needed.
- **Overdue is computed, not stored**: `due_date < today AND status != Done`. Stored "overdue" flags would go stale at midnight.
- The **filter runs in the backend** (`GET /tasks?overdue=true|false`) so the API is the single source of truth and the rule is unit-testable. The frontend *also* computes overdue locally for the red card pill — accepted duplication of one comparison; worst case is a brief visual mismatch around midnight if client and server clocks differ.
- **Past due dates are allowed on create.** Rejecting them would make overdue tasks impossible to enter or test, and overdue is a display/filter concern, not a validity rule.

## Decision — Feature 2: Tags

- Tags are a **plain `list[str]` on the task**, validated by a shared helper: trimmed, blank values rejected (422), duplicates removed, max 10 tags of max 30 characters.
- Filtering is a backend query parameter (`GET /tasks?tag=<value>`, exact match).
- The frontend uses a **comma-separated text input** in the modal and renders clickable chips; clicking a chip sets the tag filter.

## Alternatives considered and rejected

| Alternative (AI-suggested or considered) | Why rejected |
|---|---|
| Reject past due dates on create ("must be in the future") | Makes overdue state untestable and blocks entering existing late work. |
| Compute overdue only in the frontend | Filter logic would be untestable with pytest and duplicated per client. |
| Silently drop blank tags during normalization | Input disappearing without feedback; explicit 422 matches the project's validation style. |
| Separate `Tag` entity / normalized many-to-many | Overkill for an in-memory learning project; adds routes and lifecycle for no user value at this scale. |
| Redesign PATCH with `exclude_unset` so `null` can clear fields | Would change the Module 2 update contract for all fields mid-project; out of scope. |

## Consequences / known limitations

- Because PATCH treats `None` as "not provided" (Module 2 contract), a due date **cannot be cleared** once set (same as assignee). Tags *can* be cleared because `[]` is not `None`. Documented here deliberately rather than half-fixing one field.
- `overdue` and `tag` filters combine (both are applied when both are present).
- Tag matching is case-sensitive exact match; case-insensitive search was left out of scope.
