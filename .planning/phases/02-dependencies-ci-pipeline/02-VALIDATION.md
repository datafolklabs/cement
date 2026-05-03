---
phase: 2
slug: dependencies-ci-pipeline
status: draft
nyquist_compliant: false
wave_0_complete: true
created: 2026-05-02
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.0.3 + pytest-cov 7.1.0 + coverage 7.13.5 |
| **Config file** | `pyproject.toml` (no `.coveragerc` — coverage auto-discovers pyproject) |
| **Quick run command** | `pdm run pytest --cov=cement -x tests` |
| **Full suite command** | `make test` (runs `make comply` then `pdm run pytest --cov=cement tests`) |
| **Estimated runtime** | ~30s quick, ~60s full (locally) |

---

## Sampling Rate

- **After every task commit:** Run `pdm run pytest --cov=cement -x tests` plus `make comply-ruff` and `make comply-mypy`
- **After every plan wave:** Run `make test` (full suite + 100% gate)
- **Before `/gsd-verify-work`:** `make test` green locally + PR triggers all 7 matrix lanes green on GitHub Actions
- **Max feedback latency:** ~60 seconds local; CI matrix run is the integration-layer probe

---

## Per-Task Verification Map

Phase 2 modifies config files (`pyproject.toml`, `.github/workflows/*.yml`, `.github/dependabot.yml`, `pdm.lock`) — not application code. Coverage is provided by the existing test suite (proves nothing regresses under the bumped lockfile) plus structural checks (grep / yaml-lint / `gh workflow run`).

| Task ID (placeholder) | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 02-01-* | 01 (lockfile refresh) | 1 | DEPS-01, DEPS-02 | — | bumped lockfile installs cleanly + full suite green | smoke + unit | `pdm install && make test` | ✅ | ⬜ pending |
| 02-02-* | 02 (pip-audit spot-check) | 1 | DEPS-03 | — | pip-audit output captured; any unpatched runtime CVE pinned-around or documented | manual | `pdm run python -m pip install pip-audit && pdm run pip-audit` | ✅ (after ad-hoc install) | ⬜ pending |
| 02-03-* | 03 (Action exact-tag pins) | 2 | CI-05 | — | every Action pinned to current stable tag | static | `grep -rn "@v[0-9]\+$\|@main\|@master" .github/workflows/` returns zero lines | ✅ (grep) | ⬜ pending |
| 02-04-* | 04 (Dependabot config) | 2 | CI-05 (CVE backstop) | — | `.github/dependabot.yml` parses; opens PRs on Action bumps | static + manual | `yamllint .github/dependabot.yml` (or in-place ymllint via Action); confirm repo-level "Dependabot security updates" toggle is ON | ✅ | ⬜ pending |
| 02-05-* | 05 (`workflow_dispatch:` on pdm.yml) | 2 | DEPS-04 | — | `gh workflow run pdm.yml` from main completes without wall-of-lint | manual | `gh workflow run pdm.yml --ref main && gh run watch` | manual-only | ⬜ pending |
| 02-06-* | 06 (matrix add pypy-3.11 + drop FIXME) | 2 | CI-01 | — | matrix has 7 lanes; pypy-3.11 lane green; FIXME comment gone | integration + static | PR triggers all 7 lanes green; `grep -n "FIXME ?" .github/workflows/build_and_test.yml` returns nothing | ✅ | ⬜ pending |
| 02-07-* | 07 (coverage gate wiring) | 1 | CI-03 | — | gate fires below 100% | unit + manual | `pdm run pytest --cov=cement tests` exits 0 at 100%; temporarily comment a covered line, expect non-zero exit; restore line | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

> Plan and task IDs are placeholders — gsd-planner assigns the canonical IDs. The map above
> shows the **verification surface** per requirement so the planner can wire `acceptance_criteria`
> directly to grep/test commands.

---

## Wave 0 Requirements

- [x] No new test files needed — existing `tests/` suite covers all phase requirements (Phase 2 changes config, not application code)
- [x] No new framework install — pytest/pytest-cov/coverage already in `[dependency-groups].dev`
- [x] No new fixtures — existing `tests/conftest.py` covers existing surface

*Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `workflow_dispatch` trigger of `pdm.yml` runs cleanly | DEPS-04 | Requires PR merged to main; only main-branch workflow triggers can be dispatched | After phase PR merges: `gh workflow run pdm.yml --ref main && gh run watch <run-id>`. Expect either no PR opened (baseline already current — passing) or PR opened with proposed updates (also passing). FAIL = wall-of-lint failure mode the cron previously hit. |
| 100% coverage gate fires below 100% | CI-03 | Need to demonstrate gate triggers on regression; can't (and shouldn't) ship a broken-coverage commit to main | Locally: comment out one covered line in `cement/core/foundation.py`, run `make test`, confirm non-zero exit + clear "FAIL Required test coverage of 100% not reached" message. Restore the line. Capture the failing-output snippet in commit body or PR description. |
| Repo-level "Dependabot security updates" toggle enabled | CI-05 (CVE backstop, complement to D-07 yaml) | yaml-only Dependabot opens version-update PRs; security-advisory-driven PRs require the repo-level toggle (cannot be set from yaml) | After Dependabot config commit lands: visit `https://github.com/datafolklabs/cement/settings/security_analysis`, confirm "Dependabot security updates" is enabled. Note state in the commit body or phase verification artifact. |
| `02-PIP-AUDIT.md` exists with output | DEPS-03 | Output is generated artifact, not derivable from CI alone | Run `pdm run python -m pip install pip-audit && pdm run pip-audit` (text output); commit captured output to `.planning/phases/02-dependencies-ci-pipeline/02-PIP-AUDIT.md` with date header and any per-CVE rationale lines. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or are listed under "Manual-Only Verifications" above (with rationale)
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references (n/a — no new tests required this phase)
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s locally
- [ ] `nyquist_compliant: true` set in frontmatter (set by gsd-planner after task IDs are wired)

**Approval:** pending
