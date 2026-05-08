---
id: 260507-to4
status: complete
type: quick
title: Rewrite PR #760 — template_dirs config override via core_meta_override
date: 2026-05-08
branch: feat/support-template-dirs-meta-override
commit: c25562d5
resolves: "#746"
---

# Quick Task 260507-to4: Summary

## What Shipped

A 113-line, single-commit rewrite of PR #760 on the existing
`feat/support-template-dirs-meta-override` branch. The branch was reset to
`origin/main` (`4d62b88a`) and rebuilt from scratch; the original buggy
commit `0cf3873c` is no longer in branch history.

**Commit:** `c25562d5 feat(core.foundation): support config override of Meta.template_dirs`

### Changes

| File | Change |
|---|---|
| `cement/core/foundation.py` | +25 lines — added `'template_dirs'` to `Meta.core_meta_override`; added a 14-line str→list conversion block immediately after the generic override loop (parallel to the existing `extensions` block); expanded the `Meta.template_dirs` docstring with config-override notes. **`_setup_template_handler` is byte-identical to `main`.** |
| `tests/core/test_foundation.py` | +82 lines — 4 new tests: list override, str→list conversion, `{label}`/`{home_dir}` substitution, full precedence chain. |
| `CHANGELOG.md` | +6 lines — Features bucket under `## 3.0.15 - DEVELOPMENT` with correct `#746` issue link. |
| `CONTRIBUTORS.md` | +1 line — Tom Freudenberg (issue reporter). |

### Verification

- `make test`: **324 passed**, 100% coverage (3249/3249 statements covered).
- `make comply`: ruff clean, mypy clean (51 source files).
- `_setup_template_handler` byte-equality with `main`: confirmed via
  `git diff origin/main -- cement/core/foundation.py` (only 3 hunks, all
  outside the function body).

## Why This Differs From the Original PR

The original PR hand-rolled custom logic inside `_setup_template_handler`,
which:

1. **BC-broke the precedence chain** — moved `core_user_template_dirs`
   ahead of `template_dir`, breaking downstream apps that ship a default
   `template_dir`.
2. **Skipped `.format(**template_dict)`** on config-supplied dirs —
   `{label}` / `{home_dir}` substitution silently failed.
3. **Skipped the `not in template_dirs` dedup check** for config-supplied
   dirs.
4. **Diverged precedence semantics** between Meta and config (config
   first-listed = highest; Meta first-listed = lowest).

Codebase research surfaced the canonical pattern: `Meta.core_meta_override`
is the generic config→Meta override hook (used by `plugin_dir`,
`template_dir`, `debug`, etc.). Routing `template_dirs` through the same
mechanism and adding only the str→list parsing collapses the new code from
~25 lines of branching logic in `_setup_template_handler` to a 14-line
parsing block alongside the existing `extensions` handling — and inherits
the existing precedence chain, substitution, and dedup for free.

## Decisions Locked In

- **Replace, not extend.** Config `template_dirs` replaces
  `Meta.template_dirs` entirely (matches `template_dir`, `plugin_dir`,
  every other config-overridable Meta attr).
- **No precedence divergence.** Config-supplied dirs flow through the same
  `_setup_template_handler` as Meta-supplied — they sit in the
  `template_dirs` precedence slot, with first-listed = lowest precedence
  (consistent with the existing `Meta.template_dirs` semantics).

## Local State (Pre-Push)

- Branch: `feat/support-template-dirs-meta-override` (1 commit ahead of
  `origin/main`, 263 commits ahead of `origin/feat/support-template-dirs-meta-override`).
- Force-push **not yet performed** — awaiting user review per task
  constraints.
- After review: `git push --force-with-lease origin feat/support-template-dirs-meta-override`
  will update PR #760 with the rewrite.

## Next Action

User reviews the local diff (`git diff origin/main..HEAD -- '*.py' '*.md'`)
and the new commit, then triggers force-push.
