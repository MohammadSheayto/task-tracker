# Governance Worksheet — Module 5 (Part 5.3)

<!-- Rows below are reconstructed from the actual Claude Code sessions in this
     repo. Add any rows from OTHER tools you used (Copilot, Cursor, chat) —
     this table should cover everything you shared, not just this repo's
     sessions. -->

## 1. What I shared with AI — risk classification

Rubric: **Low** = public/course toy code, no sensitive data. **Medium** =
private but non-sensitive context, personal identifiers, non-public material.
**High** = secrets, credentials, production config, real user data.

| Item shared | Risk | Reason | Safer future version |
|---|---|---|---|
| Task Tracker source code (all modules) | Low | Course toy project, now a public GitHub repo anyway; no proprietary logic. | Same. |
| Course prompt-library PDFs (Modules 3–5) | Medium | Instructor-authored copyrighted material pasted into a third-party tool. | Paste only the specific prompt being used, or reference by section number. |
| My real name, work email domain, and GitHub username (visible in git config / context) | Medium | Personal identifiers tied to an employer domain travel with every AI request. | Use a GitHub noreply email in git config for course repos. |
| `.env` contents | **Never shared** | `.env` is git-ignored and docker-ignored; only `.env.example` placeholders exist in the repo. | Keep the habit: placeholders in the repo, real values only local. |
| [ADD: anything shared via Copilot/Cursor/chat outside this repo] | — | — | — |

## 2. Traced generated block (5.3B) — `handleDrop()` in frontend/index.html

AI-generated in Module 3; traced line-by-line to establish ownership.

| Line(s) | What it does | Why it is there | What could break if changed | Do I own this yet? |
|---|---|---|---|---|
| `const task = tasks.find(...)` | Looks up the dragged task by id from the in-memory array. | Drop events only carry the id string (via dataTransfer), not the object. | Wrong/missing id → silent no-op (guarded on next line). | [ ] |
| `if (!task \|\| task.status === targetStatus) return;` | No-op for unknown ids and same-column drops. | Course spec: same-column drop must not send a PATCH. | Removing it → redundant PATCHes and pointless re-renders. | [ ] |
| `const previousStatus = task.status;` | Snapshots the pre-move status. | Needed for rollback if the server rejects the move. | Without it, a failed PATCH leaves the card stranded in the wrong column. | [ ] |
| `task.status = targetStatus; renderBoard(tasks);` | Optimistic update: move locally before the server confirms. | UI responsiveness — the course's chosen UX trade-off. | Removing it → card only moves after the round-trip (correct but sluggish). | [ ] |
| `fetch(..., { method: "PATCH", body: JSON.stringify({ status: targetStatus }) })` | Persists only the changed field. | PATCH semantics: send only what changes; `extra="forbid"` punishes extra fields. | Wrong body shape → 422 → rollback path triggers. | [ ] |
| `if (!response.ok) { task.status = previousStatus; renderBoard(...); showNotice(...) }` | Rollback + surface the server's message on 4xx. | Failed moves must be undone visibly, not silently kept. | Removing it → UI state silently diverges from server state. | [ ] |
| `catch { task.status = previousStatus; ... }` | Same rollback for network failure (server down). | fetch rejects on network errors, not HTTP errors — separate path required. | Removing it → optimistic move survives even though nothing was saved. | [ ] |

## 3. Personal AI usage rules (5.3C)

Grounded in actual course incidents; sharpen the wording in your voice.

| Rule category | Rule | Evidence from this course |
|---|---|---|
| Never paste | I will never paste `.env` values, credentials, tokens, or production config into any AI tool — and never paste other people's personal data. | Kept `.env` out of git, Docker, and every AI exchange all course (verified in security review). |
| Always verify | I will never accept an AI claim about business rules or security without opening the cited file: check `app/models.py` before believing a validation/transition claim, and check the exact code line before acting on a security finding. | Module 4: AI-plausible "transition rules" didn't exist (claim-vs-reality log); an XSS finding was refuted by the `textContent` insertion (review triage). |
| Record contributions | I record AI contributions in reviewable repo docs — prompt logs, review triage, claim-vs-reality — rather than in commit metadata, so the evidence is inspectable where the work lives. | `docs/midcourse/prompt-log.md`, `docs/module4/review-triage.md`, this worksheet. |
