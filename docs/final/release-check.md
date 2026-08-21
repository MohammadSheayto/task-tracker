# Release Check — End-of-Course Project

Branch: `final-project` · Date: 2026-08-21 · Repo:
https://github.com/MohammadSheayto/task-tracker

Goal: prove the Task Tracker is a teammate-maintainable release. No product
features were added for this project — this document is verification
evidence, with commands a grader or teammate can re-run.

## 1. Test evidence

- Full suite: `pytest -v` → **26 passed** (`tests/test_tasks.py` = 12,
  `tests/test_midcourse_features.py` = 14), re-run on this branch today.
- Tests are proven meaningful, not decorative: two deliberate Break Tests
  (inverted overdue comparison; blank-tag silent-drop) made exactly the
  intended tests fail, then passed again after restore —
  `docs/midcourse/verification.md` §3.

## 2. CI evidence (GitHub Actions, real run links)

| Run | Branch | Conclusion | Link |
|---|---|---|---|
| Workflow's first run | module-4 | success | https://github.com/MohammadSheayto/task-tracker/actions/runs/32469091792 |
| Intentional red (broken test assertion) | module-4 | **failure** (as intended) | https://github.com/MohammadSheayto/task-tracker/actions/runs/32469781439 |
| Restored | module-4 | success | https://github.com/MohammadSheayto/task-tracker/actions/runs/32469871835 |
| Final branch | final-project | success | https://github.com/MohammadSheayto/task-tracker/actions/runs/32483532343 |

Workflow (`.github/workflows/ci.yml`): push + pull_request triggers, pinned
Python 3.11, `pytest -v` as the last step, no `continue-on-error` /
`|| true` / `--exit-zero`.

## 3. Docker evidence

- `Dockerfile`: multi-stage, pinned `python:3.11-slim` (both stages),
  non-root `USER app` before CMD, no `--reload`, copies only
  `requirements.txt` + `app/` (no `COPY . .`).
- `.dockerignore` excludes `.env`, `.git`, venvs, caches, docs, tests.
- Runtime verification commands and the security-log template:
  `docs/module4/docker-verification.md`. **Honest status:** Docker is not
  installed on the dev machine, so build/run/whoami outputs are pending —
  the commands are ready to paste-run on any Docker host.

## 4. Secrets sweep (run on this branch today)

- `git ls-files` → the only env-like tracked file is `.env.example`, whose
  full contents are the placeholders `PORT=8000` and `APP_ENV=development`.
- Pattern grep for `api_key / secret / token / password` assignments across
  `app/ tests/ frontend/ docs/ .github/` → **no matches**.
- `.env` is excluded by both `.gitignore` and `.dockerignore`; no
  credentials, production logs, or personal/customer data are tracked.

## 5. Required branch contents (verified via `git ls-files`)

`README.md` ✔ · `AGENTS.md` ✔ · `CLAUDE.md` ✔ ·
`.github/workflows/ci.yml` ✔ · `Dockerfile` + `.dockerignore` ✔ ·
`app/` (main.py, models.py, storage.py, config.py) ✔ ·
`frontend/index.html` ✔ · `tests/` (26 tests) ✔ ·
`docs/` (midcourse/, module4/, decisions/, security-review,
governance-worksheet, architecture set, ai-playbook, final/) ✔

## 6. Known limitations (deliberate, documented — a teammate should read these first)

- In-memory storage; all data lost on restart (ADR-001; SQLite planned).
- No authentication — top item in `docs/security-review.md` backlog.
- `description`/`assignee` lack length caps (security backlog #1, SR-2).
- PATCH `null` = "not provided": `assignee`/`due_date` cannot be cleared;
  `tags: []` can.
- Overdue computed server-local for the filter, UTC client-side for the
  pill — may briefly disagree across timezones.

## 7. Teammate handover — everything needed to take over

```bash
# run
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# frontend
python -m http.server 5500   # → http://localhost:5500/frontend/index.html
# tests
pytest -v
# container
docker build -t task-tracker:dev . && docker run -d -p 8000:8000 task-tracker:dev
```

Project memory for AI agents: `AGENTS.md` (Codex-style) and `CLAUDE.md`
(Claude Code) — both verified against source, including the
"no status-transition rules" rule that AI tools repeatedly invent.
