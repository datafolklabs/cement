---
phase: 01-tooling-baseline-python-matrix
plan: 02
subsystem: tooling
tags: [ruff, lint-codification, pyproject, audit-point, tooling-baseline]

# Dependency graph
requires:
  - "01-01 (Python 3.10 floor in place)"
provides:
  - "ruff ~=0.15.12 pin (D-12 compatible-release on a fast-evolving tool)"
  - "preview = false (D-09 — ends silent absorption of preview-graduated rules)"
  - "extend-select codified to 11 families per D-06: E,F,W,B,I,A,C90,N,PT,T20,YTT"
  - "AUDIT POINT comment in [tool.ruff.lint] (D-08 hybrid drift detection)"
  - "[tool.ruff.lint] ignore = [A001, A002, C901] with one-line audit justifications"
  - "[tool.ruff.lint.per-file-ignores] tests/**/*.py = [N806, N805, PT012, PT013] with audit justifications"
  - "make comply-ruff exits 0 across cement/ and tests/ on ruff 0.15.12"
  - "make test exits 0; coverage held at 100.00% on cement/"
  - "Closure of TOOL-01 (ruff pin), TOOL-04 (no implicit drift codification)"
affects:
  - "01-03 (mypy bump) — ruff baseline is green; mypy can bump on a clean lint surface"
  - "01-04 (pytest+pytest-cov+coverage bumps) — same"
  - "Phase 2 PDM auto-update pipeline — new rule activations within selected families now fire as CI failures (the user's pain point), forcing deliberate audit-point edits"

# Tech tracking
tech-stack:
  added:
    - "ruff 0.15.12 (was 0.3.2; ~= compatible-release pin)"
  patterns:
    - "AUDIT POINT codification (D-08): comment block in [tool.ruff.lint] above preview/extend-select naming itself as the re-review point on every ruff bump"
    - "Hybrid drift posture (D-08): family-level extend-select + audited ignore + ~= pin + preview=false. Inverts implicit absorption into deliberate engagement."
    - "D-04 one-commit-per-rule-family fix granularity proven across 8 families (29 B + 80 I + 18 A + 12 C901 + 10 N + 27 PT + 8 T201 + 1 YTT203 = 185 violations) in 8 atomic fix(lint): commits"
    - "D-15 coupling held: ruff pin (~=0.15.12), preview flip (true→false), and 8-family extend-select expansion ALL land in the single chore: bump ruff to 0.15 commit"
    - "Per-call # noqa with one-line rationale (the CaughtSignal/expose/createLock pattern) for public API surface where rename would break 3.0.x"
    - "Per-file-ignore for tests/ (RESEARCH.md Pitfall 6 pattern) — N806/N805/PT012/PT013 absorbed without polluting the project-level ignore"
    - "Broad-ignore for framework-intentional builtins shadowing (A001/A002) — same posture attrs uses for the same reason"

key-files:
  created: []
  modified:
    - "pyproject.toml — ruff ~=0.15.12 pin; preview=false; extend-select 11-family codified; ignore=[A001,A002,C901] with audit justifications; [tool.ruff.lint.per-file-ignores] tests/**/*.py = [N806,N805,PT012,PT013]"
    - "cement/cli/main.py — B904 raise...from e; T201 noqa on intentional CLI prints; F401 noqa restored on jinja2 (split-import side-effect of I001 auto-fix)"
    - "cement/core/extension.py — B904 raise...from e"
    - "cement/core/foundation.py — B007 unused-loop-variable rename (res→_res, 9 sites)"
    - "cement/core/handler.py — B904 raise...from e"
    - "cement/core/interface.py — B904 raise...from e"
    - "cement/core/template.py — B005 noqa with rationale (intentional redundant lstrip preserves behavior); B011 assert False → raise AssertionError(...)"
    - "cement/core/exc.py — N818 noqa on CaughtSignal exception name (public API)"
    - "cement/ext/ext_argparse.py — B904 raise...from e; B006 mutable default arguments=[] → Optional[List[...]]=None pattern; N801 noqa on `class expose` (public decorator)"
    - "cement/ext/ext_daemon.py — B904 raise...from e (2 sites)"
    - "cement/ext/ext_dummy.py — T201 noqa on DummyMailHandler.send() print (intentional)"
    - "cement/ext/ext_generate.py — B904 raise...from e"
    - "cement/ext/ext_logging.py — N802 noqa on createLock override (logging stdlib camelCase)"
    - "cement/ext/ext_watchdog.py — B007 unused-loop-variable rename (res→_res, 6 sites)"
    - "76 other cement/ + tests/ files — I001 isort auto-fix (pure import re-ordering, no behavior change)"
    - "tests/conftest.py — PT003 implied scope='function' removed; PT022 yield→return on non-teardown fixtures"
    - "tests/core/test_foundation.py, test_plugin.py, test_template.py — T201 debug-leftover prints removed"
    - "tests/ext/test_ext_argparse.py — YTT203 stale sys.version_info[0]>=3 and sys.version_info[1]>=4 shim removed; ARGPARSE_SUPPORTS_DEFAULTS = True unconditional; unused import sys removed"

key-decisions:
  - "A001/A002 absorbed via broad-ignore in [tool.ruff.lint] ignore (Option C from plan), NOT per-call noqa (Option B). Rationale: 18 sites scattered across 5 files (ext_colorlog, ext_logging, ext_generate, utils/fs, tests/ext_smtp), most in subclass-exposed Handler kwargs matching Python stdlib conventions (logging.Formatter `format` argument). Per-call noqa was rejected as polluting many call sites for what is structurally a framework-wide intentional shadow pattern."
  - "C901 absorbed in [tool.ruff.lint] ignore with Phase 3 REFACTOR-01/02 cross-reference (RESEARCH.md Open Question 3 explicit recommendation). Refactoring 12 hot-spot functions in cement/core/foundation.py, handler.py, etc. is volunteer modernization beyond D-13 strict-minimum."
  - "N806 + N805 absorbed via [tool.ruff.lint.per-file-ignores] on tests/**/*.py (RESEARCH.md Pitfall 6 pattern). Test-fixture casing (META, DEBUG_FORMAT, Log, MyLog) is intentional; subclass-pattern test methods omit `self` deliberately."
  - "N818/N801/N802 in production cement/ kept as per-call # noqa with one-line rationale (Option B). Rationale: each is a SINGLE site protecting public API surface (CaughtSignal exception, expose decorator class, createLock logging stdlib override) — per-call noqa is the right granularity, broad-ignore would be over-suppression."
  - "PT013 absorbed via per-file-ignore on tests/**/*.py (DEVIATION from RESEARCH.md predicted resolution). Newer ruff 0.15 reversed PT013's preference: it now wants `import pytest` instead of `from pytest import raises`, the OPPOSITE of what RESEARCH.md (verified 2026-04-29 on ruff 0.15.12) predicted. The existing cement convention is `from pytest import raises` (cited at tests/core/test_exc.py); mass-rewriting the convention is itself a D-13 strict-minimum violation. Absorbed with audit comment."
  - "PT012 (multi-statement raises blocks) absorbed via per-file-ignore. 7 sites with multi-line setup-then-trigger sequences inside `with pytest.raises():` blocks. Refactoring is Phase 3 test-modernization work."
  - "B007 unused-loop-variable fixed via ruff --unsafe-fixes auto-rename (res→_res, 17 sites across foundation.py/ext_watchdog.py/2 tests). Diff inspected; rename is mechanical and confined to loop variable scope."
  - "B005 misleading multi-char lstrip in template.py annotated # noqa with behavioral parity rationale rather than refactored. The two `lstrip('\\\\\\\\')` calls have the same effect as the next line `lstrip('\\\\')` (lstrip works on character sets), making the existing code redundant-but-correct. Removing the redundant call is mechanical refactor that D-13 forbids; noqa preserves behavior parity exactly."
  - "B006 mutable default `arguments=[]` in `class expose.__init__` rewritten as `arguments: Optional[List[...]] = None` with `if arguments is not None` initialization. Public API preserved — default still semantically equivalent to []."
  - "F401 jinja2 import re-annotated with # noqa: F401. Side-effect of I001 auto-fix splitting `import yaml, jinja2  # noqa: F401 E401` into two separate lines without preserving the combined noqa. Caught and fixed in YTT203 commit (Task 9) via Rule 1 (auto-fix bug caused by current task changes)."
  - "Plan's <verify> assertion `pdm run ruff check cement/ tests/ --select A 2>&1 | grep -qE 'All checks passed|^$'` is INCOMPATIBLE with broad-ignore approach — ruff's --select explicitly overrides the project ignore list for the selected rules. Substituted equivalent assertion: `pdm run ruff check cement/ tests/ 2>&1 | grep -cE '^A001|^A002'` returns 0. Same intent, correct semantics."

patterns-established:
  - "Verification gate pattern (per RESEARCH.md sampling rate): every fix(lint): commit verifies the family is clean in normal lint output (`pdm run ruff check cement/ tests/`) PLUS the full pytest suite passes with 100% coverage. `make test-core` is NOT used mid-plan because Makefile `test` target depends on `comply` which fails until ALL families are clean — substituted with direct `pdm run pytest --cov=cement tests/` for incremental verification."
  - "Conventional Commits with 78-char wrap (CLAUDE.md): all 9 commit subjects ≤78 chars, all commit body lines ≤78 chars (verified via `git log -1 --format=%b | awk 'length>78'` returning empty)"
  - "Atomic per-rule-family commits (D-04): one commit per rule family makes bisect possible — every rule fix is independently revertable, every fix is annotated with the rule code in the commit subject"

requirements-completed: [TOOL-01, TOOL-04]

# Metrics
duration: 20 min
completed: 2026-04-30
---

# Phase 01 Plan 02: Ruff Bump + Rule-Set Codification Summary

**Bumps ruff from `>=0.3.2` to `~=0.15.12`, codifies the lint surface (preview=false, 11-family extend-select, AUDIT POINT comment per D-08), and resolves 185 violations across 8 new rule families in 8 atomic fix(lint): commits — one per family per D-04. `make comply` and `make test` are GREEN at the close of the plan with 100% coverage held.**

## Performance

- **Duration:** ~20 min
- **Started:** 2026-04-30T05:34:55Z
- **Completed:** 2026-04-30T05:54:31Z
- **Tasks:** 9 (1 chore: bump + 8 fix(lint): family fixes per D-04)
- **Files modified:** 91 (the bulk being I001 isort auto-fix re-ordering — pure declarative)
- **Commits:** 9 atomic conventional commits

## Accomplishments

- **9 atomic commits land in plan-prescribed order** per D-04:
  1. `7938c98e chore: bump ruff to 0.15` — ruff pin + preview flip + 8-family extend-select expansion + AUDIT POINT comment in ONE commit per D-15
  2. `0e56adee fix(lint): resolve I001 unsorted-imports (auto-fix)` — 80 hits resolved by `ruff check --fix --select I cement/ tests/` (safe-fix `[*]`)
  3. `dd6807a5 fix(lint): resolve B007/B904/B005/B006/B011 bugbear` — 29 hits across cement/cli, cement/core, cement/ext, tests
  4. `401a34cd fix(lint): resolve A001/A002 builtin-shadowing` — 18 hits absorbed via broad-ignore with audit justifications (framework intentionally shadows builtins per Python stdlib conventions)
  5. `c17d440f fix(lint): resolve C901 complex-structure` — 12 hits absorbed in ignore per RESEARCH.md Open Question 3 + D-13 strict-minimum, deferred to Phase 3 REFACTOR-01/02
  6. `738ad307 fix(lint): resolve N806/N801/N802/N805/N818 naming` — 10 hits split: N806/N805 via per-file-ignore on tests/, N818/N801/N802 via per-call # noqa on public-API sites
  7. `c71fb00c fix(lint): resolve PT003/PT022/PT012/PT013 pytest-style` — 26 hits: PT003+PT022 auto-fixed; PT012+PT013 absorbed via per-file-ignore (PT013 ruff 0.15 reversed its preference vs RESEARCH.md prediction)
  8. `57464a97 fix(lint): resolve T201 print-statements` — 8 hits triaged: 3 production prints kept with # noqa (intentional CLI/dummy-handler output); 5 test debug-leftovers removed
  9. `a663d84e fix(lint): resolve YTT203 sys-version-info` — 1 hit: stale sys.version_info[0]>=3 and sys.version_info[1]>=4 shim replaced with unconditional `ARGPARSE_SUPPORTS_DEFAULTS = True`; folded in F401/E501 cleanup caused by I001 auto-fix split-import side-effect (Rule 1 auto-fix bug from current task chain)
- **D-08 codification verified:** `pyproject.toml [tool.ruff.lint]` has the AUDIT POINT comment block above `preview = false`, the 11-family `extend-select` list, and the `ignore` list with one-line justifications per entry
- **D-09 preview flip verified:** `preview = false` (was `true`) — preview-graduated rules now require deliberate `extend-select` engagement
- **D-12 + D-15 coupling held:** ruff pin `~=0.15.12` lands in the SAME commit as the preview flip and extend-select expansion (the `chore: bump ruff to 0.15` commit)
- **D-13 strict-minimum honored:** zero `Optional[X]` → `X | None`, zero `Dict` → `dict`, zero `from __future__ import annotations` removals, zero f-string conversions, zero pathlib migrations
- **3.0.x no-breakage rule held:** zero public API signature changes — verified via `git diff` review of every public-class/def site touched
- **TOOL-01** (ruff bump + green) and **TOOL-04** (no implicit drift codification) closed

## Task Commits

| Task | Subject | Hash | Files |
|------|---------|------|-------|
| 1 | chore: bump ruff to 0.15 | `7938c98e` | pyproject.toml |
| 2 | fix(lint): resolve I001 unsorted-imports (auto-fix) | `0e56adee` | 78 files (cement/ + tests/ imports re-ordered) |
| 3 | fix(lint): resolve B007/B904/B005/B006/B011 bugbear | `dd6807a5` | 12 files |
| 4 | fix(lint): resolve A001/A002 builtin-shadowing | `401a34cd` | pyproject.toml |
| 5 | fix(lint): resolve C901 complex-structure | `c17d440f` | pyproject.toml |
| 6 | fix(lint): resolve N806/N801/N802/N805/N818 naming | `738ad307` | 4 files |
| 7 | fix(lint): resolve PT003/PT022/PT012/PT013 pytest-style | `c71fb00c` | 2 files |
| 8 | fix(lint): resolve T201 print-statements | `57464a97` | 5 files |
| 9 | fix(lint): resolve YTT203 sys-version-info | `a663d84e` | 2 files |

## Final State of `[tool.ruff.lint] ignore`

```toml
ignore = [
    # AUDIT POINT (D-08): each entry MUST have a one-line justification.
    # Empty list is the green-baseline goal.
    "A001",  # framework intentionally shadows builtins (`format`,
             # `vars`, `dir`, etc.) in handler/Meta locals matching
             # Python stdlib conventions (e.g., logging.Formatter
             # `format` argument). D-13 strict-minimum + 3.0.x
             # no-breakage rule. Justified 2026-04-30 Phase 1.
    "A002",  # ditto for argument-shadowing in subclass-exposed
             # Handler method signatures (e.g., LoggingLogHandler
             # `_get_console_formatter(self, format)` is a subclass
             # contract — see ColorLogHandler). Justified 2026-04-30.
    "C901",  # cement framework is intentionally complex
             # (handler/interface dispatch, lifecycle hooks,
             # extension loading). Phase 3 REFACTOR-01/02 will
             # re-evaluate. Justified 2026-04-30 Phase 1.
]
```

## Final State of `[tool.ruff.lint.per-file-ignores]`

```toml
[tool.ruff.lint.per-file-ignores]
# AUDIT POINT (D-08): per-file-ignores require one-line justification.
"tests/**/*.py" = [
    "N806",  # test-fixture variable casing (META, DEBUG_FORMAT, Log,
             # MyLog) is intentional. Justified 2026-04-30 Phase 1.
    "N805",  # subclass-pattern test methods omit `self` deliberately
             # to verify framework behavior. Justified 2026-04-30.
    "PT012", # `pytest.raises()` blocks intentionally wrap multi-step
             # setup-then-trigger-then-assert sequences; refactoring is
             # Phase 3 test-modernization work (D-13 strict-minimum).
             # Justified 2026-04-30 Phase 1.
    "PT013", # `from pytest import raises` is the existing cement
             # test convention (cited at tests/core/test_exc.py).
             # Mass-rewriting to `import pytest` exceeds D-13
             # strict-minimum. Justified 2026-04-30 Phase 1.
]
```

## Resolution Path Summary

| Family | Hits | Approach | Why |
|--------|------|----------|-----|
| I (I001) | 80 | Auto-fix `--select I --fix` | Safe-fix `[*]`; pure import re-ordering |
| B (B007/B904/B005/B006/B011) | 29 | Manual fixes + B007 unsafe-fix auto-rename | Mostly mechanical; B005 noqa for behavioral parity; B006 Optional/None pattern preserves API |
| A (A001/A002) | 18 | Broad-ignore in `[tool.ruff.lint] ignore` (Option C) | Framework intentionally shadows builtins per stdlib conventions; same posture attrs uses |
| C90 (C901) | 12 | Broad-ignore in `[tool.ruff.lint] ignore` with Phase 3 REFACTOR cross-reference | RESEARCH.md Open Question 3 explicit recommendation; D-13 forbids volunteer refactor |
| N (N806/N805/N818/N801/N802) | 10 | Hybrid: per-file-ignore for tests/ (N806/N805), per-call # noqa for public-API in cement/ (N818/N801/N802) | Test casing intentional; production sites are public API |
| PT (PT003/PT022/PT012/PT013) | 26 | Hybrid: PT003+PT022 auto-fixed; PT012+PT013 per-file-ignore on tests/ | PT013's preference reversed in newer ruff vs existing cement convention; PT012 multi-step blocks intentional |
| T20 (T201) | 8 | Triage: 3 noqa for intentional output, 5 removed (debug-leftovers) | Site-by-site review |
| YTT (YTT203) | 1 | Direct fix: replace shim with unconditional True | Python 3.4+ universal under py310 floor |

## Decisions Made

1. **A001/A002 broad-ignore (Option C)** — see key-decisions above. The 18 violations cluster in framework-intentional builtin-shadowing patterns; per-call noqa was rejected as polluting many sites for a structurally pervasive pattern.
2. **C901 absorbed in ignore** with Phase 3 REFACTOR-01/02 cross-reference per RESEARCH.md Open Question 3.
3. **N806/N805 per-file-ignore on tests/**, N818/N801/N802 per-call # noqa in cement/ — granularity matches the violation type.
4. **PT013 absorbed via per-file-ignore** (DEVIATION from RESEARCH.md prediction). Newer ruff 0.15 reversed the preference; existing cement convention is `from pytest import raises`. Mass-rewrite would itself violate D-13.
5. **B007 unsafe-fix used** for the 17 res→_res renames. The "unsafe" classification is conservative (ruff worries about loop variables referenced after the loop); diff inspection confirmed all 17 sites are local-only renames with no external references.
6. **B005 noqa with behavioral parity rationale** in template.py — the redundant lstrip is misleading-but-correct; D-13 forbids removing it as a refactor.
7. **B006 fix preserves public API** — `arguments: Optional[List[...]] = None` + initialize inside, default semantics unchanged from `arguments: List[...] = []`.
8. **F401 + E501 cleanup folded into YTT203 commit** — both were caused by my edits during Tasks 2 and 8 (Rule 1 auto-fix bug from current task chain). Folded into Task 9 commit rather than a separate commit because they were caused-by-this-plan, and bundling them with the YTT203 fix reads cleanly as "close out the last fallout from the bump."

## Deviations from Plan

The plan was executed in spirit, with several specific deviations documented per D-04 audit-trail discipline:

### Deviation 1: PT013 resolution path reversed [Rule 4 declined → Rule 3 fix]

**Found during:** Task 7

**Issue:** RESEARCH.md (verified 2026-04-29 on ruff 0.15.12) said the PT013 fix was to convert `import pytest` → `from pytest import raises` per the existing cement convention. Newer ruff 0.15 (live behavior at time of execution, also 0.15.12) actually does the OPPOSITE: it wants `from pytest import raises` → `import pytest`. RESEARCH.md was contradicted by the live ruff at the version it claimed to verify against.

**Fix:** Absorbed PT013 via per-file-ignore on tests/**/*.py with audit comment. The existing cement convention (`from pytest import raises`, cited at tests/core/test_exc.py) is preserved. Mass-rewriting the existing convention to match the newer ruff preference would itself be a D-13 strict-minimum violation. This is NOT an architectural change (no Rule 4 needed) — it's a fix-by-ignore resolution for a rule preference change that contradicts existing cement convention.

**Files modified:** pyproject.toml (added `PT013` to per-file-ignores)

**Commit:** `c71fb00c`

### Deviation 2: PT012 multi-statement raises blocks → per-file-ignore [Rule 3 - blocking]

**Found during:** Task 7

**Issue:** Plan's task description focused on PT013 as the dominant PT family violation. Live ruff also surfaced 7 PT012 violations (multi-statement `with pytest.raises():` blocks) which require non-trivial test refactor to fix. Refactoring 7 test sites to extract single error-raising statements is volunteer test modernization beyond D-13 strict-minimum.

**Fix:** Absorbed PT012 via per-file-ignore on tests/**/*.py with audit comment cross-referencing Phase 3 test-modernization work.

**Files modified:** pyproject.toml (added `PT012` to per-file-ignores)

**Commit:** `c71fb00c` (same commit as PT013, both PT family per D-04)

### Deviation 3: A-family resolution path → broad-ignore Option C [planned escape hatch invoked]

**Found during:** Task 4

**Issue:** Plan offered three options (A: rename, B: per-call noqa, C: broad-ignore). Plan recommended Option B for clustered cases, Option C only for "broad pattern." Live triage of all 18 A001/A002 sites revealed they cluster in 5 files all touching public-API surface (logging Formatter conventions, Tmp.__init__ dir kwarg, ext_generate vars local). Option C (broad-ignore) was the cleanest fit.

**Fix:** Added A001 + A002 to `[tool.ruff.lint] ignore` with one-line audit justifications referencing the framework-intentional shadow pattern and the matching attrs library precedent.

**Note:** The plan's `<verify>` assertion (`pdm run ruff check ... --select A`) is INCOMPATIBLE with the broad-ignore semantics — ruff's `--select` explicitly overrides the `ignore` list for the selected rules. Substituted with equivalent normal-lint check (`pdm run ruff check cement/ tests/ 2>&1 | grep -cE '^A001|^A002'` returns 0).

**Files modified:** pyproject.toml

**Commit:** `401a34cd`

### Deviation 4: F401 jinja2 + E501 noqa-comment over-length [Rule 1 - bugs from prior tasks]

**Found during:** Task 9 (final lint check)

**Issue 1 (F401):** I001 auto-fix in Task 2 split the original single-line `import yaml, jinja2  # type: ignore  # noqa: F401 E401` into two separate lines. The combined `noqa: F401` was preserved on the `yaml` line but NOT on the `jinja2` line, causing a new F401 violation on jinja2 once the I001 family was activated by ruff 0.15.

**Issue 2 (E501):** My `# noqa: T201 - intentional CLI error output` comments on the print sites in cement/cli/main.py (Task 8) pushed the lines over 100 characters, triggering E501.

**Fix:** Both fixed in the YTT203 commit (Task 9):
- jinja2 import re-annotated with `# noqa: F401`
- print-site noqa comments reformatted to multi-line shape so each line stays under 100 chars
- Spurious `# type: ignore` on jinja2 removed (mypy 1.9.0 reported `unused-ignore`; jinja2 has type stubs available)

**Rationale for folding into Task 9:** Both bugs were direct side-effects of my edits during Tasks 2 and 8. Per Rule 1 (auto-fix bugs caused by current task changes), they fall in scope of the current plan. Bundling with the YTT203 fix reads cleanly as "close out all remaining ruff 0.15 fallout in this plan's final commit" rather than introducing a 10th `chore: cleanup` commit that wouldn't fit the D-04 one-commit-per-family pattern.

**Files modified:** cement/cli/main.py

**Commit:** `a663d84e` (folded into YTT203 task commit)

### Deviation 5: `make test-core` not used as mid-plan sanity check [Rule 3 - blocking issue, verify substituted]

**Found during:** Task 2

**Issue:** Plan's Task 2 `<verify>` assertion includes `make test-core`. The Makefile's `test-core` target depends on `comply`, which runs full ruff lint — and ruff lint fails until ALL 8 family fixes land. So `make test-core` is structurally unrunnable mid-plan.

**Fix:** Substituted `pdm run pytest --cov=cement.core tests/core` (the actual command behind `make test-core` minus the comply gate) for incremental verification. After the final task (Task 9), `make test` (which also runs comply) is the formal end-of-plan gate and exits 0.

**No file or commit impact** — process adjustment only.

**Total deviations:** 5. **Impact on plan goals:** none. Every deviation preserves the plan's intent (clean lint surface, codified rule set, atomic per-family commits, D-13 strict-minimum) while accommodating live behavior that differed from RESEARCH.md predictions or by surfacing bugs caused by my own task chain.

## Issues Encountered

None blocking. All deviations resolved per Rule 1/3/Option-invoke without requiring user decision.

The pdm.lock was modified by `pdm install` to record ruff 0.15.12 resolution; reverted via `git checkout pdm.lock` per RESEARCH.md Pitfall 4 (Phase 2 DEPS-01 owns lockfile regeneration).

## User Setup Required

None — no external service configuration required. CI matrix verification on Python 3.10/3.11/3.12/3.13/3.14 happens in GitHub Actions on push (formal gate is `gh pr checks <PR>` once the phase-1 branch is pushed and a PR opened).

## Next Phase Readiness

**Ready for plan 01-03 (mypy bump).** The ruff baseline is now green and codified:

- Plan 03 can bump mypy from `>=1.9.0` to `~=1.20.2` on a clean ruff surface (no cross-tool fallout interference)
- Plan 04 can bump pytest+pytest-cov+coverage on a known-good lint baseline
- The PDM auto-update pipeline (Phase 2 DEPS-01 concern) now has the codification it needs to detect drift: `extend-select` is the deliberate-additions list, `ignore` is the deliberate-suppressions list with audit justifications, `~=0.15.12` is the major-stable constraint
- The audit point comment in `[tool.ruff.lint]` makes the next ruff bump (e.g., 0.16.x) require deliberate engagement: any new rules in B/I/A/C90/N/PT/T20/YTT will fire as CI failures, forcing a deliberate fix-or-ignore decision

**Risks carried forward:**

- pdm.lock not regenerated in Plan 02 (intentional per RESEARCH.md Pitfall 4). Plan 03 (mypy bump) may need to run `pdm install` and similarly revert pdm.lock; Plans 02-04 collectively defer lockfile regen to Phase 2 DEPS-01.
- `pdm run mypy` is currently green on mypy 1.9.0 + the post-I001 import re-ordering. Plan 03's mypy 1.20 bump may surface NEW type-check fallout that wasn't visible on 1.9.0 — RESEARCH.md predicted only `cement/core/handler.py:392 union-attr` as fallout. Verify in Plan 03.
- The CI matrix on push will verify ruff 0.15.12 + the new rule set across Python 3.10/3.11/3.12/3.13/3.14 + pypy3.10. Local exec only ran on the dev container's default Python (likely 3.13). pypy3.10 in particular is a risk because some bugbear rules (B904 chaining) interact with how tracebacks render — but no test asserts on `__cause__`/`__context__` in the cement test suite, so risk is low.

## Self-Check: PASSED

**File checks:**
- FOUND: pyproject.toml (modified — `ruff~=0.15.12` pin, preview=false, 11-family extend-select, ignore=[A001,A002,C901], per-file-ignores tests/=[N806,N805,PT012,PT013], all with AUDIT POINT comments)
- FOUND: cement/cli/main.py (modified — B904 from e, T201 noqa multi-line, F401 noqa restored on jinja2)
- FOUND: cement/core/extension.py (modified — B904 from e)
- FOUND: cement/core/foundation.py (modified — B007 res→_res rename, 9 sites)
- FOUND: cement/core/handler.py (modified — B904 from e)
- FOUND: cement/core/interface.py (modified — B904 from e)
- FOUND: cement/core/template.py (modified — B005 noqa, B011 raise AssertionError)
- FOUND: cement/core/exc.py (modified — N818 noqa on CaughtSignal)
- FOUND: cement/ext/ext_argparse.py (modified — B904 from e, B006 Optional/None, N801 noqa on expose)
- FOUND: cement/ext/ext_daemon.py (modified — B904 from e, 2 sites)
- FOUND: cement/ext/ext_dummy.py (modified — T201 noqa on DummyMailHandler.send)
- FOUND: cement/ext/ext_generate.py (modified — B904 from e)
- FOUND: cement/ext/ext_logging.py (modified — N802 noqa on createLock)
- FOUND: cement/ext/ext_watchdog.py (modified — B007 res→_res rename, 6 sites)
- FOUND: tests/conftest.py (modified — PT003 scope removed, PT022 yield→return)
- FOUND: tests/core/test_foundation.py, test_plugin.py, test_template.py (modified — debug prints removed)
- FOUND: tests/ext/test_ext_argparse.py (modified — YTT203 stale shim removed, ARGPARSE_SUPPORTS_DEFAULTS = True unconditional, import sys removed)

**Commit checks:**
- FOUND: `7938c98e` — chore: bump ruff to 0.15
- FOUND: `0e56adee` — fix(lint): resolve I001 unsorted-imports (auto-fix)
- FOUND: `dd6807a5` — fix(lint): resolve B007/B904/B005/B006/B011 bugbear
- FOUND: `401a34cd` — fix(lint): resolve A001/A002 builtin-shadowing
- FOUND: `c17d440f` — fix(lint): resolve C901 complex-structure
- FOUND: `738ad307` — fix(lint): resolve N806/N801/N802/N805/N818 naming
- FOUND: `c71fb00c` — fix(lint): resolve PT003/PT022/PT012/PT013 pytest-style
- FOUND: `57464a97` — fix(lint): resolve T201 print-statements
- FOUND: `a663d84e` — fix(lint): resolve YTT203 sys-version-info

**Quality gate checks:**
- `make comply-ruff` exits 0 — "All checks passed!"
- `make comply-mypy` exits 0 — "Success: no issues found in 51 source files"
- `make test` exits 0 — 316 passed, 100.00% coverage on cement/, 1692 warnings (deprecation noise from upstream libs, not cement code)
- `pdm run ruff --version` returns `ruff 0.15.12`
- All 9 commit subjects ≤78 chars; all body lines ≤78 chars (verified via `git log -1 --format=%b | awk 'length>78 {exit 1}'` per commit)

---
*Phase: 01-tooling-baseline-python-matrix*
*Completed: 2026-04-30*
