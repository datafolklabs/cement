# Phase 1: Tooling Baseline & Python Matrix - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or
> execution agents. Decisions are captured in CONTEXT.md — this log
> preserves the alternatives considered.

**Date:** 2026-04-24
**Phase:** 01-tooling-baseline-python-matrix
**Areas discussed:** Sequencing strategy, Ruff rule scope, Modernization
scope vs Phase 3, Codification details (TOOL-04)

---

## Sequencing strategy

### Q1: What order should the work land in?
| Option | Description | Selected |
|--------|-------------|----------|
| Drop 3.9 first, then bump tools | Step 1 raises requires-python and drops 3.9 from CI/Makefile/templates. Step 2 bumps tools and fixes fallout. | ✓ |
| Bump tools first, then drop 3.9 | Bump against py39 target, fix fallout, then drop 3.9. | |
| Interleaved — one combined plan | All changes in one plan. | |

**User's choice:** Drop 3.9 first, then bump tools.

### Q2: How should commits/PRs be structured within the chosen order?
| Option | Description | Selected |
|--------|-------------|----------|
| Atomic per concern, single PR | One PR, atomic conventional-commits-style commits per concern. | ✓ |
| Separate PRs per stage | One PR per stage; more merge friction. | |
| Single squashed commit | One squashed commit; loses bisect-friendliness. | |

**User's choice:** Atomic per concern, single PR.

### Q3: Within Step 2 (tool bumps), what order should ruff/mypy/pytest land in?
| Option | Description | Selected |
|--------|-------------|----------|
| Ruff → mypy → pytest | Lint first, types second, pytest last. | ✓ |
| Mypy → ruff → pytest | Types first; risk of ruff fixes re-shaping mypy-validated code. | |
| Pytest → ruff → mypy | Test framework first; front-loads lowest-value bump. | |
| Claude picks the order | Defer to planner. | |

**User's choice:** Ruff → mypy → pytest.

### Q4: How granular should lint-fix commits be within each tool bump?
| Option | Description | Selected |
|--------|-------------|----------|
| One fix commit per rule family | Per-rule-family bisectable commits. | ✓ |
| One fix commit per file or module | File-scoped commits; mixes rule families. | |
| One 'fix(lint): resolve fallout' commit | Single rollup commit. | |

**User's choice:** One fix commit per rule family.

### Q5: Where should Makefile/Docker/Dockerfile-template 3.9 references land?
| Option | Description | Selected |
|--------|-------------|----------|
| All bundled in Step 1 'drop 3.9' commit | Single coherent removal across pyproject + CI + Makefile + templates. | ✓ |
| Split: source-side vs templates | Templates as a separate user-facing-output commit. | |
| Templates stay on 3.9 (out of scope) | Defer template refresh to a later phase. | |

**User's choice:** All bundled in Step 1 'drop 3.9' commit.

---

## Ruff rule scope

### Q1: What ruff rule scope should Phase 1 land?
| Option | Description | Selected |
|--------|-------------|----------|
| Hold the line: E/F/W only, but explicit | Keep current families, pin specific codes explicitly. | |
| Modest expansion: add I + UP | isort + pyupgrade on top of E/F/W. | |
| Comprehensive: E/F/W + B + I + UP + SIM | Bigger one-time fallout, broader coverage. | |
| Claude picks | Defer to research/planner. | ✓ |

**User's choice:** Claude picks (defer to research/planner).
**Notes:** Constrained later under "Modernization scope" Q1 — research's
pick must be capped to non-modernizing families (UP/SIM off-limits this
phase).

### Q2: How should TOOL-04 'no rule drift on next ruff bump' be enforced?
| Option | Description | Selected |
|--------|-------------|----------|
| Hybrid: family select + audited ignore list + ruff version pin | ~10 lines; new rules force deliberate ignore-with-comment. | ✓ |
| Explicit individual rule codes | ~80-100 lines; literal no-drift; high maintenance. | |
| Family-level select, pin ruff version | ~5 lines; drift control is process, not config. | |

**User's choice:** Hybrid: family select + audited ignore list.
**Notes:** User asked for a concrete shape comparison before answering;
the concrete-config preview shaped the choice. Targets the actual drift
risk (ruff bumps adding new rules to selected families) without
hand-enumeration burden.

---

## Modernization scope vs Phase 3

### Q1: Where's the boundary between Phase 1 and Phase 3 (REFACTOR-04)?
| Option | Description | Selected |
|--------|-------------|----------|
| Strict minimum-to-green | Phase 1 only fixes what tools fail on. All modernization in Phase 3. | ✓ |
| Strict minimum + 3.9-conditional cleanups | Plus stripping `from __future__ import annotations` etc. tied to 3.9. | |
| Modernization fair game if ruff auto-fixes it | Whatever the chosen ruff families surface. | |
| Claude / planner draws the line | Defer to planner once ruff scope is picked. | |

**User's choice:** Strict minimum-to-green.

### Q2: Should this constrain Claude/research's ruff scope pick?
| Option | Description | Selected |
|--------|-------------|----------|
| Yes — cap ruff scope to non-modernizing families this phase | UP/SIM off-limits; E/F/W/B fair. | ✓ |
| No — accept UP modernization fallout if research picks it | Phase 3 ends up nearly empty. | |
| No — disable modernization rules within UP if it's selected | Family with surgical ignores. | |

**User's choice:** Cap ruff scope to non-modernizing families.

### Q3: `from __future__ import annotations` in cement/utils/fs.py — strip or leave?
| Option | Description | Selected |
|--------|-------------|----------|
| Strip as part of 'drop 3.9' commit | The comment self-flags it as a 3.9 breadcrumb. | |
| Leave it for Phase 3 — strict minimum means strict | Keep boundary bright. | ✓ |
| Claude's discretion at planning time | Planner decides based on count. | |

**User's choice:** Leave it for Phase 3.
**Notes:** Confirms the strict-minimum boundary is enforced literally,
even on a self-flagged TODO comment. This bound also extends to
`cement/core/foundation.py` and any other file using the same import.

---

## Codification details (TOOL-04)

### Q1: Tool pinning strategy for dev deps?
| Option | Description | Selected |
|--------|-------------|----------|
| Compatible-release (~=) for ruff/mypy, floor (>=) for the rest | Hybrid; targets actual drift risk. | ✓ |
| Compatible-release (~=) on everything | Tighter; more pin maintenance. | |
| Floor (>=) on everything (current state) | Lockfile-driven only. | |

**User's choice:** Hybrid pinning strategy.

### Q2: Ruff preview mode — keep on or turn off?
| Option | Description | Selected |
|--------|-------------|----------|
| Turn off — preview = false | Stable rules only; aligns with TOOL-04 no-drift intent. | ✓ |
| Keep on — preview = true | Catches more, but rule definitions can shift. | |
| Off + opt-in specific preview rules | Most disciplined; highest config burden. | |

**User's choice:** Turn off — preview = false.

### Q3: Mypy scope — keep `cement/`-only or expand to `tests/`?
| Option | Description | Selected |
|--------|-------------|----------|
| Keep `cement/`-only | Preserves current scope; strict-minimum-aligned. | ✓ |
| Expand to `tests/` now | Tighter discipline; large fallout. | |
| Claude's discretion | Defer to planner. | |

**User's choice:** Keep `cement/`-only.

### Q4: Should mypy strictness knobs be tightened while we're codifying?
| Option | Description | Selected |
|--------|-------------|----------|
| No — keep current strictness, just bump python_version | Strict-minimum boundary holds. | ✓ |
| Yes — add `strict = true` umbrella now | Implicit drift; contradicts TOOL-04. | |
| Yes — tighten specific knobs (warn_unreachable, disallow_any_generics) | Bounded fallout; expands phase scope. | |

**User's choice:** Keep current strictness, just bump python_version.

---

## Claude's Discretion

- Specific ruff rule families chosen (deferred to research/planner, capped
  per D-07 to non-modernizing families).
- Order of individual rule-family fix commits within Step 2.
- Exact compatible-release minor pin values for ruff and mypy.
- Whether `select` vs `extend-select` reads cleaner in pyproject for the
  chosen family list.

## Deferred Ideas

- `from __future__ import annotations` cleanup → Phase 3 REFACTOR-04.
- Type-hint syntax modernization (`Optional[X]` → `X | None`, etc.)
  → Phase 3 REFACTOR-04.
- Ruff `UP` / `SIM` rule families → Phase 3.
- Mypy expansion to `tests/` → future milestone.
- `strict = true` mypy umbrella → not adopted (implicit-drift hazard).
- Coverage strictness knob review → Phase 3 (COV-01..03).
- Pypy3.10 matrix inclusion → planner-time check, not a Phase 1 decision.
