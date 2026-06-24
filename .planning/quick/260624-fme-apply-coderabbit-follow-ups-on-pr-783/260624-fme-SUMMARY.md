---
quick_id: 260624-fme
slug: apply-coderabbit-follow-ups-on-pr-783
date: 2026-06-24
status: complete
---

# Quick Task 260624-fme — Summary

Acted on the 4 valid findings from CodeRabbit's review of PR #783 (the #782
typed-variables redesign); dismissed 3 as noise. Landed on the work branch
`feat/generate-features-redesign` as two code commits, kept separate from
this GSD planning/execution doc.

## Commits (on feat/generate-features-redesign)
- `ee0a4ccb` fix(ext.generate): harden requires gating and add cycle guard
- `29e41bc9` docs(demo): fix MD028 blockquote and drop unused #779 ref

(These were first prototyped as five commits on the disposable code-only
`-pr` branch, then consolidated to two clean commits here.)

## What changed
- `_gated_default` now fail-fasts (ValueError) when a `requires:`-gated-out
  variable has no `default`, instead of leaking the string `"None"`.
- `resolve_and_emit` gained an in-flight `resolving` set → cyclic `requires:`
  raises a clear ValueError instead of recursing to RecursionError.
- `test_generate_boolean_silent` fixture flipped to `default: false` so a
  stringified bool (`'False'` is truthy) now fails the test.
- Added test43 (gated-no-default) and test44 (requires cycle) fixtures +
  tests to cover the two new guards — restores 100% coverage.
- README: MD028 blockquote blank line fixed; unused `[779]` ref removed.

## Dismissed (with reasons, posted to PR #783)
- Regex `extend.when` for strings — by design, mirrors `validate:`.
- Test type annotations — `tests/` is mypy-excluded; matches existing style.
- 6× CHANGELOG "single line" findings — contradict the file's own wrap-at-78
  multi-line entry convention.

## Gates
- `SMTP_HOST=localhost make test` → 372 passed, 100.00% coverage.
- `make comply` → ruff clean, mypy clean (51 files).
- Redis(6379) + memcached(11211) + Mailpit(1025/8025, TLS via
  docker/mailpit dev certs) started locally for the full run.
