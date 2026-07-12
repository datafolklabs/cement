# Cement

## What This Is

Cement is a mature, extensible Python CLI application framework built around a handler/interface/extension pattern. It gives Python developers a batteries-included foundation for building CLI apps — argument parsing, config, logging, output rendering, plugins, hooks, and lifecycle management — while staying pluggable enough to swap any piece. This initiative kicks off GSD-driven modernization and long-term maintenance of the Cement 3 line.

## Core Value

**Cement 3 stays solid, secure, performant, and bug-free under strict backward compatibility — while being continuously maintained against a modern Python and tooling ecosystem.** When tradeoffs arise, stability of the public API wins over everything else; anything that would break a downstream user's app without consent is out of bounds for 3.0.x and 3.2.x release cuts.

## Requirements

### Validated

<!-- Inferred from existing codebase — Cement 3 is mature and shipped. -->

- ✓ Handler/Interface pattern for pluggable components — existing
- ✓ Core handlers: arg, config, log, output, cache, controller, extension, plugin, template, mail — existing
- ✓ Extensions system (`cement/ext/`) with `load(app)` convention — existing
- ✓ Hook system with pre/post lifecycle events and weight-based ordering — existing
- ✓ Meta-class configuration pattern via MRO merging — existing
- ✓ `App` / `TestApp` lifecycle (setup / run / close) — existing
- ✓ Argparse-based controller with nested sub-commands — existing
- ✓ CLI code generator (`cement generate`) with templates — existing
- ✓ Signal handling and application reloading — existing
- ✓ 100% test coverage + PEP8 (ruff) + mypy compliance gates — existing
- ✓ PDM-based dependency management — existing
- ✓ Sphinx documentation — existing
- ✓ Python 3.9–3.14 support matrix (current) — existing
- ✓ Python 3.10–3.14 support matrix (3.9 dropped per EOL policy) — Validated in Phase 01: tooling-baseline-python-matrix
- ✓ Tooling baseline at current pins (ruff ~=0.15.12, mypy ~=1.20.2, pytest>=9.0.3, pytest-cov>=7.1.0, coverage>=7.13.5) — Validated in Phase 01: tooling-baseline-python-matrix
- ✓ No-implicit-drift codification (AUDIT POINT comments in pyproject.toml; explicit ruff `extend-select` + `preview = false`; mypy strictness knobs enumerated) — Validated in Phase 01: tooling-baseline-python-matrix
- ✓ All 5 `cement generate` templates (project, script, extension, plugin, todo-tutorial) modernized to pdm-backend packaging, fully typed, and `make comply` + `make test` green out of the box; enforced by the CI cli-smoke-test matrix — Validated in Phase 05.3 (resolves #735)

### Active

<!-- v1 = Milestone 1: "Clean & Green" — ships as Cement 3.0.16 (dev = 3.0.15 in git). -->

- [x] **Tooling baseline current**: latest ruff, mypy, pytest, pytest-cov; all lint + type errors resolved — Validated in Phase 01
- [ ] **Dependencies current**: unblock the stalled PDM auto-update pipeline; pin/resolve CVEs if any
- [ ] **CI pipeline green**: all matrix jobs passing across supported Python versions; PDM auto-update resumes without drowning in lint
- [x] **Python 3.9 dropped per EOL policy**: floor raised to 3.10; Python matrix = 3.10–3.14 — Validated in Phase 01
- [ ] **Test coverage held at 100%**: every change lands with tests; coverage gate remains absolute
- [x] **Docs build healthy**: Sphinx builds cleanly; no broken refs; contributor docs accurate — Validated in Phase 05 (4+1 warnings cleared; `make docs -W` enforces zero-warnings; CONTRIBUTING aligned with Conventional Commits)
- [ ] **GitHub issue backlog triaged**: batch close stale/wontfix/duplicate with user approval; label survivors; spin real bugs into fix-phases
- [ ] **Internal-only refactor**: dead code removed, type hints tightened, modern stdlib idioms (pathlib, contextlib helpers, `cached_property`) — no public API changes, no architectural shifts. Cement 4 is unscoped and stays that way during this milestone.
- [x] **Deprecation warnings added (warn-only)**: surfaces emit `DeprecationWarning` now; actual removals are scheduled for 3.2.0 — Validated in Phase 05 (DEPRECATIONS dict pinned to v3.2.0; repo-root `DEPRECATIONS.md` added; runtime warning formatting fixed)
- [x] **Audit-tooling stub**: backlog item captured for pip-audit / bandit / SAST — spec'd but not implemented this milestone — Validated in Phase 05 (REQUIREMENTS.md SECv2-01..03 expanded with phase-shaped scope notes)
- [ ] **Release cut: Cement 3.0.16**: tagged release, changelog, PyPI publish

### Out of Scope

- **Breaking public API changes** — reserved for 3.2.0 (next breakage-allowed minor) and 4.0 (nuclear rewrite). This milestone is strictly non-breaking on the 3.0.x track.
- **Major architectural shifts** — even 3.2.0 avoids these; architectural rework is a Cement 4 concern only.
- **Cement 4 scoping / rewrite work** — separate future effort, zero backward-compat constraints when it happens.
- **New features beyond maintenance** — this is a modernization and tech-debt milestone; feature work defers to later milestones.
- **Security-audit tooling rollout (pip-audit, bandit, semgrep/codeql)** — stubbed as a backlog item for a later milestone; not implemented now.
- **Removing anything currently deprecated** — only adding new deprecation warnings this cycle; removals land in 3.2.0.
- **Performance optimization pass** — not anchor-priority this milestone; performance is a Core Value guarantee but lives in a later dedicated milestone unless a regression surfaces during Clean & Green.

## Context

**Codebase posture:** Cement 3 is mature. A codebase map already exists in `.planning/codebase/` (ARCHITECTURE, STACK, STRUCTURE, CONVENTIONS, TESTING, INTEGRATIONS, CONCERNS) and should be treated as authoritative for current-state facts.

**What sparked this milestone:**
- Growing backlog of stale GitHub issues with no triage capacity.
- A scheduled GitHub Actions job runs `pdm update` regularly, but the pipeline has gone stale — each run surfaces a mountain of new lint errors (primarily from ruff updates), so updates stop landing.
- General tech debt has crept in because attention has been elsewhere.
- Cement 3 is effectively in long-term maintenance mode: the major-version bucket for big changes is Cement 4, so Cement 3 needs to be a trustworthy, solid line that downstream apps can pin to with confidence.

**Versioning convention:**
- Cement follows an **odd/even minor-version** convention: odd minors (`3.1.x`) are development/in-flight; even minors (`3.0.x`, `3.2.x`) are released/stable.
- Patch versions inside a stable minor also follow the convention: odd patch in git = dev, even patch = released. Current git HEAD targets `3.0.15` (dev); next tagged release is `3.0.16`.
- `3.0.x` track = **no breakage** — patches, internal changes, deprecation warnings only.
- `3.2.x` track (later milestone) = breakage allowed, but no major architectural shifts.
- `4.0` = total rewrite, no compatibility concerns.

**GSD workflow posture:** This is the first project run through GSD on Cement. The codebase is already mapped (skipping `/gsd-map-codebase`). Research is optional; for a maintenance milestone on a mature framework, domain research is likely low value but a short best-practices scan on Python packaging/CI-hygiene in 2026 may pay off.

**Downstream users:** Cement is a framework — the consumers are other Python apps that depend on `cement`. Backward compatibility is the product, not just a nicety. Every internal change must assume unknown third-party extensions are subclassing our internals.

## Constraints

- **Compatibility**: Zero public-API breakage on the 3.0.x track — including subclass-exposed internals that downstream extensions may rely on. Deprecation warnings OK; removals go to 3.2.0 at the earliest.
- **Tech stack**: Python 3.10–3.14 after this milestone (3.9 dropped per upstream EOL policy). PDM for dependencies. No new runtime dependencies for the core framework — extensions may add optional deps.
- **Quality gates**: 100% test coverage, PEP8 via ruff, mypy type-checking — all absolute. Every phase must leave these at green.
- **Dependencies — core**: Core framework must remain zero-runtime-dependency. Optional extras handled via `[project.optional-dependencies]`.
- **Release gating**: No release cut until all phases pass, CI is green on the full Python matrix, and the issue backlog is at a known clean state.
- **Policy — Python support**: Drop Python versions on upstream EOL date. Standing rule, enforced in this milestone by dropping 3.9.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Anchor priority: Clean & Green first (lint/types/deps/CI/coverage) | Stalled update pipeline is blocking everything else; unblock the baseline before chasing security/performance pillars | — Pending |
| Deprecations OK in 3.0.x; removals move to 3.2.0 | Preserves strict no-breakage on stable track while still communicating Cement 4 intent to users | — Pending |
| Internal refactor is cleanup-only — no Cement 4 architectural seams | Cement 4 is unscoped; introducing seams for an undefined target risks locking in premature decisions and constitutes architectural change, which is out of bounds on 3.0.x. A future Cement 4 milestone gets a clean slate. | — Pending |
| GitHub issues triaged in batch-approve mode | User-reviewed bulk triage balances throughput against accuracy on issues that may have real signal buried in the pile | — Pending |
| Python 3.9 dropped this milestone (EOL Oct 2025) | Standing project policy: drop at upstream EOL. Internal/dev matrix change, not treated as public-API breakage | ✓ Done — Phase 01 |
| Release cut as Cement 3.0.16 | Even-patch convention for stable release; current dev in git = 3.0.15 (odd) | — Pending |
| Security audit tooling (pip-audit/bandit/SAST) stubbed, not implemented | Adding tooling while the lint baseline is already red would multiply noise; revisit once CI is green | — Pending |
| 100% coverage gate stays absolute | Non-negotiable for a framework; relaxing the gate erodes downstream confidence | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-07-12 after Phase 05.3 completion (modernize-project-template-packaging-and-type-all-cli-generated-templates; resolves #735)*
