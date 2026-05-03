---
phase: 03
slug: internal-refactor-coverage-hardening
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-03
updated: 2026-05-03
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
> Threat refs map to per-plan `<threat_model>` STRIDE register entries
> (T-03-NN-XX); `—` means the task is doc/audit-only with no new threat.

### Wave 1 — Plan 01 (audit gate installation)

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 01 | 1 | COV-01 | T-03-01-01 | Public API enumerator script (stdlib `ast` only; no new dev-dep) | smoke | `test -x scripts/audit-public-api.py && python3 scripts/audit-public-api.py \| grep -c '^cement:'` (≥14) | created in Plan 01 | ⬜ pending |
| 03-01-02 | 01 | 1 | COV-01 | T-03-01-01 | STANDALONE Makefile target (no prerequisites; D-03 invariant) | grep | `grep -E '^audit-public-api:[[:space:]]*$' Makefile \| wc -l` (must be 1) | exists; modified in Plan 01 | ⬜ pending |
| 03-01-03 | 01 | 1 | COV-01 | T-03-01-02, T-03-01-03 | Frozen baseline snapshot committed; audit gate now ENFORCING | shell | `make audit-public-api && pdm run pytest --cov=cement -x tests` | created in Plan 01 | ⬜ pending |

### Wave 2 — Plan 02 (ruff config: UP+FA enable)

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-02-01 | 02 | 2 | REFACTOR-04, COV-01 | T-03-02-01 | UP+FA family added to extend-select with refreshed AUDIT POINT comment (D-06); coverage gate held | grep + shell | `grep -cE '^\s*"(UP\|FA)"' pyproject.toml` (must be 2) + `pdm run pytest --cov=cement -x tests && make audit-public-api` | exists; modified in Plan 02 | ⬜ pending |

### Wave 3 — Plan 03 (UP family auto-fixes + CONVENTIONS refresh + UP032)

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-03-01 | 03 | 3 | REFACTOR-04, COV-01, COV-02 | — | UP006 sweep (`List`→`list`, `Dict`→`dict`, `Tuple`→`tuple`, `Type`→`type`); PEP 585 builtin generics | lint + unit | `pdm run ruff check --select UP006 cement/ tests/ && pdm run pytest --cov=cement -x tests && make audit-public-api` | mass-edit cement/, tests/ | ⬜ pending |
| 03-03-02 | 03 | 3 | REFACTOR-04, COV-01, COV-02 | — | UP007 sweep (`Union[X, Y]`→`X \| Y`); PEP 604 union syntax | lint + unit | `pdm run ruff check --select UP007 cement/ tests/ && pdm run pytest --cov=cement -x tests && make audit-public-api` | mass-edit cement/, tests/ | ⬜ pending |
| 03-03-03 | 03 | 3 | REFACTOR-04, COV-01, COV-02 | — | UP045 sweep (`Optional[X]`→`X \| None`); PEP 604 Optional folding | lint + unit | `pdm run ruff check --select UP045 cement/ tests/ && pdm run pytest --cov=cement -x tests && make audit-public-api` | mass-edit cement/, tests/ | ⬜ pending |
| 03-03-04 | 03 | 3 | REFACTOR-04 (doc) | — | CONVENTIONS.md type-annotation guidance refreshed to PEP 604/585 | grep + unit | `grep -c 'PEP 604' .planning/codebase/CONVENTIONS.md` (≥1) + `pdm run pytest --cov=cement -x tests` | exists; modified in Plan 03 | ⬜ pending |
| 03-03-05 | 03 | 3 | REFACTOR-04 closeout, COV-01, COV-02 | T-03-03-01, T-03-03-02 | UP032 sweep (`%`→f-string); D-19 protected `.format(**template_dict)` callsites preserved via per-file diff | lint + unit + diff | `pdm run ruff check --select UP cement/ tests/ && pdm run pytest --cov=cement -x tests && diff /tmp/protected-foundation-pre.txt /tmp/protected-foundation-post.txt` (empty diff required) | mass-edit cement/, tests/ | ⬜ pending |

### Wave 4 — Plan 04 (FA100 future-annotations strip)

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-04-01 | 04 | 4 | REFACTOR-04 (pre-flight) | — | Pre-flight forward-ref + TYPE_CHECKING grep baseline; mypy clean BEFORE strip | grep + mypy | `grep -rn "from __future__ import annotations" cement/ \| wc -l` (record) + `pdm run mypy cement` | (no commit; capture only) | ⬜ pending |
| 03-04-02 | 04 | 4 | REFACTOR-04, COV-01 | T-03-04-01, T-03-04-02 | FA100 strip; orphaned TODO comment removed; cache reset | grep + lint + unit + mypy | `grep -rn "from __future__ import annotations" cement/ \| wc -l` (must be 0) + `make comply-ruff && pdm run pytest --cov=cement -x tests && pdm run mypy cement && make audit-public-api` | mass-edit cement/ | ⬜ pending |

### Wave 5 — Plan 05 (Any tightening + 03-VERIFICATION baselines)

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-05-01 | 05 | 5 | REFACTOR-02 (baseline) | — | Pre-tightening Any/pragma/pathlib baselines captured to 03-VERIFICATION.md | shell + unit | `grep -nE ': Any\b\|-> Any\b\|Any\]' cement/core/*.py \| wc -l` (record) + `pdm run pytest --cov=cement -x tests && make audit-public-api` | created in Plan 05 | ⬜ pending |
| 03-05-02 | 05 | 5 | REFACTOR-02, COV-01 | T-03-05-01, T-03-05-02 | Hand-tightened Any sites; surviving Any carries inline justification (D-09) | grep + unit + audit | `(POST < PRE) && pdm run pytest --cov=cement -x tests && make audit-public-api && pdm run mypy cement` | edits cement/core/ | ⬜ pending |

### Wave 6 — Plan 06 (pathlib migration: 4 scoped files)

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-06-01 | 06 | 6 | REFACTOR-03 (pre-flight) | T-03-06-02 | A7 symlink pre-flight informs `.resolve()` vs `.absolute()` decision | shell + unit | `find tests/ -type l && find cement/ -type l && pdm run pytest --cov=cement -x tests && make audit-public-api` | (no commit; capture only) | ⬜ pending |
| 03-06-02 | 06 | 6 | REFACTOR-03, COV-01 | T-03-06-01, T-03-06-02 | `cement/utils/fs.py` os.path → pathlib; public funcs still return `str` (D-12 boundary) | grep + unit + audit + lint | `grep -rn 'os\.path' cement/utils/fs.py \| grep -v '# boundary:' \| wc -l` (must be 0) + all 4 gates | edits cement/utils/fs.py | ⬜ pending |
| 03-06-03 | 06 | 6 | REFACTOR-03, COV-01 | T-03-06-01 | `cement/core/config.py` os.path.exists → pathlib (1 callsite warm-up) | grep + unit + audit | `grep -rn 'os\.path' cement/core/config.py \| grep -v '# boundary:' \| wc -l` (must be 0) + gates | edits cement/core/config.py | ⬜ pending |
| 03-06-04 | 06 | 6 | REFACTOR-03, COV-01 | T-03-06-01, T-03-06-04 | `cement/core/foundation.py` os.path internals migrated; D-19 protected lines untouched | grep + unit + audit + diff | `grep -rn 'os\.path' cement/core/foundation.py \| grep -v '# boundary:' \| wc -l` (must be 0) + `grep -c '\.format(\*\*' cement/core/foundation.py` (≥14 unchanged) | edits cement/core/foundation.py | ⬜ pending |
| 03-06-05 | 06 | 6 | REFACTOR-03, COV-01 | T-03-06-01, T-03-06-03, T-03-06-04 | `cement/core/template.py` os.path migrated; D-19 protected `.format(**template_dict)` untouched; D-24 #8 GREEN across all 4 scoped files | grep + unit + audit + lint + diff | `grep -rn 'os\.path' cement/utils/fs.py cement/core/foundation.py cement/core/template.py cement/core/config.py \| grep -v '# boundary:' \| wc -l` (must be 0) | edits cement/core/template.py | ⬜ pending |

### Wave 7 — Plan 07 (pragma:nocover audit, locked vocabulary)

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-07-01 | 07 | 7 | COV-03 (pre-flight) | — | Live pragma site count + per-file batching for Tasks 2-5 | grep + unit | `grep -rn 'pragma:[[:space:]]*no[[:space:]]*cover' cement/ \| wc -l` + `pdm run pytest --cov=cement -x tests && make audit-public-api` | (no commit; capture only) | ⬜ pending |
| 03-07-02 | 07 | 7 | COV-03 | T-03-07-01, T-03-07-02 | Batch A: cement/core/* pragma sites labeled with locked vocabulary | grep + unit | `grep -nE 'pragma:[[:space:]]*no[[:space:]]*cover' cement/core/ \| grep -vE '# (abstract method\|TYPE_CHECKING import\|platform-specific\|untestable: dynamic import\|untestable: subprocess\|untestable: signal handler\|defensive: unreachable\|version constant)' \| wc -l` (must be 0) | per-file edits cement/core/ | ⬜ pending |
| 03-07-03 | 07 | 7 | COV-03 | T-03-07-01, T-03-07-02 | Batch B: cement/ext/ first half pragma sites labeled | grep + unit | (same regex constrained to Batch B files) (must be 0) | per-file edits cement/ext/ | ⬜ pending |
| 03-07-04 | 07 | 7 | COV-03 | T-03-07-01, T-03-07-02 | Batch C: cement/ext/ second half pragma sites labeled | grep + unit | (same regex constrained to Batch C files) (must be 0) | per-file edits cement/ext/ | ⬜ pending |
| 03-07-05 | 07 | 7 | COV-03 | T-03-07-01, T-03-07-02 | Batch D: cement/cli/ + cement/utils/ pragma sites labeled; GLOBAL D-17 grep empty (D-24 #7 GREEN) | grep + all gates | GLOBAL D-17 grep returns empty + `make test && make comply-ruff && pdm run mypy cement && make audit-public-api` | per-file edits cement/cli/, cement/utils/ | ⬜ pending |

### Wave 8 — Plan 08 (finalize 03-VERIFICATION + ROADMAP)

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-08-01 | 08 | 8 | All 7 REQ + D-24 | — | superclean+init reset; capture all 9 D-24 conjunct outputs | shell + grep + ls | `make test && make comply-ruff && make comply-mypy && make audit-public-api && test -f coverage-report/index.html` + 3 grep gates (#7, #8, #9) | (no commit; capture only) | ⬜ pending |
| 03-08-02 | 08 | 8 | Documentation finalization | T-03-08-01 | 03-VERIFICATION.md finalized to status: passed; 9/9 conjuncts evidenced | grep + all gates | `grep -c 'D-24 9-Conjunct' 03-VERIFICATION.md` (≥1) + `grep -c 'status: passed' 03-VERIFICATION.md` (≥1) + re-run all 4 gates | exists; updated in Plan 08 | ⬜ pending |
| 03-08-03 | 08 | 8 | Roadmap update | — | ROADMAP.md Phase 3 row checked complete; 8/8 plans listed | grep | `grep -c '\[x\] \*\*Phase 3' .planning/ROADMAP.md` (==1) + `grep -c '8/8 ' .planning/ROADMAP.md` (≥1) | exists; updated in Plan 08 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] pytest framework + 100% coverage gate already wired by Phase 2 (D-10/D-11/D-12)
- [x] ruff + mypy compliance pipeline already wired by Phase 1 (D-08 hybrid AUDIT POINT pattern)
- [x] `scripts/audit-public-api.py` (delivered by Plan 01 Task 1 — D-02; stdlib `ast` only, no new dev-dep)
- [x] `Makefile` `audit-public-api` target (delivered by Plan 01 Task 2 — D-03; STANDALONE, NOT chained)
- [x] `.planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt` (delivered by Plan 01 Task 3 — D-04; sorted, one `module:ClassName.method` per line)

*Wave 0 infrastructure is delivered as Wave 1 of the phase plan-set
itself: Plan 01 installs the audit-public-api gate that Waves 2-8 then
keep green on every commit. Existing pytest/ruff/mypy infrastructure
(Phases 1-2) covers all other phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| UP032 protection of `.format(**template_dict)` callsites | REFACTOR-04 / D-19 | ruff cannot semantically distinguish log formatting from template substitution; per-file diff inspection is required | After running `make comply-ruff-fix` for the UP032 sweep, `git diff cement/core/foundation.py cement/core/template.py` and verify no `.format(**...)` line at the protected line numbers (D-19) was rewritten to an f-string. If a hit is found, restore and add `# noqa: UP032`. |
| Surviving `Any` justification comments | REFACTOR-02 / D-09 | Comment quality is judgment, not grep-checkable beyond presence | After the Any-tightening commit, manually review each surviving `Any` site and confirm the inline comment names the actual reason (handler contract, argparse opacity, user-arbitrary config, etc.). |
| Surviving `# boundary:` comments on `os.path.*` callsites in scoped files | REFACTOR-03 / D-14 | The grep gate (Conjunct #8) verifies presence; quality of the marker is a manual read | After pathlib migration, manually confirm each surviving `os.path.*` callsite in `cement/utils/fs.py` + `cement/core/*` has a `# boundary:` comment that explains why the boundary stays `str`. |

---

## Validation Sign-Off

- [x] Every plan task includes either an `<automated>` verify command or a Wave 0 dependency
- [ ] Sampling continuity: no 3 consecutive tasks across the phase without an automated verify (most tasks here are commit-shaped and naturally sample on `make test`) — *reviewer-asserted at execution time*
- [x] Wave 0 covers all MISSING references (audit-public-api.py + Makefile target + baseline — all delivered by Plan 01)
- [x] No watch-mode flags anywhere (CI-friendly only)
- [x] Feedback latency < 90s (full suite); < 30s (quick run)
- [x] `nyquist_compliant: true` set in frontmatter once per-task verification map is filled by the planner

**Approval:** pending
