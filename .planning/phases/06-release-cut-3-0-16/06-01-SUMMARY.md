---
phase: 06-release-cut-3-0-16
plan: 01
subsystem: infra
tags: [release, provisioning, github-actions, docker-hub, pypi, oidc, rtd, git-ancestry]

# Dependency graph
requires:
  - phase: 05.4-github-actions-release-workflow
    provides: release.yml/gates.yml pipeline, 05.4-PROVISIONING.md runbook with exact match values
provides:
  - Docker Hub repo secrets DOCKERHUB_USERNAME + DOCKERHUB_TOKEN (org OAT path, D-11)
  - PyPI trusted publisher confirmed (repo datafolklabs/cement, workflow release.yml, env release)
  - RTD GitHub integration confirmed connected, no per-patch activation rule
  - stable/3.0.x ancestry recorded on main via real -s ours merge 8978b395 (branch-sync FF precondition)
  - Pre-first-tag checklist in 05.4-PROVISIONING.md checked off with live evidence
affects: [06-02 release-prep, 06-03 dry-run, 06-04 tag-and-live-run, 06-05 post-release]

# Tech tracking
tech-stack:
  added: []
  patterns: [guided D-09 provider-UI checkpoint session with per-item gh-api evidence verification]

key-files:
  created:
    - .planning/phases/06-release-cut-3-0-16/06-01-provisioning-inventory.md
  modified:
    - .planning/phases/05.4-github-actions-release-workflow/05.4-PROVISIONING.md

key-decisions:
  - "Docker Hub credentials minted via org OAT (D-11 preferred path); DOCKERHUB_USERNAME=datafolklabs"
  - "Secrets must live at REPOSITORY scope — release-environment scope rejected because the docker job declares no environment and would see empty credentials"
  - "Ancestry recorded via user-run -s ours merge directly on main (D-10), not a PR — second parent preserved (Pitfall 1)"

patterns-established:
  - "Evidence-gated checkbox discipline: no runbook box checked without gh api / git output or explicit user confirmation for provider-UI-only items"

requirements-completed: [REL-03, REL-04]

coverage:
  - id: D1
    description: "Docker Hub secrets DOCKERHUB_USERNAME + DOCKERHUB_TOKEN set as repository secrets"
    requirement: REL-04
    verification:
      - kind: other
        ref: "gh api repos/datafolklabs/cement/actions/secrets — both names listed, total 2"
        status: pass
    human_judgment: false
  - id: D2
    description: "stable/3.0.x is an ancestor of main via a real -s ours merge commit (branch-sync FF precondition)"
    requirement: REL-03
    verification:
      - kind: other
        ref: "git merge-base --is-ancestor origin/stable/3.0.x origin/main → FF-OK; merge 8978b395 parents c4dc2df2 + 0679bf51; diff across merge empty"
        status: pass
    human_judgment: false
  - id: D3
    description: "PyPI trusted publisher (datafolklabs/cement / release.yml / env release) and RTD GitHub integration (no per-patch rule) confirmed"
    requirement: REL-04
    verification: []
    human_judgment: true
    rationale: "Provider-UI state on PyPI and Read the Docs is unreadable from the repo; user confirmed both in the D-09 guided session"

# Metrics
duration: ~35min (across 3 checkpoint continuations)
completed: 2026-07-13
status: complete
---

# Phase 06 Plan 01: Pre-First-Tag Provisioning Summary

**Both hard release blockers closed — Docker Hub repo secrets set via org OAT and stable/3.0.x ancestry recorded on main via merge 8978b395 — with PyPI trusted publisher and RTD integration user-confirmed, leaving only Plan-02 items (CHANGELOG/VERSION) open on the pre-first-tag checklist.**

## Performance

- **Duration:** ~35 min wall-clock across the guided session (3 checkpoint round-trips)
- **Completed:** 2026-07-13
- **Tasks:** 3/3 (1 auto + 2 blocking human-verify checkpoints)
- **Files modified:** 2

## Accomplishments

- Re-inventoried all 12 provisioning items live (`gh api`/`git`) — state matched the 2026-07-12 research; produced the 12-row GREEN/OPEN/UNVERIFIABLE table in `06-01-provisioning-inventory.md`
- Closed blocker #7: `DOCKERHUB_USERNAME` + `DOCKERHUB_TOKEN` now exist as repository secrets (org OAT path per D-11), verified via `gh api repos/datafolklabs/cement/actions/secrets`
- Closed blocker #8: user ran the one-time `-s ours` ancestry merge directly on main (D-10); verified FF-OK, two parents (`c4dc2df2` + `0679bf51`), zero content drift at merge `8978b395`
- Recorded user confirmations for the two provider-UI-only items: PyPI trusted publisher (exact match values) and RTD GitHub integration (no per-patch activation rule)
- Checked off 11 of 15 pre-first-tag checklist boxes in `05.4-PROVISIONING.md` with dated live evidence

## Task Commits

Each task was committed atomically on `gsd/phase-6-release-cut-3-0-16`:

1. **Task 1: Re-verify live provisioning state** - `e2421f2f` (docs)
2. **Task 2: Guided provider-UI provisioning session** - `d6be41e7` (docs)
3. **Task 3: stable/3.0.x ancestry merge verification** - `dee1fa5a` (docs)

Additionally on `main` (user-run, sanctioned by D-10): `8978b395` `chore: record stable/3.0.x ancestry for release fast-forward`.

## Files Created/Modified

- `.planning/phases/06-release-cut-3-0-16/06-01-provisioning-inventory.md` - Task 1 verbatim check output + 12-row state table
- `.planning/phases/05.4-github-actions-release-workflow/05.4-PROVISIONING.md` - Pre-first-tag checklist boxes checked with live evidence annotations

## Decisions Made

- **Repository-scope secrets, not environment-scope:** the user's first placement put both Docker secrets on the `release` environment; verification caught that the `docker` job declares no `environment:` and would resolve empty credentials. User re-added at repository scope; env copies may remain as harmless shadows.
- **Org OAT chosen** for Docker Hub (D-11 preferred path) — `DOCKERHUB_USERNAME=datafolklabs`.

## Deviations from Plan

### Checkpoint-caught issues (not auto-fixes — human-verify gate worked as designed)

**1. Docker secrets initially placed at the wrong scope**
- **Found during:** Task 2 verification (first "provisioned" signal)
- **Issue:** Secrets landed as `release`-environment secrets; the `docker` job (release.yml L212) declares no environment, so it would see empty credentials at runtime
- **Fix:** Reported back with exact fix steps; user re-added both as repository secrets; re-verified via `gh api` (total: 2)
- **Committed in:** `d6be41e7` (evidence recorded in commit body)

**2. Working copy left on `main` after the user's ancestry merge**
- **Found during:** Task 3 verification
- **Issue:** The user ran the merge sequence in this working copy and remained on `main`, making the runbook appear unchecked (main predates the phase-branch commits)
- **Fix:** Verified local `main` == pushed `origin/main` and clean, switched back to `gsd/phase-6-release-cut-3-0-16`; no work lost
- **Committed in:** n/a (no repo change needed)

## Known Stubs

None.

## Remaining open checklist items (expected, out of this plan's scope)

- Pre-tag ancestry check against the actual release commit (Plan 04, at tag handoff)
- `testpypi` environment deployment-branch restriction (optional hardening)
- CHANGELOG finalization + `backend.py` VERSION bump (Plan 02 release-prep PR)
- Tag ruleset force-update behavior: verify-on-run during the live release (Pitfall 4)

## Self-Check: PASSED

- `06-01-provisioning-inventory.md` exists: FOUND
- `05.4-PROVISIONING.md` ancestry + secrets boxes checked: FOUND
- Commits `e2421f2f`, `d6be41e7`, `dee1fa5a` on phase branch: FOUND
- Merge `8978b395` on `origin/main` with two parents: FOUND
