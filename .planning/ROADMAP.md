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
- [x] **Phase 3: Internal Refactor & Coverage Hardening** - Cleanup-only refactor under the 100% coverage gate (completed 2026-05-04; all 9 D-24 conjuncts GREEN — see 03-VERIFICATION.md)
- [x] **Phase 4: Backlog Triage** - Bulk-close stale issues with user approval, label and prioritize survivors (completed 2026-05-05 via manual pass outside GSD; see 04-NOTE.md)
- [x] **Phase 5: Deprecations, Docs & Security Stubs** - Add warn-only deprecations, refresh docs, capture audit-tooling backlog (completed 2026-05-08; 12/12 must-haves verified — see 05-VERIFICATION.md)
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

  - [x] 03-06-PLAN.md — pathlib migration: utils/fs.py, core/config.py, core/foundation.py, core/template.py — atomic per-file per D-13; D-12 boundary preserved; D-19 protected callsites untouched

  **Wave 7** *(blocked on Wave 6)*

  - [x] 03-07-PLAN.md — pragma:nocover audit with D-15 locked vocabulary completed across 141 sites / 39 files. 39 per-file atomic source commits + 3 batch-summary docs(03) commits. Per-category breakdown: defensive: unreachable=51, abstract method=45, TYPE_CHECKING import=26, platform-specific=13, untestable: dynamic import=4, version constant=1, untestable: signal handler=1, total=141. D-24 conjunct #7 GREEN: locked-vocabulary inverse grep returns empty. NO D-16 vocabulary expansion triggered. 4 deviations auto-fixed inline (3 Rule 1, 1 Rule 2)

  **Wave 8** *(blocked on Wave 7 — final acceptance gate)*

  - [x] 03-08-PLAN.md — Finalize 03-VERIFICATION.md with full D-24 9-conjunct evidence + mark Phase 3 complete in ROADMAP — 03-VERIFICATION.md status: passed (9/9 GREEN); REFACTOR-01..04 + COV-01..03 SATISFIED; defense-in-depth reset (make superclean+init+test+comply+audit) all exit 0 against fresh caches

  **Wave 9** *(post-Wave-8 gap closure — verifier audit follow-up)*

  - [x] 03-09-PLAN.md — Close CR-01 + CR-02 (`cement.utils.fs:abspath` BC restoration: revert body to `os.path.abspath(os.path.expanduser(path))` with inline `# boundary: D-14 (CR-01/CR-02)` tag; +2 regression tests in `tests/utils/test_fs.py`) and WR-02 (`scripts/audit-public-api.py` `encoding='utf-8'`). 5 atomic commits; 9/9 D-24 conjuncts re-verified GREEN; test count 316 → 318 at 100.00% coverage; public-API baseline byte-identical; W-01/W-02 marked RESOLVED in 03-VERIFICATION.md

  **Cross-cutting constraints** *(applies to every plan)*

  - 100% coverage gate must remain green after each commit (Phase 2 D-10/D-11/D-12)
  - All commits follow Conventional Commits + 78-char wrap (CLAUDE.md)
  - CHANGELOG.md `## 3.0.16 - DEVELOPMENT` updated phase-by-phase per CLAUDE.md
  - No public-API breakage on the 3.0.x track — `make audit-public-api` exit 0 enforced byte-for-byte across every commit (D-04 / D-24 conjunct #4)

### Phase 4: Backlog Triage

**Goal**: Bring the GitHub issue backlog to a known clean state via user-approved bulk triage, with surviving issues consistently labeled and any real bugs surfaced as either in-milestone fixes or explicitly deferred backlog items.
**Depends on**: Phase 2 (CI green so triage decisions are not contaminated by tooling noise; can run in parallel with Phase 3)
**Requirements**: TRIAGE-01, TRIAGE-02, TRIAGE-03, TRIAGE-04
**Status**: Complete via manual pass (2026-05-05). Maintainer triaged the backlog directly against `github.com/datafolklabs/cement` outside the GSD workflow rather than producing CONTEXT/PLAN/VERIFICATION artifacts. See `.planning/phases/04-backlog-triage/04-NOTE.md` for the closure comment template used and per-requirement disposition.
**Success Criteria** (what must be TRUE):

  1. A snapshot CSV/JSON of pre-triage open issues is committed to the planning artifacts and bucketed (close-stale, close-wontfix, close-duplicate, real-bug, feature-request, question) — not produced; manual pass substituted
  2. Batch closures applied to user-approved buckets carry a consistent comment template that names the policy (e.g., "closing per Cement 3.0.16 stale-issue policy") — satisfied; template recorded in 04-NOTE.md
  3. Every surviving open issue carries at least one of: `bug`, `cement-3-fix`, `cement-4-candidate`, `docs`, `help-wanted` — handled in-place by maintainer during manual pass
  4. Real bugs identified during triage are either fixed in this milestone (with PR linked) or recorded as a backlog item with explicit deferral rationale — handled in-place during manual pass

**Plans**: None (manual completion)

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

**Plans**: 6 plans across 6 waves (linearized — CHANGELOG.md file conflicts force serial waves; matches Phase 2 precedent)

  **Wave 1**

  - [x] 05-01-PLAN.md — Tighten DEPRECATIONS registry + adjacent docstring sweep (commits 1, 2, 3 of D-16)

  **Wave 2** *(blocked on Wave 1 completion)*

  - [x] 05-02-PLAN.md — Resolve all 4 known sphinx warnings (commits 5, 6, 7, 8 of D-16)

  **Wave 3** *(blocked on Wave 2 completion)*

  - [x] 05-03-PLAN.md — Add top-level DEPRECATIONS.md mirroring GitBook narrative (commit 4 of D-16)

  **Wave 4** *(blocked on Waves 2 + 3 completion — sphinx clean is prerequisite for -W flip)*

  - [x] 05-04-PLAN.md — Wire -W into make docs + AUDIT POINT comment (commit 9 of D-16)

  **Wave 5** *(blocked on Wave 4 completion)*

  - [x] 05-05-PLAN.md — Drop Travis from README + align CONTRIBUTING with Conventional Commits + DOCS-04 sweep (commits 10, 11, optional 12 of D-16)

  **Wave 6** *(blocked on Wave 5 completion — final planning-artifact wave)*

  - [x] 05-06-PLAN.md — Sync CONVENTIONS.md ruff target-version + expand SECv2-01..03 with phase-shaped scope notes (commits 13, 14 of D-16; planning-artifact, NO CHANGELOG entries)

  **Cross-cutting constraints** *(applies to every plan)*

  - 100% coverage gate must remain green after each commit (Phase 2 D-10/D-11)
  - All commits follow Conventional Commits + 78-char wrap (CLAUDE.md)
  - CHANGELOG.md `## 3.0.15 - DEVELOPMENT` updated phase-by-phase per CLAUDE.md (commits 13 + 14 are planning-artifact and get NO CHANGELOG entry per RESEARCH.md Pitfall 7)
  - `make audit-public-api` exit 0 enforced byte-for-byte across every commit (Phase 3 D-04 / Phase 5 D-18 #3)
  - `make docs` (post-Wave 4) must exit 0 with -W enabled — zero warnings (Phase 5 D-09)

### Phase 05.4: GitHub Actions Release Workflow (INSERTED)

**Goal:** Replace the manual release checklist (issue #791) with a GitHub Actions–driven release workflow so that cutting a release becomes a tag push (or `workflow_dispatch`) instead of a cumbersome multi-day manual process that blocks active development. The workflow automates the full checklist: release gates (test matrix, coverage, compliance, Windows core tests, CLI smoke tests on Linux/macOS/Windows), PyPI distribution, Docker Hub multi-arch image builds, `stable/X.Y` version-branch sync, docs builds, GitHub Release publication, and release notifications. Pre-requisite for Phase 6 — the 3.0.16 Release Cut runs this workflow.
**Requirements**: CI-04, CI-05, REL-02, REL-03, REL-04, REL-05, DOCS-03 (this phase BUILDS the machinery; the requirement IDs themselves flip to complete in Phase 6, which RUNS the workflow)
**Depends on:** Phase 5
**Source:** https://github.com/datafolklabs/cement/issues/791 (3.0.16 Stable Release Tracker — the recurring manual checklist this phase automates)
**Success Criteria** (what must be TRUE):

  1. Pushing a release tag (or dispatching the workflow manually) runs all release gates automatically — full Python test matrix with 100% coverage, ruff/mypy compliance, core tests on Windows, and cement CLI smoke tests on Linux, macOS, and Windows — and the release hard-stops if any gate fails
  2. A gated run builds sdist + wheel and publishes to PyPI (with a TestPyPI validation path), with no credentials stored as long-lived secrets where OIDC/trusted publishing is available
  3. Docker Hub images build for linux/amd64 and linux/arm64 and push with `X`, `X.Y`, and `X.Y.Z` tags (`datafolklabs/cement`)
  4. The `stable/X.Y` version branch is created/fast-forwarded automatically and documentation builds (Read The Docs) are triggered for the release version
  5. A GitHub Release is published with the changelog body, and the remaining human steps (GitBook narrative docs, mailing list / Slack notifications) are reduced to an explicit, short post-release checklist emitted by the workflow — nothing else in issue #791's checklist requires manual execution

**Plans:** 5/5 plans complete

Plans:

  **Wave 1**

- [x] 05.4-01-PLAN.md — Dev-tooling scripts: testpypi-smoke.py (REL-02), cli-smoke-native.py (D-14), bump_dev_version.py (REL-05)

  **Wave 2** *(blocked on Wave 1)*

- [x] 05.4-02-PLAN.md — gates.yml reusable workflow (D-13) + Windows/macOS OS jobs (D-14) + build_and_test.yml thin caller (CI-05)

  **Wave 3** *(blocked on Waves 1-2)*

- [x] 05.4-03-PLAN.md — release.yml dry-run pipeline: preflight (D-02/D-09) → gates → build → TestPyPI publish + smoke (D-05/D-07/D-08); workflow_dispatch dry-run (D-06/CI-04)

  **Wave 4** *(blocked on Wave 3 — same file)*

- [x] 05.4-04-PLAN.md — release.yml publish side: single-approval OIDC publish-pypi (D-03/D-04/REL-04), Docker buildx (D-11), stable/3.0.x sync (D-10), gh-release (REL-03/DOCS-03), dev-bump PR (D-12/REL-05), checklist issue (D-16)

  **Wave 5** *(blocked on Waves 2-4 — provisioning + acceptance)*

- [x] 05.4-05-PLAN.md — Provisioning runbook + human-verify (GitHub Environment, PyPI/TestPyPI trusted publishers, Docker Hub secrets, RTD) + workflow_dispatch dry-run validation (CI-04)

### Phase 05.3: Modernize project template packaging and type all CLI-generated templates (INSERTED)

**Goal:** Modernize the packaging/setup of all 5 `cement generate` templates and make every generated file fully typed and idiomatically clean. Extends Phase 01.1 (which modernized only the `project` build) to `script`, `extension`, `plugin`, and `todo-tutorial`; migrates `todo-tutorial` off setup.py to pdm-backend; ships ruff/mypy/pytest config so a freshly generated project is `make comply` + `make test` green out of the box, enforced via the CI cli-smoke-test. Resolves #735.
**Requirements**: Phase-local — coverage by decisions D-01..D-08 (05.3-CONTEXT.md); no REQ-IDs assigned
**Depends on:** Phase 5
**Plans:** 6/6 plans complete

Plans:

  **Wave 1** *(independent per-template work — no file overlap)*

- [x] 05.3-01-PLAN.md — project template: ship ruff/mypy/pytest gate config + Makefile comply targets + type/f-string source & tests (green out of the box; D-04, D-05, D-06)
- [x] 05.3-02-PLAN.md — script/extension/plugin templates: type all defs + f-string banners; keep script VERSION tuple (D-05, D-06, D-08)
- [x] 05.3-03-PLAN.md — todo-tutorial packaging migration to pdm-backend: create pyproject (literal cement floor + gate config), delete legacy setup.py/setup.cfg/requirements*.txt/MANIFEST.in, version.py Shape B, rewrite Makefile/Dockerfile, README/CHANGELOG note (D-01, D-02, D-03)

  **Wave 2** *(blocked on Wave 1)*

- [x] 05.3-04-PLAN.md — todo-tutorial code typing + fix main.py TodoError NameError (depends 05.3-03; D-05)
- [x] 05.3-05-PLAN.md — extend cli-smoke-test: generated project make comply + make test gate + todo build/install (depends 05.3-01, 05.3-03; D-07)

  **Wave 1 (gap closure)** *(closes 05.3-VERIFICATION.md blockers)*

- [x] 05.3-06-PLAN.md — gap closure: todo-tutorial ruff comply green out of the box (isort fix + tests-excluded scope + regression guard), fix project test false-green `.find()` assertion, add CHANGELOG [cli] entries (gaps 1/2/3)

### Phase 05.2: ext.argparse command self-meta accessor (#670) (INSERTED)

**Goal:** Add a single additive, read-only accessor on `ArgparseController` (proposed `self._command_meta`) that returns the currently-dispatched command's `CommandMeta` (label, `parser_options['help']`, etc.), so exposed `@ex`/`@expose` commands can read their own decorator meta without the brittle `getattr(self, self.app.pargs.__dispatch__.split('.')[1]).__cement_meta__` dance — resolving [#670](https://github.com/datafolklabs/cement/issues/670). Purely additive: the `func()` dispatch signature is unchanged (the issue's literal `func(func_name, func_meta)` proposal is rejected as BC-breaking on the released 3.0.x surface). See 05.2-CONTEXT.md for locked decisions.
**Requirements**: phase-local (see 05.2-CONTEXT.md decisions D-01..D-07)
**Depends on:** Phase 05
**Plans:** 1/1 plans complete
Plans:

- [x] 05.2-01-PLAN.md — Add read-only `_command_meta` accessor to `ArgparseController` (+ tests at 100% coverage, CHANGELOG); resolves #670 additively

### Phase 05.1: ext.generate select-mode feature prompt UX and Jinja boolean fixes (#782) (INSERTED)

**Goal:** Merge the unreleased `ext.generate` `features:` mechanism into the template `variables:` schema so optional features behave consistently with variables — prompted in declaration order, exposed at the top level of the template context, with a default-but-overridable boolean prompt — resolving Tom Freudenberg's feedback on closed PR #780 (#782). All changes are additive to the *released* `variables:` schema; the *unreleased* `features:` schema is removed.
**Requirements**: GEN-01, GEN-02, GEN-03, GEN-04, GEN-05, GEN-06 (phase-local; see 05.1-CONTEXT.md)
**Depends on:** Phase 5
**Plans:** 5/5 plans complete

**Success Criteria** (what must be TRUE):

  1. The `features:` top-level key (and `prompt_mode`, `enabled:`/`disabled:`, select `options:`-effects) no longer exists; all former feature behavior is expressed under `variables:` via `type:` + `extend:` + `requires:`.
  2. A variable supports `type: string | boolean | choice` (default `string`); `boolean` resolves to a real Python `bool`, `choice` to the chosen `str`, and all values are exposed at the top level of the template context (`{% if feature_x %}` works) — fixing #782 point 4.
  3. Former features prompt in declaration order alongside variables (not before them) — fixing #782 point 1.
  4. A `type: boolean` variable renders a default `[(Y)es/(N)o] [default]:` prompt with no author-supplied `validate`/`case`, and accepts a custom prompt — string label (framework owns the hint) or object `{text, accept, reject}` (author owns text; non-matching input aborts like a failed `validate:`) — fixing #782 points 2 and 3.
  5. Conditional effects (`extend:` rules with `when` value/list/regex matching, composing and nesting) and dependencies (nesting + top-level `requires:`) inject `variables`/`exclude`/`ignore` correctly.
  6. A variable with none of the new keys behaves byte-identically to the released `variables:` schema (additive-only on the released surface); all in-repo cli templates, the `demo/generate-features/` template, and the ~22 generate test fixtures are migrated to the new schema; 100% coverage, ruff, and mypy stay green.

Plans:

  **Wave 1**

  - [x] 05.1-01-PLAN.md — Unified ordered resolver + `type:` key + top-level `data[name]` emit + `type: boolean` string-form prompt (migrate test6/7/13)

  **Wave 2** *(blocked on Wave 1)*

  - [x] 05.1-02-PLAN.md — `type: choice` numbered picker + polymorphic boolean object-form `prompt:` + accept/reject mapping + YAML bool-coercion guard (migrate select fixtures)

  **Wave 3** *(blocked on Wave 2)*

  - [x] 05.1-03-PLAN.md — `extend.when` value/list/regex matching + depth-first nesting + top-level `requires:` (migrate requires/nesting fixtures; remove/repurpose test17/18)

  **Wave 4** *(blocked on Wave 3)*

  - [x] 05.1-04-PLAN.md — Migrate `demo/generate-features/` to the unified schema + verify 5 cli templates generate unchanged

  **Wave 5** *(blocked on Wave 4 — acceptance)*

  - [x] 05.1-05-PLAN.md — Coverage audit (pragma vocabulary + real mapping coverage) + CHANGELOG entries for the #782 fixes

### Phase 6: Release Cut 3.0.16

**Goal**: Cut the 3.0.16 release: finalize the changelog, validate the release workflow against TestPyPI, tag, publish to PyPI, and bump the dev version to 3.0.17 per odd/even convention.
**Depends on**: Phase 5 and Phase 05.4 (and gates on Phases 1–4 being complete; release does not cut while any prior phase is open — Phase 05.4 provides the release workflow this phase runs)
**Requirements**: DOCS-03, CI-04, REL-01, REL-02, REL-03, REL-04, REL-05
**Success Criteria** (what must be TRUE):

  1. The changelog entry for 3.0.16 enumerates all user-visible changes (deprecations added, dep bumps, Python matrix change to 3.10–3.14, refactor highlights at a non-API-breaking level)
  2. A pre-release upload to TestPyPI installs cleanly on Python 3.10, 3.11, 3.12, 3.13, and 3.14, and a minimal `App().run()` round-trip succeeds on each
  3. `cement/__init__.py`, `pyproject.toml`, and any other version-of-record locations all read `3.0.16` at tag time and `3.0.17` immediately after
  4. The `3.0.16` git tag exists, the GitHub release page is published with the changelog body, and `pip install cement==3.0.16` from PyPI succeeds on a clean venv
  5. The release workflow itself (not just the artifacts) ran end-to-end without manual intervention beyond the user-approved publish step

**Plans**: 5 plans across 5 waves (strictly sequential — provisioning-first is locked by D-09, and each stage gates the next: merged release-prep commit → final dry-run → human tag push + live run → post-release verification)

  **Wave 1**

  - [ ] 06-01-PLAN.md — Provisioning checkpoint: close Docker secrets (D-11) + confirm PyPI/RTD/release-env + one-time stable/3.0.x `-s ours` ancestry merge (D-09, D-10)

  **Wave 2** *(blocked on Wave 1)*

  - [ ] 06-02-PLAN.md — Release-prep PR: finalize CHANGELOG to `## 3.0.16` (D-01..D-04) + bump backend.py VERSION to 3.0.16 (REL-01); user reviews + merges (D-05)

  **Wave 3** *(blocked on Wave 2)*

  - [ ] 06-03-PLAN.md — Final `workflow_dispatch` dry-run against the merged 3.0.16 commit; 5-Python TestPyPI smoke green (D-06, CI-04, REL-02)

  **Wave 4** *(blocked on Waves 1 + 3)*

  - [ ] 06-04-PLAN.md — Pre-tag safety + USER tag push (D-07) + shepherd live run through the single approval gate; tag + GitHub Release published (D-08, REL-03)

  **Wave 5** *(blocked on Wave 4)*

  - [ ] 06-05-PLAN.md — REL-04 clean-venv PyPI check (D-13) + merge dev-bump PR to 3.0.17 (REL-05, D-12) + announcement draft (D-14) + 06-VERIFICATION.md flipping REL-01..05/CI-04/DOCS-03

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6, with inserted decimal phases (05.1–05.4) executing between Phase 5 and Phase 6. Phase 05.4 is a hard pre-requisite for Phase 6 (the release cut runs the workflow it builds). Phases 3 and 4 are independent and parallelization-eligible once Phase 2 completes; Phase 5 can begin in parallel with Phase 4 once Phase 3 lands.

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Tooling Baseline & Python Matrix | 4/4 | Complete   | 2026-04-30 |
| 01.1. Generated Project Template Build Modernization (INSERTED) | 1/1 | Complete   | 2026-05-01 |
| 2. Dependencies & CI Pipeline | 8/8 | Complete   | 2026-05-02 |
| 3. Internal Refactor & Coverage Hardening | 8/8 | Complete   | 2026-05-04 |
| 4. Backlog Triage | manual | Complete   | 2026-05-05 |
| 5. Deprecations, Docs & Security Stubs | 6/6 | Complete   | 2026-05-08 |
| 05.1. ext.generate select-mode prompt UX + Jinja booleans (INSERTED) | 5/5 | Complete   | 2026-05-29 |
| 05.2. ext.argparse command self-meta accessor (INSERTED) | 1/1 | Complete   | 2026-06-25 |
| 05.3. Template packaging modernization + typed templates (INSERTED) | 6/6 | Complete   | 2026-07-11 |
| 05.4. GitHub Actions Release Workflow (INSERTED) | 5/5 | Complete    | 2026-07-12 |
| 6. Release Cut 3.0.16 | 0/5 | Planned | - |

## Backlog

Parking lot for post-3.0.16 (next-milestone) work. Items use `999.x` numbering,
are unsequenced, and stay out of the active phase sequence until promoted via
`/gsd-review-backlog`.

### Phase 999.1: Pydantic Settings config handler (#674) (BACKLOG)

**Goal:** Add a new **additive, optional** config handler extension backed by
[Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
(`cement/ext/ext_pydantic.py`), implementing `ConfigInterface` and registered as
a `config` handler alongside the existing configparser (default) / yaml / json
handlers. Gated behind a new optional extra (`pydantic = ["pydantic-settings"]`)
so the core stays zero-dependency. Fully typed (mypy strict), 100% test coverage,
ruff-clean, with Sphinx API docs, a GitBook narrative note, and a `[ext.pydantic]`
CHANGELOG entry.
**Requirements:** TBD (promote to derive REQ IDs)
**Plans:** 0 plans
**Source:** https://github.com/datafolklabs/cement/issues/674 (open; author derks; low priority by design)
**Scope note:** NEW feature — out of scope for the v1.0 "Clean & Green"
maintenance milestone (PROJECT.md Out of Scope: "New features beyond maintenance
… defers to later milestones"); Phase 6 is the release cut. Deferred to the next
milestone. The issue's stated prerequisite ("effort toward adding typing across
Cement") is satisfied by Phases 05.x. Additive and BC-safe, so it fits a future
3.0.x or 3.2.x line. See `.planning/phases/999.1-pydantic-settings-config-handler-674/999.1-NOTE.md`
for technical shape and open design questions.

Plans:

- [ ] TBD (promote with /gsd-review-backlog when ready)

### Phase 999.2: Cross-OS CI gates — Windows/macOS test portability (BACKLOG)

**Goal:** Re-enable the two cross-OS gate jobs shipped (commented out) in
`gates.yml` during Phase 05.4 — `test-core-windows` and `cli-smoke-native` —
and make `tests/core` pass on Windows. `cli-smoke-native` was verified GREEN
on all four legs (macOS/Windows × Python 3.10/3.14) before being parked;
`test-core-windows` surfaced ~6 genuine portability failures in
`tests/core/test_foundation.py` (assertions hardcode POSIX paths like
`/another/path` that Windows normalizes to `D:\another\path`). Fix the test
assertions to be platform-aware, uncomment both jobs, and confirm green on PR
CI. The repo has never had Windows/macOS CI, so this is a strict coverage
addition — deliberately deferred so the first automated release doesn't gate
on a brand-new OS matrix.
**Requirements:** extends D-14 (deferred from Phase 05.4)
**Plans:** 0 plans
**Source:** Phase 05.4 PR #792 debut CI run (2026-07-12)
**Scope note:** Also consider here: authenticated Docker Hub pulls (or GHCR
mirrors) for the `test-all` compose services if the anonymous-pull flake
recurs (one occurrence 2026-07-12, passed on retry).

Plans:

- [ ] TBD (promote with /gsd-review-backlog when ready)

---
*Roadmap created: 2026-04-24*
*Coverage: 42/42 v1 requirements mapped*
