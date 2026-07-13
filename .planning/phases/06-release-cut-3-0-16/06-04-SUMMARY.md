---
phase: 06-release-cut-3-0-16
plan: 04
subsystem: release
tags: [github-actions, pypi, oidc, docker, git-tags, gh-release]

# Dependency graph
requires:
  - phase: 06-release-cut-3-0-16 (plan 01)
    provides: release provisioning (Docker Hub OAT, release environment reviewer gate, stable/3.0.x ancestry merge 8978b395)
  - phase: 06-release-cut-3-0-16 (plan 02)
    provides: finalized 3.0.16 changelog + VERSION on main (squash-merge 1173c469)
  - phase: 06-release-cut-3-0-16 (plan 03)
    provides: green dry-run baseline 29262360749; 3.0.16 bytes frozen on TestPyPI
  - phase: 05.4-github-actions-release-workflow
    provides: release.yml pipeline (gates, TestPyPI smoke, approval-gated publish fan-out)
provides:
  - The 3.0.16 git tag on 1173c469e544a05e244e798b5231e5d3f118a77f (pushed by the USER, D-07)
  - Live PyPI publish of cement 3.0.16 (OIDC trusted publisher, release-environment approval)
  - GitHub Release 3.0.16 published with the awk-extracted changelog body (REL-03)
  - stable/3.0.x fast-forwarded to the release SHA; moving tags 3 and 3.0 re-pointed (RTD rebuild fired)
  - Docker Hub multi-arch images pushed (3.0.16 / 3.0 / 3 / latest)
  - dev-bump PR #796 (chore/dev-bump-3.0.17) open — handed to Plan 05
  - Post-release checklist issue #797 (manual D-08 completion)
affects: [06-05, post-release, gitbook-docs]

# Tech tracking
tech-stack:
  added: []
  patterns: ["D-07 human-tag-push release trigger with agent-proven pre-tag safety (SHA + FF-OK ancestry + empty-tag check)", "D-08 post-publish manual completion when rerun provably cannot recover"]

key-files:
  created:
    - .planning/phases/06-release-cut-3-0-16/deferred-items.md
  modified: []

key-decisions:
  - "post-release-checklist job failure is a deterministic release.yml bug (gh issue create with no checkout and no -R); rerun cannot recover, so D-08 manual completion applied: issue #797 created by hand, tag stays, fix deferred"
  - "No gh run rerun --failed issued: rerun replays the same workflow snapshot and would fail identically; all release-critical jobs were already green"

patterns-established:
  - "Pre-tag safety triple: resolve SHA from origin/main + merge-base --is-ancestor FF-OK + empty ls-remote tag check, proven before handing the user the push commands"

requirements-completed: [REL-02, REL-03]

coverage:
  - id: D1
    description: "3.0.16 tag pushed by the USER on the verified release SHA 1173c469 (D-07); pre-tag SHA/FF-OK/empty-tag checks proven first"
    requirement: REL-03
    verification:
      - kind: other
        ref: "git ls-remote --tags origin 3.0.16 == 1173c469e544a05e244e798b5231e5d3f118a77f"
        status: pass
    human_judgment: false
  - id: D2
    description: "Live release.yml run 29263984129 green through gates + all 5 testpypi-smoke legs (REL-02); publish-pypi succeeded after user approval of the release environment"
    requirement: REL-02
    verification:
      - kind: e2e
        ref: "gh run view 29263984129 -R datafolklabs/cement --json jobs (all release-critical jobs conclusion=success; publish-pypi success)"
        status: pass
      - kind: other
        ref: "curl https://pypi.org/pypi/cement/3.0.16/json returns the release metadata"
        status: pass
    human_judgment: false
  - id: D3
    description: "GitHub Release 3.0.16 published (isDraft false) with the awk-extracted changelog body starting with the highlights paragraph"
    requirement: REL-03
    verification:
      - kind: other
        ref: "gh release view 3.0.16 -R datafolklabs/cement --json tagName,isDraft,body"
        status: pass
    human_judgment: false
  - id: D4
    description: "branch-sync fast-forwarded stable/3.0.x to the release SHA; tag-sync re-pointed moving tags 3 and 3.0 (RTD rebuild fired); docker pushed multi-arch images"
    verification:
      - kind: other
        ref: "git rev-parse origin/stable/3.0.x == release SHA; git ls-remote --tags origin 3 3.0 both == release SHA; docker job conclusion=success"
        status: pass
    human_judgment: false
  - id: D5
    description: "dev-bump PR #796 (chore/dev-bump-3.0.17) open for Plan 05; zero-CI state is the accepted Pitfall 7 tradeoff"
    verification:
      - kind: other
        ref: "gh pr list -R datafolklabs/cement --json number,headRefName shows #796 chore/dev-bump-3.0.17"
        status: pass
    human_judgment: false

# Metrics
duration: ~2h 45m (incl. live run + two human checkpoint windows)
completed: 2026-07-13
status: complete
---

# Phase 6 Plan 04: Tag Push, Live Release Run, and Release Verification Summary

**3.0.16 shipped: user-pushed tag on 1173c469 triggered release.yml run 29263984129 — PyPI publish (OIDC), Docker multi-arch, stable/3.0.x fast-forward, moving tags 3/3.0, GitHub Release with changelog body, and dev-bump PR #796**

## Performance

- **Duration:** ~2h 45m (dominated by the live run + tag-push and approval checkpoint windows)
- **Started:** 2026-07-13T15:47:00Z (pre-tag safety checks)
- **Completed:** 2026-07-13T18:35:00Z (Task 3 verification green)
- **Tasks:** 3 (2 blocking human-verify checkpoints + 1 auto verification)
- **Files modified:** 0 repo files (planning artifacts only, per plan design)

## Accomplishments

- Pre-tag safety triple proven before the human push: release SHA resolved from
  origin/main (`1173c469e544a05e244e798b5231e5d3f118a77f`, matching the Plan 02
  squash-merge), `git merge-base --is-ancestor origin/stable/3.0.x <sha>`
  printed FF-OK (stable tip `0679bf51` is an ancestor), and
  `git ls-remote --tags origin 3.0.16` was empty (T-06-09 mitigations).
- USER pushed the `3.0.16` tag on the verified SHA (D-07 — agent never pushed);
  tag-triggered run 29263984129 (event `push`, ref `3.0.16`) monitored through
  preflight, comply, the full 7-leg test matrix, cli-smoke, isolated build,
  TestPyPI publish (skip-existing re-used the frozen Plan 03 bytes), and all 5
  testpypi-smoke legs (REL-02) — then paused at the single `release`
  environment gate (T-06-08).
- USER approved the deployment in the GitHub UI; publish-pypi succeeded via
  OIDC trusted publisher and the fan-out completed: docker (multi-arch
  amd64+arm64, tags 3.0.16/3.0/3/latest), branch-sync, tag-sync, gh-release,
  dev-bump all green.
- REL-03 verified end-to-end: GitHub Release 3.0.16 published (isDraft false,
  body opens with the highlights paragraph), stable/3.0.x tip == release SHA,
  moving tags `3` and `3.0` == release SHA (RTD rebuild fired), cement 3.0.16
  live on PyPI, dev-bump PR #796 open for Plan 05.

## Task Commits

This plan modifies no repo files by design — the release artifacts are the tag,
the workflow run, and its fan-out (all on GitHub/PyPI/Docker Hub), not commits.

**Plan metadata:** SUMMARY + deferred-items committed as `docs(06-04)`; tracking
(STATE/ROADMAP/REQUIREMENTS) committed separately.

## Files Created/Modified

- `.planning/phases/06-release-cut-3-0-16/deferred-items.md` - logs the
  release.yml post-release-checklist bug (out-of-scope fix)
- `.planning/phases/06-release-cut-3-0-16/06-04-SUMMARY.md` - this summary

## Decisions Made

- **No `gh run rerun --failed` for the post-release-checklist failure:** the
  failure is deterministic (see Deviations), a rerun replays the same workflow
  snapshot and would fail identically, and every release-critical job was
  already green. Rerun reserved for genuinely transient failures per D-08.
- **D-08 manual completion applied:** the checklist issue was created by hand
  (#797) with the exact body the job would have emitted; the 3.0.16 tag stays.

## Deviations from Plan

### Handled Issues

**1. [D-08 manual completion] post-release-checklist job failed on a deterministic release.yml bug**
- **Found during:** Task 2 (publish-side fan-out monitoring)
- **Issue:** The job runs `gh issue create` with no `actions/checkout` step and
  no `-R`/`GH_REPO`, so the gh CLI fails with
  `fatal: not a git repository` — flipping the run conclusion to `failure`
  even though all release-critical jobs succeeded.
- **Fix:** Created the checklist issue manually
  (https://github.com/datafolklabs/cement/issues/797, assignee derks, body
  identical to the workflow's, NEXT=3.0.17). Workflow fix (add
  `-R "$GITHUB_REPOSITORY"`) logged in `deferred-items.md` — out of scope
  because this plan modifies no repo files.
- **Files modified:** `.planning/phases/06-release-cut-3-0-16/deferred-items.md` (log only)
- **Verification:** Issue #797 exists; no duplicate checklist issue.

---

**Total deviations:** 1 (D-08 post-publish manual completion; no code changes)
**Impact on plan:** None on release correctness — the failed job is
notification-only. The tag, PyPI publish, Docker images, branch/tag sync, and
GitHub Release are all intact.

## Issues Encountered

- The run's overall conclusion reads `failure` solely because of the
  post-release-checklist job — anyone auditing run 29263984129 should read the
  per-job conclusions (all release-critical jobs `success`).

## User Setup Required

None - no external service configuration required. (Human actions performed
during execution: tag push and release-environment approval, per D-07.)

## Next Phase Readiness

- Plan 05 inputs ready: dev-bump PR **#796** (chore/dev-bump-3.0.17) open —
  its zero-CI state is the accepted Pitfall 7 tradeoff; post-release checklist
  issue **#797** open (GitBook docs, mailing list/Slack notify, merge #796).
- Deferred: fix release.yml post-release-checklist `gh issue create -R` bug
  before the next release cut (see deferred-items.md).

## Self-Check: PASSED

- 06-04-SUMMARY.md and deferred-items.md exist on disk
- SUMMARY commit 6d570632 present on gsd/phase-6-release-cut-3-0-16
- Tag 3.0.16 confirmed on release SHA 1173c469

---
*Phase: 06-release-cut-3-0-16*
*Completed: 2026-07-13*
