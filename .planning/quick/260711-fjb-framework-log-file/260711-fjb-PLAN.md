---
phase: quick-260711-fjb
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - cement/utils/misc.py
  - tests/utils/test_misc.py
  - CHANGELOG.md
autonomous: true
requirements: [ISSUE-593]

must_haves:
  truths:
    - "When CEMENT_FRAMEWORK_LOG_FILE is set AND framework logging is enabled, framework/extension debug output is written to the file in addition to the console."
    - "When CEMENT_FRAMEWORK_LOG_FILE is unset, MinimalLogger behavior is byte-for-byte identical to today (no FileHandler attached)."
    - "Repeated minimal_logger() calls for the same namespace + path do NOT stack duplicate FileHandlers (no double-writes)."
    - "An unwritable/invalid path fails gracefully — the host app never crashes."
    - "100% coverage, ruff clean, mypy strict clean remain green."
  artifacts:
    - cement/utils/misc.py
    - tests/utils/test_misc.py
    - CHANGELOG.md
  key_links:
    - "MinimalLogger.__init__ FileHandler attach is gated by the same idempotency discipline as the existing StreamHandler guard."
    - "FileHandler level mirrors the console handler level; emit methods still gate on logging_is_enabled, so the file only receives output when framework logging is enabled."
---

<objective>
Implement GitHub issue #593: add optional file logging to Cement's internal
MinimalLogger via a new CEMENT_FRAMEWORK_LOG_FILE environment variable. When
set to a path, framework/extension debug output is *also* written to that file
(in addition to the existing console StreamHandler), mirroring the existing
CEMENT_FRAMEWORK_LOGGING / CEMENT_LOG env-var pattern.

Purpose: Give developers a way to capture framework debug output to disk for a
CLI app without changing any public API or adding dependencies.
Output: Additive FileHandler in MinimalLogger.__init__, full test coverage,
CHANGELOG Features entry.
</objective>

<design_decisions>
These are resolved in this plan and must be implemented as stated:

1. **Enablement semantics = option (a) (least-surprising).** Setting
   CEMENT_FRAMEWORK_LOG_FILE does NOT turn logging on by itself. It only
   *routes* framework log output to a file when framework logging is already
   enabled via an existing switch (CEMENT_LOG / debug=True / --debug /
   CEMENT_FRAMEWORK_LOGGING). This falls out naturally: every emit method
   (info/debug/etc.) already gates on `logging_is_enabled`, so nothing is
   written to the file unless logging is enabled. The FileHandler's level is
   set to mirror the console handler (`console.level` — DEBUG when the existing
   `_enabled` gate is true, otherwise INFO). Rationale: purely additive,
   backward-compatible, no silent behavior change when the app enables neither
   switch.

2. **Idempotency guard.** `logging.getLogger(namespace)` returns a shared
   backend per namespace. Before attaching, scan `self.backend.handlers` for an
   existing `logging.FileHandler` whose `baseFilename` equals the resolved
   absolute path; attach only if none exists. This mirrors the existing
   `if not self.backend.handlers` StreamHandler guard and prevents double-writes
   across repeated minimal_logger() calls for the same namespace + path.

3. **Path resolution.** Resolve the env value with
   `os.path.abspath(os.path.expanduser(...))` so the idempotency comparison is
   stable (logging.FileHandler stores `baseFilename` as an absolute path).

4. **Error handling = swallow OSError.** Wrap FileHandler construction in
   try/except OSError. Framework logging is a dev aid and must never crash the
   host app. On failure, do not attach a handler and do not raise. (No stderr
   spam — the console handler is unaffected.)
</design_decisions>

<execution_context>
@$HOME/.claude/gsd-core/workflows/execute-plan.md
@$HOME/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/STATE.md
@cement/utils/misc.py
@tests/utils/test_misc.py
</context>

<tasks>

<task type="auto" tdd="true">
  <name>Task 1: Attach optional CEMENT_FRAMEWORK_LOG_FILE FileHandler in MinimalLogger.__init__</name>
  <files>cement/utils/misc.py</files>
  <behavior>
    - Env unset/empty: no FileHandler added; backend handler set unchanged.
    - Env set + logging enabled: a FileHandler at the resolved abspath is
      attached, sharing the same Formatter as console, level == console.level.
    - Second minimal_logger() call, same namespace + same path: no second
      FileHandler (idempotent).
    - Unwritable/invalid path: no crash, no FileHandler attached (OSError
      swallowed).
  </behavior>
  <action>
    In MinimalLogger.__init__, after the existing StreamHandler idempotency
    block (the `if not self.backend.handlers:` guard), add optional file
    logging. Read CEMENT_FRAMEWORK_LOG_FILE from os.environ (default None). When
    truthy: resolve the path with os.path.abspath(os.path.expanduser(value)).
    Check whether any handler already on self.backend.handlers is a
    logging.FileHandler whose baseFilename equals the resolved path; if one
    exists, do nothing (idempotency). Otherwise construct logging.FileHandler in
    a try/except OSError — on OSError, swallow and attach nothing (framework
    logging must never crash the host app). On success, apply the same
    `formatter` already built for the console handler, set the handler level to
    match the console handler (console.level), and addHandler to the backend.
    Reuse the module-level formatter/console objects already in scope; do not
    build a second Formatter. Do NOT change minimal_logger() or __init__
    signatures — behavior is additive and env-var gated only. Also extend the
    minimal_logger() docstring with a short note documenting the
    CEMENT_FRAMEWORK_LOG_FILE env var alongside the existing framework-logging
    switches (in-repo docstring only; narrative docs live on GitBook per
    project memory). Keep ruff line length <= 100 and full type annotations.
  </action>
  <verify>
    <automated>pdm run mypy cement/utils/misc.py && pdm run ruff check cement/utils/misc.py</automated>
  </verify>
  <done>FileHandler is attached only when CEMENT_FRAMEWORK_LOG_FILE is set; level and formatter mirror console; idempotency + OSError guards present; no signature changes; mypy + ruff clean.</done>
</task>

<task type="auto">
  <name>Task 2: Add tests for all branches and CHANGELOG entry</name>
  <files>tests/utils/test_misc.py, CHANGELOG.md</files>
  <action>
    Add tests to tests/utils/test_misc.py mirroring existing MinimalLogger test
    patterns (unique namespace per test; reset `logging.getLogger(ns).handlers =
    []` to isolate shared backend state, as
    test_minimal_logger_does_not_duplicate_handlers already does). Use the
    pytest tmp_path fixture for file artifacts and monkeypatch for env vars.
    Cover every branch to preserve 100% coverage:
    (1) env set + logging enabled (monkeypatch.setenv CEMENT_LOG=1 and
    CEMENT_FRAMEWORK_LOG_FILE=tmp_path file, or patch logging_is_enabled True):
    emit a debug/info message, assert the file exists and contains the message
    text and namespace; assert exactly one FileHandler is on the backend.
    (2) env unset: assert no FileHandler is attached to the backend (behavior
    unchanged) — monkeypatch.delenv CEMENT_FRAMEWORK_LOG_FILE raising=False.
    (3) idempotency: call minimal_logger() twice with the same namespace and
    same CEMENT_FRAMEWORK_LOG_FILE; assert the backend has exactly one
    FileHandler.
    (4) invalid/unwritable path: set CEMENT_FRAMEWORK_LOG_FILE to a path whose
    parent directory does not exist (e.g. tmp_path / 'no' / 'such' / 'dir.log')
    so logging.FileHandler raises OSError; assert minimal_logger() returns
    without raising and no FileHandler is attached. This exercises the except
    OSError branch.
    Then append a one-line Features entry to the active
    `## 3.0.15 - DEVELOPMENT` section's `Features:` list in CHANGELOG.md
    (line ~167), prefixed `[utils.misc]`, referencing issue #593 with the
    GitHub issue link on a following sub-bullet, matching the existing entry
    format. Keep CHANGELOG lines <= 78 chars per CLAUDE.md.
  </action>
  <verify>
    <automated>pdm run pytest --cov=cement.utils tests/utils/test_misc.py -x</automated>
  </verify>
  <done>All four branches tested; targeted test file passes; coverage of cement/utils/misc.py at 100%; CHANGELOG Features entry added and wrapped at 78 chars.</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| operator env → filesystem write | CEMENT_FRAMEWORK_LOG_FILE path is written by the framework |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-fjb-01 | Information Disclosure | FileHandler at operator-supplied path | low | accept | Path is set by the app operator via env var (same trust level as the process); debug output only. No untrusted input crosses this boundary. |
| T-fjb-02 | Denial of Service | Invalid/unwritable path | low | mitigate | OSError on FileHandler construction is swallowed; framework logging never crashes the host app. |
| T-fjb-03 | Tampering | Duplicate/stacked handlers | low | mitigate | Idempotency guard checks baseFilename before attaching; prevents double-writes. |
</threat_model>

<verification>
- `make comply` (ruff + mypy) clean.
- `pdm run pytest --cov=cement.utils tests/utils/test_misc.py` passes with
  100% coverage of cement/utils/misc.py.
- Full suite regression via `make test` unaffected (requires Redis + memcached
  services running per project memory).
</verification>

<success_criteria>
- CEMENT_FRAMEWORK_LOG_FILE, when set and framework logging enabled, writes
  framework debug output to the file.
- Env unset → zero behavioral change; no FileHandler attached.
- Repeated minimal_logger() calls do not duplicate the FileHandler.
- Invalid path is swallowed gracefully.
- 100% coverage, ruff clean, mypy strict clean.
- CHANGELOG Features entry added under the active DEVELOPMENT section.
</success_criteria>

<output>
Create `.planning/quick/260711-fjb-framework-log-file/260711-fjb-SUMMARY.md` when done
</output>
