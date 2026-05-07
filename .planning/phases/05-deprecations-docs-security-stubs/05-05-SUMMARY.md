---
phase: 05-deprecations-docs-security-stubs
plan: 05
subsystem: docs-content-walkthroughs
tags: [docs, readme, contributing, travis, conventional-commits, docs-04-fix-on-find]
requirements_addressed: [DOCS-02, DOCS-04]
dependency_graph:
  requires:
    - "Phase 05 Plan 04 — make docs zero-warnings gate enforced (`-W` flag) — Plan 05 Task 1 verifies `make docs` exits 0 as a smoke test"
    - "Phase 1 Travis CI removal (.travis.yml deleted, CI moved to GitHub Actions) — README's two stale Travis surfaces date to that era"
    - "CLAUDE.md §Commit Conventions — canonical commit-shape doc that CONTRIBUTING.md now back-links via `../CLAUDE.md`"
    - "Active CHANGELOG section: 3.0.15 - DEVELOPMENT (will be released as stable/3.0.16)"
  provides:
    - "README.md is Travis-free (zero `travis-ci` references); badge block shrunk from 3 to 2; More Information list shrunk from 5 to 4"
    - ".github/CONTRIBUTING.md aligned with Conventional Commits + atomic-per-concern discipline; `make commit` named; `[Conventional Commits]` reference link target appended; `../CLAUDE.md` back-link added"
    - "DOCS-02 acceptance: README + CONTRIBUTING walkthroughs accurate against the 3.0.16 release"
    - "DOCS-04 fix-on-find hold-the-line confirmation: 0 hits in `cement/` for `grep -i 'travis|python 3.9|setup.py'` (expected per RESEARCH.md A5; pre-verified 2026-05-07)"
  affects:
    - "External contributor PR experience — Conventional Commits is now explicit in CONTRIBUTING (was implicit via CLAUDE.md only); `make commit` discoverable from the public-facing CONTRIBUTING file"
    - "Public GitHub render of README — no more stale Travis badge suggesting unmaintained or split-CI posture"
    - "DOCS-02 + DOCS-04 — both checked off in REQUIREMENTS.md (DOCS-04 closed via fix-on-find hold-the-line; the load-bearing tightening landed in Plan 01)"
tech_stack:
  added: []
  patterns:
    - "Conventional Commits + atomic-per-concern — established in PROJECT.md / CLAUDE.md / Phase 1-3 commit history; now formalized in the public-facing CONTRIBUTING.md as the contributor-facing discipline"
    - "Reference-link-block append pattern — `[Conventional Commits]: https://www.conventionalcommits.org/` appended as a sibling to the existing `[Open Source Initiative]`, `[issue tracker]`, `[PEP8]`, `[Commit Guidelines]` block (preserves legacy callers; idiomatic Markdown)"
    - "Fix-on-find hold-the-line check — task with explicit zero-hit acceptance is a valid GSD task shape (Task 3 produces no commits when the surface is clean; CHANGELOG: NO ENTRY when no source change ships)"
    - "Atomic-per-file commit shape — each task touches exactly 2 files (source + CHANGELOG.md); 78-char-wrapped commit body; Conventional Commits subject ≤78 chars"
key_files:
  created: []
  modified:
    - README.md
    - .github/CONTRIBUTING.md
    - CHANGELOG.md
decisions:
  - "Both Travis surfaces (README.md:5 badge + README.md:60 list-item link) deleted in a single atomic commit per D-10 strict scope (one commit per file: README + CHANGELOG)."
  - "CONTRIBUTING.md replacement preserved the file's pre-line-33 sections (Welcome / Issue Reporting / Submitting Bug Reports) and the existing reference-link block — only the Guidelines for Code Contributions section + the trailing 'Regarding git commit messages' / ProGit example block were replaced with the Conventional Commits-aligned text per RESEARCH.md Example 9."
  - "The `[Commit Guidelines]` reference link was retained (NOT removed) per plan body — old references to it elsewhere in the doc may still resolve through it, and removing dead reference links is out of D-10 strict scope."
  - "DOCS-04 fix-on-find sweep returned 0 hits as RESEARCH.md A5 pre-verified — Task 3 produced 0 commits and 0 CHANGELOG entries (hold-the-line confirmation only)."
  - "CHANGELOG entry for Task 2 wrapped manually at 78 chars (line 1 = `- \`[docs]\` Align CONTRIBUTING with Conventional Commits +`, line 2 = `  atomic-per-concern`) per plan body's pre-wrap calculation showing the unwrapped form was 79 chars."
  - "`make docs` smoke test (Plan 04's `-W` gate) executed after Task 1 only — no docstring edits in Tasks 2 or 3, so no cumulative `-W` regression risk between commits."
patterns_established:
  - "Public-facing doc walkthroughs (README + CONTRIBUTING) are content-changes — `[docs]` area tag in CHANGELOG (NOT `[dev]`). Distinguishes from build-time discipline changes like Plan 04's `[dev]` Wire -W into make docs entry."
  - "Multi-file doc-walkthrough phase: 2 atomic commits + 2 CHANGELOG entries; single shared 78-char wrap convention; cumulative gates run twice (once per task) AND once final."
  - "GSD task with type=auto + explicit 0-commit acceptance criterion (Task 3) — valid shape when the planning evidence (RESEARCH.md A5) pre-verified 0 hits and the executor's role is hold-the-line confirmation, not body-of-work."
  - "Reference-link append pattern: when a doc rewrite introduces a new `[Foo Bar]` shorthand, append `[Foo Bar]: https://...` to the existing reference-link block at file-bottom rather than adding inline URLs (keeps the doc skim-friendly + idiomatic)."

requirements_completed: [DOCS-02, DOCS-04]

# Metrics
metrics:
  duration_minutes: 5
  duration_seconds: 322
  tasks_completed: 2
  tasks_with_zero_commits: 1
  commits: 2
  files_created: 0
  files_modified: 3
  completed_date: 2026-05-07
---

# Phase 05 Plan 05: README + CONTRIBUTING Walkthroughs (DOCS-02 + DOCS-04 Fix-on-Find) Summary

**One-liner:** Dropped the two Travis CI surfaces from `README.md` (line-5 badge and line-60 More Information list-item link), replaced the conflicting "A single commit per issue" guidance in `.github/CONTRIBUTING.md` with the project's actual current discipline (Conventional Commits + atomic-per-concern + 78-char wrap + `make commit`), and confirmed RESEARCH.md A5's hold-the-line on the DOCS-04 docstring fix-on-find sweep — 2 atomic commits, 2 `[docs]` Misc CHANGELOG entries, 0 commits from the fix-on-find sweep (as expected).

## Outcome

DOCS-02 and DOCS-04 are now SATISFIED. Two atomic Conventional Commits land
the public-facing doc walkthrough alignment with the 3.0.16 release; the
DOCS-04 fix-on-find sweep returned zero hits in `cement/` and produced no
new commits (hold-the-line confirmation per RESEARCH.md A5). All four
gates (`make comply`, `make test`, `make audit-public-api`, `make docs`
with Plan 04's `-W` flag) exit 0 across both commits at 100% coverage
(320/320 tests passing).

## Performance

- **Duration:** ~5 min (322 sec)
- **Started:** 2026-05-07T23:34:14Z
- **Completed:** 2026-05-07T23:39:36Z
- **Tasks:** 3 (2 with commits + 1 hold-the-line confirmation with 0 commits)
- **Commits:** 2 atomic
- **Files:** 0 created, 3 modified (`README.md`, `.github/CONTRIBUTING.md`, `CHANGELOG.md`)

## Tasks Completed

| Task | Name                                                                          | Commit     | Files                                                       |
| ---- | ----------------------------------------------------------------------------- | ---------- | ----------------------------------------------------------- |
| 1    | Drop Travis CI link and badge from README.md (commit 10 of D-16)              | `678ef3ff` | `README.md`, `CHANGELOG.md`                                 |
| 2    | Align CONTRIBUTING.md with Conventional Commits (commit 11 of D-16)           | `60b8955a` | `.github/CONTRIBUTING.md`, `CHANGELOG.md`                   |
| 3    | DOCS-04 fix-on-find docstring sweep verification (commit 12 of D-16)          | _no commit_ | _none — 0 hits, hold-the-line per RESEARCH.md A5_           |

## Files Created/Modified

- **Modified:** `README.md` — line-5 badge `[![Continuous Integration Status](https://app.travis-ci.com/...)](...)` removed; line-60 More Information list-item `- [Travis CI](https://travis-ci.org/datafolklabs/cement/)` removed. Surrounding badges (lines 3-4) and list items (4 remaining) preserved byte-identical. -2 lines net.
- **Modified:** `.github/CONTRIBUTING.md` — Guidelines for Code Contributions section + trailing "Regarding git commit messages" prose + ProGit example block (lines 33-80 in the pre-edit form) replaced with the Conventional Commits-aligned text per RESEARCH.md Example 9. New `### Commit Conventions` subsection with subject/body/type/authoring rules + back-link `[\`CLAUDE.md\`](../CLAUDE.md)`. Reference-link block at bottom preserved + `[Conventional Commits]: https://www.conventionalcommits.org/` appended. "A single commit per issue" line removed.
- **Modified:** `CHANGELOG.md` — 2 `[docs]` lines appended to the `Misc:` bucket of the active `3.0.15 - DEVELOPMENT` section, immediately after the Plan 04 `[dev]` Wire -W entry:
  - `` - `[docs]` Drop Travis CI link/badge (CI moved to GitHub Actions) ``
  - `` - `[docs]` Align CONTRIBUTING with Conventional Commits + `` (line wrap)
    `  atomic-per-concern`

## Verification Evidence

### DOCS-02 (a) — README is Travis-free

```bash
$ ! grep -E 'travis-ci' README.md
# (no output — exit 0; zero travis-ci hits)

$ ! grep -E 'app\.travis-ci\.com' README.md
# (no output — exit 0; zero app.travis-ci.com hits)

$ ! grep -E 'travis-ci\.org' README.md
# (no output — exit 0; zero travis-ci.org hits)
```

### DOCS-02 (b) — README More Information list preserved

```bash
$ grep -E '## More Information' README.md
## More Information

$ sed -n '/## More Information/,/## License/p' README.md | grep -c '^- '
4
```

4 list items remaining (was 5 pre-edit; the Travis CI item was the 4th).

### DOCS-02 (c) — CONTRIBUTING references Conventional Commits + make commit

```bash
$ grep -cE 'Conventional Commits' .github/CONTRIBUTING.md
2

$ grep -c 'make commit' .github/CONTRIBUTING.md
1

$ grep -F '../CLAUDE.md' .github/CONTRIBUTING.md
See [`CLAUDE.md`](../CLAUDE.md) §"Commit Conventions" for the

$ grep -F 'conventionalcommits.org' .github/CONTRIBUTING.md
[Conventional Commits]: https://www.conventionalcommits.org/

$ grep -F '[PEP8]' .github/CONTRIBUTING.md
- Contributors make every effort to comply with [PEP8]
[PEP8]: http://www.python.org/dev/peps/pep-0008/

$ grep -F '[Commit Guidelines]' .github/CONTRIBUTING.md
[Commit Guidelines]: http://git-scm.com/book/en/Distributed-Git-Contributing-to-a-Project#Commit-Guidelines
```

### DOCS-02 (d) — "A single commit per issue" removed

```bash
$ grep -F 'A single commit per issue' .github/CONTRIBUTING.md
# (no output — exit 1; the conflicting line is gone)
```

### DOCS-04 fix-on-find — 0 hits in `cement/` (hold-the-line per RESEARCH.md A5)

```bash
$ grep -rn -i 'travis\|python 3\.9\|setup\.py\b' cement/ --include='*.py'
# (no output — exit 1; zero hits)

$ grep -rn -i 'travis\|python 3\.9\|setup\.py\b' cement/ --include='*.py' | wc -l
0

$ grep -rn -i 'travis\|python 3\.9\|setup\.py' cement/ --include='*.py' | wc -l
0
```

The unbounded variant (`setup.py` without `\b`) also returns 0, matching
the plan's verify automation form. RESEARCH.md A5 (pre-verified
2026-05-07) holds at executor time. **Task 3 produced 0 commits and 0
CHANGELOG entries** — the load-bearing docstring tightening already
landed in Plan 01, and no new stale references were introduced between
research and execution.

### Cumulative gates (final, post-Task 2)

```bash
$ make comply
pdm run ruff check cement/ tests/
All checks passed!
pdm run mypy
Success: no issues found in 51 source files
# exit 0

$ make test
TOTAL                                 3243      0  100.00%
Required test coverage of 100% reached. Total coverage: 100.00%
===================== 320 passed, 1693 warnings in 51.73s ======================
# exit 0

$ make audit-public-api
# exit 0 — public-API surface byte-identical (README.md / CONTRIBUTING.md /
# CHANGELOG.md are not Python modules; AST walker doesn't touch them)

$ rm -rf docs/build && make docs
build succeeded.
DOC: file:///.../docs/build/html/index.html
# exit 0 — Plan 04's -W gate stays clean (no docstring edits in this plan)
```

### CHANGELOG — 2 new Misc entries

```bash
$ git diff c27fda67..HEAD -- CHANGELOG.md | grep -E '^\+- `\[' | wc -l
2
```

(c27fda67 = Plan 04's final commit.)

### Commit attributes

| Task | Commit     | Subject                                                                          | Subject chars | Body wrap | Files                                                                                                                                                       |
| ---- | ---------- | -------------------------------------------------------------------------------- | ------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | `678ef3ff` | `docs(readme): drop Travis CI link (moved to GitHub Actions)`                    | 59            | 78-char   | 2 (`README.md` -2 lines / `CHANGELOG.md` +1 line)                                                                                                           |
| 2    | `60b8955a` | `docs(contributing): align with Conventional Commits + atomic-per-concern`       | 72            | 78-char   | 2 (`.github/CONTRIBUTING.md` +37/-38 / `CHANGELOG.md` +2 lines)                                                                                             |

Both subjects ≤78 chars; both bodies wrapped at 78 chars per CLAUDE.md
commit conventions; both touch exactly 2 files (source + CHANGELOG.md).

## Decisions Made

- **D-10 strict scope held** — README received only the two surgical Travis-surface deletions; no walkthrough verification, no Cement 4 forward-signaling. Surrounding badges, links, and prose preserved byte-identical.
- **CONTRIBUTING replacement scope** — replaced the Guidelines for Code Contributions section AND the trailing "Regarding git commit messages" / ProGit example block (the example block was the substrate for the old "single commit per issue" guidance + the pre-Conventional-Commits format). Pre-line-33 sections (Welcome / Issue Reporting / Submitting Bug Reports) preserved.
- **`[Commit Guidelines]` reference link retained** — old references elsewhere in the doc may still resolve through it; D-10 strict scope says don't proactively prune dead reference links. The `[Conventional Commits]` target was appended as a sibling, not a replacement.
- **CHANGELOG `[docs]` area tag** — both entries are doc-content changes (not build-time discipline like Plan 04's `[dev]` entry). RESEARCH.md Pitfall 7 bucket-per-commit table was followed.
- **Manual 78-char wrap on Task 2 CHANGELOG entry** — the unwrapped form (`` - `[docs]` Align CONTRIBUTING with Conventional Commits + atomic-per-concern ``) was 79 chars; wrapped to two lines per plan body's pre-wrap calculation. The continuation indent (`  ` = 2 spaces) matches the project's existing CHANGELOG bullet-continuation convention.
- **Task 3 hold-the-line — 0 commits is the correct outcome** — RESEARCH.md A5 pre-verified the zero-hit posture on 2026-05-07; the executor-time re-run confirmed it held. Adding a "no-op commit" to record the verification would have been makework with no bisect or audit value.
- **`make docs` smoke test executed once (after Task 1)** — no docstring edits in Tasks 2 or 3, so Plan 04's `-W` gate had no incremental risk. Cumulative gates (comply + test + audit-public-api) ran after both Task 1 and Task 2; final cumulative gates (including `make docs`) ran post-Task 2 to confirm phase-end posture.

## Deviations from Plan

None — plan executed exactly as written.

The plan body's CONTRIBUTING.md replacement spec covered the section
boundaries explicitly (lines 33-80 in the pre-edit form, including the
"Regarding git commit messages" prose + ProGit example block), and the
EXACT REPLACEMENT block was applied byte-for-byte per RESEARCH.md
Example 9. No execution-time reinterpretation needed.

## Issues Encountered

None.

## User Setup Required

None — these are public-facing doc walkthrough changes. No external
service configuration, no environment variables, no secrets. The
`[Conventional Commits]` reference link target is a public URL
(https://www.conventionalcommits.org/) that requires no auth.

## Next Phase Readiness

- DOCS-02 acceptance: README + CONTRIBUTING walkthroughs accurate against the 3.0.16 release. Both files Travis-free; CONTRIBUTING uses Conventional Commits + atomic-per-concern + `make commit` + back-link to CLAUDE.md.
- DOCS-04 acceptance: docstring fix-on-find sweep returns 0 hits in `cement/` (RESEARCH.md A5 hold-the-line confirmed at executor time). Load-bearing tightening landed in Plan 01.
- D-16 steps 10 + 11 closed; step 12 (fix-on-find) closed with 0 commits per RESEARCH.md A5.
- 100% coverage gate held: 3243 stmts / 0 missed across 320 tests.
- `make comply`, `make audit-public-api`, `make docs` (with Plan 04's `-W`) all exit 0 — cumulative phase-end posture is GREEN.
- CHANGELOG Misc bucket has 2 new `[docs]` entries (Travis drop + CONTRIBUTING align), bringing the total of new entries since Plan 04 to 2.
- No blockers carried into Plan 06 (security-audit tooling stub).

## TDD Gate Compliance

N/A — Plan 05 is `type=execute` (not `type=tdd`); all three tasks are `type="auto" tdd="false"` (doc-content edits + a hold-the-line grep verification, no test-first cycle).

## Self-Check: PASSED

**Files verified:**
- FOUND: `README.md` (modified — line-5 badge removed; line-60 list-item removed; surrounding content byte-identical)
- FOUND: `.github/CONTRIBUTING.md` (modified — Guidelines + Commit Conventions sections rewritten per RESEARCH.md Example 9; reference-link block preserved + `[Conventional Commits]` appended)
- FOUND: `CHANGELOG.md` (modified — 2 new `[docs]` lines in `Misc:` bucket)

**Commits verified:**
- FOUND: `678ef3ff` `docs(readme): drop Travis CI link (moved to GitHub Actions)`
- FOUND: `60b8955a` `docs(contributing): align with Conventional Commits + atomic-per-concern`

**Final gate evidence:**
- `make comply` → exit 0 (ruff + mypy clean)
- `make test` → exit 0, 320 passed, 100.00% coverage (3243 stmts, 0 missed)
- `make audit-public-api` → exit 0 (public-API surface byte-identical)
- `make docs` → exit 0 (sphinx-build -W ./source ./build, 0 warnings, build succeeded)
- `grep -E 'travis-ci' README.md` → exit 1 (0 hits)
- `grep -cE 'Conventional Commits' .github/CONTRIBUTING.md` → 2
- `grep -c 'make commit' .github/CONTRIBUTING.md` → 1
- `grep -F 'A single commit per issue' .github/CONTRIBUTING.md` → exit 1 (0 hits)
- `grep -F '../CLAUDE.md' .github/CONTRIBUTING.md` → match
- `grep -F 'conventionalcommits.org' .github/CONTRIBUTING.md` → match
- `grep -rn -i 'travis|python 3.9|setup.py' cement/ --include='*.py' | wc -l` → 0

---
*Phase: 05-deprecations-docs-security-stubs*
*Plan: 05 (README + CONTRIBUTING walkthroughs + DOCS-04 fix-on-find)*
*Completed: 2026-05-07*
