<!-- DRAFT (X1) — grounded in this repo's actual Module 4 evidence.
     Personalize before submitting, especially the tool-fit paragraphs:
     they must reflect YOUR experience with each tool. -->

# Module 4 — Deliverable Checklist and Tool-Fit Reflection

## Deliverable checklist

| Deliverable | Status | Evidence |
|---|---|---|
| Claude Code setup + corrected CLAUDE.md | Complete | `CLAUDE.md` (verified facts, no invented transition rules, local 3.10 vs CI 3.11 documented) |
| Two verified Claude responses vs code | Complete | `docs/module4/claim-vs-reality.md` (transition-rules and Python-version claims checked against `app/models.py` / `python --version`) |
| CI workflow, no false-green patterns | Complete | `.github/workflows/ci.yml` (pinned 3.11, `pytest -v` last, no `continue-on-error` / `\|\| true` / `--exit-zero`) |
| CI green→red→green proof | See file | `docs/module4/ci-evidence.md` (run links/IDs recorded there) |
| Dockerfile + .dockerignore | Complete (runtime evidence pending) | `Dockerfile` (multi-stage, 3.11-slim, USER app, no reload), `docs/module4/docker-verification.md` — **Docker not installed on the dev machine; run the listed commands and paste outputs** |
| Documentation + claim-vs-reality log | Complete | README rewrite + `docs/module4/claim-vs-reality.md` (2 inaccuracies caught and resolved) |
| AI review + Useful/Noise/Wrong triage | Complete | `docs/module4/review-triage.md` (7 comments: 4 Useful, 2 Noise, 1 Wrong with refuting evidence) |
| Technical note + README link | Complete (rewrite pending) | `docs/decisions/ci-workflow-design.md` — Trade-offs/Open Questions marked for rewrite in your own words |

## Tool-fit reflection (draft — one paragraph per tool, no single winner)

**Copilot** fits the keystroke scale: completing the next line of a test you
are already writing, filling a docstring skeleton, or repeating a pattern
(the third status column, the fifth assertion). In this module's work it
would have shined inside `tests/` where the fixture pattern repeats, but it
has no view of whether CI is honest or whether a docstring's claim is true.

**Cursor** fits the file-and-refactor scale: multi-file edits you want to see
as inline diffs in the editor, such as threading the `due_date` field through
models → storage → routes, with you approving each hunk visually. It keeps
the human in the diff-review loop naturally, but it is not built to run a
verification campaign end-to-end.

**Claude Code** fits the repo-and-workflow scale: it read this whole
repository, wrote the CI/Docker artifacts, ran pytest between layers,
executed the deliberate green→red→green breakage, and produced the evidence
logs — the agentic loop Module 4 is actually about. The cost of that power is
exactly what the lecture warns: it will confidently propose plausible-but-
wrong claims (see the XSS "finding" triaged Wrong, and the invented
transition rules caught in claim-vs-reality), so the stronger the tool scope,
the stricter the human verification has to be.

[ADD 2–3 SENTENCES OF YOUR OWN: which of these you would actually reach for
first on your next project, and one concrete moment from this module that
changed how much you trust AI output.]
