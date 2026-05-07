---
phase: 05-deprecations-docs-security-stubs
plan: 01
subsystem: deprecations-docstring-sweep
tags: [deprecations, docstrings, ext_logging, ext_smtp, rst, autodoc]
requirements_addressed: [DEPREC-01, DEPREC-03, DOCS-04]
dependency_graph:
  requires:
    - "Phase 03 closeout (audit-public-api gate enforcing; ruff/mypy/pytest baselines green)"
    - "Active CHANGELOG section: 3.0.15 - DEVELOPMENT (will be released as stable/3.0.16)"
  provides:
    - "DEPRECATIONS dict where every entry names a concrete removal version (Cement v3.2.0)"
    - "Adjacent deprecation docstrings (ext_logging set_level/fatal, ext_smtp send) name v3.2.0"
    - ".. deprecated:: 3.0.16 admonition on SMTPMailHandler.send() rendering in autodoc HTML"
  affects:
    - "Phase 05 Plan 02 (Sphinx warning resolution): admonition introduces no new warnings (verified clean rebuild = 4 pre-existing warnings, unchanged)"
    - "Phase 05 Plan 04 (Makefile -W flip): admonition is well-formed RST and will pass under -W once Plan 02 resolves the 4 baseline warnings"
tech_stack:
  added: []
  patterns:
    - "Sphinx .. deprecated:: directive (8-space indent, 12-space body indent — RST canonical)"
    - "RST inline-literal double-backtick form ``CRITICAL`` / ``critical()`` for autodoc code rendering"
key_files:
  created: []
  modified:
    - cement/core/deprecations.py
    - cement/ext/ext_logging.py
    - cement/ext/ext_smtp.py
    - CHANGELOG.md
decisions:
  - "DEPREC-03 already-satisfied — existing tests assert by deprecation ID, not by message text, so no test work was required (verified in 05-RESEARCH.md A1, A6)"
  - "Plan grep `grep -F 'removed in Cement v3.2.0' cement/ext/ext_logging.py | wc -l ≥ 2` returns 1 (set_level: phrase on one line; fatal: phrase wraps across lines 368-369). Intent verified via `grep -cF 'Cement v3.2.0' cement/ext/ext_logging.py` = 2. Both docstrings correctly name v3.2.0; the difference is line-wrap, not semantics."
metrics:
  duration_minutes: 7.7
  duration_seconds: 461
  tasks_completed: 3
  commits: 3
  files_modified: 4
  completed_date: 2026-05-07
---

# Phase 05 Plan 01: Tighten Deprecation Removal-Version Language Summary

**One-liner:** Pinned all 4 DEPRECATIONS dict entries to `Cement v3.2.0`, swept the `set_level`/`fatal` docstrings in `ext_logging.py` and added a `.. deprecated:: 3.0.16` admonition to `SMTPMailHandler.send()` in `ext_smtp.py` — DEPREC-01 acceptance criterion #5 closed.

## Outcome

DEPREC-01 acceptance criterion #5 ("every entry in `cement/core/deprecations.py:DEPRECATIONS` names a removal version") is now SATISFIED. DEPREC-03 was already-satisfied (existing tests assert by ID, not by message text — no regression). DOCS-04 (adjacent docstring sweep) is COMPLETE for the load-bearing user-visible surface. Three atomic commits landed under D-16, each touching exactly 2 files (source + CHANGELOG), each with a Conventional Commits subject ≤78 chars and a 78-char-wrapped body. All three gates (`make comply`, `make audit-public-api`, `make test`) exited 0 on every commit at 100% coverage (320/320 tests passing).

## Tasks Completed

| Task | Name                                                                                | Commit     | Files                                               |
| ---- | ----------------------------------------------------------------------------------- | ---------- | --------------------------------------------------- |
| 1    | Pin removal-version language in DEPRECATIONS dict                                   | `dedacccb` | `cement/core/deprecations.py`, `CHANGELOG.md`       |
| 2    | Tighten ext_logging.py set_level + fatal() docstrings                               | `3f809b90` | `cement/ext/ext_logging.py`, `CHANGELOG.md`         |
| 3    | Add `.. deprecated:: 3.0.16` admonition to ext_smtp.py send() docstring             | `059fab38` | `cement/ext/ext_smtp.py`, `CHANGELOG.md`            |

## Verification Evidence

### DEPREC-01 acceptance — every DEPRECATIONS entry names a removal version

```bash
$ grep -cE "'3\.[0-9]+\.[0-9]+-[0-9]+':" cement/core/deprecations.py
4
$ grep -cE 'Cement v3\.2\.0' cement/core/deprecations.py
4
$ grep -E 'future version[s]? of Cement' cement/core/deprecations.py
(no output — exit 1 → vague phrasing eliminated)
```

Note: The plan body's grep used double-quote anchors `"3\..."` but the DEPRECATIONS dict entries use single-quote keys (`'3.0.8-1':`). The plan grep returns 0 against the actual codebase shape; the single-quote variant returns the expected 4. Same intent, equivalent acceptance.

### DEPREC-03 regression hold — existing tests pass without modification

```bash
$ pdm run pytest tests/core/test_deprecations.py tests/ext/test_ext_smtp.py -x
===================== 320 passed, 1693 warnings in 51.66s ======================
```

(Note: pytest's `addopts` configuration triggers the full suite + 100% coverage gate when running individual files; coverage gate exit 0 confirms the targeted tests pass alongside the rest.)

### DOCS-04 — both ext_logging docstrings name v3.2.0

```bash
$ grep -cF 'Cement v3.2.0' cement/ext/ext_logging.py
2
$ grep -E 'future versions of Cement' cement/ext/ext_logging.py
(no output — vague phrasing gone)
$ grep -E 'Please us \`' cement/ext/ext_logging.py
(no output — typo fixed)
$ grep -F '``CRITICAL``' cement/ext/ext_logging.py
        removed in Cement v3.2.0. Please use ``CRITICAL`` instead.
$ grep -F '``critical()``' cement/ext/ext_logging.py
        Cement v3.2.0. Please use ``critical()`` instead.
```

### DOCS-04 — smtp send() admonition

```bash
$ grep -cF '.. deprecated:: 3.0.16' cement/ext/ext_smtp.py
1
$ grep -F 'senderrs ``dict`` in Cement v3.2.0' cement/ext/ext_smtp.py
            ``smtplib`` senderrs ``dict`` in Cement v3.2.0. See
$ grep -F "DEPRECATIONS['3.0.16-1']" cement/ext/ext_smtp.py
            ``DEPRECATIONS['3.0.16-1']``.
$ grep -F 'bool: ``True``' cement/ext/ext_smtp.py
            bool: ``True`` if message is sent successfully, ``False`` otherwise
$ grep -F 'bool:``True``' cement/ext/ext_smtp.py
(no output — RST formatting bug fixed)
$ grep -F "deprecate('3.0.16-1')" cement/ext/ext_smtp.py
        deprecate('3.0.16-1')
(runtime callsite preserved at line 191)
```

### Sphinx pre-condition for Plan 02 — no new warnings introduced

```bash
$ rm -rf docs/build && pdm run sphinx-build ./docs/source ./docs/build 2>&1 | grep -ic warning
4
```

The 4 warnings are the same pre-existing baseline (InterfaceManager.list signature, cement.utils.shell.cmd inline-literal, api/index.rst toctree, theme `logo` option). The new admonition introduces zero additional warnings — confirms the directive is well-formed RST. Plan 02 will resolve the 4 baseline warnings; Plan 04 will flip `-W`.

### Cumulative gates — green at every commit

- `make comply` → ruff clean + mypy clean (51 source files)
- `make audit-public-api` → exit 0 (no public-API drift)
- `make test` → 320 passed, 1693 warnings, 100.00% coverage (3243 statements / 0 missing)

### CHANGELOG — 3 new entries appended to active Refactoring bucket

```bash
$ git diff e774fa9d..HEAD -- CHANGELOG.md | grep -E '^\+- \`\[' | wc -l
3
```

Verbatim diff (3 lines added at the end of the `Refactoring:` bucket inside `## 3.0.15 - DEVELOPMENT (will be released as stable/3.0.16)`):

```diff
+- `[core.deprecations]` Pin 3.0.10-1 and 3.0.16-1 removal version to v3.2.0
+- `[ext.logging]` Tighten FATAL deprecation removal version in docstrings
+- `[ext.smtp]` Document send() bool-return removal in v3.2.0
```

## Final Coverage Line

```
TOTAL                                 3243      0  100.00%
Required test coverage of 100% reached. Total coverage: 100.00%
===================== 320 passed, 1693 warnings in 51.91s ======================
```

## Deviations from Plan

### Plan grep regex anchored on the wrong quote style (informational, no behavior impact)

- **Found during:** Task 1 verification
- **Issue:** Plan body's verification command `grep -E '"3\.[0-9]+\.[0-9]+-[0-9]+":' cement/core/deprecations.py | wc -l | grep -qx 4` uses double-quote anchors; the DEPRECATIONS dict keys are single-quoted (`'3.0.8-1':`). The plan grep returns 0 against the live codebase shape.
- **Fix:** Verified with the single-quote variant `grep -cE "'3\.[0-9]+\.[0-9]+-[0-9]+':" cement/core/deprecations.py` returning 4. Same intent, same outcome.
- **Files modified:** None (plan-spec issue, not a code deviation)

### Plan grep `removed in Cement v3.2.0 | wc -l ≥ 2` returns 1 due to line-wrap (informational)

- **Found during:** Task 2 verification
- **Issue:** Plan body's `grep -F 'removed in Cement v3.2.0' cement/ext/ext_logging.py | wc -l | grep -qE '^[[:space:]]*2$'` expects ≥2 matches. The `set_level` docstring has the phrase on one line (line 147 — matches); the `fatal()` docstring wraps "removed in" at end of line 368 and "Cement v3.2.0" at start of line 369 (does not match). The literal phrase therefore appears once.
- **Fix:** Verified intent with `grep -cF 'Cement v3.2.0' cement/ext/ext_logging.py` = 2. Both docstrings correctly name v3.2.0; only the line-wrap differs.
- **Files modified:** None (plan-spec issue, not a code deviation)

No code-level deviations. The BEFORE/AFTER text in the plan was applied verbatim.

## Auth Gates

None — fully autonomous run.

## Self-Check: PASSED

- `cement/core/deprecations.py` exists and contains 4 entries all naming `Cement v3.2.0` ✓
- `cement/ext/ext_logging.py` set_level + fatal docstrings name v3.2.0; double-backticks applied; typo fixed ✓
- `cement/ext/ext_smtp.py` send() has `.. deprecated:: 3.0.16` admonition; runtime callsite preserved ✓
- `CHANGELOG.md` has 3 new Refactoring entries ✓
- All 3 commits exist in git log:
  - `dedacccb refactor(core.deprecations): tighten removal-version language` ✓
  - `3f809b90 refactor(ext.logging): tighten FATAL deprecation removal version in docstrings` ✓
  - `059fab38 refactor(ext.smtp): document send() bool-return removal in v3.2.0` ✓
- All gates green: `make comply` exit 0, `make audit-public-api` exit 0, `make test` exit 0 at 100.00% coverage ✓
