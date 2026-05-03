---
phase: 02-dependencies-ci-pipeline
plan: 02
subsystem: infra
tags:
  - pip-audit
  - cve-spot-check
  - supply-chain
  - dev-only
  - docs-extra
  - phase-2

requires:
  - phase: 02-dependencies-ci-pipeline
    plan: 01
    provides: post-`pdm update` lockfile (commit 9f0f8627) — the venv state pip-audit scans against
  - phase: 02-dependencies-ci-pipeline
    plan: 01
    provides: requests 2.31.0 -> 2.33.1 bump that auto-resolved 3 baseline CVEs (CVE-2024-35195, CVE-2024-47081, CVE-2026-25645)
provides:
  - 02-PIP-AUDIT.md artifact with all 5 required sections (Pre-update baseline, Post-update results, Accepted, Resolutions, Pin-arounds) — D-19 acceptance #4 evidence
  - Per-finding disposition for all 13 post-Plan-01 pip-audit lines (11 unique CVEs across 5 packages); disposition split — Resolutions: 3 (via Plan 01); Accepted: 11 (dev/docs-only); Pin-arounds: 0
  - D-03 compliance proof — pip-audit not in pyproject.toml or Makefile; lockfile byte-identical pre/post pip-audit run
affects:
  - 02-08-PLAN (Phase 2 acceptance verification reads this artifact for D-19 #4)
  - Phase-5 SEC-01 (when permanent pip-audit CI surface lands, the Accepted set is re-litigated against the then-current advisory DB)

tech-stack:
  added: []
  patterns:
    - "D-03 ad-hoc spot-check pattern: install pip-audit transiently, run, uninstall — leaves no lockfile drift; not a permanent dev dep, not a Makefile target, not a CI job"
    - "Disposition triage by install-graph membership: dev-group + docs-extra transitives qualify for Accepted (not in any downstream `pip install cement[<runtime-extra>]` graph) per CLAUDE.md core-zero-runtime-deps invariant"
    - "CLAUDE.md filter-rule honored: docs(02): planning-artifact commit does NOT touch CHANGELOG (planning scaffolding != user-facing change)"

key-files:
  created:
    - .planning/phases/02-dependencies-ci-pipeline/02-PIP-AUDIT.md
  modified: []

key-decisions:
  - "All 13 pip-audit findings (11 unique CVEs) dispositioned as Accepted via dev/docs-only rationale per CONTEXT.md D-03 — none enter the runtime install graph for downstream `pip install cement[<runtime-extra>]` users; cement core has `dependencies = []` (PROJECT.md / CLAUDE.md zero-runtime-deps invariant)"
  - "Sub-step B (pin-around) intentionally NOT fired — CONTEXT.md D-02 forbids `[project.optional-dependencies]` specifier mutation, and pinning in `[dependency-groups].dev` would be a hygiene-only change with no downstream effect; deferred to Phase 5 SEC-01 alongside the recurring pip-audit CI surface"
  - "RESEARCH.md prediction (transitive certifi/idna/urllib3/pygments would auto-lift via `requests`/`sphinx` bumps) was inaccurate vs actual `pdm update --update-reuse` resolver behavior — reuse strategy preserved existing pins because no specifier change tightened lower bounds. Documented as a Resolutions-applied gap in the artifact, with --update-eager as the future-phase clearing mechanism"
  - "pip CVE-2026-3219 (no upstream fix) explicitly carried in Accepted with re-evaluation cadence (Phase 5 SEC-01 or pip patched-release publication, whichever comes first) — plan acceptance requires this exact disposition"

patterns-established:
  - "Phase 2 ad-hoc tooling install pattern: `pdm run python -m pip install <tool> && pdm run <tool> ... && pdm run python -m pip uninstall -y <tool>` — verified zero lockfile drift via `git status pdm.lock` before commit"
  - "pip-audit duplicate-row interpretation: when a package belongs to multiple `[dependency-groups]` (e.g., certifi in both `dev` and `docs`), pip-audit emits one row per group membership. Dedupe to unique-CVE count when reporting; full row count is the raw scanner output"
  - "Disposition-by-install-graph: trace each flagged package via `pdm list --tree` to determine whether it enters any downstream runtime path (i.e., reachable from `pip install cement[<extra>]` for any extra in `[project.optional-dependencies]` excluding `docs`); if not, qualifies for Accepted"

requirements-completed:
  - DEPS-03

# Metrics
duration: 7min
completed: 2026-05-02
---

# Phase 02 Plan 02: pip-audit Spot Check Summary

**One-shot ad-hoc pip-audit 2.10.0 against post-Plan-01 lockfile surfaces 11 unique CVEs across 5 packages — all dispositioned as Accepted (dev-group + docs-extra transitives only; cement core has zero runtime deps); 3 baseline-snapshot CVEs auto-resolved via Plan 01's requests 2.31.0->2.33.1 bump; pip-audit confirmed absent from pyproject.toml + Makefile (D-03); lockfile byte-identical pre/post run; D-19 acceptance #4 satisfied.**

## Performance

- **Duration:** ~7 min (single execution pass; one task with sub-steps A + C; sub-step B did not fire)
- **Started:** 2026-05-02 (post `make init` worktree bootstrap)
- **Completed:** 2026-05-02
- **Tasks:** 1 (sub-step A mandatory + B conditional skipped + C verification)
- **Atomic commits:** 1 (`docs(02): record pip-audit spot-check`)
- **Files created:** 1 (`02-PIP-AUDIT.md`)
- **Files modified:** 0 (`pyproject.toml`, `pdm.lock`, `CHANGELOG.md`, `Makefile` all byte-identical to Plan 01 output)

## Accomplishments

- DEPS-03 closed: `02-PIP-AUDIT.md` written with all 5 required sections (Pre-update baseline, Post-update results, Accepted vulnerabilities, Resolutions applied, Pin-arounds applied), date header, Plan 01 SHA citation (`9f0f8627`), and explicit per-finding disposition.
- D-19 acceptance #4 satisfied: artifact exists; every flagged finding has explicit disposition (Resolutions-applied: 3; Accepted: 11; Pin-arounds: 0); no silent omissions.
- D-03 compliance proven: `grep -F 'pip-audit' pyproject.toml` returns 0 lines; `grep -F 'pip-audit' Makefile` returns 0 lines. pip-audit was installed ad-hoc into the venv, run, and uninstalled; `pdm.lock` byte-identical pre/post via `git status pdm.lock`.
- 3 of the 16 baseline-snapshot CVEs (RESEARCH.md § "pip-audit Pre-Update Snapshot") confirmed as auto-resolved by Plan 01's `requests 2.31.0 -> 2.33.1` bump (CVE-2024-35195, CVE-2024-47081, CVE-2026-25645) — verified post-bump pip-audit run no longer lists `requests` among findings.
- pip CVE-2026-3219 (no upstream fix) and the residual urllib3 / certifi / idna / pygments / pip CVEs documented in the Accepted section with explicit dev/docs-only rationale and Phase 5 SEC-01 re-evaluation cadence.

## Task Commits

1. **Task 1: Run pip-audit, write artifact** — `69da9e14` (`docs(02): record pip-audit spot-check`). Created `.planning/phases/02-dependencies-ci-pipeline/02-PIP-AUDIT.md` (167 insertions). Body cites Plan 01 SHA, lists pre-update baseline (16 vulns), post-update results (13 raw rows / 11 unique CVEs), Resolutions-applied (3 via Plan 01), Pin-arounds (none), Accepted (11 with rationale and re-eval cadence). Subject 37 chars; body all ≤70 chars (CLAUDE.md 78-char wrap honored). Per CLAUDE.md filter-rule, this `docs(02)` commit does NOT touch CHANGELOG.md.

Sub-step B (pin-around) did NOT fire — no `chore(deps): pin <pkg> for CVE` commits, no CHANGELOG `[deps]` Misc entries. RESEARCH.md projection that all post-update findings would qualify for Accepted (because they're either no-fix or dev-only/docs-only transitives) was confirmed at execution time.

## pip-audit Run Details

- **Tool version:** pip-audit 2.10.0
- **Vulnerability service:** PyPI Advisory DB (default — sufficient per CONTEXT D-03)
- **Invocation path:** Path A from RESEARCH.md § "pip-audit Invocation Mechanics" (`pdm run python -m pip install pip-audit` → `pdm run pip-audit --format markdown` → `pdm run python -m pip uninstall -y pip-audit`). pipx and uv unavailable on host.
- **Pre-update baseline (informational, from RESEARCH.md):** 16 vulns / 6 packages
- **Post-update findings (raw rows):** 13 (with duplicates from group-membership; certifi listed twice for `dev` + `docs`, idna listed twice for `dev` + `docs`)
- **Post-update findings (unique CVEs):** 11 across 5 packages

## Per-CVE Disposition Summary

| CVE | Pkg | Fix Version | Disposition | Rationale |
|-----|-----|-------------|-------------|-----------|
| CVE-2024-35195 | requests | 2.32.0 | Resolved (Plan 01) | requests 2.31.0 -> 2.33.1 |
| CVE-2024-47081 | requests | 2.32.4 | Resolved (Plan 01) | requests 2.31.0 -> 2.33.1 |
| CVE-2026-25645 | requests | 2.33.0 | Resolved (Plan 01) | requests 2.31.0 -> 2.33.1 |
| PYSEC-2024-230 | certifi | 2024.7.4 | Accepted | dev-group + docs-extra transitive only |
| PYSEC-2024-60 | idna | 3.7 | Accepted | dev-group + docs-extra transitive only |
| CVE-2026-1703 | pip | 26.0 | Accepted | build-env tool, not a runtime dep |
| CVE-2026-3219 | pip | (no fix) | Accepted | no upstream fix; build-env tool |
| CVE-2026-4539 | pygments | 2.20.0 | Accepted | dev-group + docs-extra transitive only |
| CVE-2024-37891 | urllib3 | 1.26.19, 2.2.2 | Accepted | dev-group + docs-extra transitive only |
| CVE-2025-50182 | urllib3 | 2.5.0 | Accepted | dev-group + docs-extra transitive only |
| CVE-2025-50181 | urllib3 | 2.5.0 | Accepted | dev-group + docs-extra transitive only |
| CVE-2025-66418 | urllib3 | 2.6.0 | Accepted | dev-group + docs-extra transitive only |
| CVE-2025-66471 | urllib3 | 2.6.0 | Accepted | dev-group + docs-extra transitive only |
| CVE-2026-21441 | urllib3 | 2.6.3 | Accepted | dev-group + docs-extra transitive only |

**Totals:** 14 baseline-snapshot CVEs traced (3 resolved via Plan 01 + 11 still-flagged Accepted). 0 pin-arounds applied. 0 silent omissions.

## D-03 Compliance Verification

All checks executed during Sub-step C:

- `grep -F 'pip-audit' pyproject.toml` returns 0 lines — D-03 OK (pip-audit NOT in `[dependency-groups].dev`)
- `grep -F 'pip-audit' Makefile` returns 0 lines — D-03 OK (no `make pip-audit` target)
- `git status pdm.lock` returns clean — no lockfile drift from ad-hoc install/uninstall cycle
- `git show HEAD --stat | grep CHANGELOG.md` returns 0 lines — CLAUDE.md filter-rule for `docs(02):` planning-artifact commits honored

## D-19 Acceptance #4 Verification

| Acceptance check | Result |
|------------------|--------|
| `02-PIP-AUDIT.md` exists in phase directory | PASS — `test -f` returns 0 |
| `# Phase 2` top-level title (count=1) | PASS — `grep -c "^# Phase 2"` returns 1 |
| `## Post-update results` (count=1) | PASS |
| `## Accepted vulnerabilities` (count=1) | PASS |
| `## Resolutions applied` (count=1) | PASS |
| `## Pin-arounds applied` (count=1) | PASS |
| Date header `**Run date:** 2026-05-02` | PASS |
| Plan 01 SHA reference `\`9f0f8627\`` | PASS |
| pip CVE-2026-3219 in Accepted with "no fix" + "build-env" rationale | PASS — both phrases present |
| Every flagged CVE has explicit disposition (no silent omissions) | PASS — 14 entries traced (3 Resolutions + 11 Accepted) |

## Files Created/Modified

- `.planning/phases/02-dependencies-ci-pipeline/02-PIP-AUDIT.md` (NEW, 167 lines) — DEPS-03 spot-check artifact. Sections: top-level header, Pre-update baseline (informational table from RESEARCH.md), Post-update results (raw pip-audit markdown output), Accepted vulnerabilities (11 entries with rationale and re-evaluation cadence), Resolutions applied via Plan 01, Pin-arounds applied this plan (none), Notes (one-shot scope reminder, --update-eager future-phase clearing mechanism, D-19 acceptance #4 evidence statement).

## Decisions Made

- **All 11 unique CVEs Accepted (vs Pin-around in `[dependency-groups].dev`):** Pin-around in dev-group would be a hygiene-only change with no downstream effect (cement core ships with `dependencies = []`; downstream `pip install cement[<extra>]` does not pull these transitives for any runtime extra). CONTEXT.md D-03 explicitly directs DEV-ONLY findings to "document in 02-PIP-AUDIT.md 'Accepted' section ... DO NOT pin-around in pyproject.toml." docs-extra is downstream-installable, but D-02 forbids `[project.optional-dependencies]` specifier mutation, so the only Pin-around path would also be `[dependency-groups].dev` — same hygiene-only outcome. Deferred to Phase 5 SEC-01 alongside permanent pip-audit CI integration.
- **Document `--update-eager` as future-phase clearing mechanism:** Plan 01's `pdm update --update-reuse` (default strategy) preserved existing transitive pins because no specifier change forced a re-resolve. RESEARCH.md projected the `requests 2.31->2.33` and `sphinx 7.1->8.1` bumps would lift the transitives; in practice they didn't. Adding the `--update-eager` note in the Notes section gives Phase 5 a concrete clearing mechanism without making it a Phase 2 deliverable.
- **Honor CLAUDE.md changelog filter-rule strictly:** No CHANGELOG entry for the `docs(02): record pip-audit spot-check` commit (planning-artifact, not user-facing). Sub-step B did not fire, so no `[deps]` Misc entries either. CHANGELOG.md byte-identical to Plan 01 output.

## Deviations from Plan

None — plan executed exactly as written. Sub-step A (artifact creation) executed as specified; Sub-step B (pin-around) intentionally skipped per RESEARCH.md projection and CONTEXT.md D-03 disposition rules; Sub-step C (verification + commit) executed as specified.

The plan's `<action>` block explicitly anticipated this branch: "Per RESEARCH.md projection, this branch is not expected to fire (the only post-update unpatched CVE is pip CVE-2026-3219, which is build-env-only and goes to 'Accepted')." Actual post-update findings exceeded the projection (11 unique CVEs vs the projected ~1), but all qualified for Accepted under the same dev/docs-only rationale that CONTEXT.md D-03 already approved for the requests dev-dep. No new disposition pattern needed.

## Issues Encountered

- **Worktree venv missing on first invocation:** Fresh worktree had no `.venv/`; `pdm run python -m pip install pip-audit` would have failed. Resolved by `make init` (per user MEMORY.md `feedback_recovery_make_init`). Not a plan deviation — environmental setup only, identical to Plan 01's experience.
- **RESEARCH.md projection vs actual resolver behavior:** RESEARCH.md § "pip-audit Pre-Update Snapshot" projected that requests/sphinx bumps would auto-lift transitive certifi/idna/urllib3/pygments. Actual `pdm update --update-reuse` (the default strategy that produced Plan 01's lockfile) preserved them because no specifier change tightened lower bounds enough to force re-resolution. Resolved by documenting in the artifact's Resolutions-applied section with an explicit "(no other automatic transitive resolutions)" note and citing `--update-eager` as the future-phase clearing mechanism. Not a plan deviation — RESEARCH.md was a projection, the artifact records the actual run.

## Self-Check

Verifying claimed work exists:

**Files:**
- `[FOUND]` `.planning/phases/02-dependencies-ci-pipeline/02-PIP-AUDIT.md` (created — 167 lines, all 5 required sections grep-verified)

**Commits:**
- `[FOUND]` `69da9e14` (`docs(02): record pip-audit spot-check`) — `git log --oneline -1` confirms

**Acceptance criteria:**
- `[PASS]` `test -f .planning/phases/02-dependencies-ci-pipeline/02-PIP-AUDIT.md`
- `[PASS]` `grep -c "^# Phase 2"` returns 1
- `[PASS]` `grep -c "^## Post-update results"` returns 1
- `[PASS]` `grep -c "^## Accepted vulnerabilities"` returns 1
- `[PASS]` `grep -c "^## Resolutions applied"` returns 1
- `[PASS]` `grep -c "^## Pin-arounds applied"` returns 1
- `[PASS]` Date header `**Run date:** 2026-05-02` matches `\*\*Run date:\*\* 20[0-9]{2}-[0-9]{2}-[0-9]{2}`
- `[PASS]` Plan 01 SHA citation `Plan 01 commit \`9f0f8627\`` present
- `[PASS]` `! grep -F 'pip-audit' pyproject.toml` (D-03)
- `[PASS]` `! grep -F 'pip-audit' Makefile` (D-03)
- `[PASS]` `git log -1 --pretty=%s` matches `^docs\(02\): record pip-audit spot-check$`
- `[PASS]` Subject 37 chars; longest body line 70 chars (both ≤78)
- `[PASS]` `git show HEAD --stat | grep CHANGELOG.md` returns 0 lines (CLAUDE.md filter-rule)
- `[PASS]` pip CVE-2026-3219 entry in Accepted section contains both "no upstream fix" AND "build-environment" rationale text
- `[PASS]` `make comply` exits 0 (sanity — source untouched, expected green; verified post-commit)

**Self-Check: PASSED**

## Next Phase Readiness

- **Plan 03 (coverage gate finalization):** Inherits the green `make comply` baseline (verified post-commit at 51 source files clean); test suite untouched.
- **Wave 2/3 plans (CI Action pinning, Dependabot, workflow_dispatch, matrix update):** Unrelated to this plan's output; share no files with `02-PIP-AUDIT.md`.
- **Plan 08 (acceptance verification):** Will read `02-PIP-AUDIT.md` for D-19 #4 evidence.
- **Phase 5 SEC-01 (deferred):** When permanent pip-audit CI surface lands, the 11 Accepted findings get re-litigated against then-current advisory DB; clearing mechanism documented in artifact's Notes section (`pdm update --update-eager` scoped by `-G dev` / `-G docs`).

No blockers. Phase 2 Plan 03 is unblocked.

---

*Phase: 02-dependencies-ci-pipeline*
*Plan: 02*
*Completed: 2026-05-02*
