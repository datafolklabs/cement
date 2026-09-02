# Roadmap: Cement

## Milestones

- ✅ **3.0.16 Clean & Green** — Phases 1–6 (+ 5 inserted decimal phases) — SHIPPED 2026-07-13
- 📋 **Next milestone** — not yet defined (run `/gsd-new-milestone`)

## Phases

<details>
<summary>✅ 3.0.16 Clean & Green (Phases 1–6) — SHIPPED 2026-07-13</summary>

Full archive: [milestones/3.0.16-ROADMAP.md](milestones/3.0.16-ROADMAP.md)

- [x] Phase 1: Tooling Baseline & Python Matrix (5/5 plans) — completed 2026-04-30
- [x] Phase 01.1: Generated Project Template Build Modernization (1/1 plans, INSERTED) — completed 2026-04-30
- [x] Phase 2: Dependencies & CI Pipeline (8/8 plans) — completed 2026-05-02
- [x] Phase 3: Internal Refactor & Coverage Hardening (8/8 plans) — completed 2026-05-04
- [x] Phase 4: Backlog Triage (manual pass outside GSD; 04-NOTE.md) — completed 2026-05-05
- [x] Phase 5: Deprecations, Docs & Security Stubs (7/7 plans) — completed 2026-05-08
- [x] Phase 05.1: ext.generate select-mode feature prompt UX + Jinja boolean fixes #782 (4/4 plans, INSERTED) — completed 2026-05-24
- [x] Phase 05.2: ext.argparse command self-meta accessor #670 (1/1 plans, INSERTED) — completed 2026-06-24
- [x] Phase 05.3: Modernize project template packaging + type all CLI templates (6/6 plans, INSERTED) — completed 2026-07-11
- [x] Phase 05.4: GitHub Actions Release Workflow (5/5 plans, INSERTED) — completed 2026-07-12
- [x] Phase 6: Release Cut 3.0.16 (5/5 plans) — completed 2026-07-13

</details>

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
| ----- | --------- | -------------- | ------ | --------- |
| 1. Tooling Baseline & Python Matrix | 3.0.16 | 5/5 | Complete | 2026-04-30 |
| 01.1 Generated Project Template Build Modernization | 3.0.16 | 1/1 | Complete | 2026-04-30 |
| 2. Dependencies & CI Pipeline | 3.0.16 | 8/8 | Complete | 2026-05-02 |
| 3. Internal Refactor & Coverage Hardening | 3.0.16 | 8/8 | Complete | 2026-05-04 |
| 4. Backlog Triage | 3.0.16 | manual | Complete | 2026-05-05 |
| 5. Deprecations, Docs & Security Stubs | 3.0.16 | 7/7 | Complete | 2026-05-08 |
| 05.1 ext.generate typed variables (#782) | 3.0.16 | 4/4 | Complete | 2026-05-24 |
| 05.2 ext.argparse self-meta accessor (#670) | 3.0.16 | 1/1 | Complete | 2026-06-24 |
| 05.3 Template packaging + typing modernization | 3.0.16 | 6/6 | Complete | 2026-07-11 |
| 05.4 GitHub Actions Release Workflow | 3.0.16 | 5/5 | Complete | 2026-07-12 |
| 6. Release Cut 3.0.16 | 3.0.16 | 5/5 | Complete | 2026-07-13 |

## Backlog

Parking lot for post-3.0.16 (next-milestone) work. Items use `999.x` numbering,
are unsequenced, and stay out of the active phase sequence until promoted via
`/gsd-review-backlog`.

### Phase 999.1: Pydantic Settings config handler (#674) (BACKLOG)

**Goal:** Add a new **additive, optional** config handler extension backed by
[Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
(`cement/ext/ext_pydantic.py`), implementing `ConfigInterface` and registered as
a `config` handler alongside the existing configparser (default) / yaml / json
handlers. Gated behind a new optional extra (`pydantic = ["pydantic-settings"]`)
so the core stays zero-dependency. Fully typed (mypy strict), 100% test coverage,
ruff-clean, with Sphinx API docs, a GitBook narrative note, and a `[ext.pydantic]`
CHANGELOG entry.
**Requirements:** TBD (promote to derive REQ IDs)
**Plans:** 0 plans
**Source:** https://github.com/datafolklabs/cement/issues/674 (open; author derks; low priority by design)
**Scope note:** NEW feature — out of scope for the v1.0 "Clean & Green"
maintenance milestone (PROJECT.md Out of Scope: "New features beyond maintenance
… defers to later milestones"); Phase 6 is the release cut. Deferred to the next
milestone. The issue's stated prerequisite ("effort toward adding typing across
Cement") is satisfied by Phases 05.x. Additive and BC-safe, so it fits a future
3.0.x or 3.2.x line. See `.planning/phases/999.1-pydantic-settings-config-handler-674/999.1-NOTE.md`
for technical shape and open design questions.

Plans:

- [ ] TBD (promote with /gsd-review-backlog when ready)

### Phase 999.2: Cross-OS CI gates — Windows/macOS test portability (BACKLOG)

**Goal:** Re-enable the two cross-OS gate jobs shipped (commented out) in
`gates.yml` during Phase 05.4 — `test-core-windows` and `cli-smoke-native` —
and make `tests/core` pass on Windows. `cli-smoke-native` was verified GREEN
on all four legs (macOS/Windows × Python 3.10/3.14) before being parked;
`test-core-windows` surfaced ~6 genuine portability failures in
`tests/core/test_foundation.py` (assertions hardcode POSIX paths like
`/another/path` that Windows normalizes to `D:\another\path`). Fix the test
assertions to be platform-aware, uncomment both jobs, and confirm green on PR
CI. The repo has never had Windows/macOS CI, so this is a strict coverage
addition — deliberately deferred so the first automated release doesn't gate
on a brand-new OS matrix.
**Requirements:** extends D-14 (deferred from Phase 05.4)
**Plans:** 0 plans
**Source:** Phase 05.4 PR #792 debut CI run (2026-07-12)
**Scope note:** Also consider here: authenticated Docker Hub pulls (or GHCR
mirrors) for the `test-all` compose services if the anonymous-pull flake
recurs (one occurrence 2026-07-12, passed on retry).

Plans:

- [ ] TBD (promote with /gsd-review-backlog when ready)


---
*Roadmap created: 2026-04-24*
*Milestone 3.0.16 archived: 2026-07-13 — see milestones/3.0.16-ROADMAP.md*
