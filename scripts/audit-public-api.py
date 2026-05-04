#!/usr/bin/env python3
"""
audit-public-api.py — emit sorted public-API surface for cement/.

Walks the AST of every module under cement/, prints one
'<dotted.module>:<NAME>' or '<dotted.module>:<ClassName>.<member>' line
per non-underscore module-level symbol or class member.

Sort + diff against 03-PUBLIC-API-BASELINE.txt to detect any public-API
drift. See Phase 03 D-01..D-05.

Phase 03 contract anchors:

* D-01 — Public surface = anything not ``_``-prefixed across
  ``cement/__init__.py``, ``cement/core/*``, ``cement/ext/*``,
  ``cement/utils/*``, ``cement/cli/*``. Includes ``App.Meta.<attr>`` names
  that subclasses set (``config_defaults``, ``extensions``, ``handlers``,
  ``meta_override``, ``core_interfaces``, etc.), interface abstract
  methods, handler public methods, exception classes.
* D-02 — Stdlib ``ast`` only. NO new dev dependency. Walks every ``.py``
  module under ``cement/`` and dumps non-underscore module-level names,
  class names, class public attributes, and class public method names
  to stdout (sorted).
* D-03 — Wired into ``make audit-public-api`` as a STANDALONE target
  (NOT chained into ``make test`` or ``make comply``).
* D-04 — Baseline snapshot lives at
  ``.planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt``.
  Captured BEFORE any refactor commit lands.
* D-05 — Script + Makefile target are PERMANENT dev affordances post
  Phase 03; future 3.0.x patches and Phase 5 deprecations reuse them as
  a regression check (mirrors ``scripts/cli-smoke-test.sh``).

Output format:

    cement.core.foundation:App
    cement.core.foundation:App.Meta
    cement.core.foundation:App.Meta.argument_handler
    ...

One line per public symbol, sorted, deduplicated.

Excluded paths (matches ``[tool.coverage.run] omit`` per Phase 2 D-12):

* ``cement/cli/templates/``
* ``cement/cli/contrib/``

Exit codes:

* ``0`` — surface enumerated successfully
* ``2`` — a source file failed to parse (SyntaxError); path printed to stderr
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
        # Re-exports — `from X import Y` and `from X import Y as Z` at module
        # level introduce `Y` (or `Z`) into the importing module's public
        # surface. The canonical case is `cement/__init__.py` re-exporting
        # `App`, `TestApp`, `Controller` (= ArgparseController), `ex`, etc.
        # — these are the 14 entries listed in `__all__` and they ARE part
        # of the public surface that downstream code imports as
        # `from cement import App`. Per Phase 03 D-01.
        elif isinstance(node, ast.ImportFrom):
            # `from __future__ import annotations` (and similar future-flag
            # imports) bind the name `annotations` in the module namespace
            # but it's not a public symbol — it's a compiler directive. Per
            # Phase 03 D-08 these come due for removal anyway; meanwhile we
            # MUST NOT enumerate them as public surface or every module that
            # carries the future import would emit `<mod>:annotations`.
            if node.module == '__future__':
                continue
            for alias in node.names:
                # `from X import *` has alias.name == '*' — skip (no name to
                # enumerate; the canonical case is wildcard re-exports which
                # cement/ does not use).
                if alias.name == '*':
                    continue
                exposed = alias.asname if alias.asname is not None else alias.name
                if is_public(exposed):
                    out.append(f"{mod_name}:{exposed}")
        elif isinstance(node, ast.Import):
            # `import X` and `import X as Y` at module level — the bound name
            # is `X` (or `Y`). Only the bound name lands in the importing
            # module namespace; we emit it if public.
            for alias in node.names:
                # `import a.b.c` binds `a` (the top-level package); `import
                # a.b.c as d` binds `d`. Match Python's import semantics.
                if alias.asname is not None:
                    bound = alias.asname
                else:
                    bound = alias.name.split('.', 1)[0]
                if is_public(bound):
                    out.append(f"{mod_name}:{bound}")
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
    # `__init__.py` files name the package, not a submodule. Drop the
    # trailing `__init__` so `cement/__init__.py` -> `cement` (NOT
    # `cement.__init__`). Matches Python's import semantics: `from cement
    # import App` reads from `cement/__init__.py`, exposed as the
    # `cement` namespace.
    if parts and parts[-1] == '__init__':
        parts = parts[:-1]
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
            tree = ast.parse(py.read_text(encoding='utf-8'))
        except SyntaxError as e:
            print(f"SYNTAX ERROR in {py}: {e}", file=sys.stderr)
            return 2
        symbols.extend(collect_module_symbols(tree, mod_name))
    for line in sorted(set(symbols)):
        print(line)
    return 0


if __name__ == '__main__':
    sys.exit(main())
