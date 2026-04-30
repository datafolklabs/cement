---
phase: 1
slug: tooling-baseline-python-matrix
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-29
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.x + pytest-cov 7.x + coverage 7.x (post-bump) |
| **Config file** | `pyproject.toml` `[tool.pytest.ini_options]` |
| **Quick run command** | `make test-core` (core tests only, ~5–10s) |
| **Full suite command** | `make test` (full suite + coverage + ruff + mypy) |
| **Estimated runtime** | ~30–90s for full `make test` |

---

## Sampling Rate

- **After every task commit:** Run `make comply` (ruff + mypy) — confirms the
  bumped tools still pass and no new lint/type fallout was introduced.
- **After every plan wave:** Run `make test` (ruff + mypy + pytest + coverage).
- **Before `/gsd-verify-work`:** Full `make test` green AND CI matrix
  (3.10/3.11/3.12/3.13/3.14, plus pypy3.10 if retained) green on the PR.
- **Max feedback latency:** ~90s locally; CI matrix is the ground-truth check
  per RESEARCH.md Assumption A1 (cross-version fallout transferability is
  empirically established by CI, not by single-Python local probes).

---

## Per-Task Verification Map

> Filled in by gsd-planner. Each task gets one row. The planner is the source
> of truth for `Task ID`, `Plan`, `Wave`, `Requirement`, and `Automated Command`.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| {N}-01-01 | 01 | 1 | REQ-{XX} | — / T-{N}-01 | {expected secure behavior or "N/A"} | unit / integration / lint / type / manual | `{command}` | ✅ / ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

> **Verification primitives available for Phase 1:**
> - `make comply-ruff` — ruff lint check (exits 0 = clean)
> - `make comply-mypy` — mypy type check (exits 0 = clean)
> - `make comply` — both above
> - `make test` — full pytest + coverage + comply gate
> - `make test-core` — core tests only (faster signal for foundation changes)
> - `pdm run pytest --co tests/` — collect-only (catches collection errors)
> - `grep -rn '3\.9\|sys\.version_info.*9' cement/` — confirms Success
>   Criterion #4 (no 3.9 compat shims remain)
> - `grep -E '^requires-python|^target-version|^python_version' pyproject.toml`
>   — confirms Success Criterion #4 / #5 (codified versions)

---

## Wave 0 Requirements

*Phase 1 is a tooling-and-CI phase. There is NO new runtime feature surface,
so Wave 0 does NOT need to create new test stubs.* The existing test
infrastructure (`tests/`, `make test`, CI matrix) IS the validation surface.

- [x] `tests/` — existing pytest tree provides the runtime correctness signal
- [x] `make comply` / `make test` — existing entry points
- [x] `.github/workflows/build_and_test.yml` — existing CI matrix is the
      cross-version check; Phase 1 modifies it (drops 3.9) but does not add
      new test files

> *Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Scheduled `pdm update` Action no longer drowns in ruff lint on next weekly run | TOOL-04 (no implicit drift) | `pdm.yml` runs on a `cron` — empirical proof requires waiting for the next scheduled run after merge. Phase 2 owns unblocking it; Phase 1's job is to NOT regress it. | After Phase 1 merges, watch the next scheduled run of `.github/workflows/pdm.yml`. Confirm the produced lockfile diff does NOT change ruff's compatible-release floor (`~=X.Y` pin holds). If the next ruff minor introduces new rules in a selected family, those fire as CI failures (the intended D-08 hybrid behavior) — that is success, not a regression. |
| `cement` CLI users scaffolding from `cement/cli/templates/generate/*/Dockerfile` get a working `python:3.10-alpine` image | PYVER-03 (downstream user-visible base-image bump) | Requires running `cement generate project` then `docker build` against the resulting Dockerfile. CI does not exercise the generate-templates Dockerfiles. | After merge, scaffold a fresh project: `pdm run cement generate project /tmp/cement-pyver-test`. Then `cd /tmp/cement-pyver-test && docker build .`. Image must build cleanly on the new `python:3.10-alpine` base. (Flag for changelog in Phase 6 DOCS-03.) |
| pypy3.10 in CI matrix stays green when 3.9 drops | PYVER-01 / Success Criterion #1–#3 | pypy local runs are slow and finicky; CI is the right place to prove it. | Watch the `test-all` matrix job for the `pypy3.10` row on the Phase 1 PR. If it fails, the planner needs a follow-up commit to either fix the failure or remove pypy from the matrix (decision deferred to that point per CONTEXT.md). |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 90s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
