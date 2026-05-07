---
phase: 05-deprecations-docs-security-stubs
plan: 03
subsystem: deprecations-in-repo-narrative
tags: [deprecations, docs, repo-root, gitbook, markdown]
requirements_addressed: [DEPREC-02]
dependency_graph:
  requires:
    - "Phase 05 Plan 01 — DEPRECATIONS dict entries pinned to Cement v3.2.0 (commits dedacccb, 3f809b90, 059fab38)"
    - "Phase 05 Plan 02 — sphinx warnings cleared (no markdown impact, but signals Wave 3 readiness)"
    - "Active CHANGELOG section: 3.0.15 - DEVELOPMENT (will be released as stable/3.0.16)"
  provides:
    - "Top-level repo-root DEPRECATIONS.md (sibling of README.md, CHANGELOG.md, CONTRIBUTORS.md)"
    - "4 H2 sections — one per DEPRECATIONS dict ID (3.0.8-1, 3.0.8-2, 3.0.10-1, 3.0.16-1)"
    - "Locked 5-element block format (Surface / Since / Removal / migration prose / GitBook back-link)"
    - "Dotted GitBook anchors (#3.0.8-1) matching cement/core/deprecations.py:15 deprecate() runtime URL convention"
  affects:
    - "Phase 05 closing — DEPREC-02 acceptance closed for the in-repo touchpoint deliverable"
    - "Future deprecation additions — new IDs append at the bottom under their since-version section per the established convention"
tech_stack:
  added: []
  patterns:
    - "Repo-root developer-narrative markdown (sibling of README.md / CHANGELOG.md / CONTRIBUTORS.md, no frontmatter, H1 + H2 structure)"
    - "GitBook back-link convention: dotted-version anchor (#3.0.8-1, NOT GitHub-slugified #3-0-8-1) — matches the runtime DeprecationWarning URL emitted by cement.core.deprecations.deprecate()"
    - "Per-deprecation locked block: H2 (id) → Surface / Since / Removal bold-labelled lines → migration prose with optional fenced code block → GitBook back-link"
key_files:
  created:
    - DEPRECATIONS.md
  modified:
    - CHANGELOG.md
decisions:
  - "Wrote DEPRECATIONS.md verbatim per plan body — no reinterpretation needed at execution time. CONTEXT.md D-05/D-06 reinterpretation (Sphinx is strictly API reference; developer narrative lives on GitBook) was already settled at planning time."
  - "Anchor format used dotted (#3.0.8-1) per Pitfall 8 — verified 0 GitHub-slugified anchors via grep `release-information/deprecations#3-0-`."
  - "Used Misc: bucket per RESEARCH.md Pitfall 7 table (modest scope; new file but documentation-mirror, not user-visible feature). Sibling Plan 02 also uses [docs] in Misc:, so the pattern is consistent across the active 3.0.15 - DEVELOPMENT section."
  - "Did NOT modify docs/source/deprecations.rst — the literal REQUIREMENTS.md DEPREC-02 wording said `a dedicated docs/source/deprecations.rst page`, but CONTEXT.md D-05/D-06 explicitly reinterprets the medium because Sphinx is strictly API reference per docs/source/index.rst note. The repo-root DEPRECATIONS.md is the in-repo touchpoint; GitBook (off-band, hand-authored by user) is the canonical developer narrative."
patterns_established:
  - "`DEPRECATIONS.md` joins README.md / CHANGELOG.md / CONTRIBUTORS.md as a top-level repo-root markdown sibling — convention is no frontmatter, H1 title, H2 sections."
  - "GitBook back-link anchor format = dotted version (`#3.0.8-1`). DO NOT GitHub-slugify (`#3-0-8-1`) — must match the runtime URL emitted by `cement.core.deprecations.deprecate()` so users land on the same anchor whether they follow the DeprecationWarning URL or the in-repo back-link."
  - "Future deprecation additions: append a new H2 block at the bottom under its since-version section. Block layout is locked at 5 elements (Surface / Since / Removal / migration prose / GitBook back-link)."

requirements_completed: [DEPREC-02]

# Metrics
metrics:
  duration_minutes: 2.5
  duration_seconds: 152
  tasks_completed: 1
  commits: 1
  files_created: 1
  files_modified: 1
  completed_date: 2026-05-07
---

# Phase 05 Plan 03: Top-Level DEPRECATIONS.md Summary

**One-liner:** Created `DEPRECATIONS.md` at the repo root with one H2 section per DEPRECATIONS dict ID (4 total) using the locked 5-element block format and dotted GitBook back-link anchors — DEPREC-02 acceptance closed for the in-repo touchpoint deliverable.

## Outcome

DEPREC-02 acceptance is now SATISFIED via the repo-root in-repo touchpoint
(per CONTEXT.md D-05/D-06 reinterpretation of the literal "docs/source/deprecations.rst"
wording — Sphinx is strictly API reference per `docs/source/index.rst`; free-form
developer narrative lives on GitBook at `docs.builtoncement.com`). One atomic commit
landed under D-16 step 4, touching exactly 2 files (`DEPRECATIONS.md` + `CHANGELOG.md`),
with a Conventional Commits subject (35 chars, well under the 78-char cap) and a
78-char-wrapped body. All three gates (`make comply`, `make audit-public-api`,
`make test`) exited 0 at 100% coverage (320/320 tests passing).

## Performance

- **Duration:** ~2.5 min
- **Started:** 2026-05-07T23:22:48Z
- **Completed:** 2026-05-07T23:25:20Z
- **Tasks:** 1 atomic commit
- **Files:** 1 created (`DEPRECATIONS.md`), 1 modified (`CHANGELOG.md`)

## Tasks Completed

| Task | Name                                                                          | Commit     | Files                            |
| ---- | ----------------------------------------------------------------------------- | ---------- | -------------------------------- |
| 1    | Create DEPRECATIONS.md with 4 H2 blocks (commit 4 of D-16)                    | `1c9606b7` | `DEPRECATIONS.md`, `CHANGELOG.md`|

## Files Created/Modified

- **Created:** `DEPRECATIONS.md` — 84 lines / 2169 bytes / md5 `66bfad02e553c8e610da82a5d325c833`. Contains H1 (`# Cement Deprecations`) + intro paragraph + 4 H2 blocks (one per DEPRECATIONS dict ID, ordered by since-version ascending: 3.0.8-1, 3.0.8-2, 3.0.10-1, 3.0.16-1). No frontmatter (matches sibling `CHANGELOG.md` / `CONTRIBUTORS.md` / `README.md` repo-root convention).
- **Modified:** `CHANGELOG.md` — single `[docs]` line appended to the `Misc:` bucket of the active `3.0.15 - DEVELOPMENT` section (line 331): `` - `[docs]` Add top-level DEPRECATIONS.md mirroring GitBook narrative ``.

## Verification Evidence

### File-level acceptance — DEPREC-02 in-repo touchpoint

```bash
$ test -f DEPRECATIONS.md && echo "exists"
exists

$ wc -l DEPRECATIONS.md
84 DEPRECATIONS.md                  # ≥60 required

$ grep -cE '^# Cement Deprecations' DEPRECATIONS.md
1                                   # H1

$ grep -cE '^## 3\.0\.' DEPRECATIONS.md
4                                   # one H2 per registry ID

$ grep -cE '^## 3\.0\.8-1' DEPRECATIONS.md
1
$ grep -cE '^## 3\.0\.8-2' DEPRECATIONS.md
1
$ grep -cE '^## 3\.0\.10-1' DEPRECATIONS.md
1
$ grep -cE '^## 3\.0\.16-1' DEPRECATIONS.md
1
```

### Locked 5-element block format

```bash
$ grep -cE '\*\*Surface:\*\*' DEPRECATIONS.md
4
$ grep -cE '\*\*Since:\*\*' DEPRECATIONS.md
4
$ grep -cE '\*\*Removal:\*\*' DEPRECATIONS.md
4
$ grep -cF 'Cement v3.2.0' DEPRECATIONS.md
4                                   # one Removal: line per ID
```

### Pitfall 8 — anchor format dotted (NOT GitHub-slugified)

```bash
$ grep -cE 'docs\.builtoncement\.com/release-information/deprecations#3\.0\.[0-9]+-[0-9]+' DEPRECATIONS.md
4                                   # ≥4 required (one back-link per ID)

$ grep -cE 'release-information/deprecations#3-0-' DEPRECATIONS.md
0                                   # MUST be 0 — no GitHub-slugified anchors
```

The anchor format matches the runtime URL emitted by
`cement/core/deprecations.py:15`:
```
f"...{msg}. See: https://docs.builtoncement.com/release-information/deprecations#{deprecation_id}"
```
where `deprecation_id` is the dotted form (`3.0.8-1`, etc.).

### ID set parity with the runtime DEPRECATIONS dict

```bash
$ diff \
    <(grep -oE "'3\\.0\\.[0-9]+-[0-9]+'" cement/core/deprecations.py | sort -u) \
    <(grep -oE '^## 3\\.0\\.[0-9]+-[0-9]+' DEPRECATIONS.md \
        | sed 's/^## //' \
        | awk '{print "'\''"$0"'\''"}' \
        | sort -u)
# (no output — exit 0; ID sets are identical)

$ # The 4 IDs in cement/core/deprecations.py:DEPRECATIONS:
#   '3.0.8-1', '3.0.8-2', '3.0.10-1', '3.0.16-1'
# are byte-for-byte the same set as the 4 H2 anchors in DEPRECATIONS.md.
```

### CHANGELOG entry

```bash
$ grep -nF '`[docs]` Add top-level DEPRECATIONS.md mirroring GitBook narrative' CHANGELOG.md
331:- `[docs]` Add top-level DEPRECATIONS.md mirroring GitBook narrative
```

The entry sits in the `Misc:` bucket of the active `3.0.15 - DEVELOPMENT` section, immediately after the four sibling `[docs]` entries from Plan 02.

### Cumulative gates

```bash
$ make comply
pdm run ruff check cement/ tests/
All checks passed!
pdm run mypy
Success: no issues found in 51 source files

$ make audit-public-api
# exit 0 — public-API surface byte-identical (DEPRECATIONS.md is repo-root
# markdown, not a Python module; AST walker doesn't touch it)

$ make test
...
TOTAL                                 3243      0  100.00%
Required test coverage of 100% reached. Total coverage: 100.00%
===================== 320 passed, 1693 warnings in 51.73s ======================
```

### Commit attributes

- **Subject:** `docs: add top-level DEPRECATIONS.md` (35 chars; well under 78-char cap)
- **Body:** 78-char-wrapped per CLAUDE.md commit conventions
- **Files touched:** exactly 2 (`DEPRECATIONS.md` + `CHANGELOG.md`)
- **Insertions:** 85 (+84 new file, +1 CHANGELOG)
- **Deletions:** 0

## Decisions Made

- **No reinterpretation needed at execution time** — CONTEXT.md D-05/D-06 had already reinterpreted the literal REQUIREMENTS.md DEPREC-02 wording ("a dedicated docs/source/deprecations.rst page") at planning time. Plan body specified the exact file content verbatim; this plan is mechanical-write-only.
- **Anchor format dotted, not slugified** — Verified via grep that `release-information/deprecations#3-0-` returns 0 hits. Dotted form (`#3.0.8-1`) matches the runtime URL emitted by `cement/core/deprecations.py:15` (Pitfall 8 satisfied).
- **`Misc:` bucket over `Features:`** — Per RESEARCH.md Pitfall 7 table guidance, this is a documentation-mirror addition (modest scope, not a user-visible feature). Sibling Plan 02 also placed its 4 `[docs]` entries in `Misc:`, so the convention holds across the active 3.0.15 - DEVELOPMENT section.
- **`docs/source/deprecations.rst` deliberately NOT created** — DEPREC-02's literal wording said "a dedicated docs/source/deprecations.rst page". CONTEXT.md D-05/D-06 reinterprets this because Sphinx is strictly API reference per `docs/source/index.rst` ("This is the **api** documentation. ... Free-form developer/contribution narrative lives at https://docs.builtoncement.com (GitBook)."). The repo-root `DEPRECATIONS.md` is the in-repo touchpoint; GitBook is the canonical narrative.

## Deviations from Plan

None — plan executed exactly as written.

The plan body's automated verify grep `grep -F '[docs] Add top-level DEPRECATIONS.md mirroring GitBook narrative' CHANGELOG.md` returns exit 1 against the live CHANGELOG because actual entries follow the project convention of wrapping the area tag in backticks (`` `[docs]` `` not `[docs]`). The `<acceptance_criteria>` block names the literal as `` - \`[docs]\` Add top-level DEPRECATIONS.md mirroring GitBook narrative `` which is the form actually written. The grep in the `<verify>` block is missing the backticks — interpreted as a doc-only typo (the acceptance_criteria is the source of truth) and resolved by following the project convention. Verified via `grep -F '` `` `[docs]` Add top-level DEPRECATIONS.md mirroring GitBook narrative` `` ` CHANGELOG.md` returns line 331 successfully.

## Issues Encountered

None.

## User Setup Required

None — this is a docs-only plan. No external service configuration, no environment variables, no secrets.

## Next Phase Readiness

- DEPREC-02 acceptance: in-repo touchpoint exists with one H2 section per registry ID; per-block format = surface, since, removal, migration prose with code example, GitBook back-link.
- D-16 step 4 closed (the 4th of the D-16 enumerated commits across Phase 05).
- ID set parity verified: 4 dict IDs ↔ 4 markdown H2 anchors, byte-for-byte identical.
- Anchor convention established: dotted-version (`#3.0.8-1`). Future plans adding new deprecation IDs append a new H2 block at the bottom of `DEPRECATIONS.md` under the appropriate since-version section.
- 100% coverage gate held: 3243 stmts / 0 missed across 320 tests.
- `make audit-public-api` exit 0 — public-API surface byte-identical (markdown is not a Python module).
- No blockers carried into Plan 04+.

## TDD Gate Compliance

N/A — Plan 03 is `type=execute` (not `type=tdd`); the single task is `type="auto" tdd="false"` (markdown content edit + CHANGELOG append, no test-first cycle).

## Self-Check: PASSED

**Files verified:**
- FOUND: `DEPRECATIONS.md` (created, 84 lines, 2169 bytes)
- FOUND: `CHANGELOG.md` (modified — `[docs] Add top-level DEPRECATIONS.md` entry at line 331)

**Commits verified:**
- FOUND: `1c9606b7` `docs: add top-level DEPRECATIONS.md`

**Final gate evidence:**
- `make comply` → exit 0 (ruff + mypy clean)
- `make audit-public-api` → exit 0 (public-API surface byte-identical)
- `make test` → exit 0, 320 passed, 100.00% coverage (3243 stmts, 0 missed)
- 4 H2 anchors in `DEPRECATIONS.md` ≡ 4 IDs in `cement/core/deprecations.py:DEPRECATIONS` (diff exit 0)
- 0 GitHub-slugified anchors (`#3-0-`) in `DEPRECATIONS.md`
- 4 dotted GitBook back-links matching the runtime URL convention

---
*Phase: 05-deprecations-docs-security-stubs*
*Plan: 03 (top-level DEPRECATIONS.md)*
*Completed: 2026-05-07*
