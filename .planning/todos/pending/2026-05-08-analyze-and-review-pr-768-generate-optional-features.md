---
created: 2026-05-08T18:32:34.201Z
title: Analyze and review GitHub PR #768
area: ext.generate
files:
  - cement/ext/ext_generate.py
  - cement/cli/templates/generate/
---

## Problem

PR #768 (`feat(ext.generate): add optional features support for templates`) is
an open self-authored PR by @derks (head: `feat/generate-optional-features`,
base: `main`). It adds feature-driven template generation to `ext_generate`:
optional features in `.generate.yml` with conditional variables, `exclude`
and `ignore` patterns, and dependency resolution via `requires` with
transitive cascading. Also includes a fix to `setup_template_items` to catch
`ImportError` and a default-value correction (`{}` → `[]`). Resolves issue
#743.

Scope is non-trivial: 45 changed files, +615 / −10. PR was opened
2026-03-09 and has been sitting since — needs a fresh look to decide:

- Does the current branch still apply cleanly to `main` and pass CI on the
  full Python matrix?
- Is the design still right for Cement 3.0.x backward-compatibility
  constraints (no public-API breakage, no new core deps)?
- Are the new YAML schema additions (`features`, `requires`, `exclude`,
  `ignore`) covered by tests at 100% and documented?
- Is the implementation salvageable with targeted updates, or has the
  surrounding `ext_generate` code drifted enough that a rewrite on a fresh
  branch is cheaper?

## Solution

TBD — investigation task. Suggested approach:

1. `gh pr checkout 768 -R datafolklabs/cement` and rebase on current `main`;
   note conflict surface area.
2. Run `make test` and `make comply` against the rebased branch; capture
   failures.
3. Read the diff against current `cement/ext/ext_generate.py` and the
   `cement/cli/templates/generate/` tree to spot drift.
4. Cross-check against issue #743 to confirm the PR still satisfies the
   original ask.
5. Produce an LOE estimate with two options: (a) update-in-place patch list,
   (b) rewrite scope. Recommend one with rationale.
6. If updating: route through `/gsd-quick` or a planned phase depending on
   size. If rewriting: capture as a phase candidate and close #768 with a
   pointer.
