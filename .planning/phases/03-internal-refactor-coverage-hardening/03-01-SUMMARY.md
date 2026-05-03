---
phase: 03-internal-refactor-coverage-hardening
plan: 01
subsystem: testing
tags: [audit, public-api, ast, makefile, baseline, stdlib]

# Dependency graph
requires:
  - phase: 02-dependencies-ci-pipeline
    provides: 100% coverage gate (D-10/D-11/D-12) — Plan 01 leaves it green by touching no cement/ source.
provides:
  - scripts/audit-public-api.py (stdlib `ast` walker enumerating every non-underscore symbol under cement/)
  - Makefile `audit-public-api` STANDALONE target (NOT chained — D-03 invariant)
  - 03-PUBLIC-API-BASELINE.txt frozen snapshot (1014 lines, ASCII-sorted, byte-for-byte enforcement surface)
  - D-04 audit gate ENFORCING for every subsequent Phase 03 commit
affects:
  - 03-02 (ruff UP+FA family enable) — must keep `make audit-public-api` exit 0
  - 03-03..03-07 (UP, FA, pathlib, Any, pragma sweeps) — same gate
  - 03-08 (verification artifact) — references baseline diff result
  - All future 3.0.x patches and Phase 5 deprecation cycles (D-05 permanent affordance)

# Tech tracking
tech-stack:
  added:
    - "Python stdlib `ast` (already in stdlib — zero new dev dependency, per D-02)"
  patterns:
    - "Permanent dev affordance pattern: scripts/<X>.sh|.py + standalone Makefile target (mirrors scripts/cli-smoke-test.sh + Makefile cli-smoke-test target from quick task 260430-i7q)"
    - "Frozen-baseline-as-planning-artifact: sorted plain text, captured at first phase commit, diff-enforced byte-for-byte across every later commit (no cousin precedent in repo — Phase 03 D-04 seeds it)"

key-files:
  created:
    - scripts/audit-public-api.py
    - .planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt
  modified:
    - Makefile
    - CHANGELOG.md

key-decisions:
  - "AST walker handles `ast.ImportFrom` and `ast.Import` re-exports (deviation from RESEARCH.md canonical pattern) so that `cement/__init__.py`'s `from .core.foundation import App` re-exports surface as `cement:App` — Open Question 4 / Assumption A6 resolved by extending the walker, NOT by post-processing."
  - "AST walker drops `__future__` imports explicitly so `from __future__ import annotations` does not leak as a public symbol named `annotations` in every importing module (would have produced 28 spurious `<mod>:annotations` lines)."
  - "module_name_for() collapses `cement/__init__.py` to `cement` (drops the `__init__` part) so the canonical re-export surface emits as `cement:App` (matches what users actually `from cement import` against)."
  - "Sort discipline is Python's `sorted()` (ASCII byte order, equivalent to `LC_ALL=C sort`). Shell `sort -c` under default locale will report 'disorder' on uppercase-vs-lowercase boundaries — irrelevant; the Makefile uses `diff -u` against the captured baseline, byte-for-byte."

patterns-established:
  - "AST-walk public API audit: walk `cement/**/*.py`, emit `<module>:<NAME>` and `<module>:<Class>.<member>` (and `<module>:<Class>.<NestedClass>.<attr>` for the canonical Meta inner-class case), filter by `not name.startswith('_')`, skip `cement/cli/templates/` + `cement/cli/contrib/` (matches `[tool.coverage.run] omit`)."
  - "Standalone Makefile target shape: bare `audit-public-api:` (no prerequisites), echo-suppressed `@pdm run python scripts/audit-public-api.py > /tmp/cement-public-api.txt` then `@diff -u <baseline> /tmp/cement-public-api.txt`. NOT chained into `make test` or `make comply` (D-03)."

requirements-completed: [COV-01]

# Metrics
duration: 4min
completed: 2026-05-03
---

# Phase 3 Plan 01: Public API Baseline + Audit Gate Summary

**AST-walk public-API surface enumerator (1014 entries) + standalone `make audit-public-api` Makefile target + frozen 03-PUBLIC-API-BASELINE.txt snapshot — D-04 audit gate is now ENFORCING byte-for-byte across every subsequent Phase 03 commit.**

## Performance

- **Duration:** 4 min
- **Started:** 2026-05-03T21:33:51Z
- **Completed:** 2026-05-03T21:38:20Z
- **Tasks:** 3
- **Files modified:** 4 (2 created, 2 modified)

## Accomplishments
- `scripts/audit-public-api.py` (192 lines, stdlib-only, executable) walks every `.py` under `cement/`, emits 1014 sorted `module:Class.member` (or `module:NAME`) lines.
- `make audit-public-api` STANDALONE Makefile target wired (D-03 invariant verified — no prerequisite list, no other target depends on it).
- `03-PUBLIC-API-BASELINE.txt` captured (1014 lines, ASCII-sorted) and committed as the first Phase 03 commit.
- 100% coverage gate held: `pdm run pytest --cov=cement -x tests` → 316 passed, 100.00% coverage on the cement/ tree.
- Lint + types still green: `make comply-ruff` clean, `make comply-mypy` `Success: no issues found in 51 source files`.
- D-04 audit gate now ENFORCING for Wave 2 onward — any change in the public surface (signature/name/export) will fail `make audit-public-api` byte-for-byte.

## Task Commits

Wave 1 of Phase 03 lands as a SINGLE commit per plan D-22 step 1 (artifact + script + Makefile target + CHANGELOG entry):

1. **Wave 1 (Tasks 1+2+3): docs(03): capture public API baseline** — `f10f8ce3` (docs)

Per the plan's Task 3 acceptance criteria, the script (Task 1), Makefile target (Task 2), and baseline snapshot + CHANGELOG entry (Task 3) all land in this single commit. Tasks 1 and 2 are pre-commit work staged for the Wave 1 commit.

## Files Created/Modified
- `scripts/audit-public-api.py` (created, 192 lines) — stdlib `ast` walker; emits sorted public surface for `cement/**/*.py`. Executable.
- `Makefile` (modified, +4 lines) — added `audit-public-api` token to `.PHONY` and a STANDALONE 2-line target after `cli-smoke-test`. No other target depends on it.
- `.planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt` (created, 1014 lines) — sorted plain-text snapshot of the post-Phase-2/pre-Phase-3 public API surface. Frozen for the rest of Phase 03.
- `CHANGELOG.md` (modified, +1 line) — `[dev]` entry under `## 3.0.15 - DEVELOPMENT` Misc bucket: `Add make audit-public-api target + AST-walk public surface enumerator + baseline snapshot (Phase 03 D-02..D-05).`

## Decisions Made

- **Extended the AST walker beyond RESEARCH.md's canonical pattern to handle `ast.ImportFrom` and `ast.Import` re-exports.** RESEARCH.md's reference walker only enumerated `Assign`, `AnnAssign`, `FunctionDef`, `AsyncFunctionDef`, `ClassDef`. Without `ImportFrom` handling, `cement/__init__.py` (which is purely re-exports + `__all__`) would have emitted ZERO public symbols — failing the Open Question 4 sanity check ("output MUST contain at least 14 lines starting with `cement:`"). Adding `ImportFrom`/`Import` is consistent with D-01 ("public surface = anything not `_`-prefixed at module level") because re-exports ARE module-level public names downstream code imports against (`from cement import App`).

- **Skipped `from __future__ import` lines explicitly.** Without this filter, every module carrying `from __future__ import annotations` (28 modules pre-Phase-03 D-08) would emit a spurious `<mod>:annotations` symbol — those are compiler directives, not public API surface. After D-08 lands in a later wave the filter becomes a no-op (no `__future__` imports left in `cement/`), so it's defensive future-proofing too.

- **Collapsed `cement/__init__.py` module name to `cement` (drop the `__init__` suffix).** Without this, the surface for `App` would emit as `cement.__init__:App` rather than `cement:App`. The latter matches what users `from cement import App` against — the import-semantically correct dotted name for the package.

- **Sort discipline = Python's `sorted()` (ASCII byte order = `LC_ALL=C sort`).** Shell `sort -c` under default locale flags `Optional` < `main` as "disorder" because lowercase sorts before uppercase under most LC_COLLATE settings. Irrelevant — the Makefile gate uses `diff -u` against the captured baseline, which is byte-for-byte. The script's output is deterministically ordered per commit and reproducible across machines.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Extended AST walker to handle `ast.ImportFrom` / `ast.Import` re-exports**
- **Found during:** Task 1 sanity check (output had 0 `cement:` lines, plan required >= 14)
- **Issue:** RESEARCH.md's canonical AST walker (lines 239-345) only enumerates `Assign`, `AnnAssign`, `FunctionDef`, `AsyncFunctionDef`, `ClassDef` at module level. `cement/__init__.py` is purely re-exports + `__all__` — none of those node types apply. The walker emitted ZERO public symbols for `cement/__init__.py`, failing the Open Question 4 / Assumption A6 sanity check ("at least 14 cement: entries").
- **Fix:** Added `ast.ImportFrom` and `ast.Import` branches to `collect_module_symbols`. Re-exports surface as `<mod>:<exposed_name>` (uses `alias.asname` if present, else `alias.name`). Skips `from __future__ import` (compiler directive, not public surface) and `from X import *` (wildcard — cement does not use). Added 15 cement/ module-level re-exports including all 14 entries from `cement.__all__`.
- **Files modified:** scripts/audit-public-api.py
- **Verification:** `python3 scripts/audit-public-api.py | grep -c '^cement:'` → 15 (>= 14 required)
- **Committed in:** f10f8ce3 (Wave 1 commit)

**2. [Rule 1 - Bug] `__init__.py` module-name collapse**
- **Found during:** Task 1 sanity check (re-export entries surfaced as `cement.__init__:App` not `cement:App`)
- **Issue:** `module_name_for()` derived from `path.relative_to(root.parent).with_suffix('').parts` left the `__init__` part in the dotted module name, producing `cement.__init__:App`. The plan and downstream usage expect `cement:App` (matching `from cement import App`). Without the fix, the audit gate would have flagged every re-export as living in a non-existent `cement.__init__` namespace.
- **Fix:** After splitting parts, drop a trailing `__init__` part. So `cement/__init__.py` → `cement`, `cement/core/__init__.py` would → `cement.core`, etc.
- **Files modified:** scripts/audit-public-api.py
- **Verification:** `grep -E '^cement:App$' .planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt` → 1 match.
- **Committed in:** f10f8ce3 (Wave 1 commit)

**3. [Rule 1 - Bug] Filter `from __future__ import` to prevent `annotations` leakage**
- **Found during:** Task 1 sanity check (`sort -c` reported "disorder", investigation showed `<mod>:annotations` entries leaking from 28 modules)
- **Issue:** With `ImportFrom` handling added (deviation #1), every module carrying `from __future__ import annotations` (28 modules pre-Phase-03 D-08) emitted a `<mod>:annotations` line. `annotations` is a compiler directive bound by the Python parser — not a public API symbol. Without the filter, the baseline would have contained 28 spurious entries that would cleanly disappear when D-08 lands in a later wave, masquerading as public-API breakage.
- **Fix:** In the `ast.ImportFrom` branch, skip the node if `node.module == '__future__'`.
- **Files modified:** scripts/audit-public-api.py
- **Verification:** `python3 scripts/audit-public-api.py | grep -c ':annotations$'` → 0
- **Committed in:** f10f8ce3 (Wave 1 commit)

---

**Total deviations:** 3 auto-fixed (1 missing critical, 2 bugs — all surfaced by the plan's own sanity-check assertion in Task 1)
**Impact on plan:** All three deviations were necessary to satisfy the plan's stated acceptance criteria (≥14 cement: lines, sorted output, no private-symbol leaks). The plan's `<read_first>` note for Task 1 explicitly anticipated this: "If fewer than 14, the AST walker is missing a case (likely re-export aliases like `Controller = ArgparseController`); fix before proceeding." The fix went broader than re-export aliases (any `ImportFrom`/`Import` re-export, plus the `__init__` collapse and `__future__` filter), but the resulting surface IS the canonical public surface downstream users import against — strictly better baseline. No scope creep beyond Task 1's `<action>` directive (still 1 commit, still 4 files, still stdlib-only).

## Issues Encountered

- None — all auto-fixes happened during Task 1's sanity check before any commit landed. The Task 1 spec was explicit ("if fewer than 14 … fix before proceeding"), so the plan anticipated this outcome.

## User Setup Required

None - no external service configuration required. The audit gate is invoked via `make audit-public-api` (developer-side); CI is NOT wired to it per D-03 (standalone affordance).

## Next Phase Readiness

- D-04 audit gate is ENFORCING. Every subsequent Phase 03 commit MUST keep `make audit-public-api` at exit 0 — the baseline snapshot is byte-for-byte locked.
- 100% coverage gate (Phase 2 D-10/D-11/D-12) still green.
- Wave 2 (ruff UP+FA family enable, plan 03-02) is unblocked.
- All 8 plans for Phase 03 (waves 2-8) ride on the gate this plan installed.

## Self-Check: PASSED

**Files:**
- FOUND: scripts/audit-public-api.py (executable, 192 lines)
- FOUND: Makefile (audit-public-api target verified)
- FOUND: .planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt (1014 lines)
- FOUND: CHANGELOG.md (entry under ## 3.0.15 - DEVELOPMENT Misc bucket)

**Commit:**
- FOUND: f10f8ce3 (`docs(03): capture public API baseline`)

**Gates verified post-commit:**
- `make audit-public-api` → exit 0 (D-04 baseline matches surface byte-for-byte)
- `pdm run pytest --cov=cement -x tests` → 316 passed, 100.00% coverage
- `make comply-ruff` → All checks passed!
- `make comply-mypy` → Success: no issues found in 51 source files

---
*Phase: 03-internal-refactor-coverage-hardening*
*Completed: 2026-05-03*
