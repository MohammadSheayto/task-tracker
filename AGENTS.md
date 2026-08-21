# AGENTS.md — Task Tracker

Repo-level instructions for AI coding agents (Codex App, Claude Code, etc.).
Everything below is grounded in actual repo files; nothing here is aspirational.

## Project summary

Learning-project REST API for tracking tasks (FastAPI, in-memory dict store
per ADR-001) with a single-file vanilla JS Kanban frontend. Built across
course Modules 1–5. Not production software: no auth, no database, no
deployment.

## Tech stack and commands (verified)

- Python 3.10 locally (`venv/`); CI and Docker use 3.11
- FastAPI 0.115.0, Pydantic 2.9.2, Uvicorn 0.30.6, pytest 8.3.2, httpx 0.27.2
- Run: `uvicorn app.main:app --reload --port 8000`
- Test: `pytest -v` (26 tests)
- Frontend: `python -m http.server 5500` → `http://localhost:5500/frontend/index.html`

## Business rules visible in the code (app/models.py, app/main.py)

- Statuses: exactly `ToDo`, `InProgress`, `Done` — **no transition rules**.
- Priorities: exactly `Low`, `Medium`, `High`; board sorts High → Low.
- Title: required, trimmed, ≤200 chars, else 422. All models `extra="forbid"`.
- Tags: trimmed, blank → 422, deduped, ≤10 tags of ≤30 chars; `?tag=` exact match.
- `due_date`: optional ISO date; past allowed; overdue = before today AND not Done.
- PATCH: omitted/`null` fields are not updated (`tags: []` does clear tags).

## Module 5 guardrails

- **Docs-first:** write only under `docs/` (and this file) unless the human
  explicitly approves another path.
- **Read-only by default** on `app/`, `tests/`, `frontend/`, CI, and Docker
  files. Module 5 permits at most one explicitly approved one-line fix.
- One bounded task per thread/session.
- Cite the actual file (and line where possible) for every claim about this
  repo; if a file is not visible, say so — do not guess or use generic
  FastAPI knowledge as if it were repo fact.

## Security and governance reminders

- Never paste, log, or commit secrets; `.env` is git-ignored and
  docker-ignored — keep it that way.
- No destructive commands (resets, force-pushes, deletions) without approval.
- Do not invent findings, rules, or test results to fill space.
- AI contributions are recorded in `docs/` evidence files (prompt logs,
  review triage, claim-vs-reality) — keep that practice for new work.
