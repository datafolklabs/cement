---
phase: 01-tooling-baseline-python-matrix
plan: 01
subsystem: infra
tags: [python-matrix, ci, docker, pyproject, eol, tooling-baseline]

# Dependency graph
requires: []
provides:
  - "Python 3.10 floor across pyproject.toml, ruff target-version, mypy python_version"
  - "GitHub Actions test-all matrix on 3.10..3.14 + pypy3.10 (no 3.9)"
  - "docker-compose service set without cement-py39"
  - "Generate-template Dockerfiles bumped to python:3.10-alpine"
  - "Atomic D-05 commit (single chore: drop python 3.9 from supported matrix)"
  - "Closure of PYVER-01, PYVER-02, PYVER-03"
  - "Removal of dead .travis.yml CI definition"
affects:
  - "01-02 (ruff bump) — can target py310 floor"
  - "01-03 (mypy bump) — can target python_version 3.10 floor"
  - "01-04 (pytest+pytest-cov+coverage bumps) — can target py310 floor"
  - "Phase 2 PDM auto-update pipeline — now resolves against >=3.10"

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Atomic-commit-per-concern (D-05): all 9 traces of a single supported-version drop land in ONE conventional commit"
    - "Conventional Commits with 78-char wrap (CLAUDE.md) verified via `git log -1 --format=%b | awk 'length>78'` (returns nothing)"

key-files:
  created: []
  modified:
    - "pyproject.toml — requires-python, ruff target-version, mypy python_version -> 3.10"
    - ".github/workflows/build_and_test.yml — test-all matrix drops 3.9"
    - "Makefile — dev target drops cement-py39 line"
    - "docker-compose.yml — cement-py39 service block removed"
    - "cement/cli/templates/generate/todo-tutorial/Dockerfile — FROM python:3.10-alpine"
    - "cement/cli/templates/generate/project/Dockerfile — FROM python:3.10-alpine"
    - "README.md — prose + cement-py39 examples updated to py310"
  deleted:
    - "docker/Dockerfile.dev-py39"
    - ".travis.yml (dead CI infrastructure; GitHub Actions is the active CI)"

key-decisions:
  - "D-05 atomic-commit pattern proven: 9 file changes (7 modifications + 2 deletions) land in one commit and the verification grep returns empty without needing follow-up clean-up commits."
  - "Travis configuration deleted rather than partially edited (RESEARCH.md Pitfall 7 + Open Question 2): keeping a non-active CI definition for a project on GitHub Actions is dead infrastructure and a future-grep liability."
  - "D-13/D-14 strict-minimum honored: cement/utils/fs.py `from __future__ import annotations` and the self-flagged `derks@2024-06-22: remove after 3.9 is EOL?` comment stay in place — modernization-style cleanup defers to Phase 3 REFACTOR-04."

patterns-established:
  - "Verification gate pattern: every Phase 1 commit MUST satisfy `make comply && make test` before landing — applied here on tool-version-unchanged baseline (ruff 0.3.2, mypy 1.9.0, pytest 4.3.1 floors)."
  - "Single-concern atomic commit: '3.9 drop' is one concern even though it spans 9 files and two file-format domains (Python config + YAML compose + shell Makefile + Markdown docs + Dockerfile)."

requirements-completed: [PYVER-01, PYVER-02, PYVER-03]

# Metrics
duration: 2 min
completed: 2026-04-30
---

# Phase 01 Plan 01: Drop Python 3.9 Support Summary

**Atomic D-05 commit drops Python 3.9 from every project surface (pyproject.toml floor + ruff/mypy targets, GitHub Actions matrix, Makefile dev target, docker-compose service set, two scaffolding-template Dockerfiles, README prose) plus deletes dead Travis CI; ruff/mypy/pytest 100% green on the unchanged tool floors.**

## Performance

- **Duration:** 2 min
- **Started:** 2026-04-30T05:28:35Z
- **Completed:** 2026-04-30T05:31:11Z
- **Tasks:** 1 (single atomic-commit task per D-05)
- **Files modified:** 9 (7 edits + 2 deletions)

## Accomplishments

- Single atomic commit `00d37e16` lands per D-05 with subject `chore: drop python 3.9 from supported matrix` (exactly per plan's `<verify>` regex `^chore: drop python 3\.9`).
- Python floor raised to 3.10 in pyproject.toml: `requires-python = ">=3.10"`, `[tool.ruff] target-version = "py310"`, `[tool.mypy] python_version = "3.10"`.
- CI matrix in `.github/workflows/build_and_test.yml` now `["3.10", "3.11", "3.12", "3.13", "3.14", "pypy3.10"]` — pypy3.10 retained as planned.
- `cement-py39` references and supporting Dockerfile removed from Makefile dev target, docker-compose.yml, and `docker/Dockerfile.dev-py39`.
- Both generate-template Dockerfiles (`cement/cli/templates/generate/{todo-tutorial,project}/Dockerfile`) bumped from `FROM python:3.9-alpine` to `FROM python:3.10-alpine` in lockstep.
- README.md "Tested on Python 3.9+" -> "Tested on Python 3.10+"; the `docker-compose ps` example block updated to drop the `cement-py39_1` row and rewrite the `docker-compose exec cement-py39` example to `cement-py310`.
- `.travis.yml` deleted entirely per RESEARCH.md Pitfall 7 + Open Question 2 — Travis was non-active CI; keeping it would have been dead infrastructure and a future-grep liability.
- PYVER-01 (drop 3.9 from CI matrix), PYVER-02 (raise floor + bump scaffolds), and PYVER-03 (verification audit returns empty) all closed.

## Task Commits

Single atomic task per D-05:

1. **Task 1: Atomic Python 3.9 drop across all traces (single commit per D-05)** - `00d37e16` (chore)

_No plan-metadata commit yet — that lands after STATE/ROADMAP/REQUIREMENTS updates below._

## Files Created/Modified

### Modified

- `pyproject.toml` — `requires-python = ">=3.10"` (line 19), `target-version = "py310"` (line 72), `python_version = "3.10"` (line 110). Other ruff/mypy/dep-pin knobs untouched per D-13/D-15 (those land in Plans 02-04).
- `.github/workflows/build_and_test.yml` — `test-all.strategy.matrix.python-version` drops `"3.9"`. Sibling lines (`python-version: "3.x"` defaults at lines 27, 48) untouched — they already resolve to latest stable.
- `Makefile` — single-line delete: `docker compose exec cement-py39 pdm install`. `cement`, `cement-py310..cement-py313` lines preserved.
- `docker-compose.yml` — six-line block delete (`cement-py39:` service, lines 56–61 in pre-edit file). `cement-py310:` block becomes the new lowest-Python-version service.
- `cement/cli/templates/generate/todo-tutorial/Dockerfile` — `FROM python:3.9-alpine` -> `FROM python:3.10-alpine`. User-facing change; flag for Phase 6 DOCS-03 changelog.
- `cement/cli/templates/generate/project/Dockerfile` — same FROM bump in lockstep with todo-tutorial sibling.
- `README.md` — `Tested on Python 3.9+` -> `Tested on Python 3.10+`; example `docker-compose ps` block has the `cement_cement-py39_1` row removed; the `docker-compose exec cement-py39 /bin/bash` example rewritten to `cement-py310`; the `|> cement-py39 <|` PS1 line in the example output rewritten to `|> cement-py310 <|`; the parenthetical `(ex: cement-py39, cement-py310, etc)` rewritten to `(ex: cement-py310, cement-py311, etc)`.

### Deleted

- `docker/Dockerfile.dev-py39` — sibling Dockerfile.dev-py310..py314 are the surviving pattern; nothing else referenced this file (verified by grep before delete).
- `.travis.yml` — deleted per RESEARCH.md Pitfall 7 + Open Question 2; Travis is no longer cement's CI.

## Decisions Made

1. **Single atomic commit covering all 9 traces (D-05).** No splitting into per-file or per-domain commits. This proves the D-05 atomic-commit pattern works for a 9-file, multi-format change and gives a clean bisect anchor: "before this commit, 3.9 supported; after this commit, 3.9 dropped."
2. **`.travis.yml` deleted, not partially edited.** RESEARCH.md Pitfall 7 explicitly recommends deletion because Travis is not the active CI and trimming 3.8/3.9 entries while leaving the file would be dead-infrastructure technical debt. Deletion also satisfies D-05 "ALL 3.9 traces simultaneously" cleanly without leaving a partially-edited Travis file as a future-grep hit.
3. **`cement/utils/fs.py` `from __future__ import annotations` + the `derks@2024-06-22: remove after 3.9 is EOL?` comment stay (D-14).** Strict-minimum boundary holds — even self-flagged 3.9-related cleanups defer to Phase 3 REFACTOR-04. The PYVER-03 audit grep filter explicitly excludes the `__future__` line for the same reason.
4. **No tool version bumps in this commit (D-13).** `ruff>=0.3.2`, `mypy>=1.9.0`, `pytest>=4.3.1` floors retained. Plans 02-04 own the ruff/mypy/pytest bumps respectively. This protects the strict-minimum boundary and ensures `make comply && make test` exit 0 on the same tool floors that produced the pre-bump baseline.
5. **README.md edits keep the example shape with `cement-py310` rather than dropping the docker-compose example.** Per PATTERNS.md "Recommend replace with py310" guidance — the example is teaching the docker-compose-exec pattern, not advocating for py39 specifically.

## Deviations from Plan

None - plan executed exactly as written.

The plan's 9-target-file list was followed in lockstep. The plan's exact `<verify>` automated assertions all returned the expected results:

- `make comply` -> "All checks passed!" + "Success: no issues found in 51 source files"
- `make test` -> 316 passed, 1692 warnings, 100.00% coverage on TOTAL (cement/), 52.85s
- The `! grep -rn '3\.9\|py39\|python:3\.9' pyproject.toml .github/ Makefile docker-compose.yml docker/ cement/cli/templates/generate/ README.md` assertion returns empty
- `test ! -e docker/Dockerfile.dev-py39` and `test ! -e .travis.yml` both true
- All seven `grep -q '<exact target text>'` assertions match
- `git log -1 --pretty=%s | grep -E '^chore: drop python 3\.9'` matches with subject `chore: drop python 3.9 from supported matrix` (44 chars)
- Body lines all ≤78 chars, verified via `git log -1 --format=%b | awk 'length>78'` returning empty

The PYVER-03 audit grep, with the documented filters for `__future__` annotations and `cement/utils/version.py` runtime version reporter, returns one match (`cement/utils/fs.py:3: # derks@2024-06-22: remove after 3.9 is EOL?`). That line is the **comment above** the `from __future__ import annotations` line that D-14 explicitly preserves; D-14 stays in scope for Phase 3 REFACTOR-04. This is **not a deviation** — the plan's verification grep filters the `__future__` line itself, and the comment is the reason that filter exists. The grep confirms zero unexpected 3.9 traces remain.

**Total deviations:** 0. **Impact on plan:** none.

## Issues Encountered

None — single-task plan executed cleanly. All quality gates green on first run.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

**Ready for plan 01-02 (ruff bump).** The py310 floor is now in place:

- Plan 02 can target py310 in its ruff `extend-select` family additions without worrying about lower-version compatibility.
- Plan 03 can bump mypy with `python_version = "3.10"` already pinned.
- Plan 04 can bump pytest/pytest-cov/coverage on a known-good py310+ test surface.
- The PDM auto-update pipeline (Phase 2 concern) will now resolve dependencies against `>=3.10` when it next runs — consistent with the Phase 1 → Phase 2 handoff intent.

**Risks carried forward:**

- CI matrix verification on Python 3.10/3.11/3.12/3.14 hasn't been exercised yet (only 3.13 ran locally via `make test`). The matrix run happens in GitHub Actions on push. Risk is low because cement uses legacy-form type annotations (`Dict`/`Optional`/`List`) and no PEP 695 / 3.12-only syntax — but `gh pr checks <PR>` after push is the formal gate.
- `pdm.lock` not regenerated in this commit (intentional — out of scope for this plan). Plans 02-04 dependency bumps will trigger the re-lock and that re-lock will resolve against the new `>=3.10` floor.

## Self-Check: PASSED

**File checks:**
- FOUND: pyproject.toml (modified — `requires-python = ">=3.10"`, `target-version = "py310"`, `python_version = "3.10"` all confirmed via grep)
- FOUND: .github/workflows/build_and_test.yml (modified — matrix is `["3.10", "3.11", "3.12", "3.13", "3.14", "pypy3.10"]`, no 3.9)
- FOUND: Makefile (modified — no `cement-py39` line)
- FOUND: docker-compose.yml (modified — no `cement-py39:` service block)
- FOUND: cement/cli/templates/generate/todo-tutorial/Dockerfile (modified — `FROM python:3.10-alpine`)
- FOUND: cement/cli/templates/generate/project/Dockerfile (modified — `FROM python:3.10-alpine`)
- FOUND: README.md (modified — "Tested on Python 3.10+", `cement-py310` examples)
- DELETED (intentional): docker/Dockerfile.dev-py39
- DELETED (intentional): .travis.yml

**Commit checks:**
- FOUND: `00d37e16` — `chore: drop python 3.9 from supported matrix` (subject 44 chars, body all ≤78 chars, 9 files changed: 10 insertions(+), 112 deletions(-), 2 file deletions registered)

**Quality gate checks:**
- `make comply` exit 0 on unchanged tool floors (ruff 0.3.2, mypy 1.9.0)
- `make test` exit 0: 316 passed, 100.00% coverage on cement/

---
*Phase: 01-tooling-baseline-python-matrix*
*Completed: 2026-04-30*
