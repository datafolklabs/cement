---
phase: 03-internal-refactor-coverage-hardening
reviewed: 2026-05-03T23:45:00Z
depth: standard
files_reviewed: 9
files_reviewed_list:
  - scripts/audit-public-api.py
  - Makefile
  - pyproject.toml
  - cement/utils/fs.py
  - cement/core/foundation.py
  - cement/core/template.py
  - cement/core/config.py
  - cement/core/controller.py
  - cement/core/handler.py
findings:
  critical: 2
  warning: 5
  info: 4
  total: 11
status: issues_found
---

# Phase 3: Code Review Report

**Reviewed:** 2026-05-03T23:45:00Z
**Depth:** standard
**Files Reviewed:** 9
**Status:** issues_found

## Summary

The substantive-logic surface of the Phase 3 refactor was reviewed at standard
depth (mechanical Wave 3/4/7 changes were out of scope per the rationale). The
new audit script is well-commented and the protected `.format(**template_dict)`
callsites in `foundation.py` and `template.py` were preserved intact. However,
two BC-breaking behavior changes introduced by the pathlib migration in
`cement/utils/fs.py:abspath()` are blockers for the 3.0.x stability promise:
silent symlink resolution and `RuntimeError` on unknown `~user` paths. A
handful of additional warnings and info-level concerns are surfaced below for
the audit script and the Wave 5 type-tightening sweep.

The Phase 3 contract work itself (audit script + Makefile target + ruff/mypy
config tightening) is sound. The blockers are localized to `fs.py` and have
straightforward fixes.

## Critical Issues

### CR-01: `fs.abspath()` now resolves symlinks — public-API behavior change

**File:** `cement/utils/fs.py:102`
**Issue:**

The pathlib migration replaced
`os.path.abspath(os.path.expanduser(path))` with
`str(_Path(path).expanduser().resolve(strict=False))`. These are NOT
equivalent: `os.path.abspath` does NOT follow symlinks, but
`Path.resolve()` does. Verified empirically:

```
input:   /tmp/symlink_test/link  (link -> target)
old:     /tmp/symlink_test/link        (os.path.abspath)
new:     /tmp/symlink_test/target      (Path.resolve)
```

This is a public-API surface (`cement.utils.fs:abspath` is in
`03-PUBLIC-API-BASELINE.txt`) and feeds every config-dir, plugin-dir,
template-dir, plugin-file, config-file, and `HOME_DIR` resolution in the
framework (`fs.HOME_DIR` is computed via `abspath('~')` or
`abspath(os.environ['HOME'])` at module load — `cement/utils/fs.py:252-254`).
Downstream apps that rely on the original (non-resolving) string — e.g.,
users with `~/.config` symlinked to a dotfiles repo, or template/plugin
dirs deliberately accessed through a symlink for namespacing — will see
their paths silently rewritten. This violates the project's
"Zero public-API breakage on the 3.0.x track" rule (CLAUDE.md → Constraints).

**Fix:**

Use `os.path.abspath` (which is already imported via `os`) on the
expanded path string instead of `Path.resolve`:

```python
def abspath(path: str, strip_trailing_slash: bool = True) -> str:
    return os.path.abspath(str(_Path(path).expanduser()))
```

Or, equivalently, retain `os.path.abspath(os.path.expanduser(path))`
verbatim as the body — this is a leaf utility where the pathlib
migration provides no readability win and a real BC cost. Verify with a
new test that constructs a symlinked tempdir and asserts the link path
is preserved (not resolved) on the return.

---

### CR-02: `fs.abspath()` raises `RuntimeError` on unknown `~user` paths

**File:** `cement/utils/fs.py:102`
**Issue:**

`os.path.expanduser('~nosuchuser/foo')` returns the input unchanged
(silent fallthrough). `Path('~nosuchuser/foo').expanduser()` raises
`RuntimeError: Could not determine home directory.` Verified on
Python 3.14:

```
old:  '~nosuchuser/foo'                              (os.path.expanduser)
new:  RuntimeError: Could not determine home directory.   (Path.expanduser)
```

`abspath()` is called from every public path-accepting App method
(`add_config_dir`, `add_config_file`, `add_plugin_dir`, `add_template_dir`,
`remove_template_dir` — `foundation.py:1708,1726,1745,1764,1783`) and
from `template.copy()`, `template._load_template_from_file()`,
`ext_smtp` attachments, `ext_logging` log files, and `ext_watchdog`.
A user passing a stale `~deleteduser/path` from a config file used to
get a no-op string back; now they get an unhandled `RuntimeError` mid-
setup. This is a regression on the 3.0.x stability contract (CLAUDE.md
→ Constraints: "Deprecation warnings OK; removals go to 3.2.0").

**Fix:**

Same as CR-01 — restore `os.path.expanduser` semantics. Either revert
the body to `os.path.abspath(os.path.expanduser(path))` or guard the
pathlib version:

```python
def abspath(path: str, strip_trailing_slash: bool = True) -> str:
    expanded = os.path.expanduser(path)
    return os.path.abspath(expanded)
```

Add a regression test that `fs.abspath('~nosuchuser/foo')` does not
raise (returns `os.path.abspath('~nosuchuser/foo')` verbatim).

## Warnings

### WR-01: `Path('a') / 'b'` differs from `os.path.join('a', 'b')` for empty / absolute trailing components

**File:** `cement/core/template.py:234, 247, 254, 265, 273, 285`
**Issue:**

`os.path.join('/foo', '')` returns `/foo/` (preserves trailing slash).
`str(Path('/foo') / '')` returns `/foo` (no trailing slash). Other
divergences exist for absolute-path second args, but those don't apply
in `template.py` because the `cur_dir_stub` / `new_file` / `new_sub_dir`
strings are `lstrip`'ed of leading `/` first.

The empty-string case can theoretically arise if `re.sub(escaped_src_pattern, '', escaped_cur_dir)`
strips everything in `cur_dir_stub`. The code routes the `cur_dir == src`
case down a separate branch (line 215-218), so the empty-stub path is
unlikely in the happy path. But if a user's template tree contains a
directory whose name happens to match `escaped_src_pattern` again (e.g.,
nested directory named the same as the source root after some encoding
roundtrip), the resulting joined path now lacks the trailing separator
that `os.path.join` would have produced. Downstream `_Path(...).exists()`
checks tolerate this; downstream string-comparison checks (e.g., the
dedup `if d not in template_dirs` in `foundation.py`) would treat
`/foo/` and `/foo` as distinct, which previously deduped under the old
`os.path.join` output.

**Fix:**

Audit each `str(_Path(X) / Y)` call site in `template.py` for the
empty-`Y` case. If the contract requires `os.path.join` parity, fall
back to `os.path.join(X, Y)` at the boundary (Phase 03 D-14
boundary-tag accommodation). Add a parametrized test exercising
`copy()` against a tree whose directory names trigger the
empty-stub edge case.

---

### WR-02: `audit-public-api.py` reads source files without explicit encoding

**File:** `scripts/audit-public-api.py:181`
**Issue:**

`tree = ast.parse(py.read_text())` calls `Path.read_text()` with no
`encoding` argument — defaults to `locale.getpreferredencoding(False)`
(platform-dependent). On systems where the locale is not UTF-8 (Windows
default cp1252, some macOS/CI containers, locale-stripped Docker
images), source files containing non-ASCII characters (e.g., the em
dashes already present in cement's docstrings — `cement/core/foundation.py`
contains "—" in the audit-point comments) will fail to decode and the
script will crash mid-walk.

The script is wired into `make audit-public-api` which is the gate for
public-API drift detection (Phase 03 D-03/D-05). A locale-dependent
crash makes that gate unreliable across the supported Python 3.10–3.14
matrix and across CI/dev workstations.

**Fix:**

```python
tree = ast.parse(py.read_text(encoding='utf-8'))
```

Python source files are guaranteed UTF-8 by default per PEP 3120, so
this is safe and explicit.

---

### WR-03: `audit-public-api.py` skips tuple-unpacking module-level assignments

**File:** `scripts/audit-public-api.py:67-73`
**Issue:**

`collect_module_symbols` only handles `ast.Name` targets in
`ast.Assign` and `ast.AnnAssign`. Tuple-unpacking assignments
(`PUBLIC_A, PUBLIC_B = func()`) and starred targets are silently
dropped — the AST target there is `ast.Tuple` / `ast.Starred`, not
`ast.Name`. No such pattern currently exists in `cement/`, so this is
a latent gap rather than a current miss; but the audit script is the
permanent regression check for the 3.0.x → 3.2.x line (Phase 03 D-05),
and any future contributor who lands a tuple-unpacked public name
will silently bypass the baseline diff.

**Fix:**

Add a recursive name-extraction helper:

```python
def _extract_names(target: ast.expr) -> list[str]:
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, (ast.Tuple, ast.List)):
        out = []
        for elt in target.elts:
            out.extend(_extract_names(elt))
        return out
    if isinstance(target, ast.Starred):
        return _extract_names(target.value)
    return []
```

Then iterate target names through it in both `collect_module_symbols`
and `collect_class_members`.

---

### WR-04: `App.__import__` return type `ModuleType` is wrong on the `from_module` branch

**File:** `cement/core/foundation.py:1787,1799`
**Issue:**

The `from_module is not None` branch returns
`getattr(_loaded, obj)` (line 1799), which is whatever attribute `obj`
names on the imported module — typically a class or function, not a
`ModuleType`. The annotation says `-> "ModuleType"`. Wave 5 was the
type-tightening pass and explicitly cited this method
(`foundation.py:1787` comment block) — it tightened `obj: Any → str`
but left the return type narrower than the actual contract.

This propagates an inaccurate type signature to downstream users who
call `_loaded = app.__import__('json', from_module='ujson')` and try to
use the return as a class/function (mypy would falsely flag the
attribute access).

**Fix:**

Widen the return type to match the actual two-mode contract:

```python
def __import__(self, obj: str, from_module: str | None = None) -> Any:
```

Or split into two overloads if mypy strict-mode enforcement makes the
caller experience worse with `Any`.

---

### WR-05: `HandlerManager.resolve` return type retains a redundant `Handler | Handler` union

**File:** `cement/core/handler.py:344`
**Issue:**

The return annotation is `Handler | Handler | None`. The duplicate
`Handler |` union member is acknowledged in the comment at lines
337-340 as a Wave 3 UP007 cascade artifact deferred to "future tech-debt
cleanup." However, this is the file under active type-tightening review
in Wave 5 (per the scope rationale). Since `Handler | Handler` is
strictly equivalent to `Handler` (mypy normalizes it but the source
artifact is misleading), and the fix is a one-character delete, leaving
it documented-but-unfixed creates documentation debt.

**Fix:**

```python
def resolve(self,
            interface: str,
            handler_def: str | Handler | type[Handler],
            **kwargs: Any) -> Handler | None:
```

Drop the audit-point comment line about the duplicate-union since the
artifact is gone.

## Info

### IN-01: `fs.abspath` `strip_trailing_slash` parameter is unused (pre-existing)

**File:** `cement/utils/fs.py:80`
**Issue:**

`def abspath(path: str, strip_trailing_slash: bool = True) -> str` —
the `strip_trailing_slash` parameter is not read by the body and was
not read by the pre-migration body either. It is a public-API parameter
(in `03-PUBLIC-API-BASELINE.txt`) so it cannot be removed on the 3.0.x
track. Note for Phase 5 deprecation cycle.

**Fix:**

Out of scope for Phase 3. File a Phase 5 deprecation candidate to
either (a) honor the flag (strip a trailing `/` from the return when
`True`), or (b) emit a `DeprecationWarning` and remove in 3.2.0.

---

### IN-02: `_setup_config_handler` may reference unbound `ext_list` (pre-existing)

**File:** `cement/core/foundation.py:1473`
**Issue:**

If `exts = self.config.get(label, 'extensions')` returns a value that
is neither `str` nor `list` (e.g., `None`, `int`, dict), the
`for ext in ext_list:` loop at line 1473 reads `ext_list` before it
was bound and raises `UnboundLocalError`. This is pre-existing baseline
behavior, not introduced by this phase.

**Fix:**

Out of scope for Phase 3 logic. Worth a separate small fix to add an
`else: ext_list = []` branch or a stronger type assertion.

---

### IN-03: Audit script — `module_name_for` uses `relative_to(root.parent)` brittle to symlinked checkouts

**File:** `scripts/audit-public-api.py:155-165`
**Issue:**

`rel = path.relative_to(root.parent)` will raise `ValueError` if
`path` (from `cement_root.rglob('*.py')`) is not under
`cement_root.parent`. This holds in the normal case, but if the dev
checkout is reached through a symlink and `path` is not resolved (it
isn't — `rglob` preserves the iteration root) while `root` is
(the script does `Path(__file__).resolve().parent.parent`, line 169),
then `path` and `root.parent` have different real prefixes and the
relative-path computation crashes.

**Fix:**

Either resolve both ends (`py.resolve()` and `cement_root.resolve()`)
or neither. Resolving both is the safer option:

```python
repo_root = Path(__file__).resolve().parent.parent
cement_root = repo_root / 'cement'
for py in sorted(cement_root.rglob('*.py')):
    rel = py.resolve().relative_to(repo_root)
```

---

### IN-04: `audit-public-api` Makefile target uses `/tmp` — non-portable on hardened CI

**File:** `Makefile:38`
**Issue:**

`@pdm run python scripts/audit-public-api.py > /tmp/cement-public-api.txt`
hardcodes `/tmp` as the diff scratch path. This is fine for Linux/macOS
dev but breaks on Windows runners and on hardened CI containers that
mount `/tmp` read-only or don't have one. Cement's CI matrix is Linux-
only today (Phase 1 RESEARCH), so this is currently not load-bearing,
but is a portability gap if the matrix expands.

**Fix:**

Use a Make-local scratch path:

```makefile
audit-public-api:
	@pdm run python scripts/audit-public-api.py > tmp/cement-public-api.txt
	@diff -u .planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt tmp/cement-public-api.txt
```

(`tmp/` is already in the `superclean` target — `Makefile:80` —
indicating it's an established repo-local scratch dir.)

---

_Reviewed: 2026-05-03T23:45:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
