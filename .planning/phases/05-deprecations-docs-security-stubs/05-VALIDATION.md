---
phase: 5
slug: deprecations-docs-security-stubs
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-07
---

# Phase 5 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (existing — no new framework) |
| **Config file** | `pyproject.toml` `[tool.pytest.ini_options]` |
| **Quick run command** | `pdm run pytest --cov=cement.core tests/core` |
| **Full suite command** | `make test` |
| **Estimated runtime** | ~30–60 seconds (existing baseline; doc-only phase, no new tests) |

---

## Sampling Rate

- **After every task commit:** Run `make comply` (ruff + mypy) — fast doc/source linting; doc commits also trigger a `make docs` re-run for any task that edits a docstring or RST file
- **After every plan wave:** Run `make test` (full suite + 100% coverage gate) + `make docs` (zero-warnings `-W` gate after Wave covering D-08)
- **Before `/gsd-verify-work`:** All gates must be green: `make test`, `make comply`, `make docs -W`, `make audit-public-api` (per CONTEXT.md D-18 #3 around the `interface.py:102` string-quote)
- **Max feedback latency:** 60 seconds for `make comply`; ~5 seconds for individual `make docs` runs after Wave 1

---

## Per-Task Verification Map

> Populated by gsd-planner during PLAN.md generation. The planner derives one row per task with its grep/exit-code `automated_command` and the wave + requirement assignment from CONTEXT.md D-16.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| _TBD by planner_ | _TBD_ | _TBD_ | _TBD_ | _T-05-* (see threat_model in PLAN.md)_ | _N/A — doc/registry phase_ | grep / exit-code | _TBD_ | ✅ existing | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements.* DEPREC-03 is already-satisfied per CONTEXT.md (4 deprecations / 4 assertions across `tests/core/test_deprecations.py` + `tests/ext/test_ext_smtp.py:631`). No new test files required this phase.

The only Wave 0-shaped pre-flight is the `make audit-public-api` baseline check around the `cement/core/interface.py:102` string-quote — RESEARCH.md confirmed (Pitfall 1) that `audit-public-api.py` is annotation-blind and the diff is empty, so this collapses to a single sanity assertion rather than a Wave 0 install task.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| GitBook back-links resolve from `DEPRECATIONS.md` | DEPREC-02 | GitBook is off-band; not in CI | After Wave covering `DEPRECATIONS.md`, click each `https://docs.builtoncement.com/release-information/deprecations#3.0.X-Y` link and confirm it lands on the right anchor |

*All other phase behaviors have automated verification (grep + exit-code).*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s for `make comply`
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
