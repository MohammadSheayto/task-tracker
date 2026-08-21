# Technical Note — CI Workflow Design

<!-- Draft prepared with AI assistance per Module 4 T1. Sections marked
     "DRAFT - REWRITE IN MY OWN WORDS" must be rewritten in your voice
     before this counts as your decision record. -->

## 1. Context

The Task Tracker had a 26-test pytest suite but nothing enforced it: tests
only ran when someone remembered to run them locally. Module 4 introduces the
repo's first CI pipeline. The risk this note addresses is not "no CI" — it is
**false-green CI**: a workflow that looks successful while silently skipping
or swallowing test failures (`continue-on-error`, `|| true`, `--exit-zero`,
piped exit codes).

## 2. Decision

Use a single GitHub Actions workflow (`.github/workflows/ci.yml`) that runs on
every `push` and `pull_request`: check out the repo, set up **pinned Python
3.11**, `pip install -r requirements.txt`, and run `pytest -v` as the final
step with no error suppression of any kind. The workflow does not deploy,
lint, or build Docker — it does exactly one job: fail when a test fails.

## 3. Alternatives Considered

- **Matrix build (3.10 + 3.11):** would close the local-3.10 vs CI-3.11 gap
  found in review; rejected for now as beyond the module's single-version
  requirement, though it is the most likely next step.
- **Adding lint/format jobs (ruff, black):** valuable, but expands scope and
  invites `--exit-zero`-style softening; rejected for this module.
- **Running tests inside the Docker image:** couples CI to the Dockerfile and
  slows every run; the image is verified separately in Part 4.3.
- **`pytest -q` (quiet):** rejected — `-v` names each test in the log, which
  is what makes the red-run evidence readable.

## 4. Trade-offs

DRAFT - REWRITE IN MY OWN WORDS

- Pinning 3.11 gives reproducible CI but does not match the local 3.10 venv;
  a version-specific difference would surface in only one of the two places.
- Triggering on every push of every branch costs more Actions minutes but
  means experiment branches get the same safety net as main.
- Keeping the workflow single-job keeps the log trivially readable at the
  cost of no parallelism — acceptable at 26 tests (~2s).

## 5. Consequences

- Every push now produces a public pass/fail signal; the green→red→green
  exercise (docs/module4/ci-evidence.md) proves the signal is real.
- Contributors cannot merge silently-broken code without the log showing it.
- The workflow becomes the natural place to later add a Docker build step or
  a version matrix — both would be additive, not rewrites.

## 6. Open Questions

DRAFT - REWRITE IN MY OWN WORDS

- Should the local venv be upgraded to 3.11 to eliminate the version skew, or
  should CI gain a 3.10 matrix leg instead?
- When the SQLite migration lands (planned post-Module 4), do tests need a
  service container or is a temp-file database enough?
- At what point does the suite become slow enough to justify caching pip
  downloads (`actions/cache`)?

I would do this differently by... [YOUR SENTENCE HERE]

*README links to this note from the "CI workflow" section.*
