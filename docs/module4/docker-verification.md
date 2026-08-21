# Docker Verification and Security Log — Module 4 (Part 4.3)

> **Status: Docker is not installed on this machine**, so the runtime evidence
> below is still pending. The artifacts (`Dockerfile`, `.dockerignore`) are
> complete; run these commands on a machine with Docker Desktop and paste the
> outputs where marked.

Names used: image `task-tracker:dev`, container `tt-dev`.

## Commands and expected evidence

| # | Command | Expected evidence |
|---|---|---|
| 1 | `docker build -t task-tracker:dev .` | Build succeeds; final stage based on `python:3.11-slim`. |
| 2 | `docker run -d --name tt-dev -p 8000:8000 task-tracker:dev` | Container id printed; `docker ps` shows tt-dev on 0.0.0.0:8000. |
| 3 | `curl http://localhost:8000/health` | `{"status":"ok","timestamp":"..."}` |
| 4 | `docker exec tt-dev whoami` | `app` (NOT `root`) |
| 5 | `docker exec tt-dev ls -a /home/app` | `app/` present; **no** `.env`, `venv/`, `.git/`, `tests/`, `frontend/` |
| 6 | `docker image inspect task-tracker:dev --format "{{.Config.User}}"` | `app` |
| 7 | Cleanup: `docker rm -f tt-dev` | Container removed. |

Static checks already verified in the files (no Docker needed):

- Base image is pinned `python:3.11-slim` (twice, both stages) — not `python:latest`. ✔
- Multi-stage: dependencies built in `builder`, only `/opt/venv` + `app/` copied to runtime. ✔
- `USER app` appears before `CMD`. ✔
- CMD has no `--reload`. ✔
- `.dockerignore` excludes `.env`, `.git`, `venv`/`.venv`, `__pycache__`, `.pytest_cache`, `node_modules`, editor/OS files. ✔
- No `COPY . .` — secrets cannot be baked in even without `.dockerignore`. ✔

## 3-line security log (complete after running commands)

```
Non-root:        [PASTE `docker exec tt-dev whoami` output — expected: app]
Slim base:       python:3.11-slim (both stages) — verified in Dockerfile
No baked secrets: COPY limited to requirements.txt and app/; .env in .dockerignore
                 [PASTE output of command #5 confirming no .env in the image]
```
