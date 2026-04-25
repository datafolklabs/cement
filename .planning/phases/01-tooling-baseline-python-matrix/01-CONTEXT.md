# Phase 1: Tooling Baseline & Python Matrix - Context

**Gathered:** 2026-04-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Bring `ruff`, `mypy`, and `pytest`/`pytest-cov`/`coverage` to current stable
versions, drop Python 3.9 from every surface (pyproject, ruff target, mypy
python_version, CI matrix, Makefile dev target, docker-compose services,
generate-templates Dockerfiles), and clear the lint/type fallout so the rest
of the milestone has a clean starting line. Codify the ruff/mypy rule sets in
`pyproject.toml` so the next tool bump cannot change the rule surface
implicitly.

**In scope:** tooling version bumps, rule-set codification, Python 3.9
removal, mechanical fix-the-fallout work that the chosen rule families
literally surface.

**Out of scope:** any modernization the tools don't directly fail on
(syntax, idioms, pathlib, cached_property, f-string conversion, type-hint
syntax migration). Those belong to Phase 3 (REFACTOR-04).

</domain>

<decisions>
## Implementation Decisions

### Sequencing & commit shape
- **D-01:** Land in two ordered steps inside a single PR.
  Step 1 = drop Python 3.9 (mechanical removal). Step 2 = bump tools and
  fix the fallout.
- **D-02:** Single PR for the whole phase, atomic per-concern commits inside
  it. Commits use Conventional Commits per CLAUDE.md (e.g.,
  `chore: drop python 3.9 from supported matrix`,
  `chore: bump ruff to X.Y`,
  `fix(lint): resolve E501 fallout from ruff bump`).
  Subject and body wrapped at 78 chars.
- **D-03:** Within Step 2, tool bumps land in this order: **ruff → mypy →
  pytest**. Each bump is a `chore: bump <tool>` commit followed by one or
  more `fix(...)` commits resolving its specific fallout, before moving to
  the next tool.
- **D-04:** Lint-fix commits inside Step 2 are split **one commit per ruff
  rule family** (e.g., `fix(lint): resolve E501 line-length`, `fix(lint):
  resolve F401 unused imports`). Bisect-friendly and matches the
  rule-codification discipline TOOL-04 wants.
- **D-05:** Step 1's "drop 3.9" commit is a single coherent change that
  covers ALL 3.9 traces simultaneously: `pyproject.toml` `requires-python`,
  ruff `target-version`, mypy `python_version`, GitHub Actions matrix in
  `.github/workflows/build_and_test.yml`, the `dev` target in `Makefile`
  (the `cement-py39` container reference), any `docker/` compose service
  for py39, and the two generate-template Dockerfiles
  (`cement/cli/templates/generate/todo-tutorial/Dockerfile` and
  `cement/cli/templates/generate/project/Dockerfile`, both `python:3.9-alpine`
  → `python:3.10-alpine`).

### Ruff rule scope
- **D-06:** **Claude's Discretion** — the exact ruff rule families enabled
  for Phase 1 are deferred to research/planner. They will compare current
  community standards for backward-compat-strict Python framework projects
  (pydantic / httpx / attrs / similar) and pick.
- **D-07:** **Constraint on D-06:** the chosen families MUST be
  bug-and-style families (e.g., `E`, `F`, `W`, `B`), not modernization-
  driving families. **`UP` (pyupgrade), `SIM`, and similar syntax-modernizing
  rule families are off-limits for Phase 1** and belong to Phase 3
  (REFACTOR-04). This protects the strict-minimum boundary (D-13).
- **D-08:** TOOL-04 "no implicit drift" is enforced via the **hybrid
  pattern**: family-level `extend-select`, an explicit `ignore = []` block
  (with a comment naming itself as the audit point on every ruff bump), and
  a compatible-release pin on ruff in `[dependency-groups]` (D-15). New
  rules added to a selected family will fire as CI failures, forcing a
  deliberate add-with-comment to `ignore`. Drift is detected, not silently
  absorbed.
- **D-09:** Ruff `preview` flag flipped to **`false`**. Currently
  `preview = true` — preview rules can change, be removed, or graduate
  between releases, which is the literal opposite of TOOL-04's intent.

### mypy configuration
- **D-10:** mypy scope held at **`cement/`-only**. Tests stay excluded.
  Expanding mypy coverage to `tests/` is a future concern (likely Phase 3
  or a dedicated type-coverage milestone), not a Phase 1 codification
  detail.
- **D-11:** mypy strictness knobs **not tightened** this phase. Bump
  `python_version = "3.9"` → `"3.10"` and leave every other knob exactly
  as-is. REFACTOR-02 in Phase 3 owns "tighten type hints" — pulling that
  forward would violate the strict-minimum boundary.

### Tool dev-deps pinning
- **D-12:** Pinning strategy is **hybrid**: `ruff` and `mypy` move to
  compatible-release (`~=X.Y`) since they evolve fast and rule sets shift
  on minor bumps. `pytest`, `pytest-cov`, `coverage`, `mock`, `pypng`,
  `requests`, `commitizen` stay on floor (`>=`) pins since they break
  rarely. Targeted control where the actual drift risk lives.

### Modernization boundary (Phase 1 vs Phase 3)
- **D-13:** **Strict minimum-to-green.** Phase 1 only fixes what the
  bumped tools literally fail on with the chosen, rule-set-capped (D-07)
  configuration. No volunteer modernization. Type-hint syntax stays
  exactly as-is (`Optional[X]`, `Union[X, Y]`, `List[X]`, `Tuple[X, Y]`,
  `Dict[K, V]` per current CONVENTIONS.md). f-strings, contextlib helpers,
  `cached_property`, `pathlib` migration — all stay in Phase 3.
- **D-14:** **`from __future__ import annotations` stays in place this
  phase**, including in `cement/utils/fs.py` line 4 (despite the
  self-flagged "remove after 3.9 EOL?" comment) and any other file that
  uses it (e.g., `cement/core/foundation.py`). Stripping these is Phase 3
  REFACTOR-04 work. Strict-minimum means strict — even self-flagged
  3.9-related cleanups defer.

### Codification side-effects
- **D-15:** Ruff version pin (D-08) lands in the same commit that bumps
  ruff in Step 2. Mypy version pin (D-12) lands in the same commit that
  bumps mypy. Pin and bump are coupled — never split.

### Claude's Discretion
- The specific ruff rule families chosen (D-06).
- The order of individual rule-family fix commits within Step 2 (e.g.,
  whether `fix(lint): resolve E501` lands before `fix(lint): resolve F401`).
- Exact compatible-release minor pin values for ruff and mypy (research
  picks current stable, then applies `~=`).
- Whether to use `select` vs `extend-select` for the chosen family list
  (semantic equivalent for our purposes; planner picks based on what
  reads cleaner in pyproject).

### Folded Todos
None — STATE.md "Pending Todos" is empty.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project intent and constraints
- `.planning/PROJECT.md` — Core Value, no-breakage rule on 3.0.x, Constraints
  block (Python 3.10–3.14 floor after this milestone, zero new runtime deps,
  100% coverage absolute), Key Decisions table.
- `.planning/REQUIREMENTS.md` §"Tooling Baseline" (TOOL-01..04) and
  §"Python Version Policy" (PYVER-01..03) — exact requirements this phase
  must satisfy.
- `.planning/ROADMAP.md` §"Phase 1: Tooling Baseline & Python Matrix" —
  goal, dependencies (none — first phase), success criteria, requirement
  mapping.
- `.planning/ROADMAP.md` §"Phase 3: Internal Refactor & Coverage Hardening"
  — REFACTOR-02/03/04 define what modernization work LIVES in Phase 3 and
  is therefore explicitly out of bounds for Phase 1 (see D-13, D-14).

### Existing codebase intel
- `.planning/codebase/CONVENTIONS.md` — current ruff config, line length,
  type-annotation full-form convention (Optional/Union/List/Tuple/Dict).
  This phase preserves this convention exactly.
- `.planning/codebase/STACK.md` — current tool versions, Python matrix,
  optional-dependency map.
- `.planning/codebase/TESTING.md` — current pytest invocation surface,
  coverage gate enforcement, what `make test` actually runs.
- `CLAUDE.md` §"Commit Conventions" — Conventional Commits required, 78-char
  subject and body wrap, `make commit` (`pdm run cz commit`) for interactive
  authoring.

### Files this phase will touch
- `pyproject.toml` — `[project] requires-python`, `[tool.ruff] target-version`
  + `preview` + `[tool.ruff.lint] extend-select`/`ignore`,
  `[tool.mypy] python_version`, `[dependency-groups] dev` pins.
- `.github/workflows/build_and_test.yml` — `test-all.strategy.matrix.python-version`
  (drop `"3.9"`).
- `.github/workflows/pdm.yml` — verify the scheduled `pdm update` job runs
  cleanly against the new baseline (Phase 2 owns unblocking it; Phase 1
  must not regress it).
- `Makefile` — `dev` target removes `cement-py39` line.
- `cement/cli/templates/generate/todo-tutorial/Dockerfile`,
  `cement/cli/templates/generate/project/Dockerfile` — `python:3.9-alpine`
  → `python:3.10-alpine`.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `make comply`, `make comply-ruff`, `make comply-ruff-fix`, `make comply-mypy`,
  `make test`, `make test-core` — existing entry points, no new make targets
  required this phase.
- `pdm run cz commit` (`make commit`) — already wired up; honors the
  Conventional Commits requirement from CLAUDE.md.

### Established Patterns
- **Strict mypy config** with explicit knobs (not `strict = true` umbrella).
  Phase 1 preserves this pattern — bumping `python_version` only.
- **Ruff config keeps `extend-select` style** rather than full `select`
  override. Phase 1 keeps this style (D-08).
- **`tool.ruff.lint.fixable = ["ALL"]`** — broad auto-fix permission already
  in place; Phase 1's rule-family fixes will leverage `make comply-ruff-fix`.
- **`tests/` excluded from mypy**. Preserved (D-10).
- **Coverage report HTML**: `--cov-report=html:coverage-report` — already
  configured; not touched this phase.

### Integration Points
- **CI gate**: `.github/workflows/build_and_test.yml` runs `make comply`
  (ruff + mypy) and `make test` (pytest + coverage) on every PR. The
  Phase 1 PR must turn this gate green end-to-end across the new matrix
  (3.10 / 3.11 / 3.12 / 3.13 / 3.14, plus pypy3.10 if kept).
- **Scheduled job**: `.github/workflows/pdm.yml` runs `pdm update` weekly.
  This phase does NOT change that workflow — Phase 2 unblocks it. But
  Phase 1's tool pins (D-12, D-15) directly affect what `pdm update`
  produces in Phase 2.
- **Generate templates**: `cement` CLI users scaffold apps from
  `cement/cli/templates/generate/`. The template Dockerfile bumps from
  `python:3.9-alpine` to `python:3.10-alpine` are user-facing and should
  be flagged in the eventual 3.0.16 changelog (Phase 6 DOCS-03 work).

### Known traces of Python 3.9
- `pyproject.toml` line 19: `requires-python = ">=3.9"`
- `pyproject.toml` line 72: `target-version = "py39"`
- `pyproject.toml` line 110: `python_version = "3.9"` (mypy)
- `.github/workflows/build_and_test.yml` line 68: matrix includes `"3.9"`
- `Makefile` line 16: `docker compose exec cement-py39 pdm install`
- `cement/cli/templates/generate/todo-tutorial/Dockerfile` line 1
- `cement/cli/templates/generate/project/Dockerfile` line 1
- `cement/utils/fs.py` lines 3-4: `from __future__ import annotations` with
  "remove after 3.9 EOL?" comment — **stays in place per D-14**, not a
  3.9 trace this phase removes.
- `cement/utils/version.py` line 78: `sys.version_info[0:3]` — runtime
  reporting, NOT a 3.9 conditional. Leave as-is.
- A planner-time `grep -rn "3\.9\|sys\.version_info.*9" cement/` is
  required to confirm no other shims hide.

</code_context>

<specifics>
## Specific Ideas

- The user-articulated pain point (PROJECT.md "What sparked this milestone")
  is the stalled `pdm update` GitHub Action drowning in ruff lint each
  week. Phase 1's success is measured in part by whether the rule-set
  codification (D-08) plus version pin (D-12, D-15) actually prevent
  that drowning the next time the lockfile auto-updates. The hybrid
  audited-ignore pattern is chosen specifically because it converts new
  rule additions into deliberate config decisions instead of silent CI
  red.
- The "no implicit drift" framing in TOOL-04 is the user's literal ask;
  the hybrid pattern (D-08) was chosen over full per-rule enumeration
  because the latter is high-maintenance for a project without a dedicated
  lint-curator role and is not what comparable mature Python libraries
  actually do.

</specifics>

<deferred>
## Deferred Ideas

- **`from __future__ import annotations` cleanup** — multiple files use it
  (e.g., `cement/utils/fs.py`, `cement/core/foundation.py`). Strip in
  Phase 3 alongside REFACTOR-04 modern-stdlib-idioms work. Phase 1 keeps
  them in place (D-14).
- **Type-hint syntax modernization** (`Optional[X]` → `X | None`,
  `Union[X, Y]` → `X | Y`, `List`/`Tuple`/`Dict` → builtin generics).
  Belongs to Phase 3 REFACTOR-04. Phase 1 leaves the `typing` imports
  untouched (D-13).
- **Ruff `UP` / `SIM` rule families** — explicitly banned for Phase 1
  (D-07). Re-evaluate in Phase 3 once the modernization pass is happening
  and the lint surface can absorb the additional fallout.
- **Mypy expansion to `tests/`** — deferred (D-10). Likely future-milestone
  work, not in v1.
- **`strict = true` mypy umbrella** — not adopted (D-11) because that IS
  implicit drift. Stays an explicit-knob config indefinitely.
- **Coverage strictness knob review** (e.g., branch coverage, fail_under
  threshold) — Phase 3 owns coverage hardening (COV-01..03). Not touched
  in Phase 1.
- **Pypy3.10 in CI matrix** — currently included alongside CPython 3.9–3.14.
  Not a Phase 1 decision; planner verifies it stays green when 3.9 drops
  and otherwise leaves it alone.

</deferred>

---

*Phase: 01-tooling-baseline-python-matrix*
*Context gathered: 2026-04-24*
