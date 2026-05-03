---
phase: 02-dependencies-ci-pipeline
plan: 05
subsystem: ci
tags:
  - ci-matrix
  - pypy
  - github-actions
  - phase-2
  - ci-01

requires:
  - phase: 02-dependencies-ci-pipeline
    plan: 01
    provides: refreshed pdm.lock + green make test (316/316, 100%) baseline preserved by this plan
  - phase: 02-dependencies-ci-pipeline
    plan: 03
    provides: pyproject.toml `[tool.coverage.report] fail_under = 100` armed coverage gate (un-touched here)
  - phase: 02-dependencies-ci-pipeline
    plan: 04
    provides: exact-tag pins on actions/setup-python@v6.2.0 + 6 other Action+repo pairs across both workflow files (preserved)
provides:
  - .github/workflows/build_and_test.yml — test-all matrix expanded from 6 → 7 lanes (added pypy3.11 alongside pypy3.10)
  - .github/workflows/build_and_test.yml — `# FIXME ?` comment + commented-out 3-OS line removed (D-15 cleanup)
  - CHANGELOG `[ci]` Misc-bucket entry in `## 3.0.15 - DEVELOPMENT` documenting the pypy3.11 lane addition
  - 2 atomic commits per D-17 #8 + #9 (no folding — each commit is its own concern)
affects:
  - 02-06-PLAN (Dependabot for github-actions ecosystem) — operates on the same workflow file but on Action invocations, not matrix entries; no merge conflict
  - 02-07-PLAN (workflow_dispatch trigger) — modifies pdm.yml `on:` block, not build_and_test.yml; no merge conflict
  - 02-08-PLAN (phase acceptance verification) — verifies all 7 matrix lanes report green on a fresh PR (CI-01 closure gate)

tech-stack:
  added: []
  patterns:
    - "D-14 honored: existing pypy3.10 lane PRESERVED while adding pypy3.11 (no downstream-observable matrix removals on the 3.0.x track)"
    - "RESEARCH.md A5 verified: actions/setup-python@v6.2.0 accepts both `pypy3.X` and `pypy-3.X`; cement convention is no-dash, so we mirrored existing `pypy3.10` style with `pypy3.11`"
    - "D-15 cleanup: dead-code FIXME comment + commented-out 3-OS line removed in dedicated commit (D-17 #9 atomic split)"
    - "D-17 #8 + #9 atomic split honored: 2 distinct commits, NOT folded — pypy lane addition is a user-visible matrix expansion (changelog entry); FIXME-drop is comment cleanup (no changelog entry per CLAUDE.md filter rule)"
    - "78-char subject + body wrap (CLAUDE.md Conventional Commits + line-length policy held on both commits)"

key-files:
  created:
    - .planning/phases/02-dependencies-ci-pipeline/02-05-SUMMARY.md (this file)
  modified:
    - .github/workflows/build_and_test.yml (test-all matrix + FIXME block)
    - CHANGELOG.md (Misc bucket — `[ci]` Add PyPy 3.11)

key-decisions:
  - "D-14 honored — pypy3.10 PRESERVED, pypy3.11 ADDED (not replaced). Matrix grows from 6 → 7 lanes in declared order."
  - "No-dash convention `pypy3.11` chosen to mirror existing `pypy3.10` (RESEARCH.md A5 — both no-dash and dashed forms are interchangeable for actions/setup-python@v6.2.0; cement style is no-dash)."
  - "D-15 honored — FIXME comment + commented-out 3-OS line both removed; OS matrix stays `[ubuntu-latest]` only (cross-platform CI is a dedicated future milestone outside Phase 2 scope per CONTEXT.md <deferred>)."
  - "D-17 #8 + #9 NOT folded — pypy3.11 addition is user-visible (changelog entry); FIXME-drop is cleanup (no changelog entry per CLAUDE.md filter rule). Atomic split keeps bisect surface clean."
  - "CHANGELOG entry only for the pypy3.11 commit — FIXME-drop commit modifies only the workflow file (no CHANGELOG.md edit per RESEARCH.md § \"Changelog Bucketing\" entry #9)."

patterns-established:
  - "Atomic-commit shape: when a plan groups multiple D-17 entries, fold ONLY when they share a concern (Plan 04 D-17 #4+#5 folded since both were exact-tag pinning); split when concerns differ (Plan 05 D-17 #8 lane-add vs #9 comment-drop)."
  - "Changelog-or-not heuristic: user-visible matrix expansion → changelog entry; comment cleanup / dead-code removal → no entry."

requirements-completed:
  - CI-01

duration: ~3min
completed: 2026-05-03
---

# Phase 02 Plan 05: PyPy 3.11 + FIXME Cleanup Summary

**test-all matrix expanded from 6 to 7 Python lanes — pypy3.11 added alongside preserved pypy3.10 (D-14) — and the dead-code `# FIXME ?` OS-matrix comment block removed (D-15); both shipped as 2 atomic D-17-shaped commits with one `[ci]` CHANGELOG entry for the lane addition only.**

## Performance

- **Duration:** ~3 min (Edit + verify + commit cycle ×2; one `make test` run since first edit was YAML-only and second was YAML-only)
- **Started:** 2026-05-03T04:18:00Z (approx — Plan 04 finished 2026-05-02T22:15:00Z; Plan 05 began after Wave 4 dispatch)
- **Completed:** 2026-05-03T04:21:12Z
- **Tasks:** 2 (both `type="auto"`, both committed individually)
- **Files modified:** 2 (`.github/workflows/build_and_test.yml`, `CHANGELOG.md`)
- **Files created:** 1 (`.planning/phases/02-dependencies-ci-pipeline/02-05-SUMMARY.md` — this file)

## Accomplishments

- pypy3.11 added to the test-all matrix as the 7th lane, mirroring the no-dash convention of the existing pypy3.10 (preserved per D-14)
- `# FIXME ?` comment + commented-out 3-OS line both removed cleanly from the test-all matrix block (D-15)
- 2 atomic commits with subjects exactly per D-17 #8 + #9 (`ci: add pypy-3.11 to test matrix` / `ci: drop FIXME OS-matrix comment`), all subject + body lines ≤ 78 chars
- 1 `[ci]` Misc CHANGELOG entry for the pypy3.11 addition; FIXME-drop commit correctly omits CHANGELOG per CLAUDE.md filter rule
- Plan 04's exact-tag pins on `build_and_test.yml` are fully preserved (no regressions to actions/checkout@v6.0.2, ConorMacBride/install-package@v1.1.0, actions/setup-python@v6.2.0, pdm-project/setup-pdm@v4.4, hoverkraft-tech/compose-action@v2.6.0)
- yaml syntactically valid post-both-commits; `make test` exits 0 at 316/316, 100% coverage

## Task Commits

Each task was committed atomically:

1. **Task 1: Add pypy3.11 to test-all matrix and append CHANGELOG entry** — `6ecfbc65` (`ci: add pypy-3.11 to test matrix`)
2. **Task 2: Drop the `# FIXME ?` OS-matrix comment block** — `4b5160a8` (`ci: drop FIXME OS-matrix comment`)

Both commits use `ci:` Conventional Commit type per CLAUDE.md § "Commit Conventions". Subject lines + body lines all ≤ 78 chars verified post-commit.

## Final Matrix State

```yaml
test-all:
  needs: test
  runs-on: ${{ matrix.os }}
  strategy:
    matrix:
      os: [ubuntu-latest]
      python-version: ["3.10", "3.11", "3.12", "3.13", "3.14", "pypy3.10", "pypy3.11"]
```

7 lanes confirmed via `pdm run python -c "import yaml; ..."` round-trip:

```
os: ['ubuntu-latest']
python-version: ['3.10', '3.11', '3.12', '3.13', '3.14', 'pypy3.10', 'pypy3.11']
```

D-14 invariant: **pypy3.10 PRESERVED**, **pypy3.11 ADDED**. No downstream-observable matrix removal.

## Acceptance Criteria — All Satisfied

| Criterion | Result |
| --------- | ------ |
| Matrix has all 7 expected lanes in correct order | PASS |
| `grep -c '"pypy3.10"' .github/workflows/build_and_test.yml` returns 1 (D-14 preservation) | PASS |
| `grep -c '"pypy3.11"' .github/workflows/build_and_test.yml` returns 1 (added) | PASS |
| `grep -c 'FIXME ?'` returns 0 (D-15 cleanup) | PASS |
| `grep -c 'os: \[ubuntu-latest, macos-latest, windows-latest\]'` returns 0 (commented-out 3-OS line removed) | PASS |
| `grep -c 'os: \[ubuntu-latest\]'` returns 1 (active line preserved) | PASS |
| Python yaml round-trip passes assertions on os + python-version | PASS |
| `make test` exits 0 at 316/316, 100% coverage | PASS |
| Task 1 commit subject matches `^ci: add pypy-3\.11 to test matrix$` | PASS |
| Task 2 commit subject matches `^ci: drop FIXME OS-matrix comment$` | PASS |
| Subject + body lines all ≤ 78 chars (both commits) | PASS |
| `[ci]` Add PyPy 3.11 entry in CHANGELOG `## 3.0.15 - DEVELOPMENT` Misc bucket | PASS |
| Task 2 commit does NOT touch CHANGELOG.md (FIXME-drop is cleanup-only) | PASS |
| Plan 04 exact-tag pins preserved (actions/setup-python@v6.2.0 etc.) | PASS |

## Files Created/Modified

- `.github/workflows/build_and_test.yml` — test-all matrix line: added `, "pypy3.11"`; removed `# FIXME ?` + commented-out 3-OS line
- `CHANGELOG.md` — Misc bucket: appended `- \`[ci]\` Add PyPy 3.11 to CI test matrix (alongside existing PyPy 3.10)`
- `.planning/phases/02-dependencies-ci-pipeline/02-05-SUMMARY.md` — this file

## Decisions Made

- **D-14 honored: ADD pypy3.11, KEEP pypy3.10.** Plan was unambiguous, no judgment call.
- **No-dash form `pypy3.11`.** Per RESEARCH.md A5 both forms work with setup-python@v6.2.0; mirrored existing `pypy3.10` style.
- **D-17 #8 + #9 NOT folded.** Two distinct concerns (lane addition vs comment cleanup) → 2 commits. Plan 04 (D-17 #4 + #5) was folded because both shared the exact-tag-pin concern; that does not apply here.
- **No changelog entry for FIXME-drop.** Per RESEARCH.md § "Changelog Bucketing" entry #9 + CLAUDE.md "filter out workflow scaffolding" rule, comment cleanup is not user-visible.

## Deviations from Plan

None — plan executed exactly as written. Both tasks ran cleanly; verification commands all returned expected values on first attempt; no auto-fixes (Rules 1–3) needed; no architectural decisions (Rule 4) surfaced.

## Issues Encountered

- **PyYAML not pre-installed in fresh worktree venv:** First yaml round-trip attempt via `pdm run python -c "import yaml; ..."` failed with `ModuleNotFoundError: No module named 'yaml'` because the worktree's `.venv` was empty (this is the same issue Plan 04 encountered, recorded in user memory as "broken Cement env → `make init` rebuilds devbox + venv before any PDM internals"). Resolved by running `make init` once before the first verification — installed all 58 packages including PyYAML 6.0.3. Subsequent yaml round-trip (and `make test`) ran cleanly. No commits affected; no edits or test failures arose from this.

## Threat Model Disposition

| Threat ID | Disposition | Status After This Plan |
| --------- | ----------- | ---------------------- |
| T-02-05-01 (Tampering / accidentally dropping pypy3.10 while adding pypy3.11) | mitigate | RESOLVED — `grep -c '"pypy3.10"'` returns 1; `grep -c '"pypy3.11"'` returns 1; both lanes present in matrix, in declared order |
| T-02-05-02 (Information disclosure / new pypy3.11 lane fails on a real cement bug) | accept | ACCEPTED — if pypy3.11 surfaces a real regression on the first PR run, that's a learning signal; D-04 atomic-split applies if found post-merge |
| T-02-05-03 (EoP / removing FIXME could hide a future cross-platform need) | accept | ACCEPTED — CONTEXT.md `<deferred>` already records the cross-platform milestone deferral with full rationale; FIXME comment was unactionable cruft |

## CI-01 Closure Note

This plan **adds the pypy3.11 lane** but does not itself **validate it green**. CI-01 acceptance ("all 7 matrix lanes report green on a fresh PR") is **Plan 08's verification task** — it requires a real PR run on GitHub to exercise the new matrix end-to-end. Local `make test` cannot validate `pypy3.X` lanes (those run only in the CI matrix on GitHub-hosted runners with PyPy installed via setup-python).

If pypy3.11 surfaces a real regression on the first Plan-08 PR run, that's a follow-up bug — not a Phase 2 blocker. D-04 atomic-split applies: file as a separate issue, fix in a dedicated commit.

## Self-Check

Verifying claimed work exists:

**Files:**
- `[FOUND]` `.github/workflows/build_and_test.yml` (verified: 7-lane matrix, FIXME removed, OS=ubuntu-latest)
- `[FOUND]` `CHANGELOG.md` (verified: `[ci]` Add PyPy 3.11 entry in `## 3.0.15 - DEVELOPMENT` Misc bucket)
- `[FOUND]` `.planning/phases/02-dependencies-ci-pipeline/02-05-SUMMARY.md` (this file)

**Commits:**
- `[FOUND]` `6ecfbc65` (`ci: add pypy-3.11 to test matrix`) — verified via `git log --oneline -3`
- `[FOUND]` `4b5160a8` (`ci: drop FIXME OS-matrix comment`) — verified via `git log --oneline -3`

**Acceptance criteria:** All PASS as documented in the table above.

## Self-Check: PASSED

## Next Phase Readiness

- **Plan 06 (Dependabot for github-actions + repo-level security-updates toggle):** Operates on `.github/dependabot.yml` (new file) + `.github/workflows/build_and_test.yml` Action invocations — not the matrix block. No merge conflict with Plan 05 changes.
- **Plan 07 (workflow_dispatch trigger on pdm.yml):** Modifies `.github/workflows/pdm.yml` `on:` block. Plan 05 only touched `build_and_test.yml`. No merge conflict.
- **Plan 08 (phase acceptance verification):** Re-runs the D-19 acceptance grep set + verifies all 7 matrix lanes green on a fresh PR. CI-01 closure depends on Plan 08's PR run, not this plan in isolation.

No blockers. Phase 2 wave 4 dispatch (Plans 05/06/07) is unblocked for the remaining waves.

---
*Phase: 02-dependencies-ci-pipeline*
*Plan: 05*
*Completed: 2026-05-03*
