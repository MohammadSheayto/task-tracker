<!-- DRAFT written with AI assistance from the real session history.
     Personalize this in your own words before submitting — the facilitator
     expects your voice and your judgment here. -->

# Reflection — Mid-Course Project

For this sprint I used Claude Code inside VS Code as my single AI tool, but in different roles: as a planner (choosing two scoped features and sequencing backend → tests → frontend), as a code generator working in small diffs on `app/models.py`, `app/storage.py`, `app/main.py`, and `frontend/index.html`, and as a test writer following the fixture pattern already established in `tests/test_tasks.py`. Every layer was verified with pytest before moving to the next, exactly as the Module 3 workflow taught.

The moment AI clearly helped was test generation. Once I gave it the exact validation rules for tags (trim, reject blank with 422, dedupe, max 10 × 30 chars), it produced eight focused tests in the existing TestClient style in one pass, including edge cases I might have skipped, like proving tags survive an unrelated PATCH. The suite went from 12 to 26 tests with each test asserting both status code and response body.

The moment it slowed me down was mundane but real: a multi-line git commit message got mangled by PowerShell quoting, the commit failed halfway, and we had to redo it with a message file. It was a reminder that the assistant's environment assumptions (POSIX-style shells) still need watching on Windows, even when the code itself is fine.

The clearest place my review changed the result was the overdue rule. The first draft counted every task with a past due date as overdue, which would have flagged completed work as late. I corrected it to `due_date < today AND status != Done`, added a test for the Done case, and later proved that test by deliberately inverting the comparison and watching exactly the right two tests fail. The second correction was rejecting blank tags with a 422 instead of silently dropping them — silent data loss would have contradicted how the rest of the API treats bad input.

The habit I am keeping: never trust a green test until I have seen it red. Both Break Tests failed for precisely the behavior they claim to protect, which is what makes the 26-passing result meaningful rather than decorative.

<!-- Word count ≈ 330 — within the 250–500 requirement. -->
