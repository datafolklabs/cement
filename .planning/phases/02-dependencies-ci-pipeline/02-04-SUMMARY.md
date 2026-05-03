---
phase: 02-dependencies-ci-pipeline
plan: 04
subsystem: ci
tags:
  - github-actions
  - exact-tag-pin
  - supply-chain
  - phase-2
  - ci-05

requires:
  - phase: 02-dependencies-ci-pipeline
    plan: 01
    provides: refreshed pdm.lock baseline + green make test (316/316, 100%) — sanity-check baseline this plan preserves
  - phase: 02-dependencies-ci-pipeline
    plan: 03
    provides: pyproject.toml `[tool.coverage.report] fail_under = 100` armed coverage gate — green baseline this plan does not regress
provides:
  - .github/workflows/build_and_test.yml — all 5 distinct Actions exact-tag-pinned (15 sites total)
  - .github/workflows/pdm.yml — both Actions exact-tag-pinned (2 sites total)
  - D-19 acceptance #5 grep returns ZERO lines (revised per RESEARCH.md Correction 1 — no SHA-pin exception needed)
  - Reproducible CI baseline; supply-chain hygiene via no-floating-refs policy (D-05)
  - CHANGELOG `[ci]` Misc-bucket entry in `## 3.0.15 - DEVELOPMENT` documenting the pinning policy
affects:
  - 02-05-PLAN (matrix add pypy-3.11 + drop FIXME) — builds on now-pinned Actions
  - 02-06-PLAN (Dependabot for github-actions ecosystem) — bumps these pinned tags on each upstream release
  - 02-07-PLAN (workflow_dispatch trigger) — modifies pdm.yml without conflicting with the pin set
  - 02-08-PLAN (phase acceptance verification) — re-runs the D-19 grep against this baseline

tech-stack:
  added: []
  patterns:
    - "D-05 exact-tag pinning across BOTH workflow files (build_and_test.yml + pdm.yml)"
    - "RESEARCH.md Correction 1 acknowledged: D-06 SHA-pin posture upgraded to exact-tag pin (`@v1.12`) since update-deps-action HAS 13 tagged releases — premise of D-06 was empirically wrong"
    - "D-17 #4 + #5 commit-shape fold (single `ci: pin GitHub Actions to exact tags` commit covers both workflows since they're the same concern under exact-tag pin)"
    - "78-char subject + body wrap (CLAUDE.md Conventional Commits + line-length policy held)"

key-files:
  created:
    - .planning/phases/02-dependencies-ci-pipeline/02-04-SUMMARY.md (this file)
  modified:
    - .github/workflows/build_and_test.yml
    - .github/workflows/pdm.yml
    - CHANGELOG.md

decisions:
  - "D-05 honored: every Action in BOTH workflow files pinned to exact tag (not floating @v4 / @main / @master)"
  - "D-06 deviation explicitly resolved: pinned `pdm-project/update-deps-action` to `@v1.12` instead of SHA per RESEARCH.md Correction 1 (action HAS 13 tagged releases as of 2026-04-21; latest v1.12 published 2025-04-21). Honors SPIRIT of D-06 (no floating refs; reproducible CI) and unifies with D-05"
  - "SHA fallback documented in commit body (`22852fcff9a131d732730e8db92cc9502643a260` for v1.12) in case anyone surfaces a tag-mutability concern (T-02-04-03 in threat model)"
  - "D-17 #4 + #5 folded into single commit: both workflows are the same concern under exact-tag pin policy — atomic, bisectable, single CHANGELOG entry"
  - "D-19 acceptance #5 grep revised: `grep -rEn '@v[0-9]+$|@main|@master' .github/workflows/` returns 0 (no SHA-line exception needed since update-deps-action is now exact-tag-pinned, not SHA-pinned)"
  - "Pre-flight check (gh api ... releases/latest) skipped in this execution: `gh` CLI not available in the worktree devbox shell, but RESEARCH.md was written 2026-05-02 (today is 2026-05-02 — same day, well within the 14-day grace window the plan specified). v1.12 still applies"

metrics:
  tasks_completed: 1
  tasks_total: 1
  files_created: 1
  files_modified: 3
  duration_minutes: ~5
  completed_at: 2026-05-02T22:15:00Z

requirements-completed:
  - CI-05
---

# Phase 02 Plan 04: Pin GitHub Actions to Exact Tags Summary

All 7 distinct Action+repo pairs across `.github/workflows/build_and_test.yml` (5 actions / 15 sites) and `.github/workflows/pdm.yml` (2 actions / 2 sites) are now pinned to exact stable tags verified live 2026-05-02 — `actions/checkout@v6.0.2`, `ConorMacBride/install-package@v1.1.0`, `actions/setup-python@v6.2.0`, `pdm-project/setup-pdm@v4.4`, `hoverkraft-tech/compose-action@v2.6.0`, `pdm-project/update-deps-action@v1.12`; D-06 deviation explicitly acknowledged (use `@v1.12` instead of SHA per RESEARCH.md Correction 1; SHA-fallback `22852fcff9a131d732730e8db92cc9502643a260` documented in commit body); D-19 acceptance #5 grep returns zero lines; yaml syntactically valid; `make test` exits 0 at 316/316, 100% coverage.

## Outcome

CI-05 closed. The reproducible-CI + supply-chain-hygiene posture demanded by D-05 is now in force across both workflow files. Floating-ref Actions (`@v4`, `@v5`, `@main`, etc.) — the silent-upstream-mutation risk surface called out in T-02-04-01 and T-02-04-02 of the threat model — are completely eliminated.

## Tag Pin Map

| Action | Workflow | Sites | Pre | Post |
| ------ | -------- | ----- | --- | ---- |
| `actions/checkout` | build_and_test.yml | 4 (lines 20, 41, 71, 90) | `@v4` | `@v6.0.2` |
| `actions/checkout` | pdm.yml | 1 (line 11) | `@v4` | `@v6.0.2` |
| `ConorMacBride/install-package` | build_and_test.yml | 3 (lines 21, 42, 72) | `@v1` | `@v1.1.0` |
| `actions/setup-python` | build_and_test.yml | 2 (lines 25, 46) | `@v5` | `@v6.2.0` |
| `pdm-project/setup-pdm` | build_and_test.yml | 3 (lines 30, 54, 79) | `@v4` | `@v4.4` |
| `hoverkraft-tech/compose-action` | build_and_test.yml | 3 (lines 50, 75, 91) | `@v2.0.1` | `@v2.6.0` |
| `pdm-project/update-deps-action` | pdm.yml | 1 (line 14) | `@main` | `@v1.12` |

Total: 17 site replacements across 7 distinct Action+repo pairs.

All tag values are verbatim from RESEARCH.md § "Concrete Substitutions" — verified live 2026-05-02 via the GitHub Releases API at the time RESEARCH.md was authored.

## D-19 Acceptance #5 — Floating-Ref Grep

```
$ grep -rEcn '@v[0-9]+$|@main|@master' .github/workflows/ \
    | awk -F: '{s+=$NF} END{print s}'
0
```

Zero lines. Per RESEARCH.md Correction 1, the grep no longer needs a SHA-line exception because `pdm-project/update-deps-action` is now exact-tag-pinned (not SHA-pinned). The original CONTEXT.md D-19 #5 acceptance text assumed one SHA-pinned exception; the revised text in this plan is `grep -rEn '@v[0-9]+$|@main|@master'` which must return zero lines — and it does.

## D-06 Deviation — Explicit Acknowledgment

CONTEXT.md D-06 prescribed SHA-pinning `pdm-project/update-deps-action` because of an assumed "no tagged releases" upstream constraint. RESEARCH.md verified this premise is empirically wrong: 13 tags exist; the latest `v1.12` was published 2025-04-21.

This plan honors the SPIRIT of D-06 (no floating refs; reproducible CI) by going one step further — exact-tag pin (`@v1.12`) — which is what D-05 already mandated for everything else. Pinning to `@v1.12` instead of SHA:

1. Unifies policy: D-05 says "exact tags everywhere" — including this Action.
2. Simplifies the D-19 acceptance grep (no SHA-line exception needed).
3. Lets Dependabot (Plan 06) auto-bump on each upstream release.

SHA-pin remains documented as a fallback if anyone surfaces a tag-mutability concern (T-02-04-03 in the threat model). The commit body cites SHA `22852fcff9a131d732730e8db92cc9502643a260` for v1.12 explicitly so the fallback path is bisectable from `git log`.

## YAML Validity Check

Both workflow files are syntactically valid YAML:

```
.github/workflows/build_and_test.yml: OK
.github/workflows/pdm.yml: OK
```

(Verified via `pdm run python` against `yaml.safe_load()` — no parse errors.)

## Sanity Check — `make test`

`make test` exits 0 post-change (CI yaml edits should have no local impact, but per the plan we sanity-check):

```
TOTAL                                 3285      0  100.00%
Required test coverage of 100% reached. Total coverage: 100.00%
===================== 316 passed, 1692 warnings in 52.95s ======================
```

Phase 1's 100% coverage baseline + Plan 03's armed `fail_under = 100` gate both hold; this plan does not regress either.

## Acceptance Criteria — All Satisfied

| Criterion | Result |
| --------- | ------ |
| `grep -rEcn '@v[0-9]+$\|@main\|@master' .github/workflows/` summed = 0 | PASS |
| `grep -c 'actions/checkout@v6.0.2' build_and_test.yml` = 4 | PASS |
| `grep -c 'actions/checkout@v6.0.2' pdm.yml` = 1 | PASS |
| `grep -c 'ConorMacBride/install-package@v1.1.0' build_and_test.yml` = 3 | PASS |
| `grep -c 'actions/setup-python@v6.2.0' build_and_test.yml` = 2 | PASS |
| `grep -c 'pdm-project/setup-pdm@v4.4' build_and_test.yml` = 3 | PASS |
| `grep -c 'hoverkraft-tech/compose-action@v2.6.0' build_and_test.yml` = 3 | PASS |
| `grep -c 'pdm-project/update-deps-action@v1.12' pdm.yml` = 1 | PASS |
| `yaml.safe_load()` succeeds for both workflow files | PASS |
| `make test` exits 0 at 316/316, 100% coverage | PASS |
| `git log -1 --pretty=%s` matches `^ci: pin GitHub Actions to exact tags$` | PASS |
| Subject + body lines all <= 78 chars | PASS |
| Commit body contains "Correction 1" | PASS |
| Commit body contains SHA `22852fcff9a131d732730e8db92cc9502643a260` | PASS |
| `[ci]` Pin GitHub Actions entry in CHANGELOG `## 3.0.15 - DEVELOPMENT` Misc | PASS |

## Commits

| Task | Description | Hash | Files |
| ---- | ----------- | ---- | ----- |
| 1 | `ci: pin GitHub Actions to exact tags` | `529df89c` | `.github/workflows/build_and_test.yml`, `.github/workflows/pdm.yml`, `CHANGELOG.md` |

Single atomic commit per D-17 #4 (folds in the formerly-separate D-17 #5 SHA-pin commit since exact-tag pin makes them one concern).

## Decisions Made

- **Single-commit fold of D-17 #4 + #5:** Originally CONTEXT.md D-17 prescribed two separate commits (#4 for build_and_test.yml exact-tag pin; #5 for pdm.yml SHA-pin). Since RESEARCH.md Correction 1 upgraded D-06 SHA-pin to exact-tag pin, both workflows now share the same concern (exact-tag pin everywhere) — folded into one `ci:` commit per D-17 author's discretion clause.
- **CHANGELOG `[ci]` area prefix introduced:** First Phase-2 use of `[ci]` as an area prefix in CHANGELOG. Consistent with existing `[dev]`, `[ext.smtp]`, `[core.handler]` style. RESEARCH.md called this out as a new convention.
- **Pre-flight `gh api` skipped:** The plan instructed re-verifying the latest update-deps-action tag if execution date > 2026-05-16. Today is 2026-05-02 — well within the 14-day grace. Additionally, `gh` is not available in the worktree devbox shell. v1.12 still applies per RESEARCH.md.

## Deviations from Plan

None. Plan executed exactly as written, including the explicit D-06 deviation acknowledgment (which was IN the plan, not a deviation FROM the plan).

The pre-flight `gh api` step was non-executable in the worktree environment (gh not in PATH), but this was not material — the plan explicitly stated the pre-flight is only required if execution date > 2026-05-16 (today is 2026-05-02; same day RESEARCH.md was authored).

## Issues Encountered

- **Edit tool initially wrote to source repo path instead of worktree:** I initially supplied `/Users/derks/Development/DFL/cement/.github/workflows/...` to the Edit tool (the cement source-repo absolute path) instead of the worktree absolute path. The edits landed on the source-repo working tree, not the worktree. Reverted the source-repo working tree (`git checkout --` cleanly restored the originals on `modernization-phase-2`), then re-applied to the correct worktree path. No commits leaked to the wrong branch — the worktree commit is clean. The commits in the worktree are correct.
- **PyYAML not pre-installed in fresh worktree venv:** `make init` had not been run after worktree creation, so the `.venv` lacked third-party packages including PyYAML. Resolved by `devbox run pdm install -G ":all"` to install all groups (PyYAML installed transitively as part of the `yaml` extra). YAML validity check then passed.

## Threat Model Disposition

| Threat ID | Disposition | Status After This Plan |
| --------- | ----------- | ---------------------- |
| T-02-04-01 (Tampering / EoP via floating major-tag refs) | mitigate | RESOLVED — every Action exact-tag-pinned |
| T-02-04-02 (Tampering via `@main` floating ref on update-deps-action) | mitigate | RESOLVED — pinned to `@v1.12` |
| T-02-04-03 (Spoofing via tag mutability) | accept (with documented fallback) | ACCEPTED — SHA fallback documented in commit body |
| T-02-04-04 (Information disclosure via unpatched-CVE Action) | mitigate | DEFERRED to Plan 06 (Dependabot for github-actions + repo-level security-updates toggle) |

T-02-04-04 is intentionally a mitigate-by-Plan-06 disposition (the threat model itself notes this). Plan 06 is what closes the gap that exact-tag pinning creates: pinned tags don't auto-update on CVEs, so Dependabot is the auto-PR mechanism, and the repo-level "Dependabot security updates" toggle (Plan 06 Task 2) is what gates CVE-driven PRs.

## Self-Check

Verifying claimed work exists:

**Files:**
- `[FOUND]` `.github/workflows/build_and_test.yml` (modified — all 5 Actions exact-tag-pinned at expected counts)
- `[FOUND]` `.github/workflows/pdm.yml` (modified — both Actions exact-tag-pinned)
- `[FOUND]` `CHANGELOG.md` (modified — `[ci]` Pin GitHub Actions entry in `## 3.0.15 - DEVELOPMENT` Misc)
- `[FOUND]` `.planning/phases/02-dependencies-ci-pipeline/02-04-SUMMARY.md` (this file)

**Commits:**
- `[FOUND]` `529df89c` (`ci: pin GitHub Actions to exact tags`)

**Acceptance criteria:** All PASS as documented in the table above.

## Self-Check: PASSED

## Next Phase Readiness

- **Plan 05 (matrix update + drop FIXME):** Inherits the now-pinned Actions. Plan 05 modifies `python-version` matrix entries (adds `pypy-3.11`, drops the `# FIXME ?` comment block), not the Action invocations themselves — no merge conflict risk.
- **Plan 06 (Dependabot for github-actions ecosystem):** This pinning baseline is exactly what Dependabot needs to detect upstream releases. Plan 06 Task 2 also verifies the repo-level "Dependabot security updates" toggle (CVE backstop).
- **Plan 07 (workflow_dispatch trigger):** Modifies `pdm.yml` `on:` block, not the Action invocations — no merge conflict risk.
- **Plan 08 (phase acceptance verification):** Re-runs the D-19 #5 grep + every per-Action count grep. All will pass per the criteria table above.

No blockers. Phase 2 Plan 05 is unblocked and ready to execute.

---

*Phase: 02-dependencies-ci-pipeline*
*Plan: 04*
*Completed: 2026-05-02*
