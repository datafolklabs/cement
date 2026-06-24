---
quick_id: 260624-fme
slug: apply-coderabbit-follow-ups-on-pr-783
date: 2026-06-24
status: ready
---

# Quick Task 260624-fme: Apply CodeRabbit follow-ups on PR #783

## Goal

Act on the 4 valid findings from CodeRabbit's review of PR #783
(`feat/generate-features-redesign-pr`). Three findings are deliberately
dismissed as noise (see Out of Scope). Each change is committed atomically.

All work stays on the current branch `feat/generate-features-redesign-pr`.
Quality gates (`make comply`, targeted pytest) must stay green.

## Tasks

### Task 1 — `_gated_default`: reject requires-gated-out var with no default
File: `cement/ext/ext_generate.py` (~lines 330-338)

When `requires:` gates a variable out and the variable declares no `default`,
`_gated_default` currently returns `str(None)` → the literal string `"None"`
lands in the template context (and the choice path skips its required-default
validation). Add a fail-fast guard at the top of `_gated_default`:

- If `var['default'] is None`: raise `ValueError` —
  `f"Variable '{var['name']}' uses requires: but has no default"`.
- Keep boolean branch (`bool(default)`) and string/choice branch
  (`str(default)`) unchanged otherwise.

This survives `python -O` (ValueError, not assert), matching the D-17 guard
style already in the file.

### Task 2 — cycle detection in `resolve_and_emit`
File: `cement/ext/ext_generate.py` (~lines 377-412)

`A requires B` + `B requires A` recurses to `RecursionError` because
memoization only happens after a var fully resolves (`data[name]` set at the
end). Add an in-flight guard:

- Introduce a `resolving: set[str]` in the enclosing scope (alongside the
  other resolver-local state).
- At the start of `resolve_and_emit`, after the `data` membership memo-check:
  if `var['name'] in resolving`, raise `ValueError` —
  `f"Cyclic variable dependency detected for '{var['name']}'"`.
- Add the name to `resolving` before resolving prerequisites/prompting, and
  remove it in a `finally` so the happy path is unaffected. Ensure the early
  `return` on the gated-out path still clears `resolving`.

### Task 3 — make `test_generate_boolean_silent` catch stringification
Files: `tests/data/templates/generate/test33/.generate.yml`,
`tests/ext/test_ext_generate.py` (~lines 365-374)

Current fixture uses `default: true`, so a regressed impl emitting the string
`'True'` (truthy) still renders `flag-on` and the test passes — it cannot
detect the typed-output contract breaking.

- Flip the test33 fixture `default: true` → `default: false`.
- Update the test to assert `'flag-off'` is rendered (real `False` → else
  branch). A regressed `'False'` string is truthy → would render `flag-on` →
  test fails. Update the test comment accordingly.

### Task 4 — README cleanups (`demo/generate-features/README.md`)
- MD028: remove the blank line at ~160 inside the blockquote so the
  bool-token note and the `{{ bool }}` gotcha are separate blocks correctly
  (merge into one blockquote OR keep two blocks with no stray blank quoted
  line — simplest: drop line 160's blank, letting the two `>` paragraphs be
  one block, or add a non-quoted separator). Resolve the MD028 warning.
- MD053: delete the unused `[779]:` link reference definition (line 272).
  Verify no remaining `[779]` usage in the doc first.

## Out of Scope (dismissed CodeRabbit findings — do NOT change)
- Regex `extend.when` for string vars (ext_generate.py:324): by design,
  mirrors existing `validate:` semantics; documented in code comments.
- Test type annotations (test_ext_generate.py): `tests/` is excluded from
  mypy (pyproject.toml `files`/`exclude`); all existing tests are unannotated.
- All 6 CHANGELOG "consolidate to single line" findings: contradict the
  file's own established wrap-at-78 multi-line entry style.

## Verification
- `pdm run pytest tests/ext/test_ext_generate.py` — all green, including the
  strengthened silent-bool test.
- `make comply-ruff` and `make comply-mypy` — clean.
- (Full `make test` needs Redis+memcached; targeted ext-generate run is
  sufficient for these changes.)
