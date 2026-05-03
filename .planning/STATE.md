---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: executing
stopped_at: Phase 2 context gathered
last_updated: "2026-05-03T01:00:05.235Z"
last_activity: 2026-05-03 -- Phase 02 execution started
progress:
  total_phases: 7
  completed_phases: 2
  total_plans: 13
  completed_plans: 5
  percent: 38
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-04-24)

**Core value:** Cement 3 stays solid, secure, performant, and bug-free under strict backward compatibility — while being continuously maintained against a modern Python and tooling ecosystem.
**Current focus:** Phase 02 — dependencies-ci-pipeline

## Current Position

Phase: 02 (dependencies-ci-pipeline) — EXECUTING
Plan: 1 of 8
Status: Executing Phase 02
Last activity: 2026-05-03 -- Phase 02 execution started

Progress: [████░░░░░░] 38% (5/13 plans completed)

## Performance Metrics

**Velocity:**

- Total plans completed: 6
- Average duration: —
- Total execution time: 0 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01 | 4 | - | - |
| 01.1 | 1 | - | - |

**Recent Trend:**

- Last 5 plans: —
- Trend: —

*Updated after each plan completion*
| Phase 01-tooling-baseline-python-matrix P01 | 2 min | 1 tasks | 9 files |
| Phase 01-tooling-baseline-python-matrix P02 | 20 min | 9 tasks | 91 files |
| Phase 01-tooling-baseline-python-matrix P03 | 3 min | 2 tasks tasks | 2 files files |
| Phase 01-tooling-baseline-python-matrix P04 | 11 | 1 tasks | 1 files |
| Phase 01.1 P01 | 12 min | 7 tasks | 6 files |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Initialization: Anchor priority is Clean & Green (lint/types/deps/CI/coverage) — unblock the baseline before chasing security/performance.
- Initialization: Deprecations OK in 3.0.x; removals deferred to 3.2.0.
- Initialization: Internal refactor is cleanup-only; no Cement 4 architectural seams.
- Initialization: Python 3.9 dropped this milestone (EOL Oct 2025) per standing policy.
- Initialization: Release cut as 3.0.16 (even-patch convention); current dev = 3.0.15.
- [Phase 01-tooling-baseline-python-matrix]: D-05 atomic-commit pattern proven on a 9-file change: all Python 3.9 traces dropped in a single conventional commit (chore: drop python 3.9 from supported matrix, 00d37e16) without splitting. — Validates D-05: ALL 3.9 traces simultaneously. Bisect anchor is clean — before this commit 3.9 supported, after it dropped. PYVER-03 audit grep returned empty on first pass.
- [Phase 01-tooling-baseline-python-matrix]: Travis CI configuration deleted entirely (.travis.yml) rather than partially edited to drop 3.8/3.9 entries. — Travis is no longer cement's CI; GitHub Actions is. Per RESEARCH.md Pitfall 7 + Open Question 2, keeping a non-active CI definition is dead infrastructure and a future-grep liability. Deletion satisfies D-05 ALL-3.9-traces cleanly.
- [Phase 01-tooling-baseline-python-matrix]: D-13/D-14 strict-minimum upheld: cement/utils/fs.py from __future__ import annotations and the self-flagged remove-after-3.9-EOL comment stay in place this phase. — Phase 1 is mechanical-removal-only; modernization-style cleanup defers to Phase 3 REFACTOR-04. The PYVER-03 audit grep filter explicitly excludes the __future__ line for this reason.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 02]: D-15 coupling held — ruff pin (~=0.15.12) + preview flip + 11-family extend-select + AUDIT POINT comment all land in ONE chore: bump ruff to 0.15 commit. Pin and bump are inseparable for D-08 hybrid drift detection.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 02]: A001/A002 absorbed via broad-ignore in [tool.ruff.lint] ignore (Option C from plan). 18 sites cluster across 5 files in framework-intentional builtin-shadowing patterns matching Python stdlib conventions (logging.Formatter format kwarg, Tmp.__init__ dir kwarg). Same posture attrs uses for the same reason; per-call noqa rejected as polluting too many sites for a structurally pervasive pattern.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 02]: C901 absorbed in [tool.ruff.lint] ignore with Phase 3 REFACTOR-01/02 cross-reference (RESEARCH.md Open Question 3 explicit recommendation). 12 hot-spot functions in cement/core/foundation.py + handler.py exceed default complexity 10; refactoring violates D-13 strict-minimum. Adding C90 family to extend-select keeps the signal active for new code.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 02]: D-04 one-commit-per-rule-family proven across 8 families (185 violations resolved in 8 atomic fix(lint): commits). Each commit is independently revertable, each fix is annotated with the rule code in the commit subject, and bisect can pinpoint exactly which family's fix introduced any regression.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 02]: PT013 ruff 0.15 reversed its preference (now wants 'import pytest' instead of 'from pytest import raises') vs the existing cement convention (cited at tests/core/test_exc.py). Absorbed via per-file-ignore on tests/**/*.py rather than mass-rewriting the convention — mass-rewrite would itself be a D-13 strict-minimum violation. Documented as deviation from RESEARCH.md prediction.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 03]: D-15 coupling pattern repeated — mypy pin (~=1.20.2) + AUDIT POINT comment land in single chore: bump mypy to 1.20 commit. Same shape as Plan 02's chore: bump ruff. Pattern generalized across both ruff and mypy.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 03]: D-11 strict preservation held — ZERO mypy strictness knob value changed; the only [tool.mypy] addition was the 4-line AUDIT POINT comment block. Knob tightening explicitly deferred to Phase 3 REFACTOR-02.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 03]: D-13 strict-minimum on handler.py:394 — chose # type: ignore append over narrowing assertion. Mirrors framework's established sibling pattern at lines 387/389/390/393/395 (all use # type: ignore for the same MetaMixin/Meta union-attr pattern). Phase 3 REFACTOR-02 may revisit.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 03]: Line drift acknowledged — RESEARCH.md cited line 392; Plan 02 lint fixes shifted union-attr site to line 394. Same code, same fix. Plan anticipated this with read-line-numbers-first directive.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 04]: D-15 coupling generalized to floor-only test-tool family — pytest, pytest-cov, coverage all bumped (>=) in single chore: bump pytest+pytest-cov+coverage commit. Pattern now proven across both ~= (ruff/mypy) and >= (pytest-family) pin types.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 04]: D-13 strict-minimum honored absolutely — ZERO test-config or test-code modernization. [tool.pytest.ini_options] untouched. RESEARCH.md prediction (cement test surface bug-clean against pytest 9.0/pytest-cov 7.0/coverage 7.13) verified — no fix(test): commits needed.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 04]: Pitfall 3 (pytest-cov 7.0 subprocess-measurement removal) verified no-op for cement — cement/utils/shell.py 129/0/100% and cement/cli/main.py 28/0/100% pre/post-bump identical. Per-module Miss=0 held across cement/ tree. TOTAL stmt-count drift (3311->3285) is coverage 7.6->7.13 detection-heuristics internal, not a coverage regression.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 04]: Phase 1 implementation COMPLETE — all 5 ROADMAP cumulative success criteria GREEN (PYVER-01/02, TOOL-01/02/03/04). 13 atomic phase-1 commits across 4 plans. CI matrix (3.10/3.11/3.12/3.13/3.14/pypy3.10) is the final verification gate on PR open.
- [Phase ?]: [Phase 01.1 Plan 01]: pdm-backend migration green on full Python 3.10-3.14 matrix; build-time cement dependency removed; setup.py-era files (5) deleted; PEP 735 dev deps via [dependency-groups].
- [Phase ?]: [Phase 01.1 Plan 01]: Rule 1 deviation auto-fixed: tests/cli/test_main.py::test_generate updated to assert pyproject.toml exists (was setup.py). Regression caught in Task 7 acceptance check after Task 4 deletion; mechanical one-line fix preserves end-to-end behavior validation.

### Roadmap Evolution

- Phase 01.1 inserted after Phase 1: Generated Project Template Build Modernization (URGENT) — PEP 517 build isolation fails because the generated `cement generate project` template imports cement at build time via setup.py → version.py. Blocks Phase 2 CI-green goal; smoke test cannot pass on the matrix until template no longer requires cement (or any runtime dep) at build time.

### Pending Todos

None yet.

### Plan-Phase Gate Overrides

- **Phase 2 / 2026-05-02 / decision-coverage gate** — D-16 (negative-space rule: "keep the serial job graph") and D-18 (meta convention governing `docs(02):` plan-artifact commits) are not explicitly cited in any plan's `must_haves`/`truths` block. User chose "Proceed anyway" — both decisions are correctly handled (D-16 by omission, no task touches the job graph; D-18 by the GSD workflow's own `docs(02): create phase plan` commit). Re-surface in `/gsd-verify-work` if the decisions are mis-handled at execution time.

### Blockers/Concerns

- Stalled `pdm update` GitHub Action (the user's pain point): drowning in ruff lint on each run. Phase 1 directly unblocks this.
- 100% coverage gate is absolute and must hold across every phase — no temporary relaxations.
- Public API surface includes subclass-exposed internals (downstream extensions may subclass); refactor must assume unknown third-party subclasses.

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 260430-3b0 | fix scripts/cli-smoke-test.sh — drop py3.9 default and modernize generated-project install path (phase-1 gap closure) | 2026-04-30 | 020ec7b7 | [260430-3b0-fix-scripts-cli-smoke-test-sh-drop-py3-9](./quick/260430-3b0-fix-scripts-cli-smoke-test-sh-drop-py3-9/) |
| 260430-i7q | add cli-smoke-test Makefile target wiring scripts/cli-smoke-test.sh | 2026-04-30 | 786a440e | [260430-i7q-add-cli-smoke-test-target-to-makefile-th](./quick/260430-i7q-add-cli-smoke-test-target-to-makefile-th/) |

## Session Continuity

Last session: 2026-05-02T03:32:57.149Z
Stopped at: Phase 2 context gathered
Resume file: .planning/phases/02-dependencies-ci-pipeline/02-CONTEXT.md
