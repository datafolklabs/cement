# Phase 2: Dependencies & CI Pipeline - Context

**Gathered:** 2026-05-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Refresh `pdm.lock` against current package indexes (extras + dev deps), prove
the GitHub Actions test matrix is green end-to-end on Python 3.10–3.14
(plus pypy3.10 and pypy3.11), pin every Action to a current stable tag (or
SHA where upstream has no tags), enable Dependabot for the `github-actions`
ecosystem to surface CVE-driven Action bumps, demonstrate the previously
stalled `pdm-project/update-deps-action` scheduled job runs cleanly against
the new baseline, and wire the 100% coverage gate so CI actually fails
below 100%.

**In scope:**
- `pdm update` against current package indexes; per-failure split into
  follow-up `fix(...)` commits per Phase 1's D-04 atomic-per-concern shape
- `[project.optional-dependencies]` extras stay unpinned in `pyproject.toml`
  (downstream apps own their version policy)
- One-shot `pip-audit` run against the bumped lockfile; output captured to
  `.planning/phases/02-.../02-PIP-AUDIT.md` (or commit-message body); any
  unpatched runtime CVE either pinned-around with rationale or documented
  as accepted
- Action pin tightening across `.github/workflows/build_and_test.yml` and
  `.github/workflows/pdm.yml` to exact tags (`@vX.Y.Z`); SHA-pin for
  untagged Actions (`pdm-project/update-deps-action`) with a date comment
- New `.github/dependabot.yml` enabling the `github-actions` ecosystem so
  Dependabot opens PRs for Action bumps (with security advisories
  prioritized)
- `workflow_dispatch:` trigger added to `pdm.yml` so the deps-update job
  can be manually triggered for end-to-end verification (not just waited
  on for the Monday cron)
- pypy3.11 added to the matrix alongside existing pypy3.10
- `[tool.coverage.report] fail_under = 100` added to `pyproject.toml`;
  pytest addopts already include `--cov-report=term`, so the gate fires
  via pytest-cov at session end (research confirms pytest-cov v7 honors
  `[tool.coverage.report].fail_under`)
- Explicit `[tool.coverage.run]` block added with `source = ["cement"]`
  and `omit = ["cement/cli/templates/*", "cement/cli/contrib/*"]` to
  mirror ruff's `exclude` discipline
- Removal of the `# FIXME ?` cruft comment above the OS matrix line in
  `build_and_test.yml`

**Out of scope:**
- Ruff/mypy/pytest version bumps (locked in Phase 1: `ruff ~=0.15.12`,
  `mypy ~=1.20.2`, `pytest>=9.0.3`, `pytest-cov>=7.1.0`,
  `coverage>=7.13.5`) — Phase 2 inherits these floors and updates the
  REST of the lockfile around them
- `pip-audit` / `bandit` / SAST CI integration (PROJECT.md Out of Scope;
  Phase 5 SEC-01/02/03 stubs only). Phase 2's `pip-audit` is a one-shot
  manual spot-check, NOT a recurring CI job
- Adding `pragma: no cover` audit / pruning unjustified exclusions
  (Phase 3 COV-03)
- Adding macOS or Windows OS matrix lanes (libmemcached + signal/daemon
  + bash dependencies make this a dedicated platform-support effort, not
  Phase 2 scope)
- Flattening the serial `comply → test → test-all → cli-smoke-test` job
  graph (intentional fail-fast; touching it risks regressions while we're
  trying to prove the pipeline works)
- Coverage instrumentation on the `cli-smoke-test` job (it's a black-box
  install/run smoke test by design)
- `[project.optional-dependencies]` lower-bound or upper-bound pinning
  (would be a downstream-observable change to pip resolution; backward-
  compat constraint says no)
- CI-04 (release workflow validated end-to-end against TestPyPI) — that's
  Phase 6 work, not Phase 2

</domain>

<decisions>
## Implementation Decisions

### Lockfile refresh
- **D-01:** **`pdm update`** (not `pdm lock` and not targeted per-extra).
  The 0cca6f88 relock was a passive py39-drop refresh — Phase 2 actively
  bumps deps to latest non-breaking versions per current specifiers,
  which is what the stalled cron would have done if it hadn't drowned in
  Phase 1 lint. Single commit `chore(deps): pdm update to current
  non-breaking versions` lands first, then per-failure splits.

### Optional-extras pin policy
- **D-02:** **`[project.optional-dependencies]` STAYS UNPINNED.** Keep
  shape `colorlog = ["colorlog"]`, `jinja2 = ["jinja2"]`, etc. Downstream
  apps control their own version policy; cement's lockfile pins for
  development only. Adding `>=` floors or upper bounds would be a
  downstream-observable change to pip resolution, which the 3.0.x
  no-breakage constraint forbids.

### CVE spot-check (DEPS-03)
- **D-03:** **One-shot `pip-audit` run; output committed.** Run
  `pdm run pip-audit` (or `pipx run pip-audit`) once locally after the
  pdm-update commit lands. Capture the report to
  `.planning/phases/02-dependencies-ci-pipeline/02-PIP-AUDIT.md`. Any
  unpatched runtime CVE either:
  - gets pinned-around in a follow-up `chore(deps): pin <pkg> for CVE
    <id>` commit with rationale in the body, OR
  - documented in 02-PIP-AUDIT.md as accepted (with rationale)
  Do NOT add `pip-audit` to `[dependency-groups].dev` or to a Makefile
  target — that overlaps Phase 5 SEC-01's intended scope. One-shot only
  this phase.

### Drift-fix policy when `pdm update` produces failures
- **D-04:** **Phase 1 D-04 atomic split.** Land
  `chore(deps): pdm update to current non-breaking versions` FIRST (CI
  may temporarily go red within the branch — acceptable). Then split
  each resulting failure into a separate commit:
  - `fix(lint): resolve <rule> from <pkg> bump`
  - `fix(type): resolve <error code> from <pkg>-stubs bump`
  - `fix(test): resolve <test name> deprecation/regression from <pkg> bump`
  PR-level acceptance is what gates merge. Bisect-friendly per Phase 1's
  established pattern.

### GitHub Action pinning
- **D-05:** **Exact tags everywhere** (`@v4.2.2`, not `@v4`). Pin every
  Action across both `build_and_test.yml` and `pdm.yml` to the current
  stable tagged release. Satisfies CI-05 literally and matches the
  AUDIT-POINT discipline from Phase 1's D-08 — explicit values, no
  floating refs.
- **D-06:** **For the one untagged Action (`pdm-project/update-deps-action`,
  `@main` only), SHA-pin** with a dated comment:
  ```yaml
  uses: pdm-project/update-deps-action@<sha>  # pinned 2026-05-XX, no tagged release upstream
  ```
  Bumps land as Dependabot PRs (Dependabot tracks SHA-pinned Action
  branch HEAD changes when the github-actions ecosystem is enabled).
- **D-07:** **Enable Dependabot for the `github-actions` ecosystem.**
  Add `.github/dependabot.yml` with the `github-actions` package
  ecosystem entry (and ONLY that ecosystem in Phase 2 — `pip` is already
  handled by the pdm.yml cron). Dependabot auto-opens a PR when any
  pinned Action ships a new version, with security advisories
  prioritized and labeled. This closes the upstream-monitoring gap that
  exact-tag pinning would otherwise create. Costs ~10 lines of yaml +
  occasional bump PRs to merge.

### `pdm update` job verification (DEPS-04)
- **D-08:** **Add `workflow_dispatch:` trigger to `pdm.yml`** as part of
  this phase. After Phase 2's PR merges to main, manually trigger via
  `gh workflow run pdm.yml` (or the Actions UI) and observe a clean run
  to completion (no PR opened ⇒ baseline already current; PR opened ⇒
  inspect the proposed updates). Capture evidence in the phase
  verification artifact. `workflow_dispatch:` becomes a permanent
  affordance — no code added solely for verification.
- **D-09:** Acceptance: workflow_dispatch run completes WITHOUT producing
  the wall-of-lint failure mode the cron previously hit. If the run
  produces no PR (because pdm update is a no-op against the baseline
  Phase 2 just landed), that's a passing outcome — proves the cron path
  works against the new baseline.

### Coverage gate (CI-03)
- **D-10:** **Wire fail_under in `pyproject.toml`**, not in CI YAML.
  Single source of truth — applies anywhere `coverage report` runs
  (local + CI + ad-hoc). Add to `[tool.coverage.report]` next to the
  existing `precision = 2`:
  ```toml
  [tool.coverage.report]
  precision = 2
  fail_under = 100
  ```
- **D-11:** **Also add `--cov-fail-under=100` explicitly to pytest
  `addopts`** as belt-and-braces. pytest-cov v7 honors
  `[tool.coverage.report].fail_under` when generating its term report at
  session end (research confirms this), but the explicit addopts flag
  guarantees the failure surfaces even if pytest-cov defaults shift on
  a future bump. Update `[tool.pytest.ini_options].addopts`:
  ```
  -v --cov-report=term --cov-report=html:coverage-report
     --cov-fail-under=100 --capture=sys tests/
  ```
- **D-12:** **Add explicit `[tool.coverage.run]` block** to mirror
  ruff's `exclude` discipline:
  ```toml
  [tool.coverage.run]
  source = ["cement"]
  omit = [
      "cement/cli/templates/*",
      "cement/cli/contrib/*",
  ]
  ```
  Makes the measurement boundary explicit and grep-able. Insulates
  against future `.py` files in `cement/cli/templates/` accidentally
  getting measured (today the only real `.py` file there is
  `cement/cli/templates/__init__.py`).
- **D-13:** **No coverage on the `cli-smoke-test` job.** It's a black-box
  install/run test by design (verifies the generated-project template
  builds and runs end-to-end). Adding `--cov=cement` would change what
  the smoke test measures and complicate its artifact.

### CI matrix
- **D-14:** **Keep pypy3.10 + ADD pypy3.11.** The matrix grows from 6 to
  7 lanes:
  ```yaml
  python-version: ["3.10", "3.11", "3.12", "3.13", "3.14",
                   "pypy-3.10", "pypy-3.11"]
  ```
  `actions/setup-python@v5` supports `pypy-3.11`. pypy3.10 is not
  dropped (would be a downstream-observable change). pypy3.11 modernizes
  the pypy story.
- **D-15:** **Leave OS matrix as ubuntu-only; remove the `# FIXME ?`
  comment.** macOS and Windows lanes are out of scope for Clean & Green
  (libmemcached install paths differ on macOS, signal/daemon code is
  Unix-only per INTEGRATIONS.md, scripts/cli-smoke-test.sh is bash, and
  surfacing 5 new platform bugs would derail the milestone). Removing
  the FIXME cleans up cruft without changing semantics.
- **D-16:** **Keep the serial job graph** (`comply → test → test-all →
  cli-smoke-test`). Intentional fail-fast: don't burn 7 matrix lanes if
  ruff/mypy is red. Touching the job graph risks regressions while
  Phase 2's whole goal is proving the pipeline works. Job-graph
  optimization is out of scope.

### Commit shape
- **D-17:** **Atomic per-concern, Conventional Commits, 78-char wrap**
  (CLAUDE.md + Phase 1 D-02 + 01.1 D-15). Suggested split (planner
  refines):
  1. `chore(deps): pdm update to current non-breaking versions`
  2. `fix(lint|type|test): ...` per failure surfaced by D-01 (zero or
     more)
  3. `chore(deps): pin <pkg>` per CVE pin-around (zero or more)
  4. `ci: pin GitHub Actions to exact tags` (build_and_test.yml +
     pdm.yml in one commit — they're all the same concern)
  5. `ci: SHA-pin pdm-project/update-deps-action`
  6. `ci: enable Dependabot for github-actions ecosystem`
  7. `ci: add workflow_dispatch trigger to pdm.yml`
  8. `ci: add pypy-3.11 to test matrix`
  9. `ci: drop FIXME OS-matrix comment`
  10. `test: enforce 100% coverage gate via fail_under + addopts`
      (combines D-10/D-11/D-12 — they're one logical change to coverage
      enforcement)
- **D-18:** **GSD artifact commits** follow `docs(02): ...` shape
  (mirrors Phase 1 / 01.1 patterns).

### Acceptance
- **D-19:** Phase 2 acceptance is the conjunction of:
  1. A fresh PR triggers Actions; all 7 matrix lanes report green
  2. Compliance + 100% coverage gate visibly fails at <100% (verifiable
     by temporarily dropping a covered line in a throwaway commit, then
     reverting)
  3. `workflow_dispatch`-triggered run of pdm.yml completes without the
     wall-of-lint failure mode
  4. `02-PIP-AUDIT.md` exists in the planning artifacts; any flagged CVE
     is either pinned-around (with commit + rationale) or documented as
     accepted
  5. `grep -rn "@v[0-9]\+$\|@main" .github/workflows/` returns only the
     SHA-pinned Action lines (per D-06's exception); no other floating
     refs

### Claude's Discretion
- Exact commit-message body phrasing within the D-17 split (planner picks).
- Whether to author commits via `make commit` or directly via `git commit`
  (either satisfies CLAUDE.md as long as the result matches Conventional
  Commits + 78-char wrap).
- Order of unrelated `ci: ...` commits within D-17's middle (Dependabot
  enablement, workflow_dispatch trigger, pypy-3.11 add, FIXME drop) —
  planner can interleave.
- Specific tag/SHA values for Action pins (research picks current
  stable; planner verifies via `gh api repos/<owner>/<repo>/releases`
  or equivalent).
- Whether to bundle Dependabot config additions for `pip` ecosystem
  too — kept OUT of scope above per D-07 (pdm.yml cron handles it),
  but planner can revisit if research surfaces a strong reason.

### Folded Todos
None — STATE.md "Pending Todos" is empty.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project intent and constraints
- `.planning/PROJECT.md` — Core Value, no-breakage rule on 3.0.x,
  Constraints block (zero new runtime deps for core, 100% coverage
  absolute), Key Decisions table. **Out of Scope** specifically defers
  pip-audit/bandit/SAST CI ROLLOUT to Phase 5 (D-03 above respects this).
- `.planning/REQUIREMENTS.md` §"Dependencies" (DEPS-01..04), §"CI
  Pipeline" (CI-01, CI-02, CI-03, CI-05 — note: CI-04 is Phase 6, NOT
  Phase 2). Also §"Test Coverage" COV-01..03 (Phase 3 owns COV-03;
  Phase 2 only wires the 100% gate, doesn't audit pragmas).
- `.planning/ROADMAP.md` §"Phase 2: Dependencies & CI Pipeline" — goal,
  dependencies (Phase 1), 5 success criteria, requirement mapping.
- `.planning/ROADMAP.md` §"Phase 5" and §"Phase 6" — what's deferred to
  later phases (security tooling rollout, release workflow validation).

### Precedent — same project, same scope discipline
- `.planning/phases/01-tooling-baseline-python-matrix/01-CONTEXT.md` —
  D-02 atomic-commit shape, D-04 one-commit-per-rule-family, D-08 hybrid
  audit-point pattern, D-12 hybrid pin strategy (compat-release for
  fast-moving tools, floor for stable test-tools). Phase 2 inherits all
  of these.
- `.planning/phases/01.1-generated-project-template-build-modernization/01.1-CONTEXT.md`
  — D-15 multiple-atomic-commits-per-branch pattern; revision_history
  precedent for pulling deferred work forward when reality demands it.

### Existing codebase intel
- `.planning/codebase/STACK.md` — current dep tree, optional-extras
  inventory, dev-dep set.
- `.planning/codebase/INTEGRATIONS.md` §"CI/CD & Deployment",
  §"Local Development Orchestration" — docker-compose service-only
  harness used by `comply`/`test`/`test-all` jobs (compose-services-only
  brings up redis, memcached, mailpit). Phase 2 must not regress this.
- `.planning/codebase/CONVENTIONS.md` — current ruff config (already
  updated by Phase 1; Phase 2 doesn't touch).

### Files this phase will touch
- `pdm.lock` — regenerated by `pdm update`
- `pyproject.toml` — `[tool.coverage.report] fail_under`,
  `[tool.coverage.run] source/omit`, `[tool.pytest.ini_options].addopts`
  (`--cov-fail-under=100`), possibly individual dep pins for CVE
  pin-arounds (D-03)
- `.github/workflows/build_and_test.yml` — Action exact-tag pins for
  `actions/checkout`, `actions/setup-python`, `pdm-project/setup-pdm`,
  `ConorMacBride/install-package`, `hoverkraft-tech/compose-action`;
  `python-version` matrix gains `"pypy-3.11"`; `# FIXME ?` OS-matrix
  comment block deleted
- `.github/workflows/pdm.yml` — `workflow_dispatch:` trigger added under
  `on:`; `pdm-project/update-deps-action@main` SHA-pinned with comment;
  `actions/checkout` exact-tag pinned
- `.github/dependabot.yml` — NEW file enabling `github-actions`
  ecosystem (only — `pip` ecosystem stays out per D-07)
- `.planning/phases/02-dependencies-ci-pipeline/02-PIP-AUDIT.md` — NEW
  artifact capturing the DEPS-03 spot-check output

### External docs
- pdm-project/update-deps-action repo: https://github.com/pdm-project/update-deps-action
  — for SHA pin selection (D-06) and confirming no tagged release stream
- Dependabot github-actions ecosystem docs:
  https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file#package-ecosystem
- pip-audit CLI: https://pypi.org/project/pip-audit/
- pytest-cov fail_under behavior:
  https://pytest-cov.readthedocs.io/en/latest/config.html
  (research confirms `[tool.coverage.report].fail_under` is honored)

### Conventions
- `CLAUDE.md` §"Commit Conventions" — Conventional Commits, 78-char
  subject + body wrap, `make commit` (`pdm run cz commit`) for
  interactive authoring.
- `CLAUDE.md` §"Changelog Maintenance" — append entries to active
  `## 3.0.16 - DEVELOPMENT` section; `chore(deps):` → Misc, `ci:` →
  Misc, `fix(lint|type|test):` → Bugs, `feat(...)` would be Features
  (none expected this phase). Phase 2 lands changelog entries
  phase-by-phase, not at release-cut time.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `make comply`, `make comply-ruff`, `make comply-mypy`, `make test` —
  existing entry points; no new make targets required this phase.
- `[tool.pytest.ini_options].addopts` already requests `--cov-report=term`
  — pytest-cov's term-report path is the surface that will read
  `fail_under` (D-10/D-11).
- The `compose-services-only.yml` docker-compose harness already brings
  up redis/memcached/mailpit for the `test`/`test-all` CI jobs — pdm
  bumps that touch redis/pylibmc client libs are exercised against real
  services, not mocks. Phase 2's `pdm update` will benefit from this
  on the PR's CI run.
- The `cli-smoke-test` Makefile target was added in quick task
  `260430-i7q` and the `cli-smoke-test` job in build_and_test.yml runs
  it on each PR. Phase 01.1 wired the generated-project template to
  pdm-backend so this passes today on the full Python 3.10–3.14 matrix.
  Phase 2 doesn't touch this.

### Established Patterns
- **Hybrid pin strategy** (Phase 1 D-12): compat-release (`~=`) for
  fast-moving tools (ruff, mypy), floor (`>=`) for slow-moving deps
  (pytest-family, mock, pypng, requests, commitizen). Phase 2's `pdm
  update` operates within these specifiers — `~=` deps can move on the
  patch but not the minor; `>=` deps can move on minor and major but
  not below the floor. This is the safety net for "non-breaking
  versions" in DEPS-01.
- **AUDIT POINT comments** (Phase 1 D-08) — every config change that
  could silently drift gets a comment naming itself as the audit point.
  Pattern carries forward: D-12's new `[tool.coverage.run] omit`
  block deserves an AUDIT POINT comment naming the
  templates/contrib exclusion as the audit surface for future
  template-dir changes.
- **Atomic-per-concern commits** (Phase 1 D-02 + D-04, 01.1 D-15) —
  enforced again here per D-04/D-17.
- **`# noqa` / `# type: ignore` discipline** (CONVENTIONS.md) — when
  pdm-update's fix-up commits need ignores, follow the existing
  per-line + comment-explaining-why pattern.

### Integration Points
- **CI gate**: `.github/workflows/build_and_test.yml` runs `make comply`
  (ruff + mypy), `make test` (pytest + coverage), and `cli-smoke-test`
  on every PR. Phase 2 must turn this gate green end-to-end across the
  new 7-lane matrix.
- **Scheduled job**: `.github/workflows/pdm.yml` runs
  `pdm-project/update-deps-action` weekly on Mondays 03:05 UTC. Phase 2's
  D-08 adds `workflow_dispatch:` for manual verification; once green,
  the cron will continue to work without further intervention.
- **Dependabot (NEW)**: Phase 2's D-07 introduces Dependabot. Its PRs
  trigger `build_and_test.yml` (because that workflow is `on:
  pull_request`), so Dependabot Action-bump PRs are automatically
  gated on CI green — same shape as human-authored PRs.

### Known floating-ref / pinning gaps (Phase 2 fixes)
- `.github/workflows/pdm.yml:14` — `pdm-project/update-deps-action@main`
  (floating ref; D-06 SHA-pins)
- `.github/workflows/build_and_test.yml` lines 20, 25, 30, 41, 50, 54,
  71, 78, 91 — mix of `@v4`, `@v5`, `@v4`, `@v2.0.1`. D-05 unifies to
  exact tags.

### Coverage state today (pre-Phase-2)
- `make test` is currently green (Phase 1 ended green). `--cov=cement`
  reports 100% per Phase 1's D-04 acceptance. Phase 2's D-10/D-11/D-12
  is wiring the gate, not closing gaps in coverage.
- The single real `.py` file in the soon-to-be-omitted directories is
  `cement/cli/templates/__init__.py`. Today it's covered by
  the import. After D-12 it's omitted from measurement entirely (cleaner).

</code_context>

<specifics>
## Specific Ideas

- The user-articulated pain point (PROJECT.md "What sparked this
  milestone") is the stalled `pdm update` GitHub Action drowning in ruff
  lint each week. Phase 1 unblocked the lint side; Phase 2 closes the
  loop by (a) running `pdm update` manually NOW so the cron's first
  post-merge run is a no-op, (b) adding `workflow_dispatch:` so we can
  verify the cron path end-to-end without waiting a week, and (c)
  enabling Dependabot for Actions so the Action-version drift problem
  doesn't become the next pdm-cron-style stall.
- The exact-tag-everywhere pin policy (D-05) is chosen specifically
  because Dependabot (D-07) backstops it. Without Dependabot, exact
  tags would create the same "auto-patch CVE goes unnoticed" problem
  exact pins create for PyPI deps — but Dependabot's github-actions
  ecosystem watches GHSA and prioritizes security advisories, so the
  combination gives both reproducibility AND auto-CVE-surfacing.
- Adding pypy3.11 (D-14) modernizes the pypy lane WITHOUT dropping
  pypy3.10 — explicitly chosen by the user during discussion to avoid
  any downstream-observable change to the support matrix while still
  picking up the modern runtime.

</specifics>

<deferred>
## Deferred Ideas

- **macOS / Windows OS matrix lanes** — D-15 keeps ubuntu-only this
  phase. Cross-platform support is a dedicated platform-support effort
  involving libmemcached install paths (macOS via Homebrew), signal/
  daemon code (Unix-only per INTEGRATIONS.md), bash dependency in
  scripts/cli-smoke-test.sh, and likely surfaced 3.0.x-incompatible
  fixes. Out of scope for Clean & Green; revisit as a separate
  milestone.
- **Job-graph flattening** — D-16 keeps serial sequencing. Optimizing
  PR feedback time below ~25–40 min would mean parallelizing
  comply/test/test-all, which trades fail-fast for compute. Cement is
  not a high-PR-velocity project; deferred indefinitely.
- **`pip` ecosystem in Dependabot** — D-07 enables `github-actions`
  only. The `pip` ecosystem is already handled by `pdm.yml` cron
  (`pdm update`). Adding pip to dependabot.yml would create duplicate
  PR streams. Revisit if pdm.yml is ever retired.
- **Coverage instrumentation for cli-smoke-test** — D-13 keeps it
  black-box. Adding `--cov=cement` through the smoke-test invocation
  would surface CLI-generation and template-rendering paths but blur
  unit/integration/smoke boundaries. Revisit if a coverage gap analysis
  in a future phase shows the smoke path covers something unit tests
  miss.
- **Optional-extras lower-bound floors (`>=`)** — D-02 keeps unpinned.
  Adding minimum-tested-version signal for downstream apps would be a
  downstream-observable change; revisit on a 3.2.0 breakage-allowed
  milestone if there's a real pain point.
- **`pip-audit` / `bandit` / SAST CI integration** — Phase 5 SEC-01/02/03
  stubs. Phase 2's pip-audit is a one-shot manual spot-check (D-03);
  CI integration is out of scope per PROJECT.md.

</deferred>

---

*Phase: 02-dependencies-ci-pipeline*
*Context gathered: 2026-05-01*
