---
phase: 01-tooling-baseline-python-matrix
verified: 2026-04-30T15:00:00Z
status: passed
score: 11/11 must-haves verified
overrides_applied: 0
---

# Phase 01: Tooling Baseline & Python Matrix Verification Report

**Phase Goal:** Bring ruff, mypy, and pytest tooling to current stable, drop Python 3.9, and clear all resulting lint/type errors so the rest of the work has a clean starting line.
**Verified:** 2026-04-30T15:00:00Z
**Status:** passed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths (ROADMAP Success Criteria + Plan Must-Haves)

| #   | Truth                                                                          | Status     | Evidence                                                                                                  |
| --- | ------------------------------------------------------------------------------ | ---------- | --------------------------------------------------------------------------------------------------------- |
| 1   | `make comply-ruff` exits 0 with latest stable ruff (TOOL-01, ROADMAP SC #1)    | VERIFIED   | `make comply` -> "All checks passed!" + ruff 0.15.12 active                                               |
| 2   | `make comply-mypy` exits 0 with latest stable mypy (TOOL-02, ROADMAP SC #2)    | VERIFIED   | `make comply` -> "Success: no issues found in 51 source files" + mypy 1.20.2 active                       |
| 3   | `make test` runs without pytest/pytest-cov/coverage internal deprecation warnings (TOOL-03, ROADMAP SC #3) | VERIFIED   | `pytest tests/core -W "error::pytest.PytestRemovedIn10Warning" -W "error::pytest.PytestDeprecationWarning"` exit 0; 316 passed |
| 4   | `pyproject.toml` declares `requires-python = ">=3.10"` (PYVER-02, ROADMAP SC #4) | VERIFIED   | `pyproject.toml:19` reads `requires-python = ">=3.10"`                                                    |
| 5   | PYVER-03 grep audit returns no compat shims (ROADMAP SC #4)                   | VERIFIED   | Grep returns one historical comment (`cement/utils/fs.py:3 # derks@2024-06-22: remove after 3.9 is EOL?`) — the comment ABOUT the `__future__` import line that D-14 explicitly preserves; deferred to Phase 3 REFACTOR-04 per plan 01-01 SUMMARY |
| 6   | Ruff and mypy rule sets explicitly enumerated (TOOL-04, ROADMAP SC #5)        | VERIFIED   | 4 AUDIT POINT comments in pyproject.toml (`[tool.ruff.lint]`, `ignore`, `per-file-ignores`, `[tool.mypy]`); 11-family extend-select; preview=false |
| 7   | Python 3.9 dropped from CI matrix (PYVER-01)                                  | VERIFIED   | `.github/workflows/build_and_test.yml:68` -> `python-version: ["3.10", "3.11", "3.12", "3.13", "3.14", "pypy3.10"]` (no 3.9) |
| 8   | Python 3.10 floor declared in ruff/mypy (PYVER-02)                            | VERIFIED   | `pyproject.toml:72 target-version = "py310"`; `pyproject.toml:158 python_version = "3.10"`               |
| 9   | 100% test coverage held (Quality gate)                                        | VERIFIED   | `make test` -> 316 passed, TOTAL 3285/0/100.00% coverage on cement/                                       |
| 10  | Tool pins use D-12 hybrid posture (TOOL-04)                                   | VERIFIED   | `ruff~=0.15.12` (~=), `mypy~=1.20.2` (~=), `pytest>=9.0.3`, `pytest-cov>=7.1.0`, `coverage>=7.13.5` (>=)  |
| 11  | Python 3.9 removed from every surface (Makefile, docker-compose, Dockerfiles, README, .travis.yml) | VERIFIED   | Makefile dev target has no `cement-py39`; docker-compose.yml has no `cement-py39:` block; both generate Dockerfiles `FROM python:3.10-alpine`; README "Tested on Python 3.10+" with 0 `cement-py39` refs; `.travis.yml` and `docker/Dockerfile.dev-py39` deleted |

**Score:** 11/11 truths verified

### Required Artifacts

| Artifact                                                       | Expected                                                          | Status      | Details                                                                              |
| -------------------------------------------------------------- | ----------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------------------ |
| `pyproject.toml`                                               | requires-python>=3.10, target-version py310, python_version 3.10  | VERIFIED    | Lines 19, 72, 158 all confirmed                                                      |
| `pyproject.toml` (ruff)                                        | `ruff~=0.15.12`, preview=false, 11-family extend-select, AUDIT POINT | VERIFIED | Lines 85-138, 214: all present                                                       |
| `pyproject.toml` (mypy)                                        | `mypy~=1.20.2`, AUDIT POINT comment, knobs preserved              | VERIFIED    | Lines 157-188, 213: AUDIT POINT comment present, all knobs unchanged from pre-Plan-3 |
| `pyproject.toml` (test tools)                                  | `pytest>=9.0.3`, `pytest-cov>=7.1.0`, `coverage>=7.13.5`          | VERIFIED    | Lines 210-212: all three floor pins                                                  |
| `.github/workflows/build_and_test.yml`                         | matrix `["3.10","3.11","3.12","3.13","3.14","pypy3.10"]`         | VERIFIED    | Line 68 exact match                                                                  |
| `Makefile`                                                     | dev target without `cement-py39`                                  | VERIFIED    | Lines 13-20: `cement-py310..313` only, no py39                                       |
| `docker-compose.yml`                                           | no `cement-py39:` service block                                   | VERIFIED    | `cement-py310..313` services only; no py39                                           |
| `cement/cli/templates/generate/project/Dockerfile`             | `FROM python:3.10-alpine`                                         | VERIFIED    | Line 1 exact match                                                                   |
| `cement/cli/templates/generate/todo-tutorial/Dockerfile`       | `FROM python:3.10-alpine`                                         | VERIFIED    | Line 1 exact match                                                                   |
| `cement/core/handler.py`                                       | union-attr resolved via `# type: ignore`                          | VERIFIED    | Line 394: `if not self.registered(interface, han._meta.label):  # type: ignore`     |
| `docker/Dockerfile.dev-py39`                                   | DELETED                                                           | VERIFIED    | File does not exist                                                                  |
| `.travis.yml`                                                  | DELETED                                                           | VERIFIED    | File does not exist                                                                  |
| `README.md`                                                    | no Python 3.9 references                                          | VERIFIED    | "Tested on Python 3.10+" present; 0 `cement-py39` refs                              |

### Key Link Verification

| From                                                | To                                       | Via                                                  | Status | Details                                                                                                              |
| --------------------------------------------------- | ---------------------------------------- | ---------------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------- |
| `pyproject.toml requires-python`                    | GH Actions matrix python-version          | atomic D-05 commit                                   | WIRED  | Both updated in commit `00d37e16 chore: drop python 3.9 from supported matrix`                                       |
| `Makefile dev target`                               | `docker-compose.yml services`             | cement-py39 removed in lockstep with Dockerfile.dev-py39 deletion | WIRED  | Same atomic commit `00d37e16` removed Makefile line, compose block, and Dockerfile.dev-py39 file                     |
| `pyproject.toml [tool.ruff.lint] extend-select`     | `make comply-ruff`                        | ruff config -> CI gate                                | WIRED  | `make comply-ruff` exits 0 with the 11-family extend-select active; new rule additions on bumps fire as CI failures |
| `pyproject.toml [dependency-groups] dev ruff~=0.15.12` | scheduled `pdm.yml`                    | compatible-release pin protects against rule-set drift | WIRED  | `~=0.15.12` allows 0.15.x but excludes 0.16+ (D-12 compatible-release pin)                                          |
| `pyproject.toml [tool.mypy]`                        | `make comply-mypy`                        | mypy strict knobs codified with audit-point comment   | WIRED  | `make comply-mypy` exits 0; AUDIT POINT comment present                                                              |
| `cement/core/handler.py:394 fix`                    | siblings at lines 387/389/390/393/395    | MetaMixin/Meta `# type: ignore` pattern               | WIRED  | Sibling pattern verified — line 394 trailing `# type: ignore` matches surrounding lines                              |
| `pyproject.toml [dependency-groups] dev`            | `make test`                               | pdm install resolves new floors; pytest 9.x picks up natively | WIRED | `pytest 9.0.3 / pytest-cov 7.1.0 / coverage 7.13.5` active; `make test` exits 0                                  |
| `pytest 9.0 dropping Python 3.9`                    | Phase 1 PYVER-01                          | natural alignment                                     | WIRED  | pytest 9.0 itself dropped 3.9, co-validating Plan 01's floor                                                         |

### Behavioral Spot-Checks

| Behavior                                                  | Command                                                                                          | Result                                                                              | Status |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- | ------ |
| ruff at pinned version                                    | `pdm run ruff --version`                                                                         | `ruff 0.15.12`                                                                      | PASS   |
| mypy at pinned version                                    | `pdm run mypy --version`                                                                         | `mypy 1.20.2 (compiled: yes)`                                                       | PASS   |
| pytest at pinned floor                                    | `pdm run pytest --version`                                                                       | `pytest 9.0.3`                                                                      | PASS   |
| pytest-cov at pinned floor                                | `python -c "import pytest_cov; print(pytest_cov.__version__)"`                                  | `7.1.0`                                                                             | PASS   |
| coverage at pinned floor                                  | `python -c "import coverage; print(coverage.__version__)"`                                       | `7.13.5`                                                                            | PASS   |
| Full compliance (ruff + mypy)                             | `make comply`                                                                                    | `All checks passed!` + `Success: no issues found in 51 source files`                | PASS   |
| Full test suite + coverage gate                           | `make test`                                                                                      | 316 passed, 100.00% coverage on cement/, 1692 warnings (all cement's own DeprecationWarnings) | PASS   |
| No pytest-internal deprecations                           | `pytest tests/core -W error::pytest.PytestRemovedIn10Warning -W error::pytest.PytestDeprecationWarning` | exit 0, 316 passed                                                                  | PASS   |
| PYVER-03 grep audit                                       | `grep -rn "3\.9\|sys\.version_info.*9\|py39\|python:3\.9" cement/ tests/ pyproject.toml .github/ Makefile docker-compose.yml docker/` (filtered) | 1 hit: `cement/utils/fs.py:3 # derks@2024-06-22: remove after 3.9 is EOL?` (a comment ABOUT the preserved `__future__` line, deferred to Phase 3 REFACTOR-04 per plan 01-01 SUMMARY) | PASS   |
| AUDIT POINT count                                         | `grep -c "AUDIT POINT" pyproject.toml`                                                          | 4                                                                                   | PASS   |

### Requirements Coverage

| Requirement | Source Plan | Description                                                                                              | Status     | Evidence                                                                                                |
| ----------- | ----------- | -------------------------------------------------------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------- |
| TOOL-01     | 01-02       | Latest stable ruff adopted; `make comply-ruff` exits clean                                               | SATISFIED  | ruff 0.15.12 active, `make comply-ruff` exits 0                                                        |
| TOOL-02     | 01-03       | Latest stable mypy adopted; `make comply-mypy` exits clean                                               | SATISFIED  | mypy 1.20.2 active, `make comply-mypy` exits 0                                                          |
| TOOL-03     | 01-04       | pytest, pytest-cov, coverage upgraded; `make test` runs without their own deprecation warnings           | SATISFIED  | pytest 9.0.3 / pytest-cov 7.1.0 / coverage 7.13.5; pytest filter test exit 0                            |
| TOOL-04     | 01-02, 01-03 | ruff + mypy rule configuration codified; no implicit drift                                                 | SATISFIED  | 4 AUDIT POINT comments; `~=` pins on ruff/mypy; preview=false; explicit knob enumeration in [tool.mypy] |
| PYVER-01    | 01-01       | Python 3.9 removed from pyproject.toml `python-requires` and CI matrix                                   | SATISFIED  | `requires-python = ">=3.10"`; CI matrix has no 3.9 entry                                                |
| PYVER-02    | 01-01       | Python 3.10 declared as minimum supported across pyproject, docs, README, CI                             | SATISFIED  | pyproject `>=3.10`; README "Tested on Python 3.10+"; CI matrix `["3.10",..."pypy3.10"]`                  |
| PYVER-03    | 01-01       | No 3.9-only compat shims in source (verified by grep + linter pass)                                      | SATISFIED  | PYVER-03 grep audit returns only the deferred D-14 comment + `__future__` annotation (filtered by design); YTT203 stale shim resolved in 01-02 |

All 7 requirement IDs declared in PLAN frontmatters map to REQUIREMENTS.md and are satisfied. No orphaned requirements (REQUIREMENTS.md maps exactly TOOL-01..04 + PYVER-01..03 to Phase 1, all accounted for).

### Anti-Patterns Found

No blocking anti-patterns. All anti-pattern grep results are documented in plan SUMMARYs as intentional and audited:

| File                                | Line | Pattern                              | Severity | Impact                                                                                                                                                                       |
| ----------------------------------- | ---- | ------------------------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cement/utils/fs.py`                | 3    | Comment "remove after 3.9 is EOL?"  | Info     | Self-flagged TODO comment associated with `from __future__ import annotations` line. Per D-14 + plan 01-01 SUMMARY, deferred to Phase 3 REFACTOR-04. Not a Phase 1 blocker. |
| `cement/cli/main.py`, `ext_dummy.py`, etc. | various | `# noqa: T201` / `# noqa: F401` etc. | Info     | All audited per plan 01-02 SUMMARY: each noqa carries one-line rationale; framework-intentional patterns (CLI output, public-API names, etc.).                              |
| `pyproject.toml`                    | various | `ignore = [A001, A002, C901]`        | Info     | Audited per plan 01-02 SUMMARY: each ignore entry carries one-line justification. C901 explicitly cross-references Phase 3 REFACTOR-01/02 for re-evaluation.                |

### Human Verification Required

None. All Phase 1 success criteria are programmatically verifiable and have been verified above.

The only outstanding non-local verification is **CI matrix validation on push** — `gh pr checks <PR>` against Python 3.10/3.11/3.12/3.13/3.14/pypy3.10. Local exec ran on the dev container's default Python only. Per plan 01-04 SUMMARY this is the formal end-of-Phase-1 gate when the PR opens. This is a CI-job verification, not a human-judgment verification, and is captured under Phase 2 / CI-01 in REQUIREMENTS.md (Phase 2 success criterion #1: "A fresh PR triggers GitHub Actions and all matrix jobs report green").

### Gaps Summary

No gaps. All 11 must-have truths verified, all artifacts present and substantive, all key links wired, all 7 requirements satisfied, no blocking anti-patterns. Tool versions confirmed live (ruff 0.15.12, mypy 1.20.2, pytest 9.0.3, pytest-cov 7.1.0, coverage 7.13.5). Quality gates green (`make comply` + `make test` both exit 0, 316 tests pass, 100.00% coverage on cement/, no pytest-internal deprecation warnings under `-W error` filters).

The 17 atomic conventional commits land in the plan-prescribed order:
- `00d37e16 chore: drop python 3.9 from supported matrix` (Plan 01)
- `7938c98e chore: bump ruff to 0.15` (Plan 02 pin+codification per D-15)
- `0e56adee` through `a663d84e` — 8 `fix(lint):` family-scoped commits (D-04)
- `3966a8fd chore: bump mypy to 1.20` (Plan 03 pin+codification per D-15)
- `8d392dd2 fix(types): resolve union-attr in core/handler.py` (D-04)
- `3ff270f3 chore: bump pytest+pytest-cov+coverage` (Plan 04 D-15 floor coupling)
- Plus 4 `docs(NN-NN):` plan SUMMARY commits

Phase 1 implementation is complete and all ROADMAP success criteria are met.

---

_Verified: 2026-04-30T15:00:00Z_
_Verifier: Claude (gsd-verifier)_
