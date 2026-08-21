# CI Green → Red → Green Evidence — Module 4 (Part 4.2)

Workflow: `.github/workflows/ci.yml` (push + pull_request, Python 3.11 pinned,
`pytest -v`, no failure-swallowing). Branch: `module-4`.
All three runs below are real GitHub Actions runs, executed 2026-08-21.

| Run | Commit | What changed | Local pytest result | Actions conclusion | Link |
|---|---|---|---|---|---|
| #1 GREEN | `ce9f7da` | Module 4 artifacts added (workflow's first run) | 26 passed | **success** | https://github.com/MohammadSheayto/task-tracker/actions/runs/32469091792 |
| #2 RED (intentional) | `7beed3e` | One test expectation broken on purpose: `test_create_task_returns_201_with_defaults` asserted status `"Todo"` instead of `"ToDo"` (test-only change; no production code touched) | 1 failed, 11 passed (confirmed locally before push) | **failure** | https://github.com/MohammadSheayto/task-tracker/actions/runs/32469781439 |
| #3 GREEN | `752a729` | Assertion restored to `"ToDo"` | 26 passed | **success** | https://github.com/MohammadSheayto/task-tracker/actions/runs/32469871835 |

## Why this proves the pipeline is honest

- The red run failed **for the intended reason**: the deliberately wrong
  assertion in `tests/test_tasks.py::test_create_task_returns_201_with_defaults`,
  reproduced locally before pushing (same failure, same test).
- The failure was not swallowed: the workflow has no `continue-on-error`,
  `|| true`, or `--exit-zero`, and `pytest -v` is the final step, so its exit
  code is the job's exit code.
- Restoring the one-line change returned the pipeline to green, showing the
  red state was caused by exactly that change and nothing else.

Evidence checklist (C3): green link ✔ · intentional red link ✔ · restored
green link ✔ · local confirmation of the failure before each push ✔
