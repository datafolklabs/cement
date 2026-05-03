---
phase: 02-dependencies-ci-pipeline
plan: 07
subsystem: ci
tags:
  - workflow-dispatch
  - pdm-update-job
  - phase-2
requirements:
  - DEPS-04
dependency_graph:
  requires:
    - 02-01
    - 02-03
    - 02-04
    - 02-05
    - 02-06
  provides:
    - "manual workflow_dispatch trigger affordance for `.github/workflows/pdm.yml` (Plan 08 fires it post-merge)"
  affects:
    - .github/workflows/pdm.yml
    - CHANGELOG.md
tech_stack:
  added: []
  patterns:
    - "workflow_dispatch trigger added as a sibling key of the existing `schedule:` cron under `on:` (no `inputs:` block per RESEARCH.md — action runs without parameters)"
key_files:
  created: []
  modified:
    - .github/workflows/pdm.yml
    - CHANGELOG.md
decisions:
  - "Add workflow_dispatch with NO inputs (D-08) — pdm-project/update-deps-action does not accept runtime parameters; an empty `workflow_dispatch:` block is sufficient and avoids creating a parameter contract surface"
  - "Fold the CHANGELOG `[ci]` entry into the same atomic `ci: add workflow_dispatch trigger to pdm.yml` commit (per D-17 #7 and CLAUDE.md changelog-as-you-go practice) instead of a follow-up `docs:` commit — keeps the changelog and the user-visible change in lock-step"
  - "Defer DEPS-04 acceptance verification to Plan 08 — this plan only adds the trigger affordance; the actual gh workflow run + outcome capture happens post-merge in Plan 08 against the merged main branch"
metrics:
  duration: ~2 min (plus ~1 min `make init` venv bootstrap + ~52 s `make test`)
  completed: 2026-05-02
---

# Phase 02 Plan 07: workflow_dispatch trigger Summary

Added a manual `workflow_dispatch:` trigger to `.github/workflows/pdm.yml` as a sibling of the existing Monday cron — turns the deps-update workflow into a permanent on-demand affordance so Plan 08 (and any future user) can fire it without waiting on the cron.

## Diff

`.github/workflows/pdm.yml` — exactly +1 line, 0 deletions:

```diff
 on:
   schedule:
     - cron: "5 3 * * 1"
+  workflow_dispatch:
```

`CHANGELOG.md` — exactly +1 line in the `## 3.0.15 - DEVELOPMENT` Misc bucket:

```diff
 - `[ci]` Enable Dependabot for github-actions ecosystem (weekly)
+- `[ci]` Add workflow_dispatch trigger to pdm.yml
```

## Plan 04 Exact-Tag Pins Preserved

| Action | Pin | Status |
|---|---|---|
| `actions/checkout` | `v6.0.2` | preserved (unchanged by this plan) |
| `pdm-project/update-deps-action` | `v1.12` | preserved (unchanged by this plan) |

Floating-ref grep (`@v\d+$|@main|@master`) returns 0 matches — Plan 04's invariant held.

## Verification Evidence

| Check | Command | Expected | Got |
|---|---|---|---|
| trigger added | `grep -cE '^\s*workflow_dispatch:' .github/workflows/pdm.yml` | 1 | 1 |
| cron preserved | `grep -cF 'cron: "5 3 * * 1"' .github/workflows/pdm.yml` | 1 | 1 |
| checkout pin | `grep -cF 'actions/checkout@v6.0.2' .github/workflows/pdm.yml` | 1 | 1 |
| update-deps pin | `grep -cF 'pdm-project/update-deps-action@v1.12' .github/workflows/pdm.yml` | 1 | 1 |
| floating refs | `grep -cE '@v[0-9]+$\|@main\|@master' .github/workflows/pdm.yml` | 0 | 0 |
| CHANGELOG entry | `grep -cF '\`[ci]\` Add workflow_dispatch trigger to pdm.yml' CHANGELOG.md` | 1 | 1 |
| pdm.yml diff | `git diff HEAD~1 -- .github/workflows/pdm.yml \| grep -E '^[+-]' \| grep -vE '^[+-]{3}' \| wc -l` | 1 | 1 |
| `make test` | exit 0 | green | 316 passed, 100% coverage, 0 lint, 0 mypy |

YAML round-trip via PyYAML confirmed `on:` block has both `schedule` and `workflow_dispatch` keys; `workflow_dispatch` value is `None` (no inputs) — exactly the shape D-08 requires.

## Commit Summary

| Subject | Hash | Files |
|---|---|---|
| `ci: add workflow_dispatch trigger to pdm.yml` | `a3078b84` | `.github/workflows/pdm.yml`, `CHANGELOG.md` |

Subject length: 44 chars (≤ 78). All body lines ≤ 78. CHANGELOG entry folded into the same atomic commit per D-17 #7.

## DEPS-04 Closure Hand-off (Plan 08)

This plan **does not** close DEPS-04 — it only adds the trigger affordance. Plan 08 closes the loop post-merge by:

1. After phase-02 merges to `main`, fire the workflow:

   ```bash
   gh workflow run pdm.yml -R datafolklabs/cement
   gh run watch -R datafolklabs/cement
   ```

   If `gh` CLI is unavailable locally (per RESEARCH.md "Environment Availability" — `gh` is not installed in the user's box), use the GitHub Actions UI fallback: **Actions tab → "Update dependencies" workflow → "Run workflow" button → select `main` → Run**.

2. Verify the run completes WITHOUT the wall-of-lint failure mode that the cron previously hit (D-19 acceptance #3).

3. Per D-09, **two outcomes are both passing**:
   - The workflow opens a PR with proposed updates → cron path is healthy and produces actionable output
   - The workflow opens NO PR (because `pdm update` is a no-op against Plan 01's bumped baseline) → cron path is healthy AND the new lockfile is current

   Either outcome closes DEPS-04. The failure mode being avoided is the historic one where the action errored out mid-run with a wall of lint output.

## Deviations from Plan

None — plan executed exactly as written. Pre-flight idempotency check (`workflow_dispatch:` not yet present) and Plan 04 pin baseline check both passed before edit. Edit was the exact `Edit`-tool replacement specified in the plan's `<action>` block. Diff is exactly the +1 line predicted (0 unintended modifications elsewhere in pdm.yml). `make test` required a worktree-local `make init` bootstrap to materialize the per-worktree venv (per the documented recovery path in user memory) — this is environment setup, not a plan deviation; tests then ran clean (316 passed, 100% coverage, 0 lint, 0 mypy errors).

## Threat Flags

None — this plan only adds an `on:` trigger key to an existing CI workflow. No new network endpoints, auth paths, file access patterns, or schema changes at trust boundaries beyond what the plan's `<threat_model>` already documents (T-02-07-01..03, all `accept` disposition).

## Self-Check: PASSED

- FOUND: `.github/workflows/pdm.yml` (modified)
- FOUND: `CHANGELOG.md` (modified)
- FOUND: commit `a3078b84` (`git log --oneline | grep a3078b84` → present)
- FOUND: this `02-07-SUMMARY.md`
