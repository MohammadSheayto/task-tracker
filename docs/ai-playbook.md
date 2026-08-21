# My Personal AI Coding Playbook

## 1. When I reach for AI first

When we have something traditional or repetitive, like adding a new page
similar to one we already have in the same project — but I don't use it to
invent. (Evidence: the 14 mid-course tests where AI followed my existing
fixture pattern from tests/test_tasks.py — docs/midcourse/prompt-log.md)

## 2. When I do not reach for AI

When I have something with raw requirements, or something not yet discussed
related to design. (Evidence: the overdue rule — the AI's first draft counted
Done tasks as overdue; excluding them was my decision, not the AI's —
docs/midcourse/mini-adr.md)

## 3. My non-negotiables

Code review and preliminary testing before accepting an AI change and putting
it in. (Evidence: an AI review comment claimed an XSS bug in my frontend, but
the code inserts all text via textContent, so the finding was wrong —
docs/module4/review-triage.md. AI also invented status-transition rules that
do not exist in my code — docs/module4/claim-vs-reality.md)

## 4. My review rules

- Changes must be testable; I work with test-driven development (unit tests).
- Check whether the code is noisy or not; fix the issues and make the
  comments more human — remove AI-sounding narration before committing.

## 5. What I am still figuring out

Till now, I do not have a full workflow with AI: designing in advanced
phases, coding, code reviewing, and testing are in place, but doing the
CI/CD step without assistance is still ongoing to complete the cycle.

## Decision Card

- For a new feature I reach for: Claude.
- For a code review I reach for: Codex.
- For debugging I reach for: Claude.
- For infrastructure I reach for: Claude.
- I will never paste credentials or API keys into an AI tool. (My governance
  worksheet flags that my work-domain email already travels with every AI
  request — docs/governance-worksheet.md)
- My one rule is: no AI change is committed until I've read the diff and the
  full test suite (pytest) has passed.

**30-day commitment:** I will re-read this playbook on 21/09/2026 and revise
any rule that turned out to be vague or wrong.
