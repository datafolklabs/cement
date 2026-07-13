---
phase: 06-release-cut-3-0-16
verified: 2026-07-13T19:12:00Z
status: passed
score: 5/5 must-haves verified
behavior_unverified: 0
overrides_applied: 0
overrides: []
re_verification: "2026-07-13T19:12:00Z — independent gsd-verifier pass corroborated all claims against live systems (git tags via gh api, PyPI JSON, gh release, run 29263984129 jobs, REQUIREMENTS/ROADMAP flips); no discrepancies, status passed upheld"
gaps: []
deferred:
  - truth: "Post-release notifications sent (mailing list, Slack, GitBook changelog + stable docs)"
    addressed_in: "Post-release checklist issue #797 (human steps, beyond the phase boundary per D-12/D-15)"
    evidence: "https://github.com/datafolklabs/cement/issues/797 — 5-item checklist created manually (D-08) after the post-release-checklist job's deterministic failure; 06-ANNOUNCEMENT.md provides the paste-ready copy (D-14)"
  - truth: "Milestone v1.0 completion (archive, next-milestone setup)"
    addressed_in: "Separate /gsd-complete-milestone session (D-15)"
    evidence: "06-CONTEXT.md D-15: milestone completion is explicitly a follow-up session, not a Phase 6 deliverable; Phase 6 closes at the requirement flips + this VERIFICATION.md (D-12)"
  - truth: "release.yml post-release-checklist job creates its issue automatically"
    addressed_in: "Future fix (deferred-items.md item 1) — add -R \"$GITHUB_REPOSITORY\" (or GH_REPO env) to the gh issue create step"
    evidence: "deferred-items.md: job fails with 'not a git repository' (no checkout, no -R); rerun cannot recover (same workflow snapshot); manual D-08 completion applied as issue #797; all release-critical jobs green on run 29263984129"
  - truth: "RTD auto-rebuilds versioned docs when tag-sync force-updates the moving tags 3/3.0"
    addressed_in: "Pre-next-release check (deferred-items.md item 2) — verify the RTD webhook/automation-rule trigger path for force-updated tags before the 3.0.17/3.0.18 cut"
    evidence: "Observed live on the 3.0.16 release: the tag-sync job force-repointed tags 3/3.0 but no RTD build fired; the user triggered a manual RTD build. If a stale build persists, wipe the RTD build cache (Builds -> wipe) before rebuilding."
human_verification: []
---

# Phase 6: Release Cut 3.0.16 Verification Report

**Phase Goal:** Cut the 3.0.16 release: finalize the changelog, validate the
release workflow against TestPyPI, tag, publish to PyPI, and bump the dev
version to 3.0.17 per odd/even convention.

**Verified:** 2026-07-13
**Status:** passed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths (ROADMAP Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | The changelog entry for 3.0.16 enumerates all user-visible changes (deprecations added, dep bumps, Python matrix change to 3.10–3.14, refactor highlights at a non-API-breaking level) | ✓ VERIFIED | Plan 02: release-prep PR #795 squash-merged to main as `1173c469` carrying the finalized `## 3.0.16 - July 13, 2026` section — narrative highlights paragraph (four locked D-03 themes) + Bugs/Features/Refactoring/Misc/Deprecations buckets. D-01 cross-check added 3 initially-missing entries (#756 `__all__`, #757 base PR CI, devbox/direnv). The `gh-release` job awk-extracted this exact section as the GitHub Release body. |
| 2 | A pre-release upload to TestPyPI installs cleanly on Python 3.10, 3.11, 3.12, 3.13, and 3.14, and a minimal `App().run()` round-trip succeeds on each | ✓ VERIFIED | Plan 03: final `workflow_dispatch` dry-run [run 29262360749](https://github.com/datafolklabs/cement/actions/runs/29262360749) against finalized main `1173c469` — all 5 `testpypi-smoke` matrix legs (3.10–3.14) green (install + import + `App().run()` round-trip + version assert via `scripts/testpypi-smoke.py`). The live release run 29263984129 re-smoked the identical frozen TestPyPI bytes (skip-existing) on all 5 legs. |
| 3 | `cement/__init__.py`, `pyproject.toml`, and any other version-of-record locations all read `3.0.16` at tag time and `3.0.17` immediately after | ✓ VERIFIED | At tag time: tag `3.0.16` points at `1173c469e544a05e244e798b5231e5d3f118a77f` whose `cement/core/backend.py` reads `VERSION = (3, 0, 16, 'final', 0)` (single source of truth — `pyproject.toml` reads it via `[tool.pdm.version] source="call"`, `cement/__init__.py` re-exports `get_version()`). Immediately after: dev-bump PR #796 merged `2026-07-13T18:38:28Z` as `e9aede10`; `git show origin/main:cement/core/backend.py` now reads `VERSION = (3, 0, 17, 'final', 0)` and `git show origin/main:CHANGELOG.md` heads with `## 3.0.17 - DEVELOPMENT` (REL-05, D-12). |
| 4 | The `3.0.16` git tag exists, the GitHub release page is published with the changelog body, and `pip install cement==3.0.16` from PyPI succeeds on a clean venv | ✓ VERIFIED | `gh release view 3.0.16` → published `2026-07-13T18:23:43Z`, `isDraft: false`, https://github.com/datafolklabs/cement/releases/tag/3.0.16 (body = awk-extracted changelog section). REL-04 clean-venv proof (Plan 05 Task 1, D-13): fresh venv → `pip install cement==3.0.16` from production PyPI succeeded first try (no propagation lag) → `SmokeApp(argv=[])` `App().run()` round-trip clean → `get_version()` assert passed → output `REL-04 clean-venv OK: cement 3.0.16 on Python 3.14.3`. |
| 5 | The release workflow itself (not just the artifacts) ran end-to-end without manual intervention beyond the user-approved publish step | ✓ VERIFIED | Live tag-push run [29263984129](https://github.com/datafolklabs/cement/actions/runs/29263984129): gates → build → testpypi-publish → 5-leg testpypi-smoke → (single user approval on the `release` environment) → publish-pypi → docker (multi-arch, 4 tags) → branch-sync (stable/3.0.x FF) → tag-sync (3/3.0 repointed) → gh-release → dev-bump (PR #796) all green with zero manual intervention beyond the one approval. Sole exception: the non-release-critical `post-release-checklist` job failed on a deterministic release.yml bug (`gh issue create` without checkout/`-R`); manually completed as issue #797 per D-08 and recorded as deferred, not a gap (fix logged in deferred-items.md). |

**Score:** 5/5 truths verified (0 present-but-behavior-unverified; 0 overrides)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `.planning/phases/06-release-cut-3-0-16/06-VERIFICATION.md` | status: passed; requirement-coverage table flipping REL-01..05/CI-04/DOCS-03 | ✓ VERIFIED | This report. |
| `.planning/phases/06-release-cut-3-0-16/06-ANNOUNCEMENT.md` | Paste-ready announcement copy derived from the finalized changelog highlights (D-14) | ✓ VERIFIED | Created (commit `a42d0a33`): subject line, highlights paragraph reused verbatim (all four locked themes), `pip install -U cement` upgrade line, GitHub Release + changelog + docs links, Docker tags, and an explicit note that SENDING stays human on issue #797 (D-15). |
| Flipped traceability rows in `.planning/REQUIREMENTS.md` | REL-01..05, CI-04, DOCS-03 Complete | ✓ VERIFIED | REL-01/REL-02/REL-03/CI-04/DOCS-03 flipped by Plans 02–04; REL-04/REL-05 flipped this plan. See Requirements Coverage below. |
| Phase 6 completion in `.planning/ROADMAP.md` | Phase 6 `[x]`, Progress row Complete | ✓ VERIFIED | Updated this plan (5/5 plans, Complete, 2026-07-13). |
| main on the 3.0.17 dev cycle (via merged dev-bump PR #796, authored by the workflow) | `VERSION = (3, 0, 17, ...)` + fresh `## 3.0.17 - DEVELOPMENT` | ✓ VERIFIED | Merge commit `e9aede10` (`2026-07-13T18:38:28Z`); both confirmed live against `origin/main`. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|-----|-----|--------|---------|
| REQUIREMENTS.md traceability | Phase 6 evidence | REL-01..05/CI-04/DOCS-03 rows → Complete | ✓ WIRED | Each flip is backed by a live citation in the Requirements Coverage table below (run id / gh release / clean-venv / merge commit). |
| dev-bump PR #796 merge | 3.0.17 dev cycle on main | User merge (D-12 phase-end boundary) | ✓ WIRED | `origin/main` VERSION tuple + CHANGELOG header confirmed post-merge; downstream work now targets 3.0.17. Milestone completion remains a separate session (D-15). |
| tag `3.0.16` | GitHub Release + PyPI artifact | release.yml run 29263984129 | ✓ WIRED | Tag on `1173c469`; release published; `cement==3.0.16` live on production PyPI (proven by the clean-venv install). |

### Behavioral Spot-Checks / Probe Execution

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| REL-04 clean-venv install from production PyPI | `python3 -m venv <tmp> && pip install cement==3.0.16` | `Successfully installed cement-3.0.16` (first attempt, no retry needed) | ✓ PASS |
| Import + `App().run()` round-trip + version assert | `SmokeApp(argv=[])` pattern mirroring `scripts/testpypi-smoke.py` | `REL-04 clean-venv OK: cement 3.0.16 on Python 3.14.3` | ✓ PASS |
| GitHub Release published, not draft | `gh release view 3.0.16 --json tagName,url,publishedAt,isDraft` | `publishedAt: 2026-07-13T18:23:43Z`, `isDraft: false` | ✓ PASS |
| Dev-bump PR merged | `gh pr view 796 --json state,mergedAt,mergeCommit` | `MERGED` at `2026-07-13T18:38:28Z`, merge commit `e9aede10` | ✓ PASS |
| main advanced to 3.0.17 | `git show origin/main:cement/core/backend.py \| grep VERSION` | `VERSION = (3, 0, 17, 'final', 0)  # pragma: nocover  # version constant` | ✓ PASS |
| Fresh dev changelog section | `git show origin/main:CHANGELOG.md \| head` | Top section header `## 3.0.17 - DEVELOPMENT` with empty buckets | ✓ PASS |
| Dev-bump PR diff scope | `gh pr diff 796` | Exactly 2 files: backend.py one-line VERSION bump + CHANGELOG 12-line prepend | ✓ PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| REL-01 | 02 | Version bumped to 3.0.16 across all version-of-record locations | ✓ SATISFIED | `backend.py` `VERSION = (3, 0, 16, 'final', 0)` on release SHA `1173c469` (PR #795 squash-merge); pyproject/`__init__` read it via `get_version()` single source of truth — the tagged bytes carry 3.0.16 everywhere. |
| REL-02 | 03, 04 | Pre-release smoke-test on TestPyPI passes (install + import + round-trip on each supported Python) | ✓ SATISFIED | Dry-run 29262360749 + live run 29263984129: all 5 `testpypi-smoke` legs (3.10–3.14) green on the frozen 3.0.16 TestPyPI bytes. |
| REL-03 | 04 | 3.0.16 git tag created, GitHub release notes published with changelog | ✓ SATISFIED | Tag `3.0.16` = `1173c469e544a05e244e798b5231e5d3f118a77f` (user-pushed, D-07); `gh release view 3.0.16` published `2026-07-13T18:23:43Z` with the awk-extracted changelog body. |
| REL-04 | 05 | PyPI publish completed; version installs cleanly on Python 3.10–3.14 | ✓ SATISFIED | `publish-pypi` (OIDC, approval-gated) green on run 29263984129; independent clean-venv production-PyPI proof (D-13): `pip install cement==3.0.16` + `App().run()` round-trip + version assert → `REL-04 clean-venv OK: cement 3.0.16 on Python 3.14.3`. Per-Python 3.10–3.14 coverage proven on the identical bytes by the 5-leg TestPyPI smoke (REL-02). |
| REL-05 | 05 | Post-release version bumped to 3.0.17 (next dev cycle) | ✓ SATISFIED | Workflow-authored dev-bump PR #796 merged by the user (`e9aede10`, `2026-07-13T18:38:28Z`); `origin/main` reads `(3, 0, 17, 'final', 0)` with a fresh `## 3.0.17 - DEVELOPMENT` changelog section. |
| CI-04 | 03 | Release workflow validated end-to-end against TestPyPI before the 3.0.16 cut | ✓ SATISFIED | GREEN `workflow_dispatch` dry-run [29262360749](https://github.com/datafolklabs/cement/actions/runs/29262360749) against finalized main `1173c469`: gates + build + testpypi-publish + all 5 smoke legs green; publish-side correctly skipped. |
| DOCS-03 | 02 | Changelog updated for 3.0.16 with all user-visible changes | ✓ SATISFIED | Finalized `## 3.0.16 - July 13, 2026` section on main (`1173c469`): D-01 commit-log cross-check completed (3 missing entries added), highlights paragraph with the four locked themes, `[area]`-prefixed one-line entries per CLAUDE.md convention. |

No orphaned requirements: the phase's declared set (DOCS-03, CI-04, REL-01..05)
exactly matches the seven IDs flipped to Complete in REQUIREMENTS.md.

### Anti-Patterns Found

None. This plan authored planning artifacts only (announcement draft +
verification report + traceability flips); no product code was touched. Scanned
the new artifacts for `TBD`/`FIXME`/`XXX`/`HACK`/`PLACEHOLDER` — zero hits (the
announcement's unchecked sending boxes are the deliberate human handoff, D-15).

### Human Verification Required

None blocking phase closure. The following remain open BEYOND the phase
boundary by design (D-12/D-15) — deferred, NOT gaps:

1. **Post-release checklist issue [#797](https://github.com/datafolklabs/cement/issues/797)** — GitBook changelog page, GitBook stable docs,
   mailing list + Slack notifications (paste-ready copy in 06-ANNOUNCEMENT.md).
2. **Milestone completion** — a separate `/gsd-complete-milestone` session
   archives the milestone (D-15).
3. **release.yml `post-release-checklist` job fix** — add `-R "$GITHUB_REPOSITORY"`
   (or `GH_REPO` env) to the `gh issue create` step (deferred-items.md item 1).
4. **RTD trigger path for force-updated tags** — the RTD webhook did not
   auto-fire when tag-sync force-repointed the moving tags `3`/`3.0` on the live
   run; the user triggered a manual RTD build. Before the next release, verify
   RTD's automation rules/webhook handle force-updated tags; if a stale build
   persists, wipe the RTD build cache before rebuilding (deferred-items.md item 2).

### Gaps Summary

No gaps. One live-run deviation occurred and was resolved within the phase: the
`post-release-checklist` job failed deterministically (release.yml bug — `gh
issue create` with no checkout and no `-R`), and per D-08 the checklist issue
was created manually as #797 with the exact body the job would have emitted; no
rerun was issued because a rerun replays the same workflow snapshot and all
release-critical jobs were already green. The workflow fix and the newly
observed RTD force-updated-tag trigger gap are recorded in the frontmatter
`deferred` section with named follow-up homes, not as gaps.

---

_Verified: 2026-07-13_
_Verifier: Claude (gsd-executor, Plan 06-05 Task 3)_
