# Security Review — Module 5 (Part 5.2)

Read-only audit. No `app/` files were modified. Files inspected:
`app/main.py`, `app/models.py`, `app/storage.py`, `app/config.py`,
`tests/`, `requirements.txt`, `Dockerfile`, `.dockerignore`,
`.github/workflows/ci.yml`, `frontend/index.html`, `AGENTS.md`.

## 1. AI audit findings

| ID | Severity | File / location | Finding | Evidence | Suggested next step | Confidence |
|---|---|---|---|---|---|---|
| SR-1 | High (production) / Accepted (course) | `app/main.py` (all routes) | No authentication or authorization on any endpoint; anyone who can reach the API can read/modify/delete all tasks. | No auth dependency or middleware anywhere in `app/`. | Document as course-scope decision; must be resolved before any real deployment. | High |
| SR-2 | Medium | `app/models.py` `TaskCreate`/`TaskUpdate` | `description` and `assignee` have **no length limits** (title is capped at 200, tags at 10×30 — these two fields are not). A client can POST a multi-megabyte description. | No validator on either field; storage keeps the full string in memory. | Add max-length validation (e.g. description ≤ 2000, assignee ≤ 100) — backlog. | High |
| SR-3 | Medium (low likelihood locally) | `app/storage.py` | Unbounded in-memory growth: no cap on task count and no request-size limit → memory-exhaustion DoS against the dict store. | `TaskStorage._tasks` grows without limit; uvicorn default has no body-size cap. | Accept for course scope; note as risk until the SQLite migration. | High |
| SR-4 | Low | `app/main.py` (Pydantic 422 responses) | Validation errors echo the submitted input back in the `input` field of the 422 body (Pydantic v2 default) — minor information reflection. | Any 422 response includes the rejected value. | No action for course scope. | Medium |
| SR-5 | Low | `app/main.py` CORS middleware | `allow_methods=["*"]` / `allow_headers=["*"]`; origins are correctly allowlisted to the two local :5500 origins and credentials are not enabled. | CORS block in `app/main.py`. | No action — origins allowlist is the control that matters here. | High |
| SR-6 | Low | `app/main.py` `list_tasks` | `GET /tasks` returns the entire store with no pagination — a resource concern at scale, not a vulnerability at course scale. | Route returns `storage.get_all_tasks()` directly. | No action for course scope. | High |

**Categories with no issue found (checked, not skipped):**

- Secrets: `.env` is git-ignored and docker-ignored; `.env.example` holds only
  placeholder keys; no secrets in code, image, or workflow.
- Docker: pinned `python:3.11-slim`, multi-stage, non-root `USER app`, no
  `--reload`, no `COPY . .`.
- CI: no `continue-on-error` / `|| true` / `--exit-zero`; `pytest -v` exit
  code is the job result.
- XSS: all task/tag text enters the DOM via `createElement`/`textContent`
  (`frontend/index.html`); `innerHTML` is never used for user data.
- SQL/command injection: not applicable — no SQL, no shell-outs.

## 2. Grading (Valid / False Positive / Noise)

| Finding | Grade | Reason |
|---|---|---|
| SR-1 no auth | **Valid** (course-scope) | Real production risk, intentionally out of course scope — the distinction the module asks for. |
| SR-2 unbounded description/assignee | **Valid** | Genuine validation gap inconsistent with the rest of the model (title/tags are capped). |
| SR-3 unbounded store growth | **Valid** (accepted risk) | True, but inherent to the ADR-001 in-memory design; fix belongs with the SQLite migration. |
| SR-4 422 input echo | **Noise** | Default framework behavior; no sensitive data in this app to reflect. |
| SR-5 CORS wildcard methods/headers | **Noise** | Technically true, not actionable: origin allowlist + no credentials is the effective control. |
| SR-6 no pagination | **Noise** | Performance concern, not security; irrelevant at course scale. |

## 3. Manual scan (human-owned)

> Confirm or extend these — this column is the point of the exercise.
> The two findings below came from human review during Module 4, not from
> the AI audit prompt above.

- **M-1:** PATCH `null`-means-omitted semantics mean a client can never clear
  `assignee`/`due_date` — a data-governance quirk (stale personal data cannot
  be removed via the API) that pure vulnerability scanning does not surface.
- **M-2:** Overdue is computed with **server-local** `date.today()` in the
  filter but **UTC** in the frontend pill — a timezone-dependent consistency
  gap a generic audit misses because it needs cross-file business context.

## 4. Reconciliation

| Agreement | AI-only | You-only |
|---|---|---|
| No auth (SR-1); unbounded strings (SR-2) — both obvious once looked for | 422 input echo (SR-4); CORS wildcard detail (SR-5) | PATCH can't-clear semantics (M-1); server-vs-client date skew (M-2) |

**Observation:** AI coverage is strong on file-local, pattern-shaped issues
(missing validators, config flags) and weak on cross-file business-logic
consequences — both You-only findings required knowing how two layers
interact, not reading one file.

## 5. Top-3 security backlog

| Rank | Finding | Why it matters | Suggested owner | Next action |
|---|---|---|---|---|
| 1 | SR-2 unbounded `description`/`assignee` | Only validation gap inconsistent with the model's own rules; cheap to fix. | backend | Add max-length validators + 2 tests (post-Module 5). |
| 2 | SR-1 no auth | Blocks any non-local deployment. | course/project owner | Keep documented in README limitations; decide auth story with SQLite module. |
| 3 | SR-3 unbounded store growth | Memory DoS on long-running instance. | backend | Fold into the SQLite migration design. |

**Optional one-line fix (5.2X): declined.** SR-2 is the candidate, but it is
two fields plus tests — beyond a one-line change — so it goes to the backlog
instead. `app/` remains untouched in Module 5, per the guardrails.
