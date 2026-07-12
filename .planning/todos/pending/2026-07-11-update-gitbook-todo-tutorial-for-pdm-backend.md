---
created: 2026-07-11T00:00:00.000Z
title: Update GitBook todo-tutorial walkthrough for pdm-backend packaging
area: docs
files:
  - cement/cli/templates/generate/todo-tutorial/
issue: 735
blocked_by: Phase 05.3 todo-tutorial pdm-backend migration
---

## Problem

Phase 05.3 migrates the `todo-tutorial` generate template from setup.py-era
packaging (`setup.py` + `setup.cfg` + `requirements*.txt` + `MANIFEST.in`) to a
`pdm-backend` + `[project]`-table `pyproject.toml` (decisions D-02/D-03).

The external GitBook tutorial at https://docs.builtoncement.com walks the reader
through the OLD setup.py-based flow. After the template migrates, that narrative
is desynced — the generated files no longer match the tutorial steps.

Per the project convention, Sphinx is API-reference only; narrative/tutorial docs
live in GitBook (outside this repo), so this cannot be fully closed from the
cement repo and is deferred out of Phase 05.3.

## Solution

Once Phase 05.3 lands the pdm-backend `todo-tutorial` template:

1. Update the GitBook tutorial to reflect the new packaging:
   - Replace `setup.py`/`requirements.txt` steps with the `pyproject.toml`
     (`[project]` table, `[dependency-groups]`, `pdm-backend`) flow.
   - Update install/build steps (`pip install .` still works; drop
     `requirements*.txt` install instructions).
2. Verify the walkthrough end-to-end against a freshly generated
   `cement generate todo-tutorial` output.
3. Cross-link the tutorial from any CHANGELOG 3.0.16 entry that mentions the
   template modernization.
4. Confirm the in-template README/CHANGELOG packaging note (shipped in Phase 05.3)
   points readers at the updated tutorial.
