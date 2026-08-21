# Ownership Evidence — End-of-Course Project

Claim: AI assisted heavily across Modules 1–5, but the final result is
owned — every AI contribution was inspected, verified, corrected where
wrong, and is explainable. The evidence below is all in this repo.

## 1. Where I corrected the AI (judgment, not acceptance)

| Incident | What AI proposed | My decision | Recorded in |
|---|---|---|---|
| Overdue rule | First draft: any task with `due_date < today` is overdue | Excluded `Done` tasks — a completed task cannot be late; added a test for it | `docs/midcourse/mini-adr.md`, `tests/test_midcourse_features.py` |
| Blank tags | Silently drop blank tag values | Reject with 422 — silent data loss contradicts the API's validation style | `docs/midcourse/mini-adr.md`; proven by Break Test B |
| XSS "finding" | Review claimed unescaped task text (high severity) | Graded **Wrong**: all insertion is via `textContent`; no fix applied | `docs/module4/review-triage.md` #3 |
| Status transitions | Plausible claim that transition rules exist | Verified none exist; wrote "do not invent transition rules" into both agent-memory files | `docs/module4/claim-vs-reality.md`, `AGENTS.md`, `CLAUDE.md` |
| Python version | Template said "Python 3.11" | Documented the truth: local venv 3.10, CI/Docker 3.11 | `docs/module4/claim-vs-reality.md` |

## 2. Where I proved the work instead of trusting it

- **Tests proven by breakage:** two deliberate source breaks made exactly
  the intended tests fail (`docs/midcourse/verification.md` §3).
- **CI proven by a red run:** intentional failing commit → Actions run
  concluded `failure`; restore → `success`
  (`docs/module4/ci-evidence.md`, real run links).
- **Security findings graded, not swallowed:** 6 AI findings triaged
  Valid/Noise with reasons; 2 human-only findings AI missed; top-3 backlog
  (`docs/security-review.md`).

## 3. Where I can explain the generated code

- Line-by-line trace of the drag-and-drop `handleDrop()` optimistic-update /
  rollback block — what each line does, why it exists, what breaks without
  it (`docs/governance-worksheet.md` §2).
- Architecture written three ways (minimal / structured / targeted context)
  and compared, with a stated verdict and a reusable context-engineering
  rule (`docs/architecture.md`).

## 4. Governance of my own AI use

- Risk-classified inventory of everything shared with AI tools during the
  course, with safer alternatives (`docs/governance-worksheet.md` §1).
- Three concrete usage rules, each tied to a course incident
  (`docs/governance-worksheet.md` §3).
- Personal playbook with an evidence citation on every rule and a filled
  Decision Card (`docs/ai-playbook.md`).

## 5. Course-work trail by branch

| Branch | Contents |
|---|---|
| `main` | Modules 1–3 baseline: API, validation, storage, Kanban frontend, 12 tests |
| `mid-course-project` | Due dates + overdue filter, tags (+14 tests), docs/midcourse/ deliverables |
| `module-4` | CLAUDE.md, CI + green→red→green proof, Docker artifacts, review triage, claim-vs-reality, decision note |
| `module-5` | AGENTS.md, security review, governance worksheet, comments plans, architecture experiment, playbook |
| `final-project` | All of the above + this release check and ownership evidence |
