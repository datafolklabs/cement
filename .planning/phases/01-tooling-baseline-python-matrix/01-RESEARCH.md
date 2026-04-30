# Phase 1: Tooling Baseline & Python Matrix - Research

**Researched:** 2026-04-29
**Domain:** Python build tooling — `ruff` / `mypy` / `pytest` / `pytest-cov` / `coverage`
configuration, Python version-floor migration on a strict-back-compat library
(`cement`).
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Sequencing & commit shape**
- **D-01:** Two ordered steps inside a single PR. Step 1 = drop Python 3.9
  (mechanical removal). Step 2 = bump tools and fix the fallout.
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
  rule family** (e.g., `fix(lint): resolve E501 line-length`,
  `fix(lint): resolve F401 unused imports`). Bisect-friendly and matches
  the rule-codification discipline TOOL-04 wants.
- **D-05:** Step 1's "drop 3.9" commit is a single coherent change that
  covers ALL 3.9 traces simultaneously: `pyproject.toml` `requires-python`,
  ruff `target-version`, mypy `python_version`, GitHub Actions matrix in
  `.github/workflows/build_and_test.yml`, the `dev` target in `Makefile`
  (the `cement-py39` container reference), any `docker/` compose service
  for py39, and the two generate-template Dockerfiles.

**Ruff rule scope**
- **D-06:** **Claude's Discretion** — exact ruff rule families enabled for
  Phase 1 are deferred to research/planner. (See § "D-06 Recommendation".)
- **D-07:** Constraint on D-06 — chosen families MUST be bug-and-style
  (e.g., `E`, `F`, `W`, `B`), not modernization-driving. **`UP`, `SIM`,
  and similar syntax-modernizing families are off-limits for Phase 1**
  (Phase 3 REFACTOR-04 territory).
- **D-08:** TOOL-04 enforced via the **hybrid pattern** — family-level
  `extend-select`, an explicit `ignore = []` block (with audit-point
  comment), and a compatible-release pin on ruff in
  `[dependency-groups]`. New rules added to a selected family fire as
  CI failures, forcing a deliberate add-with-comment to `ignore`.
- **D-09:** Ruff `preview` flag flipped to **`false`**. Currently
  `preview = true` — preview rules can change/be removed/graduate
  between releases.

**mypy configuration**
- **D-10:** mypy scope held at **`cement/`-only**. Tests stay excluded.
- **D-11:** mypy strictness knobs **not tightened** this phase. Bump
  `python_version = "3.9"` → `"3.10"` and leave every other knob exactly
  as-is.

**Tool dev-deps pinning**
- **D-12:** Hybrid pinning. `ruff` and `mypy` move to compatible-release
  (`~=X.Y`). `pytest`, `pytest-cov`, `coverage`, `mock`, `pypng`,
  `requests`, `commitizen` stay on floor (`>=`) pins.

**Modernization boundary**
- **D-13:** **Strict minimum-to-green.** Phase 1 only fixes what the
  bumped tools literally fail on with the chosen, rule-set-capped (D-07)
  configuration. No volunteer modernization. Type-hint syntax stays
  exactly as-is (`Optional[X]`, `Union[X, Y]`, `List[X]`, `Tuple[X, Y]`,
  `Dict[K, V]`).
- **D-14:** **`from __future__ import annotations` stays in place this
  phase**, including in `cement/utils/fs.py` line 4 and any other file
  that uses it (e.g., `cement/core/foundation.py` plus 27 other files —
  see § "Runtime State Inventory"). Stripping these is Phase 3 work.

**Codification side-effects**
- **D-15:** Ruff version pin (D-08) lands in the same commit that bumps
  ruff in Step 2. Mypy version pin (D-12) lands in the same commit that
  bumps mypy. Pin and bump are coupled — never split.

### Claude's Discretion

- The specific ruff rule families chosen (D-06).
- The order of individual rule-family fix commits within Step 2.
- Exact compatible-release minor pin values for ruff and mypy (research
  picks current stable, then applies `~=`).
- Whether to use `select` vs `extend-select` for the chosen family list.

### Deferred Ideas (OUT OF SCOPE)

- **`from __future__ import annotations` cleanup** — Phase 3 REFACTOR-04.
- **Type-hint syntax modernization** (`Optional[X]` → `X | None`,
  `Union[X, Y]` → `X | Y`, `List`/`Tuple`/`Dict` → builtin generics) —
  Phase 3 REFACTOR-04.
- **Ruff `UP` / `SIM` rule families** — explicitly banned for Phase 1
  (D-07). Phase 3 territory.
- **Mypy expansion to `tests/`** — deferred (D-10).
- **`strict = true` mypy umbrella** — not adopted (D-11).
- **Coverage strictness knob review** (branch coverage, fail_under) —
  Phase 3 COV-01..03.
- **Pypy3.10 in CI matrix** — currently included; not a Phase 1 decision.

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| TOOL-01 | Latest stable `ruff` adopted; `make comply-ruff` exits clean across `cement/` and `tests/` | § "Standard Stack" → ruff 0.15.12 verified latest. § "Ruff Family Selection (D-06)" → fallout volume per candidate family. |
| TOOL-02 | Latest stable `mypy` adopted; `make comply-mypy` exits clean | § "Standard Stack" → mypy 1.20.2 verified latest. § "Mypy Bump Fallout" → exact 1-error fallout under 1.20.2. |
| TOOL-03 | `pytest`, `pytest-cov`, `coverage` upgraded to current stable; no deprecation warnings from the test framework itself | § "Standard Stack" → pytest 9.0.3 / pytest-cov 7.1.0 / coverage 7.13.5 verified. § "pytest 9.0 Migration Notes" → breaking-change checklist. |
| TOOL-04 | `ruff` and `mypy` rule configuration in `pyproject.toml` reviewed and codified (no implicit rule drift) | § "Hybrid Codification Pattern" → exact pyproject.toml shape. § "Ruff Family Selection" → comparison vs pydantic / httpx / attrs. |
| PYVER-01 | Python 3.9 removed from `pyproject.toml` `python-requires` and CI matrix | § "Runtime State Inventory" → exhaustive 3.9-trace list. |
| PYVER-02 | Python 3.10 declared as minimum supported version across pyproject, docs, README, and CI | § "Runtime State Inventory" → list includes README and CLAUDE.md edits. |
| PYVER-03 | No 3.9-only compat shims remain in source (verified by grep + linter pass) | § "Runtime State Inventory" → grep audit complete. § "Architecture Patterns → Verification" → grep command codified. |

</phase_requirements>

## Project Constraints (from CLAUDE.md)

These project directives MUST hold across the phase. The planner verifies
compliance.

- **Conventional Commits required.** Subject ≤ 78 chars. Body lines ≤ 78
  chars. Tooling: `make commit` (`pdm run cz commit`) is wired up. The
  per-rule-family commits in D-04 use `fix(lint): resolve <CODE>
  <one-liner>`; tool bumps use `chore: bump <tool> to X.Y`.
- **Zero runtime dependencies for the core framework.** Phase 1 only
  touches `[dependency-groups] dev` and `[tool.*]` sections — no change
  to `dependencies = []`.
- **100% test coverage absolute.** Phase 1 must not regress coverage.
  Tool bumps and lint fixes are non-functional changes; the existing
  coverage gate is the verification.
- **`ruff check cement/ tests/` is the only ruff invocation surface.**
  Driven by `make comply-ruff`. Don't alter the makefile invocation.
- **`mypy` runs against `cement/` only.** `tests/` excluded from mypy in
  current config. D-10 preserves this.
- **Type annotations use full form** (`Optional[X]`, `Union[X, Y]`,
  `List[X]`, etc.). D-13 + D-14 mean Phase 1 does not migrate these.

## Summary

Phase 1 is a **tooling-bump phase**, not a feature phase. The deliverable
is a single PR with two ordered steps: (1) drop Python 3.9 wherever it
appears, (2) bump `ruff` / `mypy` / `pytest` / `pytest-cov` / `coverage`
to current stable and clear the lint/type fallout that the bumps surface
under the chosen, codified rule set. The rule-set codification (TOOL-04)
is the structural payload that prevents the next `pdm update` from
reproducing the stalled-pipeline pain that triggered this milestone.

The single most important research finding is that **the lint explosion
visible when you naively bump ruff (1,010 errors going from 0.14.2 →
0.15.12) is almost entirely caused by `preview = true` activating
preview-graduated rules outside `E`/`F`/`W` — UP, SIM, RUF, C, PIE, FA,
PYI families that the project never opted into.** Flipping
`preview = false` (D-09) on the latest ruff drops the count from 1,010
to **0** under the existing `extend-select = ["E","F","W"]` list. This
collapses Phase 1's lint-fix scope to whatever new families are added
under D-06; the ruff bump itself is otherwise zero-fallout. **The
strict-minimum boundary (D-13) effectively means: pick the new families,
absorb the per-family fallout, and that's the entire Step 2 lint-fix
surface.** [VERIFIED: pdm run ruff check (this session, 2026-04-29)]

The mypy bump from 1.14.1 → 1.20.2 surfaces exactly **one** new error
(a union-attr issue in `cement/core/handler.py:392`) under the
unchanged strict-knobs config — a small, contained fallout.
[VERIFIED: pdm run mypy (this session)]

The pytest 9.0 bump aligns naturally with PYVER-01: pytest 9.0 itself
dropped Python 3.9 support. pytest 9.0 surfaces no project-internal
deprecation noise on the cement test suite (the warnings observed are
cement's own intentional `DeprecationWarning`s already asserted by
`tests/core/test_deprecations.py`). pytest-cov 7.0 has one breaking
change (subprocess measurement removed) — cement does not appear to
use subprocess coverage measurement, so this is a no-op risk to verify
not address. [VERIFIED: pdm run pytest tests/core, this session]

**Primary recommendation:** Adopt the **`E, F, W, B, I, A, C90, N, PT,
T20, YTT` family list** for D-06 (rationale and fallout numbers in
§ "Ruff Family Selection"). This sits squarely in bug-and-style
territory per D-07, matches the bug-finder lean of mature
backward-compat-strict libraries (httpx and pydantic both include `B`;
pydantic adds `I`/`B`/comprehension/print families), and produces a
**total ~232 lint violations** to fix across Step 2 — bisect-friendly
under D-04's one-commit-per-family rule. Combined with `preview = false`
(D-09) and the hybrid `extend-select` + audited `ignore = []` pattern
(D-08), this codifies a stable rule surface that the scheduled
`pdm update` workflow can sit on top of without drowning in noise on
the next ruff minor.

## Architectural Responsibility Map

This is a tooling/configuration phase. Capabilities map to
configuration tiers, not application tiers.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Lint rule definition | `pyproject.toml` `[tool.ruff.lint]` | — | Single source of truth for ruff config; CI reads directly |
| Lint rule pinning | `pyproject.toml` `[dependency-groups] dev` | `pdm.lock` | Pin lives in groups; lock captures exact resolution |
| Type-check config | `pyproject.toml` `[tool.mypy]` | — | Owned by mypy section directly |
| Test runner config | `pyproject.toml` `[tool.pytest.ini_options]` | — | Phase 1 does not touch this section |
| Python version floor | `pyproject.toml` `[project] requires-python` | ruff `target-version`, mypy `python_version`, CI matrix, Dockerfiles | Cross-cutting — D-05 makes this one atomic commit |
| CI matrix definition | `.github/workflows/build_and_test.yml` | `.github/workflows/pdm.yml` (read-only) | Phase 1 edits build_and_test only |
| Dev-loop entry | `Makefile` (`make comply`, `make test`) | — | Untouched by Phase 1 — only the `dev` target's py39 line goes |
| Generated-app templates | `cement/cli/templates/generate/**/Dockerfile` | — | User-facing; flagged for changelog in Phase 6 |

## Standard Stack

### Core (the bumps Phase 1 lands)

| Library | Verified Latest | Current Pin | Phase 1 Pin | Why Standard |
|---------|-----------------|-------------|-------------|--------------|
| `ruff` | 0.15.12 | `>=0.3.2` | `~=0.15.12` (D-12) | Industry-default Python linter as of 2026; replaces flake8/isort/pyupgrade in one binary; rule sets evolve fast on minor bumps so compatible-release is the right floor. |
| `mypy` | 1.20.2 | `>=1.9.0` | `~=1.20.2` (D-12) | Reference Python type checker; type-error surface drifts on minor bumps so compatible-release pin matches D-08 audit posture. |
| `pytest` | 9.0.3 | `>=4.3.1` | `>=9.0.3` (D-12) | Industry-default Python test runner. 9.0.3 drops 3.9 — aligns with PYVER-01. Stays on `>=` per D-12 (breaks rare). |
| `pytest-cov` | 7.1.0 | `>=2.6.1` | `>=7.1.0` (D-12) | Coverage adapter for pytest. 7.0 dropped subprocess measurement (verify not used). |
| `coverage` | 7.13.5 | `>=4.5.3` | `>=7.13.5` (D-12) | Underlying coverage measurement; floor pin avoids capturing minor changes that don't affect cement's invocation. |

`[VERIFIED: pdm run pip index versions <pkg>, this session 2026-04-29]`
for all five.

### Supporting (untouched in Phase 1, listed for planner sanity)

| Library | Current | Phase | Note |
|---------|---------|-------|------|
| `mock` | `>=5.1.0` | Out-of-scope | Not bumped this phase; floor pin per D-12. |
| `pypng` | `>=0.20220715.0` | Out-of-scope | Floor pin per D-12. |
| `requests` | `>=2.31.0` | Out-of-scope | Floor pin per D-12. |
| `commitizen` | `>=4.10.1` | Out-of-scope | Floor pin per D-12. Drives `make commit`. |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `~=0.15.12` (compatible-release) for ruff | `==0.15.12` (exact pin) | Exact pin would force a deliberate human bump for every patch. Rejected: too rigid for a project that currently uses `>=0.3.2` floor — compatible-release is the half-step that gets D-08's "deliberate decisions on minors" without churning on patches. |
| Floor pins for ruff/mypy | Compatible-release for everything | Rejected per D-12; pytest-family breaks are rare and the project's pain point is exclusively ruff/mypy minor drift. |
| Minimum-Python = 3.10 | Minimum-Python = 3.11 (already-stable; 3.10 in security-only support per upstream PEP 619 calendar through 2026-10) | Rejected: PYVER-01 / PYVER-02 explicitly target 3.10 as the new floor (Python 3.10 EOL is 2026-10; cement drops on EOL per standing policy, so 3.10 will leave the matrix in the *next* milestone, not this one). |

**Installation (in pyproject.toml `[dependency-groups] dev`):**

```toml
[dependency-groups]
dev = [
    "pytest>=9.0.3",
    "pytest-cov>=7.1.0",
    "coverage>=7.13.5",
    "mypy~=1.20.2",
    "ruff~=0.15.12",
    "mock>=5.1.0",
    "pypng>=0.20220715.0",
    "requests>=2.31.0",
    "commitizen>=4.10.1",
]
```

**Version verification command (re-run before commit, in case the
research-to-execution gap is non-trivial):**

```bash
pdm run pip index versions ruff | head -2
pdm run pip index versions mypy | head -2
pdm run pip index versions pytest | head -2
pdm run pip index versions pytest-cov | head -2
pdm run pip index versions coverage | head -2
```

## Architecture Patterns

### System Architecture Diagram

```
                   ┌─────────────────────────┐
                   │      pyproject.toml     │  ← single source of truth
                   │                         │
     ┌─────────────┤ [project]               │
     │             │   requires-python       │
     │             │ [tool.ruff]             │
     │             │   target-version        │
     │             │ [tool.ruff.lint]        │
     │             │   extend-select         │
     │             │   ignore (audit point)  │
     │             │   preview = false       │
     │             │ [tool.mypy]             │
     │             │   python_version        │
     │             │ [dependency-groups] dev │
     │             │   ruff~= mypy~=         │
     │             │   pytest>= cov>=        │
     │             └──┬──────────────────────┘
     │                │
     │ requires-python│ rule config / version floors
     ▼                ▼
┌─────────┐     ┌──────────────────────┐     ┌──────────┐
│ pdm.lock│◄────┤   make comply        │     │ make test│
│  (resol)│     │   (CI gate per PR)   │     │ (pytest +│
└─────────┘     │  ├ ruff check        │     │  100% cov)│
     │          │  └ mypy              │     └────┬─────┘
     │          └──────────┬───────────┘          │
     │                     │                      │
     │           ┌─────────┴──────────┐           │
     ▼           ▼                    ▼           ▼
┌───────────────────────────────────────────────────────┐
│  GitHub Actions: build_and_test.yml                   │
│   ├── comply (job)        ─── reads pyproject + lock  │
│   ├── test (job)          ─── reads pyproject + lock  │
│   └── test-all (matrix)   ─── matrix sources Python   │
│                                versions from yaml     │
└───────────────────────────────────────────────────────┘

      ┌───────────────────────────────────┐
      │  pdm.yml (scheduled, weekly)      │ ← Phase 2 owns; Phase 1
      │   runs `pdm update`               │   must NOT regress.
      │   re-resolves against new ranges  │   Tighter pins (~=) on
      │   regenerates pdm.lock            │   ruff/mypy reduce
      │   opens PR if changed             │   minor-version surprises
      │   ↑ this is the "drowning" job    │   in this PR.
      │     that Phase 1 unblocks         │
      └───────────────────────────────────┘
```

The flow is one-directional: pyproject.toml drives every consumer. The
codification (D-08) makes the pyproject.toml the *only* place rule
membership can change — so a rule-surface change becomes a deliberate
edit, not a side-effect of `pdm update`.

### Recommended Project Structure (for the change set, not the codebase)

Phase 1 touches the following files. **No new files created; no files
deleted aside from `docker/Dockerfile.dev-py39`.**

```
pyproject.toml                                       (edits)
.github/workflows/build_and_test.yml                 (edits)
Makefile                                             (edits — remove py39 line)
docker-compose.yml                                   (edits — remove cement-py39 service)
docker/Dockerfile.dev-py39                           (DELETE)
cement/cli/templates/generate/todo-tutorial/Dockerfile  (edits — 3.9→3.10 base)
cement/cli/templates/generate/project/Dockerfile        (edits — 3.9→3.10 base)
README.md                                            (edits — Python matrix prose)
.travis.yml                                          (edits OR delete — see § Pitfalls)
cement/                                              (edits — only as ruff/mypy fallout demands)
tests/                                               (edits — only as ruff fallout demands)
```

### Hybrid Codification Pattern (TOOL-04, D-08)

This is the **structural payload** of Phase 1. It is the pattern that
prevents the next `pdm update` from drowning the CI in lint.

```toml
[tool.ruff]
target-version = "py310"  # D-05 — was "py39"
line-length = 100         # unchanged
indent-width = 4          # unchanged
exclude = [
    ".git",
    "cement/cli/templates",
    "cement/cli/contrib"
]
include = [
    "cement/**/*.py",
    "tests/**/*.py"
]

[tool.ruff.lint]
# AUDIT POINT: `extend-select` and `ignore` MUST be re-reviewed on every
# `chore: bump ruff` commit. New rules added by ruff to a selected family
# fire as CI failures, forcing a deliberate add-with-comment to `ignore`.
# Drift is detected, not silently absorbed. See ROADMAP.md Phase 1 D-08.
preview = false           # D-09 — was true
extend-select = [
    "E",   # pycodestyle errors           (existing)
    "F",   # Pyflakes                     (existing)
    "W",   # pycodestyle warnings         (existing)
    "B",   # flake8-bugbear (likely-bug)  (NEW — D-06 recommendation)
    "I",   # isort                        (NEW — D-06 recommendation)
    "A",   # flake8-builtins              (NEW — D-06 recommendation)
    "C90", # mccabe complexity            (NEW — D-06 recommendation)
    "N",   # pep8-naming                  (NEW — D-06 recommendation)
    "PT",  # flake8-pytest-style          (NEW — D-06 recommendation)
    "T20", # flake8-print                 (NEW — D-06 recommendation)
    "YTT", # flake8-2020 (sys.version)    (NEW — D-06 recommendation)
]
ignore = [
    # AUDIT POINT: each entry MUST have a one-line justification comment.
    # No silent ignores. Empty list is the green-baseline goal.
]
fixable = ["ALL"]         # unchanged — preserves `make comply-ruff-fix`
unfixable = []            # unchanged
```

The same audit-point comment lives in `[tool.mypy]`:

```toml
[tool.mypy]
python_version = "3.10"   # D-05 — was "3.9"
# AUDIT POINT: strictness knobs are deliberately enumerated, NOT
# `strict = true`. See ROADMAP.md Phase 1 D-11. Adding a new knob is a
# deliberate decision; mypy bumps that introduce new strict defaults
# will fail CI and force the same audit conversation as ruff.
disallow_untyped_calls = true
disallow_untyped_defs = true
disallow_any_unimported = false
disallow_incomplete_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
strict_optional = true
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
show_error_codes = true
# (rest unchanged)
```

### Ruff Family Selection (D-06 Recommendation)

I probed each candidate family against the cement codebase **with the
target settings** (`preview = false`, `target-version = "py310"`,
files: `cement/` + `tests/`). All numbers below are concrete violation
counts measured against the actual codebase under those settings on
ruff 0.15.12. [VERIFIED: pdm run ruff check, this session]

#### Recommended (in)

| Family | Code | Violations | Rationale |
|--------|------|-----------:|-----------|
| pycodestyle errors | E | 0 | Already enabled. Keep. |
| Pyflakes | F | 0 | Already enabled. Keep. |
| pycodestyle warnings | W | 0 | Already enabled. Keep. |
| flake8-bugbear | B | 29 | Bug-finder family. Enabled by httpx, pydantic, attrs (the comparison set). D-07 explicitly cites `B` as in-scope. Top rules: `B007` unused-loop-variable (17), `B904` raise-without-from (8). |
| isort | I | 80 | Import-order enforcement. **All 80 are `I001` unsorted-imports — fixable.** `make comply-ruff-fix` resolves them mechanically. Enabled by pydantic and httpx. Style-not-bug, but in-scope per D-07 (organizational hygiene, not syntax modernization). |
| flake8-builtins | A | 18 | Catches accidental shadowing of built-in names (`list`, `dict`, etc.) — bug-adjacent. Cement currently has 14 `A001` and 4 `A002` violations. May ignore `A001`/`A002` if any are intentional in the codebase (attrs ignores them for that reason — see comparison table). |
| mccabe complexity | C90 | 12 | Bug-finder for over-complex functions. Cement framework is "complex software" (attrs leans the same way) but the default threshold of 10 catches 12 hot spots; planner can tune via `[tool.ruff.lint.mccabe] max-complexity = N` or absorb in `ignore` with a comment. |
| pep8-naming | N | 10 | Style-bug-finder. Mostly `N806` (non-lowercase variable, 6) — usually intentional in test classes. May want to ignore `N806` for tests via per-file-ignores; see § "Pitfalls". |
| flake8-pytest-style | PT | 27 | Catches pytest anti-patterns (e.g., `import pytest` vs `from pytest import raises`). Cement tests already follow this style (see `from pytest import raises` in `tests/core/test_exc.py`); 27 hits are in places that diverged. Bug-adjacent. |
| flake8-print | T20 | 8 | Catches stray `print()` calls. 8 hits — likely all in CLI templates or scripts; fast to audit. Bug-finder. |
| flake8-2020 | YTT | 1 | Catches incorrect `sys.version_info` comparisons. Single hit at `tests/ext/test_ext_argparse.py:13` — exactly the kind of stale Python-version shim PYVER-03 wants caught. |

**Total estimated fallout: ~232 violations** across 8 new families, of
which ~80 (the `I001` block) are auto-fixable. Per D-04, this becomes
**8 fix commits** in Step 2 (one per family that surfaces violations,
which is all 8 of them).

#### NOT Recommended (deliberately excluded under D-07)

| Family | Code | Violations | Why excluded |
|--------|------|-----------:|--------------|
| pyupgrade | UP | 287 | **D-07 hard ban.** Phase 3 REFACTOR-04. Most are `UP006` (181, `Dict`→`dict`) and `UP045` (47, `Optional[X]` → `X \| None`) — exactly the type-hint-syntax migration D-13 forbids in Phase 1. |
| flake8-simplify | SIM | 91 | **D-07 hard ban.** Modernization-driving. Phase 3. |
| Ruff-specific | RUF | 244 | Mixed bag — some bug-finders (`RUF013` implicit-optional, 4) and some modernization (`RUF055` unnecessary-regex, 5). Defer to Phase 3 to avoid mixing modernization in. |
| Pylint | PL | 248 | Includes "too-many-X" complexity rules. attrs' config explicitly disables these for "complex software." Cement is in that category. Phase 3 is the natural place to re-evaluate. |
| Bandit security | S | 570 | Dominated by `S101` `assert` (531 hits, all in `tests/`). Asserts in tests are correct usage; this family without per-file-ignores is unmanageable. Phase 5 / SEC-01..03 backlog territory. |
| Annotations | ANN | 761 | Type-annotation completeness. mypy already enforces this on `cement/`; ANN duplicates and adds tests-coverage on top, which is D-10's deferred work. |
| Unused arguments | ARG | 46 | Tempting but cement's handler/interface pattern intentionally has unused method args (interface contracts override). Same family attrs explicitly ignores. Phase 3 territory. |

#### Comparison vs Mature Backward-Compat-Strict Libraries

| Library | Family List | Notes |
|---------|-------------|-------|
| **pydantic** | F, E, I, D (pydocstyle), UP, YTT, B, T10 (debugger), T20 (print), C4 (comprehensions), PERF, PIE, plus selected PYI | More aggressive: includes UP and PERF. Pydantic is on Python 3.10+ and willing to modernize. Cement on 3.0.x track is more conservative — D-07 puts UP off-limits. |
| **httpx** | E, F, I, B, PIE | Lean — focused on bug-finding (B) and import order (I). Closest match to our recommended floor. |
| **attrs** | `select = ["ALL"]` then ignore-many | Inverse pattern — opt out of modernization (ANN, UP via UP031/UP006/UP035, ARG, C901, COM, D, FBT, N, PD, PLR0912/0913/0915/2004, PLW0603, S307, SLF, TC, TD). |
| **My D-06 rec** | E, F, W, B, I, A, C90, N, PT, T20, YTT | Sits between httpx (lean) and pydantic (broader). Bug-and-style only per D-07. Excludes UP/SIM/RUF/PL per D-07 hard ban. |

`[CITED: github.com/pydantic/pydantic/blob/main/pyproject.toml]`
`[CITED: github.com/encode/httpx/blob/master/pyproject.toml]`
`[CITED: github.com/python-attrs/attrs/blob/main/pyproject.toml]`

#### Optional escape hatches the planner can apply

If the per-family fallout is undesirable in the strict-minimum-to-green
boundary (D-13), individual rules can land in `ignore = []` with
audit-point justification comments instead of fixing every site:

- `B007` unused-loop-variable (17) — fix is trivial (`for _ in ...`).
  Recommend fix.
- `B904` raise-without-from-inside-except (8) — fix is mechanical
  (add `from`). Recommend fix.
- `N806` (non-lowercase variable in function, 6) — usually intentional
  in tests. Consider per-file-ignore for `tests/`.
- `PT013` pytest-incorrect-import (14) — likely a stylistic call.
  Recommend fix to preserve the test-file convention already used.
- `C901` (12 complex functions) — recommend `max-complexity = 12` (or
  ignore C901 with comment) to absorb without a refactor that would
  violate D-13.
- `A001`/`A002` (18) — review case-by-case; if framework intentionally
  shadows builtins in handler kwargs, ignore with comment.

### Pattern 1: One Commit Per Rule Family (D-04)

```
chore: bump ruff to 0.15
fix(lint): resolve I001 unsorted-imports (auto-fix)
fix(lint): resolve B007 unused-loop-variable
fix(lint): resolve B904 raise-without-from
fix(lint): resolve B005/B006/B011 misc bugbear
fix(lint): resolve A001/A002 builtin-shadowing
fix(lint): resolve C901 complex-structure
fix(lint): resolve N806/N801/N802 naming
fix(lint): resolve PT013/PT012 pytest-style
fix(lint): resolve T201 print-statements
fix(lint): resolve YTT203 sys-version-info
chore: bump mypy to 1.20
fix(types): resolve union-attr in core/handler.py
chore: bump pytest+pytest-cov+coverage
```

Bisect-friendly. Each commit is independently revertable. Within the
ruff block, the order is the planner's discretion (D-06 Discretion);
running auto-fix first (`I001`) clears 80 of 232 violations in one
move, which is a natural opener.

### Pattern 2: Use auto-fix where safe

```bash
make comply-ruff-fix     # safe-fix only (matches `fixable = ["ALL"]`
                         # plus ruff's safe/unsafe split)
```

`I001` is `[*]` (safe-fix) — 80 import sorts resolve without manual
review. Bugbear hits are mostly not auto-fixable (`[ ]`); plan manual.

### Pattern 3: Verify rule surface didn't drift on bump

Before committing the ruff bump (Step 2 first commit), run:

```bash
# Capture rule list active under current config
pdm run ruff config | grep -E "^lint\." > /tmp/before.txt

# After bumping ruff in pyproject:
pdm run ruff config | grep -E "^lint\." > /tmp/after.txt
diff /tmp/before.txt /tmp/after.txt
```

If the diff is non-trivial (a new rule landed in a selected family),
the planner addresses it via the audit-comment pattern in `ignore` or
fixes the violations. This is D-08's "drift is detected, not silently
absorbed" in operational form.

### Anti-Patterns to Avoid

- **Don't enable `select = ["ALL"]` and then ignore 80% of it.** That's
  the attrs pattern, which works for them because they have a
  dedicated maintainer auditing it. Cement does not. The opposite
  pattern (extend-select with intentional families) matches the
  human-resource constraint stated in CONTEXT.md `<specifics>`.
- **Don't bump ruff and mypy in the same commit.** D-03 / D-04
  explicitly forbid this — bisect needs per-tool isolation.
- **Don't fix `UP` or `SIM` violations even if they look easy.** D-07.
  Even one `Optional[X]` → `X | None` substitution opens the door to
  Phase 3's scope. Strict minimum.
- **Don't change `[tool.ruff.lint] fixable = ["ALL"]`.** It's currently
  permissive and `make comply-ruff-fix` relies on it. Untouched in
  Phase 1.
- **Don't touch `.travis.yml` casually.** It still references Python
  3.8 and 3.9 (lines 15, 22). Travis CI is not the active CI surface
  (GitHub Actions is). Either delete `.travis.yml` (cleanest) or
  update its matrix in lockstep with `.github/workflows/build_and_test.yml`
  per D-05 ("ALL 3.9 traces simultaneously"). Recommend deletion —
  saves maintaining a second CI definition that is not run.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Linting Python | Custom flake8 plugin set | ruff with codified family list | Single binary, 30x faster, replaces flake8/isort/pyupgrade/pylint pieces. Already in use; this phase just bumps and codifies. |
| Type checking | Anything other than mypy | mypy with explicit knobs (D-11) | Reference implementation for PEP 484. Strict knobs already configured. Don't replace with pyright/pyre — knob semantics differ. |
| Test framework | unittest with custom runner | pytest 9.x | Already in use. pytest 9.0 drops 3.9 — perfect alignment. |
| Coverage | Hand-rolled coverage tracking | `coverage` + `pytest-cov` | Industry standard. The 100% gate (CI-03 / COV-01) is enforced against this. |
| Conventional Commit checking | Custom commit-msg hook | `commitizen` (already wired via `make commit`) | Already in `dev` group. CLAUDE.md cites `make commit`. |
| Python version compatibility shim | `sys.version_info` checks | Drop oldest supported version on EOL | This phase IS that pattern. The one shim at `tests/ext/test_ext_argparse.py:13` is itself stale (checks for Py3.4!) and should go in PYVER-03's grep audit. |

**Key insight:** Phase 1 builds *nothing*. It deletes (Python 3.9
references) and re-configures (rule sets and pins). The scope blowup
risk in this phase is *adding* anything beyond rule-set codification.

## Runtime State Inventory

This is a refactor/migration phase (drop a Python version, change tool
config). Runtime state inventory is mandatory.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| **Stored data** | None — Phase 1 makes no data changes. cement is a framework, not a service; there is no database, cache, or persistent store the framework owns. The only state is the codebase itself. | None. |
| **Live service config** | None — cement does not run as a live service in this repo. | None. |
| **OS-registered state** | None — no scheduled tasks, systemd units, launchd plists, pm2 saved processes registered for cement-the-framework. | None. |
| **Secrets / env vars** | `CEMENT_TEST=1` set in `tests/__init__.py` — unrelated to 3.9 drop. `SMTP_HOST`, `MEMCACHED_HOST`, `REDIS_HOST` in CI workflow — unrelated. | None. |
| **Build artifacts / installed packages** | `pdm.lock` will need regeneration after Phase 1's pin changes — but this is **Phase 2's job (DEPS-01)**, not Phase 1's. Phase 1 must not commit a stale lockfile that conflicts with the new ranges. | Verify `pdm install` succeeds with the new pins and decide: leave lockfile alone (Phase 2 regenerates) OR run `pdm lock` once at the end of Step 2. Recommend: let Phase 2 own it. |

### Exhaustive 3.9-trace inventory (D-05 commit covers ALL of these)

`[VERIFIED: grep -rn "3\.9\|sys\.version_info.*9\|py39\|python:3.9", this session]`

| File | Line | Current | Target |
|------|-----:|---------|--------|
| `pyproject.toml` | 19 | `requires-python = ">=3.9"` | `">=3.10"` |
| `pyproject.toml` | 72 | `target-version = "py39"` | `"py310"` |
| `pyproject.toml` | 110 | `python_version = "3.9"` | `"3.10"` |
| `.github/workflows/build_and_test.yml` | 68 | `["3.9", "3.10", "3.11", "3.12", "3.13", "3.14", "pypy3.10"]` | `["3.10", "3.11", "3.12", "3.13", "3.14", "pypy3.10"]` |
| `Makefile` | 16 | `docker compose exec cement-py39 pdm install` | (delete line) |
| `docker-compose.yml` | 56–61 | `cement-py39:` service block | (delete service block) |
| `docker/Dockerfile.dev-py39` | (entire file) | exists | (delete file) |
| `cement/cli/templates/generate/todo-tutorial/Dockerfile` | 1 | `FROM python:3.9-alpine` | `FROM python:3.10-alpine` |
| `cement/cli/templates/generate/project/Dockerfile` | 1 | `FROM python:3.9-alpine` | `FROM python:3.10-alpine` |
| `README.md` | 45 | "Tested on Python 3.9+" | "Tested on Python 3.10+" |
| `README.md` | 136 | example mentions `cement-py39` container | update prose to drop py39 reference |
| `README.md` | 142, 152, 154 | `cement_cement-py39_1`, `docker-compose exec cement-py39`, `\|> cement-py39 <\|` | drop py39-specific examples (or replace with py310 to keep parity) |
| `.travis.yml` | 15–28 | matrix includes `python: "3.8"` and `python: "3.9"` | **Recommend: delete `.travis.yml` entirely.** GitHub Actions is the active CI; Travis is dead infra. If kept, drop both 3.8 and 3.9 entries in lockstep with build_and_test.yml. Either action satisfies D-05's "ALL 3.9 traces simultaneously." |

### NOT 3.9 traces (these stay per D-13/D-14)

| File | Line | Why it's NOT a Phase 1 edit |
|------|-----:|------------------------------|
| `cement/utils/fs.py` | 3–4 | `# derks@2024-06-22: remove after 3.9 is EOL?` self-flagged comment with `from __future__ import annotations`. **D-14 explicit: stays in place.** Phase 3 REFACTOR-04 owns. |
| 28 other files using `from __future__ import annotations` | various | All of `cement/core/*.py`, `cement/ext/*.py`, `cement/cli/main.py`. **D-14 explicit: stays in place.** Phase 3. |
| `cement/utils/version.py` | 78 | `'.'.join([str(x) for x in sys.version_info[0:3]])` — runtime version reporting; not a 3.9 conditional. |
| `tests/ext/test_ext_argparse.py` | 13 | `if (sys.version_info[0] >= 3 and sys.version_info[1] >= 4):` — checks for **Python 3.4+**, not 3.9. Stale shim that PYVER-03 will catch via `flake8-2020 (YTT203)` if `YTT` is in the family list. **Phase 1 fixes this as part of YTT fallout in Step 2, not as part of Step 1's 3.9 drop.** |
| `CLAUDE.md` | 110, 114, 121, 123, 161, 172, 198 | Project doc; gets updated by `/gsd-transition` after the phase ships. Not in the D-05 atomic commit. |
| `.planning/codebase/STACK.md`, `.planning/codebase/CONVENTIONS.md` | various | Documentation describing current state. Updated post-phase, not part of D-05. |

## Common Pitfalls

### Pitfall 1: ruff `preview = true` masquerading as version drift
**What goes wrong:** Bumping ruff produces hundreds of new lint errors
"out of nowhere" and the team blames the rule set or the version.
**Why it happens:** `preview = true` activates rules that haven't
graduated to stable. The rule set is *time-coupled* to the ruff
version, not to the explicit `extend-select` list.
**How to avoid:** D-09 (`preview = false`) is the structural fix.
Phase 1 lands this in the same commit that bumps ruff.
**Warning signs:** Confirmed in this session — the same codebase
reports 0 errors on ruff 0.14.2 with `preview = true` and 1010 errors
on ruff 0.15.12 with `preview = true`. Flipping `preview = false` on
0.15.12 brings it back to 0. [VERIFIED: this session]

### Pitfall 2: pytest 9.0 `PytestRemovedIn9Warning` becoming errors
**What goes wrong:** pytest 9.0 turns `PytestRemovedIn9Warning` into
errors by default. Previously these were warnings.
**Why it happens:** Major-version breaking change in pytest 9.0.
**How to avoid:** Run `pytest tests/core 2>&1 | grep PytestRemovedIn`
under pytest 8.x **before** bumping; resolve any hits first.
**Warning signs:** None found in cement's current test suite under
pytest 8.3.5. The 1674 warnings observed under pytest 9.0.3 are
cement's own intentional `DeprecationWarning`s, not pytest's.
[VERIFIED: this session]

### Pitfall 3: pytest-cov 7.0 dropped subprocess measurement
**What goes wrong:** Tests that measure coverage of subprocess-spawned
code stop measuring it; coverage drops silently.
**Why it happens:** pytest-cov 7.0 breaking change — subprocess
measurement requires explicit opt-in via `[run] patch = subprocess`
in `.coveragerc`.
**How to avoid:** Verify cement does not use subprocess coverage
measurement (the `cement/utils/shell.py` exec_cmd functions are
*tested* in subprocess-style but the test process is the one being
measured, not a forked child).
**Warning signs:** Watch for unexplained coverage regressions on
`cement/utils/shell.py` and `cement/cli/` after the pytest-cov bump.
[CITED: pytest-cov 7.0.0 changelog —
pytest-cov.readthedocs.io/en/latest/changelog.html]

### Pitfall 4: `pdm install` regenerating lockfile mid-PR
**What goes wrong:** Bumping pins in pyproject.toml causes `pdm install`
to silently regenerate `pdm.lock`, polluting the diff.
**Why it happens:** PDM's default behavior on missing-resolution.
**How to avoid:** Decide upfront — Phase 1 either explicitly leaves
the lockfile to Phase 2 (Phase 2's DEPS-01 owns lockfile regen) or
explicitly runs `pdm lock` as a final, separate commit. **Recommend
the former.** Run `pdm install --check` (or equivalent dry-run) on the
new pyproject before pushing.
**Warning signs:** A `pdm.lock` change in the Phase 1 PR that wasn't
deliberately staged.

### Pitfall 5: Mypy 1.20 surface change beyond the one error
**What goes wrong:** Bumping mypy from 1.14 → 1.20 might surface more
than one new error if local probe missed code paths.
**Why it happens:** mypy minor versions add new checks and refine
existing ones; type-narrowing improvements can flip results both ways.
**How to avoid:** The 1-error result was measured against `cement/`
(matching the existing `[tool.mypy] files = ["cement/"]` config) under
the current strict-knobs set. If the planner discovers additional
errors during Step 2, treat them as fallout to fix (per D-13) — they
fall under TOOL-02 not a scope expansion.
**Warning signs:** mypy errors outside `cement/core/handler.py:392`
appearing during `make comply-mypy` under 1.20.2.
[VERIFIED: pdm run mypy under 1.20.2 — 1 error in `cement/core/handler.py:392`,
this session]

### Pitfall 6: Per-file-ignores explosion on N806 / S101
**What goes wrong:** Adding `N` or `S` family naively triggers hundreds
of ignored sites in `tests/` because tests legitimately use `assert`
and non-lowercase locals.
**Why it happens:** ruff defaults are biased toward production code.
**How to avoid:** If the planner enables these families, use
`[tool.ruff.lint.per-file-ignores]`:
```toml
[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["N806"]    # variable casing in tests is fine
```
Per § "Ruff Family Selection", N is recommended (10 violations, low).
S is NOT recommended (570 violations, mostly S101 in tests).

### Pitfall 7: Forgetting `.travis.yml`
**What goes wrong:** D-05 says "ALL 3.9 traces simultaneously" but the
context list doesn't include `.travis.yml`, which still references
Python 3.8 and 3.9.
**Why it happens:** `.travis.yml` is dead infrastructure; nobody
notices.
**How to avoid:** The planner explicitly addresses `.travis.yml` in
the D-05 commit — either delete it (recommended) or drop 3.8/3.9 from
its matrix.
**Warning signs:** A grep for `3.9` post-Step-1 returns hits in
`.travis.yml`. The planner either deletes the file in Step 1 or
documents it as out-of-scope and PYVER-03's "no 3.9 shims" passes
because `.travis.yml` is not source code under PYVER-03's scope.

## Code Examples

### Final pyproject.toml shape (the Phase 1 deliverable)

```toml
# === [project] ===
[project]
name = "cement"
# (...other fields unchanged...)
requires-python = ">=3.10"          # was ">=3.9"  (D-05)
dependencies = []

# === [tool.ruff] ===
[tool.ruff]
target-version = "py310"            # was "py39"  (D-05)
line-length = 100
indent-width = 4
exclude = [
    ".git",
    "cement/cli/templates",
    "cement/cli/contrib"
]
include = [
    "cement/**/*.py",
    "tests/**/*.py"
]

[tool.ruff.lint]
# AUDIT POINT (D-08): re-review on every ruff bump. New rules added by
# ruff to a selected family fire as CI failures, forcing a deliberate
# add-with-comment to `ignore` or a fix. See Phase 1 RESEARCH.md.
preview = false                     # was true  (D-09)
extend-select = [
    "E", "F", "W",                  # already enabled
    "B",                            # flake8-bugbear (NEW, D-06)
    "I",                            # isort (NEW, D-06)
    "A",                            # flake8-builtins (NEW, D-06)
    "C90",                          # mccabe (NEW, D-06)
    "N",                            # pep8-naming (NEW, D-06)
    "PT",                           # flake8-pytest-style (NEW, D-06)
    "T20",                          # flake8-print (NEW, D-06)
    "YTT",                          # flake8-2020 (NEW, D-06)
]
ignore = [
    # AUDIT POINT (D-08): each entry MUST have a one-line justification.
    # Empty list is the green-baseline goal. Examples:
    # "C901",  # cement framework is intentionally complex; see Phase 3
    #          # REFACTOR-01 for revisit. Justified 2026-04-29.
]
fixable = ["ALL"]                   # unchanged
unfixable = []                      # unchanged

# (optional, only if planner enables N family and decides tests-side
# casing is fine)
# [tool.ruff.lint.per-file-ignores]
# "tests/**/*.py" = ["N806"]  # test-fixture variable casing intentional

# === [tool.mypy] ===
[tool.mypy]
python_version = "3.10"             # was "3.9"  (D-05)
# AUDIT POINT (D-08+D-11): strictness knobs deliberately enumerated,
# NOT `strict = true`. Adding a knob is a deliberate decision. mypy
# bumps that introduce new strict defaults will fail CI.
disallow_untyped_calls = true
disallow_untyped_defs = true
disallow_any_unimported = false
disallow_incomplete_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
strict_optional = true
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
show_error_codes = true

disable_error_code = ["attr-defined"]  # MetaMixin/Meta pattern, unchanged

files = ["cement/"]                 # tests excluded (D-10)
exclude = """(?x)(
    ^cement/cli/templates |
    ^.git/ |
    ^tests
  )"""

# === [dependency-groups] ===
[dependency-groups]
dev = [
    "pytest>=9.0.3",                # was >=4.3.1
    "pytest-cov>=7.1.0",            # was >=2.6.1
    "coverage>=7.13.5",             # was >=4.5.3
    "mypy~=1.20.2",                 # was >=1.9.0  (D-12: ~=)
    "ruff~=0.15.12",                # was >=0.3.2  (D-12: ~=)
    "mock>=5.1.0",                  # unchanged
    "pypng>=0.20220715.0",          # unchanged
    "requests>=2.31.0",             # unchanged
    "commitizen>=4.10.1",           # unchanged
]
```
[CITED: pyproject.toml current state, this session]

### Final build_and_test.yml matrix line (single edit per D-05)

```yaml
# .github/workflows/build_and_test.yml line 68
- python-version: ["3.10", "3.11", "3.12", "3.13", "3.14", "pypy3.10"]
#                  ^^^^^^^^ was: "3.9", "3.10", ...
```

### Verification grep for PYVER-03

```bash
# Run from repo root after Step 1 commits. MUST return zero hits in
# cement/ source tree (excluding .planning/, .git/, and the
# explicitly-deferred __future__ imports).
grep -rn "3\.9\|sys\.version_info.*9\|py39\|python:3\.9" \
    cement/ tests/ pyproject.toml .github/ Makefile docker-compose.yml \
    docker/ \
    | grep -v 'from __future__ import annotations' \
    | grep -v 'cement/utils/version.py.*sys\.version_info\[0:3\]'

# Expected output: empty.
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| flake8 + isort + pyupgrade + pylint as separate tools | ruff (single binary) | 2023–2024 became default for new projects; mainstream by 2025 | Cement already uses ruff; this phase only bumps. |
| Ruff `preview = true` for early access to new rules | `preview = false` for stability on rule surface | This phase (D-09) | Stable rule surface; deliberate opt-ins for new rules. |
| Floor-pin everything (`>=`) | Hybrid: `~=` for fast-evolving (ruff/mypy), `>=` for stable | This phase (D-12) | Targeted control where drift risk lives. |
| `select = ["ALL"]` + many ignores | `extend-select = [...]` with intentional families | Phase 1 chooses extend-select per D-08 | Lower-maintenance for projects without dedicated lint-curators. |
| Implicit lint via tool defaults | Explicit codification with audit-point comments | This phase (D-08) | Drift detected, not absorbed. |
| Python 3.9 still in security support | EOL Oct 2025 — drop on EOL per project policy | This phase (PYVER-01) | Aligns with pytest 9.0 (also dropped 3.9), mainstream community drop pattern. |

**Deprecated/outdated:**
- **`.travis.yml`** — Travis CI is no longer cement's primary or
  secondary CI. Recommend deletion as part of D-05 cleanup.
- **pytest-cov subprocess auto-measurement** — removed in pytest-cov
  7.0; opt-in via `[run] patch = subprocess` if needed. Cement does
  not appear to need this.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The 1010-error spike on `ruff 0.15.12` collapses to 0 with `preview = false`, *across all Python versions in the new matrix (3.10–3.14, pypy3.10)*. I verified this on Python 3.14.3 only (the local devbox). | § "Summary" | Low. Ruff is implemented in Rust and does not depend on the host Python version for rule semantics. But if it does diverge on a specific version, that version surfaces additional fallout in CI as more `fix(lint)` commits — same pattern, larger scope. The audit-point hybrid pattern (D-08) handles this correctly: the new rules surface as failures, not as silent drift. | `[ASSUMED]` |
| A2 | pytest-cov 7.0's subprocess-measurement breaking change does not affect cement. I read the changelog and inspected `cement/utils/shell.py` and the test files; cement runs subprocesses for testing but does not measure coverage of those subprocesses (the test process itself is what's measured). | § "Pitfall 3" | Low. If wrong, coverage will silently drop on a few `cement/utils/shell.py` lines after the bump and the 100% gate (CI-03) catches it. The fix is a one-line `.coveragerc` opt-in. | `[ASSUMED]` |
| A3 | The optional dependencies (colorlog, jinja2, pyyaml, redis, pylibmc, watchdog, pystache, tabulate) all support Python 3.10+ at their latest versions. I verified the latest version exists on PyPI for each but did not inspect each package's `python_requires`. | § "Standard Stack — Supporting" / open question | Low. Phase 2 (DEPS-02) owns the optional-extras refresh and is the natural place this gets verified. Phase 1 only needs the *core* tooling versions to support 3.10+, which is verified. | `[ASSUMED]` |
| A4 | Deleting `.travis.yml` is a clean, no-side-effects operation. | § "Pitfalls — Pitfall 7" | Very low. Travis CI is not the active CI surface. If something downstream depends on the file's presence, the planner can choose the alternative (drop 3.9/3.8 from the matrix instead). The discuss-phase did not surface a constraint either way. | `[ASSUMED]` |
| A5 | The cement codebase has no `.pre-commit-config.yaml`, `tox.ini`, or other hidden lint/version configuration that would also need a 3.9 → 3.10 bump. | § "Runtime State Inventory" | Very low. I grepped the entire repo for `3.9` and `py39` references and the inventory above is complete relative to that grep. | `[ASSUMED]` |

The assumptions above are LOW-risk operational details, not core
phase-defining decisions. Locked decisions D-01..D-15 plus the
verified version numbers and verified ruff/mypy fallout numbers are
the load-bearing facts; nothing in this Assumptions Log requires
user re-confirmation before the planner proceeds.

## Open Questions

1. **Does the Python 3.14.3 local probe of ruff fallout accurately
   represent fallout on 3.10/3.11/3.12/3.13?**
   - What we know: ruff is Rust-based and does not interpret Python
     code via the host interpreter; rule semantics are independent of
     host Python version. Configuration `target-version = "py310"`
     controls what syntax ruff recognizes as valid for the *target*,
     and is the same regardless of runtime.
   - What's unclear: nothing observed in this session contradicts the
     assumption that fallout numbers transfer. But the Phase 1 PR's CI
     run is the empirical confirmation across the matrix.
   - Recommendation: planner explicitly notes in the Step 2 plan that
     the per-family fallout counts came from a Python 3.14.3 probe and
     CI is the cross-version verification. No structural change.

2. **Should `.travis.yml` be deleted, updated, or left alone?**
   - What we know: it references Python 3.8 and 3.9. It is not the
     active CI. CONTEXT.md does not mention it.
   - What's unclear: whether deletion is in-scope or out-of-scope for
     Phase 1 under D-05's "ALL 3.9 traces simultaneously" wording.
   - Recommendation: deletion is in-scope and is the cleanest move.
     The planner can include it in Step 1's atomic commit. If the user
     wants to preserve `.travis.yml` (e.g., for documentation
     purposes), the alternative is a 3.8/3.9 drop from its matrix —
     same atomic commit, slightly more text.

3. **What's the right `mccabe.max-complexity` threshold (12 violations
   on default of 10)?**
   - What we know: 12 functions in `cement/` exceed default `C901` of
     10. attrs config explicitly tags itself as "complex software" and
     ignores complexity rules.
   - What's unclear: whether the Phase 1 stance is "fix the 12 hot
     spots" (potentially scope-creep into refactoring) or "absorb in
     `ignore` with an audit comment" (D-13 strict-minimum).
   - Recommendation: **absorb in `ignore`** for Phase 1 with a
     comment pointing to Phase 3 REFACTOR-01 (dead code) /
     REFACTOR-02 (type tightening) for re-evaluation. Adding `C90`
     family signal *as a baseline* without enforcing the threshold
     gets the bug-finder benefit on *new* code without forcing a
     refactor of the framework. Alternative: bump to
     `max-complexity = 12` to absorb the existing baseline. Either
     reads cleanly under D-13.

4. **Should the planner also bump `commitizen`?**
   - What we know: pinned `>=4.10.1`, current latest is likely higher.
     `make commit` is the user's stated workflow.
   - What's unclear: whether Phase 1's TOOL-* requirements include
     commitizen.
   - Recommendation: leave `commitizen` alone in Phase 1. TOOL-01..04
     enumerate ruff/mypy/pytest specifically. commitizen is a
     workflow tool, not a code-quality tool, and it's stable on the
     current floor.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3.14 (host) | Local dev | ✓ | 3.14.3 | — |
| PDM (host) | Project workflow | ✓ | (latest) | — |
| ruff | Compliance | ✓ | 0.14.2 (current pin) → 0.15.12 (probe) | — |
| mypy | Compliance | ✓ | 1.14.1 (current pin) → 1.20.2 (probe) | — |
| pytest | Tests | ✓ | 8.3.5 (current pin) → 9.0.3 (probe) | — |
| pytest-cov | Coverage | ✓ | 5.0.0 (current pin) → 7.1.0 (probe) | — |
| coverage | Coverage | ✓ | 7.6.1 (current pin) → 7.13.5 (probe) | — |
| Docker / docker-compose | Multi-version test loop (`make dev`) | (assumed available — not probed) | n/a | Run-of-`make test` per matrix is the actual CI gate; local Docker is convenience-only. |
| `make` (Makefile) | Dev-loop entry | ✓ | (system) | — |
| `git` | Conventional Commits via cz | ✓ | (system) | — |
| GitHub Actions | CI | ✓ (workflow files present) | — | — |

**Missing dependencies with no fallback:** None.

**Missing dependencies with fallback:** None.

**Note:** This phase is purely tooling/config. The "environment" being
audited is the dev tool surface, not external services. Service
dependencies (Redis/Memcached/SMTP via mailpit) are owned by the test
suite, not Phase 1, and are unaffected by this phase.

## Validation Architecture

`workflow.nyquist_validation: true` per `.planning/config.json`.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest (current 8.3.5 → Phase 1 target 9.0.3) |
| Config file | `pyproject.toml` `[tool.pytest.ini_options]` |
| Quick run command | `pdm run pytest tests/core --cov=cement.core` (matches `make test-core`) |
| Full suite command | `make test` (= `make comply` then `pdm run pytest --cov=cement tests`) |

### Phase Requirements → Test Map

Phase 1 has no new runtime feature surface, so requirement-to-test
mapping is about **tool-level verification** rather than behavioral
unit tests. Each requirement has an automated verification command.

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| TOOL-01 | `make comply-ruff` exits 0 on `cement/` and `tests/` under latest ruff | tooling | `pdm run ruff check cement/ tests/ && echo PASS` | ✅ |
| TOOL-02 | `make comply-mypy` exits 0 under latest mypy with strict knobs | tooling | `pdm run mypy && echo PASS` | ✅ |
| TOOL-03 | `make test` runs without deprecation warnings emitted by pytest itself | tooling | `pdm run pytest tests/core -W error::PytestRemovedIn10Warning -W error::PytestDeprecationWarning && echo PASS` | ✅ (workaround: filter cement's own DeprecationWarnings via `:Cement` module filter or use the explicit pytest categories above) |
| TOOL-04 | Ruff and mypy rule sets explicitly enumerated; no implicit defaults | structural | `python -c "import tomllib; d=tomllib.loads(open('pyproject.toml').read()); assert d['tool']['ruff']['lint']['extend-select'] and d['tool']['ruff']['lint']['preview'] is False"` | ✅ |
| PYVER-01 | Python 3.9 removed from `pyproject.toml` and CI matrix | structural | `! grep -E '"3\.9"\|3\.9-alpine\|requires-python.*3\.9\|target-version.*py39\|python_version.*3\.9' pyproject.toml .github/workflows/build_and_test.yml` | ✅ |
| PYVER-02 | Python 3.10 declared as minimum | structural | `grep 'requires-python = ">=3.10"' pyproject.toml && grep '"3.10"' .github/workflows/build_and_test.yml` | ✅ |
| PYVER-03 | No 3.9-only compat shims in source | structural | See § "Code Examples — Verification grep for PYVER-03" | ✅ |
| Per-matrix CI green | All matrix jobs (3.10, 3.11, 3.12, 3.13, 3.14, pypy3.10) green | E2E | `gh pr checks <PR-NUMBER>` | ✅ (CI infra exists) |

### Sampling Rate

- **Per task commit (in Step 2):** `pdm run ruff check cement/ tests/`
  for ruff-fix commits; `pdm run mypy` for mypy-fix commit; `pdm run
  pytest tests/core` for pytest-bump commit. Each ≤ 10s.
- **Per wave / step boundary:** `make comply && make test` (full
  compliance + full suite) — local equivalent of CI gate. ~30s.
- **Phase gate:** `gh pr checks <PR>` — full matrix green across all
  Python versions in `.github/workflows/build_and_test.yml`. This is
  the binding success criterion for ROADMAP success criteria 1–3
  (paraphrased: ruff clean, mypy clean, pytest clean).

### Wave 0 Gaps

- **None.** All required test infrastructure already exists:
  - `pytest` config in `pyproject.toml`
  - `tests/conftest.py` shared fixtures
  - `tests/__init__.py` setting `CEMENT_TEST=1`
  - `make test`, `make test-core`, `make comply`, `make comply-ruff`,
    `make comply-ruff-fix`, `make comply-mypy` — all wired up

The phase verifies *tooling outputs*, not new runtime behavior. There
are no new tests to write. The verification surface is the existing
`make comply` and `make test` invocations under bumped tools.

## Security Domain

`security_enforcement` not explicitly set in `.planning/config.json` —
treat as enabled per default rule.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | Phase 1 is a tooling/CI phase — no auth surface touched. |
| V3 Session Management | no | No session management in Phase 1. |
| V4 Access Control | no | No access control in Phase 1. |
| V5 Input Validation | no | No new input handlers; existing cement code untouched except for lint-fix mechanical changes. |
| V6 Cryptography | no | No cryptography in Phase 1. |
| V14 Configuration | yes (limited) | Tooling configuration (`pyproject.toml`) is the deliverable. The audit-point hybrid pattern (D-08) is the security-adjacent control: it ensures the lint surface is a deliberate decision rather than implicit drift. |

### Known Threat Patterns for {tooling phases}

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Supply-chain risk via dev-dep range broadening | Tampering | Compatible-release pins (`~=`) on fast-evolving tools (ruff, mypy) per D-12. Floor pins (`>=`) on stable tools. `pdm.lock` captures the exact resolution. The scheduled `pdm update` job (Phase 2 owns) becomes the deliberate review point for new versions. |
| Linter-rule injection through `pdm update` | Tampering | Phase 1 is the explicit fix: rule families codified, `preview = false`, audit-point comments. New rule activations require a deliberate edit to `pyproject.toml`. |
| Outdated Python version with unpatched stdlib CVEs | EoP / Information disclosure | PYVER-01 drops 3.9 (EOL Oct 2025). Standing project policy enforces this. |
| Unbounded version ranges admitting malicious uploads | Tampering | All dev-deps have explicit pins (lower bound) per D-12. PDM lockfile pins exact versions for reproducibility. |

Phase 1 is not the place to add `pip-audit` / `bandit` / SAST — those
are tracked under SEC-01..03 as Phase 5 backlog stubs (per
ROADMAP.md), explicitly to avoid "multiplying noise" while the
baseline is being unblocked. This phase removes one threat (stale
Python 3.9, drift on rule surface); SEC-01..03 are when the project
adds active threat-detection surfaces.

## Sources

### Primary (HIGH confidence)

- `.planning/phases/01-tooling-baseline-python-matrix/01-CONTEXT.md`
  — locked decisions D-01..D-15 (this session)
- `.planning/REQUIREMENTS.md` §"Tooling Baseline", §"Python Version
  Policy" — TOOL-01..04, PYVER-01..03
- `.planning/ROADMAP.md` §"Phase 1: Tooling Baseline & Python Matrix"
  — goal, success criteria
- `.planning/PROJECT.md` — Core Value, Constraints, Key Decisions
- `pyproject.toml` (this session, lines 1–168) — current tool config
- `.github/workflows/build_and_test.yml` (this session, lines 1–99)
  — current CI matrix
- `.github/workflows/pdm.yml` (this session, lines 1–14) — scheduled
  `pdm update` workflow
- `Makefile` (this session, lines 1–88)
- `docker-compose.yml` (this session)
- `CLAUDE.md` (this session) — Conventional Commits, 78-char wrap
- pip index versions queries for ruff (0.15.12), mypy (1.20.2),
  pytest (9.0.3), pytest-cov (7.1.0), coverage (7.13.5) — this
  session 2026-04-29
- `pdm run ruff check` outputs — verified fallout numbers per family
- `pdm run mypy` output under 1.20.2 — verified 1-error fallout
- `pdm run pytest tests/core` under pytest 9.0.3 — verified no
  pytest-internal deprecation noise

### Secondary (MEDIUM confidence)

- pydantic `pyproject.toml` (`github.com/pydantic/pydantic/blob/main/`)
  — comparison config for D-06
- httpx `pyproject.toml` (`github.com/encode/httpx/blob/master/`) —
  comparison config for D-06
- attrs `pyproject.toml` (`github.com/python-attrs/attrs/blob/main/`)
  — comparison config for D-06
- pytest changelog (`docs.pytest.org/en/stable/changelog.html`) —
  pytest 9.0 breaking-change list
- pytest-cov changelog (`pytest-cov.readthedocs.io/en/latest/changelog.html`)
  — pytest-cov 7.0 breaking-change list

### Tertiary (LOW confidence)

- None used. All claims in this research are either VERIFIED via tool
  invocation in-session or CITED to a primary source.

## Metadata

**Confidence breakdown:**
- Standard stack (versions, pins): **HIGH** — exact PyPI versions
  confirmed via `pdm run pip index versions` in-session.
- Architecture (config file shapes): **HIGH** — current state read
  in-session; target state verified by running ruff/mypy under the
  proposed config.
- Pitfalls: **HIGH** — most pitfalls verified by direct probe in this
  session (ruff preview behavior, mypy 1.20 fallout, pytest 9.0
  warnings posture).
- D-06 family selection: **HIGH** — fallout counts measured directly;
  comparison configs read from upstream.
- Cross-version (3.10–3.14, pypy3.10) fallout extrapolation: **MEDIUM**
  — local probe was on Python 3.14.3 only; ruff/mypy are not
  Python-runtime-coupled but the CI matrix is the empirical
  cross-version check.
- Optional-dep 3.10+ compatibility: **MEDIUM** — Phase 2 owns this; I
  verified latest versions exist but did not inspect each
  `python_requires`. Low-risk because Phase 2 is the natural fix.

**Research date:** 2026-04-29
**Valid until:** 2026-05-29 (30 days — versions checked are stable;
no fast-moving claims).
