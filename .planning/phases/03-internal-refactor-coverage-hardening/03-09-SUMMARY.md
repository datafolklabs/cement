---
phase: 03-internal-refactor-coverage-hardening
plan: 09
subsystem: utils.fs / dev.audit-script / verification-artifact
tags: [bc-restoration, regression-tests, audit-script, gap-closure, wave-9]
requires: [03-08]
provides:
  - "cement.utils.fs:abspath() BC contract restored (symlink preservation + silent ~user fallthrough)"
  - "Two regression tests pinning the BC contract"
  - "Audit script portable across non-UTF-8 locales"
  - "03-VERIFICATION.md W-01/W-02 marked RESOLVED with empirical evidence"
affects:
  - "cement/utils/fs.py (1 line + boundary tag)"
  - "tests/utils/test_fs.py (+43 lines, 2 new tests, sys import added)"
  - "scripts/audit-public-api.py (1 line — encoding kwarg)"
  - "CHANGELOG.md (2 new Bugs entries)"
  - ".planning/phases/03-internal-refactor-coverage-hardening/03-VERIFICATION.md (W-01/W-02 resolution sub-blocks, frontmatter timestamp, Wave 9 audit row)"
tech-stack:
  added: []
  patterns:
    - "inline `# boundary: D-14 (CR-01/CR-02)` tag co-located with `os.path` callsite on the public surface (D-12 / D-14 boundary discipline; matches `cement/core/foundation.py:53` precedent)"
    - "TDD-style sanity check via temporary revert: confirmed both new regression tests FAIL against the Wave 6 pathlib body and PASS against the restored stdlib body"
key-files:
  created: []
  modified:
    - "cement/utils/fs.py"
    - "tests/utils/test_fs.py"
    - "scripts/audit-public-api.py"
    - "CHANGELOG.md"
    - ".planning/phases/03-internal-refactor-coverage-hardening/03-VERIFICATION.md"
decisions:
  - "Single-line body revert + inline boundary tag (NOT a wider pathlib rollback): the boundary discipline for cement/core/{config,foundation,template}.py is preserved unchanged because those are non-public-surface internals; only fs.py:abspath reverts because it is on 03-PUBLIC-API-BASELINE.txt and downstream callers depend on the os.path semantics."
  - "TDD sanity-check via temporary revert chosen over pre-Task-1 RED commit pattern: Task 2 used cp + sed to verify both new tests FAIL against the Wave 6 body, then restored the Task 1 fix. This proves the tests pin the BC contract without polluting git history with a known-failing commit."
  - "CHANGELOG `[utils.fs]` and `[dev]` area prefixes per CLAUDE.md Changelog Maintenance policy. Both entries land in the active 3.0.15 DEVELOPMENT Bugs bucket (fix: -> Bugs)."
metrics:
  duration: "12 min"
  completed: "2026-05-04T05:37:24Z"
  tasks: 5
  files: 5
  commits: 5
---

# Phase 03 Plan 09: Wave 9 Gap Closure (CR-01, CR-02, WR-02) Summary

Restore 3.0.x BC contract on `cement.utils.fs:abspath` (symlink
preservation + silent unknown-`~user` fallthrough) plus
audit-script encoding portability. Five atomic commits; all 9
D-24 conjuncts re-verified GREEN; W-01/W-02 marked RESOLVED.

## What Changed

| Task | Type | File | Net Change | Commit |
|------|------|------|-----------:|--------|
| 1 | fix | `cement/utils/fs.py` | 1 line (body revert + `# boundary: D-14` tag) | `52248e1d` |
| 2 | test | `tests/utils/test_fs.py` | +43 lines, 2 new tests, `import sys` | `25983a57` |
| 3 | fix | `scripts/audit-public-api.py` | 1 line (encoding kwarg) | `cc50a3e3` |
| 4 | docs | `CHANGELOG.md` | +9 lines (2 Bugs entries) | `e31f88d7` |
| 5 | docs | `.planning/phases/03-internal-refactor-coverage-hardening/03-VERIFICATION.md` | +68 lines (W-01/W-02 RESOLVED, Wave 9 row, ts bump) | `4a767d00` |

## D-24 9-Conjunct Re-Verification (Post-Fix)

| # | Gate | Command | Expected | Result | Status |
|---|------|---------|---------:|-------:|:------:|
| 1 | Tests + 100% coverage | `make test` | 318 passed, 100.00% (3241/3241 stmts) | **318 passed, 100.00% coverage 3241/3241 stmts** | **GREEN** |
| 2 | Lint clean | `make comply-ruff` | exit 0; All checks passed! | **All checks passed!** | **GREEN** |
| 3 | Type clean | `make comply-mypy` | exit 0; Success: no issues found in 51 source files | **Success: no issues found in 51 source files** | **GREEN** |
| 4 | Public-API audit | `make audit-public-api` | exit 0, empty diff vs 934-line baseline | **exit 0, silent (empty diff)** | **GREEN** |
| 5 | Coverage HTML | `ls coverage-report/index.html` | present, non-zero size | **25733 bytes, present** | **GREEN** |
| 6 | `Any` count | `grep -nE ': Any\b\|-> Any\b\|Any\]' cement/core/*.py \| wc -l` | 40 (unchanged from Wave 8) | **40** | **GREEN** |
| 7 | Locked-vocab pragma | filtered grep for unauthorized labels | 0 lines | **0** | **GREEN** |
| 8 | `os.path` scoped (untagged) | `grep -rn 'os\.path' cement/utils/fs.py cement/core/{foundation,template,config}.py \| grep -v '# boundary:' \| wc -l` | 0 (Task 1's `# boundary: D-14` inline tag filters out the restored `return` line) | **0** | **GREEN** |
| 9 | `from __future__ import annotations` | `grep -rn 'from __future__ import annotations' cement/` | 0 matches | **0** | **GREEN** |

**All 9 conjuncts GREEN.** Test count: 316 → 318 (+2 regression
tests). `Any` count, pragma vocabulary, scoped `os.path`, and
future-annotations grep all unchanged from Wave 8 baseline.

## Empirical CR-01 / CR-02 Reproductions (Pre-Fix vs Post-Fix)

### CR-01 — `fs.abspath()` symlink preservation

**Pre-fix (Wave 6 body, `_Path(p).expanduser().resolve(strict=False)`):**

```
input:   /tmp/<tmpdir>/link  (link -> target)
result:  /tmp/<tmpdir>/target  (FOLLOWED symlink — BC-break)
FAIL
```

**Post-fix (restored stdlib body, `os.path.abspath(os.path.expanduser(path))`):**

```
input:   /tmp/tmp9vskqq8r/link  (link -> target)
result:  /tmp/tmp9vskqq8r/link  (preserved — BC contract restored)
PASS
```

### CR-02 — `fs.abspath()` unknown `~user` silent fallthrough

**Pre-fix (Wave 6 body):**

```
input:   '~nosuchuser_xyz_phase03_gap/foo'
result:  RuntimeError: Could not determine home directory.   (Path.expanduser raises)
FAIL
```

**Post-fix (restored stdlib body):**

```
input:    ~nosuchuser_xyz_phase03_gap/foo
result:   /Users/.../~nosuchuser_xyz_phase03_gap/foo  (no RuntimeError)
expected: /Users/.../~nosuchuser_xyz_phase03_gap/foo
PASS
```

Both reproductions executed against the live Python 3.14 +
post-fix tree. The new regression tests
(`tests/utils/test_fs.py::test_abspath_preserves_symlinks` and
`::test_abspath_unknown_user_does_not_raise`) pin both
behaviors. TDD-style sanity check during Task 2 confirmed both
tests FAIL against a temporary revert to the Wave 6 body.

## Public API Baseline Diff

`make audit-public-api` exit 0 with **empty diff** against
`03-PUBLIC-API-BASELINE.txt` (934 lines) post-fix. No public
symbols added, removed, or changed signature. The
`cement.utils.fs:abspath` symbol at baseline line 839 is
byte-identical pre- and post-fix.

## Test Count + Coverage

- **Pre-Wave-9:** 316 passed at 100.00% coverage (3241/3241 stmts)
- **Post-Wave-9:** 318 passed at 100.00% coverage (3241/3241 stmts)
- **Delta:** +2 tests (`test_abspath_preserves_symlinks` +
  `test_abspath_unknown_user_does_not_raise`); **0** stmt
  delta (the new tests exercise existing executable code paths
  in `fs.py:abspath` already at 100% coverage).
- **Coverage gate:** held at 100% across all 5 commits.

## CHANGELOG.md Entries (Verbatim)

Appended to `## 3.0.15 - DEVELOPMENT` Bugs bucket:

```
- `[utils.fs]` Restore `os.path` semantics in `abspath()` —
  preserves symlink paths and silently falls through on unknown
  `~user` prefixes (regression introduced by the Phase 03 Wave 6
  pathlib migration; restores 3.0.x BC contract on the public
  `cement.utils.fs:abspath` surface)
- `[dev]` Use explicit `encoding='utf-8'` in
  `scripts/audit-public-api.py` so the
  `make audit-public-api` regression gate is portable across
  non-UTF-8 locales (Windows cp1252, locale-stripped Docker, etc.)
```

## 03-VERIFICATION.md Final State

- **Frontmatter `verified:`** bumped from
  `2026-05-04T04:26:40Z` → `2026-05-04T05:34:56Z`.
- **`status:`** retained as `passed` (user disposition was
  fix-now / disposition #1, not defer / disposition #2 or
  override / disposition #3).
- **`score:`** retained `9/9 D-24 conjuncts GREEN` (re-verified
  post-fix).
- **W-01 RESOLVED sub-block** appended under the original
  W-01 finding (CR-01 + CR-02): records 5 commit SHAs in a
  table, re-runs both empirical reproductions with PASS
  output, names both regression tests, confirms test count
  316 → 318 at 100% coverage.
- **W-02 RESOLVED sub-block** appended under the original
  W-02 finding (audit-script encoding): records `cc50a3e3`
  fix commit, confirms `make audit-public-api` continues to
  exit 0 with empty diff vs the 934-line baseline.
- **Phase 3 Commit Audit table** gains a Wave 9 row (4 source/
  test/changelog commits + 1 docs verification commit). Total
  commits bumped 82 → 87.

The original W-01 and W-02 blocks are NOT deleted — Resolution
sub-blocks are appended underneath, preserving the original
verifier-audit reasoning + recommended dispositions for forensic
auditability.

## Deviations from Plan

**None — plan executed exactly as written.**

All 5 tasks landed in order with the exact commit subjects
specified in the plan (with one minor wording tweak: Task 1's
subject reads `fix(utils.fs): preserve symlinks and silent
~user fallthrough` — dropped trailing `in abspath()` to keep
the subject line under 78 chars per CLAUDE.md). Boundary tag
applied inline on the `return` line (Task 1) on the first
edit; D-24 conjunct #8 stayed GREEN throughout — no follow-up
boundary-tag commit needed. CHANGELOG entries appended at the
end of the existing Bugs bucket; `Features:` header preserved
unchanged. 03-VERIFICATION.md original W-01/W-02 blocks
preserved; Resolution sub-blocks appended.

## Phase 03 BC Contract Status

`cement.utils.fs:abspath` BC contract on the 3.0.x track:
**RESTORED**.

- **Symlink preservation:** restored (CR-01 closed)
- **Silent ~user fallthrough:** restored (CR-02 closed)
- **Audit-script encoding portability:** fixed (WR-02 closed)
- **Public API signature:** byte-identical (audit gate empty diff)
- **All 7 phase requirements:** SATISFIED (REFACTOR-01..04 +
  COV-01..03; no regression)
- **All 5 ROADMAP Phase 3 success criteria:** SATISFIED
- **All 9 D-24 conjuncts:** GREEN
- **Test count:** 318/318 passing at 100.00% coverage

**Phase 03 ready to merge to `main`.** The Wave 9 gap closure
is the last outstanding item from the verifier audit; the
`status: passed` verdict in 03-VERIFICATION.md now reflects
the live post-fix tree with full BC compatibility on the
public `fs.abspath` surface.

## Self-Check: PASSED

**Files claimed created/modified — all verified:**

- `cement/utils/fs.py` — FOUND (modified, 1 line + boundary tag)
- `tests/utils/test_fs.py` — FOUND (modified, +43 lines)
- `scripts/audit-public-api.py` — FOUND (modified, 1 line)
- `CHANGELOG.md` — FOUND (modified, +9 lines)
- `.planning/phases/03-internal-refactor-coverage-hardening/03-VERIFICATION.md` — FOUND (modified, +68 lines)

**Commits claimed — all verified in git log:**

- `52248e1d` `fix(utils.fs): preserve symlinks and silent ~user fallthrough` — FOUND
- `25983a57` `test(utils.fs): cover symlink preservation and unknown-~user` — FOUND
- `cc50a3e3` `fix(dev.audit-script): explicit UTF-8 encoding in audit script` — FOUND
- `e31f88d7` `docs(changelog): record fs.abspath BC fix + audit script encoding` — FOUND
- `4a767d00` `docs(03): record Wave 9 gap closure (CR-01, CR-02, WR-02)` — FOUND

All claims verified against the live post-fix tree.
