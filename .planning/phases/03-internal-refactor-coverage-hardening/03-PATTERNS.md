# Phase 03: Internal Refactor & Coverage Hardening - Pattern Map

**Mapped:** 2026-05-03
**Files analyzed:** 9 distinct file roles (3 NEW, 6 MODIFIED categories)
**Analogs found:** 8 / 9 (1 brand-new convention being seeded — see § "No
Analog Found")

This document keeps the planner's `<read_first>` lists pointed at real
analog files in the repo so executor tasks copy from concrete excerpts
instead of abstract guidance. Each pattern excerpt is reproduced in-line
so the planner can paste from here without re-reading.

## File Classification

| New / Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---------------------|------|-----------|----------------|---------------|
| `scripts/audit-public-api.py` (NEW) | dev script (Python, AST walker) | batch (one-shot stdout) | `scripts/devtools.py` (Python script header form) + `scripts/cli-smoke-test.sh` (permanent dev affordance precedent per CONTEXT D-05) | partial — `scripts/devtools.py` is shape-analog (Python script with `#!/usr/bin/env python` header + module docstring); `scripts/cli-smoke-test.sh` is policy-analog (the "permanent dev affordance" precedent from quick task `260430-i7q`) |
| `Makefile` `audit-public-api` target | Makefile target addition | request-response (`make` invocation) | `Makefile:34-35` (`cli-smoke-test`) | exact — single-line standalone target, NOT chained into `comply` or `test`, mirrors D-03 "INDEPENDENT" rule |
| `pyproject.toml` `[tool.ruff.lint] extend-select` UP+FA addition | ruff config addition | config-as-code | `pyproject.toml:101-118` (existing Phase 1 D-08 extend-select block with sibling AUDIT POINT comment) | exact — same block, append `UP` + `FA` siblings with their own one-line justification + AUDIT POINT comment per D-06 |
| `cement/utils/fs.py` (pathlib internals) | source-tree refactor (boundary-preserving) | file-I/O | `cement/utils/fs.py:75-79` (`Tmp.__exit__` already PEP 604) — same file, modern-syntax exemplar | exact — Phase 03 makes the rest of the file consistent with the already-modern `__exit__` signature; no other `cement/utils/*.py` uses `pathlib` (verified `grep -l 'pathlib' cement/utils/*.py` returns nothing) |
| `cement/core/foundation.py` (pathlib internals + Any tightening + UP family) | source-tree refactor | request-response (handler dispatch) + file-I/O | `cement/utils/fs.py:75-79` (PEP 604 syntax exemplar); `cement/core/foundation.py:1317` (target-state os.path callsite) | role-match — no existing `cement/core/*.py` uses `pathlib.Path` internally; `Tmp.__exit__` is the in-tree PEP 604 anchor |
| `cement/core/template.py` (pathlib internals — biggest blast, ~25 sites) | source-tree refactor | file-I/O (template walk) | `cement/utils/fs.py:75-79` PEP 604 exemplar; current `cement/core/template.py:186-260` os.path-heavy walk | role-match — same boundary-preserve rule as fs.py but on a `os.walk` template-rendering loop |
| `cement/core/config.py` (pathlib internals) | source-tree refactor | file-I/O (config parse) | `cement/core/config.py:225-226` (single `os.path.exists` callsite); `cement/utils/fs.py` exemplar | role-match — minimal blast (1 callsite); follows fs.py boundary pattern |
| pragma:nocover category-label sweep across `cement/` | test/coverage policy comment | inline source comment | `cement/cli/main.py:53` (`# pragma: nocover  # noqa: T201`) — existing site with sibling-comment shape; NO existing site uses a category-vocabulary label | partial — the sibling-comment SHAPE exists (cli/main.py:53 + ext_logging.py:35 use `# pragma: ...  # <reason>`); the category-vocabulary CONTENT is brand-new convention seeded by Phase 03 D-15 |
| `03-PUBLIC-API-BASELINE.txt` (NEW) | planning-artifact baseline file | batch | `.planning/phases/02-dependencies-ci-pipeline/02-PIP-AUDIT.md` (closest planning-artifact precedent — frozen snapshot referenced by future verification) | partial — no existing `.planning/phases/*/*-BASELINE.txt` artifact exists; PIP-AUDIT.md is the closest "frozen snapshot for later diff" precedent. The artifact FORMAT is brand-new (sorted plain text, one symbol per line) |
| `03-VERIFICATION.md` (NEW) | planning-artifact verification report | batch | `.planning/phases/01-tooling-baseline-python-matrix/01-VERIFICATION.md`; `.planning/phases/02-dependencies-ci-pipeline/02-VERIFICATION.md` | exact — Phase 03 inherits the YAML-frontmatter + Goal-Achievement / Required-Artifacts / Behavioral-Spot-Checks / Requirements-Coverage / Gaps-Summary section structure |

## Pattern Assignments

### `scripts/audit-public-api.py` (NEW — dev script, batch)

**Analogs:**
- `scripts/devtools.py` (in-tree Python script header form)
- `scripts/cli-smoke-test.sh` (permanent dev affordance precedent per
  D-05; not itself a Python file but anchors the policy that
  `scripts/*` is a permanent dev surface, not phase throwaway)

**Header pattern (analog: `scripts/devtools.py:1`):**

```python
#!/usr/bin/env python

import os
import sys
import re
import tempfile

from cement import App, Controller, ex
```

**Phase 03 target shape** (mandatory module-docstring header per D-02 +
"script header MUST include commentary" per CONTEXT § Specifics):

```python
#!/usr/bin/env python3
"""
audit-public-api.py — emit sorted public-API surface for cement/.

Walks the AST of every module under cement/, prints one
'<dotted.module>:<NAME>' or '<dotted.module>:<ClassName>.<member>' line
per non-underscore module-level symbol or class member.

Sort + diff against 03-PUBLIC-API-BASELINE.txt to detect any public-API
drift. See Phase 03 D-01..D-05.
"""
from __future__ import annotations  # script-internal; doesn't affect cement/

import ast
import sys
from pathlib import Path
```

**Note on `from __future__ import annotations` in this script:** The
FA100 sweep (D-08) only fires inside `cement/` per ruff config
`include = ["cement/**/*.py", "tests/**/*.py"]` (`pyproject.toml:96-99`).
`scripts/` is OUT of ruff's include scope, so the script can keep the
future import without violating Phase 03 D-08. Documented in
RESEARCH.md § Anti-Patterns ("Confusing-but-fine: cement/ becomes
future-import-free, scripts/ is unconstrained").

**Note on dash-named filename:** `audit-public-api.py` (dash, NOT
`audit_public_api.py` snake_case) per user direction in CONTEXT § Specifics.
Diverges from CONVENTIONS.md "Module files: lowercase with underscores"
because this is a `scripts/` utility, not an importable Python module.
The dash matches the Makefile target name (`make audit-public-api`) for
symmetry.

**AST-walk core pattern** (full canonical form already spelled out in
RESEARCH.md lines 256-345 — executor copies that excerpt verbatim).

---

### `Makefile` `audit-public-api` target (modified file, request-response)

**Analog:** `Makefile:34-35` (`cli-smoke-test` target)

**Existing pattern** (verbatim from `Makefile:34-35`):

```makefile
cli-smoke-test:
	bash scripts/cli-smoke-test.sh
```

**`Makefile:7` `.PHONY` declaration** (verbatim — must add
`audit-public-api` token per D-03):

```makefile
.PHONY: init dev up down test test-core cli-smoke-test comply-fix commit docs clean superclean dist dist-upload docker docker-push
```

**Phase 03 target shape** (per RESEARCH.md § Pattern 1 Makefile target,
~line 358; planner verifies the diff path matches the committed
artifact):

```makefile
audit-public-api:
	@pdm run python scripts/audit-public-api.py > /tmp/cement-public-api.txt
	@diff -u .planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt /tmp/cement-public-api.txt
```

**D-03 invariant — STANDALONE target:** Per CONTEXT D-03 the new target
is INDEPENDENT, NOT chained into `make test`, `make comply`, or any
other action. Verify against `Makefile:28-32`:

```makefile
test: comply
	pdm run pytest --cov=cement tests
```

`audit-public-api:` MUST NOT have a prerequisite list (no `:` followed
by another target). Mirrors `cli-smoke-test:` shape exactly.

---

### `pyproject.toml` `[tool.ruff.lint] extend-select` UP+FA addition (ruff config addition)

**Analog:** `pyproject.toml:101-118` (existing Phase 1 D-08 hybrid AUDIT
POINT block — exact pattern to extend)

**Current state** (verbatim from `pyproject.toml:101-118`):

```toml
[tool.ruff.lint]
# AUDIT POINT (D-08): re-review on every ruff bump. New rules added by
# ruff to a selected family fire as CI failures, forcing a deliberate
# add-with-comment to `ignore` or a fix. See Phase 1 RESEARCH.md.
preview = false
extend-select = [
    "E",   # pycodestyle errors
    "F",   # Pyflakes
    "W",   # pycodestyle warnings
    "B",   # flake8-bugbear (NEW, D-06)
    "I",   # isort (NEW, D-06)
    "A",   # flake8-builtins (NEW, D-06)
    "C90", # mccabe complexity (NEW, D-06)
    "N",   # pep8-naming (NEW, D-06)
    "PT",  # flake8-pytest-style (NEW, D-06)
    "T20", # flake8-print (NEW, D-06)
    "YTT", # flake8-2020 (NEW, D-06)
]
```

**Phase 03 target shape** (per D-06 — append `UP` + `FA` family
siblings with their own one-line annotation; the existing AUDIT POINT
comment block above already covers the audit discipline, but the
sibling-line tag identifies the Phase 03 origin for future `git blame`):

```toml
extend-select = [
    "E",   # pycodestyle errors
    "F",   # Pyflakes
    "W",   # pycodestyle warnings
    "B",   # flake8-bugbear (NEW, D-06)
    "I",   # isort (NEW, D-06)
    "A",   # flake8-builtins (NEW, D-06)
    "C90", # mccabe complexity (NEW, D-06)
    "N",   # pep8-naming (NEW, D-06)
    "PT",  # flake8-pytest-style (NEW, D-06)
    "T20", # flake8-print (NEW, D-06)
    "YTT", # flake8-2020 (NEW, D-06)
    "UP",  # pyupgrade (NEW, Phase 03 D-06; lifts Phase 1 D-07 UP ban)
    "FA",  # flake8-future-annotations (NEW, Phase 03 D-06; mechanizes
           # `from __future__ import annotations` removal — D-08)
]
```

**AUDIT POINT comment refresh** (per D-06 "sibling AUDIT POINT comment
naming the UP family addition as the audit point on the NEXT ruff
bump") — recommended planner refinement to the existing
`pyproject.toml:102-104` comment block:

```toml
# AUDIT POINT (D-08, Phase 03 D-06): re-review on every ruff bump. New
# rules added by ruff to a selected family fire as CI failures. The
# UP and FA families (Phase 03) are the highest-churn surfaces — a
# UP rule graduating from preview lands as a deliberate config
# decision, not silent CI red. See Phase 1 RESEARCH.md + Phase 03 D-06.
```

---

### `cement/utils/fs.py` (source-tree refactor: pathlib internals + boundary-preserve via `str(p)`)

**Analogs:**
- `cement/utils/fs.py:75-79` — same file, the `Tmp.__exit__` signature
  is already PEP 604 modern syntax (the only modern-syntax anchor in
  the file). Phase 03 makes the rest consistent.
- `cement/utils/fs.py:104` — current `os.path.abspath` callsite that is
  the canonical migration target.

**Existing modern-syntax anchor** (verbatim from `cement/utils/fs.py:72-79`):

```python
    def __enter__(self):  # type: ignore
        return self

    def __exit__(self,
                 __exc_type: type[BaseException] | None,
                 __exc_value: BaseException | None,
                 __exc_traceback: TracebackType | None) -> None:
        self.remove()
```

**Existing self-flagged TODO comment** (verbatim from
`cement/utils/fs.py:1-11`) — Phase 1 D-14 explicitly preserved this for
Phase 03 to close:

```python
"""Common File System Utilities."""

# derks@2024-06-22: remove after 3.9 is EOL?
from __future__ import annotations

import os
import shutil
import tempfile
from datetime import datetime
from types import TracebackType
from typing import Any, Optional
```

**Existing os.path callsite (BEFORE — verbatim from
`cement/utils/fs.py:82-104`):**

```python
def abspath(path: str, strip_trailing_slash: bool = True) -> str:
    """
    Return an absolute path, while also expanding the ``~`` user directory
    shortcut.

    Args:
        path (str): The original path to expand.

    Returns:
        str: The fully expanded, absolute path to the given ``path``

    Example:

        .. code-block:: python

            from cement.utils import fs

            fs.abspath('~/some/path')
            fs.abspath('./some.file')

    """

    return os.path.abspath(os.path.expanduser(path))
```

**Phase 03 target shape (AFTER — boundary-preserving per D-12):**

```python
def abspath(path: str, strip_trailing_slash: bool = True) -> str:
    p = Path(path).expanduser().resolve(strict=False)
    return str(p)
```

**Existing pragma site to label** (verbatim from
`cement/utils/fs.py:241-245`):

```python
# Kinda dirty, but should resolve issues on Windows per #183
if 'HOME' in os.environ:
    HOME_DIR = abspath(os.environ['HOME'])
else:
    HOME_DIR = abspath('~')  # pragma: nocover
```

Becomes (D-15 vocabulary, `# platform-specific` category):

```python
    HOME_DIR = abspath('~')  # pragma: nocover  # platform-specific
```

---

### `cement/core/foundation.py` (source-tree refactor: pathlib internals + Any tightening + UP family + pragma audit)

**Analogs:**
- `cement/utils/fs.py:75-79` (PEP 604 syntax anchor — same modernization
  shape applies post-UP sweep)
- `cement/core/foundation.py:1315-1317` (current `os.path.isdir`
  callsite — canonical migration target)

**Existing os.path callsite (BEFORE — verbatim from
`cement/core/foundation.py:1315-1317`):**

```python
    def _find_config_files(self, path: str) -> List[str]:
        found_files = []
        if not os.path.isdir(path):
            return []
```

**Phase 03 target shape (AFTER — pathlib internal + UP006
`List[str]` → `list[str]`):**

```python
    def _find_config_files(self, path: str) -> list[str]:
        found_files = []
        if not Path(path).is_dir():
            return []
```

**Existing pragma sites to label** (verbatim from
`cement/core/foundation.py:48,58,123,125`):

```python
if TYPE_CHECKING:
    from types import FrameType, ModuleType, TracebackType  # pragma: nocover
...
if platform.system() == 'Windows':
    SIGNALS = [signal.SIGTERM, signal.SIGINT]   # pragma: nocover
...
            continue  # pragma: nocover
        # ...
            continue  # pragma: nocover
```

Become (D-15 vocabulary):

```python
    from types import FrameType, ModuleType, TracebackType  # pragma: nocover  # TYPE_CHECKING import
...
    SIGNALS = [signal.SIGTERM, signal.SIGINT]   # pragma: nocover  # platform-specific
...
            continue  # pragma: nocover  # untestable: signal handler
            continue  # pragma: nocover  # untestable: signal handler
```

**PROTECTED — DO NOT TOUCH** (`.format(**template_dict)` template
substitution at `cement/core/foundation.py:1359, 1364, 1372, 1377,
1385, 1390, 1478, 1483, 1488, 1492, 1553, 1558, 1563, 1567` per D-19).
RESEARCH.md § Pitfall 1 details the verification grep:

```bash
git diff cement/core/foundation.py | grep -E '\.format\(' || echo "OK"
```

---

### `cement/core/template.py` (source-tree refactor: pathlib internals — ~25 sites, biggest single-file blast)

**Analogs:**
- `cement/utils/fs.py:75-79` (PEP 604 anchor)
- `cement/core/template.py:186-260` (current os.path-heavy `os.walk`
  template-render loop — canonical migration target shape)

**Existing os.path callsites (verbatim sample from
`cement/core/template.py:186-219`):**

```python
        assert os.path.exists(src), f"Source path {src} does not exist!"

        if not os.path.exists(dest):
            os.makedirs(dest)

        LOG.debug(f'copying source template {src} -> {dest}')

        # here's the fun
        for cur_dir, sub_dirs, files in os.walk(src):
            escaped_cur_dir = cur_dir.encode('unicode-escape').decode('utf-8')

            cur_dir_stub: str
            if cur_dir == '.':
                continue    # pragma: nocover
            elif cur_dir == src:
                # don't render the source base dir (because we are telling it
                # where to go as `dest`)
                cur_dir_dest = dest
            ...
                cur_dir_dest = os.path.join(dest, cur_dir_stub)
```

**Phase 03 target shape pattern** (per RESEARCH.md § Pattern 3 +
os.path → pathlib equivalents table at lines 442-453):

| os.path call | pathlib equivalent | Notes |
|--------------|---------------------|-------|
| `os.path.exists(p)` | `Path(p).exists()` | Identical semantics |
| `os.path.join(a, b, c)` | `Path(a) / b / c` | Returns Path; wrap in `str()` for boundary |
| `os.makedirs(p)` | `Path(p).mkdir(parents=True, exist_ok=True)` | Note `exist_ok=True` matches existing `os.makedirs` semantics if branched |

**PROTECTED — DO NOT TOUCH:** `cement/core/template.py:359+`
`.format(**template_dict)` template substitution per D-19.

---

### `cement/core/config.py` (source-tree refactor: pathlib internals — minimal blast, 1 callsite)

**Analogs:**
- `cement/utils/fs.py:75-79` (PEP 604 anchor)
- `cement/core/config.py:225-226` (the single os.path callsite)

**Existing os.path callsite (verbatim from `cement/core/config.py:218-231`):**

```python
            file_path (str): The file system path to the configuration file.

        Returns:
            bool: ``True`` if the given ``file_path`` was parsed, and ``False``
                otherwise.

        """
        file_path = abspath(file_path)
        if os.path.exists(file_path):
            LOG.debug(f"config file '{file_path}' exists, loading settings...")
            return self._parse_file(file_path)
        else:
            LOG.debug(f"config file '{file_path}' does not exist, skipping...")
            return False
```

**Phase 03 target shape (AFTER):**

```python
        file_path = abspath(file_path)
        if Path(file_path).exists():
            LOG.debug(f"config file '{file_path}' exists, loading settings...")
            return self._parse_file(file_path)
```

This is the smallest of the four pathlib commits. Per CONTEXT D-13,
order is `cement/utils/fs.py` FIRST (foundational), then the three
`cement/core/*.py` files in any order — `config.py` is a natural
warm-up after fs.py given the 1-callsite blast.

---

### pragma:nocover category-label sweep (test/coverage policy comment, ~141 sites across `cement/`)

**Analogs:**
- `cement/cli/main.py:53` — existing pragma site WITH a sibling comment
  (the closest existing `# pragma: ... # <text>` SHAPE in the codebase)
- `cement/ext/ext_logging.py:35` — same pattern with both `# type:
  ignore` AND `# noqa` siblings (most decorated existing example)

**Existing sibling-comment SHAPE** (verbatim from
`cement/cli/main.py:53`):

```python
            print(f'AssertionError > {e.args[0]}')  # pragma: nocover  # noqa: T201
```

**Most-decorated existing pragma site** (verbatim from
`cement/ext/ext_logging.py:35`):

```python
        def createLock(self):  # type: ignore  # pragma: no cover  # noqa: N802 - overrides logging.Handler.createLock (stdlib camelCase)
```

**Existing untagged pragma sites** (verbatim from
`cement/core/cache.py:49`, `cement/core/backend.py:3`,
`cement/utils/fs.py:237`):

```python
        pass    # pragma: nocover
```

```python
VERSION = (3, 0, 15, 'final', 0)  # pragma: nocover
```

```python
        else:
            break  # pragma: nocover
```

**Phase 03 target shape (D-15 locked vocabulary append):**

```python
        pass    # pragma: nocover  # abstract method
```

```python
VERSION = (3, 0, 15, 'final', 0)  # pragma: nocover  # version constant
```

```python
        else:
            break  # pragma: nocover  # defensive: unreachable
```

**Locked vocabulary** (verbatim D-15):

| Category label | When to apply |
|----------------|---------------|
| `# abstract method` | interface `pass` lines |
| `# TYPE_CHECKING import` | deferred imports under `if TYPE_CHECKING:` |
| `# platform-specific` | env / OS / Windows fallbacks |
| `# untestable: dynamic import` | runtime `__import__` / `importlib.import_module` |
| `# untestable: subprocess` | shell / git subprocess calls |
| `# untestable: signal handler` | signal-handler internals |
| `# defensive: unreachable` | else branches coverage.py can't prove unreachable |
| `# version constant` | module-level version tuples |

**D-17 verification grep** (verbatim from CONTEXT.md):

```bash
grep -nE 'pragma:\s*no\s*cover' cement/ \
  | grep -vE '# (abstract method|TYPE_CHECKING import|platform-specific|untestable: dynamic import|untestable: subprocess|untestable: signal handler|defensive: unreachable|version constant)'
```

Must return empty.

**Note on dual spelling** — coverage.py honors both `# pragma: nocover`
(no space, ~110 sites) and `# pragma: no cover` (with space, ~31 sites).
RESEARCH.md § Critical syntax-form variants recommends NOT canonicalizing
spelling (would create huge churn). The locked-vocabulary regex matches
both via `\s*`.

---

### `03-PUBLIC-API-BASELINE.txt` (NEW — planning-artifact baseline file)

**Analogs:**
- `.planning/phases/02-dependencies-ci-pipeline/02-PIP-AUDIT.md` —
  closest "frozen snapshot for later diff" precedent in the project's
  planning artifacts (different format — Markdown table — but same
  policy intent: capture a known state for later regression check).

**Format** (per CONTEXT D-04 — sorted plain text, one symbol per line):

```
cement.core.cache:CacheHandler
cement.core.cache:CacheHandler.delete
cement.core.cache:CacheHandler.get
cement.core.cache:CacheHandler.list
cement.core.cache:CacheHandler.purge
cement.core.cache:CacheHandler.set
cement.core.foundation:App
cement.core.foundation:App.Meta
cement.core.foundation:App.Meta.argument_handler
...
```

Captured as the FIRST phase commit `docs(03): capture public API
baseline` (per CONTEXT D-04, D-22 step 1). Production via:

```bash
pdm run python scripts/audit-public-api.py > \
  .planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt
```

---

### `03-VERIFICATION.md` (NEW — planning-artifact verification report)

**Analogs:**
- `.planning/phases/01-tooling-baseline-python-matrix/01-VERIFICATION.md`
  (canonical verification-doc shape — YAML frontmatter, Goal Achievement
  table, Required Artifacts, Behavioral Spot-Checks, Requirements
  Coverage)
- `.planning/phases/02-dependencies-ci-pipeline/02-VERIFICATION.md`
  (Phase 2 instance with PENDING-evidence pattern — shows how to mark
  conditions that can only be verified post-PR-open)

**Existing frontmatter pattern** (verbatim from
`.planning/phases/01-tooling-baseline-python-matrix/01-VERIFICATION.md:1-7`):

```markdown
---
phase: 01-tooling-baseline-python-matrix
verified: 2026-04-30T15:00:00Z
status: passed
score: 11/11 must-haves verified
overrides_applied: 0
---
```

**Existing section structure** (Phase 1 + Phase 2):

1. Goal Achievement (Observable Truths table)
2. Required Artifacts (file existence + content table)
3. Key Link Verification (cross-reference wiring)
4. Behavioral Spot-Checks (commands run + results)
5. Requirements Coverage (REQ-ID → SATISFIED rows)
6. Anti-Patterns Found (info-level findings if any)
7. Human Verification Required
8. Gaps Summary

**Phase 03 D-24 mapping** — VERIFICATION.md must capture:
- Pre/post `Any` count (per D-09; CONTEXT says ~25, RESEARCH says
  actual is **40**; planner uses 40)
- Pre/post audit-public-api diff (must be empty per D-04/D-24)
- `make audit-public-api` exit status (must be 0)
- REFACTOR-01 acceptance-via-coverage rationale (per D-20)
- Locked-vocabulary grep result (must be empty per D-17)
- `os.path` grep result in scoped files (must be empty OR only
  `# boundary: str`-tagged sites per D-14)
- `from __future__ import annotations` grep result across `cement/`
  (must be empty per D-08 / FA100)

## Shared Patterns

### Hybrid AUDIT POINT comment (Phase 1 D-08, applied to Phase 03 D-06)

**Source:** `pyproject.toml:67-72, 78-84, 101-105, 119-122, 139-140,
173-178` — six existing AUDIT POINT comments.

**Apply to:** Any new ruff / mypy / coverage / linter config addition
in this phase (D-06 UP+FA addition is the only one).

**Verbatim canonical form** (from `pyproject.toml:101-105`):

```toml
[tool.ruff.lint]
# AUDIT POINT (D-08): re-review on every ruff bump. New rules added by
# ruff to a selected family fire as CI failures, forcing a deliberate
# add-with-comment to `ignore` or a fix. See Phase 1 RESEARCH.md.
preview = false
```

### Atomic-per-concern conventional commit (Phase 1 D-02/D-04 + Phase 2 D-17)

**Source:** Phase 1 D-04 family-split discipline; Phase 2 D-17
commit-shape continuity. The Phase 1/2 git log is the canonical
shape — every commit subject ≤ 78 chars, body wrapped at 78 chars,
Conventional Commits prefixes (`fix:`, `chore:`, `refactor:`,
`docs:`, `feat:`, `test:`).

**Apply to:** All Phase 03 commits per D-22 14-step suggested sequence.

**Sample shape** (verbatim from Phase 1 commit log):

```
fix(lint): resolve PT006 pytest parametrize argname tuple-style
chore(ruff): bump ruff to 0.15
refactor(test): audit pragma:nocover sites with category labels
```

### Permanent-dev-affordance precedent (D-05)

**Source:** `scripts/cli-smoke-test.sh` + `Makefile:34-35`
`cli-smoke-test:` target — both retained from quick task `260430-i7q`
as a permanent dev affordance, not phase-throwaway.

**Apply to:** `scripts/audit-public-api.py` + `Makefile`
`audit-public-api:` target. Both stay in the tree post-Phase-03 for
all 3.0.x patch work and Phase 5 deprecation cycles to use as
regression checks.

### Boundary-preservation rule (D-12; pathlib migration)

**Source:** Documented in CONTEXT D-12 + RESEARCH.md § Pattern 3.

**Apply to:** All four pathlib-scoped files (`cement/utils/fs.py`,
`cement/core/foundation.py`, `cement/core/template.py`,
`cement/core/config.py`).

**Rule:** Locals are `Path`. Every public return goes back through
`str(p)`. `HOME_DIR` stays a `str` constant. `Tmp.dir` / `Tmp.file`
stay `str` instance attributes. ZERO bytes change to public type
signatures. The audit-public-api gate (D-04) verifies this.

## No Analog Found

Files / conventions with no close match in the codebase. The planner
should use RESEARCH.md patterns directly for these.

| File / Convention | Role | Why no analog | Planner reference |
|-------------------|------|---------------|-------------------|
| Locked-vocabulary `# pragma: nocover` category labels (D-15..D-18) | inline source comment convention | This is a brand-new convention being seeded by Phase 03. NO existing pragma site in `cement/` carries a category label from the locked vocabulary — only ad-hoc sibling comments like `# noqa: T201` (cli/main.py:53) and free-form `# overrides logging.Handler.createLock` (ext_logging.py:35) | RESEARCH.md § Example 1 (lines 590-677) — eight before/after examples covering all eight categories |
| `03-PUBLIC-API-BASELINE.txt` exact line format | planning artifact format | No existing `.planning/phases/*/0*-*BASELINE*.txt` artifact exists. The closest planning-artifact precedent is `02-PIP-AUDIT.md` (Markdown), but that's a different format | CONTEXT D-04 ("one `module:ClassName.method` per line") + RESEARCH.md § Pattern 1 (the AST script's stdout format defines the file format) |

## Metadata

**Analog search scope:**
- `scripts/` (Python script header analog)
- `Makefile` (target shape analog)
- `pyproject.toml` (ruff config block analog + AUDIT POINT pattern)
- `cement/utils/fs.py` (PEP 604 anchor + pathlib migration target)
- `cement/utils/*.py` (pathlib usage check — none found)
- `cement/core/foundation.py` (os.path migration target + pragma sites)
- `cement/core/template.py` (os.path migration target — biggest blast)
- `cement/core/config.py` (os.path migration target — minimal blast)
- `cement/cli/main.py` + `cement/ext/ext_logging.py` (existing pragma
  sibling-comment shape)
- `.planning/phases/01-tooling-baseline-python-matrix/01-VERIFICATION.md`
  (verification-doc shape)
- `.planning/phases/02-dependencies-ci-pipeline/02-VERIFICATION.md`
  (verification-doc with PENDING-evidence pattern)
- `.planning/phases/02-dependencies-ci-pipeline/02-PIP-AUDIT.md`
  (closest "frozen snapshot for later diff" precedent)

**Files scanned:** ~15 files, all targeted reads (no whole-file scans
beyond `Makefile` and `pyproject.toml` which are small)

**Pattern extraction date:** 2026-05-03
