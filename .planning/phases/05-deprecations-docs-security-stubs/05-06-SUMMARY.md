---
phase: 05-deprecations-docs-security-stubs
plan: 06
subsystem: planning-intel-closeout
tags: [planning-artifact, conventions, requirements, secv2, docs-04, sec-01, sec-02, sec-03, phase-close]
requirements_addressed: [DOCS-04, SEC-01, SEC-02, SEC-03]
dependency_graph:
  requires:
    - "Phase 03 Plan 03 — UP cascade landed PEP 604/585 syntax in cement/ source; CONVENTIONS.md prescriptive guidance was already in modern form heading into this plan"
    - "Phase 1 PYVER-01 — pyproject.toml target-version updated to py310 (the source-of-truth this plan syncs the doc example to)"
    - "Phase 02 D-03 + 02-PIP-AUDIT.md — anchor referenced by SECv2-01 expansion (Anchor sub-bullet)"
    - "Phase 05 Plans 01-05 — D-18 conjuncts 1-10 already GREEN heading into this plan"
  provides:
    - ".planning/codebase/CONVENTIONS.md ruff target-version example reflects py310 (matches live pyproject.toml:88)"
    - ".planning/REQUIREMENTS.md SECv2-01..03 are multi-line phase-shaped scope notes per D-14 (6 sub-bullets per stub: Tool, Make target, CI placement, Config, New dev-dep, Exit behavior + Anchor)"
    - "DOCS-04 closeout (planning-intel side); SEC-01/SEC-02/SEC-03 satisfied"
    - "Phase 05 D-18 conjuncts #11 and #12 GREEN — final plan in Phase 5"
  affects:
    - "Future security-tooling milestone — picks up phase-shaped SECv2-01..03 starting points without re-discovery"
    - "Future GSD discuss/plan/research phases reading .planning/codebase/CONVENTIONS.md — sees consistent modern PEP 604/585 form throughout (no stale Dict/List/Optional/Union prescriptions)"
tech_stack:
  added: []
  patterns:
    - "Planning-artifact filter — both commits touch only .planning/ files; per CLAUDE.md Changelog Maintenance + RESEARCH.md Pitfall 7 rows 13/14, NO CHANGELOG entries (planning intel is not user-facing surface)"
    - "Pitfall 6 wholesale-refresh branch — pre-task grep surfaced body-text Dict/List/Optional/Union references in negative-example prose plus one stale active prescription at line 246; took the wholesale-but-minimal path (5 prose tweaks + the line-39 target-version update) over the branch-1 1-line edit"
    - "6-property × 3-stub grep gate — D-14 acceptance shape proven (each of Tool, Make target, CI placement, Config, New dev-dep, Exit behavior matches exactly 3 times across SECv2-01..03; SECv2-04 stays as a one-liner with 0 sub-bullets — distinct concern per D-13)"
key_files:
  created:
    - .planning/phases/05-deprecations-docs-security-stubs/05-06-SUMMARY.md
  modified:
    - .planning/codebase/CONVENTIONS.md
    - .planning/REQUIREMENTS.md
decisions:
  - "Pitfall 6 branch 2 (wholesale refresh) selected over branch 1 (1-line edit). Pre-task grep returned 5 body-text Dict/List/Optional/Union hits (lines 24/25/94/95 negative-example contrast prose; line 246 stale active prescription). Plan body's `<acceptance_criteria>` strict zero-hits gate would have failed with branch 1; Pitfall 6 explicitly authorizes branch 2 (wholesale refresh) when body-text hits surface. Recorded as a Rule 1+2 deviation (auto-fix bug / auto-add missing critical functionality — fixing stale doc surfaces)."
  - "Branch-2 refresh kept minimal: dropped the `— NOT \\`Dict[...]\\`...` and `— NOT \\`Optional[str]\\` or \\`Union[int, str]\\`` negative-example trailers from lines 24/25/94/95, and modernized line 246 (`-> Dict[str, Any]`, `-> List[str]` → `-> dict[str, Any]`, `-> list[str]`). Total diff: 6 insertions / 6 deletions in 1 file (vs the plan author's expected 1 insertion / 1 deletion). Acceptance gate `! grep -nE 'Dict\\[|List\\[|Optional\\[|Union\\['` now returns clean."
  - "SECv2-04 (`SECURITY.md` / disclosure process) intentionally LEFT as a one-liner per D-13 (distinct concern; out of SEC-01..03 scope). Confirmed via `grep -A 1 '^- \\*\\*SECv2-04\\*\\*' .planning/REQUIREMENTS.md | grep -cE '^    -'` → 0 hits."
  - "SECv2-01 Anchor sub-bullet references both `02-CONTEXT.md D-03` and `02-PIP-AUDIT.md` per the D-14 + Pattern Map locked-shape (gives the future milestone two breadcrumbs: the decision-record and the capture-artifact)."
  - "Both commits are planning-artifact edits — NO CHANGELOG entries (CLAUDE.md filter / RESEARCH.md Pitfall 7 rows 13 + 14). Verified post-commit via `git show HEAD --stat | grep -F 'CHANGELOG.md'` → 0 hits on both commits."
  - "Cumulative gates (`make comply`, `make test`, `make audit-public-api`, `make docs`) run AFTER each task's edit and BEFORE each commit. All four exit 0 cleanly twice (once per task). 100% coverage gate held (3243/3243 stmts; 320 passed; 51.7s)."

requirements_completed: [DOCS-04, SEC-01, SEC-02, SEC-03]

# Metrics
metrics:
  duration_minutes: 6
  duration_seconds: 360
  tasks_completed: 2
  tasks_with_zero_commits: 0
  commits: 2
  files_created: 0
  files_modified: 2
  completed_date: 2026-05-07
---

# Phase 05 Plan 06: Planning-intel closeout (CONVENTIONS sync + SECv2-01..03 expansion) Summary

Closed two Phase-3 / Phase-5 planning-intel deferreds in 2 atomic
planning-artifact commits: synced the `.planning/codebase/CONVENTIONS.md`
ruff `target-version` example from `py39` to `py310` (closes Phase 3
D-22 step 5 / DOCS-04 planning-intel side) and expanded the
`.planning/REQUIREMENTS.md` SECv2-01..03 one-liners into multi-line
phase-shaped scope notes per D-14 (closes SEC-01, SEC-02, SEC-03).
Both commits are `.planning/`-only edits — NO CHANGELOG entries per
CLAUDE.md Changelog Maintenance filter / RESEARCH.md Pitfall 7 rows
13/14. This is the final plan in Phase 5.

## Deliverables

### Commits

| Commit | Subject | Files |
|--------|---------|-------|
| `69004fbe` | `docs(codebase): refresh CONVENTIONS to PEP 604/585 syntax` | `.planning/codebase/CONVENTIONS.md` |
| `dc74b2eb` | `docs(05): expand SECv2-01..03 with phase-shaped scope notes` | `.planning/REQUIREMENTS.md` |

### Task 1 — `.planning/codebase/CONVENTIONS.md` diff (D-16 step 13)

Authored as a Pitfall-6 branch-2 wholesale-but-minimal refresh
(rationale in Decisions §1 above). Final diff: 6 insertions / 6
deletions across 5 line groups in 1 file.

```diff
@@ Types section (line ~24)
-- Use **PEP 585 builtin generics** (Python 3.10+): `dict[str, Any]`, `list[str]`, `tuple[int, str]`, `type[Handler]` — NOT `Dict[str, Any]`, `List[str]`, `Tuple[int, str]`, `Type[Handler]`
-- Use **PEP 604 union syntax** (Python 3.10+): `str | None`, `int | str`, `dict[str, Any] | None` — NOT `Optional[str]` or `Union[int, str]`
+- Use **PEP 585 builtin generics** (Python 3.10+): `dict[str, Any]`, `list[str]`, `tuple[int, str]`, `type[Handler]`
+- Use **PEP 604 union syntax** (Python 3.10+): `str | None`, `int | str`, `dict[str, Any] | None`

@@ Ruff Configuration block (line 39)
-target-version = "py39"
+target-version = "py310"

@@ Type Annotations Patterns (lines ~94-95)
-- Use **PEP 585 builtin generics** (Python 3.10+): `dict[str, Any]`, `list[str]`, `tuple[int, str]`, `type[Handler]` — NOT `Dict[str, Any]`, `List[str]`, `Tuple[int, str]`, `Type[Handler]`
-- Use **PEP 604 union syntax** (Python 3.10+): `str | None`, `int | str`, `dict[str, Any] | None` — NOT `Optional[str]` or `Union[int, str]`
+- Use **PEP 585 builtin generics** (Python 3.10+): `dict[str, Any]`, `list[str]`, `tuple[int, str]`, `type[Handler]`
+- Use **PEP 604 union syntax** (Python 3.10+): `str | None`, `int | str`, `dict[str, Any] | None`

@@ Function Design / Return Values (line ~246)
-- Dict/List returns should be typed: `-> Dict[str, Any]`, `-> List[str]`
+- Dict/list returns should be typed: `-> dict[str, Any]`, `-> list[str]`
```

### Task 2 — `.planning/REQUIREMENTS.md` SECv2-01..03 expansion (D-16 step 14)

Authored per RESEARCH.md Example 10 + PATTERNS.md SECv2 expansion
section. SECv2-04 left UNCHANGED per D-13.

**6-property × 3-stub grep gate (D-14 acceptance evidence):**

| Property | Hits across SECv2-01..03 | Expected |
|----------|--------------------------|----------|
| `**Tool:**` | 3 | 3 |
| `**Make target:**` | 3 | 3 |
| `**CI placement:**` | 3 | 3 |
| `**Config:**` | 3 | 3 |
| `**New dev-dep:**` | 3 | 3 |
| `**Exit behavior:**` | 3 | 3 |
| **Total sub-bullets present (6 × 3)** | **18** | **18** |

Plus the optional `**Anchor:**` 7th sub-bullet appears on all three
stubs (SECv2-01 references `02-CONTEXT.md D-03 + 02-PIP-AUDIT.md`;
SECv2-02 + SECv2-03 reference `02-CONTEXT.md D-03`).

**SECv2-04 one-liner preservation evidence:**

```
$ grep -A 1 '^- \*\*SECv2-04\*\*' .planning/REQUIREMENTS.md | grep -cE '^    -'
0
```

(The line below SECv2-04 has zero 4-space-indented sub-bullets,
confirming SECv2-04 stays as the original one-liner per D-13.)

## CHANGELOG Verification (Planning-Artifact Filter)

Both commits intentionally touched ZERO CHANGELOG.md lines per
CLAUDE.md §"Changelog Maintenance" filter rule (planning-artifact
commits do not ship to users) and RESEARCH.md Pitfall 7 rows 13 + 14.

```
$ git show 69004fbe --stat | grep -F 'CHANGELOG.md'
(0 hits)
$ git show dc74b2eb --stat | grep -F 'CHANGELOG.md'
(0 hits)
```

Per-commit file count:
- `69004fbe`: 1 file changed (`.planning/codebase/CONVENTIONS.md`)
- `dc74b2eb`: 1 file changed (`.planning/REQUIREMENTS.md`)

## Cumulative Phase Gate Status (post-plan)

All four cumulative gates exit 0:

| Gate | Status | Evidence |
|------|--------|----------|
| `make comply` | exit 0 | `All checks passed!` (ruff) + `Success: no issues found in 51 source files` (mypy) |
| `make test` | exit 0 | `320 passed, 1693 warnings in 51.66s` + `Required test coverage of 100% reached. Total coverage: 100.00%` (3243/3243 stmts) |
| `make audit-public-api` | exit 0 | EXIT=0 (silent success — public-API baseline byte-identical) |
| `make docs` | exit 0 | `build succeeded.` (Plan 04's `-W` gate active; zero warnings) |

Gates run twice (once per task — after each edit, before each
commit) and once final after both tasks. Each invocation green.

## Phase 5 D-18 Acceptance Criteria Status (final, across all 6 plans)

This is the final plan of Phase 5; the D-18 acceptance shape is the
12-conjunct conjunction defined in `05-CONTEXT.md` lines 350-385.
Status across the entire phase:

| # | Criterion | Status | Closing Plan |
|---|-----------|--------|--------------|
| 1 | `make test` passes at 100% coverage | GREEN | All plans (held continuously) |
| 2 | `make comply` passes (ruff + mypy clean) | GREEN | All plans (held continuously) |
| 3 | `make audit-public-api` exits 0 | GREEN | Plan 03 (string-quote applied without baseline drift) |
| 4 | `make docs` exits 0 with `-W` enabled | GREEN | Plan 04 (`-W` gate wired) |
| 5 | `cement/core/deprecations.py` DEPRECATIONS dict every entry names removal version | GREEN | Plan 01 |
| 6 | `tests/core/test_deprecations.py` + `tests/ext/test_ext_smtp.py:631` still assert each warning fires | GREEN | All plans (no test regression) |
| 7 | Repo root contains `DEPRECATIONS.md` with H2 per ID + GitBook back-link | GREEN | Plan 02 |
| 8 | `README.md` no longer contains `travis-ci.org` / `app.travis-ci.com` | GREEN | Plan 05 |
| 9 | `.github/CONTRIBUTING.md` references "Conventional Commits" + `make commit` | GREEN | Plan 05 |
| 10 | `grep -rn -i 'travis\|python 3\.9' cement/ --include='*.py'` returns no docstring hits | GREEN | Plan 05 (hold-the-line; pre-verified clean) |
| 11 | `.planning/codebase/CONVENTIONS.md` "Type annotations" paragraph uses PEP 604/585 lowercase-builtin syntax | **GREEN** | **Plan 06 (this plan)** |
| 12 | `.planning/REQUIREMENTS.md` SECv2-01..03 are multi-line entries with tool / invocation / CI placement / config / dev-dep / exit behavior | **GREEN** | **Plan 06 (this plan)** |

**All 12 conjuncts GREEN.** Phase 5 D-18 acceptance satisfied.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1+2 — Bug + Missing critical functionality] CONVENTIONS.md wholesale-refresh branch taken instead of 1-line edit branch**

- **Found during:** Task 1 pre-task verification grep
- **Issue:** The plan body declared the edit as "1-line edit" with
  `<acceptance_criteria>` reporting "1 insertion(+), 1 deletion(-)"
  AND a strict zero-hits gate `! grep -nE 'Dict\[|List\[|Optional\[|Union\['`.
  The pre-task grep returned 5 body-text hits — 4 in negative-example
  contrast prose at lines 24, 25, 94, 95 (e.g., "Use ... NOT
  `Dict[...]`...") and 1 stale active prescription at line 246 (`Dict/List
  returns should be typed: \`-> Dict[str, Any]\`, \`-> List[str]\``).
  The two acceptance criteria conflicted; the plan author's "1-line
  edit" framing was based on Pitfall 6 branch 1 (assumes negative-
  example prose is illustrative-and-can-stay), but the plan's own
  zero-hits acceptance gate aligns with Pitfall 6 branch 2 (wholesale
  refresh).
- **Fix:** Took Pitfall 6 branch 2 explicitly per its own text
  ("If the grep returns the body-text Dict/List/etc. references,
  the doc was reverted — do the wholesale refresh"). Removed the
  4 negative-example trailers (kept the prescriptive positive
  guidance intact) and modernized the line-246 active prescription
  (`Dict/List` → `Dict/list`; `-> Dict[str, Any]` → `-> dict[str, Any]`;
  `-> List[str]` → `-> list[str]`). Plus the line-39 `py39` → `py310`
  sync (the original target). Final diff: 6 insertions / 6 deletions
  in 1 file. Pre-commit grep now returns clean (only line 39 hits
  `target-version`; zero hits for `Dict\[|List\[|Optional\[|Union\[`).
- **Files modified:** `.planning/codebase/CONVENTIONS.md`
- **Commit:** `69004fbe`
- **Acceptance criteria impact:** Satisfies the strict zero-hits gate
  AND the "exactly 1 file" gate AND `target-version = "py310"` gate.
  Does NOT satisfy the literal "1 insertion / 1 deletion" expectation
  (final stat: 6 / 6) — but that expectation was based on the plan
  author's incorrect read of the live doc, and the zero-hits gate
  takes precedence as the END-STATE the plan wants.

### Auth Gates

None.

### Architectural Decisions Required

None — Pitfall 6 branch 2 is an authorized fallback within the plan
(not a Rule-4 architectural escalation; the plan body explicitly
documents it as the alternative path under "If body-text hits
surface...").

## Key Patterns Established

- **Planning-artifact filter discipline (CLAUDE.md / Pitfall 7):**
  Both commits are `.planning/`-only edits; the `docs(codebase): ...`
  and `docs(05): ...` Conventional-Commit subjects are themselves the
  GSD planning-artifact convention. Verified post-commit via
  `git show HEAD --stat | grep -F 'CHANGELOG.md'` → 0 hits on both.
- **Pitfall 6 branch 2 (wholesale-but-minimal refresh):** When pre-task
  grep surfaces body-text legacy-syntax references not anticipated by
  the plan author's 1-line-edit framing, take the authorized fallback
  branch with minimum-impact prose tweaks (drop negative-example
  trailers; modernize active prescriptions). Document as Rule 1+2
  deviation. Final diff stays small (6/6).
- **6-property × 3-stub grep gate (D-14):** Generalizable D-14 acceptance
  shape for multi-stub structured-bullet REQUIREMENTS.md expansions —
  each property must match exactly N times where N = number of stubs
  (here 3). The `awk '/^- \*\*FIRST\*\*/,/^- \*\*LAST\*\*/'` range +
  `grep -cE '\*\*Property:\*\*'` per-property invocation idiom is
  greppable, deterministic, and survives line-number drift.
- **SECv2 stub Anchor breadcrumb shape:** `02-CONTEXT.md D-03 +
  02-PIP-AUDIT.md` for SECv2-01 (decision-record + capture-artifact);
  `02-CONTEXT.md D-03` alone for SECv2-02/03 (decision-record only —
  the bandit and SAST stubs don't have a Phase-2 capture artifact yet).

## Self-Check: PASSED

**Files verified:**
- FOUND: `.planning/codebase/CONVENTIONS.md` (modified)
- FOUND: `.planning/REQUIREMENTS.md` (modified)
- FOUND: `.planning/phases/05-deprecations-docs-security-stubs/05-06-SUMMARY.md` (this file)

**Commits verified (`git log --oneline -3`):**
- FOUND: `69004fbe docs(codebase): refresh CONVENTIONS to PEP 604/585 syntax`
- FOUND: `dc74b2eb docs(05): expand SECv2-01..03 with phase-shaped scope notes`

**Acceptance gates verified:**
- `grep -F 'target-version = "py310"' .planning/codebase/CONVENTIONS.md` — matches at line 39
- `grep -F 'target-version = "py39"' .planning/codebase/CONVENTIONS.md` — 0 hits
- `grep -nE 'Dict\[|List\[|Optional\[|Union\[' .planning/codebase/CONVENTIONS.md` — 0 hits
- 6-property × 3-stub grep — 18 hits across SECv2-01..03 (3 each)
- SECv2-04 sub-bullet count — 0
- `02-PIP-AUDIT.md` Anchor breadcrumb — present (2 occurrences)
- `pdm run pip-audit` — present
- `make comply && make test && make audit-public-api && make docs` — all exit 0
- Both commits — 0 CHANGELOG.md hits in `git show --stat`
- Both subjects ≤78 chars (57 + 59)
