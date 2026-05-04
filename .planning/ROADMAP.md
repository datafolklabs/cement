# Roadmap: Cement 3.0.16 — Clean & Green

## Overview

This roadmap delivers Cement 3.0.16, a maintenance/modernization release on the strict no-public-API-breakage 3.0.x track. The journey starts by unblocking the baseline (current ruff/mypy/pytest tooling, drop Python 3.9), then resumes the stalled `pdm update` pipeline and gets the CI matrix green. From a green baseline we run an internal-only refactor (cleanup, type tightening, pathlib, modern stdlib idioms) while holding the absolute 100% coverage gate. In parallel, the GitHub issue backlog is bulk-triaged with user approval. Late in the cycle we add `DeprecationWarning` surfaces (warn-only — removals defer to 3.2.0), refresh docs, and capture security-audit tooling as a stubbed backlog. The final phase cuts the 3.0.16 release: TestPyPI smoke test, tag, GitHub release, PyPI publish, and a post-release bump to 3.0.17 (next dev cycle).

**Cement 4 is unscoped and stays out of bounds for this milestone.** No phase introduces architectural seams, public API changes, or pre-work for a future rewrite.

**Quality gates that hold across every phase:** 100% test coverage, ruff clean, mypy clean.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [x] **Phase 1: Tooling Baseline & Python Matrix** - Bump ruff/mypy/pytest, drop 3.9, fix the lint/type fallout (completed 2026-04-30)
- [x] **Phase 2: Dependencies & CI Pipeline** - Refresh deps, unblock the `pdm update` Action, get the matrix green (completed 2026-05-02; D-19 #1 PR-CI-green and #3 post-merge workflow_dispatch deferred to live-CI verification — see 02-VERIFICATION.md)
- [ ] **Phase 3: Internal Refactor & Coverage Hardening** - Cleanup-only refactor under the 100% coverage gate
- [ ] **Phase 4: Backlog Triage** - Bulk-close stale issues with user approval, label and prioritize survivors
- [ ] **Phase 5: Deprecations, Docs & Security Stubs** - Add warn-only deprecations, refresh docs, capture audit-tooling backlog
- [ ] **Phase 6: Release Cut 3.0.16** - Changelog, TestPyPI smoke test, tag, GitHub release, PyPI publish, bump to 3.0.17

## Phase Details

### Phase 1: Tooling Baseline & Python Matrix
**Goal**: Bring ruff, mypy, and pytest tooling to current stable, drop Python 3.9, and clear all resulting lint/type errors so the rest of the work has a clean starting line.
**Depends on**: Nothing (first phase)
**Requirements**: TOOL-01, TOOL-02, TOOL-03, TOOL-04, PYVER-01, PYVER-02, PYVER-03
**Success Criteria** (what must be TRUE):
  1. `make comply-ruff` exits with status 0 against the latest stable ruff across `cement/` and `tests/`
  2. `make comply-mypy` exits with status 0 against the latest stable mypy with the project's strict configuration
  3. `make test` runs without deprecation warnings emitted by pytest, pytest-cov, or coverage themselves
  4. `pyproject.toml` declares `requires-python = ">=3.10"` and a `grep -rn "3\.9\|sys\.version_info.*9"` across `cement/` returns no compat shims
  5. Ruff and mypy rule sets are explicitly enumerated in `pyproject.toml` (no implicit defaults that drift on the next tool bump)
**Plans**: 4 plans
  - [x] 01-01-PLAN.md — Step 1: atomic Python 3.9 drop across all 9 files (D-05)
  - [x] 01-02-PLAN.md — Step 2a: ruff 0.15.12 bump + codification + 8 per-family fix commits
  - [x] 01-03-PLAN.md — Step 2b: mypy 1.20.2 bump + audit comment + union-attr fix
  - [x] 01-04-PLAN.md — Step 2c: pytest+pytest-cov+coverage floor bump

### Phase 01.1: Generated Project Template Build Modernization (INSERTED)

**Goal:** Restore `pip install .` on freshly-generated `cement generate project` outputs under pip's default PEP 517 build isolation by migrating the generate-project template from setuptools+setup.py to pdm-backend with a complete `[project]`-table-driven `pyproject.toml`. This unblocks the cli-smoke-test on the Python 3.10-3.14 matrix and clears Phase 2's CI-green prerequisite. (Re-scoped 2026-04-30 — original strict-minimum patch was empirically insufficient; see 01.1-CONTEXT.md revision_history.)
**Requirements**: (none — inserted urgent phase, no REQ-IDs assigned)
**Depends on:** Phase 1
**Plans:** 1/1 plans complete

Plans:
- [x] 01.1-01-PLAN.md — Migrate generate-project template to pdm-backend (6 atomic commits + verification); verify `make cli-smoke-test` green on Python 3.10-3.14

### Phase 2: Dependencies & CI Pipeline
**Goal**: Regenerate the lockfile against the new tooling baseline, refresh optional-extras to versions compatible with Python 3.10–3.14, and prove the GitHub Actions matrix is green end-to-end (including the previously stalled `pdm update` job).
**Depends on**: Phase 1
**Requirements**: DEPS-01, DEPS-02, DEPS-03, DEPS-04, CI-01, CI-02, CI-03, CI-05
**Success Criteria** (what must be TRUE):
  1. A fresh PR triggers GitHub Actions and all matrix jobs (Python 3.10, 3.11, 3.12, 3.13, 3.14) report green
  2. Compliance jobs (ruff, mypy) and the 100% coverage gate run on every PR and fail the build below 100%
  3. The scheduled `pdm update` workflow runs to completion against the new baseline without surfacing a wall of lint errors
  4. `pdm.lock` reflects current non-breaking versions of all extras (yaml, jinja2, mustache, colorlog, redis, memcached, watchdog, etc.) and `pip-audit`-style spot-check shows no unpatched runtime CVEs (or each is documented with rationale)
  5. All GitHub Action versions (checkout, setup-python, etc.) are pinned to current stable tags
**Plans**: 8 plans across 8 waves (linearized — CHANGELOG.md + workflow yaml file conflicts prevent wave-level parallelism; matches Phase 1 precedent)

  **Wave 1**
  - [x] 02-01-PLAN.md — `pdm update` lockfile refresh + atomic drift-fix follow-ups (D-01, D-04)

  **Wave 2** *(blocked on Wave 1 completion)*
  - [x] 02-02-PLAN.md — pip-audit spot-check + 02-PIP-AUDIT.md artifact (D-03)
  - [x] 02-03-PLAN.md — Wire 100% coverage gate via fail_under + addopts + explicit [tool.coverage.run] (D-10/D-11/D-12/D-13)

  **Wave 3** *(blocked on Wave 2 completion)*
  - [x] 02-04-PLAN.md — Pin every GitHub Action to exact tags across both workflows (D-05; D-06 deviation: use @v1.12 per RESEARCH.md Correction 1)

  **Wave 4** *(blocked on Wave 3 completion)*
  - [x] 02-05-PLAN.md — Add pypy-3.11 to test matrix + drop FIXME OS-matrix comment (D-14, D-15)

  **Wave 5** *(blocked on Wave 4 completion)*
  - [x] 02-06-PLAN.md — Enable Dependabot for github-actions ecosystem + verify repo-level security-updates toggle (D-07; RESEARCH.md Correction 2)

  **Wave 6** *(blocked on Wave 5 completion)*
  - [x] 02-07-PLAN.md — Add workflow_dispatch trigger to pdm.yml (D-08)

  **Wave 8** *(blocked on Waves 1–6 completion — final acceptance gate; wave 7 intentionally skipped)*
  - [x] 02-08-PLAN.md — Phase 2 acceptance verification: PR-CI green + workflow_dispatch run clean + 02-VERIFICATION.md (D-19) [D-19 #1 and #3 deferred to post-PR / post-merge — recorded PENDING in VERIFICATION.md]

  **Cross-cutting constraints** *(applies to every plan)*
  - 100% coverage gate must remain green after each plan's changes (sampling: `pdm run pytest --cov=cement -x tests` per task; `make test` per wave)
  - All commits follow Conventional Commits + 78-char wrap (CLAUDE.md §"Commit Conventions")
  - CHANGELOG.md `## 3.0.16 - DEVELOPMENT` updated phase-by-phase per CLAUDE.md §"Changelog Maintenance"
  - No public-API breakage on the 3.0.x track (PROJECT.md Constraints)

### Phase 3: Internal Refactor & Coverage Hardening
**Goal**: Run a cleanup-only internal refactor (dead code, type-hint tightening, `pathlib`, modern stdlib idioms) without changing any public signature, and audit coverage exclusions so the 100% gate is meaningful, not papered over.
**Depends on**: Phase 2
**Requirements**: REFACTOR-01, REFACTOR-02, REFACTOR-03, REFACTOR-04, COV-01, COV-02, COV-03
**Success Criteria** (what must be TRUE):
  1. `make test` produces a 100% coverage report on the refactored tree with zero drift from prior baseline
  2. `coverage-report/` HTML generates without warnings and every remaining `pragma: no cover` line has an inline comment justifying the exclusion
  3. A diff of public symbols (module-level + class public methods) between `main` and the refactor branch is empty — no signatures changed, no exports added or removed
  4. mypy strict mode reports fewer `Any` occurrences in `cement/core/` than the pre-refactor baseline (concrete number captured in the phase summary)
  5. `os.path` usage in `cement/utils/fs.py` and core internals is migrated to `pathlib` where it doesn't change a public signature; remaining `os.path` callsites are explicitly documented as boundary-preserving
**Plans**: 8 plans across 8 waves (sequential due to file-ownership invariants — UP-family auto-fixes must precede FA strip per D-08; pathlib migration is atomic per-file per D-13; pragma audit lands AFTER refactor commits per D-18)

  **Wave 1**
  - [x] 03-01-PLAN.md — Capture public API baseline (D-04 audit gate; permanent dev affordance per D-05) — committed f10f8ce3

  **Wave 2** *(blocked on Wave 1)*
  - [x] 03-02-PLAN.md — Re-enable ruff UP+FA family in extend-select with refreshed AUDIT POINT comment (D-06)

  **Wave 3** *(blocked on Wave 2)*
  - [x] 03-03-PLAN.md — UP-family auto-fixes (UP006/UP007/UP045/UP031/UP032 + UP004/UP008/UP015/UP024/UP025/UP026/UP028/UP035) + CONVENTIONS.md PEP 604/585 refresh (D-07, D-19, RESEARCH.md A5) — 16 atomic commits, REFACTOR-04 closed, D-19 protected callsites verified untouched

  **Wave 4** *(blocked on Wave 3 — UP must precede FA per D-08)*
  - [x] 03-04-PLAN.md — Strip `from __future__ import annotations` from cement/ via FA100 (D-08)

  **Wave 5** *(blocked on Wave 4)*
  - [x] 03-05-PLAN.md — Capture Any-baseline in 03-VERIFICATION.md + tighten Any in cement/core/ (D-09 — `2f3a063f` records pre-counts Any=41/pragma=141/pathlib=33; `6365a6c7` tightens 2 sites: `App.__import__(obj: Any)` → `obj: str` and `_dispatch() -> Any | None` → `-> Any`; 41 → 40 substantive delta; D-24 conjunct #6 GREEN; inline D-09 justifications added to all 40 surviving sites)

  **Wave 6** *(blocked on Wave 5; A7 symlink pre-flight first)*
  - [ ] 03-06-PLAN.md — pathlib migration: utils/fs.py, core/config.py, core/foundation.py, core/template.py — atomic per-file per D-13; D-12 boundary preserved; D-19 protected callsites untouched

  **Wave 7** *(blocked on Wave 6)*
  - [ ] 03-07-PLAN.md — pragma:nocover audit with D-15 locked vocabulary (per-file commits across approx 39 files per RESEARCH.md A4: 141 sites, not 123)

  **Wave 8** *(blocked on Wave 7 — final acceptance gate)*
  - [ ] 03-08-PLAN.md — Finalize 03-VERIFICATION.md with full D-24 9-conjunct evidence + mark Phase 3 complete in ROADMAP

  **Cross-cutting constraints** *(applies to every plan)*
  - 100% coverage gate must remain green after each commit (Phase 2 D-10/D-11/D-12)
  - All commits follow Conventional Commits + 78-char wrap (CLAUDE.md)
  - CHANGELOG.md `## 3.0.16 - DEVELOPMENT` updated phase-by-phase per CLAUDE.md
  - No public-API breakage on the 3.0.x track — `make audit-public-api` exit 0 enforced byte-for-byte across every commit (D-04 / D-24 conjunct #4)

### Phase 4: Backlog Triage
**Goal**: Bring the GitHub issue backlog to a known clean state via user-approved bulk triage, with surviving issues consistently labeled and any real bugs surfaced as either in-milestone fixes or explicitly deferred backlog items.
**Depends on**: Phase 2 (CI green so triage decisions are not contaminated by tooling noise; can run in parallel with Phase 3)
**Requirements**: TRIAGE-01, TRIAGE-02, TRIAGE-03, TRIAGE-04
**Success Criteria** (what must be TRUE):
  1. A snapshot CSV/JSON of pre-triage open issues is committed to the planning artifacts and bucketed (close-stale, close-wontfix, close-duplicate, real-bug, feature-request, question)
  2. Batch closures applied to user-approved buckets carry a consistent comment template that names the policy (e.g., "closing per Cement 3.0.16 stale-issue policy")
  3. Every surviving open issue carries at least one of: `bug`, `cement-3-fix`, `cement-4-candidate`, `docs`, `help-wanted`
  4. Real bugs identified during triage are either fixed in this milestone (with PR linked) or recorded as a backlog item with explicit deferral rationale
**Plans**: TBD

### Phase 5: Deprecations, Docs & Security Stubs
**Goal**: Land warn-only `DeprecationWarning` surfaces flagged for removal in 3.2.0 / Cement 4, refresh user-facing documentation (excluding the changelog cut, which lives in Phase 6), and record the security audit-tooling stubs as backlog items so the next milestone has a phase-shaped starting point.
**Depends on**: Phase 3 (refactor surfaces what should be deprecated; can run in parallel with Phase 4)
**Requirements**: DEPREC-01, DEPREC-02, DEPREC-03, DOCS-01, DOCS-02, DOCS-04, SEC-01, SEC-02, SEC-03
**Success Criteria** (what must be TRUE):
  1. Every newly deprecated surface emits `DeprecationWarning` with migration guidance in the message; running the test suite under `-W error::DeprecationWarning` against a fixture that exercises the deprecated path fails with the expected warning text
  2. Each new deprecation is documented in `docs/source/deprecations.rst` and the test suite asserts the warning fires (so the 3.2.0 removal has a concrete failing test as its trigger)
  3. `make docs` builds Sphinx docs with zero warnings and no broken cross-references; README and CONTRIBUTING walkthroughs run end-to-end against the 3.0.16 development tree without errors
  4. Public API docstrings have been swept for staleness — examples that don't run are corrected or removed (a sampling round-trip on representative examples passes)
  5. SEC-01/02/03 backlog items exist (issues or planning entries) with phase-shaped scope notes for `pip-audit`, `bandit`, and CodeQL/Semgrep — sufficient for a future milestone to pick up without re-discovery
**Plans**: TBD

### Phase 6: Release Cut 3.0.16
**Goal**: Cut the 3.0.16 release: finalize the changelog, validate the release workflow against TestPyPI, tag, publish to PyPI, and bump the dev version to 3.0.17 per odd/even convention.
**Depends on**: Phase 5 (and gates on Phases 1–4 being complete; release does not cut while any prior phase is open)
**Requirements**: DOCS-03, CI-04, REL-01, REL-02, REL-03, REL-04, REL-05
**Success Criteria** (what must be TRUE):
  1. The changelog entry for 3.0.16 enumerates all user-visible changes (deprecations added, dep bumps, Python matrix change to 3.10–3.14, refactor highlights at a non-API-breaking level)
  2. A pre-release upload to TestPyPI installs cleanly on Python 3.10, 3.11, 3.12, 3.13, and 3.14, and a minimal `App().run()` round-trip succeeds on each
  3. `cement/__init__.py`, `pyproject.toml`, and any other version-of-record locations all read `3.0.16` at tag time and `3.0.17` immediately after
  4. The `3.0.16` git tag exists, the GitHub release page is published with the changelog body, and `pip install cement==3.0.16` from PyPI succeeds on a clean venv
  5. The release workflow itself (not just the artifacts) ran end-to-end without manual intervention beyond the user-approved publish step
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6. Phases 3 and 4 are independent and parallelization-eligible once Phase 2 completes; Phase 5 can begin in parallel with Phase 4 once Phase 3 lands.

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Tooling Baseline & Python Matrix | 4/4 | Complete   | 2026-04-30 |
| 2. Dependencies & CI Pipeline | 0/TBD | Not started | - |
| 3. Internal Refactor & Coverage Hardening | 4/8 | In Progress | - |
| 4. Backlog Triage | 0/TBD | Not started | - |
| 5. Deprecations, Docs & Security Stubs | 0/TBD | Not started | - |
| 6. Release Cut 3.0.16 | 0/TBD | Not started | - |

---
*Roadmap created: 2026-04-24*
*Coverage: 42/42 v1 requirements mapped*
