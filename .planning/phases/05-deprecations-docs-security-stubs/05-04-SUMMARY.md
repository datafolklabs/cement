---
phase: 05-deprecations-docs-security-stubs
plan: 04
subsystem: docs-build-discipline
tags: [docs, sphinx, makefile, audit-point, zero-warnings-gate]
requirements_addressed: [DOCS-01]
dependency_graph:
  requires:
    - "Phase 05 Plan 02 — sphinx warnings cleared (4 known warnings resolved at commits 3712fe91, cbf42b27, 4e7f9a5c, ae6a6036, ca1ea3b1) — pre-flight gate prerequisite"
    - "Active CHANGELOG section: 3.0.15 - DEVELOPMENT (will be released as stable/3.0.16)"
    - "AUDIT POINT comment-style precedent (Phase 1 D-08 / Phase 2 D-10/D-11/D-12 / Phase 3 D-06)"
  provides:
    - "Makefile docs: target now invokes `sphinx-build -W ./source ./build` — zero-warnings gate enforced (not aspirational)"
    - "AUDIT POINT (Phase 5 D-09) comment block in Makefile mirroring pyproject.toml convention — every deliberate-configuration site grep-able from `Makefile` AND `pyproject.toml`"
    - "DOCS-01 acceptance closed: future Sphinx warnings now fail the local docs build"
  affects:
    - "All future Phase 05 plans + downstream maintenance — `make docs` is now fail-fast on any new warning"
    - "Phase 05 D-09 closeout — gate-flip per CONTEXT.md is enforced rather than aspirational"
    - "AUDIT POINT inventory grep — extends from 6 sites (pyproject.toml only) to 7 sites (pyproject.toml + Makefile)"
tech_stack:
  added: []
  patterns:
    - "Makefile recipe AUDIT POINT comment — TAB-prefixed shell-style `# AUDIT POINT (Phase N D-NN): <rationale>` block matching pyproject.toml's TOML-style precedent (same parenthetical phase-reference grammar, same wrap discipline)"
    - "sphinx-build CLI grammar discipline: `-W` flag inserted between command and source/build positionals (matches `sphinx-build [OPTIONS] SOURCE BUILD` shape)"
    - "Zero-warnings build gate (per-tool family) — joins coverage gate (Phase 2 D-10/D-11) + ruff/mypy gates (Phase 1 D-08 / Phase 3 D-06) as a deliberate-configuration anchor"
key_files:
  created: []
  modified:
    - Makefile
    - CHANGELOG.md
decisions:
  - "Plan body specified the exact AFTER recipe verbatim (Makefile:62-69 with -W flag + 4-line AUDIT POINT comment); no execution-time reinterpretation needed."
  - "Pre-flight gate (Pitfall 5) verified: clean `pdm run sphinx-build ./docs/source ./docs/build` returns 0 warnings before flipping `-W`. Plan 02's posture holds — flipping is safe."
  - "AUDIT POINT parenthetical = `(Phase 5 D-09)` matching the Phase N D-NN grammar already present at pyproject.toml:68 (`Phase 2 D-12`), pyproject.toml:79 (`Phase 2 D-10/D-11`), pyproject.toml:180 (`D-08+D-11`), pyproject.toml:102 (`D-08, Phase 03 D-06`). Convention is `Phase N` (zero-pad on Phase 03+, no zero-pad on Phase 1/2/5 — matches the directory-name conventions across `.planning/phases/`)."
  - "CHANGELOG entry uses `[dev]` area tag (NOT `[docs]`) — this is a build-time discipline change (zero-warnings gate), not a doc-content change. Per RESEARCH.md Pitfall 7 bucket-per-commit table."
  - "Entry placed in Misc: bucket of the active `3.0.15 - DEVELOPMENT` section, immediately after the sibling `[docs]` entries from Plan 02 and the Plan 03 `[docs]` entry — matches the established 3.0.15 changelog ordering convention."
  - "`-W` is local-only this phase. CI integration of `make docs` is deferred to a future milestone per CONTEXT.md `<deferred>`."
patterns_established:
  - "AUDIT POINT comments now span both `pyproject.toml` (6 sites — coverage measurement boundary, coverage fail_under, ruff extend-select, ruff lint ignore, ruff per-file-ignores, mypy strictness knobs) and `Makefile` (1 site — docs zero-warnings gate). The grep `grep -nE 'AUDIT POINT' Makefile pyproject.toml` enumerates every deliberate-configuration site across the repo (7 sites total post-Phase 5)."
  - "Build-time hardening + AUDIT POINT comment is a generalizable pattern. Future zero-X gates (e.g., zero-PYTHONWARNINGS, zero-coverage-warnings) follow the same shape: flip the gate, add a 4-line AUDIT POINT comment with phase-reference parenthetical, append a single `[dev]` Misc: changelog entry."
  - "Pre-flight gate before flipping a zero-X gate (Pitfall 5) — always verify the underlying surface is zero-X-clean before flipping the enforcement flag, otherwise the flip itself becomes the regression. Mirrors Phase 1 D-04 one-commit-per-rule-family discipline."

requirements_completed: [DOCS-01]

# Metrics
metrics:
  duration_minutes: 1
  duration_seconds: 46
  tasks_completed: 1
  commits: 1
  files_created: 0
  files_modified: 2
  completed_date: 2026-05-07
---

# Phase 05 Plan 04: Wire -W into make docs (Zero-Warnings Gate) Summary

**One-liner:** Flipped the `make docs` recipe from `sphinx-build ./source ./build` to `sphinx-build -W ./source ./build` (treat warnings as errors) with a 4-line `AUDIT POINT (Phase 5 D-09)` comment matching the pyproject.toml convention — DOCS-01 acceptance closed; future Sphinx warnings now fail the local docs build.

## Outcome

DOCS-01 acceptance is now SATISFIED. Plan 02 (D-16 steps 5-8) resolved all 4 known
sphinx warnings; this commit makes that posture **enforced** (build-error on any
new warning) rather than aspirational. One atomic commit landed under D-16 step 9
touching exactly 2 files (`Makefile` + `CHANGELOG.md`), with a Conventional Commits
subject (54 chars, well under the 78-char cap) and a 78-char-wrapped body. All
three gates (`make comply`, `make audit-public-api`, `make test`) exited 0 at 100%
coverage (320/320 tests passing); `make docs` exits 0 with the new `-W` flag.

## Performance

- **Duration:** ~46 sec
- **Started:** 2026-05-07T23:30:08Z
- **Completed:** 2026-05-07T23:30:54Z
- **Tasks:** 1 atomic commit
- **Files:** 0 created, 2 modified (`Makefile`, `CHANGELOG.md`)

## Tasks Completed

| Task | Name                                                                          | Commit     | Files                            |
| ---- | ----------------------------------------------------------------------------- | ---------- | -------------------------------- |
| 1    | Wire -W into make docs + AUDIT POINT comment (commit 9 of D-16)               | `c27fda67` | `Makefile`, `CHANGELOG.md`       |

## Files Created/Modified

- **Modified:** `Makefile` — `docs:` recipe (lines 62-70) now contains a 4-line
  AUDIT POINT comment block (`# AUDIT POINT (Phase 5 D-09): -W enforces zero
  docs warnings.` etc.) plus the `-W` flag inserted between `sphinx-build` and
  `./source` (matches `sphinx-build [OPTIONS] SOURCE BUILD` CLI grammar). The
  trailing `@echo` lines (`@echo`, `@echo DOC: "file://"...`, `@echo`) are
  byte-identical to the pre-edit form.
- **Modified:** `CHANGELOG.md` — single `[dev]` line appended to the `Misc:`
  bucket of the active `3.0.15 - DEVELOPMENT` section (line 332):
  `` - `[dev]` Wire -W into make docs (zero-warnings gate) ``.

## Verification Evidence

### Pre-flight gate (Pitfall 5 — verify Plan 02 prerequisite holds)

```bash
$ rm -rf docs/build && pdm run sphinx-build ./docs/source ./docs/build 2>&1 | grep -ic warning
0
```

Plan 02's posture holds: 0 warnings on a clean sphinx-build before the `-W` flip.

### Acceptance criterion: -W flag wired

```bash
$ grep -F 'sphinx-build -W ./source ./build' Makefile
	cd docs; pdm run sphinx-build -W ./source ./build; cd ..
```

### Acceptance criterion: un-flagged form removed (no half-state)

```bash
$ grep -F 'sphinx-build ./source ./build' Makefile
# (no output — exit 1; un-flagged form gone)
```

### Acceptance criterion: AUDIT POINT (Phase 5 D-09) parenthetical present

```bash
$ grep -F 'AUDIT POINT (Phase 5 D-09)' Makefile
	# AUDIT POINT (Phase 5 D-09): -W enforces zero docs warnings.
```

### Acceptance criterion: trailing @echo DOC line preserved (byte-identical)

```bash
$ grep -F 'DOC: "file://"' Makefile
	@echo DOC: "file://"$$(echo `pwd`/docs/build/html/index.html)
```

### Acceptance criterion: make docs exits 0 with -W enabled

```bash
$ rm -rf docs/build && make docs 2>&1 | tail -10
writing additional pages... search done
dumping search index in English (code: en)... done
dumping object inventory... done
build succeeded.

The HTML pages are in build.

DOC: file:///src/cement/docs/build/html/index.html

# exit 0
```

The recipe printed the `# AUDIT POINT ...` comment lines as part of the make
trace (because Makefile recipe lines starting with `#` are still echoed by make
unless silenced with `@`), and `pdm run sphinx-build -W ./source ./build`
completed with `build succeeded.` and exit 0.

### AUDIT POINT inventory across the repo

```bash
$ grep -nE 'AUDIT POINT' Makefile pyproject.toml
Makefile:63:	# AUDIT POINT (Phase 5 D-09): -W enforces zero docs warnings.
pyproject.toml:68:# AUDIT POINT (Phase 2 D-12): explicit measurement boundary mirrors
pyproject.toml:79:# AUDIT POINT (Phase 2 D-10/D-11): fail_under = 100 is the absolute
pyproject.toml:102:# AUDIT POINT (D-08, Phase 03 D-06): re-review on every ruff bump. New
pyproject.toml:125:    # AUDIT POINT (D-08): each entry MUST have a one-line justification.
pyproject.toml:145:# AUDIT POINT (D-08): per-file-ignores require one-line justification.
pyproject.toml:180:# AUDIT POINT (D-08+D-11): strictness knobs are deliberately enumerated,
$ grep -nE 'AUDIT POINT' Makefile pyproject.toml | wc -l
       7
```

7 deliberate-configuration sites total (1 Makefile + 6 pyproject.toml) — every
zero-X gate, lint family, type-check strictness knob, and coverage measurement
boundary is grep-able from a single command.

### CHANGELOG entry

```bash
$ grep -nF '`[dev]` Wire -W into make docs (zero-warnings gate)' CHANGELOG.md
332:- `[dev]` Wire -W into make docs (zero-warnings gate)
```

The entry sits in the `Misc:` bucket of the active `3.0.15 - DEVELOPMENT`
section, immediately after the sibling `[docs]` entry from Plan 03 (line 331).

### Cumulative gates

```bash
$ make comply
pdm run ruff check cement/ tests/
All checks passed!
pdm run mypy
Success: no issues found in 51 source files

$ make audit-public-api
# exit 0 — public-API surface byte-identical (Makefile / CHANGELOG.md are not
# Python modules; AST walker doesn't touch them)

$ make test
...
TOTAL                                 3243      0  100.00%
Required test coverage of 100% reached. Total coverage: 100.00%
===================== 320 passed, 1693 warnings in 51.70s ======================
```

### Commit attributes

- **Subject:** `chore(make): wire -W into make docs (zero-warnings gate)` (54 chars; well under 78-char cap)
- **Body:** 78-char-wrapped per CLAUDE.md commit conventions
- **Files touched:** exactly 2 (`Makefile` + `CHANGELOG.md`)
- **Insertions:** 6 (+5 Makefile, +1 CHANGELOG)
- **Deletions:** 1 (-1 Makefile, the un-flagged sphinx-build line)

## Decisions Made

- **Plan body specified the exact recipe verbatim** — Makefile EXACT BEFORE/AFTER blocks were lifted directly from the plan; no execution-time reinterpretation needed. The 4-line AUDIT POINT comment block, the `-W` flag position (between `sphinx-build` and `./source` per the sphinx CLI grammar), and the `(Phase 5 D-09)` parenthetical were all pre-specified.
- **Pre-flight gate executed before the flip** — Pitfall 5 is non-negotiable: flipping `-W` while warnings still emit would have made the flip itself the regression. Verified `grep -ic warning` returns 0 on a clean sphinx-build before staging the Makefile mutation.
- **`[dev]` area tag (NOT `[docs]`) for the CHANGELOG entry** — per plan body and RESEARCH.md Pitfall 7 bucket-per-commit table, this is a build-time discipline change (zero-warnings gate), not a doc-content change. Sibling Plan 02 + Plan 03 used `[docs]` for content additions; this one is correctly distinguished.
- **`Misc:` bucket placement** — same convention as the surrounding 3.0.15 - DEVELOPMENT entries; new line 332 immediately follows the Plan 03 `[docs]` entry on line 331.
- **CI integration of `make docs` deferred** — per CONTEXT.md `<deferred>`, `-W` is local-only this phase. The build-time gate fires on every developer run; CI wiring is a future-milestone concern that does not block DOCS-01 acceptance.

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None — this is a build-discipline change. No external service configuration, no environment variables, no secrets.

## Next Phase Readiness

- DOCS-01 acceptance: `make docs` runs `sphinx-build -W` and exits 0 with all 4 known warnings cleared (Plan 02 prerequisite) and the gate enforced (Plan 04).
- D-16 step 9 closed (the 9th of the D-16 enumerated commits across Phase 05).
- AUDIT POINT inventory now spans both `Makefile` and `pyproject.toml` — 7 sites total, all grep-able from a single command.
- 100% coverage gate held: 3243 stmts / 0 missed across 320 tests.
- `make audit-public-api` exit 0 — public-API surface byte-identical (build artifacts are not Python modules).
- No blockers carried into Plan 05 (cement/utils/version.py PEP 440 / dunder-version stub) or Plan 06 (security-audit tooling stub).

## TDD Gate Compliance

N/A — Plan 04 is `type=execute` (not `type=tdd`); the single task is `type="auto" tdd="false"` (Makefile recipe edit + CHANGELOG append, no test-first cycle).

## Self-Check: PASSED

**Files verified:**
- FOUND: `Makefile` (modified — `docs:` recipe now has 4-line AUDIT POINT comment block at lines 63-66 + `-W` flag at line 67; trailing `@echo` lines preserved at lines 68-70)
- FOUND: `CHANGELOG.md` (modified — `[dev] Wire -W into make docs (zero-warnings gate)` entry at line 332)

**Commits verified:**
- FOUND: `c27fda67` `chore(make): wire -W into make docs (zero-warnings gate)`

**Final gate evidence:**
- `make docs` → exit 0 (sphinx-build -W ./source ./build, 0 warnings, build succeeded)
- `make comply` → exit 0 (ruff + mypy clean)
- `make audit-public-api` → exit 0 (public-API surface byte-identical)
- `make test` → exit 0, 320 passed, 100.00% coverage (3243 stmts, 0 missed)
- `grep -nE 'AUDIT POINT' Makefile pyproject.toml | wc -l` → 7 (1 Makefile + 6 pyproject.toml)
- `grep -F 'sphinx-build ./source ./build' Makefile` → exit 1 (un-flagged form removed)
- `grep -F 'sphinx-build -W ./source ./build' Makefile` → exit 0 (flagged form present)

---
*Phase: 05-deprecations-docs-security-stubs*
*Plan: 04 (wire -W into make docs)*
*Completed: 2026-05-07*
