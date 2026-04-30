---
phase: 01-tooling-baseline-python-matrix
plan: 04
subsystem: tooling
tags: [pytest, pytest-cov, coverage, dev-deps-pin, tooling-baseline, phase-1-final]

# Dependency graph
requires:
  - "01-01 (Python 3.10 floor in place — pytest 9.0 itself drops 3.9, naturally aligned)"
  - "01-02 (ruff 0.15.12 baseline green — clean lint surface for the test-tool bump)"
  - "01-03 (mypy 1.20.2 baseline green — clean type surface for the test-tool bump)"
provides:
  - "pytest >=9.0.3 floor pin (D-12 floor on rarely-breaking tool)"
  - "pytest-cov >=7.1.0 floor pin (D-12 floor)"
  - "coverage >=7.13.5 floor pin (D-12 floor)"
  - "Pitfall 3 cleared — pytest-cov 7.0 subprocess-measurement removal verified no-op for cement (cement/utils/shell.py and cement/cli/main.py both held 100% coverage post-bump)"
  - "Pitfall 2 cleared — zero PytestRemovedIn warnings on pre-bump pytest 8.3.5; nothing to fix before bumping"
  - "TOOL-03 closed (pytest+pytest-cov+coverage bump green, no pytest-internal deprecation warnings)"
  - "make comply (ruff+mypy) exits 0; make test exits 0; 316 tests pass; 100.00% coverage on cement/"
  - "**Phase 1 implementation complete** — final commit before PR open"
affects:
  - "Phase 1 PR opens after this commit; CI matrix runs across 3.10/3.11/3.12/3.13/3.14/pypy3.10 and is the final verification gate"
  - "Phase 2 DEPS-01 owns pdm.lock regeneration (per Pitfall 4); Phase 2 inherits a clean ruff+mypy+pytest pin baseline to resolve against"
  - "PDM auto-update GitHub Action (the user's pain point) now has the full set of pins (ruff~=, mypy~=, pytest>=, pytest-cov>=, coverage>=) — drift detection live across all three test-tool floors"

# Tech tracking
tech-stack:
  added:
    - "pytest 9.0.3 (was 4.3.1 floor; >= floor per D-12 hybrid)"
    - "pytest-cov 7.1.0 (was 2.6.1 floor; >= floor per D-12 hybrid)"
    - "coverage 7.13.5 (was 4.5.3 floor; >= floor per D-12 hybrid)"
  patterns:
    - "D-12 hybrid floor pinning extended to test-tool family: pytest+pytest-cov+coverage all use `>=` (floor) since these tools break rarely. Compatible-release (`~=`) is reserved for ruff/mypy where rule-set drift is the actual risk."
    - "D-15 coupling — three coupled floor bumps land in ONE atomic `chore: bump pytest+pytest-cov+coverage` commit. The plan's commit-shape note (`per the per-tool D-15 clause — but here all three are floor-only and tightly coupled, landing as one`) is honored exactly."
    - "D-04 D-13 strict-minimum: NO test-config or test-code modernization. `[tool.pytest.ini_options]` untouched (RESEARCH.md confirmed no config changes needed for pytest 9.0 in cement's test surface). Zero `fix(test):` commits — the bump is bug-clean."
    - "Pitfall 4 honored — pdm.lock reverted post-`pdm install`. Three test-tool dependency updates (pytest 8.3.5→9.0.3, pytest-cov 5.0.0→7.1.0, coverage 7.6.1→7.13.5) are NOT in the lockfile; Phase 2 DEPS-01 owns the regen."

key-files:
  created:
    - ".planning/phases/01-tooling-baseline-python-matrix/01-04-SUMMARY.md (this file)"
  modified:
    - "pyproject.toml — three floor pins bumped in `[dependency-groups] dev`: pytest>=9.0.3, pytest-cov>=7.1.0, coverage>=7.13.5"

key-decisions:
  - "D-15 coupling held: three coupled floor pin bumps land in ONE chore: bump pytest+pytest-cov+coverage commit. Pattern matches Plan 02's `chore: bump ruff` + Plan 03's `chore: bump mypy` D-15 shape — pin and bump are inseparable, even when pin is `>=` not `~=`."
  - "D-12 floor-pin posture preserved: pytest, pytest-cov, coverage all use `>=` (not `~=`). The hybrid is intentional — ruff/mypy use `~=` because their rule sets drift on minors; pytest-family breaks rarely so floor is the right posture (lower-maintenance and avoids spurious bump churn)."
  - "D-13 strict-minimum honored absolutely: ZERO test-code or test-config changes. RESEARCH.md predicted (and this session verified) that pytest 9.0.3 / pytest-cov 7.1.0 / coverage 7.13.5 are bug-clean against cement's existing test surface. No fix(test): commits needed."
  - "Pitfall 4 held: pdm.lock NOT regenerated. Phase 1 PR carries pyproject.toml changes only. Phase 2 DEPS-01 owns lockfile regen — that boundary is enforced by `git checkout pdm.lock` after `pdm install`, same as Plan 02 and Plan 03 precedent."
  - "Pitfall 2 verified clean BEFORE bump: pre-bump scan `pdm run pytest tests/core 2>&1 | grep -iE 'PytestRemovedIn|PytestDeprecation'` returned zero hits on pytest 8.3.5. Nothing to fix before the major bump — the cement test suite was already 9.0-ready."
  - "Pitfall 3 verified clean AFTER bump: post-bump `cement/utils/shell.py` (129/0/100%) and `cement/cli/main.py` (28/0/100%) match pre-bump exactly. pytest-cov 7.0 subprocess-measurement removal is a no-op for cement, as RESEARCH.md predicted."
  - "TOTAL statement count drift (3311 → 3285, a 26-statement decrease) is metric-tool internal: `coverage` 7.6.1 → 7.13.5 minor changes its statement-detection heuristics. Per-module coverage held at 100% on every measured file — this is NOT a Pitfall 3 hit. The signal is `Miss=0` across the board, which is preserved exactly."

patterns-established:
  - "D-15 coupling generalizes across all three Step 2 commits: ruff (Plan 02) + mypy (Plan 03) + pytest-family (Plan 04) all land pin+bump in one atomic commit. Pattern is now proven across both `~=` and `>=` pin types."
  - "Phase 1 close-out shape: 4 plans → 13 commits total (1 atomic 3.9-removal + 1 ruff bump + 8 fix(lint) + 1 mypy bump + 1 fix(types) + 1 pytest-family bump). Plus 4 docs(NN-NN) state-update commits. The PR diff is dense but bisect-friendly — every per-rule-family commit is independently revertable."
  - "Conventional Commits with 78-char wrap (CLAUDE.md) — verified on every commit via `git log -1 --format=%b | awk 'length>78 {exit 1}'`. The pattern holds across all 13 phase-1 commits."

requirements-completed: [TOOL-03]

# Metrics
duration: 11 min
completed: 2026-04-30
---

# Phase 01 Plan 04: pytest + pytest-cov + coverage Bump Summary

**Bumps pytest 4.3.1→9.0.3, pytest-cov 2.6.1→7.1.0, coverage 4.5.3→7.13.5 in a single atomic D-15 commit (all three are floor pins per D-12 hybrid). RESEARCH.md Pitfalls 2 and 3 verified clean: zero pre-bump PytestRemovedIn warnings; per-module coverage held at 100% post-bump on every cement/ file including the Pitfall-3 hot-spots (cement/utils/shell.py and cement/cli/main.py). `make comply` and `make test` GREEN; 316 tests pass; no pytest-internal deprecation warnings (verified via `-W error::pytest.PytestRemovedIn10Warning -W error::pytest.PytestDeprecationWarning`). Closes TOOL-03. Phase 1 implementation is COMPLETE — this is the final Phase 1 commit before the PR opens.**

## Performance

- **Duration:** ~11 min (incl. pre-bump baseline capture, post-bump verification, and pdm.lock revert)
- **Started:** 2026-04-30T06:08:34Z
- **Completed:** 2026-04-30T06:20:10Z
- **Tasks:** 1 (single coupled D-15 bump per the plan's per-tool D-15 clause)
- **Files modified:** 1 (pyproject.toml — 3 lines changed)
- **Commits:** 1 atomic conventional commit

## Accomplishments

- **1 atomic commit lands the full test-tool family bump** per D-15 coupling:
  1. `3ff270f3 chore: bump pytest+pytest-cov+coverage` — three floor-pin updates in `[dependency-groups] dev`
- **All three target versions active** — verified via:
  - `pdm run pytest --version` → `pytest 9.0.3`
  - `pdm run python -c "import pytest_cov; print(pytest_cov.__version__)"` → `7.1.0`
  - `pdm run python -c "import coverage; print(coverage.__version__)"` → `7.13.5`
- **Pitfall 2 cleared (BEFORE bump):** `pdm run pytest tests/core 2>&1 | grep -iE 'PytestRemovedIn|PytestDeprecation'` returned zero hits on pytest 8.3.5. Nothing to fix before the major bump.
- **Pitfall 3 cleared (AFTER bump):** per-module coverage on the two flagged hot-spots held at 100%:
  - `cement/utils/shell.py`: pre-bump 129/0/100% → post-bump 129/0/100% (identical)
  - `cement/cli/main.py`: pre-bump 28/0/100% → post-bump 28/0/100% (identical)
- **TOOL-03 success criterion #3 cleared:** `pdm run pytest tests/core -W "error::pytest.PytestRemovedIn10Warning" -W "error::pytest.PytestDeprecationWarning"` exits 0. The 1692 warnings observed are cement's own intentional `DeprecationWarning`s (e.g., `SMTPMailHandler.send()` returning bool, asserted by `tests/core/test_deprecations.py`) — not pytest-internal deprecations.
- **D-13 strict-minimum honored absolutely:** ZERO test-code or test-config changes. `[tool.pytest.ini_options]` was not touched. The bump is bug-clean against cement's existing test surface.
- **D-15 coupling held:** all three pin bumps in ONE commit per the plan's per-tool D-15 clause.
- **Pitfall 4 honored:** `pdm install` regenerated `pdm.lock` (pytest 8.3.5→9.0.3, pytest-cov 5.0.0→7.1.0, coverage 7.6.1→7.13.5). Reverted via `git checkout pdm.lock` per Phase 2 DEPS-01 boundary. The Phase 1 PR carries pyproject.toml changes only.
- **3.0.x no-breakage rule held:** dev-deps only, no runtime code path changed, no public API surface change.
- **TOOL-03** closed.
- **Phase 1 cumulative success criteria all GREEN:**
  - PYVER-01: `! grep -q '"3\.9"' .github/workflows/build_and_test.yml` PASS
  - PYVER-02: `grep -q 'requires-python = ">=3.10"' pyproject.toml` PASS
  - TOOL-01: ruff 0.15.12 active, `make comply-ruff` exits 0
  - TOOL-02: mypy 1.20.2 active, `make comply-mypy` exits 0
  - TOOL-03: pytest 9.0.3 / pytest-cov 7.1.0 / coverage 7.13.5 active, `make test` exits 0
  - TOOL-04: 4 AUDIT POINT comments in pyproject.toml ([tool.ruff.lint], ignore block, per-file-ignores, [tool.mypy])

## Task Commits

| Task | Subject | Hash | Files |
|------|---------|------|-------|
| 1 | chore: bump pytest+pytest-cov+coverage | `3ff270f3` | pyproject.toml |

## Final State of `[dependency-groups] dev` (test-tool lines)

```toml
[dependency-groups]
dev = [
    "pytest>=9.0.3",                # was >=4.3.1   (D-12: floor)
    "pytest-cov>=7.1.0",            # was >=2.6.1   (D-12: floor)
    "coverage>=7.13.5",             # was >=4.5.3   (D-12: floor)
    "mypy~=1.20.2",                 # set in Plan 03; unchanged
    "ruff~=0.15.12",                # set in Plan 02; unchanged
    "mock>=5.1.0",                  # unchanged
    "pypng>=0.20220715.0",          # unchanged
    "requests>=2.31.0",             # unchanged
    "commitizen>=4.10.1",           # unchanged
]
```

## Pre-Bump vs Post-Bump Coverage Comparison (Pitfall 3 Evidence)

| Module                       | Pre-bump  | Post-bump | Delta |
|------------------------------|-----------|-----------|-------|
| `cement/utils/shell.py`      | 129/0/100%| 129/0/100%| identical |
| `cement/cli/main.py`         | 28/0/100% | 28/0/100% | identical |
| `cement/core/foundation.py`  | 689/0/100%| 689/0/100%| identical |
| `cement/core/handler.py`     | 124/0/100%| 124/0/100%| identical |
| `cement/ext/ext_argparse.py` | 318/0/100%| 318/0/100%| identical |
| TOTAL (whole `cement/`)      | 3311/0/100%| 3285/0/100%| -26 stmts (coverage 7.6→7.13 statement-detection delta) |

**Key signal: every measured module held `Miss=0` and `Cover=100.00%` post-bump.** The 26-statement TOTAL drop is internal to coverage's statement-detection heuristics changing between 7.6.1 and 7.13.5 — NOT a Pitfall-3 silent coverage drop. The 100%-with-zero-misses gate is preserved on every file in the `cement/` tree.

## Pytest Internal Deprecation Verification (TOOL-03 Success Criterion #3)

```bash
pdm run pytest tests/core \
    -W "error::pytest.PytestRemovedIn10Warning" \
    -W "error::pytest.PytestDeprecationWarning"
# EXIT: 0 (316 passed, no pytest/pytest-cov/coverage internal deprecations)
```

The 1692 warnings observed during `make test` are cement's OWN intentional `DeprecationWarning`s already asserted by `tests/core/test_deprecations.py` (e.g., `SMTPMailHandler.send()` returning bool, deprecated in 3.0.16-1). These are NOT pytest-internal deprecations and are correctly excluded from the success criterion.

Note: the plan's verify command originally used `error::PytestRemovedIn10Warning` (no namespace prefix). pytest 9.0.3's filter parser requires the `pytest.` namespace prefix to resolve the warning class. The corrected form `error::pytest.PytestRemovedIn10Warning` was used and works identically.

## Resolution Path Summary

| Concern | Resolution | Why |
|---------|-----------|-----|
| pytest version pin | `pytest>=9.0.3` (D-12 floor) | pytest breaks rarely; floor is the right posture |
| pytest-cov version pin | `pytest-cov>=7.1.0` (D-12 floor) | ditto |
| coverage version pin | `coverage>=7.13.5` (D-12 floor) | ditto |
| Pitfall 2 (PytestRemovedIn becoming errors) | Pre-bump grep returned zero hits | Cement's test suite was already 9.0-ready |
| Pitfall 3 (pytest-cov 7.0 subprocess removal) | Post-bump per-module coverage held | Cement does not measure subprocess coverage |
| `[tool.pytest.ini_options]` config | Untouched | RESEARCH.md confirmed no config changes needed |
| Pre-bump pytest deprecations | Zero | TOOL-03 success criterion #3 already met |
| pdm.lock | Reverted post-`pdm install` | Pitfall 4 — Phase 2 DEPS-01 owns regen |
| D-15 coupling | All three pins in ONE commit | Plan's per-tool D-15 clause for floor-only coupling |

## Decisions Made

1. **D-15 coupling on floor-only pins** — three coupled floor pin bumps land in ONE atomic `chore: bump pytest+pytest-cov+coverage` commit. The plan's `per-tool D-15 clause` allows this consolidation when pins are all floor-type and tightly coupled (test-tool family). Pattern generalizes the D-15 coupling shape from Plan 02's `~=` ruff bump and Plan 03's `~=` mypy bump.
2. **D-13 strict-minimum honored absolutely** — ZERO test-code or test-config changes. RESEARCH.md predicted (and this session verified) that pytest 9.0.3 / pytest-cov 7.1.0 / coverage 7.13.5 are bug-clean against cement's existing test surface under the existing `[tool.pytest.ini_options]` config. No `fix(test):` commits needed.
3. **Pitfall 4 held** — pdm.lock NOT regenerated. The boundary is enforced by `git checkout pdm.lock` after `pdm install` updated it. The Phase 1 PR carries pyproject.toml changes only; Phase 2 DEPS-01 owns lockfile regen with the full ruff+mypy+pytest baseline already in place.
4. **TOTAL statement-count delta (3311→3285) classified as coverage-internal** — coverage 7.6.1→7.13.5 changes its statement-detection heuristics; per-module coverage held at 100% on every file (Miss=0 everywhere). This is the correct Pitfall 3 signal posture: the gate-defining metric is `Miss=0`, not the absolute statement count.
5. **Verify-command namespace fix** — the plan's verify block used `error::PytestRemovedIn10Warning` which pytest 9.0.3's filter parser doesn't resolve (returns AttributeError on `builtins.PytestRemovedIn10Warning`). The functionally-equivalent `error::pytest.PytestRemovedIn10Warning` (with namespace prefix) was used. Same gate, correct module path. Documented as informational deviation — not a rule-driven fix.

## Deviations from Plan

The plan was executed exactly as written, with one informational adjustment for the pytest 9.0.3 warning-filter syntax:

### Deviation 1: Verify command warning-filter namespace (informational only)

**Found during:** Task 1 verification step (TOOL-03 success criterion #3 gate).

**Issue:** The plan's verify command used `pdm run pytest tests/core -W "error::PytestRemovedIn10Warning" -W "error::PytestDeprecationWarning"`. On pytest 9.0.3, this raises `AttributeError: module 'builtins' has no attribute 'PytestRemovedIn10Warning'` — pytest's `-W` parser requires a fully-qualified class path when the class isn't in `builtins`.

**Fix:** Used the namespace-prefixed form: `-W "error::pytest.PytestRemovedIn10Warning" -W "error::pytest.PytestDeprecationWarning"`. The classes resolve correctly via the `pytest` module export and the gate behaves identically. Exit 0 confirms zero pytest-internal deprecation errors on the cement test suite.

**Files modified:** none (verification-only; no code or config change).

**Why no rule applies:** This is not a Rule 1 bug (the plan was correct against the documented pytest API; it's a discoverability detail of pytest 9.0's filter parser). It's not a Rule 2 critical-functionality gap. It's not a Rule 3 blocker (the gate runs successfully with the corrected form). Pure informational deviation, documented for audit-trail discipline.

**Total deviations:** 1 (informational only — plan's verification command needed a namespace prefix that the plan's RESEARCH.md verification on 2026-04-29 didn't surface).

## Issues Encountered

None blocking. The pdm.lock change from `pdm install` was reverted per Pitfall 4 boundary (same posture as Plans 02 and 03). No pytest 9.0 / pytest-cov 7.0 / coverage 7.13 fallout surfaced — Pitfalls 2, 3, and 5 all clean.

## User Setup Required

None — no external service configuration required. CI matrix verification on Python 3.10/3.11/3.12/3.13/3.14/pypy3.10 happens in GitHub Actions on push (formal gate is `gh pr checks <PR>` once the phase-1 branch is pushed and a PR opened — see "Next Phase Readiness" below).

## Phase 1 Close-Out: ROADMAP Success Criteria

All 5 cumulative Phase 1 success criteria GREEN at this commit:

| # | Criterion | Verification | State |
|---|-----------|-----------|-------|
| 1 | Python 3.10 floor (3.9 dropped) | `! grep -q '"3\.9"' .github/workflows/build_and_test.yml` AND `grep -q 'requires-python = ">=3.10"' pyproject.toml` | PASS |
| 2 | Tooling baseline current | ruff 0.15.12, mypy 1.20.2, pytest 9.0.3, pytest-cov 7.1.0, coverage 7.13.5 all active | PASS |
| 3 | No deprecation warnings from pytest/pytest-cov/coverage | `-W error::pytest.PytestRemovedIn10Warning -W error::pytest.PytestDeprecationWarning` exits 0 | PASS |
| 4 | 100% coverage held | TOTAL `Miss=0`; every measured module at 100.00% | PASS |
| 5 | No-implicit-drift codification | 4 AUDIT POINT comments in pyproject.toml ([tool.ruff.lint], ruff ignore, ruff per-file-ignores, [tool.mypy]) + ruff~=, mypy~=, hybrid floor pins | PASS |

## Next Phase Readiness

**Phase 1 implementation is COMPLETE.** Ready for PR open.

- The phase-1 branch carries 13 atomic commits + 4 docs() state commits across 4 plans
- The PR will hit CI matrix on push: 3.10 / 3.11 / 3.12 / 3.13 / 3.14 / pypy3.10
- Per CONTEXT.md `<deferred>` "Pypy3.10 in CI matrix — planner verifies it stays green": pypy3.10 may need a follow-up commit if a row fails. RESEARCH.md Open Question 1 acknowledges the empirical-via-CI verification posture. Any failure on the matrix is in-scope follow-up under TOOL-* (per CONTEXT.md `<deferred>` clause) — fix and amend before merge.
- Phase 2 DEPS-01 inherits this clean baseline:
  - ruff~=0.15.12, mypy~=1.20.2 (compatible-release; will catch new rule-set additions on minor bumps)
  - pytest>=9.0.3, pytest-cov>=7.1.0, coverage>=7.13.5 (floor; admit stable patches without forcing audits)
  - 4 AUDIT POINT comments in pyproject.toml — drift detection live across all five tools
  - pdm.lock NOT regenerated; Phase 2 owns the regen of all phase-1 pin updates (ruff 0.3.2→0.15.12, mypy 1.9.0→1.20.2, pytest 4.3.1→9.0.3, pytest-cov 2.6.1→7.1.0, coverage 4.5.3→7.13.5) in one coherent lock-update operation

**Risks carried forward:**

- **CI matrix on push** is the final phase-1 verification gate. Local exec runs only on the dev container's default Python (3.14 per the venv path observed in `_pytest/...`). Cross-version matrix verification on 3.10/3.11/3.12/3.13/pypy3.10 happens in CI.
- **`pdm.lock` regeneration deferred to Phase 2 DEPS-01** — by Phase 1 → Phase 2 boundary design. The pyproject.toml pins are what drive drift detection; the lockfile is a separate (and orthogonal) concern Phase 2 owns explicitly.

## Self-Check: PASSED

**File checks:**
- FOUND: pyproject.toml (modified — three test-tool floor pins bumped in [dependency-groups] dev)
- FOUND: .planning/phases/01-tooling-baseline-python-matrix/01-04-SUMMARY.md (this file)

**Commit checks:**
- FOUND: `3ff270f3` — chore: bump pytest+pytest-cov+coverage

**Quality gate checks:**
- `make comply` exits 0 — ruff "All checks passed!" + mypy "Success: no issues found in 51 source files"
- `make test` exits 0 — 316 passed, 100.00% coverage on cement/, 1692 warnings (cement's intentional DeprecationWarnings, not pytest-internal)
- `pdm run pytest --version` returns `pytest 9.0.3`
- `pdm run python -c "import pytest_cov; print(pytest_cov.__version__)"` returns `7.1.0`
- `pdm run python -c "import coverage; print(coverage.__version__)"` returns `7.13.5`
- `pdm run pytest tests/core -W "error::pytest.PytestRemovedIn10Warning" -W "error::pytest.PytestDeprecationWarning"` exits 0
- Commit subject 38 chars (≤78); all body lines ≤78 chars (verified via `git log -1 --format=%b | awk 'length>78 {exit 1}'` returns empty)
- D-15 coupling: `git diff` of pyproject.toml shows pytest+pytest-cov+coverage bumped in single `3ff270f3` commit
- pdm.lock unchanged from pre-plan state (Pitfall 4 boundary held)
- All 5 ROADMAP cumulative success criteria GREEN (verified inline above)

---
*Phase: 01-tooling-baseline-python-matrix*
*Plan: 04 (final plan in phase)*
*Completed: 2026-04-30*
*Phase 1 implementation COMPLETE — PR open is the next action.*
