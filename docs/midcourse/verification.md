# Verification — Mid-Course Project

All commands run from the project root with the project venv:
`venv\Scripts\python.exe -m pytest tests -q`

## 1. Baseline (before any change, on fresh `mid-course-project` branch)

```
............                                                             [100%]
12 passed
```

## 2. Backend test results per layer

| Checkpoint | Result |
|---|---|
| Baseline (Modules 1–3 suite) | 12 passed |
| After Feature 1 (due dates) backend + 6 new tests | 18 passed |
| After Feature 2 (tags) backend + 8 new tests | 26 passed |
| After title-validator refactor | 26 passed |

New tests live in `tests/test_midcourse_features.py` (14 new; requirement was ≥ 4).

## 3. Break Test evidence (deliberate source breakage)

### Break Test A — overdue filter (Feature 1)

Temporary change: in `app/main.py` `_is_overdue()`, inverted `task.due_date < date.today()` to `>`.

Failing output (excerpt):

```
>       assert future["id"] in ids
E       AssertionError: assert '9f72f142-...' in ['0e925d9e-...']

FAILED tests/test_midcourse_features.py::test_overdue_filter_returns_only_overdue_tasks
FAILED tests/test_midcourse_features.py::test_overdue_false_filter_excludes_overdue_tasks
2 failed, 12 passed
```

Exactly the two overdue tests failed and nothing else → the tests target the comparison they claim to test. Source restored afterwards.

### Break Test B — blank tag rejection (Feature 2)

Temporary change: in `app/models.py` `_validate_tags()`, replaced `raise ValueError("tags must not contain blank values")` with `continue` (silent drop).

Failing output (excerpt):

```
    def test_create_task_blank_tag_returns_422():
        response = client.post("/tasks", json={"title": "x", "tags": ["ok", "   "]})
>       assert response.status_code == 422
E       assert 201 == 422

FAILED tests/test_midcourse_features.py::test_create_task_blank_tag_returns_422
1 failed, 13 passed
```

The test fails specifically when validation regresses to silent dropping. Source restored afterwards.

### After restoring both breaks

```
..........................                                               [100%]
26 passed
```

## 4. Behavior contract — before/after refactor

Refactor: extracted duplicated title validation in `app/models.py` into `_validate_title()` (commit "Refactor: extract shared _validate_title helper"). Full suite: **26 passed before, 26 passed after** — no assertions changed.

| # | Behavior | Before | After |
|---|---|---|---|
| 1 | Three status columns render with counts | Pass | Pass |
| 2 | Cards sort High → Medium → Low per column | Pass | Pass |
| 3 | Loading / ready / empty / error states | Pass | Pass |
| 4 | Valid drag PATCHes and persists | Pass | Pass |
| 5 | Failed PATCH reverts card + shows message | Pass | Pass |
| 6 | Modal create/edit with `.trim()` title validation and 422 display | Pass | Pass |
| 7 | Due/overdue pill and Overdue-only filter | Pass | Pass |
| 8 | Tag chips, tag filter, clear-filter control | Pass | Pass |

Rows 1–6 are the Module 3 contract; 7–8 extend it for the new features. Backend behavior is locked by the 26-test suite; frontend rows are verified manually (section 5).

## 5. Manual browser checks

Setup: `uvicorn app.main:app --reload --port 8000` + `python -m http.server 5500`, open `http://localhost:5500/frontend/index.html`.

Complete this checklist in the browser and mark results:

- [ ] Create a task with a future due date → card shows blue "Due YYYY-MM-DD" pill.
- [ ] Create a task with a past due date (status ToDo) → red "Overdue" pill.
- [ ] Drag the overdue task to Done → pill switches from Overdue to plain Due.
- [ ] Check "Overdue only" → only overdue tasks remain; columns stay visible; unchecking restores all.
- [ ] Enter an invalid date by editing the request in DevTools (or POST via /docs with `"due_date": "not-a-date"`) → 422, modal/board unaffected.
- [ ] Create a task with tags `backend, urgent , backend` → two chips: `backend`, `urgent` (trimmed, deduped).
- [ ] Click a tag chip → board filters to that tag; active-filter chip appears; × clears it.
- [ ] Edit a task, clear the tags field, save → chips removed ( `[]` clears tags).
- [ ] Stop the backend, click Retry → error state with Retry button still works.
