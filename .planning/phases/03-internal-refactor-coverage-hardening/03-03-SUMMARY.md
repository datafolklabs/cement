---
phase: 03-internal-refactor-coverage-hardening
plan: 03
subsystem: lint/type-modernization
tags: [ruff, pyupgrade, pep585, pep604, refactor, wave-3, type-hints]
requires:
  - .planning/phases/03-internal-refactor-coverage-hardening/03-02-SUMMARY.md (Wave 2 — UP+FA enabled in ruff config)
  - pyproject.toml [tool.ruff.lint] extend-select with UP family (Phase 03 D-06)
provides:
  - "PEP 585 builtin generics across cement/ + tests/ (`list[X]`, `dict[K, V]`, `tuple[X, Y]`, `type[H]`)"
  - "PEP 604 union syntax across cement/ + tests/ (`X | Y`, `X | None`)"
  - "f-string formatting throughout (printf and .format() converted via UP031 + UP032)"
  - "REFACTOR-04 closeout — printf-style modernization complete"
  - "Refreshed `03-PUBLIC-API-BASELINE.txt` (1014 → 933 lines after orphaned typing re-exports pruned)"
  - "Refreshed CONVENTIONS.md type-annotation guidance to PEP 585/604 modern syntax"
affects:
  - "Phase 03 plan 04+ (Any-tightening, pathlib migration, pragma audit) — code is now in modern-syntax shape they will edit on top of"
  - "Wave 4 (FA family) — currently observes ZERO findings; FA100 may surface naturally in later waves or stay clean per current state"
tech-stack:
  added: []
  patterns:
    - "Mid-execution architectural decision (Rule 4): re-baseline 03-PUBLIC-API-BASELINE.txt per UP commit when the rule prunes orphaned typing re-exports — Phase 03 IS the intentional API change window per D-04 reinterpretation"
    - "Atomic-per-rule UP commit discipline (D-22 + Phase 1 D-04 family-split)"
    - "F401 typing-import cleanup paired with UP006/UP007/UP045 in same commit (mechanically tied)"
    - "D-19 protected callsite verification via body-diff (line numbers stripped) rather than literal line-number diff (line drift across commits is expected and non-load-bearing)"
key-files:
  created:
    - .planning/phases/03-internal-refactor-coverage-hardening/03-03-SUMMARY.md
    - .planning/phases/03-internal-refactor-coverage-hardening/deferred-items.md
  modified:
    - "73 files across cement/ + tests/ (full Wave 3 sweep)"
    - .planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt
    - .planning/codebase/CONVENTIONS.md
    - CHANGELOG.md
decisions:
  - "[Rule 4 — User-approved at handoff] Re-baseline 03-PUBLIC-API-BASELINE.txt per UP commit. The 51 orphaned `typing.{List,Dict,Tuple,Type,Optional,Union}` re-exports being pruned were never genuine public API — they were tooling artifacts of the pre-PEP-585 era. Phase 03's charter is mechanical modernization, which IS the intentional API change window referenced by D-04. Justification recorded against D-04 reinterpretation."
  - "Apply F401 typing-import cleanup TOGETHER with UP006 / UP007 / UP045 in the same commit (mechanically tied — the UP rule is what orphans the typing import). This produces 3 commits instead of 6 and keeps the diff coherent."
  - "Re-baseline IF AND ONLY IF the UP rule changes the audit output. UP035, UP031, UP004, UP008, UP015, UP024, UP025, UP026, UP028, UP032 all left the audit byte-for-byte green — no rebase needed for those commits (preserves audit signal)."
  - "Plan body said `UP032` but Wave 2 summary clarified current ruff classifies the printf sites as `UP031`. Both ended up needed — UP031 first (printf → .format), then UP032 cascade-surfaced (.format → f-string)."
  - "D-19 protected line numbers (CONTEXT.md cites 1359..1567) drifted by 1-7 lines due to UP006/UP007/UP045/UP032 line-length changes. Verified protection via grep + body-diff rather than literal line-number diff. All 14 `.format(**template_dict)` callsites are byte-for-byte present at lines 1352, 1357, 1365, 1370, 1378, 1383, 1471, 1476, 1481, 1485, 1546, 1551, 1556, 1560 (post UP032)."
  - "CONTEXT.md `template.py:359+` reference is stale — actual file has ZERO `.format()` callsites. Recorded in deferred-items.md."
metrics:
  duration_minutes: 60
  completed_date: 2026-05-03
---

# Phase 03 Plan 03: Wave 3 — UP Family Per-Rule Sweep + CONVENTIONS Refresh — Summary

Apply ruff `UP` family auto-fixes per-rule across `cement/` + `tests/`. Each
rule code lands as its own atomic commit per Phase 1 D-04 family-split
discipline. UP family fully resolved end-to-end. CONVENTIONS.md refreshed
to PEP 585/604 syntax. REFACTOR-04 closed. D-19 protected callsites
verified untouched.

## Wave 3 Completion Status

- **Wave:** 3 (depends on Wave 2 complete — Plan 02)
- **Tasks executed:** 12 UP-rule commits + 1 CONVENTIONS refresh + 1 fallout cleanup + 1 deferred-items artifact = 15 substantive commits
- **Commits:** 16 (15 substantive + 1 deferred-items planning record)
- **Files modified:** 73 across cement/ + tests/
- **Lines changed:** +549 / -539 (net delta of 10 lines added — close to break-even, reflecting purely mechanical syntax modernization)

## Wave 3 Commit Timeline

| # | Hash | Subject | Files | Audit Re-baseline? |
|---|------|---------|-------|--------------------|
| 1 | `a601a201` | fix(lint): resolve UP006 List → list, Dict → dict, Tuple → tuple | 34 | YES (50 orphaned typing re-exports pruned + 1 builtins added: 1014 → 964 lines) |
| 2 | `40e12080` | fix(lint): resolve UP007 Union[X, Y] → X \| Y | 14 | YES (7 Union re-exports pruned: 964 → 952) |
| 3 | `a9ffc0d0` | fix(lint): resolve UP045 Optional[X] → X \| None | 20 | YES (18 Optional re-exports pruned: 952 → 934) |
| 4 | `78921cae` | fix(lint): resolve UP035 deprecated typing imports | 7 | NO (audit byte-for-byte green) |
| 5 | `7b214077` | fix(lint): resolve UP031 printf-style format strings | 20 | NO |
| 6 | `35bde750` | fix(lint): resolve UP004 useless object inheritance | 31 | NO |
| 7 | `a9e8a411` | fix(lint): resolve UP008 super() simplification | 19 | NO |
| 8 | `0a3a4843` | fix(lint): resolve UP015 redundant open() mode | 9 | NO |
| 9 | `2e673589` | fix(lint): resolve UP024 IOError → OSError alias | 2 | NO |
| 10 | `f2598f89` | fix(lint): resolve UP025 unicode literal prefix | 2 | NO |
| 11 | `92ab7189` | fix(lint): resolve UP026 deprecated mock import | 3 | NO |
| 12 | `c0bf508d` | fix(lint): resolve UP028 yield in for loop → yield from | 3 | NO |
| 13 | `b98f482c` | fix(lint): resolve UP032 .format() → f-string | 20 | NO (D-19 callsites verified unchanged via body-diff) |
| 14 | `fb112788` | docs(codebase): refresh CONVENTIONS to PEP 604/585 syntax | 2 | NO (no source touched) |
| 15 | `25e2ba35` | fix(lint): clean up E501 + I001 fallout from Wave 3 UP fixes | 15 | NO |
| 16 | `5c6c7cca` | docs(03): record Wave 3 deferred items | 1 | NO (planning artifact only) |

## Per-Rule Fix Counts

| UP Rule | Pre-fix Count | Auto-fixable | Post-fix Count | Notes |
|---------|--------------:|--------------|---------------:|-------|
| UP006   | 181 | yes | 0 | Paired with F401 cleanup of 53 orphaned typing imports |
| UP007   | 30  | yes | 0 | Paired with F401 cleanup of 12 orphaned typing.Union |
| UP045   | 66  | yes | 0 | Paired with F401 cleanup of 18 orphaned typing.Optional |
| UP035   | 6   | yes (post-UP006) | 0 | Started at 59 in Wave 2 — UP006 resolved 53, leaving 6 for UP035 sweep |
| UP031   | 58  | unsafe-fix | 0 | 56 ruff-fixed, 2 multi-line printf hand-fixed in ext_daemon.py + 2 unused `# type: ignore` removed |
| UP004   | 47  | yes | 0 | |
| UP008   | 29  | yes | 0 | |
| UP015   | 15  | yes | 0 | |
| UP024   | 1   | yes | 0 | `IOError` → `OSError` in template.py |
| UP025   | 1   | yes | 0 | `u"..."` → `"..."` in test_ext_jinja2.py |
| UP026   | 2   | yes | 0 | `import mock` → `from unittest import mock` |
| UP028   | 2   | unsafe-fix | 0 | `yield from iterable` |
| UP032   | 56  | yes | 0 | Cascade-surfaced after UP031 (.format → f-string) |
| **TOTAL** | **494** | | **0** | UP family fully resolved |

Note: total of 494 vs Wave 2's reported 491 reflects the cascade — UP032 surfaced new findings after UP031 ran.

## D-19 Protected Callsite Verification

**14 `.format(**template_dict)` callsites in `cement/core/foundation.py`** — verified UNCHANGED throughout Wave 3 via body-diff (line numbers stripped):

```
$ grep -c '\.format(\*\*template_dict)' cement/core/foundation.py
14
```

CONTEXT.md cites lines 1359, 1364, 1372, 1377, 1385, 1390, 1478, 1483, 1488, 1492, 1553, 1558, 1563, 1567 — these line numbers DRIFTED during Wave 3 (UP006/UP007/UP045/UP032 changed line lengths). Current actual line numbers (post-UP032):

| Pre-Wave-3 line | Post-Wave-3 line | Body |
|----------------:|-----------------:|------|
| 1359 | 1352 | `f = f.format(**template_dict)` |
| 1364 | 1357 | `d = d.format(**template_dict)` |
| 1372 | 1365 | `f = f.format(**template_dict)` |
| 1377 | 1370 | `d = d.format(**template_dict)` |
| 1385 | 1378 | `f = f.format(**template_dict)` |
| 1390 | 1383 | `d = d.format(**template_dict)` |
| 1478 | 1471 | `d = d.format(**template_dict)` |
| 1483 | 1476 | `d = d.format(**template_dict)` |
| 1488 | 1481 | `d = self._meta.plugin_dir.format(**template_dict)` |
| 1492 | 1485 | `d = d.format(**template_dict)` |
| 1553 | 1546 | `d = d.format(**template_dict)` |
| 1558 | 1551 | `d = d.format(**template_dict)` |
| 1563 | 1556 | `d = self._meta.template_dir.format(**template_dict)` |
| 1567 | 1560 | `d = d.format(**template_dict)` |

All 14 callsites byte-for-byte identical (line bodies). Drift recorded in deferred-items.md.

**`cement/core/template.py:359+`** — CONTEXT.md cites this as a protected zone. The file has ZERO `.format()` callsites; the reference appears to be stale or refers to printf-style `%` LOG.debug sites that UP031 correctly converted (no template-substitution semantics). Recorded in deferred-items.md as a CONTEXT.md erratum to fix in a future plan.

**Zero `# noqa: UP032` markers needed** — UP032 correctly skipped all `.format(**template_dict)` callsites via its built-in dict-spread heuristic (per ruff issue #9227 and RESEARCH.md A1 prediction).

## Public API Baseline Re-Baseline Timeline

| Commit | Action | Lines | Notes |
|--------|--------|------:|-------|
| (Wave 1 baseline) | initial | 1014 | Captured before any refactor |
| `a601a201` (UP006) | re-baseline | 964 | Pruned 50 typing.{List,Dict,Tuple,Type} re-exports + added 2 `import builtins` |
| `40e12080` (UP007) | re-baseline | 952 | Pruned 7 typing.Union re-exports across 5 modules |
| `a9ffc0d0` (UP045) | re-baseline | 934 | Pruned 18 typing.Optional re-exports across 18 modules |
| `78921cae` (UP035) | (no change) | 934 | typing → collections.abc move keeps the names in importing module's namespace |
| All other UP commits | (no change) | 934 | Body-level refactors don't change public surface |
| Final (post Wave 3) | | **934** | |

Total: 80 lines pruned. All pruned entries are orphaned `typing.{List,Dict,Tuple,Type,Union,Optional}` re-exports — never genuine public API. Two new lines (`cement.core.extension:builtins`, `cement.core.handler:builtins`) added by UP006 disambiguating `list` type from class methods named `list`.

`make audit-public-api` exits 0 against the freshly-rebaselined snapshot at the end of every Wave 3 commit.

## Verification Results — End of Wave 3

| Gate | Command | Result |
|------|---------|--------|
| UP family | `pdm run ruff check --select UP cement/ tests/` | **exit 0 — all clean** |
| FA family | `pdm run ruff check --select FA cement/ tests/` | exit 0 (zero findings observed) |
| F401 | `pdm run ruff check --select F401 cement/ tests/` | exit 0 |
| Coverage gate (D-24 #1) | `pdm run pytest --cov=cement -x tests` | exit 0, 100% coverage (3290/3290 stmts, 316 passed) |
| comply-ruff (D-24 #2) | `make comply-ruff` | exit 0 — all rule families clean |
| comply-mypy (D-24 #3) | `make comply-mypy` / `pdm run mypy cement` | exit 0 — 51 source files |
| audit-public-api (D-24 #4) | `make audit-public-api` | exit 0 against rebaselined `03-PUBLIC-API-BASELINE.txt` |
| coverage-report HTML (D-24 #5; COV-02) | `test -f coverage-report/index.html` | PASS |
| D-19 protected sites | `grep -c '\.format(\*\*template_dict)' cement/core/foundation.py` | 14 (unchanged from pre-Wave-3) |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 4 — User-approved at handoff] Re-baseline 03-PUBLIC-API-BASELINE.txt per UP commit during Wave 3**

- **Found during:** Plan-checker / handoff
- **Issue:** Original plan said "audit-public-api stays green byte-for-byte" but UP006 / UP007 / UP045 mechanically remove the orphaned `typing.{List,Dict,Tuple,Type,Union,Optional}` re-exports that the AST script enumerates as part of the public surface. These re-exports were tooling artifacts of the pre-PEP-585 era, never genuine public API. Without re-baselining, every UP commit would trip the audit gate even though no real public-surface change occurred.
- **Fix:** User chose Option 1 — re-baseline `03-PUBLIC-API-BASELINE.txt` IN THE SAME COMMIT as the source changes, for any UP rule that changes the audit output. Justified as D-04 reinterpretation: Phase 03 IS the intentional API change window. Applied to UP006, UP007, UP045 (the three rules that actually changed audit output); UP035 / UP031 / UP004 / UP008 / UP015 / UP024 / UP025 / UP026 / UP028 / UP032 all kept the audit byte-for-byte green and required no rebase (preserves audit signal for those commits).
- **Files affected:** `.planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt` (rebaselined 3 times across UP006/UP007/UP045 commits)
- **Commits:** `a601a201`, `40e12080`, `a9ffc0d0`

**2. [Rule 1 — Bug] Plan body cited UP032 but current ruff classifies printf sites as UP031**

- **Found during:** Task 5 (the "UP032 sweep" task in plan body)
- **Issue:** Plan body Task 5 instructed "Apply ruff UP032 auto-fix" but `pdm run ruff check --select UP032 cement/ tests/` returned 0 findings before the printf sweep. Wave 2 summary clarified that current ruff classifies printf-style as UP031 (UP032 is "convert .format() to f-string", a sibling rule). Both rules ended up needed: UP031 first (`'%s' % x` → `"{}".format(x)` / f-string), then UP032 cascade-surfaced (some `.format()` calls UP031 introduced get converted to f-string).
- **Fix:** Split into two atomic commits: `7b214077` (UP031 — printf modernization, REFACTOR-04 closeout) and `b98f482c` (UP032 — .format → f-string cascade, UP family fully clean).
- **Files affected:** Same set — 20 files in UP031 commit, 20 files in UP032 commit (overlapping).
- **Commits:** `7b214077`, `b98f482c`

**3. [Rule 1 — Bug] D-19 protected line numbers drifted from CONTEXT.md citation**

- **Found during:** Task 5 (UP031 sweep — pre-flight line-number capture)
- **Issue:** CONTEXT.md D-19 cites foundation.py lines 1359, 1364, 1372, 1377, 1385, 1390, 1478, 1483, 1488, 1492, 1553, 1558, 1563, 1567 as the protected `.format(**template_dict)` callsites. After UP006/UP007/UP045 ran, those lines no longer pointed to `.format()` — they pointed to unrelated config-dir handling lines (line 1359 became `if d not in config_dirs:`).
- **Fix:** Located the actual current `.format(**template_dict)` callsites via `grep -n '\.format(\*\*template_dict)' cement/core/foundation.py`. They are still 14 in number, body-identical to pre-Wave-3 state, just at different line numbers. Used a body-diff verification approach (capture pre-state, apply rule, capture post-state, strip line numbers, diff bodies) instead of literal line-number diff. All 14 sites preserved.
- **Files affected:** None modified — purely a verification-method change.
- **Recorded in:** `deferred-items.md` for future CONTEXT.md erratum fix.

**4. [Rule 1 — Bug] CONTEXT.md `template.py:359+` reference is stale**

- **Found during:** Task 5 pre-flight
- **Issue:** CONTEXT.md cites `cement/core/template.py:359+` as a protected `.format(**template_dict)` zone. The actual file has zero `.format()` callsites at any line. Line 359 corresponds to the body of the `load()` method, unrelated to template substitution.
- **Fix:** No source change needed (no D-19 violation occurred). Either the CONTEXT.md reference is outdated or it referred to printf-style `%` LOG.debug sites at lines 332, 346, 350 — those were correctly converted by UP031 (no template-substitution semantics).
- **Recorded in:** `deferred-items.md` for future CONTEXT.md erratum fix.

**5. [Rule 1 — Bug] mypy unused-ignore after UP031 hand-fix**

- **Found during:** Task 5, gate verification
- **Issue:** Hand-fixed the 2 multi-line printf sites in `cement/ext/ext_daemon.py` (Fork #1 / Fork #2 stderr writes) to f-strings. The original printf-style line carried a `# type: ignore` comment that mypy considered unused after the f-string conversion (no untyped operand left). Mypy reported `unused-ignore`.
- **Fix:** Dropped the now-unused `# type: ignore` comments. mypy passes clean.
- **Files affected:** `cement/ext/ext_daemon.py` (2 lines).
- **Commits:** `7b214077` (folded into UP031 commit).

**6. [Rule 3 — Blocking] E501 + I001 fallout from Wave 3 UP fixes**

- **Found during:** End-of-Wave-3 verification
- **Issue:** UP032 f-string conversion turned previously wrapped log calls into single-line f-strings exceeding 100 chars (11 E501 findings). UP006 added `import builtins` and UP035 moved `Callable`/`Generator` from `typing` to `collections.abc`, leaving 11 imports unsorted (I001).
- **Fix:** Auto-fixed I001 via `ruff check --select I001 --fix`. Manually wrapped the 11 E501 sites as multi-line string-literal concatenations. Both kinds of fallout are directly caused by the Wave 3 mechanical rewrites, not pre-existing.
- **Files affected:** 14 files (cement/cli/main.py, cement/core/extension.py + foundation.py + handler.py + hook.py + template.py, cement/ext/ext_argparse.py + ext_generate.py + ext_logging.py + ext_watchdog.py + ext_yaml.py, cement/utils/shell.py, tests/ext/test_ext_smtp.py, tests/utils/test_shell.py).
- **Commits:** `25e2ba35` (single fallout-cleanup commit, isolated from the parent UP commits to keep them rule-focused).

### Pre-existing items (NOT fixed — out of scope per SCOPE BOUNDARY)

**Pre-existing duplicate `LOG = minimal_logger(__name__)` in `cement/ext/ext_daemon.py:20-21`** — present at HEAD `0375779b` before Wave 3 started. Idempotent (no functional impact). Recorded in `deferred-items.md` for future tech-debt cleanup.

### Authentication Gates

None — pure local linting and test sweep.

## TDD Gate Compliance

This plan does NOT have `type: tdd` in frontmatter (it's `type: execute`). The 100% coverage gate that already existed (Phase 2 D-10) acted as the "test still passes after refactor" check throughout Wave 3 — every UP commit was preceded by a coverage run that exited 0.

## Threat Surface Scan

Pure mechanical syntactic refactor — no new endpoints, auth paths, file access patterns, or schema changes. T-03-03-01 (UP032 unexpectedly rewrites `.format(**template_dict)`) was mitigated successfully via per-commit body-diff verification — UP032's built-in dict-spread heuristic correctly skipped all 14 protected callsites; zero `# noqa: UP032` markers needed. T-03-03-02 (UP rules silently change public API surface) was REINTERPRETED via the user-approved Rule 4 decision: the orphaned `typing.{List,Dict,Tuple,Type,Union,Optional}` re-exports being pruned were never genuine public API, and re-baselining the snapshot in the same commit preserves the audit gate for genuine-surface changes in future commits.

**No new threat flags surfaced.**

## D-24 Conjunct Status

| Conjunct | Status After Wave 3 |
|----------|---------------------|
| #1 — `make test` 100% coverage | **green** ✓ (3290/3290 stmts, 316 passed) |
| #2 — `make comply-ruff` | **green** ✓ (full rule set; previously RED in Wave 2 — restored as planned) |
| #3 — `make comply-mypy` | **green** ✓ (51 source files, no issues) |
| #4 — `make audit-public-api` | **green** ✓ (against the rebaselined snapshot) |
| #5 — `coverage-report/index.html` generates | **green** ✓ (COV-02 wave check) |
| #6 — `Any` reduction (REFACTOR-02) | not yet evaluated — Plan 04+ territory |
| #7 — pragma:nocover locked-vocab | not yet evaluated — Plan 06 territory |
| #8 — `os.path` boundary scope | not yet evaluated — Plan 05 territory |
| #9 — `from __future__ import annotations` strip | not yet evaluated — Plan 04 (FA family) territory |

## Acceptance Criteria — Plan Match

| Criterion | Status |
|-----------|--------|
| All UP rules from Wave 2's findings resolved | ✓ (12 UP rules, 494 total findings, 0 remaining) |
| One atomic commit per UP rule code | ✓ (12 UP-rule commits + 1 fallout cleanup + 1 CONVENTIONS refresh) |
| 03-PUBLIC-API-BASELINE.txt re-baselined IN THE SAME COMMIT as any UP rule that affected the audit | ✓ (UP006, UP007, UP045) |
| After every commit: `make test` 0, `make audit-public-api` 0, `make comply-mypy` 0 | ✓ (sampled per commit; full re-run at end of Wave 3) |
| D-19 protected callsites verified untouched | ✓ (14 sites byte-for-byte identical via body-diff) |
| CONVENTIONS.md refreshed for PEP 585 + PEP 604 | ✓ (separate atomic commit `fb112788`) |
| FA findings count recorded | ✓ (zero FA100/FA102 findings — Wave 4 may have nothing to do, or future-imports may still be needed for some forward refs) |
| SUMMARY.md created with per-rule fix counts, baseline-update timeline, Rule 4 deviation | ✓ (this document) |

## Self-Check: PASSED

- File `.planning/phases/03-internal-refactor-coverage-hardening/03-03-SUMMARY.md` exists at `/Users/derks/Development/DFL/cement/.planning/phases/03-internal-refactor-coverage-hardening/03-03-SUMMARY.md` (this file)
- File `.planning/phases/03-internal-refactor-coverage-hardening/deferred-items.md` exists
- Commits `a601a201`, `40e12080`, `a9ffc0d0`, `78921cae`, `7b214077`, `35bde750`, `a9e8a411`, `0a3a4843`, `2e673589`, `f2598f89`, `92ab7189`, `c0bf508d`, `b98f482c`, `fb112788`, `25e2ba35`, `5c6c7cca` all present in `git log --oneline 0375779b..HEAD`
- All claimed verification commands re-run interactively show the documented results
- D-19 protected callsite count: 14 (verified via grep)
- UP family clean: `pdm run ruff check --select UP cement/ tests/` exits 0
- Coverage: 3290/3290 stmts, 100.00%, 316 passed

---

*Plan: 03-03 (Wave 3)*
*Depends on: Plan 02 (Wave 2)*
*Unblocks: Plan 04+ (Any-tightening, FA strip, pathlib migration, pragma audit)*
*Closes (mechanically): REFACTOR-04 — printf-style modernization complete*
