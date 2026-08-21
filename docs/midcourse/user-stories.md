# User Stories — Mid-Course Project

Features selected: **Due dates + overdue filter** and **Tags / labels**.

## Feature 1: Due dates + overdue filter

**US-1.1** — As a task owner, I want to set an optional due date when creating or editing a task, so that I can track deadlines.
- AC: The modal has a date field; leaving it empty saves the task with `due_date: null`.
- AC: A valid ISO date (`YYYY-MM-DD`) is stored and returned by the API.
- AC: An invalid date value is rejected by the backend with HTTP 422.

**US-1.2** — As a task owner, I want to see the due date on each card, so that deadlines are visible on the board.
- AC: Cards with a due date show a "Due YYYY-MM-DD" pill.
- AC: Cards without a due date show no pill.

**US-1.3** — As a task owner, I want overdue tasks to stand out, so that I notice missed deadlines.
- AC: A task with a due date before today that is **not Done** shows a red "Overdue" pill.
- AC: Done tasks never show as overdue, regardless of due date.

**US-1.4** — As a task owner, I want an "Overdue only" filter, so that I can focus on late work.
- AC: Checking "Overdue only" reloads the board via `GET /tasks?overdue=true` and shows only overdue tasks.
- AC: Columns stay visible when the filter returns no tasks (empty state message shown).

> **AI assumption corrected:** The first draft of the overdue rule treated *any* task with `due_date < today` as overdue. Corrected during review: tasks with status `Done` are excluded — a completed task cannot be "late". The rule is now `due_date < today AND status != Done`, and there is a dedicated test for the Done case.

## Feature 2: Tags / labels

**US-2.1** — As a task owner, I want to add tags to a task in the modal, so that I can categorize work.
- AC: Tags are entered comma-separated; whitespace around each tag is trimmed.
- AC: Duplicate tags are de-duplicated; order of first appearance is preserved.
- AC: A blank tag value (e.g. `"ok,   "` sent as `["ok", "   "]`) is rejected with HTTP 422.
- AC: More than 10 tags, or a tag over 30 characters, is rejected with HTTP 422.

**US-2.2** — As a task owner, I want to see tag chips on cards, so that categories are visible at a glance.
- AC: Each tag renders as a chip on the card; tasks without tags show no chip row.

**US-2.3** — As a task owner, I want to filter the board by tag, so that I can see one category at a time.
- AC: Clicking a tag chip reloads the board via `GET /tasks?tag=<value>` and shows only tasks with that exact tag.
- AC: The active tag filter is shown above the board with a clear (×) control.

**US-2.4** — As a task owner, I want tags to survive unrelated edits, so that categorization is not lost.
- AC: A PATCH that only changes status/priority leaves `tags` unchanged (covered by a test).
- AC: Editing a task pre-fills its tags in the modal; clearing the field and saving sends `[]`, which removes all tags.

> **AI assumption corrected:** The first draft silently dropped blank tag values during normalization. Corrected during review: blank tags return HTTP 422 so the user gets explicit feedback instead of input disappearing silently. The Break Test for `test_create_task_blank_tag_returns_422` proves the test catches a regression to silent-drop behavior.
