---
phase: 06-release-cut-3-0-16
plan: 05
subsystem: release
tags: [pypi, clean-venv, dev-bump, verification, announcement, github-release]

# Dependency graph
requires:
  - phase: 06-release-cut-3-0-16 (plan 02)
    provides: finalized 3.0.16 changelog highlights on main (1173c469) — source of the announcement copy
  - phase: 06-release-cut-3-0-16 (plan 03)
    provides: CI-04 green dry-run baseline 29262360749
  - phase: 06-release-cut-3-0-16 (plan 04)
    provides: live release run 29263984129, GitHub Release 3.0.16, dev-bump PR #796, checklist issue #797
provides:
  - REL-04 clean-venv proof — pip install cement==3.0.16 from production PyPI + App().run() round-trip + version assert (Python 3.14.3)
  - REL-05 closed — dev-bump PR #796 merged by the user (e9aede10); origin/main on VERSION (3, 0, 17, 'final', 0) with fresh `## 3.0.17 - DEVELOPMENT` changelog section
  - 06-ANNOUNCEMENT.md — paste-ready announcement derived verbatim from the changelog highlights (D-14); sending stays human on issue #797
  - 06-VERIFICATION.md — status passed, 5/5 ROADMAP success criteria with live evidence; REL-01..05/CI-04/DOCS-03 all Complete
  - REQUIREMENTS.md + ROADMAP.md — Phase 6 closed (5/5 plans, Complete 2026-07-13)
affects: [complete-milestone, post-release, gitbook-docs, next-release-cut]

# Tech tracking
tech-stack:
  added: []
  patterns: ["D-13 independent production-PyPI clean-venv proof after TestPyPI matrix smoke", "D-12 phase-end boundary: dev-bump merge + requirement flips close the phase; milestone completion is a separate session (D-15)"]

key-files:
  created:
    - .planning/phases/06-release-cut-3-0-16/06-ANNOUNCEMENT.md
    - .planning/phases/06-release-cut-3-0-16/06-VERIFICATION.md
  modified:
    - .planning/REQUIREMENTS.md
    - .planning/ROADMAP.md
    - .planning/phases/06-release-cut-3-0-16/deferred-items.md

key-decisions:
  - "Announcement body reuses the finalized CHANGELOG highlights paragraph verbatim (D-03/D-14 one source of truth); no fresh prose invented"
  - "RTD did not auto-rebuild when tag-sync force-updated moving tags 3/3.0 — user ran a manual RTD build; trigger-path check logged as deferred item 2 for the next release, NOT a gap"
  - "Post-release checklist #797, milestone completion (D-15), release.yml checklist-job fix, and the RTD trigger check recorded as deferred/human items in 06-VERIFICATION.md frontmatter, not gaps"

patterns-established:
  - "Clean-venv release proof: throwaway venv + pip install from production PyPI + SmokeApp(argv=[]) round-trip + get_version() assert, mirroring scripts/testpypi-smoke.py"

requirements-completed: [REL-04, REL-05]

coverage:
  - id: D1
    description: "3.0.16 installs cleanly from production PyPI in a clean venv with a working App().run() round-trip and exact version assert (REL-04, D-13)"
    requirement: REL-04
    verification:
      - kind: e2e
        ref: "pip install cement==3.0.16 (production PyPI) + SmokeApp(argv=[]) round-trip → 'REL-04 clean-venv OK: cement 3.0.16 on Python 3.14.3'"
        status: pass
    human_judgment: false
  - id: D2
    description: "Dev-bump PR #796 merged; main advanced to the 3.0.17 dev cycle (REL-05, D-12)"
    requirement: REL-05
    verification:
      - kind: other
        ref: "gh pr view 796 → MERGED 2026-07-13T18:38:28Z (e9aede10); git show origin/main:cement/core/backend.py → VERSION = (3, 0, 17, 'final', 0); origin/main CHANGELOG heads with '## 3.0.17 - DEVELOPMENT'"
        status: pass
    human_judgment: false
  - id: D3
    description: "Paste-ready release announcement derived from the finalized changelog highlights (D-14); sending stays a human step on issue #797"
    verification:
      - kind: other
        ref: "grep -qi 'cement 3.0.16' .planning/phases/06-release-cut-3-0-16/06-ANNOUNCEMENT.md"
        status: pass
    human_judgment: true
    rationale: "The copy quality and the decision of when/where to send (mailing list, Slack, GitBook) are human calls on checklist issue #797 (D-15)"
  - id: D4
    description: "06-VERIFICATION.md status passed; REL-01..05/CI-04/DOCS-03 flipped Complete; ROADMAP Phase 6 Complete"
    verification:
      - kind: other
        ref: "grep 'status: passed' 06-VERIFICATION.md; grep -E 'REL-0[1-5]|CI-04|DOCS-03' .planning/REQUIREMENTS.md shows zero Pending; ROADMAP Progress row '5/5 | Complete | 2026-07-13'"
        status: pass
    human_judgment: false

# Metrics
duration: ~25min (incl. human checkpoint window for the PR #796 merge)
completed: 2026-07-13
status: complete
---

# Phase 6 Plan 05: Release Close-Out Summary

**REL-04 clean-venv proof off production PyPI + user-merged dev-bump to 3.0.17 (PR #796), with a highlights-derived announcement draft and a passed 06-VERIFICATION.md flipping all 7 phase requirement IDs to Complete**

## Performance

- **Duration:** ~25 min (including the human checkpoint window for the PR #796 merge)
- **Started:** 2026-07-13T18:34:00Z
- **Completed:** 2026-07-13T18:58:00Z
- **Tasks:** 3 (1 checkpoint:human-verify + 2 auto)
- **Files modified:** 5 (2 created, 3 modified)

## Accomplishments

- REL-04 closed: fresh venv → `pip install cement==3.0.16` from production PyPI succeeded first try → `SmokeApp(argv=[])` `App().run()` round-trip clean → `get_version()` assert passed → `REL-04 clean-venv OK: cement 3.0.16 on Python 3.14.3`
- REL-05 closed: dev-bump PR #796 verified (VERSION → `(3, 0, 17, 'final', 0)`, fresh `## 3.0.17 - DEVELOPMENT` prepended) and merged by the user at 2026-07-13T18:38:28Z (`e9aede10`); origin/main confirmed on the 3.0.17 dev cycle
- 06-ANNOUNCEMENT.md drafted from the finalized changelog highlights paragraph verbatim (D-14) — subject line, upgrade line, GitHub Release/changelog/docs links, Docker tags; sending explicitly left human on issue #797
- 06-VERIFICATION.md written (status: passed, 5/5 ROADMAP success criteria with live run-id/gh-release/clean-venv evidence); REL-04/REL-05 flipped in REQUIREMENTS.md (the other five were flipped by Plans 02–04); ROADMAP Phase 6 marked Complete 2026-07-13
- New live-run observation logged: RTD did not auto-rebuild on the force-updated moving tags `3`/`3.0` — manual RTD build applied by the user; trigger-path check + stale-cache wipe guidance recorded in deferred-items.md item 2

## Task Commits

Each task was committed atomically:

1. **Task 1: REL-04 clean-venv verification + dev-bump PR merge** — no repo commit (verification-only checkpoint; evidence captured in 06-VERIFICATION.md; the merge itself is `e9aede10` on origin/main, authored by the workflow and merged by the user)
2. **Task 2: Draft the release announcement** — `a42d0a33` (docs(06-05): draft 3.0.16 release announcement from changelog highlights)
3. **Task 3: 06-VERIFICATION.md + requirement flips** — `0bbc57d5` (docs(06-05): verify phase 6 and flip REL-04/REL-05 to complete)

## Files Created/Modified

- `.planning/phases/06-release-cut-3-0-16/06-ANNOUNCEMENT.md` — paste-ready announcement copy (highlights-derived, D-14)
- `.planning/phases/06-release-cut-3-0-16/06-VERIFICATION.md` — phase verification report (status: passed)
- `.planning/REQUIREMENTS.md` — REL-04/REL-05 checkboxes + traceability rows → Complete
- `.planning/ROADMAP.md` — Phase 6 `[x]`, 5/5 plans, Progress row Complete 2026-07-13
- `.planning/phases/06-release-cut-3-0-16/deferred-items.md` — added item 2 (RTD force-updated-tag trigger gap)

## Decisions Made

- Announcement body quotes the CHANGELOG highlights paragraph verbatim rather than re-summarizing — preserves the D-03/D-14 single source of truth
- The `post-release-checklist` job failure (manually completed as #797), milestone completion (D-15), the release.yml fix, and the RTD trigger check are all recorded as deferred/human items in the VERIFICATION frontmatter — not gaps — because each has a named follow-up home

## Deviations from Plan

None on the plan's own tasks — executed as written. One environmental observation surfaced during the checkpoint window and was logged rather than fixed (scope boundary): the RTD webhook did not auto-trigger a rebuild when `tag-sync` force-updated the moving tags `3`/`3.0`; the user ran a manual RTD build. Logged to `deferred-items.md` item 2 with a pre-next-release trigger-path check and stale-cache wipe guidance.

## Issues Encountered

None. PyPI propagation had no lag (install succeeded on the first attempt, no retry needed), and PR #796's zero-CI state was the expected Pitfall 7 tradeoff, not a blocker.

## User Setup Required

None for the phase itself. Human follow-ups live on post-release checklist issue [#797](https://github.com/datafolklabs/cement/issues/797): GitBook changelog page, GitBook stable docs, mailing list + Slack announcements (paste-ready copy in 06-ANNOUNCEMENT.md).

## Next Phase Readiness

- Phase 6 is CLOSED at the D-12 boundary: all 7 requirement IDs (REL-01..05, CI-04, DOCS-03) Complete with live evidence; main is on the 3.0.17 dev cycle
- Milestone completion is a separate `/gsd-complete-milestone` session (D-15)
- Before the next release cut: fix the release.yml `post-release-checklist` job (`-R "$GITHUB_REPOSITORY"`) and verify the RTD trigger path for force-updated tags (deferred-items.md items 1–2)

---
*Phase: 06-release-cut-3-0-16*
*Completed: 2026-07-13*
## Self-Check: PASSED

All created files exist on disk and all task commits (a42d0a33, 0bbc57d5) plus the summary commit (15b39c94) are present in git history.
