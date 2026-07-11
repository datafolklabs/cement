---
phase: quick-260711-fjb
plan: 01
subsystem: utils.misc
tags: [logging, framework, env-var, issue-593]
requires: []
provides: [CEMENT_FRAMEWORK_LOG_FILE]
affects: [cement/utils/misc.py]
tech_stack:
  added: []
  patterns: [additive-env-var-gate, handler-idempotency-guard, oserror-swallow]
key_files:
  created: []
  modified:
    - cement/utils/misc.py
    - tests/utils/test_misc.py
    - CHANGELOG.md
decisions:
  - "Enablement semantics option (a): CEMENT_FRAMEWORK_LOG_FILE only routes output; it does not enable logging on its own."
  - "FileHandler level and formatter mirror the console handler; emits still gate on logging_is_enabled."
  - "Idempotency by baseFilename comparison against resolved abspath, mirroring the existing StreamHandler guard."
  - "OSError on FileHandler construction is swallowed so framework logging never crashes the host app."
metrics:
  duration: ~10m
  completed: 2026-07-11
  tasks: 2
  files: 3
requirements: [ISSUE-593]
status: complete
---

# Phase quick-260711-fjb Plan 01: CEMENT_FRAMEWORK_LOG_FILE Summary

Added an optional `CEMENT_FRAMEWORK_LOG_FILE` environment variable that routes
Cement's internal `MinimalLogger` output to a file (in addition to the console)
when framework logging is already enabled — purely additive, zero public-API
change, zero new dependencies (GitHub issue #593).

## What Was Built

### Task 1 — FileHandler attach in `MinimalLogger.__init__`
- After the existing `StreamHandler` idempotency block, read
  `CEMENT_FRAMEWORK_LOG_FILE` from `os.environ` (default `None`).
- When set: resolve the value with `os.path.abspath(os.path.expanduser(...))`
  so the idempotency comparison against `FileHandler.baseFilename` is stable.
- Idempotency guard: scan `self.backend.handlers` for an existing
  `logging.FileHandler` at the same resolved path; attach only if none exists
  (prevents double-writes across repeated `minimal_logger()` calls for the same
  namespace + path).
- Construct the `FileHandler` inside `try/except OSError` — on failure, attach
  nothing and do not raise (framework logging is a dev aid, must never crash the
  host app).
- On success, reuse the console's `formatter` and mirror `console.level`, then
  `addHandler` to the backend.
- Extended the `minimal_logger()` docstring documenting the new env var
  alongside the existing framework-logging switches (in-repo docstring only;
  narrative docs live on GitBook per project convention).
- No signature changes to `minimal_logger()` or `MinimalLogger.__init__`.

### Task 2 — Tests + CHANGELOG
- Added four tests to `tests/utils/test_misc.py` (unique namespace per test,
  `backend.handlers = []` reset for shared-backend isolation, `tmp_path` +
  `monkeypatch` fixtures), covering every branch:
  1. env set + logging enabled (`CEMENT_LOG=1`): file exists, contains the
     message text and namespace, exactly one `FileHandler` attached.
  2. env unset: no `FileHandler` attached (behavior unchanged).
  3. idempotency: two calls, same namespace + path → exactly one `FileHandler`.
  4. invalid path (missing parent dir): `OSError` swallowed, no `FileHandler`,
     no raise (exercises the `except OSError` branch).
- Appended a one-line `[utils.misc]` Features entry (with issue link) under the
  active `## 3.0.15 - DEVELOPMENT` section of `CHANGELOG.md`, wrapped at 78
  chars.

## Deviations from Plan

None — plan executed exactly as written.

Note on execution environment (not a code deviation): the worktree had no
`.venv` (PDM could not build a virtualenv). Ran the project toolchain from the
main repo's venv (`/Users/derks/Development/DFL/cement/.venv/bin`) with
`PYTHONPATH` set to the worktree root, confirming `cement.utils.misc` resolved
to the worktree copy. Started the required Redis (6379) and memcached (11211)
devbox services, which were down, so the full-suite coverage gate could run.

## Quality Gates

- `ruff check cement/utils/misc.py tests/utils/test_misc.py` — All checks passed.
- `mypy cement/utils/misc.py` — Success: no issues found.
- `pytest --cov=cement.utils tests/utils/test_misc.py` (full suite via addopts,
  `--cov-fail-under=100`) — 382 passed; `cement/utils/misc.py` at **100.00%**
  coverage; `cement.utils` package total 100.00%.

## Threat Model Outcome

- T-fjb-02 (DoS via invalid/unwritable path) — mitigated: `OSError` swallowed.
- T-fjb-03 (stacked/duplicate handlers) — mitigated: `baseFilename` idempotency
  guard.
- T-fjb-01 (info disclosure at operator-supplied path) — accepted per plan
  (operator-trust boundary, debug output only).

No new threat surface introduced beyond the operator-env → filesystem-write
boundary already captured in the plan's threat model.

## Known Stubs

None.

## Self-Check: PASSED

- FOUND: cement/utils/misc.py (modified)
- FOUND: tests/utils/test_misc.py (modified)
- FOUND: CHANGELOG.md (modified)
- FOUND commit 5e032017 (feat — source)
- FOUND commit 2a9a59cd (test + changelog)
