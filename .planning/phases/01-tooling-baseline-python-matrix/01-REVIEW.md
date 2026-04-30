---
phase: 01-tooling-baseline-python-matrix
reviewed: 2026-04-30T00:00:00Z
depth: standard
files_reviewed: 86
files_reviewed_list:
  - .github/workflows/build_and_test.yml
  - Makefile
  - README.md
  - cement/cli/main.py
  - cement/cli/templates/generate/project/Dockerfile
  - cement/cli/templates/generate/todo-tutorial/Dockerfile
  - cement/core/arg.py
  - cement/core/cache.py
  - cement/core/config.py
  - cement/core/controller.py
  - cement/core/exc.py
  - cement/core/extension.py
  - cement/core/foundation.py
  - cement/core/handler.py
  - cement/core/hook.py
  - cement/core/interface.py
  - cement/core/log.py
  - cement/core/mail.py
  - cement/core/output.py
  - cement/core/plugin.py
  - cement/core/template.py
  - cement/ext/ext_alarm.py
  - cement/ext/ext_argparse.py
  - cement/ext/ext_colorlog.py
  - cement/ext/ext_configparser.py
  - cement/ext/ext_daemon.py
  - cement/ext/ext_dummy.py
  - cement/ext/ext_generate.py
  - cement/ext/ext_jinja2.py
  - cement/ext/ext_json.py
  - cement/ext/ext_logging.py
  - cement/ext/ext_memcached.py
  - cement/ext/ext_mustache.py
  - cement/ext/ext_plugin.py
  - cement/ext/ext_print.py
  - cement/ext/ext_redis.py
  - cement/ext/ext_scrub.py
  - cement/ext/ext_smtp.py
  - cement/ext/ext_tabulate.py
  - cement/ext/ext_watchdog.py
  - cement/ext/ext_yaml.py
  - cement/utils/fs.py
  - cement/utils/misc.py
  - cement/utils/shell.py
  - cement/utils/version.py
  - docker-compose.yml
  - pyproject.toml
  - tests/__init__.py
  - tests/cli/test_main.py
  - tests/conftest.py
  - tests/core/test_arg.py
  - tests/core/test_cache.py
  - tests/core/test_config.py
  - tests/core/test_controller.py
  - tests/core/test_deprecations.py
  - tests/core/test_exc.py
  - tests/core/test_extension.py
  - tests/core/test_foundation.py
  - tests/core/test_handler.py
  - tests/core/test_hook.py
  - tests/core/test_interface.py
  - tests/core/test_log.py
  - tests/core/test_mail.py
  - tests/core/test_output.py
  - tests/core/test_plugin.py
  - tests/core/test_template.py
  - tests/ext/test_ext_alarm.py
  - tests/ext/test_ext_argparse.py
  - tests/ext/test_ext_colorlog.py
  - tests/ext/test_ext_configparser.py
  - tests/ext/test_ext_daemon.py
  - tests/ext/test_ext_generate.py
  - tests/ext/test_ext_jinja2.py
  - tests/ext/test_ext_json.py
  - tests/ext/test_ext_logging.py
  - tests/ext/test_ext_memcached.py
  - tests/ext/test_ext_mustache.py
  - tests/ext/test_ext_plugin.py
  - tests/ext/test_ext_redis.py
  - tests/ext/test_ext_smtp.py
  - tests/ext/test_ext_watchdog.py
  - tests/ext/test_ext_yaml.py
  - tests/test_init.py
  - tests/utils/test_fs.py
  - tests/utils/test_misc.py
  - tests/utils/test_shell.py
findings:
  critical: 0
  warning: 2
  info: 7
  total: 9
status: issues_found
---

# Phase 1: Code Review Report

**Reviewed:** 2026-04-30
**Depth:** standard
**Files Reviewed:** 86
**Status:** issues_found (2 warnings, 7 info — no blockers)

## Summary

Phase 1 is a disciplined, narrowly-scoped tooling-baseline modernization. The phase
hits its strict-minimum target (D-13) cleanly: zero gratuitous refactors, zero new
runtime dependencies (`pyproject.toml [project] dependencies = []` preserved),
zero public API signature changes, AUDIT POINT comments codified at four sites
in `pyproject.toml`, all four ruff/mypy/pytest tool bumps land with the
prescribed D-15 coupling, and all 86 reviewed files compile/import cleanly under
the new ruff 0.15.12 + mypy 1.20.2 + pytest 9.0.3 surface.

The bulk of the diff (~70 files) is pure I001 isort import re-ordering — pure
declarative, no behavior change, light scrutiny only. Real semantic edits cluster
in ten files and are well-justified per the SUMMARYs.

The phase invariants are all upheld:

1. **3.0.x public API breakage:** none. `expose`, `CaughtSignal`, `Handler`,
   `App`, `ArgparseController` all keep exact public signatures. The
   `expose.__init__` `arguments` parameter shifts from `=[]` to
   `Optional[List]=None` with default-list initialization inside — a stealth
   correctness fix (avoids shared-mutable-default bug) but documented default
   semantics unchanged. See IN-02.
2. **D-13 strict-minimum:** honored. All `Optional[X]`/`Union`/`List`/`Dict`
   typing forms preserved, `from __future__ import annotations` retained
   wherever present, no f-string conversions, no pathlib migration.
3. **Zero new runtime deps for core:** `pyproject.toml [project] dependencies`
   is `[]` — verified.
4. **100% coverage:** held per SUMMARY metrics (316 passed, Miss=0 across all
   measured modules). Branches added in this phase are noqa annotations and
   `from e` chaining — no new executable branches to test.
5. **noqa/type-ignore rationale:** every per-line suppression added in this
   phase carries an inline justification. Two issues with the *placement* of
   noqa annotations in `cement/cli/main.py` are flagged below (WR-01).

Two findings warrant attention before merge: a misplaced `# noqa` directive in
`cement/cli/main.py` (cosmetic, but genuinely confusing), and a behavior delta
under `python -O` from the B011 `assert False` → `raise AssertionError` rewrite
in `cement/core/template.py` that should be acknowledged in the 3.0.x changelog.

## Warnings

### WR-01: Misplaced `# noqa: T201` directive in `cement/cli/main.py`

**File:** `cement/cli/main.py:52, 56`
**Issue:** The standalone `# noqa: T201 - intentional CLI error output` comments
on lines 52 and 56 sit on dedicated lines *above* the `print()` calls. A
`# noqa` directive is line-scoped — it only suppresses lint on the line it is
written on. Lines 52 and 56 contain no T201 violation (they are pure comments),
so the `# noqa:` token there is a no-op. The actual suppression is the
trailing `# noqa: T201` already present on the `print()` lines themselves
(lines 53 and 57), which is correct.

The floating `# noqa:` lines look like they are doing real work. They are not.
This will:
- Confuse readers who think the standalone `noqa:` is the suppression source
- Fire `RUF100` (unused noqa) if/when that ruff family is ever added to the
  selected set in a future audit-point edit
- Survive code-review only because `RUF100` is not currently in
  `extend-select`

**Fix:**
```python
        except AssertionError as e:  # pragma: nocover
            # intentional CLI error output (suppressed via noqa on the print line)
            print(f'AssertionError > {e.args[0]}')  # pragma: nocover  # noqa: T201
            app.exit_code = 1  # pragma: nocover
        except CaughtSignal as e:  # pragma: nocover
            # intentional CLI signal output (suppressed via noqa on the print line)
            print(f'\n{e}')  # pragma: nocover  # noqa: T201
            app.exit_code = 0  # pragma: nocover
```

Either drop the `noqa:` token from the standalone comment (rewriting it as a
plain explanatory comment) or fold the rationale into the inline noqa as
`# noqa: T201 - intentional CLI error output`. Either form is unambiguous.

### WR-02: B011 `assert False` → `raise AssertionError` changes behavior under `python -O`

**File:** `cement/core/template.py:278-280`
**Issue:** The Phase-1 B011 fix replaces the old `assert False, msg` form with
an unconditional `raise AssertionError(msg)`. Under `python -O` (or
`PYTHONOPTIMIZE=1`), `assert` statements are stripped at bytecode-compile time;
the old code would silently fall through under optimized mode, allowing the
"destination already exists" branch to continue past the guard. The new code
unconditionally raises regardless of `-O`, which:

- Aligns with the documented contract on `TemplateHandler.copy()` lines
  165-169 ("Raises: AssertionError ... when a `dest` file already exists and
  `force is not True`").
- Is the safer behavior: the old optimized-mode path could have silently
  overwritten or skipped destination files.
- Is a *behavior change* for downstream applications running cement under
  `python -O`. Tests with `force=False` against an existing dest will now
  raise where previously they may not have under `-O`.

This is a stealth correctness improvement, not a regression. Per the 3.0.x
no-breakage rule, however, anything that *can* alter downstream observable
behavior is worth surfacing.

**Fix:** No code change needed — the new behavior is correct. Add a one-line
mention to the eventual 3.0.16 changelog (Phase 6 DOCS-03) noting that
`TemplateHandler.copy()` now raises `AssertionError` consistently regardless
of Python optimization mode. Suggested phrasing:

```
- TemplateHandler.copy() now raises AssertionError unconditionally when a
  destination file already exists and force=False. Previously, this
  AssertionError was elided under `python -O` (assert-statement stripping).
  The new behavior matches the documented contract.
```

If a 3.0.x patch-level no-breakage interpretation considers this a
behavior delta (it changes optimized-mode runtime), the alternative is to
revert to `assert False, ...` and add `# noqa: B011` with a behavioral-parity
rationale (parallel to the B005 noqa pattern adopted at lines 217 and 230).
Recommended path: keep the fix, document the change.

## Info

### IN-01: `# noqa: F401` on jinja2 import is correct but lacks explanatory rationale

**File:** `cement/cli/main.py:42-43`
**Issue:** Per Plan 02 SUMMARY Deviation 4, the original
`import yaml, jinja2  # type: ignore  # noqa: F401 E401` was split by the
I001 isort auto-fix into two lines, and the combined noqa was preserved on
yaml but lost on jinja2. The fix re-annotates jinja2 with `# noqa: F401`,
and intentionally drops the `# type: ignore` on jinja2 because mypy 1.20
finds type stubs for jinja2 (so `unused-ignore` warns).

This is correct behavior. The two import lines now have asymmetric trailing
comments, and the *reason* for that asymmetry (yaml lacks type stubs, jinja2
has them) is not explained in the file itself. A single-line comment above the
try/except block would make the asymmetry self-documenting:

**Fix:**
```python
    # NOTE: yaml lacks type stubs in this environment (hence # type: ignore);
    # jinja2 ships PEP 561 stubs so no type ignore needed. Both are imported
    # for side-effect availability checking only — F401 suppressed.
    try:
        import jinja2  # noqa: F401
        import yaml  # type: ignore  # noqa: F401
    except ModuleNotFoundError as e:  # pragma: nocover
        ...
```

Optional polish — not blocking.

### IN-02: `expose.__init__` mutable-default fix is a stealth correctness improvement worth changelog mention

**File:** `cement/ext/ext_argparse.py:158-166`
**Issue:** B006 fix replaced `arguments: List[...] = []` with
`arguments: Optional[List[...]] = None` plus
`self.arguments = arguments if arguments is not None else []`. The OLD code
shared the same `[]` list across every `expose()` decorator instance at
class-definition time (Python's notorious mutable-default-argument bug); the
NEW code gives each instance a fresh list.

Per the Plan 02 SUMMARY, this is documented as "default semantics unchanged
from `arguments: List[...] = []`" — which is true for any caller that simply
*reads* `obj.arguments` after construction. However, downstream code that
relied on the shared-list-across-instances bug (e.g.,
`expose().arguments.append(x)` mutating *all* decorator instances at once) would
break. That usage pattern is not a documented contract and would be a clear
caller bug, but the 3.0.x no-breakage rule is strict enough to warrant a
mention in the eventual 3.0.16 changelog.

**Fix:** No code change. Add a changelog entry (Phase 6 DOCS-03):

```
- expose() decorator's `arguments` parameter no longer shares a mutable list
  across decorator instances (B006 fix). Per-instance behavior unchanged for
  documented usage. Code that relied on the shared-list side-effect (an
  undocumented Python mutable-default-argument bug) will need to switch to
  explicit list passing.
```

### IN-03: `tests/conftest.py` `request` fixture parameter unused after PT022 simplification

**File:** `tests/conftest.py:11, 21, 26`
**Issue:** All three fixtures (`tmp`, `key`, `rando`) declare a `request`
parameter that is never referenced inside the function body. Pytest accepts
this without warning (fixtures get `request` injected on demand), but the
parameter is now visibly noise after the PT022 yield→return simplification.

This is pre-existing noise in `tmp` and `key`/`rando` (they never used
`request`), surfaced by the simplification rather than introduced by it.
Removing it is Phase 3 test-modernization scope, not Phase 1.

**Fix:** Phase 3 REFACTOR-04 / test-modernization candidate. Drop the unused
`request` parameters:

```python
@pytest.fixture
def tmp():
    t = fs.Tmp()
    yield t
    if os.path.exists(t.dir) and t.cleanup is True:
        shutil.rmtree(t.dir)


@pytest.fixture
def key():
    return _rando()


@pytest.fixture
def rando():
    return _rando()[:12]
```

No action this phase.

### IN-04: `cement/core/handler.py:394` `# type: ignore` is appropriate but acknowledges known typing debt

**File:** `cement/core/handler.py:394`
**Issue:** The single-line `# type: ignore` append at line 394 mirrors the
sibling pattern at lines 387/389/390/393/395 — five existing per-line
suppressions all guarding the same `MetaMixin/Meta` union-attr pattern. The
file also disables `attr-defined` globally via
`pyproject.toml [tool.mypy] disable_error_code`. This is technical debt the
project has explicitly accepted (D-11 + Phase 3 REFACTOR-02 will revisit).

The Phase 1 fix is the right granularity for D-13 strict-minimum: a narrowing
assertion (`assert han is not None`) would have introduced a new code shape
diverging from the established pattern. Mirroring the sibling suppression is
correct.

**Fix:** No action this phase. Phase 3 REFACTOR-02 should revisit the
MetaMixin/Meta typing surface holistically and ideally retire the disable
block + per-line ignores together.

### IN-05: `cement/core/template.py:217, 230` B005 redundant lstrip preserved with rationale

**File:** `cement/core/template.py:217, 230`
**Issue:** The `lstrip('\\\\')` call (one of three sequential `lstrip` calls
at each site) is redundant: `lstrip` operates on a character set, not a
substring, so `lstrip('\\\\')` is functionally identical to `lstrip('\\')`
followed on the next line. The B005 noqa with "intentional redundant strip
preserved for behavioral parity (D-13)" is the correct strict-minimum posture
— removing the redundant call is mechanical refactor that D-13 explicitly
defers.

This is justified per Plan 02 SUMMARY decision #6 and crystal-clear from the
inline rationale.

**Fix:** No action this phase. Phase 3 REFACTOR-04 candidate: collapse the
three-line `lstrip('/')` / `lstrip('\\\\')` / `lstrip('\\')` chain into a
single `lstrip('/\\')` call (character set), with test verification that the
visible behavior is identical.

### IN-06: `pyproject.toml:140-147` commented-out legacy `ignore = [...]` block

**File:** `pyproject.toml:140-147`
**Issue:** A commented-out block referencing the legacy `ignore = ["E402",
"E713", "E721", "E714", "F841", "F507"]` list sits below the new
`[tool.ruff.lint.per-file-ignores]` section. This is dead documentation —
the active `ignore` list above already supersedes it. The "TBD" block at lines
149-151 (`[tool.ruff.format]`) and the commented-out
`[[tool.mypy.overrides]]` at lines 153-155 are similarly stale.

This is pre-existing noise in `pyproject.toml`, not introduced by Phase 1, but
visible after the new audit-point structure was added.

**Fix:** Phase 3 housekeeping candidate. Either remove the dead blocks
entirely or fold their decision rationale into the surviving AUDIT POINT
comment (e.g., "we do not use [tool.ruff.format] because ..."). No action
this phase.

### IN-07: `pdm.lock` not regenerated for the bumped pin set

**File:** `pdm.lock` (intentionally NOT modified by this phase)
**Issue:** Per Plan 02/03/04 Pitfall 4, `pdm.lock` was reverted via
`git checkout pdm.lock` after each `pdm install`, deferring lockfile
regeneration to Phase 2 DEPS-01. This is the correct phase boundary, but it
means CI on the Phase 1 PR resolves dependencies fresh against
`pyproject.toml` rather than against a frozen lockfile — which is the
intended behavior for the unpinned `>=` floor pins (pytest, pytest-cov,
coverage, mock, pypng, requests, commitizen) but slightly looser than
desirable for the `~=` compatible-release pins (ruff, mypy).

In practice the `~=0.15.12` and `~=1.20.2` constraints will resolve to the
same patched versions on every CI run modulo new patch releases. The risk is
that a brand-new ruff 0.15.13 (not yet released at phase-close) could ship a
new rule in a selected family between PR-open and PR-merge and fail CI on a
fresh resolve.

**Fix:** No code change. Acknowledged as known carry-forward risk per Plan
04 SUMMARY. Phase 2 DEPS-01 owns the lockfile regen and will pin the exact
ruff/mypy patch versions used at merge time.

---

_Reviewed: 2026-04-30_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
