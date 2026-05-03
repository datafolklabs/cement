---
phase: 02-dependencies-ci-pipeline
plan: 03
subsystem: infra
tags:
  - coverage-gate
  - fail-under
  - tool-coverage
  - pytest-cov
  - phase-2
  - ci-03

requires:
  - phase: 01-tooling-baseline-python-matrix
    plan: 04
    provides: Phase 1 closed at 100.00% coverage on cement/ — the green baseline this plan wraps without backfill
  - phase: 02-dependencies-ci-pipeline
    plan: 01
    provides: refreshed pdm.lock with pytest-cov 7.1.0 + coverage 7.13.5 — the toolchain that honors `[tool.coverage.report].fail_under` (RESEARCH.md verified)
provides:
  - pyproject.toml `[tool.coverage.report] fail_under = 100` (D-10) — single source of truth coverage gate
  - pyproject.toml pytest `addopts` includes `--cov-fail-under=100` (D-11) — belt-and-braces explicit flag survives any future pytest-cov pyproject discovery semantics change
  - pyproject.toml explicit `[tool.coverage.run]` block (D-12) with `source = ["cement"]` and `omit = ["cement/cli/templates/*", "cement/cli/contrib/*"]` — explicit measurement boundary mirroring ruff `exclude` discipline
  - AUDIT POINT comments on both `[tool.coverage.run]` and `[tool.coverage.report]` (Phase 1 D-08 inheritance) — re-review triggers documented in-place
  - cli-smoke-test job in `.github/workflows/build_and_test.yml` UNCHANGED (D-13 — smoke test stays black-box install/run, no `--cov` added)
  - D-19 acceptance #2 evidence — captured FAIL snippet from local gate-fires demonstration (embedded below)
  - CHANGELOG `[dev]` entry in `## 3.0.15 - DEVELOPMENT` Misc bucket
affects:
  - 02-04-PLAN (CI workflow inherits the now-armed gate via `make test` invocation)
  - 02-08-PLAN (Phase 2 acceptance verification re-confirms the gate fires below 100%)
  - Phase 3 REFACTOR plans (any future code change must keep coverage at 100% — gate is now CI-blocking)

tech-stack:
  added: []
  patterns:
    - explicit measurement boundary via `[tool.coverage.run]` source+omit (mirrors ruff `[tool.ruff].exclude` precedent)
    - belt-and-braces gate (pyproject `fail_under` + pytest CLI `--cov-fail-under=100`) — defense-in-depth against pytest-cov pyproject discovery churn
    - AUDIT POINT comment idiom inherited from Phase 1 D-08 — re-review triggers named in-source

key-files:
  created: []
  modified:
    - pyproject.toml
    - CHANGELOG.md

decisions:
  - D-10 wired as `fail_under = 100` in `[tool.coverage.report]` (single source of truth)
  - D-11 wired as `--cov-fail-under=100` in pytest `addopts` (belt-and-braces explicit flag)
  - D-12 wired as explicit `[tool.coverage.run]` block with `source = ["cement"]` + `omit = ["cement/cli/templates/*", "cement/cli/contrib/*"]`
  - D-13 invariant honored — cli-smoke-test job UNCHANGED; no `--cov` added (smoke test stays black-box)
  - D-17 #10 commit shape — combined D-10/D-11/D-12 as one logical change (`test: enforce 100% coverage gate via fail_under + addopts`)
  - D-19 acceptance #2 evidence captured locally via comment-out demo on `cement/utils/version.py:get_version_banner()` (NOT a throwaway PR — RESEARCH.md Pitfall 5 honored)
  - Pitfall 1 / Open Question 2 acknowledgment — `make test-core` will now fail under the gate (it scopes coverage to `cement.core` only, ~30% of cement/); accepted as Phase-2 side-effect; CI uses `make test`, not `make test-core`; flag for Plan 08 verification artifact

metrics:
  tasks_completed: 2
  tasks_total: 2
  files_created: 0
  files_modified: 2
  duration_minutes: ~15
  completed_at: 2026-05-03T02:13:00Z
---

# Phase 02 Plan 03: Wire 100% Coverage Gate Summary

100% coverage gate now armed via `[tool.coverage.report] fail_under = 100` + `--cov-fail-under=100` pytest addopts + explicit `[tool.coverage.run] source/omit` in pyproject.toml; Phase-1 baseline (100.00%) holds; gate-fires demo captured (D-19 #2); cli-smoke-test job unchanged (D-13).

## Outcome

CI-03 closed. The absolute 100% coverage gate that PROJECT.md and ROADMAP both treat as non-negotiable is now wired through both the pyproject discovery path AND an explicit pytest CLI flag (defense in depth). Any drift below 100% coverage causes `make test` to exit non-zero locally AND any PR's CI to turn red.

## Verbatim Diff Summary — pyproject.toml

### `[tool.pytest.ini_options].addopts` (D-11)

Before:
```toml
addopts = "-v --cov-report=term --cov-report=html:coverage-report --capture=sys tests/"
```

After:
```toml
addopts = "-v --cov-report=term --cov-report=html:coverage-report --cov-fail-under=100 --capture=sys tests/"
```

(Inserts `--cov-fail-under=100` between `--cov-report=html:coverage-report` and `--capture=sys`. No other formatting changes.)

### New `[tool.coverage.run]` block (D-12) + Updated `[tool.coverage.report]` (D-10)

Before:
```toml
[tool.coverage.report]
precision = 2
```

After:
```toml
[tool.coverage.run]
# AUDIT POINT (Phase 2 D-12): explicit measurement boundary mirrors
# ruff `exclude` discipline. Re-review if files are added under
# cement/cli/templates/ or cement/cli/contrib/ that should be
# measured.
source = ["cement"]
omit = [
    "cement/cli/templates/*",
    "cement/cli/contrib/*",
]

[tool.coverage.report]
# AUDIT POINT (Phase 2 D-10/D-11): fail_under = 100 is the absolute
# coverage gate. Belt-and-braces: pytest addopts also passes
# --cov-fail-under=100 in case future pytest-cov bumps change
# pyproject discovery semantics.
precision = 2
fail_under = 100
```

All comment lines <= 78 chars (CLAUDE.md compliant).

## Post-Change `make test` Result (no false-positive)

`make test` exits **0** at 100.00% coverage post-change:

```
cement/utils/version.py                 34      0  100.00%
----------------------------------------------------------
TOTAL                                 3285      0  100.00%
Coverage HTML written to dir coverage-report
Required test coverage of 100% reached. Total coverage: 100.00%
===================== 316 passed, 1692 warnings in 52.65s ======================
```

Exit code: 0. Confirms the wired gate does NOT false-positive against Phase 1's inherited 100% baseline. The D-12 omit globs (`cement/cli/templates/*`, `cement/cli/contrib/*`) anchor correctly — `cement/cli/contrib/` does not exist in the repo today (forward-looking insulation per CONTEXT.md).

## D-19 Acceptance #2 Evidence — Gate-Fires Demonstration

Per RESEARCH.md Pitfall 5, the demonstration was captured LOCALLY (NOT a throwaway PR):

1. Introduced one unreachable line inside `cement/utils/version.py:get_version_banner()`.
2. Ran `make test`.
3. Captured the FAIL output below.
4. Restored the file to baseline (verified before this commit; `git status` clean).

Captured FAIL snippet (user-approved):

```
cement/utils/version.py                 36      1  97.22%
TOTAL                                 3287      1  99.97%
FAIL Required test coverage of 100% not reached. Total coverage: 99.97%
make: *** [Makefile:29: test] Error 1
```

Exit code: **2** (coverage.py `fail-under` exit code — non-zero gate fired as designed).

Outcome:
- `Required test coverage of 100% not reached` line clearly emitted
- coverage.py exit status 2 propagated through `make test`
- Demo file restored to baseline before commit (working tree clean post-restore)

User explicitly approved this captured evidence as satisfying D-19 acceptance #2 — checkpoint resolved without re-running the demo in this fresh worktree.

## D-13 Invariant — cli-smoke-test Unchanged

`.github/workflows/build_and_test.yml` cli-smoke-test job verified UNCHANGED:

```yaml
  cli-smoke-test:
    needs: test-all
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hoverkraft-tech/compose-action@v2.0.1
        with:
          compose-file: "./docker-compose.yml"
      - name: CLI Smoke Tests
        run: ./scripts/cli-smoke-test.sh
      - if: always()
        name: Review Output
        run: cat ./tmp/cli-smoke-test.out
```

Verification: `grep -A 8 'cli-smoke-test:' .github/workflows/build_and_test.yml | grep -F -- '--cov'` → 0 matches. cli-smoke-test stays black-box install/run by design.

## Acceptance Criteria — All Satisfied

| Criterion | Result |
| --------- | ------ |
| `grep -c -- '--cov-fail-under=100' pyproject.toml` returns 1 (D-11) | PASS |
| `grep -cE '^fail_under = 100$' pyproject.toml` returns 1 (D-10) | PASS |
| `grep -cE '^\[tool\.coverage\.run\]$' pyproject.toml` returns 1 (D-12) | PASS |
| `grep -cE '^\[tool\.coverage\.report\]$' pyproject.toml` returns 1 (kept) | PASS |
| `grep -cF 'source = ["cement"]' pyproject.toml` returns 1 (D-12) | PASS |
| `grep -cF '"cement/cli/templates/*"' pyproject.toml` returns 1 (D-12) | PASS |
| `grep -cF '"cement/cli/contrib/*"' pyproject.toml` returns 1 (D-12) | PASS |
| `grep -cF 'AUDIT POINT (Phase 2 D-12)' pyproject.toml` returns 1 | PASS |
| `grep -cF 'AUDIT POINT (Phase 2 D-10/D-11)' pyproject.toml` returns 1 | PASS |
| `make test` exits 0 at 100% baseline | PASS |
| cli-smoke-test job has no `--cov` (D-13) | PASS |
| Commit subject matches `^test: enforce 100% coverage gate via fail_under \+ addopts$` | PASS |
| Subject + body lines all <= 78 chars | PASS |
| CHANGELOG `[dev]` entry in active `## 3.0.15 - DEVELOPMENT` Misc bucket | PASS |
| AUDIT POINT comment lines <= 78 chars | PASS |
| Gate-fires demonstration captured (D-19 #2) | PASS (user-approved snippet) |

## Commits

| Task | Description | Hash | Files |
| ---- | ----------- | ---- | ----- |
| 1 | `test: enforce 100% coverage gate via fail_under + addopts` | `875fe621` | pyproject.toml, CHANGELOG.md |
| 2 | checkpoint:human-verify — D-19 #2 evidence captured (no commit; demo is local-only per RESEARCH.md Pitfall 5) | n/a | n/a |

## Side-Effects / Pitfalls Acknowledged

- **`make test-core` now fails under the gate** (RESEARCH.md Pitfall 1 + Open Question 2). `make test-core` scopes coverage to `cement.core` (~30% of `cement/`); under `fail_under = 100` it will report ~30% and fail. Accepted as Phase-2 side-effect — CI uses `make test`, not `make test-core`. Flag for Plan 08 verification artifact and possible CHANGELOG note if a developer reports it during the milestone.
- The D-12 omit pattern includes `cement/cli/contrib/*` even though that directory does not exist today — forward-looking insulation per CONTEXT.md and Phase 1 D-08 audit-point precedent. The AUDIT POINT comment names this exact failure mode (T-02-03-02 in the threat register) and instructs reviewers to re-evaluate when files land under those globs.

## Continuation Notes

- This SUMMARY was authored by a CONTINUATION executor. The previous executor (in worktree `worktree-agent-a709288a03803735b`) reached the human-verify checkpoint after wiring Task 1 (commits `71372fc7`, `f02773d1` in that worktree); the user approved the captured demo evidence; the previous worktree was removed before merge. This continuation worktree re-executed Task 1 in a fresh branch (commit `875fe621`) and embedded the user-approved FAIL snippet in this SUMMARY.
- Per the orchestrator's instructions: STATE.md and ROADMAP.md were NOT modified by this executor. The orchestrator owns those updates after merge.

## Self-Check: PASSED

- pyproject.toml — verified contains `--cov-fail-under=100`, `fail_under = 100`, `[tool.coverage.run]`, `source = ["cement"]`, both omit globs, both AUDIT POINT comments
- CHANGELOG.md — verified `[dev]` Wire 100% coverage gate entry present in `## 3.0.15 - DEVELOPMENT` Misc bucket
- Commit `875fe621` — verified present in `git log` on this branch
- `make test` — exits 0 at 100.00% coverage post-change
- cli-smoke-test invocation in `.github/workflows/build_and_test.yml` — verified UNCHANGED (no `--cov`)
- D-19 #2 captured snippet — embedded above (user-approved)
