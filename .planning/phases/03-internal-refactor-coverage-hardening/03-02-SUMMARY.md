---
phase: 03-internal-refactor-coverage-hardening
plan: 02
subsystem: tooling/ruff-config
tags: [ruff, lint-config, pyupgrade, flake8-future-annotations, audit-point, wave-2]
requires:
  - .planning/phases/03-internal-refactor-coverage-hardening/03-01-SUMMARY.md (Wave 1 — D-04 audit gate enforcing)
  - pyproject.toml [tool.ruff.lint] extend-select (Phase 1 D-08 hybrid block)
provides:
  - "ruff config with `UP` (pyupgrade) family enabled — unblocks Wave 3 UP006/UP007/UP045/UP032 fix commits"
  - "ruff config with `FA` (flake8-future-annotations) family enabled — primes Wave 4 FA100 future-annotations strip"
  - "refreshed AUDIT POINT comment naming UP+FA as highest-churn audit surfaces on next ruff bump"
affects:
  - "make comply-ruff (intentionally goes RED — 491 findings; restored to green by Wave 3/4)"
tech-stack:
  added: []
  patterns:
    - "Phase 1 D-08 hybrid AUDIT POINT pattern reused for UP+FA family (Phase 03 D-06)"
    - "D-15 coupling pattern (config-knob equivalent): extend-select change + AUDIT POINT refresh land in single atomic commit"
key-files:
  created: []
  modified:
    - pyproject.toml
    - CHANGELOG.md
decisions:
  - "Used the actual active CHANGELOG dev section header (`## 3.0.15 - DEVELOPMENT (will be released as stable/3.0.16)`) rather than the `## 3.0.16 - DEVELOPMENT` literal cited in the plan body. The active section is unambiguous (`grep -n DEVELOPMENT` returns line 3 only) and the plan's own CONTEXT canonical_refs (`§Conventions`) says `## 3.0.16 - DEVELOPMENT` while CHANGELOG.md ships as `3.0.15`. Selected the actual file state."
  - "FA family currently surfaces ZERO findings because `from __future__ import annotations` is still required by other UP-violations being unfixed. FA100 will surface naturally AFTER UP006/UP007/UP045 land per D-08 — confirms the Phase 03 D-08 ordering rationale (UP first, FA strip last)."
metrics:
  duration_minutes: 5
  completed_date: 2026-05-03
---

# Phase 03 Plan 02: Re-enable Ruff UP+FA Families — Summary

Re-enable ruff `UP` (pyupgrade) family + add `FA` (flake8-future-annotations)
family to `[tool.ruff.lint] extend-select` with refreshed AUDIT POINT comment
(Phase 03 D-06). Single atomic config-only commit.

## Wave 2 Completion Status

- **Wave:** 2 (depends on Wave 1 complete — verified at 03-01-SUMMARY.md)
- **Tasks executed:** 1 / 1
- **Commits:** 1 (`b8427466`)
- **Files modified:** 2 (`pyproject.toml`, `CHANGELOG.md`)
- **Files in `cement/` source tree touched:** 0 (config-only)

## Commit

| Hash | Subject | Files |
|------|---------|-------|
| `b8427466` | chore(ruff): re-enable UP family with AUDIT POINT comment | pyproject.toml, CHANGELOG.md |

Subject = 57 chars (limit 78). All body lines wrap ≤ 78 chars.

## Verification Results

| Gate | Command | Result | Required Status |
|------|---------|--------|-----------------|
| Audit-public-api | `make audit-public-api` | exit 0 | MUST be green ✓ |
| Coverage gate | `pdm run pytest --cov=cement -x tests` | exit 0, 100% coverage (3285/3285 stmts, 316 passed) | MUST be green ✓ |
| Ruff comply | `make comply-ruff` | exit 2 (RED — 491 findings) | EXPECTED to go red ✓ |
| UP/FA pattern markers | `grep -E '^\s*"UP"' pyproject.toml \| wc -l` | 1 | == 1 ✓ |
|  | `grep -E '^\s*"FA"' pyproject.toml \| wc -l` | 1 | == 1 ✓ |
| SIM excluded | `grep -E '^\s*"SIM"' pyproject.toml \| wc -l` | 0 | == 0 ✓ |
| AUDIT POINT refreshed | `grep -c 'Phase 03 D-06' pyproject.toml` | 4 | ≥ 1 ✓ |

## UP+FA Finding Count (Wave 3 Expected Fix Volume)

Total: **491 errors** (378 auto-fixable via `make comply-ruff-fix`).

Per-rule breakdown:

| Rule | Count | Description | Auto-fixable |
|------|-------|-------------|--------------|
| UP006 | 181 | Use `list` / `dict` / `tuple` instead of `List` / `Dict` / `Tuple` (PEP 585) | yes |
| UP045 | 66 | Use `X \| None` instead of `Optional[X]` (PEP 604) | yes |
| UP035 | 59 | Import deprecated (e.g. `from typing import List` → `from collections.abc import ...`) | partial |
| UP031 | 58 | Use format specifiers instead of percent format (`'%s' % x` → f-string) | yes |
| UP004 | 47 | Class inherits from `object` (drop) | yes |
| UP007 | 30 | Use `X \| Y` instead of `Union[X, Y]` (PEP 604) | yes |
| UP008 | 29 | Use `super()` instead of `super(__class__, self)` | yes |
| UP015 | 15 | Unnecessary mode argument to `open()` | yes |
| UP028 | 2 | Replace `yield` over `for` loop with `yield from` | yes |
| UP026 | 2 | `mock` is removed; use `unittest.mock` | yes |
| UP025 | 1 | Remove unicode literal prefix (e.g., `u"..."`) | yes |
| UP024 | 1 | Replace alias exception (`EnvironmentError`, `IOError`) with `OSError` | yes |
| **FA100** | **0** | **`from __future__ import annotations` removable** | **(see below)** |
| **FA102** | **0** | **`from __future__ import annotations` missing where required** | — |

**FA gate observation — primes Phase 03 D-08:** FA100/FA102 surfacing
ZERO findings is **expected** for this commit. `from __future__ import
annotations` is currently REQUIRED in all 28 files because their typing
imports (`from typing import List`, `Optional`, `Union`, etc.) and PEP
585/604 syntax usage create circular obligations that the future-import
papers over. Once UP006/UP007/UP045 land in Wave 3 (and the `typing`
imports prune to the modern surface), FA100 will surface — at which
point the Wave 4 `fix(lint): resolve FA100 future-annotations imports`
commit becomes well-defined. This confirms the D-08 ordering rationale
and the planner's note in 03-CONTEXT.md.

## Wave 3 Planning Hint (Per-Rule Commit Sequence)

Per Phase 1 D-04 family-split discipline, Wave 3 splits as:

1. `fix(lint): resolve UP006 List → list` (181 sites — biggest)
2. `fix(lint): resolve UP007 Union → |` (30 sites)
3. `fix(lint): resolve UP045 Optional → X | None` (66 sites)
4. `fix(lint): resolve UP035 deprecated typing imports` (59 sites — gated on UP006/UP007/UP045 landing first; many UP035 fixes follow naturally from those)
5. `fix(lint): resolve UP031 printf → f-string` (58 sites — UP032 sibling; CONTEXT.md cites ~14 sites but ruff finds 58 — discrepancy noted; `.format(**template_dict)` sites in foundation.py 1359..1567 + template.py 359+ MUST stay untouched per D-19; verify per-file diff before commit)
6. `fix(lint): resolve UP004 useless object inheritance` (47 sites)
7. `fix(lint): resolve UP008 super() simplification` (29 sites)
8. `fix(lint): resolve UP015 redundant open() mode` (15 sites)
9. `fix(lint): resolve UP028/UP026/UP025/UP024 misc modernization` (6 sites combined — single sweep commit acceptable)

After UP006/UP007/UP045 land, re-run `pdm run ruff check --select FA cement/ tests/` to surface FA100 — that becomes Wave 4's commit.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] CHANGELOG active dev section header mismatch**
- **Found during:** Task 1, step 4 (CHANGELOG entry)
- **Issue:** Plan body literally specified `## 3.0.16 - DEVELOPMENT` for the CHANGELOG section header, but the actual `CHANGELOG.md:3` ships as `## 3.0.15 - DEVELOPMENT (will be released as stable/3.0.16)`.
- **Fix:** Inserted the new `[dev]` Misc bullet under the actual active section (line 67, after the Phase 03 D-02..D-05 entry from Plan 01). No content change to the section header.
- **Files modified:** CHANGELOG.md
- **Commit:** `b8427466`
- **Rationale:** Plan body text vs. file state mismatch. The active dev section is unambiguous (only one `DEVELOPMENT` token in the file). The user's CLAUDE.md `Changelog Maintenance` policy says "append entries to the active `## X.Y.Z - DEVELOPMENT` section" — this plan honors the policy, not the literal version-string in the plan body. Recommend planner refresh references to `## 3.0.16 - DEVELOPMENT` in CONTEXT.md / 03-PATTERNS.md / future plans (or harmonize the CHANGELOG header to `## 3.0.16 - DEVELOPMENT` in a separate `docs:` commit when the release-cut convention triggers).

**2. [Rule 1 - Bug] Plan-frontmatter `requirements:` declaration vs. acceptance ambiguity**
- **Found during:** State update (`gsd-sdk requirements mark-complete REFACTOR-04 COV-01`)
- **Issue:** Plan frontmatter declares `requirements: [REFACTOR-04, COV-01]`. SDK `mark-complete` marked both as `[x]` in REQUIREMENTS.md. But REFACTOR-04 acceptance ("Modern stdlib idioms applied where backward-compatible — f-strings everywhere, contextlib helpers, functools.cached_property") fires when the UP032 sweep LANDS in Wave 3+, not when ruff is configured to detect them. COV-01 ("100% coverage report; any drift closed before milestone completion") is multi-phase ongoing — Plan 01 already marked the COV-01 checkbox `[x]` (this commit's coverage gate stayed green, consistent with that).
- **Fix:** Reverted the SDK mark on REQUIREMENTS.md (`git checkout .planning/REQUIREMENTS.md`). Both lines stay `[ ]`/`Pending` — they will be marked at the natural gate (Phase 03 D-24 conjunction at phase-end Plan 08, OR mid-phase when Wave 3's UP032 commit actually applies the f-string rewrites).
- **Files modified:** none (revert was the fix)
- **Rationale:** The plan declared requirements that this Wave 2 plan UNBLOCKS but does not by itself SATISFY. Marking complete prematurely would falsify the requirement-trace gate and leak credit. Recommend a future planner refinement: split `requirements:` declaration into `unblocks:` (declared here) vs `satisfies:` (actually completed here — empty for Wave 2). Phase 03 D-24 acceptance gate is the right place for these marks.

### Authentication Gates

None — config-only change with no external services touched.

## Threat Surface Scan

Config-only change; no new files in `cement/`. Threat register entry
T-03-02-01 (Tampering of `pyproject.toml extend-select`) per plan
threat_model — `accept` disposition with AUDIT POINT comment as the
long-term mitigation. **No new threat flags surfaced** beyond what the
plan already declared.

## Acceptance Criteria — Plan Match

| Criterion | Status |
|-----------|--------|
| `pyproject.toml` extend-select contains `"UP"` exactly once | ✓ (1 match) |
| `pyproject.toml` extend-select contains `"FA"` exactly once | ✓ (1 match) |
| Refreshed AUDIT POINT comment present (`grep 'Phase 03 D-06'`) | ✓ (4 matches across new sibling tags + comment block) |
| `SIM` NOT added | ✓ (0 matches) |
| `pdm run pytest --cov=cement -x tests` exits 0 with 100% coverage | ✓ |
| `make audit-public-api` exits 0 | ✓ |
| `make comply-ruff` may exit non-zero (EXPECTED) | ✓ (exit 2, 491 findings) |
| Single commit with subject ≤ 78 chars | ✓ (57 chars) |
| Commit body lines wrap at ≤ 78 chars | ✓ |
| Commit touches exactly 2 files | ✓ (pyproject.toml, CHANGELOG.md) |
| Commit body includes UP+FA finding count | ✓ (491 total + per-rule breakdown) |
| CHANGELOG.md has new `[dev]` entry referencing `UP` and `FA` | ✓ |

## D-24 Conjunct Status

| Conjunct | Status After This Plan |
|----------|------------------------|
| #1 — `make test` 100% coverage | green ✓ |
| #2 — `make comply-ruff` | RED (intentional; restored by Wave 3) |
| #3 — `make comply-mypy` | green (config change does not affect mypy) |
| #4 — `make audit-public-api` | green ✓ (no `cement/` source touched) |
| #5 — `coverage-report/index.html` generates | green ✓ (run as side effect of pytest) |
| #6..#9 (Any reduction, pragma vocab, os.path scope, future-annotations strip) | not yet evaluated (Wave 3+) |

## Self-Check: PASSED

- File `pyproject.toml` exists at `/Users/derks/Development/DFL/cement/pyproject.toml` and contains `"UP"` + `"FA"` lines
- File `CHANGELOG.md` exists and contains the new Misc bullet
- Commit `b8427466` exists in `git log`
- All claimed verification commands re-run interactively show the documented results

---

*Plan: 03-02 (Wave 2)*
*Depends on: Plan 01 (Wave 1)*
*Unblocks: Plan 03 (Wave 3 — UP+FA per-rule fix sweep)*
