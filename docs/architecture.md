# Architecture Doc — Context Strategy Comparison (Part 5.5)

Same one-page architecture task run three ways:
**A** = minimal context (free inspection, no guidance) → `architecture-A.md`
**B** = structured context (AGENTS.md + file summaries) → `architecture-B.md`
**C** = targeted context (only main.py/models.py/storage.py) → `architecture-C.md`

## Comparison

| Strategy | What it got right | What it missed / risked | Best suited for |
|---|---|---|---|
| A (minimal) | Full, readable picture; correct data model and flow. | Nothing forced it to separate repo fact from framework convention — several sentences would be true of any FastAPI app; hardest draft to audit. | Quick orientation when you'll verify claims yourself. |
| B (structured) | Most specific and most complete: caught the no-transition rule, PATCH null semantics, the SR-2 link, CI/Docker facts — because AGENTS.md pre-encoded verified facts. | Longest draft; inherits any error in AGENTS.md (context becomes a single point of failure); most confident tone. | Onboarding docs and anything a reader will trust without re-verifying. |
| C (targeted) | Perfectly honest about limits — API/model/storage facts precise, everything else explicitly "not visible". | By design blind to frontend, tests, CI, Docker; cannot describe any cross-layer behavior. | Backend-only questions; audits where honesty about scope matters more than coverage. |

## Verdict

**B is the final architecture doc.** Its advantage did not come from more
tokens — it came from *curated* context: AGENTS.md contains only verified
facts, so the draft inherited verification instead of doing it. C is the
runner-up and the most trustworthy per-sentence; A is the draft most likely
to smuggle in plausible filler.

## Context-engineering rule

For repo-wide documents a reader will trust without checking (architecture,
onboarding), I use structured context — a verified AGENTS/CLAUDE file plus
file summaries — because the draft inherits verification instead of
inventing. For narrow technical questions I use targeted context (the two or
three anchor files) because "not visible from the files I read" is more
valuable than confident guessing.
