---
phase: 02-dependencies-ci-pipeline
plan: 01
subsystem: infra
tags:
  - pdm-update
  - lockfile
  - optional-extras
  - dev-deps
  - phase-2
  - redis-7
  - watchdog-6
  - mypy-drift

requires:
  - phase: 01-tooling-baseline-python-matrix
    provides: green make-comply + make-test baseline (ruff~=0.15, mypy~=1.20, pytest>=9.0, 100% coverage), Phase-1 dev pin specifiers in [dependency-groups].dev that constrain pdm update
  - phase: 01-tooling-baseline-python-matrix
    provides: Plan-04 deferred lockfile regeneration (Pitfall 4 — pdm.lock was deliberately NOT regenerated in Phase 1, exactly so this Phase-2 plan owns it)
provides:
  - pdm.lock refreshed against current PyPI within Phase 1 specifiers (14 packages bumped)
  - redis 7.4.0 / watchdog 6.0.0 (MAJOR) / tabulate 0.10.0 first-order optional-extras current
  - sphinx 8.1.3 + sphinxcontrib-* 2.x docs-extra transitive bumps
  - commitizen 4.13.10 + requests 2.33.1 + packaging 26.2 dev tooling current
  - Drift-fix posture for redis 7 typing union and watchdog 6 stub improvements (D-04 atomic split per failure)
  - Green baseline (make comply + make test, 316 passed, 100% coverage) for Plan 02 (pip-audit) and Plan 03 (coverage gate) to inherit
affects:
  - 02-02-PLAN (DEPS-03 pip-audit runs against this lockfile)
  - 02-03-PLAN (coverage gate wraps the green make test baseline this plan preserved)
  - 02-04-PLAN, 02-06-PLAN, 02-07-PLAN (CI workflow + Dependabot + workflow_dispatch verification all build on this lockfile)

tech-stack:
  added:
    - redis 7.4.0 (major bump from 6.1.1 — RESP3 typing changes)
    - watchdog 6.0.0 (major bump from 4.0.2 — improved type stubs)
    - tabulate 0.10.0 (minor bump from 0.9.0)
    - sphinx 8.1.3 (major-ish bump from 7.1.2)
    - sphinxcontrib-applehelp/devhelp/htmlhelp/qthelp/serializinghtml 2.x (from 1.x)
    - sphinx-rtd-theme 3.1.0 (from 3.0.2)
    - alabaster 1.0.0 (from 0.7.13)
    - commitizen 4.13.10 (from 4.10.1)
    - requests 2.33.1 (from 2.31.0)
    - packaging 26.2 (from 24.0)
  patterns:
    - "D-04 atomic-per-failure split (Phase 1 inheritance): one chore(deps) + N fix(type/lint/test) commits, never bundled"
    - "D-13 strict-minimum drift-fix: # type: ignore[<code>] append over narrowing assertion (mirrors Phase 1 Plan 03 handler.py:394 precedent)"
    - "D-02 unpinned optional-extras held: zero diff in pyproject.toml [project.optional-dependencies] specifiers"
    - "CHANGELOG bucketing: chore(deps) -> Misc [dev]; fix(type) -> Bugs [ext.<area>]"

key-files:
  modified:
    - pdm.lock (14 packages bumped within Phase 1 specifiers)
    - CHANGELOG.md (1 Misc + 2 Bugs entries appended to ## 3.0.15 - DEVELOPMENT)
    - cement/ext/ext_redis.py (3 # type: ignore annotations for redis 7 union returns)
    - cement/ext/ext_watchdog.py (3 # type: ignore comments dropped — watchdog 6 stubs precise)

key-decisions:
  - "D-01 lockfile bump landed as single chore(deps) commit (9f0f8627); no specifier changes in pyproject.toml [dependency-groups].dev or [project.optional-dependencies] (D-02 held)"
  - "Drift surfaced in mypy only: 6 errors across 2 files. Tests passed unmodified (316/316, 100%). RESEARCH.md Pitfall 4 prediction (watchdog 4->6 most likely fallout) confirmed; redis 7 typing drift was unexpected from RESEARCH.md but absorbed via the same D-04 split."
  - "Redis 7.x introduced sync-client return-type unions (Awaitable[Any] | Any) since the same client class supports RESP3 sync+async. Three sites in ext_redis.py needed minimum-fix # type: ignore[union-attr|arg-type|misc] — Phase 3 REFACTOR-02 may revisit with isinstance narrowing."
  - "Watchdog 6.x ships precise Observer stubs, making the legacy # type: ignore on schedule/start/stop comments fire as unused-ignore. Removed all 3; the framework-Meta # type: ignore on line 73 (MetaMixin pattern) intentionally kept."
  - "Changelog fold-in for chore(deps): committed lockfile and CHANGELOG entry together (single atomic operation per plan A.6 Discretion). Drift-fix CHANGELOG entries folded into their own fix(type) commits."

patterns-established:
  - "fix(type): <subsystem> drift commits inherit Phase 1 D-04 atomic split: one commit per independent typing-failure source, regardless of count of suppression annotations needed inside that source"
  - "Major-version bumps absorbed via minimum-fix # type: ignore[<specific-code>] (not bare # type: ignore) to keep diagnostics surface-readable; Phase 3 owns proper narrowing"
  - "pdm update --dry-run post-commit returning 'All packages are synced to date' is the DEPS-01 acceptance signal (matches latest non-breaking versions)"

requirements-completed:
  - DEPS-01
  - DEPS-02

# Metrics
duration: 13min
completed: 2026-05-03
---

# Phase 02 Plan 01: Lockfile Refresh + Drift-Fix Atomic Split Summary

**`pdm update` regenerates lockfile (14 packages), absorbing redis 7.4.0 + watchdog 6.0.0 (MAJOR) + tabulate 0.10.0 + sphinx 8.1.3 + dev tooling (commitizen/requests/packaging) within Phase 1 specifiers; D-04 atomic-split absorbs 6 mypy drift errors across ext_redis.py and ext_watchdog.py via two separate `fix(type)` commits — `make comply` and `make test` exit 0 at 316/316 + 100% coverage, with optional-extras specifiers unchanged (D-02 held).**

## Performance

- **Duration:** ~13 min (single execution pass, no rollback iterations)
- **Started:** 2026-05-03T00:58:00Z (post worktree-init `make init`)
- **Completed:** 2026-05-03T01:11:06Z
- **Tasks:** 1 (with 3 sub-steps: A mandatory + B conditional invoked + C verification)
- **Atomic commits:** 3 (1 chore(deps) + 2 fix(type))
- **Files modified:** 4 (pdm.lock, CHANGELOG.md, cement/ext/ext_redis.py, cement/ext/ext_watchdog.py)

## Accomplishments

- DEPS-01 closed: `pdm.lock` matches latest non-breaking versions within Phase 1 specifiers; `pdm update --dry-run` post-commit returns "All packages are synced to date".
- DEPS-02 closed: optional-extras (redis 7.4.0, watchdog 6.0.0, tabulate 0.10.0) at PyPI current; `[project.optional-dependencies]` specifiers byte-identical to pre-bump (D-02 unpinned policy held — zero diff in pyproject.toml).
- Drift-fix posture proven for major-version bumps: redis 7 typing-union drift and watchdog 6 stub-improvement drift each absorbed in independent `fix(type)` commits per D-04 (Phase 1 inheritance).
- Green baseline preserved: `make comply` exits 0 (ruff + mypy clean across 51 source files); `make test` exits 0 at 316 passed / 100% coverage.
- Plan 02 (pip-audit) inherits a current lockfile to scan; Plan 03 (coverage gate) inherits the green test baseline.

## Task Commits

Each task/sub-step was committed atomically:

1. **Sub-step A: Lockfile bump (D-01)** — `9f0f8627` (chore(deps): pdm update to current non-breaking versions). 14 packages updated; CHANGELOG `[dev] Bump dev/extras lockfile` appended to Misc bucket; pyproject.toml unchanged (D-02 held).
2. **Sub-step B.1: Redis 7 typing drift (fix(type))** — `bf567f2b` (fix(type): resolve redis 7 typing drift in ext_redis). Three `# type: ignore[union-attr|arg-type|misc]` annotations on get/delete/purge sites; CHANGELOG `[ext.redis]` entry appended to Bugs bucket.
3. **Sub-step B.2: Watchdog 6 stub-improvement drift (fix(type))** — `54253244` (fix(type): drop unused type-ignores in ext_watchdog vs watchdog 6). Three legacy `# type: ignore` comments removed from Observer schedule/start/stop calls; CHANGELOG `[ext.watchdog]` entry appended to Bugs bucket.

All 3 commits: subject ≤78 chars (56 / 52 / 65); body lines all ≤78 chars; Conventional Commits compliant (CLAUDE.md).

## Files Created/Modified

- `pdm.lock` — Regenerated against current PyPI within Phase 1 specifiers. 14 packages updated. Diff confined to lockfile entries; no specifier mutation in pyproject.toml.
- `CHANGELOG.md` — 3 entries appended to `## 3.0.15 - DEVELOPMENT`:
  - Misc: `` `[dev]` Bump dev/extras lockfile to current non-breaking versions (redis 7.4, watchdog 6.0, tabulate 0.10, sphinx 8.1, requests 2.33, others) ``
  - Bugs: `` `[ext.redis]` Resolve mypy union-attr/arg-type/misc errors surfaced by redis 7 typing changes (sync client return-type unions) ``
  - Bugs: `` `[ext.watchdog]` Drop now-unused `# type: ignore` comments on Observer schedule/start/stop calls — watchdog 6 ships precise type stubs ``
- `cement/ext/ext_redis.py` — 3 minimum-fix annotations:
  - line 98: `# type: ignore[union-attr]` on `res.decode('utf-8')` (get())
  - line 134: `# type: ignore[arg-type]` on `int(res)` (delete())
  - line 145: `# type: ignore[misc]` on `self.r.delete(*keys)` (purge())
- `cement/ext/ext_watchdog.py` — 3 legacy `# type: ignore` comments removed from `Observer.schedule()` / `start()` / `stop()` invocations (lines 108, 120, 133 pre-edit). The framework-Meta `# type: ignore` on line 73 (MetaMixin pattern) intentionally retained.

## Bumped Packages — Predicted vs Actual

RESEARCH.md predicted 14 packages would move; the actual run confirmed 14:1 match (the `cement 3.0.15 -> 3.0.15` self-relock is a synchronization no-op, not counted against the 14):

| Package | Pre | Post | Family |
|---------|-----|------|--------|
| redis | 6.1.1 | 7.4.0 | first-order optional-extra (MAJOR) |
| watchdog | 4.0.2 | 6.0.0 | first-order optional-extra (MAJOR) |
| tabulate | 0.9.0 | 0.10.0 | first-order optional-extra |
| sphinx | 7.1.2 | 8.1.3 | docs-extra direct |
| sphinx-rtd-theme | 3.0.2 | 3.1.0 | docs-extra direct |
| sphinxcontrib-applehelp | 1.0.4 | 2.0.0 | docs-extra transitive |
| sphinxcontrib-devhelp | 1.0.2 | 2.0.0 | docs-extra transitive |
| sphinxcontrib-htmlhelp | 2.0.1 | 2.1.0 | docs-extra transitive |
| sphinxcontrib-qthelp | 1.0.3 | 2.0.0 | docs-extra transitive |
| sphinxcontrib-serializinghtml | 1.1.5 | 2.0.0 | docs-extra transitive |
| alabaster | 0.7.13 | 1.0.0 | docs-extra transitive |
| commitizen | 4.10.1 | 4.13.10 | dev tooling |
| requests | 2.31.0 | 2.33.1 | dev tooling |
| packaging | 24.0 | 26.2 | pure transitive |

Sphinx 9.x and Sphinx 8.2.x (and rcs) were correctly skipped by the resolver because they require Python>=3.11 and our `requires-python = ">=3.10"` floor pins us below — expected behavior, not a regression.

## Decisions Made

- **Lockfile + CHANGELOG fold-in for `chore(deps)`:** Per plan A.6 Discretion — single-pass atomic operation. Drift-fix `[ext.redis]` and `[ext.watchdog]` Bugs entries each fold into their own `fix(type)` commit (not separated as `docs(02): ...` updates) to keep CHANGELOG bucket-line and the source diff bisectable together.
- **Minimum-fix `# type: ignore[<code>]` over narrowing assertion (Phase 1 D-13 strict-minimum):** Three redis sites used per-error-code suppression (`union-attr`, `arg-type`, `misc`) rather than bare `# type: ignore`, keeping the diagnostic surface readable for future revisits.
- **Watchdog `# type: ignore` removal vs replacement:** Watchdog 6 stubs are precise enough that the comments are now unused-ignore noise. Removing them is the minimum fix (mirrors Phase 1 D-13). The framework-Meta `# type: ignore` on the Meta class annotation is structurally different (MetaMixin metaclass workaround) and stays.
- **D-04 split granularity:** Two `fix(type)` commits, one per independent source file, even though both fixes share the root cause "post-bump mypy drift". Each commit is independently revertable; bisect can pinpoint redis-7 vs watchdog-6 fallout separately.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug / D-04 atomic split] Mypy drift surfaced post-bump in `cement/ext/ext_redis.py`**
- **Found during:** Sub-step A.4 (post-bump `make comply` smoke test)
- **Issue:** Redis 7.0.0 introduced typing where the sync client's return values are unioned with `Awaitable[Any]` (RESP3 sync/async dual-purpose client class), surfacing 3 mypy errors:
  - `ext_redis.py:98` — `union-attr` on `res.decode('utf-8')` (get())
  - `ext_redis.py:134` — `arg-type` on `int(res)` (delete())
  - `ext_redis.py:145` — `misc` "Expected iterable as variadic argument" on `self.r.delete(*keys)` (purge())
- **Fix:** Append minimum-fix `# type: ignore[<code>]` annotations per Phase 1 D-13 strict-minimum precedent. Runtime semantics unchanged.
- **Files modified:** `cement/ext/ext_redis.py`, `CHANGELOG.md`
- **Verification:** `pdm run mypy cement/ext/ext_redis.py` returns "Success: no issues found"; `tests/ext/test_ext_redis.py` passes within full suite (316/316, 100%).
- **Committed in:** `bf567f2b` (fix(type): resolve redis 7 typing drift in ext_redis)

**2. [Rule 1 - Bug / D-04 atomic split] Mypy drift surfaced post-bump in `cement/ext/ext_watchdog.py`**
- **Found during:** Sub-step A.4 (post-bump `make comply` smoke test) — predicted by RESEARCH.md Pitfall 4
- **Issue:** Watchdog 6.0.0 ships precise type stubs for `Observer.schedule()` / `start()` / `stop()`, making the legacy `# type: ignore` comments fire as `unused-ignore` errors:
  - `ext_watchdog.py:108` — schedule()
  - `ext_watchdog.py:120` — start()
  - `ext_watchdog.py:133` — stop()
- **Fix:** Remove the 3 unused-ignore comments. The framework-Meta `# type: ignore` on line 73 (MetaMixin pattern) intentionally kept.
- **Files modified:** `cement/ext/ext_watchdog.py`, `CHANGELOG.md`
- **Verification:** `make comply` exits 0; `tests/ext/test_ext_watchdog.py` passes within full suite (316/316, 100%).
- **Committed in:** `54253244` (fix(type): drop unused type-ignores in ext_watchdog vs watchdog 6)

---

**Total deviations:** 2 auto-fixed (both Rule 1 bugs / D-04 atomic-split drift-fixes — exactly the shape Phase 1 D-04 anticipated for major-version bumps).
**Impact on plan:** Both deviations were planned-for under Sub-step B (conditional drift-fix). Plan executed as written. RESEARCH.md Pitfall 4 (watchdog 4→6 risk) confirmed; redis 7 drift was an unforecasted second source but absorbed via the same D-04 mechanism.

## Issues Encountered

- **Worktree venv missing on first `pdm install`:** `pdm install` failed with `VirtualenvCreateError` because the freshly-created worktree had no `.venv/`. Resolved by running `make init` (per user MEMORY.md `feedback_recovery_make_init`), which runs `devbox install && devbox run pdm install` and provisions the worktree-local venv. Not a plan deviation — environmental setup only.
- **Resolver warnings about Sphinx ≥ 8.2 / 9.x:** PDM emitted PackageWarnings about Sphinx 8.2.x and 9.x being skipped because they require Python ≥ 3.11 and our floor is 3.10. Expected behavior given `requires-python = ">=3.10"` — the resolver correctly picked the highest-compatible Sphinx (8.1.3). Not a regression.

## Self-Check

Verifying claimed work exists:

**Files:**
- `[FOUND]` `pdm.lock` (modified — `redis = 7.4.0`, `watchdog = 6.0.0`, `tabulate = 0.10.0` confirmed via grep)
- `[FOUND]` `CHANGELOG.md` (modified — `[dev] Bump dev/extras lockfile`, `[ext.redis]`, `[ext.watchdog]` entries verified in `## 3.0.15 - DEVELOPMENT`)
- `[FOUND]` `cement/ext/ext_redis.py` (modified — 3 `# type: ignore[<code>]` annotations confirmed)
- `[FOUND]` `cement/ext/ext_watchdog.py` (modified — 3 unused `# type: ignore` removed; only line-73 Meta one remains)

**Commits:**
- `[FOUND]` `9f0f8627` (chore(deps): pdm update to current non-breaking versions)
- `[FOUND]` `bf567f2b` (fix(type): resolve redis 7 typing drift in ext_redis)
- `[FOUND]` `54253244` (fix(type): drop unused type-ignores in ext_watchdog vs watchdog 6)

**Acceptance criteria:**
- `[PASS]` `make comply` exits 0
- `[PASS]` `make test` exits 0 at 316/316 / 100% coverage
- `[PASS]` `git log -1 --pretty=%s` matches `^chore\(deps\): pdm update` (after first checkout to chore commit) — verified by hash 9f0f8627 on stack
- `[PASS]` All 3 commits' subject + body lines ≤ 78 chars (56/52/65 subjects; body all checked via awk)
- `[PASS]` `redis = "7.4.0"`, `watchdog = "6.0.0"`, `tabulate = "0.10.0"` in pdm.lock
- `[PASS]` `[dev] Bump dev/extras lockfile` entry in `## 3.0.15 - DEVELOPMENT` Misc bucket
- `[PASS]` `pyproject.toml` `[project.optional-dependencies]` byte-identical to pre-bump (`git diff aafa632a -- pyproject.toml | grep -E '^\+.*\b(colorlog|jinja2|pyYaml|redis|pylibmc|pystache|tabulate|watchdog)\b'` returns 0 lines)
- `[PASS]` Each `fix(type):` commit subject matches `^fix\(type\):` and has corresponding `[<area>]` Bugs entry in CHANGELOG
- `[PASS]` `pdm update --dry-run` post-commit returns "All packages are synced to date" — DEPS-01 acceptance verified

**Self-Check: PASSED**

## Next Phase Readiness

- **Plan 02 (DEPS-03 pip-audit):** Inherits this exact lockfile. pip-audit will scan redis 7.4.0, watchdog 6.0.0, tabulate 0.10.0, sphinx 8.1.3, requests 2.33.1, commitizen 4.13.10 + transitives. Any vulnerabilities surfaced will be documented in `02-PIP-AUDIT.md`.
- **Plan 03 (coverage gate):** Inherits the green `make test` baseline (316 passed / 100% coverage / `TOTAL 3285 stmts`). Plan 03 wires the `fail_under=100` gate around this exact baseline.
- **Plan 04 (Action pins), Plan 06 (Dependabot), Plan 07 (workflow_dispatch verify):** All build on the now-current lockfile state.
- **Phase 3 carry-over backlog:**
  - REFACTOR-02: revisit redis 7 typing with proper isinstance narrowing (replace `# type: ignore` annotations)
  - REFACTOR-04: continue ratcheting strict-minimum cleanup (e.g., the `from __future__ import annotations` carry-overs)

No blockers. Phase 2 Plan 02 is unblocked and ready to execute.

---

*Phase: 02-dependencies-ci-pipeline*
*Plan: 01*
*Completed: 2026-05-03*
