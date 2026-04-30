---
phase: quick-260430-i7q
plan: 01
subsystem: build-tooling
tags: [makefile, smoke-test, developer-ux]
type: execute
requires: []
provides:
  - "Makefile cli-smoke-test target wiring scripts/cli-smoke-test.sh"
affects:
  - "Makefile"
tech-stack:
  added: []
  patterns:
    - "Makefile target convention: lowercase-with-hyphens, tab-indented recipe, no docstring"
key-files:
  created: []
  modified:
    - "Makefile"
decisions:
  - "Quick-260430-i7q: cli-smoke-test target has NO comply/test prerequisite — Docker-based smoke test is independent of lint/type gates. Keeps the target cheap to invoke standalone for quick CLI verification."
  - "Quick-260430-i7q: Used `bash scripts/cli-smoke-test.sh` (not `./scripts/cli-smoke-test.sh`) per explicit user request, even though the script is executable. Consistent invocation regardless of file-mode state."
  - "Quick-260430-i7q: Placed cli-smoke-test in .PHONY between test-core and comply-fix (test-family grouping) and as a target between test-core and virtualenv. Preserves existing visual ordering: tests → env → comply → ops."
metrics:
  duration: "1 min"
  completed: "2026-04-30"
  tasks: 1
  files_modified: 1
---

# Quick Task 260430-i7q: Add cli-smoke-test Target to Makefile Summary

Added a `make cli-smoke-test` target wiring the existing `scripts/cli-smoke-test.sh`
into the project's standard Makefile-driven developer UX, matching the convention
used by `make test`, `make test-core`, and `make docs`.

## What Was Done

Two-line edit to `Makefile`:

1. Updated the `.PHONY` declaration on line 7 to register `cli-smoke-test` between
   `test-core` and `comply-fix` (test-family grouping):

   ```makefile
   .PHONY: init dev up down test test-core cli-smoke-test comply-fix commit docs clean superclean dist dist-upload docker docker-push
   ```

2. Added a new target block between `test-core` (ends line 32) and `virtualenv`
   (now line 37), matching the exact style of the surrounding targets — no
   docstring, no prerequisite, single tab-indented recipe line:

   ```makefile
   cli-smoke-test:
       bash scripts/cli-smoke-test.sh
   ```

   (The leading whitespace on the recipe line is a literal TAB, as required by GNU
   Make.)

## Verification

All four automated checks from the plan passed:

```
$ grep -E '^\.PHONY:.*\bcli-smoke-test\b' Makefile
.PHONY: init dev up down test test-core cli-smoke-test comply-fix commit docs clean superclean dist dist-upload docker docker-push

$ grep -E '^cli-smoke-test:' Makefile
cli-smoke-test:

$ grep -P '^\tbash scripts/cli-smoke-test\.sh$' Makefile
        bash scripts/cli-smoke-test.sh

$ make -n cli-smoke-test
bash scripts/cli-smoke-test.sh
```

Pre-existing targets continue to resolve correctly:

```
$ make -n test           → ruff + mypy + pytest --cov=cement tests
$ make -n test-core      → ruff + mypy + pytest --cov=cement.core tests/core
$ make -n comply         → ruff + mypy
```

`git diff --stat Makefile` shows the minimal additive change: 1 modified line
(`.PHONY`) and 3 added lines (target line, recipe line, trailing blank).

## Out of Scope (Explicit)

The actual CLI smoke test was NOT executed during this task. The smoke test
script:

- Pulls 5 Docker images (`python:3.10` through `python:3.14`)
- Builds a Cement dist via `docker compose exec cement pdm build`
- Runs end-to-end CLI generation tests inside each container

Running it requires Docker + the docker-compose `cement` service up, which is
outside the scope of a Makefile-wiring task. The wiring itself is what was
delivered. Developers can now run the smoke test on demand via
`make cli-smoke-test`.

## Deviations from Plan

None — plan executed exactly as written. Both edits applied cleanly on the first
attempt; verification commands all passed without modification.

## Commits

| Task | Description                              | Commit   |
| ---- | ---------------------------------------- | -------- |
| 1    | Add cli-smoke-test target to Makefile    | 786a440e |

## Self-Check: PASSED

- File present: `/Users/derks/Development/DFL/cement/Makefile` — FOUND
- Commit present: `786a440e` — FOUND in `git log`
- `.PHONY` updated, target defined, recipe tab-indented, `make -n` resolves
  correctly — all confirmed via `grep` + `make -n` checks above.
