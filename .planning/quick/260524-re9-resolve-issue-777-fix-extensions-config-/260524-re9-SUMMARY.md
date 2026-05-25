---
quick_id: 260524-re9
description: Fix extensions config-override to honor Meta.config_section (#777)
status: complete
created: 2026-05-25
commit: f8a62e98
issue: https://github.com/datafolklabs/cement/issues/777
related_pr: https://github.com/datafolklabs/cement/pull/760
---

# Quick Task 260524-re9: Summary

## What was done

Mirrored the `template_dirs` fix from PR #760 onto the parallel
`extensions` config-override block in `cement/core/foundation.py`. The
block guarded against `self._meta.config_section` but read/wrote via
`label`, silently dropping extensions defined in a customized
`Meta.config_section` (a hidden divergence when `config_section != label`).

## Changes

- `cement/core/foundation.py` (2 lines, inside `_setup_config_handler`):
  - L1491: `self.config.get(label, ...)` → `self.config.get(self._meta.config_section, ...)`
  - L1501-1503: `self.config.set(label, ...)` → `self.config.set(self._meta.config_section, ...)` (wrapped for ≤100 col)
- `tests/core/test_foundation.py`:
  - Added `test_load_extensions_via_config_with_custom_config_section` —
    exercises both input shapes (comma-separated string and list) at a
    section name distinct from `Meta.label`.
- `CHANGELOG.md`:
  - Added `[core.foundation]` entry under `## 3.0.15 - DEVELOPMENT` → Bugs.

## Verification

- `make comply` → green (ruff + mypy)
- `pdm run pytest tests/core/test_foundation.py -k extensions_via_config` →
  2/2 passed (existing + new regression test)
- `pdm run pytest --cov=cement.core tests/core` → 348/348 passed
  (5 unrelated memcached failures from absent local service — pre-existing,
  not introduced by this change)
- Regression test confirmed load-bearing: temporarily stashing the
  foundation.py fix made the new test fail with
  `NoSectionError`/missing-extensions assertion before the fix and pass
  after, proving it would have caught the bug.
- No BC change for the common `Meta.config_section is None` path
  (config_section falls back to label at L1370-1371; existing
  `test_load_extensions_via_config` and `test_core_meta_override`
  continue to pass unchanged).

## Commit

`f8a62e98` — `fix(core.foundation): honor Meta.config_section for extensions (#777)`

## Follow-ups

- Move
  `.planning/todos/pending/2026-05-08-resolve-issue-777-extensions-config-section.md`
  to `completed/` (handled by the orchestrator commit below).
- Close GitHub issue #777 on next sync.
