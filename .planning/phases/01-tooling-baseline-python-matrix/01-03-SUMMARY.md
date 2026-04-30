---
phase: 01-tooling-baseline-python-matrix
plan: 03
subsystem: tooling
tags: [mypy, type-codification, pyproject, audit-point, tooling-baseline]

# Dependency graph
requires:
  - "01-01 (Python 3.10 floor in place — mypy python_version='3.10' set)"
  - "01-02 (ruff baseline green — clean lint surface for the mypy bump)"
provides:
  - "mypy ~=1.20.2 pin (D-12 compatible-release on a fast-evolving tool)"
  - "AUDIT POINT comment in [tool.mypy] (D-08+D-11 hybrid drift detection)"
  - "All mypy strictness knobs preserved exactly per D-11 (no value changes)"
  - "tests/ exclusion preserved exactly per D-10"
  - "cement/core/handler.py:394 union-attr fallout resolved via existing `# type: ignore` pattern"
  - "make comply-mypy exits 0 on mypy 1.20.2"
  - "make comply (ruff + mypy) exits 0"
  - "make test exits 0; 316 passed, 100.00% coverage held on cement/"
  - "Closure of TOOL-02 (mypy bump green) and TOOL-04 (mypy half of no-implicit-drift codification)"
affects:
  - "01-04 (pytest+pytest-cov+coverage bumps) — mypy baseline now green; pytest can bump on a clean ruff+mypy surface"
  - "Phase 2 PDM auto-update pipeline — new mypy strict defaults in future minor bumps now fire as CI failures, forcing deliberate audit-point edits"

# Tech tracking
tech-stack:
  added:
    - "mypy 1.20.2 (was 1.9.0 floor; ~= compatible-release pin)"
  patterns:
    - "AUDIT POINT codification (D-08+D-11): comment block in [tool.mypy] above the strictness knobs naming itself as the re-review point on every mypy bump"
    - "Hybrid drift posture extended to mypy (D-08): explicit-knob enumeration + ~= pin + audit comment. Same posture as ruff in 01-02. New strict defaults in mypy bumps fire CI failures, not silent absorption."
    - "D-15 coupling held: mypy pin (~=1.20.2) and AUDIT POINT comment land in the SAME `chore: bump mypy to 1.20` commit"
    - "D-04 one-commit-per-fallout: union-attr fix lands in its own `fix(types):` commit, separate from the bump"
    - "D-13 strict-minimum: handler.py fix is a single-line append of `  # type: ignore`. NO narrowing assertion, NO refactor. Mirrors framework's established sibling pattern."

key-files:
  created: []
  modified:
    - "pyproject.toml — mypy ~=1.20.2 pin in [dependency-groups] dev; AUDIT POINT comment block added in [tool.mypy] above strictness knobs"
    - "cement/core/handler.py:394 — appended `  # type: ignore` to mirror sibling pattern at lines 387/389/390/393/395"

key-decisions:
  - "D-15 coupling enforced: mypy pin (`mypy~=1.20.2`) and AUDIT POINT comment land in ONE chore: bump mypy to 1.20 commit. Pin and audit point are inseparable for D-08 hybrid drift detection."
  - "D-11 boundary held: ZERO strictness knob value changes. The ONLY content addition in [tool.mypy] is the AUDIT POINT comment block. disallow_untyped_calls/defs/decorators, disallow_incomplete_defs, no_implicit_optional, strict_optional, check_untyped_defs, warn_return_any, warn_unused_ignores, show_error_codes, disable_error_code=['attr-defined'] all preserved verbatim."
  - "D-10 boundary held: `[tool.mypy] files = ['cement/']` and the exclude block (cement/cli/templates, .git/, tests) preserved verbatim. tests/ remains excluded — Phase 3+ owns mypy expansion to tests."
  - "D-13 strict-minimum: handler.py fix is single-line append of `  # type: ignore` — NOT a narrowing assertion (`assert han is not None`) and NOT a refactor. Mirrors the framework's established pattern at sibling lines 387/389/390/393/395 (all of which already use `# type: ignore` for the same MetaMixin/Meta union-attr pattern)."
  - "Line number drift acknowledged: RESEARCH.md (verified 2026-04-29) cited the union-attr site as line 392. Plan 02's I001 isort auto-fix and B007 res→_res rename shifted the line to 394. Same code, same fix; line drift is the only delta. Documented in commit body."
  - "pdm.lock reverted post-`pdm install` per Plan 02 precedent + RESEARCH.md Pitfall 4. Phase 2 DEPS-01 owns lockfile regeneration; Plans 02-04 collectively defer it. The pyproject.toml pin update is what matters for tool-version drift detection — pdm.lock regen is a separate orthogonal concern."

patterns-established:
  - "D-15 coupling pattern repeated: pin + audit comment in single chore: bump commit, fallout fix in separate fix(types): commit. Same shape as Plan 02's `chore: bump ruff to 0.15` + `fix(lint): resolve <family>` chain — generalizable across tool bumps."
  - "Conventional Commits with 78-char wrap (CLAUDE.md): both commit subjects ≤78 chars, all commit body lines ≤78 chars (verified via `git log -1 --format=%b | awk 'length>78 {exit 1}'` returning empty)"
  - "Atomic per-tool-fallout commits (D-04): mypy union-attr fix is its own commit, separable from the pin bump for bisect granularity"

requirements-completed: [TOOL-02, TOOL-04]

# Metrics
duration: 3 min
completed: 2026-04-30
---

# Phase 01 Plan 03: mypy Bump + Type Fallout Resolution Summary

**Bumps mypy from `>=1.9.0` to `~=1.20.2`, codifies the type-check surface (AUDIT POINT comment per D-08+D-11), and resolves the single union-attr fallout at `cement/core/handler.py:394` via the framework's established `# type: ignore` sibling pattern. Plan 02's ruff baseline + Plan 03's mypy baseline together close the no-implicit-drift codification (TOOL-04). `make comply` and `make test` are GREEN at the close of the plan with 100% coverage held.**

## Performance

- **Duration:** ~3 min
- **Started:** 2026-04-30T06:00:44Z
- **Completed:** 2026-04-30T06:03:32Z
- **Tasks:** 2 (1 chore: bump + 1 fix(types) per D-04)
- **Files modified:** 2 (pyproject.toml, cement/core/handler.py)
- **Commits:** 2 atomic conventional commits

## Accomplishments

- **2 atomic commits land in plan-prescribed order** per D-04:
  1. `3966a8fd chore: bump mypy to 1.20` — mypy pin (`mypy~=1.20.2`) + AUDIT POINT comment in ONE commit per D-15
  2. `8d392dd2 fix(types): resolve union-attr in core/handler.py` — single-line append of `  # type: ignore` at line 394 mirroring sibling pattern
- **mypy 1.20.2 active** — verified via `pdm run mypy --version` returning `mypy 1.20.2 (compiled: yes)`
- **Total mypy errors resolved:** 1 — exactly as RESEARCH.md predicted. The single union-attr at `cement/core/handler.py:394` (line drifted from research's 392 due to Plan 02 lint fixes; same line of code, same fix). No additional mypy 1.20 errors surfaced — Pitfall 5 cleared.
- **D-08+D-11 codification verified:** `pyproject.toml [tool.mypy]` has the AUDIT POINT comment block above the first strictness knob; `[dependency-groups] dev` has `mypy~=1.20.2`
- **D-11 boundary held:** ZERO strictness knob value changed. Verified via diff inspection — the only [tool.mypy] additions are the 4-line comment block.
- **D-10 boundary held:** `files = ["cement/"]` and `exclude` block preserved verbatim. tests/ stays excluded.
- **D-13 strict-minimum honored:** handler.py fix is single-line `  # type: ignore` append. No narrowing assertion. No refactor. No code shape change.
- **D-15 coupling held:** mypy pin (`mypy~=1.20.2`) lands in the SAME commit as the AUDIT POINT comment (the `chore: bump mypy to 1.20` commit)
- **3.0.x no-breakage rule held:** the `# type: ignore` annotation is a no-op at runtime; no public API surface change. Verified via `git diff cement/core/handler.py` showing single-line trailing-comment append.
- **TOOL-02** (mypy bump + green) closed; **TOOL-04** (no-implicit-drift codification) fully closed (mypy half this plan, ruff half in Plan 02)

## Task Commits

| Task | Subject | Hash | Files |
|------|---------|------|-------|
| 1 | chore: bump mypy to 1.20 | `3966a8fd` | pyproject.toml |
| 2 | fix(types): resolve union-attr in core/handler.py | `8d392dd2` | cement/core/handler.py |

## Final State of `[tool.mypy]`

```toml
[tool.mypy]
python_version = "3.10"
# AUDIT POINT (D-08+D-11): strictness knobs are deliberately enumerated,
# NOT `strict = true`. Adding a knob is a deliberate decision; mypy
# bumps that introduce new strict defaults will fail CI and force the
# same audit conversation as ruff. See Phase 1 RESEARCH.md.
disallow_untyped_calls = true
disallow_untyped_defs = true
disallow_any_unimported = false
disallow_incomplete_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
strict_optional = true
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
show_error_codes = true

disable_error_code = [
    # disable as MetaMixin/Meta is used everywhere and triggers this
    "attr-defined",
]

files = [
    "cement/",
    # "tests/"
]
exclude = """(?x)(
    ^cement/cli/templates |
    ^.git/ |
    ^tests
  )"""
```

The ONLY change vs. pre-Plan-03 state is the addition of the 4-line AUDIT POINT comment block between `python_version` and `disallow_untyped_calls`. Every knob value is preserved verbatim.

## Final State of `[dependency-groups] dev` (mypy line)

```toml
"mypy~=1.20.2",                # was >=1.9.0  (D-12: ~= compatible-release)
```

## Final State of `cement/core/handler.py:394` Fix

```python
        elif hasattr(handler_def, 'Meta'):
            han = handler_def(**meta_defaults)  # type: ignore
            if not self.registered(interface, han._meta.label):  # type: ignore  ← FIXED
                self.register(handler_def)  # type: ignore
```

The fix mirrors the surrounding sibling pattern. Lines 387/389/390/393/395 all already use `# type: ignore` for the same MetaMixin/Meta union-attr pattern. Plan 03's fix adds the missing one at line 394, completing the pattern. NOT a narrowing assertion (would have required deeper code change beyond D-13). NOT a refactor.

## Resolution Path Summary

| Concern | Resolution | Why |
|---------|-----------|-----|
| mypy version pin | `mypy~=1.20.2` (D-12 compatible-release) | mypy evolves fast on minors with new strict defaults; ~= prevents implicit drift |
| AUDIT POINT comment | Added above strictness knobs in [tool.mypy] | D-08+D-11 hybrid drift detection — same pattern as ruff in Plan 02 |
| Strictness knob values | All preserved verbatim | D-11 explicit: NO knob value changes this phase |
| tests/ exclusion | Preserved verbatim | D-10 explicit: mypy expansion to tests/ is future work |
| union-attr at handler.py:394 | `# type: ignore` append | D-13 strict-minimum + framework's established sibling pattern |
| pdm.lock | Reverted post-`pdm install` | Pitfall 4 — Phase 2 DEPS-01 owns lockfile regen |

## Decisions Made

1. **D-15 coupling enforced** — pin + audit comment landed in single `chore:` commit. The pin and audit point are inseparable for the hybrid drift-detection pattern; splitting them would dilute the commit's purpose and break the bisect anchor.
2. **D-11 strict preservation** — zero strictness knob value changes. Even though mypy 1.20.2 exposes new strictness knobs, this phase explicitly defers tightening to Phase 3 REFACTOR-02 ("tighten type hints"). The phase boundary is structural codification only.
3. **D-13 strict-minimum on handler.py:394** — chose `# type: ignore` append over narrowing assertion (`assert han is not None`). The narrowing approach would have introduced a new code shape (assertion-based narrowing) that diverges from the framework's existing pattern at sibling lines 387/389/390/393/395. Mirroring the established pattern is the strict-minimum choice and matches `disable_error_code = ["attr-defined"]`'s acknowledgement that MetaMixin/Meta is a framework-wide accepted trade-off.
4. **Line number drift documented in commit** — RESEARCH.md cited line 392; live state is line 394. Plan 02's I001 isort auto-fix and B007 res→_res rename shifted handler.py imports + locals. Same fix, same code, line drift only. Commit body explicitly notes this so future bisect can follow the trail.
5. **pdm.lock revert** — `pdm install` regenerated pdm.lock to record mypy 1.20.2 + typing-extensions 4.15.0 + cement 3.0.15 resolution. Reverted via `git checkout pdm.lock` per Plan 02 precedent + Pitfall 4. The pyproject.toml pin is what matters for tool-version drift detection in this phase; pdm.lock regen is Phase 2 DEPS-01 work.

## Deviations from Plan

The plan was executed exactly as written, with one minor adjustment documented for audit-trail discipline:

### Deviation 1: union-attr line number 392 → 394 [no rule applies — informational]

**Found during:** Task 2 read of cement/core/handler.py

**Issue:** Plan 03 + RESEARCH.md cited the union-attr site as `cement/core/handler.py:392`, verified 2026-04-29. Live state on 2026-04-30 (post-Plan-02) is line 394. The shift is the cumulative effect of Plan 02's I001 auto-fix (re-ordering imports added/removed lines at the top of the module) and B904 raise...from e fixes elsewhere in handler.py.

**Fix:** No fix needed — the plan anticipated this exact possibility ("Plans 02 lint-fix work may have shifted line numbers slightly... verify the actual line numbers BEFORE applying the edit"). I read lines 380-405 before editing, confirmed line 394 is the union-attr site (matches `if not self.registered(interface, han._meta.label):`), and applied the fix to line 394. Same code, same fix, just a different line index.

**Files modified:** none beyond plan scope

**Commit:** `8d392dd2` (commit body notes the line shift)

**Total deviations:** 1 (informational only — line drift documented and resolved per plan's own anticipation).

## Issues Encountered

None blocking. The pdm.lock change from `pdm install` was reverted per Pitfall 4; same posture as Plan 02. No mypy errors beyond the predicted union-attr surfaced — Pitfall 5 cleared.

## User Setup Required

None — no external service configuration required. CI matrix verification on Python 3.10/3.11/3.12/3.13/3.14 happens in GitHub Actions on push (formal gate is `gh pr checks <PR>` once the phase-1 branch is pushed and a PR opened).

## Next Phase Readiness

**Ready for plan 01-04 (pytest+pytest-cov+coverage bumps).** The mypy baseline is now green and codified:

- Plan 04 can bump pytest/pytest-cov/coverage on a clean ruff+mypy surface (no cross-tool fallout interference)
- The PDM auto-update pipeline now has the mypy half of the codification it needs to detect drift: strictness knobs are the deliberate-additions list, AUDIT POINT comment is the re-review trigger, `~=1.20.2` is the major-stable constraint
- TOOL-04 ("no implicit drift") is now FULLY codified across both ruff (Plan 02) and mypy (Plan 03)

**Risks carried forward:**

- pdm.lock not regenerated in Plan 03 (intentional per Pitfall 4). Plan 04 (pytest bump) may need to run `pdm install` and similarly revert pdm.lock; Plans 02-04 collectively defer lockfile regen to Phase 2 DEPS-01.
- The CI matrix on push will verify mypy 1.20.2 across Python 3.10/3.11/3.12/3.13/3.14. Local exec only ran on the dev container's default Python (likely 3.13). mypy version-specific inference behavior should be uniform across CPython 3.10+ but is worth validating in CI.

## Self-Check: PASSED

**File checks:**
- FOUND: pyproject.toml (modified — `mypy~=1.20.2` pin in [dependency-groups] dev; AUDIT POINT comment block in [tool.mypy] above strictness knobs)
- FOUND: cement/core/handler.py (modified — line 394 `  # type: ignore` append)
- FOUND: .planning/phases/01-tooling-baseline-python-matrix/01-03-SUMMARY.md (this file)

**Commit checks:**
- FOUND: `3966a8fd` — chore: bump mypy to 1.20
- FOUND: `8d392dd2` — fix(types): resolve union-attr in core/handler.py

**Quality gate checks:**
- `make comply-ruff` exits 0 — "All checks passed!"
- `make comply-mypy` exits 0 — "Success: no issues found in 51 source files"
- `make comply` exits 0
- `make test` exits 0 — 316 passed, 100.00% coverage on cement/, 1692 warnings (deprecation noise from upstream libs, not cement code)
- `pdm run mypy --version` returns `mypy 1.20.2 (compiled: yes)`
- All 2 commit subjects ≤78 chars; all body lines ≤78 chars (verified per commit)
- D-15 coupling: `git log -p pyproject.toml` shows pin + audit comment in single `3966a8fd` commit
- D-13 single-line: `git diff` of handler.py shows exactly one line changed (trailing `  # type: ignore` append)

---
*Phase: 01-tooling-baseline-python-matrix*
*Completed: 2026-04-30*
