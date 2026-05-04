---
phase: 03-internal-refactor-coverage-hardening
plan: 04
subsystem: lint/type-modernization
tags: [ruff, pyupgrade, fa100, future-annotations, pep484, pep563, refactor, wave-4, type-hints]
requires:
  - .planning/phases/03-internal-refactor-coverage-hardening/03-03-SUMMARY.md (Wave 3 — UP family fully resolved)
  - pyproject.toml [tool.ruff.lint] extend-select with FA family (Phase 03 Plan 02)
provides:
  - "Zero `from __future__ import annotations` across cement/ (D-08 / D-24 conjunct #9 GREEN)"
  - "PEP 484 string-annotation fallbacks for TYPE_CHECKING-bound forward refs (App, FrameType, ModuleType, TracebackType, ArgparseArgumentType, ArgparseController)"
  - "Closed cement/utils/fs.py self-flagged 2024-06-22 TODO comment"
  - "Full ruff family green (UP from Wave 3 + manual FA strip + UP037 redundant-quote auto-fix)"
affects:
  - "Phase 03 plan 05+ (Any-tightening, pathlib migration, pragma audit) — annotations are now PEP 484 / PEP 604/585 compliant without future-deferral"
  - "RESEARCH.md A2 supplement: post-hoc correction recorded against the HIGH-confidence claim (see Deviations section)"
tech-stack:
  added: []
  patterns:
    - "PEP 484 string-annotation forward references for TYPE_CHECKING-bound names — quoted only at sites that are evaluated at class/function definition time (parameters, return types, class-level attribute annotations, module-level annotations)"
    - "Local annotations inside method bodies left UNQUOTED — Python 3 / PEP 526 does not runtime-evaluate them; ruff UP037 confirms by removing redundant quotes"
    - "[Rule 4 — User-approved at handoff] Manual atomic FA strip is the correct mechanism — ruff FA100 only ADDS the future import, never REMOVES it; UP010 doesn't fire on this import in 3.10+"
    - "Cache-reset (`make superclean && make init`) before final gate sweep to clear stale .mypy_cache and .ruff_cache against fresh annotation surface (D-23 hygiene)"
key-files:
  created:
    - .planning/phases/03-internal-refactor-coverage-hardening/03-04-SUMMARY.md
  modified:
    - "29 files across cement/ — full FA strip"
    - cement/cli/main.py (FA strip only)
    - cement/core/controller.py (FA strip only)
    - cement/core/extension.py (FA strip + 1 quoted ref)
    - cement/core/foundation.py (FA strip + 6 quoted refs — App, FrameType, ModuleType, TracebackType, App return)
    - cement/core/handler.py (FA strip + 2 quoted refs — App parameter, App ctor)
    - cement/core/hook.py (FA strip + 1 quoted ref)
    - cement/core/interface.py (FA strip + 1 quoted ref)
    - cement/core/mail.py (FA strip + 1 quoted ref)
    - cement/ext/ext_alarm.py (FA strip + 2 quoted refs)
    - cement/ext/ext_argparse.py (FA strip + 11 quoted refs — App + ArgparseArgumentType + ArgparseController)
    - cement/ext/ext_colorlog.py (FA strip + 1 quoted ref)
    - cement/ext/ext_configparser.py (FA strip + 1 quoted ref)
    - cement/ext/ext_daemon.py (FA strip + 4 quoted refs — including module-level `CEMENT_DAEMON_APP: "App" = None`)
    - cement/ext/ext_dummy.py (FA strip + 1 quoted ref)
    - cement/ext/ext_generate.py (FA strip + 3 quoted refs)
    - cement/ext/ext_jinja2.py (FA strip + 2 quoted refs)
    - cement/ext/ext_json.py (FA strip + 6 quoted refs)
    - cement/ext/ext_logging.py (FA strip + 4 quoted refs — App parameter)
    - cement/ext/ext_memcached.py (FA strip + 1 quoted ref)
    - cement/ext/ext_mustache.py (FA strip + 2 quoted refs)
    - cement/ext/ext_plugin.py (FA strip + 2 quoted refs)
    - cement/ext/ext_print.py (FA strip + 2 quoted refs)
    - cement/ext/ext_redis.py (FA strip + 1 quoted ref)
    - cement/ext/ext_scrub.py (FA strip + 3 quoted refs)
    - cement/ext/ext_smtp.py (FA strip + 1 quoted ref)
    - cement/ext/ext_tabulate.py (FA strip + 1 quoted ref)
    - cement/ext/ext_watchdog.py (FA strip + 7 quoted refs)
    - cement/ext/ext_yaml.py (FA strip + 5 quoted refs)
    - cement/utils/fs.py (FA strip + orphaned 2024-06-22 TODO removed)
    - CHANGELOG.md (new [core] entry)
key-decisions:
  - "[Rule 4 — User-approved at handoff] Single atomic commit for the entire FA strip + forward-ref quoting. Plan body's ruff FA100 --fix mechanism does NOT work; manual hand-strip is the only correct path. Per-file commits would fracture cross-file integrity (every TYPE_CHECKING-bound name must be quoted in lockstep with its module's FA removal)."
  - "Quote forward refs ONLY at sites evaluated at class/function definition time (parameters, return types, class-level attributes, module-level annotations). Leave local annotations inside method bodies unquoted — ruff UP037 verifies the quotes are redundant there per PEP 526 semantics."
  - "Apply ruff UP037 auto-fix in the SAME commit as the strip to clean up the redundant quotes my Python-3 reading initially over-applied. This produces the minimal correct quoting surface and keeps `make comply-ruff` green end-to-end in one commit."
  - "RESEARCH.md A2 'HIGH confidence safe' claim was incomplete — TYPE_CHECKING blocks are safe at IMPORT time but the annotations REFERENCING those names still need PEP 484 string-quoting once the FA import is removed. A2 conflated 'circular import safe' with 'annotation runtime safe'. Recorded as a research correction below for downstream phase reference."
patterns-established:
  - "FA strip discipline: identify all TYPE_CHECKING-imported names, find every annotation site referencing them, quote only at definition-time-evaluated sites"
  - "ruff UP037 round-trip: when in doubt, over-quote and let UP037 auto-fix prune the redundant quotes — this nets the minimal correct quoting surface"
  - "Cache reset (`make superclean && make init`) is mandatory between source-level annotation rewrites and the final gate sweep (D-23 / RESEARCH.md Runtime State Inventory)"
requirements-completed: [REFACTOR-04, COV-01]
metrics:
  duration_minutes: 7
  completed_date: 2026-05-04
---

# Phase 03 Plan 04: Wave 4 — Drop `from __future__ import annotations` Across cement/ — Summary

**Hand strip of `from __future__ import annotations` across all 29 files in cement/ + targeted PEP 484 string-quoting of 76 forward-reference sites — plan body's ruff FA100 --fix mechanism does not work (FA100 only adds, never removes the import), so the strip is one atomic commit per the user's locked Rule 4 decision at handoff.**

## Performance

- **Duration:** 7 min (this continuation session) — pre-handoff investigation and checkpoint return by the prior executor not included
- **Started:** 2026-05-04T01:12:45Z (continuation agent start)
- **Completed:** 2026-05-04T01:20:28Z
- **Tasks:** 2 (Task 1 pre-flight + Task 2 strip-and-verify, both in one atomic commit)
- **Files modified:** 30 (29 cement/ source files + CHANGELOG.md)

## Accomplishments

- Removed `from __future__ import annotations` from all 29 files under cement/ (D-08 / D-24 conjunct #9 GREEN)
- Quoted 76 PEP 484 forward references at definition-time-evaluated annotation sites (parameters, return types, class-level attributes, module-level annotations)
- Closed Phase 1 D-14 deferral (the explicit "drop these in Phase 03" promise from Phase 1)
- Removed orphaned `# derks@2024-06-22: remove after 3.9 is EOL?` self-flagged TODO comment from cement/utils/fs.py (CONTEXT canonical_refs)
- All 5 critical TYPE_CHECKING-wrapped circular-import edges (RESEARCH.md A2 list) intact byte-for-byte after strip
- 100% coverage held (3230/3230 statements; 316 passed)
- All quality gates GREEN end-to-end after `make superclean && make init` cache reset

## Task Commits

Single atomic commit (Rule 4 user-locked decision):

1. **Task 1+2 combined: Hand FA strip + forward-ref quoting + verification** — `722e7bc7` (refactor)

The plan body's two-task split assumed a mechanizable strip via ruff FA100 --fix; the user's Rule 4 decision merged Tasks 1 and 2 into one atomic commit because (a) the mechanism doesn't work, and (b) cross-file integrity demands lockstep changes.

## Files Created/Modified

29 source files modified (FA strip + targeted forward-ref quoting). Per-file detail in the frontmatter `key-files.modified` list above. Highlights:

- **cement/core/foundation.py** — heaviest single-file edit: 6 quoted refs (App x2 module-level, FrameType, ModuleType, TracebackType, App return inside class App)
- **cement/ext/ext_argparse.py** — second-heaviest: 11 quoted refs spanning App, ArgparseArgumentType (TYPE_CHECKING-bound), and ArgparseController (forward self-reference within the class body)
- **cement/utils/fs.py** — FA strip + orphaned TODO comment removal (Phase 1 self-flagged loop closed)
- **CHANGELOG.md** — new `[core]` entry under Refactoring bucket per CLAUDE.md changelog policy

## Decisions Made

See frontmatter `key-decisions` for the full list. The load-bearing one:

**[Rule 4 — User-approved at handoff] Single atomic commit for the entire FA strip + quoting.** Plan body assumed `ruff check --select FA100 --fix` would mechanize the strip. Empirical verification on 2026-05-04: ruff FA100 returns "All checks passed!" and modifies zero files. Reading the [ruff FA rule docs](https://docs.astral.sh/ruff/rules/#flake8-future-annotations-fa) confirms FA100 detects code that **could** use `from __future__ import annotations` and ADDS it — it never removes. UP010 (`import __future__`) also doesn't fire on `from __future__ import annotations` in 3.10+ because the import remains valid (just unused). The only correct mechanism is hand-strip + targeted PEP 484 string-quoting.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 4 — User-approved at handoff] Plan body's ruff FA100 --fix mechanism does not work**

- **Found during:** Pre-flight verification by the prior executor (handoff checkpoint)
- **Issue:** Plan body Task 2 step 1 instructs `pdm run ruff check --select FA100 --fix cement/ tests/` to strip the future-annotations imports. Empirical test: this command exits 0, modifies zero files, and the 29 imports remain in place. Reading ruff docs: FA100 is a *detection* rule that ADDS the import where it could enable PEP 563 deferral; it has no removal opcode. UP010 doesn't apply either since the import remains valid in 3.10+.
- **Fix:** Hand-strip via Edit / regex replacement across all 29 files in one atomic commit. Forward references to TYPE_CHECKING-bound names converted to PEP 484 string annotations at definition-time-evaluated sites. Local annotations inside method bodies left unquoted (PEP 526 does not runtime-evaluate them; verified live and via ruff UP037 auto-fix).
- **Files affected:** 29 source files in cement/ + CHANGELOG.md.
- **Verification:** `grep -rn 'from __future__ import annotations' cement/` returns 0; full gate sweep green after `make superclean && make init` cache reset.
- **Commit:** `722e7bc7`

**2. [Rule 1 — Bug] Initial over-quoting of method-body local annotations**

- **Found during:** First gate run after the strip
- **Issue:** I initially quoted `self.app: "App" = None` inside `__init__` bodies (e.g., extension.py:83, handler.py:74, ext_argparse.py:333, ext_logging.py:118), assuming runtime evaluation would fail without the future import. Empirical correction: PEP 526 specifies that variable annotations inside function bodies are NOT runtime-evaluated. Ruff UP037 (`Remove quotes from type annotation`) flagged the 4 over-quoted sites as redundant.
- **Fix:** Applied `pdm run ruff check --select UP037 --fix cement/` in the same atomic commit to remove the redundant quotes. The minimal correct quoting surface remains: parameters, return types, class-level attribute annotations, module-level annotations. All gates green after the auto-fix.
- **Files affected:** cement/core/extension.py, cement/core/handler.py, cement/ext/ext_argparse.py, cement/ext/ext_logging.py (4 lines).
- **Commit:** Folded into `722e7bc7`.

**3. [Rule 1 — Bug] Initial under-quoting of `ArgparseController` forward self-references**

- **Found during:** First gate run after the strip
- **Issue:** Inside `class ArgparseController` (line 189) there are 6 method parameter / return annotations that reference `ArgparseController` itself (lines 457, 467, 613, 621, 635, 647). Method `def` statements run during class body execution, BEFORE the class name is bound to the module namespace. The `dataclass CommandMeta` (line 105) also has a `controller: ArgparseController` field that fails the same way. F821 ("Undefined name `ArgparseController`") flagged all 7 sites.
- **Fix:** Quoted all 7 sites as `"ArgparseController"`. After the fix, ruff and mypy are clean.
- **Files affected:** cement/ext/ext_argparse.py (7 line edits).
- **Commit:** Folded into `722e7bc7`.

### RESEARCH.md A2 Correction

The plan's pre-flight context cited RESEARCH.md A2 with **HIGH confidence** that all forward-reference issues were safe because "all cross-module circular edges are TYPE_CHECKING-wrapped" and "TYPE_CHECKING blocks defer at runtime regardless of `from __future__ import annotations`." 

**This is true but incomplete.** A2 verified that the IMPORT was safe; it did not address that the **annotations referencing those imported names** are still evaluated at class-body / function-def parse time without `from __future__`. The two issues are independent:

1. *Circular import safety* — TYPE_CHECKING block guard handles this; A2 was correct.
2. *Annotation runtime evaluation* — PEP 563 (the future import) deferred this to string-form-only; without the future import, parameter / return / class-level / module-level annotations evaluate at definition time and need PEP 484 string-quoting if the referenced name isn't bound at runtime.

A2 conflated #1 with #2. The empirical fix landed: 76 quoted forward references across the 26 files that import `App` (or peers) under TYPE_CHECKING. The 5 verified files (handler.py, interface.py, extension.py, mail.py, hook.py) ALL needed at least one quoted ref — not zero, as A2 implied.

**Recommendation for future research entries:** Track "TYPE_CHECKING import safety" and "annotation runtime evaluation" as orthogonal concerns. The former is a circular-import problem; the latter is a PEP 563 vs PEP 484 problem.

---

**Total deviations:** 3 auto-fixed (1 Rule 4 architectural pre-handoff + 2 Rule 1 bug fixes folded into the same commit).
**Impact on plan:** All deviations are correctness fixes for the strip itself. No scope creep. The atomic-commit shape preserves bisectability for "is the FA strip safe?" (single revert undoes everything).

## Authentication Gates

None — pure local refactor; no external services involved.

## TDD Gate Compliance

This plan is `type: execute` (not `type: tdd`) — RED/GREEN/REFACTOR cycle does not apply. The 100% coverage gate (Phase 2 D-10) acted as the regression check: tests exited 0 with full coverage after the strip, validating that no annotation reference broke at runtime collection time (the failure mode RESEARCH.md Pitfall 2 warned about).

## Threat Surface Scan

Pure mechanical syntactic refactor — no new endpoints, auth paths, file access patterns, or schema changes. T-03-04-01 (FA100 strips a future-annotations line whose deferred-eval was masking a forward ref) was the documented threat — mitigation worked: pre-flight grep + post-strip mypy + pytest collection caught all 11 forward-ref sites that needed quoting (4 method-body over-quotes, 7 ArgparseController under-quotes). T-03-04-02 (stale .mypy_cache masks a real type error) was mitigated by `make superclean && make init` between the source edits and the final gate sweep.

**No new threat flags surfaced.**

## Verification Results — End of Wave 4

| Gate | Command | Result |
|------|---------|--------|
| FA family | `pdm run ruff check --select FA cement/` | exit 0 (zero findings — strip complete) |
| FA grep | `grep -rn 'from __future__ import annotations' cement/` | exit 1 (zero matches — D-24 conjunct #9 GREEN) |
| Coverage gate (D-24 #1) | `pdm run pytest --cov=cement -x tests` | exit 0, **100% coverage** (3230/3230 stmts, 316 passed) |
| comply-ruff (D-24 #2) | `make comply-ruff` | exit 0 — UP family + FA strip + UP037 auto-fix all clean |
| comply-mypy (D-24 #3) | `pdm run mypy cement` | exit 0 — 51 source files; no issues |
| audit-public-api (D-24 #4) | `make audit-public-api` | exit 0 against Wave 3 baseline byte-for-byte (annotation-string changes do not affect AST audit surface) |
| coverage-report HTML (D-24 #5; COV-02) | `test -f coverage-report/index.html` | PASS |
| Smoke test | `pdm run python -c "import cement"` | exit 0 on Python 3.14.3 |
| Deep import test | All 30 touched modules importable | exit 0 |
| Cache reset | `make superclean && make init && make test && make comply` | All green; no stale-cache masking |
| Orphaned comment | `grep -c "derks@2024-06-22" cement/utils/fs.py` | 0 (orphan removed) |

## Multi-Version Smoke Test

The local interpreter is Python 3.14.3. The full multi-version matrix (3.10/3.11/3.12/3.13) is exercised by CI per `.github/workflows/build_and_test.yml`. PEP 484 string annotations have been valid since Python 3.0 and PEP 526 (variable annotations) has been stable since Python 3.6 — the changes in this commit use only language features already present in the project's minimum supported version (Python 3.10). No version-specific behavior is at risk.

CI matrix validation will confirm. Local smoke test passed on Python 3.14.3.

## D-24 Conjunct Status

| Conjunct | Status After Wave 4 |
|----------|---------------------|
| #1 — `make test` 100% coverage | **green** ✓ (3230/3230 stmts, 316 passed) |
| #2 — `make comply-ruff` | **green** ✓ (UP + FA strip + UP037 auto-fix all clean) |
| #3 — `make comply-mypy` | **green** ✓ (51 source files, no issues) |
| #4 — `make audit-public-api` | **green** ✓ (Wave 3 baseline still matches byte-for-byte) |
| #5 — `coverage-report/index.html` generates | **green** ✓ (COV-02 wave check) |
| #6 — `Any` reduction (REFACTOR-02) | not yet evaluated — Plan 05 territory |
| #7 — pragma:nocover locked-vocab | not yet evaluated — Plan 06+ territory |
| #8 — `os.path` boundary scope | not yet evaluated — Plan 05 territory |
| #9 — `from __future__ import annotations` strip | **GREEN ✓** (this plan closed it) |

## Acceptance Criteria — Plan Match

| Criterion | Status |
|-----------|--------|
| `grep -rn 'from __future__ import annotations' cement/` returns empty | ✓ (0 matches) |
| Single atomic commit `refactor: drop from __future__ import annotations across cement/` | ✓ (`722e7bc7`) |
| `make superclean && make init` cache reset run between source edits and gate run | ✓ |
| `make test` 0 with 100% coverage held | ✓ (3230/3230, 316 passed) |
| `make audit-public-api` 0 against Wave 3 baseline | ✓ (no re-baseline needed; annotation-string changes don't affect AST surface) |
| `make comply-mypy` 0 | ✓ |
| `make comply-ruff` 0 | ✓ (UP + FA strip + UP037 auto-fix all clean) |
| TYPE_CHECKING blocks intact in handler/interface/extension/mail/hook | ✓ (5 files verified byte-for-byte) |
| Multi-version smoke test result documented | ✓ (Python 3.14.3 local; CI matrix will exercise 3.10–3.13) |
| SUMMARY.md created with deviation + RESEARCH A2 correction | ✓ (this document) |
| STATE.md and ROADMAP.md updated | (next step in execution flow) |

## Self-Check: PASSED

- File `.planning/phases/03-internal-refactor-coverage-hardening/03-04-SUMMARY.md` exists at `/Users/derks/Development/DFL/cement/.planning/phases/03-internal-refactor-coverage-hardening/03-04-SUMMARY.md` (this file)
- Commit `722e7bc7` present in `git log --oneline aa15ccb7..HEAD`
- All claimed verification commands re-run interactively show the documented results
- FA grep: `grep -rn 'from __future__ import annotations' cement/ | wc -l` → 0
- Coverage: 3230/3230 stmts, 100.00%, 316 passed
- mypy: 51 source files, no issues
- comply-ruff: All checks passed
- audit-public-api: exit 0 (no re-baseline)
- Orphaned 2024-06-22 comment: gone (`grep -c "derks@2024-06-22" cement/utils/fs.py` → 0)

---

*Plan: 03-04 (Wave 4)*
*Depends on: Plan 03 (Wave 3 — UP family fully resolved)*
*Unblocks: Plan 05+ (Any-tightening, pathlib migration, pragma audit)*
*Closes: D-24 conjunct #9, D-08 (FA strip), Phase 1 D-14 (deferred-to-Phase-03 promise), cement/utils/fs.py 2024-06-22 self-flagged TODO*
