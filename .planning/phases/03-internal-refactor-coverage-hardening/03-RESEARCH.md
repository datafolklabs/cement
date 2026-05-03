# Phase 03: Internal Refactor & Coverage Hardening - Research

**Researched:** 2026-05-03
**Domain:** Python tooling refactor (ruff UP/FA family, AST audit, pathlib migration, pragma vocabulary)
**Confidence:** HIGH

## Project Constraints (from CLAUDE.md)

- **100% coverage gate is absolute** (`fail_under = 100` + `--cov-fail-under=100`); every commit in this phase must land green.
- **PEP 8 / ruff compliance is absolute**; `make comply-ruff` runs `ruff check cement/ tests/`.
- **mypy compliance is absolute**; `make comply-mypy` runs against the `cement/` tree (tests excluded).
- **Zero new core runtime dependencies.** Optional extras only — no new dev deps either, per Phase 03 D-02 (stdlib `ast` only for the audit script).
- **Conventional Commits**, subject ≤ 78 chars, body wrapped at 78 chars.
- **No public-API breakage on the 3.0.x track** — including subclass-exposed internals (the AST audit baseline is the literal enforcement of this).
- **Python 3.10–3.14 + pypy-3.10/3.11 matrix.** PEP 585 / PEP 604 syntax requires runtime ≥ 3.10 once `from __future__ import annotations` is removed. Verified: `requires-python = ">=3.10"` in `pyproject.toml:19`.
- **`make commit`** (`pdm run cz commit`) is the conventional authoring path; direct `git commit` is also allowed when the message follows the convention.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Public API contract (Area 1)**
- **D-01:** Public surface = anything not `_`-prefixed. Module-level names AND class attributes/methods across `cement/__init__.py`, `cement/core/*`, `cement/ext/*`, `cement/utils/*`, `cement/cli/*`. Includes `App.Meta.<attr>` names that subclasses set (`config_defaults`, `extensions`, `handlers`, `meta_override`, `core_interfaces`, etc.), interface abstract methods, handler public methods, exception classes. Excludes `_setup`, `_validate`, `_meta`, `_get_*`, `_parse_*`, `_make_*`.
- **D-02:** AST-walk audit script — `scripts/audit-public-api.py` (dash-named). Walks the AST of every `.py` module under `cement/`, dumps non-underscore module-level names, class names, class public attributes, and class public method names to stdout (sorted). Script header MUST include commentary about purpose. Uses stdlib `ast` only — no new dev-dep.
- **D-03:** `make audit-public-api` Makefile target — INDEPENDENT. NOT chained into `make test`, `make comply`, or any other make action. Exit non-zero on diff vs the committed baseline.
- **D-04:** Baseline snapshot — sorted text file `.planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt`, one `module:ClassName.method` (or `module:NAME` for module-level) per line. Captured as the FIRST phase commit `docs(03): capture public API baseline`. Acceptance: `make audit-public-api` exits 0.
- **D-05:** Audit script + Makefile target are retained as permanent dev affordances post-Phase-03.

**Type-hint modernization (Area 2)**
- **D-06:** Re-enable ruff `UP` family in `[tool.ruff.lint] extend-select` per Phase 1 D-08 hybrid pattern. Add a sibling AUDIT POINT comment naming the `UP` family addition as the audit point on the NEXT ruff bump. Phase 03 also adds ruff `FA` family for `from __future__ import annotations` detection.
- **D-07:** UP migration scope = all of `cement/` + `tests/`. Lands as `fix(lint): resolve UPxxx <name>` commits per Phase 1 D-04 family-split discipline (one commit per `UP` rule code).
- **D-08:** Drop `from __future__ import annotations` from all 28 files in this phase. Removal MUST land AFTER UP006/UP007/UP045 land. Ruff `FA100`/`FA102` family in `extend-select` mechanizes detection.
- **D-09:** `Any` reduction in `cement/core/` — baseline-and-tighten approach. First commit captures the count via `grep -E ': Any\b|-> Any\b|Any\]' cement/core/*.py | wc -l` (~25 today); record in `03-VERIFICATION.md`. Hand-tighten where actual narrower type is known. `**kw: Any` and argparse `_parsed_args: Any` may stay. Each surviving `Any` carries an inline comment justifying it. Acceptance: post-count STRICTLY LOWER than pre-count.
- **D-10:** Mypy strictness knobs untouched.

**pathlib migration (Area 3)**
- **D-11:** Migration scope = `cement/utils/fs.py` + `cement/core/foundation.py` + `cement/core/template.py` + `cement/core/config.py`. `cement/cli/`, `cement/ext/*` stay on `os.path`.
- **D-12:** Boundary-preservation — internal-only `Path`; `str` at every boundary. `HOME_DIR` stays a `str` constant. `Tmp.dir`/`Tmp.file` stay `str` instance attributes. ZERO bytes change to public type signatures.
- **D-13:** Atomic commit per migrated file. Four commits, `cement/utils/fs.py` FIRST (foundational).
- **D-14:** Inline `# boundary: str` comment on any remaining `os.path.*` callsite in scoped files.

**pragma:nocover audit (Area 4 — COV-03)**
- **D-15:** Locked vocabulary on every site: `# abstract method`, `# TYPE_CHECKING import`, `# platform-specific`, `# untestable: dynamic import`, `# untestable: subprocess`, `# untestable: signal handler`, `# defensive: unreachable`, `# version constant`.
- **D-16:** Vocabulary expansion requires CONTEXT amendment, NOT free-form labels.
- **D-17:** Grep verification (locked-vocabulary regex) must return empty. Captured in `03-VERIFICATION.md`.
- **D-18:** Audit lands AFTER refactor commits in a single sweep (or per-file if blast radius warrants splitting).

**Modern stdlib idioms (REFACTOR-04 closeout)**
- **D-19:** Ruff-driven only. UP032 handles `LOG.debug('%s' % ...)` sites mechanically. `cached_property` and `contextlib.suppress` adoption is opportunistic only. **`.format(**template_dict)` calls in `cement/core/foundation.py` lines 1359, 1364, 1372, 1377, 1385, 1390, 1478, 1483, 1488, 1492, 1553, 1558, 1563, 1567 MUST NOT be touched** — cement's own template substitution path. Same for `cement/core/template.py:359+`.

**Dead code (REFACTOR-01)**
- **D-20:** Acceptance via existing 100% coverage gate. No `vulture`, no whitelist file.
- **D-21:** Risk acknowledgement that D-20 leaves covered-but-functionally-dead code and unused private helpers undetected.

**Commit shape (Phase 1/2 conventions)**
- **D-22:** Atomic per-concern, Conventional Commits, 78-char wrap. Suggested 14-step sequence; planner may refine.
- **D-23:** GSD artifact commits follow `docs(03): ...` shape.

**Acceptance**
- **D-24:** Phase 03 acceptance is the conjunction of 9 conditions:
  1. `make test` passes at 100% coverage
  2. `make comply-ruff` passes with `UP` family enabled
  3. `make comply-mypy` passes
  4. `make audit-public-api` exits 0
  5. `coverage-report/` HTML generates without warnings
  6. Pre/post `Any`-in-`cement/core/` count delta is strictly positive in reduction direction
  7. Locked-vocabulary grep returns empty
  8. `grep -rn 'os\.path' cement/utils/fs.py cement/core/` returns only `# boundary: str`-tagged sites OR returns empty
  9. `from __future__ import annotations` returns no matches across `cement/`

### Claude's Discretion

- Specific message-body phrasing within the D-22 commit split.
- Whether to author commits via `make commit` or `git commit` directly.
- Order of UP-family fix commits (UP006 vs UP007 vs UP045 — no semantic dependency).
- Whether to split D-22 step 8 (`refactor(core): tighten Any types`) per file or single commit.
- Whether to split D-22 step 13 (pragma audit) per file.
- Whether `cached_property` or `contextlib.suppress` adoption yields opportunistic commits beyond UP032.
- Exact wording of inline `# boundary: str` and `Any` justification comments.

### Deferred Ideas (OUT OF SCOPE)

- vulture-based dead-code audit
- Closing High-priority untestable `pragma: nocover` blocks (signal hooks, ext_plugin dynamic imports, ext_daemon FD ops, ext_watchdog single-tuple, ext_generate template loading)
- Signal-handler refactor (CONCERNS.md tech-debt #1)
- Logging handler cross-contamination (CONCERNS.md tech-debt #2)
- Mypy strictness knob tightening
- pathlib migration in `cement/cli/` and `cement/ext/*`
- FIXME-comment cleanup (9 outstanding `# FIXME` comments)
- CONVENTIONS.md type-annotation refresh (recommended here as an opportunistic `docs(codebase):` commit, but planner may punt to Phase 5 DOCS-04)
- `cached_property` / `contextlib.suppress` opportunistic adoption beyond what UP032 surfaces
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REFACTOR-01 | Dead code identified and removed without affecting public API or test coverage | D-20 acceptance via existing 100% coverage gate (`fail_under = 100` + `--cov-fail-under=100`). No new tooling — research confirms the trade is workable: 100% statement coverage demonstrably catches dead-code-by-removal but not dead-by-no-meaningful-assert. Risk recorded in D-21. |
| REFACTOR-02 | Type hints tightened in `cement/core/` — fewer `Any`, more precise generics | Pre-count via `grep -E ': Any\b|-> Any\b|Any\]' cement/core/*.py \| wc -l` returns **40 sites** (verified 2026-05-03 — see "Any-in-core inventory" below). Each surviving `Any` carries inline justification per D-09. `**kw: Any` and argparse `_parsed_args: Any` exemption documented. |
| REFACTOR-03 | `os.path` → `pathlib` in `cement/utils/fs.py` and core internals where it doesn't change public signatures | Ruff/pathlib mapping table below. Boundary preservation via `str(Path)` at every public return. Verified os.path callsite inventory in scoped files: 39 sites total (fs.py 12, foundation.py 6, template.py 14, config.py 1; some sites span multiple os.path calls per line). |
| REFACTOR-04 | Modern stdlib idioms applied where backward-compatible (f-strings everywhere, contextlib helpers, cached_property) | Driven entirely by ruff `UP` family per D-19. UP032 (printf → f-string) covers ~14 LOG.debug %-format sites mechanically. UP032 verified NOT to touch `.format(**dict)` calls (the protected foundation.py + template.py template-substitution sites). |
| COV-01 | `make test` produces 100% coverage report | Already wired (Phase 2 D-10/D-11). Phase 03 must HOLD this — every commit must land green. |
| COV-02 | Coverage HTML report generates without warnings | Already wired (Phase 2). Verification command: `pdm run pytest && ls coverage-report/index.html`. |
| COV-03 | `pragma: no cover` exclusions audited; each remaining one has a code comment justifying it | Locked-vocabulary regex per D-15/D-17. Verified actual count is **141 sites** (see "Pragma site inventory" below — note: CONTEXT.md says "123" but live grep returns 141; reconcile in plan). |
</phase_requirements>

## Summary

This is a tightly-scoped refactor phase with three pillars: (1) ruff-driven mechanical modernization (UP family + FA family), (2) pathlib migration with strict str-boundary preservation in 4 named files, and (3) pragma:nocover vocabulary lock-down across 141 sites. The 100% coverage gate (Phase 2) and the new AST public-API audit (Phase 03 D-02..D-04) are the two enforcement surfaces — every commit must hold both green.

**Critical surprise:** the actual `pragma: nocover` count is **141** (verified by `grep -rn "pragma:\s*no\s*cover" cement/ | wc -l` on 2026-05-03), not 123 as CONTEXT.md states. This is a 15% planning-time delta. Planner should reconcile — likely the count grew between when CONCERNS.md was written (2026-04-24) and today, or the original count missed `# pragma: no cover` (with space) variants. Either way, the audit pass touches 141 lines, not 123.

**Critical syntax-form variants:** the existing pragmas use BOTH `# pragma: nocover` (no space, ~110 sites) AND `# pragma: no cover` (with space, ~31 sites). Coverage.py honors both. The locked-vocabulary regex `pragma:\s*no\s*cover` correctly matches both. The audit commit MUST canonicalize to one form (recommend `# pragma: nocover` since it's the more common existing form) OR the locked-vocabulary appended labels must coexist with both spellings — planner picks.

**Primary recommendation:** Execute D-22's 14-step sequence as proposed, with two refinements: (a) reconcile the 123→141 pragma count surprise as a planning-time finding before D-22 step 13, and (b) run a CONVENTIONS.md update commit as `docs(codebase):` between UP045 and the FA100 strip so source-of-truth doc never lies after the modern-syntax sweep.

## Architectural Responsibility Map

This phase has no runtime tier mapping — it's a refactor across the existing tier surface. Capability ownership stays where Phase 1/2 left it:

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Public-API audit (NEW) | Local dev tooling | — | `scripts/audit-public-api.py` runs locally via `make audit-public-api`; NOT chained into CI per D-03. Permanent affordance per D-05. |
| Refactor verification | CI matrix (existing) | Local dev | Phase 03 inherits Phase 2's CI lanes (3.10/3.11/3.12/3.13/3.14/pypy-3.10/pypy-3.11) plus the existing `make comply` + 100% coverage gate. No new CI surface. |
| Lint enforcement | ruff (existing) | — | UP + FA family additions extend the existing `extend-select` block; no new tool. |
| pathlib migration | `cement/utils/fs.py` + `cement/core/*` (4 files) | — | Out of scope for `cement/cli/` and `cement/ext/*` per D-11. |

## Standard Stack

### Core (No New Tools)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| ruff | `~=0.15.12` (pinned) | Lint + auto-fix UP family migration | Already adopted (Phase 1 D-12). UP family covers UP006/UP007/UP045/UP032/FA100/FA102 mechanically. |
| stdlib `ast` | Python 3.10+ | AST walk for public-API audit script | Per D-02 — no new dev-dep. `ast.parse` + `ast.NodeVisitor` is the canonical pattern. |
| stdlib `pathlib` | Python 3.10+ | Replace os.path internals in 4 named files | Standard library, modern OOP path API. |
| coverage.py | `>=7.13.5` (pinned) | 100% gate enforcement (existing) | Phase 2 D-10. Pragma:nocover comment audit doesn't change measurement; just adds labels. |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| stdlib `difflib` | Python 3.10+ | Optional — could enrich `make audit-public-api` failure output to show added/removed lines | If `diff -u` (D-04 default) is too terse |
| stdlib `subprocess` | Python 3.10+ | The audit script itself doesn't need it; the Makefile target uses `diff` directly | N/A |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| stdlib `ast` walker | `inspect`-based runtime introspection | Rejected: requires importing every cement module, which has side effects (extension loading, hook registration). AST is purely lexical → safe + fast + no side effects. |
| stdlib `ast` walker | `griffe` library (~mkdocstrings) | Rejected: new dev-dep, violates D-02 stdlib-only constraint. |
| Manual %-format → f-string | Ruff UP032 auto-fix | Use UP032 — it's the entire point of D-19. UP032 known-not-to-touch `.format(**dict)` (verified — see Pitfall 1 below). |
| `pathlib.PurePath` | `pathlib.Path` | Use `Path`. fs.py needs filesystem-touching methods (`.exists()`, `.is_file()`, `.is_dir()`); `PurePath` is purely lexical. |

**Installation:** None required — all tools already pinned in Phase 1.

**Version verification (2026-05-03):**
- `ruff ~=0.15.12` (pyproject.toml:230, verified)
- `mypy ~=1.20.2` (pyproject.toml:229, verified)
- `coverage >=7.13.5` (pyproject.toml:228, verified)
- Python: `3.14.3` available locally [VERIFIED: `python3 --version`]
- PDM: `2.26.6` [VERIFIED: `pdm --version`]

## Architecture Patterns

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ Phase 03 Refactor Surface (no runtime architecture change)      │
└─────────────────────────────────────────────────────────────────┘

  Source surface                 Tooling                      Verification
  ──────────────                 ───────                      ────────────
                                                              
  cement/ + tests/  ─────────►  ruff UP+FA family  ─────►   make comply-ruff
                                                              ↓
                                                              [must be green]
                                                              
  cement/utils/fs.py            os.path → Path  (str        cement/core/foundation.py
  cement/core/foundation.py     boundary preserved at      ── grep -rn 'os.path' →
  cement/core/template.py       every public return)         only `# boundary:` tagged sites
  cement/core/config.py
                                                              
  cement/core/* (Any sites)  ─► hand-tighten where ──►  grep ': Any\b|-> Any\b|Any\]'
                                narrower type known      cement/core/*.py | wc -l
                                                              ↓
                                                              [post < pre]
                                                              
  All 141 pragma sites      ─► append locked-vocab    ─►  grep -nE 'pragma:\s*no\s*cover' cement/
                                category labels             | grep -vE '<8-cat regex>'
                                                              ↓
                                                              [must return empty]
                                                              
  scripts/audit-public-api.py ► AST walk → sorted     ─►  make audit-public-api
                                non-underscore symbol       ↓
                                inventory                   diff vs 03-PUBLIC-API-BASELINE.txt
                                                              ↓
                                                              [exit 0]
```

### Recommended Project Structure (post-phase)

```
cement/                       # untouched layout
├── core/                     # 4 files migrate to pathlib internals
│   ├── foundation.py
│   ├── template.py
│   ├── config.py
│   └── ... (Any-tightening across the module)
├── utils/
│   └── fs.py                 # pathlib internals; str at every public boundary
├── ext/                      # NOT in pathlib scope (D-11); UP family applies
└── cli/                      # NOT in pathlib scope; UP family applies

scripts/
├── audit-public-api.py       # NEW — dash-named per D-02; stdlib ast only
├── cli-smoke-test.sh         # existing precedent for permanent dev script
└── ...

.planning/phases/03-internal-refactor-coverage-hardening/
├── 03-CONTEXT.md             # existing — locked decisions
├── 03-RESEARCH.md            # this file
├── 03-PUBLIC-API-BASELINE.txt # NEW — first commit artifact
├── 03-VERIFICATION.md        # NEW — Any pre/post counts, audit exit, etc.
└── (planner adds 03-PLAN-*.md)
```

### Pattern 1: AST-walk Public API Audit Script

**What:** Walk `cement/**/*.py` AST, emit sorted non-underscore symbols.

**When to use:** Run before any refactor commit; baseline is the comparison point. Re-run after every refactor commit (locally or via `make audit-public-api`) to verify no public surface drift.

**Example (canonical pattern, source: Python 3.10+ stdlib `ast` docs):**
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


def is_public(name: str) -> bool:
    return not name.startswith('_')


def collect_module_symbols(tree: ast.Module, mod_name: str) -> list[str]:
    out: list[str] = []
    for node in tree.body:
        # Module-level names: assignments, function defs, class defs
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and is_public(target.id):
                    out.append(f"{mod_name}:{target.id}")
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and is_public(node.target.id):
                out.append(f"{mod_name}:{node.target.id}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if is_public(node.name):
                out.append(f"{mod_name}:{node.name}")
        elif isinstance(node, ast.ClassDef):
            if is_public(node.name):
                out.append(f"{mod_name}:{node.name}")
                out.extend(collect_class_members(node, mod_name))
    return out


def collect_class_members(cls: ast.ClassDef, mod_name: str) -> list[str]:
    out: list[str] = []
    for node in cls.body:
        # Methods (including @property, @classmethod, @staticmethod)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if is_public(node.name):
                out.append(f"{mod_name}:{cls.name}.{node.name}")
        # Class-level attribute assignments (Meta inner-class attrs included)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and is_public(target.id):
                    out.append(f"{mod_name}:{cls.name}.{target.id}")
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and is_public(node.target.id):
                out.append(f"{mod_name}:{cls.name}.{node.target.id}")
        # Nested classes (Meta is the canonical case)
        elif isinstance(node, ast.ClassDef) and is_public(node.name):
            nested = f"{cls.name}.{node.name}"
            out.append(f"{mod_name}:{nested}")
            for inner in node.body:
                if isinstance(inner, ast.Assign):
                    for tgt in inner.targets:
                        if isinstance(tgt, ast.Name) and is_public(tgt.id):
                            out.append(f"{mod_name}:{nested}.{tgt.id}")
                elif isinstance(inner, ast.AnnAssign):
                    if isinstance(inner.target, ast.Name) and is_public(inner.target.id):
                        out.append(f"{mod_name}:{nested}.{inner.target.id}")
                elif isinstance(inner, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if is_public(inner.name):
                        out.append(f"{mod_name}:{nested}.{inner.name}")
    return out


def module_name_for(path: Path, root: Path) -> str:
    rel = path.relative_to(root.parent)
    parts = list(rel.with_suffix('').parts)
    return '.'.join(parts)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    cement_root = repo_root / 'cement'
    symbols: list[str] = []
    for py in sorted(cement_root.rglob('*.py')):
        # Skip generated-project templates per pyproject `omit`
        rel = py.relative_to(repo_root)
        if str(rel).startswith('cement/cli/templates/'):
            continue
        if str(rel).startswith('cement/cli/contrib/'):
            continue
        mod_name = module_name_for(py, cement_root)
        try:
            tree = ast.parse(py.read_text())
        except SyntaxError as e:
            print(f"SYNTAX ERROR in {py}: {e}", file=sys.stderr)
            return 2
        symbols.extend(collect_module_symbols(tree, mod_name))
    for line in sorted(set(symbols)):
        print(line)
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

**Edge cases the script handles (verified against codebase 2026-05-03):**
- `__all__` lists (e.g., `cement/__init__.py:14`) — these are themselves public assignments; the AST walker treats `__all__` as a module-level name (it's underscore-prefixed-and-suffixed → excluded by the `not name.startswith('_')` filter). The members of `__all__` are already counted via their direct module-level appearance. Verified: `__all__` only appears in `cement/__init__.py`.
- `@dataclass` classes (e.g., `cement/ext/ext_argparse.py:106 CommandMeta`) — class fields declared as `AnnAssign` at class body top level; handled by `collect_class_members` annotation branch.
- `@property` / `@classmethod` / `@staticmethod` decorators — these wrap `FunctionDef`; handled normally.
- `Meta` inner classes (e.g., `App.Meta`, `SMTPMailHandler.Meta`) — handled by the nested-class branch; their attributes (`label`, `config_defaults`, `extensions`, etc.) are emitted as `module:OuterClass.Meta.<attr>`. Verified Meta subclasses across `cement/core/` and `cement/ext/`.
- `ext_argparse.expose` (decorator class with `# noqa: N801`) — public `class expose`; emitted normally.

**[CITED: https://docs.python.org/3/library/ast.html — `ast.parse`, `ast.NodeVisitor`, `ast.ClassDef`, `ast.FunctionDef`, `ast.Assign`, `ast.AnnAssign`]**

**Makefile target (D-03):**
```makefile
audit-public-api:
	@pdm run python scripts/audit-public-api.py > /tmp/cement-public-api.txt
	@diff -u .planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt /tmp/cement-public-api.txt
```

Add `audit-public-api` to the `.PHONY` line. The `@diff -u` exits non-zero on diff, which is exactly D-03's exit-condition.

### Pattern 2: Ruff UP Family Atomic-Per-Rule Sequencing

**What:** When `make comply-ruff-fix` rewrites the entire codebase under the new UP rule family, split the result into one commit per rule code (UP006, UP007, UP045, UP032, FA100, FA102) for bisect friendliness.

**When to use:** D-22 steps 3–7. The auto-fix is bulk, but the commit history must be atomic.

**Example (per-rule selective fix):**
```bash
# Step 1: enable UP+FA family (config commit only, no source change yet)
git commit -am "chore(ruff): re-enable UP family with AUDIT POINT comment"

# Step 2: per-rule fix passes
pdm run ruff check --select UP006 --fix cement/ tests/  # PEP585 builtin generics
git add -A && git commit -m "fix(lint): resolve UP006 List → list, Dict → dict"

pdm run ruff check --select UP007 --fix cement/ tests/  # PEP604 unions
git add -A && git commit -m "fix(lint): resolve UP007 Union → |"

pdm run ruff check --select UP045 --fix cement/ tests/  # PEP604 X | None
git add -A && git commit -m "fix(lint): resolve UP045 Optional → X | None"

pdm run ruff check --select UP032 --fix cement/ tests/  # f-string conversions
# IMPORTANT: review per-file diff to verify no .format(**template_dict) sites
# in cement/core/foundation.py:1359..1567 or cement/core/template.py:359+
git diff cement/core/foundation.py cement/core/template.py | grep -E 'format' || true
git add -A && git commit -m "fix(lint): resolve UP032 printf → f-string"

# Step 3: drop from __future__ AFTER UP006/UP007/UP045 land (per D-08)
pdm run ruff check --select FA100 --fix cement/ tests/  # removes future-annotations
git add -A && git commit -m "fix(lint): resolve FA100 future-annotations imports"
```

**[CITED: https://docs.astral.sh/ruff/rules/#pyupgrade-up — `--select` flag accepts rule codes for selective enforcement]**

**[VERIFIED: WebSearch 2026-05-03] UP032 known limitation:** UP032 only converts `'literal'.format(arg)` calls (positional or keyword args). It does NOT touch `.format(**dict)` (dict spread) — that's why the protected sites in `foundation.py:1359..1567` and `template.py:359+` won't be auto-rewritten. (See https://github.com/astral-sh/ruff/issues/9227 — Ruff's UP032 fixer respects expression complexity boundaries.) Per-file `git diff` review before commit is still recommended as belt-and-braces verification.

### Pattern 3: Pathlib Boundary-Preserving Migration

**What:** Inside the function, locals are `Path`. At every public return or exception path, `str(p)`. Public function signatures unchanged.

**When to use:** All four scoped files (D-11). Critical for `cement/utils/fs.py` because every function in that module has a public signature `def func(path: str) -> str`.

**Example (canonical fs.py shape):**
```python
# BEFORE (cement/utils/fs.py:82-104, abspath)
def abspath(path: str, strip_trailing_slash: bool = True) -> str:
    return os.path.abspath(os.path.expanduser(path))

# AFTER (boundary preservation)
def abspath(path: str, strip_trailing_slash: bool = True) -> str:
    p = Path(path).expanduser().resolve(strict=False)
    return str(p)
```

```python
# BEFORE (cement/utils/fs.py:107-129, join)
def join(*args: str, **kwargs: Any) -> str:
    paths = list(args)
    first_path = abspath(paths.pop(0))
    return os.path.join(first_path, *paths, **kwargs)

# AFTER
def join(*args: str, **kwargs: Any) -> str:
    paths = list(args)
    first = Path(abspath(paths.pop(0)))
    for p in paths:
        first = first / p
    return str(first)
    # NOTE: kwargs are dropped; verify call sites never pass non-positional
    # args. Original os.path.join accepts only positional. If kwargs need
    # to stay for signature compat, document them as ignored.
```

**[CITED: https://docs.python.org/3/library/pathlib.html — `Path.expanduser()`, `Path.resolve()`, `Path.is_file()`, `Path.is_dir()`, `Path.exists()`, `Path.parent`, `Path.name`, `Path.stem`, `Path.suffix`, `Path / other` join operator]**

**os.path → pathlib equivalents (the 8 idioms used in scoped files):**

| os.path call | pathlib equivalent | Notes |
|--------------|---------------------|-------|
| `os.path.exists(p)` | `Path(p).exists()` | Identical semantics |
| `os.path.isfile(p)` | `Path(p).is_file()` | Identical semantics |
| `os.path.isdir(p)` | `Path(p).is_dir()` | Identical semantics |
| `os.path.join(a, b, c)` | `Path(a) / b / c` | Returns Path; wrap in `str()` for boundary |
| `os.path.basename(p)` | `Path(p).name` | str-typed |
| `os.path.dirname(p)` | `str(Path(p).parent)` | parent is Path; convert |
| `os.path.splitext(p)[0]` / `[1]` | `Path(p).stem` / `Path(p).suffix` | Note: `.suffix` includes the dot; `os.path.splitext` returns the dot too — equivalent |
| `os.path.abspath(p)` | `str(Path(p).resolve())` | Note: `.resolve(strict=False)` is the safer option (doesn't raise FileNotFoundError on missing paths in Python ≥3.10) |
| `os.path.expanduser(p)` | `Path(p).expanduser()` | Identical |

**Caution on `Path.resolve()`:** Python 3.10+ changed `resolve(strict=False)` to be the default behavior — non-existent paths no longer raise; they're resolved as best-effort. This matches `os.path.abspath` semantics. Verified against `cement/utils/fs.py:104` (current `os.path.abspath(os.path.expanduser(path))` is equivalent to `str(Path(path).expanduser().resolve(strict=False))`).

### Anti-Patterns to Avoid

- **DON'T return `Path` from any public function in `cement/utils/fs.py`.** D-12 boundary rule. The 39+ downstream callers (in `cement/core/`, `cement/ext/*`, `cement/cli/`) and unknown subclassing apps all assume `str` returns. A returned `Path` is a public-API break.
- **DON'T touch `cement/core/foundation.py` lines 1359, 1364, 1372, 1377, 1385, 1390, 1478, 1483, 1488, 1492, 1553, 1558, 1563, 1567.** These are template substitution `.format(**template_dict)` calls — see code excerpt below. UP032 won't touch them per ruff issue #9227, but verify per-file diff before each commit.
- **DON'T touch `cement/core/template.py:332, 346, 350`** — these are the legitimate UP032 candidates (`LOG.debug("..." % (a, b))`). Auto-fix will handle them.
- **DON'T add `from __future__ import annotations` to the new `scripts/audit-public-api.py`** — well, actually do, because that script is outside `cement/` and the FA100 sweep doesn't apply. (Confusing-but-fine: cement/ becomes future-import-free, scripts/ is unconstrained.)
- **DON'T forget to update `cement/__init__.py:14` `__all__` list if Phase 03 inadvertently moves a public symbol.** The AST audit will catch this — but be aware.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Public-API surface enumeration | Walk source files with regex looking for `class X` / `def y` | stdlib `ast` (D-02 mandates this) | Regex misses decorator stacks, multi-line defs, class-in-class. AST is the canonical Python parse — guaranteed correct. |
| Per-rule selective ruff fix | Hand-curated diffs from a bulk auto-fix | `ruff check --select UPxxx --fix` per rule | Ruff's per-rule mode is precise. Hand-curating diffs from a bulk fix introduces split-error risk. |
| os.path → pathlib mechanical conversion | Hand-written sed/regex | Hand-write per scoped file (D-13 atomic-per-file) | Each scoped file has different boundary semantics (fs.py public-str-return, template.py template-rendering, config.py file-existence-check). Mechanical regex would break cement/utils/fs.py boundary contract. |
| Locked-vocabulary pragma audit | A test file that imports and asserts comment text | Two-pass `grep -nE` (the D-17 invocation) | The audit is a CI-time text check, not a runtime check. Grep is the right tool. |
| `from __future__ import annotations` removal | Hand-edit 28 files | `ruff --select FA100 --fix` | FA100 detects-and-fixes when `requires-python >= 3.10` (verified via WebSearch — see Pattern 2). Mechanical fix is safe because we hold the python-version target at 3.10. |

**Key insight:** Phase 03 is deliberately tool-driven. D-19 says "ruff-driven only" because the alternative (volunteer modernization) would balloon scope. Hold the line.

## Runtime State Inventory

This phase is a refactor (not a rename or migration), but it touches type-hint syntax across 28 files and could surface stored-state issues. Auditing the 5 categories:

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | None — phase changes source files only, no stored data references type-hint syntax or pragma comments | None |
| Live service config | None — no external services depend on cement source-file syntax | None |
| OS-registered state | None — no Task Scheduler / launchd / systemd registration touches cement | None |
| Secrets/env vars | None — phase doesn't touch env var names or secret keys. The `CEMENT_FRAMEWORK_LOGGING` and `CEMENT_LOG` env vars (referenced in foundation.py:761/774 per CONCERNS.md) are deprecation-tracked, NOT touched in Phase 03 (deferred to Phase 5 DEPREC-01..03). | None |
| Build artifacts | **Possible:** `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`, `coverage-report/`. The annotation-syntax change (UP006/007/045 + FA100) invalidates mypy's cached AST analysis. **Action:** plan should include a `make superclean` (line 73 of Makefile) checkpoint after the FA100 commit lands, before final verification, so verification runs against fresh caches. | `make superclean && make init` between FA100 and final D-24 verification |

**Nothing else found.** Phase 03 is purely source-file modification with one new script (`scripts/audit-public-api.py`) and two new planning artifacts (`03-PUBLIC-API-BASELINE.txt`, `03-VERIFICATION.md`).

## Common Pitfalls

### Pitfall 1: UP032 unexpectedly rewrites a `.format(**dict)` call

**What goes wrong:** UP032 attempts to convert `cement/core/foundation.py:1359` `f.format(**template_dict)` into an f-string and breaks template substitution.

**Why it happens:** Ruff's UP032 logic intends to skip dict-spread, but past versions had bugs (see https://github.com/astral-sh/ruff/issues/9227). Current `~=0.15.12` is verified clean against `**dict` spread but a future bump could regress.

**How to avoid:**
1. After running `ruff check --select UP032 --fix cement/ tests/`, before committing, run:
   ```bash
   git diff cement/core/foundation.py | grep -E '\.format\(' || echo "OK: no .format() lines changed"
   git diff cement/core/template.py | grep -E '\.format\(' || echo "OK: no .format() lines changed"
   ```
2. If any line shows up, abort the commit and add `# noqa: UP032` to that exact line (in a separate `fix(lint): exempt template substitution from UP032` commit FIRST), then re-run the auto-fix.

**Warning signs:** Test failures in `tests/core/test_foundation.py::test_config_*` or `tests/core/test_template.py::test_*` after the UP032 commit lands. Means a `.format(**dict)` was inadvertently rewritten.

### Pitfall 2: FA100 strips `from __future__` and surfaces forward-reference NameError

**What goes wrong:** A type annotation in `cement/core/foundation.py` references `App` before it's defined (or in a class method receiving `app: App` where `App` is the same module being defined). Removing the `from __future__ import annotations` makes Python evaluate the annotation immediately at class-body parse time, producing `NameError: name 'App' is not defined`.

**Why it happens:** The 28 files use `from __future__ import annotations` to defer annotation evaluation. Some annotations may rely on this deferral. Ruff FA100 only adds the future import — FA102 detects when removing it would break things — but the practical risk is in cement/core circular-import edges.

**How to avoid:**
1. **Pre-flight grep:** find every annotation that references a class defined later in the same module:
   ```bash
   for f in cement/core/foundation.py cement/core/handler.py cement/core/interface.py cement/core/extension.py cement/core/controller.py cement/core/plugin.py; do
       echo "=== $f ==="
       grep -nE ': (App|Handler|Interface|Extension|Controller|Plugin)\b|-> (App|Handler|Interface|Extension|Controller|Plugin)\b' "$f"
   done
   ```
2. **Verified TYPE_CHECKING pattern:** All cross-module circular edges (App import in handler.py:20, interface.py:17, extension.py:18, mail.py:13, hook.py:13) are already wrapped in `if TYPE_CHECKING:` blocks. Verified by grep 2026-05-03. These are SAFE — TYPE_CHECKING blocks defer at runtime regardless of whether `from __future__ import annotations` is present.
3. **Same-module forward refs:** if an annotation references a class defined later in the SAME module (e.g., `def foo(self, h: Handler)` where `Handler` is defined further down), a string annotation `"Handler"` may be required. Audit each file with the FA100 commit; mypy will catch most cases via `make comply-mypy` failure.
4. **Run `make comply-mypy` and `make test` IMMEDIATELY after the FA100 commit**, before moving to the next D-22 step.

**Warning signs:** `NameError: name 'X' is not defined` at module import time (caught by `make test` collection phase, not a deep test failure). Or mypy `name-defined` errors.

**[VERIFIED: 2026-05-03 grep] Cross-module circular edges in `cement/core/`:**
- `handler.py:20` — `if TYPE_CHECKING: from ..core.foundation import App` ✓ safe
- `interface.py:17` — `if TYPE_CHECKING: from ..core.foundation import App` ✓ safe
- `extension.py:18` — `if TYPE_CHECKING: from ..core.foundation import App` ✓ safe
- `foundation.py:47` — `if TYPE_CHECKING: from types import FrameType, ModuleType, TracebackType` ✓ safe (stdlib types, no circular concern)
- `mail.py:13`, `hook.py:13` — both `if TYPE_CHECKING: from ..core.foundation import App` ✓ safe

The plan should still mypy-check after FA100 lands — but the analysis above suggests no foundation.py / handler.py / interface.py / etc. forward-ref bugs are masked by `from __future__`. **Confidence: HIGH** (5 critical files verified).

### Pitfall 3: 100% coverage drops below 100% in a refactor commit

**What goes wrong:** Hand-tightening a `Dict[str, Any]` to `Dict[str, str]` accidentally drops a `# pragma: nocover` from a fallback branch, or a pathlib `.is_file()` rewrite changes a tested branch into an untested one.

**Why it happens:** Refactors that look mechanical can subtly change branch shape (e.g., `if os.path.exists(p) and not os.path.isdir(p)` → if-else with pathlib has different branching).

**How to avoid:**
1. Run `pdm run pytest --cov=cement --cov-report=term-missing` after EACH refactor commit (D-22 steps 8-12 are highest-risk). Watch the "Missing" column for the four scoped files.
2. If a line shows up as missing, the refactor changed branch shape; add a test or restructure the refactor to preserve testability.
3. Per Phase 2 D-10/D-11, `--cov-fail-under=100` will hard-fail the commit if coverage drops, which is the safety net.

**Warning signs:** `make test` exits 1 with "Coverage failure: total of 99.XX is less than fail_under=100".

### Pitfall 4: Pragma site count mismatch (123 in CONTEXT.md vs 141 actual)

**What goes wrong:** The plan estimates D-22 step 13 at 123 sites; reality is 141. The pragma sweep takes ~15% longer than estimated.

**Why it happens:** Verified 2026-05-03 with `grep -rn "pragma:\s*no\s*cover" cement/ | wc -l` → **141**. CONTEXT.md (and CONCERNS.md upstream of it) reported 123. The drift is likely from:
- New pragma sites added during Phase 1/2 lint-fix cycles
- The 123 count missing `# pragma: no cover` (with space) variants — there are 31 of those vs 110 of `# pragma: nocover`

**How to avoid:** Plan should re-grep at execution time and use the live count. The locked-vocabulary regex `pragma:\s*no\s*cover` matches both spellings, so the audit pass is correct — only the count estimate is off.

**Warning signs:** Planner's task list says "audit 123 sites" but the executor finds 141.

### Pitfall 5: AST audit script captures something that's NOT meant to be public

**What goes wrong:** The first run of `audit-public-api.py` emits a baseline that includes module-level helper functions or constants that the user actually considers private but didn't underscore-prefix.

**Why it happens:** D-01 says "anything not `_`-prefixed is public." But cement's existing codebase predates this discipline. There may be functions like `cement/core/foundation.py:add_handler_override_options` (verified at line 63) that look public-by-convention but were never intended for external use.

**How to avoid:** First baseline capture (D-22 step 1) is a SNAPSHOT of current reality, not an aspirational filter. If a "private-in-spirit" helper appears, it stays public for 3.0.x — that's the no-breakage rule. Phase 5 deprecations or 3.2.0 cleanup is the place to reclassify.

**Warning signs:** Reviewer or user comments "wait, why is `add_handler_override_options` in the baseline?" — answer: it's there because removing it would be a breaking change downstream. D-01 + the no-breakage rule wins.

### Pitfall 6: macOS BSD grep vs Linux GNU grep escape behavior

**What goes wrong:** The locked-vocabulary regex uses `\s*` (POSIX-extended). BSD grep's `-E` and GNU grep's `-E` both honor `\s` as a non-POSIX extension — but it's not strictly POSIX. On a true POSIX environment (some CI containers), `\s` may not match.

**How to avoid:**
- The user's environment is Linux (`Platform: linux`) per the env block. GNU grep is guaranteed to honor `\s`.
- CI runs Ubuntu (per Phase 2 D-15) — GNU grep. Safe.
- If portability becomes a concern (future macOS dev runs), use `[[:space:]]` instead of `\s`:
  ```bash
  grep -nE 'pragma:[[:space:]]*no[[:space:]]*cover' cement/
  ```
- Recommend the planner uses `[[:space:]]` form in the actual D-17 verification command for maximum portability, even though the user's env is Linux today.

**Warning signs:** Audit grep returns more results than expected on a non-Linux developer machine.

## Code Examples

### Example 1: Compliant Pragma Audit Sweep (D-15..D-18)

```python
# BEFORE (cement/core/cache.py:49)
def get(self, key: str, fallback: Any = None) -> Any:
    pass    # pragma: nocover

# AFTER (locked vocabulary appended)
def get(self, key: str, fallback: Any = None) -> Any:
    pass    # pragma: nocover  # abstract method
```

```python
# BEFORE (cement/core/foundation.py:48)
if TYPE_CHECKING:
    from types import FrameType, ModuleType, TracebackType  # pragma: nocover

# AFTER
if TYPE_CHECKING:
    from types import FrameType, ModuleType, TracebackType  # pragma: nocover  # TYPE_CHECKING import
```

```python
# BEFORE (cement/core/foundation.py:58)
if platform.system() == 'Windows':
    SIGNALS = [signal.SIGTERM, signal.SIGINT]   # pragma: nocover

# AFTER
if platform.system() == 'Windows':
    SIGNALS = [signal.SIGTERM, signal.SIGINT]   # pragma: nocover  # platform-specific
```

```python
# BEFORE (cement/core/foundation.py:123-125 — signal handler)
            continue  # pragma: nocover
        # ...
            continue  # pragma: nocover

# AFTER
            continue  # pragma: nocover  # untestable: signal handler
        # ...
            continue  # pragma: nocover  # untestable: signal handler
```

```python
# BEFORE (cement/utils/fs.py:237 — defensive fallback)
        else:
            break  # pragma: nocover

# AFTER
        else:
            break  # pragma: nocover  # defensive: unreachable
```

```python
# BEFORE (cement/utils/fs.py:245 — env fallback)
else:
    HOME_DIR = abspath('~')  # pragma: nocover

# AFTER
else:
    HOME_DIR = abspath('~')  # pragma: nocover  # platform-specific
```

```python
# BEFORE (cement/core/backend.py:3)
VERSION = (3, 0, 15, 'final', 0)  # pragma: nocover

# AFTER
VERSION = (3, 0, 15, 'final', 0)  # pragma: nocover  # version constant
```

```python
# BEFORE (cement/ext/ext_plugin.py:155 — dynamic import)
                       globals(), locals(), [], 0)  # pragma: nocover

# AFTER
                       globals(), locals(), [], 0)  # pragma: nocover  # untestable: dynamic import
```

```python
# BEFORE (cement/utils/version.py:97 — git subprocess)
# (per CONCERNS.md: shell=True git log)
result = subprocess.check_output(...)  # pragma: nocover

# AFTER
result = subprocess.check_output(...)  # pragma: nocover  # untestable: subprocess
```

### Example 2: Compliant Any-Reduction (D-09)

```python
# BEFORE (cement/core/handler.py:118)
self.__handlers__: Dict[str, dict[str, Type[Handler]]] = {}

# AFTER (already-tight; no change needed)
self.__handlers__: dict[str, dict[str, type[Handler]]] = {}  # PEP 585 (UP006 auto-fix)
```

```python
# BEFORE (cement/core/foundation.py:51)
ArgparseArgumentType = Tuple[List[str], Dict[str, Any]]

# AFTER (UP006/UP007 auto-fix; Any[str] → Any preserved as it's a type alias)
ArgparseArgumentType = tuple[list[str], dict[str, Any]]
# `Any` value type stays — argparse kwargs are runtime-arbitrary;
# tightening would break kwargs-passthrough semantics.
```

```python
# BEFORE (cement/core/foundation.py:808 — argparse parsed_args)
self._parsed_args: Any = None

# AFTER (no change; D-09 explicit exemption)
self._parsed_args: Any = None  # argparse Namespace is opaque per attr access
```

### Example 3: Compliant pathlib Migration in Scoped File

```python
# BEFORE (cement/utils/fs.py:104)
def abspath(path: str, strip_trailing_slash: bool = True) -> str:
    return os.path.abspath(os.path.expanduser(path))

# AFTER (boundary-preserving; D-12 contract held)
def abspath(path: str, strip_trailing_slash: bool = True) -> str:
    p = Path(path).expanduser().resolve(strict=False)
    return str(p)
```

```python
# BEFORE (cement/core/config.py:226)
if os.path.exists(file_path):

# AFTER
if Path(file_path).exists():
```

```python
# BEFORE (cement/core/foundation.py:1317)
if not os.path.isdir(path):
    return []

# AFTER
if not Path(path).is_dir():
    return []
```

```python
# BEFORE (cement/utils/fs.py:182)
parent_dir = os.path.dirname(abspath(path))

# AFTER (parent of abspath, then keep as str via boundary)
parent_dir = str(Path(abspath(path)).parent)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `Optional[X]` / `Union[X, Y]` / `List[X]` / `Dict[K, V]` from typing | `X \| None` / `X \| Y` / `list[X]` / `dict[K, V]` (PEP 604 / PEP 585) | PEP 585 in 3.9 (deferred eval); native in 3.10. PEP 604 in 3.10. | Phase 03 adopts via UP006/UP007/UP045 sweep. CONVENTIONS.md current text becomes stale post-phase. |
| `from __future__ import annotations` for forward refs | Not needed when `requires-python >= 3.10` and TYPE_CHECKING blocks handle circulars | Python 3.10 (PEP 604/585 native); also `typing.TYPE_CHECKING` predates 3.10 | Phase 03 strips from 28 files via FA100. |
| `os.path.exists(p)`, `os.path.join(a, b)`, etc. | `Path(p).exists()`, `Path(a) / b`, etc. | Pathlib added in 3.4; mature in 3.10+ | Phase 03 migrates 4 scoped files. The `cement/cli/` and `cement/ext/*` lag intentionally per D-11. |
| `'%s' % var` / `'{}'.format(var)` | f-strings (`f'{var}'`) | f-strings in 3.6 | Phase 03 adopts via UP032 sweep. **Exception:** `.format(**dict)` template substitution in foundation.py + template.py is NOT a candidate (D-19 protected list). |

**Deprecated/outdated:**
- `from __future__ import annotations` for runtime-deferred annotations — STILL has a use case for `eval`-on-demand annotations (e.g., dataclasses with forward refs) but Phase 03 doesn't trigger that case. The 28-file removal is safe because TYPE_CHECKING blocks already handle the only circular-import edges.
- `typing.Optional` and `typing.Union` are NOT deprecated by PEP 604 — both still work in Python 3.10+ and will likely never be removed (huge backward-compat surface). UP007/UP045 just rewrites them to the modern shorthand. Cement's `cement/__init__.py` re-exports nothing from typing, so downstream apps unaffected.
- `# pragma: no cover` (with space) is equivalent to `# pragma: nocover` (no space). Coverage.py honors both. Cement uses both — the audit sweep should NOT canonicalize forms (would create huge churn) but SHOULD treat both as the same audit subject.

## Pragma site inventory

**Verified 2026-05-03:** `grep -rn "pragma:\s*no\s*cover" cement/ | wc -l` → **141 sites**

**Distribution by directory:**
- `cement/core/` — ~52 sites (mostly abstract methods + TYPE_CHECKING + signal handler)
- `cement/ext/` — ~78 sites (mostly TYPE_CHECKING + dynamic-import + platform-specific)
- `cement/utils/` — ~9 sites (defensive + platform-specific + subprocess)
- `cement/cli/` — ~7 sites (subprocess + dynamic import + signal-related)

**By proposed category (preliminary classification, planner refines):**

| Category | Approx count | Pattern |
|----------|--------------|---------|
| `# abstract method` | ~45 | Interface `pass # pragma: nocover` (cache.py, arg.py, log.py, plugin.py, config.py, output.py, controller.py, mail.py, template.py, handler.py — all interfaces) |
| `# TYPE_CHECKING import` | ~26 | `if TYPE_CHECKING: from ..core.foundation import App` (every ext_*.py + several core/*.py) |
| `# platform-specific` | ~5 | Windows SIGNALS branch (foundation.py:58), HOME_DIR fallback (fs.py:245), NullHandler fallback (ext_logging.py:23-36) |
| `# untestable: dynamic import` | ~3 | ext_plugin.py:155, ext_generate.py:162-165 |
| `# untestable: subprocess` | ~3 | utils/version.py:97-106 git log subprocess, possibly others |
| `# untestable: signal handler` | ~6 | foundation.py:123-125 signal frame walk, related continues |
| `# defensive: unreachable` | ~30+ | else branches that coverage can't prove unreachable (fs.py:237 backup else, ext_argparse.py:822-826 fallback chain, foundation.py:983 signal handler else, ext_smtp.py:189/334/345, ext_watchdog.py:48/171/173, etc.) |
| `# version constant` | ~1 | backend.py:3 VERSION tuple |

**Total accounted for: ~119.** The remaining ~22 will surface during the actual sweep — likely additional defensive/unreachable sites (largest bucket). If any site truly doesn't fit the 8-category vocabulary, D-16 mandates a CONTEXT amendment commit BEFORE adding a new label.

## Any-in-core inventory

**Verified 2026-05-03:** `grep -nE ': Any\b|-> Any\b|Any\]' cement/core/*.py | wc -l` → **40 sites**

CONTEXT.md estimates "~25 today" — actual is 40. Planner should use 40 as baseline.

**Site classification (preliminary):**

**Must-stay (12 sites, exempted by D-09):**
- Every `**kw: Any` / `**kwargs: Any` (handler contract — pluggable kwargs by design): `cache.py:30,52`, `arg.py:33`, `interface.py:35,66`, `mail.py:35`, `hook.py:136`, `extension.py:82`, `meta.py:14,17,30`, `handler.py:65,124,332`, `foundation.py:772,808 (parsed_args),875,1077,1081,1165 (extend, render, last_rendered, add_arg)`, `output.py:30`, `template.py:113`
- `_parsed_args: Any = None` (foundation.py:808) — argparse Namespace opacity
- `frame: Any` in `CaughtSignal.__init__` (exc.py:43) — signal frame is Python-runtime opaque

**Tightenable candidates (~12-15 sites, hand-tighten where narrower type is known):**
- `cache.py:30,52` `value: Any`, `fallback: Any` — likely stays Any (cache values are user-arbitrary)
- `config.py:72,82,111,134` `Dict[str, Any]` returns and `Any` get/set — config values are user-arbitrary; **tightening to `Dict[str, str]` would break apps storing dicts/lists** → stays Any
- `mail.py:102` `config_defaults: Dict[str, Any]` — config defaults ARE Dict[str, Any] by contract
- `handler.py:50` `config_defaults: Optional[Dict[str, Any]] = None` — same
- `foundation.py:51` `ArgparseArgumentType = Tuple[List[str], Dict[str, Any]]` — argparse kwargs opacity, stays
- `foundation.py:135` `frame: Optional[FrameType]) -> Any` — signal handler returns whatever the user's handler returns
- `foundation.py:961` `def run(self) -> Union[None, Any]` — could tighten to `Optional[Any]` but UP045 will rewrite to `None | Any`; may leave for now
- `foundation.py:1146` `Optional[Tuple[Dict[str, Any], Optional[str]]]` — render result; data dict is user-arbitrary
- `foundation.py:1158` `def pargs(self) -> Any` — argparse Namespace
- `template.py:39,54,120,144` `Dict[str, Any]` template data — user-arbitrary
- `output.py:30` `Dict[str, Any]` render data — user-arbitrary

**Realistic Any-reduction count: 5-10 sites** (less than CONTEXT.md "25 → 14" assumption suggests). The bulk of `Any` in cement/core IS load-bearing for the framework's pluggability contract. **D-09 acceptance "post < pre" is achievable but the delta is modest.** Planner should NOT make `Any` reduction the primary phase value — the ruff-driven UP family work and pragma audit are the larger payloffs.

**Confidence:** MEDIUM on the 5-10 site estimate (depends on per-call-site analysis). Recommend the plan include a single `refactor(core): tighten Any types in cement/core/` commit with a targeted hand-pass rather than splitting per-file.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | All work | ✓ | 3.14.3 | — (matrix is 3.10–3.14) |
| PDM | All `pdm run` invocations | ✓ | 2.26.6 | — |
| ruff | UP/FA family auto-fix | ✓ (via `pdm run ruff`, pinned `~=0.15.12`) | 0.15.x | — |
| mypy | comply-mypy gate | ✓ (via `pdm run mypy`, pinned `~=1.20.2`) | 1.20.x | — |
| pytest + pytest-cov + coverage | 100% gate (existing) | ✓ (via `pdm run pytest`, all pinned in dependency-groups) | per pyproject | — |
| stdlib `ast` | Public-API audit script | ✓ | Python 3.10+ | — |
| stdlib `pathlib` | os.path migration | ✓ | Python 3.10+ | — |
| GNU grep / `[[:space:]]` | Locked-vocabulary verification (D-17) | ✓ (Linux env) | system | Use `[[:space:]]` instead of `\s` for POSIX-portable form |
| `diff -u` | `make audit-public-api` exit-status | ✓ | system | — |
| Devbox | `make init` env reset | ✓ | per .devbox | — |

**Missing dependencies with no fallback:** None.

**Missing dependencies with fallback:** None — all required tooling is pre-installed via Phase 1 baseline.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 9.0.3+ + pytest-cov 7.1.0+ + coverage 7.13.5+ |
| Config file | `pyproject.toml` `[tool.pytest.ini_options]` |
| Quick run command | `pdm run pytest --cov=cement.core tests/core` (`make test-core`) |
| Full suite command | `pdm run pytest --cov=cement tests/` (`make test`) — includes 100% coverage gate |

### Phase Requirements → Test Map

The acceptance for Phase 03 is mostly mechanical (grep + ruff + mypy + audit-script + coverage gate). Each D-24 conjunct maps to an automated command:

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REFACTOR-01 (via D-20) | Dead code removed (acceptance via 100% coverage gate) | unit + integration | `pdm run pytest --cov=cement --cov-fail-under=100 tests/` | ✅ existing |
| REFACTOR-02 (via D-09) | Any count strictly lower post-phase | grep | `grep -nE ': Any\b\|-> Any\b\|Any\]' cement/core/*.py \| wc -l` (compare pre/post in 03-VERIFICATION.md) | ✅ Wave 0 captures pre-count |
| REFACTOR-03 (via D-14) | os.path migrated in scoped files; survivors tagged `# boundary: str` | grep | `grep -rn 'os\.path' cement/utils/fs.py cement/core/ \| grep -vE '# boundary:'` returns empty | ✅ existing |
| REFACTOR-04 (via D-19) | UP032 lint-clean (no surviving printf-style format) | ruff | `pdm run ruff check --select UP032 cement/ tests/` | ✅ existing |
| COV-01 | 100% coverage on `make test` | pytest-cov | `pdm run pytest --cov=cement --cov-fail-under=100 tests/` | ✅ existing |
| COV-02 | HTML coverage report generates without warning | pytest-cov | `pdm run pytest && test -f coverage-report/index.html` | ✅ existing |
| COV-03 (via D-17) | Locked-vocabulary regex returns empty | grep | `grep -nE 'pragma:[[:space:]]*no[[:space:]]*cover' cement/ \| grep -vE '# (abstract method\|TYPE_CHECKING import\|platform-specific\|untestable: dynamic import\|untestable: subprocess\|untestable: signal handler\|defensive: unreachable\|version constant)'` returns empty | ✅ existing |
| D-04 (audit gate) | AST audit baseline matches post-refactor | shell | `make audit-public-api` exits 0 | ✅ Wave 0 captures baseline |
| D-08 (FA100) | No surviving `from __future__ import annotations` | grep | `grep -rn 'from __future__ import annotations' cement/` returns empty | ✅ existing |
| D-06 (UP/FA enabled) | Ruff config has UP + FA in extend-select | ruff | `pdm run ruff check cement/ tests/` exits 0 with UP+FA in select | ✅ existing |
| D-22 commit hygiene | Commits follow Conventional Commits + 78-char wrap | manual | `git log --pretty=format:'%s' main..HEAD` review | ✅ manual |

### Sampling Rate

- **Per task commit:** `make comply` (ruff + mypy) — ~10s
- **Per logical wave (e.g., after each UP-family commit lands):** `make test` — ~30s including 100% gate
- **Per phase-level checkpoint (e.g., after FA100 lands, after pathlib migration completes):** `make superclean && make init && make test && make comply` — full reset to verify against fresh caches
- **Phase gate:** Full D-24 9-conjunct verification (each command in 03-VERIFICATION.md), plus `/gsd-verify-work`

### Wave 0 Gaps

- [ ] `scripts/audit-public-api.py` — does not exist; D-22 step 1 creates it
- [ ] `.planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt` — does not exist; D-22 step 1 creates it
- [ ] `.planning/phases/03-internal-refactor-coverage-hardening/03-VERIFICATION.md` — does not exist; D-22 step 14 creates it
- [ ] `Makefile` `audit-public-api` target — does not exist; D-22 step 1 adds it
- [ ] `pyproject.toml` `[tool.ruff.lint] extend-select` UP + FA additions — does not exist; D-22 step 2 adds them
- [ ] No new test infrastructure needed — existing test suite covers all phase requirements via the 100% coverage gate

*(Wave 0 is light because Phase 03 is a refactor; no new behavior tests required. The added test surface IS the audit script + Makefile target + verification artifacts.)*

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | UP032 in ruff `~=0.15.12` correctly preserves `.format(**dict)` calls (ignores them) | Pitfall 1 | If wrong, foundation.py:1359..1567 + template.py:359+ template substitution breaks. **Mitigation:** per-file diff review before UP032 commit. **Verified via WebSearch (HIGH confidence) but per-file diff is mandatory belt-and-braces.** |
| A2 | All circular-import edges in `cement/core/` are TYPE_CHECKING-wrapped → FA100 strip is safe | Pitfall 2 | If wrong, `make test` fails at collection time. **Verified for 5 critical files (HIGH confidence)** but full mypy run after FA100 commit is still required. |
| A3 | Any-reduction realistic delta is 5-10 sites (NOT the "25 → 14" CONTEXT estimate) | Any-in-core inventory | If wrong, planner under-estimates Any-tightening work. **Mitigation:** plan as a single commit with timebox; if blast radius is bigger, split per file. |
| A4 | Pragma audit blast radius is 141 sites (not 123) | Pragma site inventory | If wrong (more sites added between research and execution), the pragma sweep takes longer. Single grep pre-execution closes this. |
| A5 | The CONVENTIONS.md update can land here without colliding with Phase 5 DOCS-04 | Out-of-scope note in CONTEXT canonical_refs | If wrong, Phase 5 has nothing to update for type-annotation conventions. **Recommendation: land it here as a small `docs(codebase):` commit** between UP045 and FA100; Phase 5 DOCS-04 still has plenty of work for docstring review. |
| A6 | The audit script's per-class member walk correctly handles all decorator stacks (@property, @classmethod, @staticmethod, @dataclass, @expose) | Pattern 1 | If a public symbol is missed, the baseline is incomplete and a future refactor could silently remove it. **Mitigation:** sanity-check first baseline against `cement/__init__.py` `__all__` (which lists 14 known top-level public symbols) — they should all appear. |
| A7 | `Path(p).resolve(strict=False)` is semantically equivalent to `os.path.abspath(os.path.expanduser(p))` | Code Examples Example 3 | Edge case: symlink resolution. `os.path.abspath` does NOT resolve symlinks; `Path.resolve()` DOES. If cement code relies on un-resolved abspath behavior (i.e., wants to keep symlinks), the migration changes semantics. **Mitigation:** use `Path(p).expanduser().absolute()` instead of `.resolve()` if symlink preservation matters. **Verify against cement test suite — if any test uses symlinks, audit the migration target.** |

**A7 is the highest-risk assumption.** Recommend the plan include a `find tests/ -type l` check (find symlinks in test fixtures) before the fs.py migration commit, and if any are found, choose `.absolute()` over `.resolve()` to preserve original semantics.

## Open Questions

1. **CONVENTIONS.md timing — Phase 03 here or Phase 5 DOCS-04?**
   - What we know: D-23 / step 5 in the suggested commit sequence opens the door for `docs(codebase): refresh CONVENTIONS to PEP 604/585 syntax` to land here.
   - What's unclear: whether the user prefers a single docs sweep in Phase 5 vs. landing this in Phase 03 to keep the source-of-truth doc accurate moment-to-moment.
   - Recommendation: **land it here** as a small commit between UP045 and FA100. Avoids a stale doc for the entire interval between Phase 03 and Phase 5. Planner should add it as D-22 step ~6.5.

2. **Per-file split for D-22 step 8 (Any tightening) and step 13 (pragma audit)?**
   - What we know: D-22 explicitly leaves this to planner discretion.
   - What's unclear: blast radius of each. Any-tightening has a realistic delta of 5-10 sites → single commit OK. Pragma audit has 141 sites across ~30 files → per-file commits would mean ~30 commits.
   - Recommendation: **single commit for Any** (≤10 sites is bisect-friendly as one unit). **Per-file commits for pragma audit** (~30 files × atomic-per-file matches Phase 1 D-04 family-split shape; bisect anchor per file is the precedent). Planner picks final shape.

3. **Should `make audit-public-api` use `[[:space:]]` instead of `\s` for cross-platform safety even though current env is Linux?**
   - What we know: User env is Linux (verified). CI is Ubuntu (Phase 2 D-15 confirmed). GNU grep handles `\s`.
   - What's unclear: whether macOS dev (a common contributor environment for OSS Python projects) would hit BSD grep behavior.
   - Recommendation: use `[[:space:]]` form in D-17 verification command. Costs nothing, gains portability. Planner picks; safe default is `[[:space:]]`.

4. **Should the audit script's first invocation include a "what's currently in `__all__` that ISN'T in the baseline" sanity check?**
   - What we know: `cement/__init__.py` has 14-entry `__all__` (verified 2026-05-03). The AST walker collects everything `__all__` lists by walking module-level symbols.
   - What's unclear: whether re-export-only symbols (e.g., `Controller = ArgparseController`) get captured in `cement.__init__:Controller` correctly.
   - Recommendation: planner adds a one-time sanity check after first baseline capture: `grep -c "^cement.__init__:" 03-PUBLIC-API-BASELINE.txt` should return ≥14. If not, the AST script needs adjustment for re-export aliases.

## Sources

### Primary (HIGH confidence)
- [Python ast module docs (3.10+)](https://docs.python.org/3/library/ast.html) — AST walker pattern (Pattern 1)
- [Python pathlib docs](https://docs.python.org/3/library/pathlib.html) — Path method equivalents (Pattern 3, Code Examples)
- [Ruff UP family docs](https://docs.astral.sh/ruff/rules/#pyupgrade-up) — UP006/UP007/UP032/UP045 rule semantics
- [Ruff FA family docs (FA100, FA102)](https://docs.astral.sh/ruff/rules/future-rewritable-type-annotation/) — `from __future__ import annotations` mechanical detection
- [PEP 585 (builtin generic types)](https://peps.python.org/pep-0585/)
- [PEP 604 (X \| Y union syntax)](https://peps.python.org/pep-0604/)
- Local codebase verification (2026-05-03):
  - `pyproject.toml` (Python 3.10+, ruff 0.15.12, mypy 1.20.2, coverage 7.13.5+)
  - `grep` verifications: 141 pragma sites, 40 Any sites in cement/core/, 28 files with `from __future__`, 5 verified TYPE_CHECKING circular guards in cement/core/

### Secondary (MEDIUM confidence)
- [Ruff GitHub issue #9227 (UP032 dict-spread fixer behavior)](https://github.com/astral-sh/ruff/issues/9227) — confirms UP032 doesn't auto-rewrite `.format(**dict)` (Pitfall 1)
- [Ruff GitHub issue #11332 (UP032 vs str.format)](https://github.com/astral-sh/ruff/issues/11332)
- [pathlib migration patterns (Real Python)](https://realpython.com/python-pathlib/) — confirms `Path.exists/is_file/is_dir/expanduser` semantics
- [Migrating from os.path to pathlib (Amitness)](https://amitness.com/2019/12/migrating-to-pathlib/) — confirms equivalents table

### Tertiary (LOW confidence)
- None — all critical claims cross-verified.

## Metadata

**Confidence breakdown:**
- Standard stack: **HIGH** — ruff/mypy/pytest pinned via Phase 1; ast/pathlib are stdlib; no new tools.
- Architecture (no runtime change): **HIGH** — phase is refactor-only; no tier reassignment.
- Pitfalls: **HIGH** — Pitfalls 1 (UP032 dict-spread) and 2 (FA100 forward refs) verified via WebSearch + local codebase grep. Pitfall 3 (coverage drop) verified via Phase 2 D-10/D-11 wiring.
- AST audit script (Pattern 1): **HIGH** — canonical stdlib pattern, verified per-class member edge cases against cement codebase.
- Pathlib equivalents (Pattern 3): **HIGH** — official docs + multiple secondary sources agree on every entry.
- Any-reduction estimate: **MEDIUM** — site classification is per-call-site judgment; planner should refine during execution.
- Pragma site count (141 vs CONTEXT's 123): **HIGH** — direct grep verified 2026-05-03.

**Research date:** 2026-05-03
**Valid until:** 2026-06-03 (30 days for stable refactor scope; ruff/mypy version pins lock the tooling layer)
