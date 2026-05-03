---
phase: 02-dependencies-ci-pipeline
plan: 06
subsystem: ci
tags:
  - dependabot
  - github-actions-ecosystem
  - supply-chain
  - phase-2
  - ci-05

requires:
  - phase: 02-dependencies-ci-pipeline
    plan: 04
    provides: exact-tag-pinned Actions across both workflow files (the static pin baseline Dependabot watches for upstream releases)
provides:
  - .github/dependabot.yml — Dependabot v2 config opening weekly version-update PRs for the github-actions ecosystem
  - CHANGELOG `[ci] Enable Dependabot for github-actions ecosystem (weekly)` Misc-bucket entry in `## 3.0.15 - DEVELOPMENT`
  - Documentation in commit body of the repo-level "Dependabot security updates" requirement (RESEARCH.md Correction 2 + Pitfall 6)
  - Verified ON state of the repo-level "Dependabot security updates" toggle (Task 2 human-verify result)
  - CI-05 closure (paired with Plan 04): static pin baseline + dynamic monitoring + CVE backstop all active
affects:
  - 02-07-PLAN (workflow_dispatch trigger on pdm.yml) — modifies pdm.yml without conflicting with Dependabot watching the same workflow
  - 02-08-PLAN (phase acceptance verification) — re-runs CI-05 acceptance against this combined baseline (Plan 04 + Plan 06)

tech-stack:
  added:
    - "Dependabot v2 (GitHub-native; no repo dependencies added)"
  patterns:
    - "D-07 honored: ONLY github-actions ecosystem in dependabot.yml; pip stays out (pdm.yml cron owns it)"
    - "RESEARCH.md Correction 2 + Pitfall 6 acknowledged: yaml file alone enables version-updates only; security-CVE-driven PRs require the repo-level `Settings -> Code security and analysis -> Dependabot security updates` toggle (the toggle the user described in CONTEXT.md `<specifics>`)"
    - "Schedule weekly + monday — aligns with pdm.yml cron's Mon 03:05 UTC review window"
    - "Labels `dependencies` + `github-actions` align with Phase 4 triage labels"
    - "Commit-message prefix `ci` matches cement D-17 convention; `include: scope` produces `ci(deps): bump...` PR titles"
    - "NO `groups` stanza — RESEARCH.md recommends OMITTING for first-time Dependabot enablement; revisit later if PR volume becomes noisy"

key-files:
  created:
    - .github/dependabot.yml
    - .planning/phases/02-dependencies-ci-pipeline/02-06-SUMMARY.md (this file)
  modified:
    - CHANGELOG.md

key-decisions:
  - "yaml-only Dependabot is insufficient for the user's stated CVE-backstop need — the repo-level `Dependabot security updates` toggle is a SEPARATE setting (no API; UI-only) and the commit body documents this requirement so it's not lost when planning artifacts age out"
  - "User confirmed the repo-level toggle is ON at https://github.com/datafolklabs/cement/settings/security_analysis (Task 2 human-verify checkpoint)"
  - "NO `groups` stanza this phase — observe per-Action PR signal first; revisit grouping later if PR volume becomes noisy"
  - "NO `pip` ecosystem — D-07 explicit exclusion; pdm.yml cron handles pip dep bumps already"
  - "Schedule weekly on Monday — aligns with pdm.yml cron Mon 03:05 UTC, giving one weekly review window for both surfaces"
  - "Continuation-agent re-execution: this is a fresh worktree (agent-a2474cebe6e1141dd) re-doing Plan 06 from base 878f0701. The prior worktree (agent-aefc699d9a5ffc12f) was removed and its commits never merged. No work was lost — Plan 06 had only reached the Task 2 checkpoint in the prior session, and Task 1's commit was scoped to dependabot.yml + CHANGELOG only."

patterns-established:
  - "yaml-config + repo-toggle dual-gate documentation pattern: when a config file is necessary but not sufficient, the commit body must document the supplementary repo-setting requirement so future maintainers can find it via `git log` even after planning artifacts move"
  - "Atomic ci: commit folding the dependabot.yml creation + the CHANGELOG entry — same shape as Plan 04's `ci: pin GitHub Actions to exact tags` commit (D-17 author's discretion)"

requirements-completed:
  - CI-05

duration: ~10min
completed: 2026-05-03
---

# Phase 02 Plan 06: Enable Dependabot for github-actions Ecosystem Summary

**Dependabot v2 config opening weekly version-update PRs for the github-actions ecosystem (D-07; pip stays out per explicit exclusion), backstopping Plan 04's exact-tag pinning; the repo-level `Dependabot security updates` toggle is verified ON (user-confirmed) so security-CVE-driven PRs also auto-open against pinned Actions per GHSA.**

## Performance

- **Duration:** ~10 min (continuation re-execution in fresh worktree)
- **Started:** 2026-05-03T04:30:00Z (approx — re-execution start in fresh worktree)
- **Completed:** 2026-05-03T04:45:13Z
- **Tasks:** 2 (Task 1 atomic; Task 2 human-verify, user-confirmed)
- **Files created:** 1 (`.github/dependabot.yml`)
- **Files modified:** 1 (`CHANGELOG.md`)

## Accomplishments

- `.github/dependabot.yml` created with valid Dependabot v2 schema for github-actions ecosystem only (D-07).
- Weekly Monday schedule aligns with pdm.yml cron Mon 03:05 UTC review window.
- CHANGELOG `## 3.0.15 - DEVELOPMENT` Misc bucket has new `[ci] Enable Dependabot for github-actions ecosystem (weekly)` entry.
- Commit body explicitly documents the repo-level `Dependabot security updates` toggle requirement and the literal phrase "MUST also be ENABLED" (so the dual-gate is bisectable from `git log` even after planning artifacts age out).
- Repo-level toggle verified ON by user (Task 2 human-verify): "the repo-level Dependabot security updates toggle is already ON / turned ON at https://github.com/datafolklabs/cement/settings/security_analysis".
- CI-05 closure achieved when paired with Plan 04: static pin baseline (Plan 04) + dynamic version-update monitoring (this plan) + CVE-driven security backstop (repo toggle, verified by user).

## Task Commits

| Task | Description | Hash | Files |
| ---- | ----------- | ---- | ----- |
| 1 | `ci: enable Dependabot for github-actions ecosystem` | `dfb9abba` | `.github/dependabot.yml` (created), `CHANGELOG.md` (Misc bucket appended) |
| 2 | Human-verify checkpoint — repo-level toggle state | (no commit) | n/a — UI-only verification, user-confirmed |

Single atomic `ci:` commit per D-17 author's discretion (same shape as Plan 04's `ci: pin GitHub Actions to exact tags` commit). The atomic commit folds the dependabot.yml creation + the CHANGELOG entry because both are the same concern.

## Task 2 — Human-Verify Result (Repo-Level Toggle)

**User verification result, embedded verbatim per the continuation-agent prompt:**

> User confirmed: Dependabot security updates toggle is already ON / turned ON at https://github.com/datafolklabs/cement/settings/security_analysis

This satisfies the Task 2 pass criteria ("`Dependabot security updates` toggle is ON at the time of verification, regardless of whether it was already on or you turned it on"). RESEARCH.md Correction 2 + Pitfall 6 mitigation is in place: yaml-only Dependabot opens version-update PRs only; the repo-level toggle is what gates security-advisory-driven PRs. Both are now armed.

**Verification method:** UI-only. GitHub does not currently expose this toggle via the public REST/GraphQL API, so an automated re-check is not possible — the user's confirmation is the authoritative signal per the plan's Task 2 specification.

## Dependabot.yml Verbatim Content

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    labels:
      - "dependencies"
      - "github-actions"
    commit-message:
      prefix: "ci"
      include: "scope"
```

## Acceptance Criteria — All Satisfied

| Criterion | Result |
| --------- | ------ |
| File `.github/dependabot.yml` exists | PASS |
| `grep -cE '^version: 2$' .github/dependabot.yml` returns 1 | PASS |
| `grep -cF 'package-ecosystem: "github-actions"' .github/dependabot.yml` returns 1 | PASS |
| `grep -cF 'directory: "/"' .github/dependabot.yml` returns 1 | PASS |
| `grep -cF 'interval: "weekly"' .github/dependabot.yml` returns 1 | PASS |
| `grep -cF 'day: "monday"' .github/dependabot.yml` returns 1 | PASS |
| `grep -cF 'prefix: "ci"' .github/dependabot.yml` returns 1 | PASS |
| `grep -cF 'package-ecosystem: "pip"' .github/dependabot.yml` returns 0 (D-07) | PASS |
| Python `yaml.safe_load()` round-trip + structural asserts | PASS |
| `make test` exits 0 at 316/316, 100% coverage | PASS |
| `git log -1 --pretty=%s` matches `^ci: enable Dependabot for github-actions ecosystem$` | PASS |
| Subject + body lines all <= 78 chars | PASS (subject 50; max body line 63) |
| Commit body contains literal `Dependabot security updates` (single line) | PASS (line 18) |
| Commit body contains literal `MUST also be ENABLED` (single line) | PASS (line 18) |
| `[ci]` Enable Dependabot entry in CHANGELOG `## 3.0.15 - DEVELOPMENT` Misc | PASS |
| Task 2 human-verify resume signal: toggle ON | PASS (user-confirmed) |

## Decisions Made

- **Atomic single-commit fold (dependabot.yml + CHANGELOG):** Same D-17 author's-discretion pattern Plan 04 used. Both edits are the same concern (enable Dependabot + record in changelog) — bisectable, single CHANGELOG entry, single feature-grain commit.
- **Body wording rewrite to keep the dual-gate literals on a single line:** The plan's spec body wrapped at 78 chars naturally split "Dependabot security / updates" across two lines, which would defeat the acceptance grep that searches for the literal phrase via single-line `grep -F`. Body was rephrased so `the "Dependabot security updates" toggle MUST also be ENABLED` sits on one line. The full meaning is preserved (RESEARCH.md Correction 2 + Pitfall 6 still cited; Settings path still cited; Task 2 still cited). One amend was used to land the corrected body on the single atomic `ci:` commit per the plan's "1 atomic commit" requirement.
- **Continuation-agent re-execution from clean base:** The prior worktree (agent-aefc699d9a5ffc12f) was removed without merging and its commits never landed. This fresh worktree re-executed Plan 06 from base `878f0701` per the orchestrator's prompt. No work was lost — Plan 06 had only reached the Task 2 checkpoint in the prior session.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 — Acceptance-grep correctness] Reworded commit body so dual-gate literals sit on a single line**
- **Found during:** Task 1 (post-commit acceptance verification)
- **Issue:** The plan's recommended body wording wrapped at 78 chars naturally split "Dependabot security / updates" across two lines, which defeats the acceptance grep `git log -1 --format=%b | grep -F 'Dependabot security updates'` (single-line match). Without this fix, Task 1's automated acceptance gate would have failed despite the body containing the phrase across two lines.
- **Fix:** Amended the just-made commit body to rephrase the NOTE block so `the "Dependabot security updates" toggle MUST also be ENABLED` sits on one body line (line 18). Full meaning preserved (RESEARCH.md Correction 2 + Pitfall 6 still cited, Settings path still cited, Task 2 still cited).
- **Files modified:** None (commit body only)
- **Verification:** `git log -1 --format=%b | grep -nF 'Dependabot security updates'` returns line 18 match; `grep -nF 'MUST also be ENABLED'` returns line 18 match (same line — even better; both literals on one line). All body lines still <= 78 chars (max 63).
- **Committed in:** `dfb9abba` (amended in place; the plan requires a single atomic commit so amend was the only way to keep the acceptance criteria satisfied without splitting into two commits)

**Total deviations:** 1 auto-fixed (Rule 1 — body-wording correctness)
**Impact on plan:** No scope creep. The amend was strictly to preserve the plan's own acceptance criteria; semantic content is unchanged. The commit remains a single atomic `ci:` commit as the plan requires.

## Issues Encountered

- **Fresh worktree venv not pre-bootstrapped:** PDM's first `pdm run python -c '...'` failed because the worktree's `.venv` was not initialized (virtualenv module missing in the system Python). Resolved by running `make init` (per MEMORY.md note: `make init` rebuilds devbox + venv before any PDM internals). Same issue Plan 04's executor encountered in its worktree — pattern now documented in user memory.

## Threat Model Disposition

| Threat ID | Disposition | Status After This Plan |
| --------- | ----------- | ---------------------- |
| T-02-06-01 (Information disclosure / unpatched-CVE persists indefinitely) | mitigate | RESOLVED — yaml enables version-update PRs; repo toggle (verified ON) enables security-CVE PRs |
| T-02-06-02 (Tampering — Dependabot PRs run untrusted upstream code) | accept | ACCEPTED — standard PR review process gates merge; build_and_test.yml CI runs on Dependabot PRs before any merge |
| T-02-06-03 (EoP — misconfigured `directory: "/"`) | accept | ACCEPTED — yaml round-trip + grep checks confirm canonical setting |
| T-02-06-04 (Tampering — yaml-only false-sense-of-security if toggle off) | mitigate | RESOLVED — Task 2 human-verify confirms toggle ON; commit body documents the requirement so it's not lost when planning artifacts age out |

## Self-Check

Verifying claimed work exists:

**Files:**
- `[FOUND]` `.github/dependabot.yml` (created — Dependabot v2 schema; ecosystem `github-actions`; weekly Monday; labels `dependencies` + `github-actions`; prefix `ci`; no `groups`; no `pip`)
- `[FOUND]` `CHANGELOG.md` (modified — `[ci] Enable Dependabot for github-actions ecosystem (weekly)` entry in `## 3.0.15 - DEVELOPMENT` Misc bucket)
- `[FOUND]` `.planning/phases/02-dependencies-ci-pipeline/02-06-SUMMARY.md` (this file — about to be committed)

**Commits:**
- `[FOUND]` `dfb9abba` (`ci: enable Dependabot for github-actions ecosystem` — body contains literal `Dependabot security updates` AND `MUST also be ENABLED` on a single line; subject + all body lines <= 78 chars)

**Acceptance criteria:** All PASS as documented in the table above.

**Task 2 (human-verify) result:** User confirmed: Dependabot security updates toggle is already ON / turned ON at https://github.com/datafolklabs/cement/settings/security_analysis. Pitfall 6 mitigation in place; Plan 04 exact-tag pinning + Plan 06 yaml + this toggle = full CI-05 backstop active.

## Self-Check: PASSED

## Next Phase Readiness

- **Plan 07 (workflow_dispatch trigger on pdm.yml):** Modifies the `on:` block of `pdm.yml`, not the Action invocations or any Dependabot-watched surface. No merge conflict risk with this plan.
- **Plan 08 (phase acceptance verification):** Re-runs the CI-05 acceptance: Action versions exact-tag-pinned (Plan 04) + Dependabot watching them (this plan) + repo-level security-updates toggle ON (verified). All three legs of CI-05 are now in place; Plan 08 will validate end-to-end.
- **Observe-and-triage window:** First Dependabot PRs will land within ~7 days post-merge if any pinned Action has a newer release (Plan 04 verified releases live 2026-05-02; some are likely to ship a patch within a week). PR triage follows Phase 4 labeling conventions (`dependencies` + `github-actions`).

No blockers. Phase 2 Plan 07 is unblocked and ready to execute.

---
*Phase: 02-dependencies-ci-pipeline*
*Plan: 06*
*Completed: 2026-05-03*
