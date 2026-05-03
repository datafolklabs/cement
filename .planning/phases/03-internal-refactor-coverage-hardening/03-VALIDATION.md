---
phase: 03
slug: internal-refactor-coverage-hardening
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-03
---

# Phase 03 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Source-of-truth acceptance: D-24 9-conjunct in
> `03-CONTEXT.md` (mirrors RESEARCH.md `## Validation Architecture`).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 4.3.1+ with pytest-cov 2.6.1+ (already wired by Phase 2) |
| **Config file** | `pyproject.toml` (`[tool.pytest.ini_options]`, `[tool.coverage.run]`, `[tool.coverage.report] fail_under = 100`) |
| **Quick run command** | `pdm run pytest --cov=cement -x tests` |
| **Full suite command** | `make test` |
| **Estimated runtime** | ~30s quick / ~90s full local single-Python |

---

## Sampling Rate

- **After every task commit:** Run `pdm run pytest --cov=cement -x tests`
- **After every plan wave:** Run `make test` (asserts 100% coverage)
- **Before `/gsd-verify-work`:** Full D-24 conjunction must be green
  (see "D-24 Acceptance Conjunction" below)
- **Max feedback latency:** 90s (full suite); 30s (quick run)

---

## D-24 Acceptance Conjunction (Phase Verification)

Every plan in this phase MUST keep these passing on every commit. The
final verify-phase pass re-runs the full conjunction.

| # | Gate | Command | Expected |
|---|------|---------|----------|
| 1 | 100% coverage / REFACTOR-01 / COV-01 | `make test` | exit 0; coverage 100% |
| 2 | ruff with UP family enabled (TOOL-04) | `make comply-ruff` | exit 0 |
| 3 | mypy hint changes (REFACTOR-02) | `make comply-mypy` | exit 0 |
| 4 | Public API baseline match (D-04 / SC-3) | `make audit-public-api` | exit 0; diff empty |
| 5 | Coverage HTML clean (COV-02) | `make test` then inspect `coverage-report/` | no warnings emitted |
| 6 | Any-count strictly lower (REFACTOR-02 / SC-4) | `grep -E ': Any\b\|-> Any\b\|Any\]' cement/core/*.py \| wc -l` | post-count < pre-count (recorded in 03-VERIFICATION.md) |
| 7 | pragma vocabulary lock (COV-03 / SC-2) | `grep -nE 'pragma:[[:space:]]*no[[:space:]]*cover' cement/ \| grep -vE '# (abstract method\|TYPE_CHECKING import\|platform-specific\|untestable: dynamic import\|untestable: subprocess\|untestable: signal handler\|defensive: unreachable\|version constant)'` | empty output |
| 8 | os.path boundary (REFACTOR-03 / SC-5) | `grep -rn 'os\.path' cement/utils/fs.py cement/core/` | empty OR all hits tagged `# boundary:` on same/adjacent line |
| 9 | future-annotations cleanup (D-08) | `grep -rn 'from __future__ import annotations' cement/` | empty output |

---

## Per-Task Verification Map

> Filled in by the planner during PLAN.md authoring. Every executable
> task gets one row mapping to which conjunct(s) it strengthens or holds.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 01 | 1 | REFACTOR-01..04, COV-01..03 | — | Public API baseline captured before any refactor | smoke | `python scripts/audit-public-api.py > /tmp/baseline.txt && diff -u .planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt /tmp/baseline.txt` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] pytest framework + 100% coverage gate already wired by Phase 2 (D-10/D-11/D-12)
- [x] ruff + mypy compliance pipeline already wired by Phase 1 (D-08 hybrid AUDIT POINT pattern)
- [ ] `scripts/audit-public-api.py` (NEW — D-02; stdlib `ast` only, no new dev-dep)
- [ ] `Makefile` `audit-public-api` target (NEW — D-03; STANDALONE, NOT chained)
- [ ] `.planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt` (NEW — D-04; sorted, one `module:ClassName.method` per line)

*Existing infrastructure covers all phase requirements except the
audit-public-api affordance, which Phase 03 introduces and retains as a
permanent dev affordance per D-05.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| UP032 protection of `.format(**template_dict)` callsites | REFACTOR-04 / D-19 | ruff cannot semantically distinguish log formatting from template substitution; per-file diff inspection is required | After running `make comply-ruff-fix` for the UP032 sweep, `git diff cement/core/foundation.py cement/core/template.py` and verify no `.format(**...)` line at the protected line numbers (D-19) was rewritten to an f-string. If a hit is found, restore and add `# noqa: UP032`. |
| Surviving `Any` justification comments | REFACTOR-02 / D-09 | Comment quality is judgment, not grep-checkable beyond presence | After the Any-tightening commit, manually review each surviving `Any` site and confirm the inline comment names the actual reason (handler contract, argparse opacity, user-arbitrary config, etc.). |
| Surviving `# boundary:` comments on `os.path.*` callsites in scoped files | REFACTOR-03 / D-14 | The grep gate (Conjunct #8) verifies presence; quality of the marker is a manual read | After pathlib migration, manually confirm each surviving `os.path.*` callsite in `cement/utils/fs.py` + `cement/core/*` has a `# boundary:` comment that explains why the boundary stays `str`. |

---

## Validation Sign-Off

- [ ] Every plan task includes either an `<automated>` verify command or a Wave 0 dependency
- [ ] Sampling continuity: no 3 consecutive tasks across the phase without an automated verify (most tasks here are commit-shaped and naturally sample on `make test`)
- [ ] Wave 0 covers all MISSING references (audit-public-api.py + Makefile target + baseline)
- [ ] No watch-mode flags anywhere (CI-friendly only)
- [ ] Feedback latency < 90s (full suite); < 30s (quick run)
- [ ] `nyquist_compliant: true` set in frontmatter once per-task verification map is filled by the planner

**Approval:** pending
