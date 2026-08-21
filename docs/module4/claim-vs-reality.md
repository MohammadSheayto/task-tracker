# Claim-vs-Reality Documentation Audit — Module 4 (Part 4.4)

Each claim was checked against the source file or a real command output, not
against AI explanation. Format follows DOC3.

| Documentation claim | Code or runtime reality | Resolution | Evidence to keep |
|---|---|---|---|
| Course template: "Tech stack: Python 3.11" | Local venv is **Python 3.10.10** (`python --version`); only CI and Docker use 3.11. | CLAUDE.md states both explicitly instead of copying the template. | `python --version` output; `ci.yml` line `python-version: "3.11"`. |
| Plausible AI claim: "Status transition rules restrict moves (e.g. Done → ToDo is blocked)" | **No transition rules exist.** `TaskUpdate.status` accepts any valid `TaskStatus`; neither `app/models.py` nor `app/main.py` checks the previous status. | CLAUDE.md says "No transition restrictions are implemented — do not invent transition rules." README's claim that a drag can only fail via 404/network was re-verified as true. | `app/models.py` `TaskUpdate`; `app/main.py` `update_task`. |
| Plausible AI claim: "Duplicate tags are rejected with 422" | Duplicates are **silently deduped preserving order**; only blank values, >30-char tags, or >10 tags return 422. | All docs phrase it as "deduped", never "rejected". | `_validate_tags()` in `app/models.py`; test `test_create_task_with_tags_trims_and_dedupes`. |
| README/docstring: "POST /tasks returns 201" | Confirmed: `status_code=status.HTTP_201_CREATED` on the route decorator. | No change needed. | `app/main.py` `create_task`; test asserts 201. |
| README/docstring: "DELETE /tasks/{id} returns 204" | Confirmed: `HTTP_204_NO_CONTENT`; 404 for unknown id. | No change needed. | `app/main.py` `delete_task`; `test_delete_task_then_get_returns_404`. |

## Docstring spot-check (DOC1 verification)

The app code was documented during Modules 1–3; three docstrings were checked
line-by-line against their bodies:

1. `list_tasks` (app/main.py) — docstring describes `overdue` semantics
   (before today AND not Done) — matches `_is_overdue()`. ✔
2. `update_task` PATCH docstring — "Only fields present in the request body
   are changed" — matches the `is not None` guards in `storage.update()`. ✔
3. `TaskStorage` class docstring — "Not thread-safe; for production use, add
   locks or move to a database" — matches implementation (plain dict, no
   locks) and ADR-001's SQLite plan. ✔

**Inaccuracies caught and resolved this module: 2** (Python version claim;
transition-rules claim) — both were corrected in CLAUDE.md before they could
propagate into future AI sessions.
