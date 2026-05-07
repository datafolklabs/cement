---
phase: 05-deprecations-docs-security-stubs
plan: 02
subsystem: docs
tags: [sphinx, sphinx_rtd_theme, autodoc, docutils, napoleon, RST]

# Dependency graph
requires:
  - phase: 05-deprecations-docs-security-stubs / 05-01
    provides: Plan 01 deprecation removal-version language sweep — keeps the active 3.0.15 - DEVELOPMENT CHANGELOG section open for Plan 02 to append into
provides:
  - Zero sphinx warnings: `pdm run sphinx-build ./docs/source ./docs/build` exits clean
  - Single live `html_theme_options` dict at `docs/source/conf.py:19-33` (duplicate at former lines 51-53 deleted)
  - `docs/source/api/index.rst` orphan deleted (option (a) per Pitfall 4)
  - `cement/core/interface.py:102` return annotation string-quoted with grep-able `# autodoc:` rationale
  - `cement/utils/shell.py:cmd()` Returns docstring reflowed so `(stdout, stderror, return_code)` literal stays single-line
  - `display_version` theme option renamed to `version_selector` (sphinx_rtd_theme 3.x rename — bonus deviation fix)
  - 5 new CHANGELOG entries (4 Misc, 1 Bugs)
affects: [Plan 04 (D-09 / D-16 step 9 — flip `make docs` to `-W` strict mode), DOCS-01 acceptance criterion #1]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "RST inline-literals MUST stay on one source line — line-spanning literals trigger docutils 'Inline literal start-string without end-string' even after napoleon Google-style preprocessing"
    - "PEP 585 method-name-shadow workaround: string-quote return annotations on methods whose name shadows the builtin (e.g., `list`, `type`, `dict`) — defers evaluation past the method binding so autodoc's `inspect.signature()` doesn't try to subscript the method object"
    - "Theme-option rename validation is the kind of diagnostic that gets MASKED by duplicate-dict overwrites — only surfaces when the duplicate is removed; document this as a Pitfall for future config audits"

key-files:
  created: []
  modified:
    - docs/source/conf.py — duplicate `html_theme_options` removed; `display_version` renamed to `version_selector`
    - docs/source/api/index.rst — DELETED (orphan)
    - cement/core/interface.py — `InterfaceManager.list` return annotation string-quoted
    - cement/utils/shell.py — `cmd()` Returns docstring reflowed
    - CHANGELOG.md — 5 new entries (4 Misc, 1 Bugs)

key-decisions:
  - "Pitfall 3 mis-identified the load-bearing fix: the prescribed `text=True` / `encoding=...` slash → `or` swap alone did NOT clear the docutils warning. Root cause was a separate inline literal `\\`\\`(stdout, stderror,⏎ return_code)\\`\\`` that spanned a line break — RST inline literals must close on the same source line they open. Fix was to reflow the prose so the parenthesized literal stays single-line. The slash → `or` swap kept (matches Pitfall 3 intent) but was not the actual root cause."
  - "5th sphinx warning emerged after Task 1 cleared the duplicate `html_theme_options` dict: sphinx_rtd_theme 3.0+ renamed `display_version` to `version_selector`. Pre-existing config bug masked by the duplicate-dict overwrite. Fixed inline as Rule 1/3 deviation (commit ae6a6036) to satisfy Task 4's phase-level gate precondition (sphinx-build emits 0 warnings → Plan 04 can flip `-W`)."
  - "Pitfall 4 option (a) — delete orphan `docs/source/api/index.rst` — preferred over option (b) (:hidden: toctree). Pre-flight grep confirmed no external references; smaller diff; preserves single source of truth at top-level `docs/source/index.rst:8-13`."
  - "`exec_cmd()` docstring (lines 73-91) intentionally left unmodified per D-08 #4 strict scope, despite carrying the same `\\`\\`text=True\\`\\` / \\`\\`encoding=...\\`\\`` slash form. Confirmed `exec_cmd()` does NOT trigger the docutils warning — its `\\`\\`(stdout, stderror, return_code)\\`\\`` literal already stays single-line, supporting the Pitfall-3-mis-identified diagnosis."

patterns-established:
  - "RST inline-literal scope: literals MUST close on the same source line they open. Source-prose wrapping that splits `\\`\\`...⏎...\\`\\`` triggers docutils warnings even if the prose looks logically connected. Fix is reflow, not the napoleon-output indentation."
  - "Method-name-shadow guard: methods named after builtins (`list`, `type`, `dict`, `set`, `bytes`, `str`, etc.) that return a generic of the same builtin (e.g., `list[str]`) need the return annotation string-quoted to dodge `inspect.signature()` subscript bugs. Inline `# autodoc:` comment makes future cleanups grep-able."
  - "Theme-option drift surface: when a duplicate dict-overwrite is removed, ANY pre-existing config-key drift in the active dict surfaces immediately. Always run sphinx-build BEFORE removing duplicates to capture the post-cleanup baseline."

requirements-completed: [DOCS-01]

# Metrics
duration: 15min
completed: 2026-05-07
---

# Phase 05 Plan 02: Sphinx Warnings Resolution Summary

**Cleared all sphinx warnings (4 plan-known + 1 deviation-discovered) so DOCS-01 acceptance criterion #1 is met and Plan 04 can flip `make docs` to `-W` strict mode.**

## Performance

- **Duration:** 15 min
- **Started:** 2026-05-07T23:03:40Z
- **Completed:** 2026-05-07T23:18:46Z
- **Tasks:** 4 (planned) + 1 deviation = 5 atomic commits
- **Files modified:** 4 source/config files + CHANGELOG.md

## Accomplishments

- All 4 originally-known sphinx warnings cleared (D-08 #1, #2, #3, #4)
- 1 bonus warning resolved (`display_version` → `version_selector`, deviation Rule 1/3)
- `pdm run sphinx-build ./docs/source ./docs/build` exits with 0 warnings — DOCS-01 acceptance criterion #1 GREEN
- `make audit-public-api` exit 0 across all 5 commits (D-18 #3 — public-API surface byte-identical)
- `make comply` (ruff + mypy) exit 0 on every commit
- `make test` exit 0 at 100% coverage post-plan (3243 stmts / 0 missed across 320 tests)
- 5 new CHANGELOG entries appended (4 Misc, 1 Bugs)
- Plan 04 prerequisite met: sphinx-build is warning-free under non-`-W` mode; `-W` flip is now a no-op safety upgrade

## Task Commits

Each task was committed atomically:

1. **Task 1: Drop duplicate `html_theme_options` dict** — `3712fe91` (docs)
   - `docs/source/conf.py:51-53` deleted (3 lines); active dict at lines 19-33 preserved with all toc-config keys (`navigation_depth: 4`, `collapse_navigation`, `titles_only`, etc.)
   - Pitfall 2 guard held: did NOT remove only the `'logo'` key (which would have left an empty dict still overwriting the active config)

2. **Task 2: Wire api/index into top-level toctree** — `cbf42b27` (docs)
   - `docs/source/api/index.rst` DELETED (Pitfall 4 option (a))
   - Pre-flight grep confirmed no external references in `.planning/`, `docs/`, `README.md`
   - Top-level `docs/source/index.rst:8-13` unchanged — already the single source of truth referencing `api/core/index`, `api/utils/index`, `api/ext/index`

3. **Task 3: String-quote `InterfaceManager.list` return annotation** — `4e7f9a5c` (fix)
   - `cement/core/interface.py:102` changed from `-> list[str]:` to `-> "list[str]":  # autodoc: PEP 585 + method-name-shadow workaround`
   - `make audit-public-api` exit 0 immediately before AND after — annotation form is annotation-blind to the AST walker (Pitfall 1 verified)
   - Inline `# autodoc:` comment grep-able for future cleanup; sibling files (hook.py, handler.py, extension.py) preserved on the existing `import builtins + builtins.list[T]` pattern as a future consistency-cleanup candidate

4. **(Deviation) Rename `display_version` → `version_selector`** — `ae6a6036` (docs)
   - `docs/source/conf.py:23` config-key rename — sphinx_rtd_theme 3.0+ renamed the option
   - Bonus warning that emerged ONLY after Task 1 deleted the duplicate dict (the duplicate had been silently overwriting the active config; once removed, the active dict's pre-existing key-name drift surfaced)
   - Required to satisfy Task 4's phase-level gate precondition (sphinx-build emits 0 warnings → Plan 04 can flip `-W`)

5. **Task 4: Fix inline-literal RST in `cmd()` docstring** — `ca1ea3b1` (docs)
   - `cement/utils/shell.py:34-41` Returns block reflowed so `(stdout, stderror, return_code)` inline literal stays single-line
   - Replaces `text=True` / `encoding=...` slash with `or` (matches Pitfall 3 intent for consistency, even though the slash was NOT the load-bearing root cause)
   - `exec_cmd()` (lines 73-91) intentionally untouched per D-08 #4 strict scope; it does not trigger the warning because its `(stdout, stderror, return_code)` literal already stays single-line

**Plan metadata:** This SUMMARY.md commit (separate, follows below)

## Files Created/Modified

- `docs/source/conf.py` — duplicate `html_theme_options` deleted (Task 1); `display_version` renamed to `version_selector` (deviation)
- `docs/source/api/index.rst` — **DELETED** (Task 2, orphan)
- `cement/core/interface.py` — `InterfaceManager.list` return annotation string-quoted with `# autodoc:` rationale (Task 3)
- `cement/utils/shell.py` — `cmd()` Returns docstring reflowed (Task 4)
- `CHANGELOG.md` — 5 new entries (4 Misc, 1 Bugs)

## Decisions Made

- **Pitfall 3 mis-identification corrected:** The plan's prescribed root-cause fix (slash → `or`) was insufficient. Investigation found the actual root cause was a different inline-literal pattern (`(stdout, stderror,⏎ return_code)` spanning a line break). Documented in commit ca1ea3b1 body so the next maintainer doesn't repeat the misdiagnosis.
- **Bonus warning fixed inline:** The `display_version` → `version_selector` rename surfaced only after Task 1 removed the duplicate dict. Per deviation Rule 1/3 (auto-fix bugs / blocking issues), fixed in a separate atomic commit (`ae6a6036`) so Task 4's phase-level zero-warnings precondition was satisfiable.
- **`exec_cmd()` left alone:** Same prose pattern as `cmd()`, but D-08 #4 names only `cmd()` and `exec_cmd()` does not trigger any sphinx warning. Confirmed by inspection: `exec_cmd()`'s `(stdout, stderror, return_code)` literal is already single-line.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Pitfall 3 mis-identified the load-bearing fix**

- **Found during:** Task 4 (Fix inline-literal RST in `cmd()` docstring)
- **Issue:** Plan called for a single-token swap (`text=True`/`encoding=...` slash → `or`), citing Pitfall 3. Sphinx-build re-run after the swap still emitted the same `Inline literal start-string without end-string` warning at the same line. Bisecting the docstring with a docutils harness identified a separate root cause: the inline literal `` ``(stdout, stderror, return_code)`` `` opened on one source line and closed on the next, which RST does not permit. The `text=True`/`encoding=...` slash was harmless on its own; only the line-spanning `(stdout, ...)` literal triggered the warning.
- **Fix:** Reflowed the entire `Returns:` block so the `(stdout, stderror, return_code)` inline literal stays on one line. Kept the slash → `or` swap for consistency with the plan's intent.
- **Files modified:** `cement/utils/shell.py`
- **Verification:** `pdm run sphinx-build ./docs/source ./docs/build 2>&1 | grep -ic 'Inline literal start-string'` → 0
- **Committed in:** `ca1ea3b1` (Task 4 commit)

**2. [Rule 3 - Blocking] 5th unscoped sphinx warning surfaced after Task 1 (display_version → version_selector)**

- **Found during:** Task 4 verification (full sphinx-build re-run for the phase-level zero-warnings precondition)
- **Issue:** After Task 1 deleted the duplicate `html_theme_options` dict at `conf.py:51-53`, sphinx-build started emitting `WARNING: unsupported theme option 'display_version' given`. This was a 5th warning NOT in the plan's enumerated 4 — sphinx_rtd_theme 3.0+ renamed `display_version` to `version_selector`, and the rename had silently been masked by the duplicate-dict overwrite (the duplicate had `'logo': 'logo-text.png'` only, so the active dict's `display_version` was effectively dead config; once the duplicate was deleted, the active dict became live and the rename-drift surfaced).
- **Fix:** Renamed the key in the active dict. Atomic separate commit (NOT folded into Task 1) so the bisect history is clean — Task 1 is "delete duplicate", deviation commit is "rename obsolete key", Task 4 is "fix inline literal".
- **Files modified:** `docs/source/conf.py`, `CHANGELOG.md`
- **Verification:** `pdm run sphinx-build ./docs/source ./docs/build 2>&1 | grep -ic 'unsupported theme option'` → 0; phase-level gate `... | grep -cE '(WARNING|ERROR):'` → 0
- **Committed in:** `ae6a6036` (deviation commit, between Task 3 and Task 4)

### Acceptance criterion mismatch (documented, not auto-fixed)

Task 4 acceptance criterion `grep -F '\`\`text=True\`\` /' cement/utils/shell.py → 0 hits` is global to `cement/utils/shell.py`. The same slash-form prose still appears in `exec_cmd()` (line 90), which the plan explicitly forbids modifying ("D-08 #4 names only `cmd()`"). Per the plan's strict scope, the slash form survives in `exec_cmd()` and the global grep matches that line. Interpreted the criterion as scoped to `cmd()` only (the function the warning fires on); deferred the parallel `exec_cmd()` fix to a future quick task per the plan's own Pitfall 9 / Example 5 guidance.

---

**Total deviations:** 2 auto-fixed (1 bug, 1 blocking) + 1 documented acceptance-criterion mismatch
**Impact on plan:** Both auto-fixes essential — without them the phase-level zero-warnings precondition (Plan 04's `-W` flip prerequisite) would not have been met. No scope creep beyond the docs/security-stubs phase boundary.

## Issues Encountered

- **Pitfall 3 misdiagnosis (Issue resolved by deviation #1 above):** RESEARCH.md's Pitfall 3 attributed the warning to the slash separator. Bisecting via a docutils-only test harness (no napoleon, no sphinx) identified the line-spanning inline literal as the actual root cause. Future docs-fix research tasks should run a docutils-only minimal repro for any "Inline literal start-string without end-string" warning before settling on the prescribed fix.
- **Stash/conflict on Task 4 CHANGELOG sequencing:** Splitting the deviation commit (ae6a6036) from Task 4 commit (ca1ea3b1) required a `git stash` of in-progress shell.py + CHANGELOG edits, then a manual conflict resolution on `git stash pop` (both stashed and committed versions appended new entries to the same Misc bucket line). Resolution: keep both entries, ordered as (Task 1, Task 2, deviation, Task 4) by ID. No content lost.

## User Setup Required

None - this is a docs-only plan. No external service configuration, no environment variables, no secrets.

## Next Phase Readiness

- DOCS-01 acceptance criterion #1 GREEN: `make docs` builds without warnings or broken cross-references.
- Plan 04 (D-09 / D-16 step 9 — flip `make docs` to use `-W`) prerequisite MET. After this plan, the `-W` flag is a no-op safety upgrade rather than a behavior-changing flip.
- 100% coverage gate held continuously: 3243 stmts / 0 missed across 320 tests.
- `make audit-public-api` exit 0 across all 5 commits — public-API surface byte-identical.
- No blockers carried into Plan 03+.

## TDD Gate Compliance

N/A — Plan 02 is type=execute (not type=tdd). All tasks were `type="auto" tdd="false"` (docs/config edits, no test-first cycle).

## Self-Check: PASSED

**Files verified:**
- FOUND: `docs/source/conf.py` (modified)
- FOUND: `cement/core/interface.py` (modified — `def list(self) -> "list[str]":` present)
- FOUND: `cement/utils/shell.py` (modified — Returns block reflowed)
- FOUND: `CHANGELOG.md` (modified — 5 new entries)
- DELETED (intended): `docs/source/api/index.rst`

**Commits verified:**
- FOUND: `3712fe91` docs(sphinx): drop unsupported 'logo' theme option from conf.py
- FOUND: `cbf42b27` docs(sphinx): wire api/index into top-level toctree
- FOUND: `4e7f9a5c` fix(core.interface): string-quote list[str] for autodoc
- FOUND: `ae6a6036` docs(sphinx): rename display_version to version_selector (deviation)
- FOUND: `ca1ea3b1` docs(utils.shell): fix inline-literal RST in cmd() docstring

**Final gate evidence:**
- `pdm run sphinx-build -E ./docs/source ./docs/build 2>&1 | grep -ic warning` → `0`
- `pdm run sphinx-build ./docs/source ./docs/build 2>&1 | grep -cE '(WARNING|ERROR):'` → `0`
- `make comply` → exit 0 (ruff + mypy clean)
- `make audit-public-api` → exit 0 (public-API surface byte-identical)
- `make test` → exit 0, 320 passed, 100.00% coverage (3243 stmts, 0 missed)

---
*Phase: 05-deprecations-docs-security-stubs*
*Plan: 02 (sphinx warnings resolution)*
*Completed: 2026-05-07*
