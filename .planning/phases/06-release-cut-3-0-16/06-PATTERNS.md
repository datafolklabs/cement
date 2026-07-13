# Phase 6: Release Cut 3.0.16 - Pattern Map

**Mapped:** 2026-07-12
**Files analyzed:** 5 (2 source edits, 1 runbook checkoff, 2 GSD artifacts)
**Analogs found:** 4 / 5 (announcement copy has no in-repo analog — first automated release)

> **Phase character:** This phase RUNS pre-built release machinery; it authors
> almost no code. The only executable source edits are a one-line VERSION tuple
> bump and CHANGELOG.md finalization. "Analogs" here are therefore prior release
> conventions (previous CHANGELOG sections, the version tuple's own shape, prior
> `*-VERIFICATION.md` reports) — not controllers/services/components. The planner
> should treat "copy the pattern" literally: match the established header/tuple
> forms byte-for-byte, because downstream automation parses them.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `cement/core/backend.py` | config (version-of-record) | transform (bump) | `scripts/bump_dev_version.py` `_render_backend()` + current tuple | exact |
| `CHANGELOG.md` | doc (release notes, parsed by CI) | transform (finalize) | `## 3.0.14 - May 5, 2025` section | exact |
| `.planning/.../05.4-PROVISIONING.md` (checkoff) | runbook | request-response (verify + check off) | `05.4-05-SUMMARY.md` checkpoint pattern | role-match |
| `.planning/.../06-VERIFICATION.md` | GSD artifact | batch (requirement flip + evidence) | `05.4-VERIFICATION.md` | exact |
| `.planning/.../06-ANNOUNCEMENT.md` (or similar) | doc (announcement copy) | transform (derive from changelog) | — | no analog |

## Pattern Assignments

### `cement/core/backend.py` (config / version-of-record, transform)

**Analog:** the file's own current single line + `scripts/bump_dev_version.py`
regex that rewrites it (do NOT run the script — hand-edit; Pitfall 2).

**Current state** (`cement/core/backend.py` line 3 — the ENTIRE file is 3 lines):
```python
"""Cement core backend module."""

VERSION = (3, 0, 15, 'final', 0)  # pragma: nocover  # version constant
```

**Target edit** (change the third tuple element ONLY; preserve the trailing
pragma + comment exactly — the script and mypy both depend on this shape):
```python
VERSION = (3, 0, 16, 'final', 0)  # pragma: nocover  # version constant
```

**Single-source-of-truth invariant** (RESEARCH REL-01): `pyproject.toml` reads
this via `[tool.pdm.version] source="call" getter="cement.utils.version:get_version"`
and `cement/__init__.py` re-exports `get_version()`. Do NOT edit those. Verify
after the edit:
```bash
grep -rn "3\.0\.15\|(3, 0, 15" --include="*.py" --include="*.toml" . | grep -v ".planning/"
# expect ONLY scripts/bump_dev_version.py's regex-doc comment (not a version of record)
python -c "from cement.utils.version import get_version; print(get_version())"  # -> 3.0.16
```

**Why hand-edit, not `bump_dev_version.py`** (Pitfall 2): the script forces
`'final'` (correct) but ALSO prepends a fresh `## X.Y.Z - DEVELOPMENT` changelog
section — wrong for a release-prep PR that FINALIZES an existing section. Reserve
the script for the post-release 3.0.17 bump, which the `dev-bump` workflow job
runs (not the planner).

---

### `CHANGELOG.md` (doc parsed by CI, transform / finalize)

**Analog:** the `## 3.0.14 - May 5, 2025` finalized section (CHANGELOG.md
lines 541-564) — the canonical shape a finalized section takes.

**Header finalization** (D-02) — the CURRENT unfinalized header at line 3:
```markdown
## 3.0.15 - DEVELOPMENT (will be released as stable/3.0.16)
```
becomes (MUST begin exactly `## 3.0.16` — `release.yml`'s `gh-release` job
awk-extracts the section by `## <tag>` match, and preflight rejects a header
still containing `DEVELOPMENT`):
```markdown
## 3.0.16 - July 12, 2026
```
Date format copies the established convention verbatim: `## 3.0.14 - May 5, 2025`.

**Bucket structure** (already present in the 3.0.15 section — preserve all five,
in this order; keep even empty ones as prior sections do with `- None`):
```
Bugs:          (CHANGELOG.md line 5)
Features:      (line 209)
Refactoring:   (line 287)
Misc:          (line 462)
Deprecations:  (line 536)
```

**Highlights paragraph** (D-03) — NEW element with no prior analog in the
changelog (previous sections have no narrative intro). Insert a 2-4 sentence
paragraph BETWEEN the `## 3.0.16 - <date>` header and the first `Bugs:` bucket.
Themes are locked by CONTEXT specifics: Python 3.10-3.14 matrix, warn-only
deprecations with 3.2.0 removals signposted, automated release workflow,
fully-typed modernized `cement generate` templates. This paragraph becomes the
top of the GitHub Release body and the source for the announcement copy (D-14).

**Entry condensation** (D-04) — copy the altitude of the 3.0.14 entries (1-3
lines, release-notes voice), NOT the verbose dev-forensic style of the current
3.0.15 entries. Example of the target altitude (from the 3.0.14 section):
```markdown
- `[ext_jinja2]` Refactor hard-coded reference to `jinja2` template handler.
  - [Issue #749](https://github.com/datafolklabs/cement/issues/749)
```
Contrast with a current 3.0.15 entry to be condensed (CHANGELOG.md lines 24-28):
```markdown
- `[utils.fs]` Restore `os.path` semantics in `abspath()` —
  preserves symlink paths and silently falls through on unknown
  `~user` prefixes (regression introduced by the Phase 03 Wave 6
  pathlib migration; restores 3.0.x BC contract on the public
  `cement.utils.fs:abspath` surface)
```
Rule (D-04): keep EVERY entry (including `[dev]` entries — do NOT delete/merge),
edit each to 1-3 lines. The `[area]` prefix convention (`[core.foundation]`,
`[ext.smtp]`, `[cli]`, `[dev]`) is already correct throughout — preserve it.

**D-01 cross-check mechanics** (reconcile, not rewrite): diff
`git log 3.0.14..HEAD` against the populated buckets, filtering planning-artifact
commits per CLAUDE.md "Changelog Maintenance" rules (drop `docs(NN.N):`,
`docs(state):`, `docs(quick-...):`; filter revert-pairs/overwrites; bucket by
Conventional Commit type: `fix:`→Bugs, `feat:`→Features, `refactor:`→Refactoring,
`chore:`→Misc). The section is already fully populated — this is a completeness
audit against success criterion 1, gated by the release-prep PR review.

---

### `.planning/.../05.4-PROVISIONING.md` (runbook checkoff, request-response)

**Analog:** the checkpoint/human-verify pattern from `05.4-05-SUMMARY.md`
(provisioning confirmed via checkpoint) — reused by D-09's guided session.

**Pattern:** for each pre-first-tag checklist item, the agent (a) presents the
exact provider value, (b) the user clicks through the provider UI, (c) the agent
verifies via `gh api`/`git` where verifiable and checks the item off in the
runbook. Verifiable-from-here commands already proven this session:
```bash
gh api repos/datafolklabs/cement/environments/release   # reviewer present
gh api repos/datafolklabs/cement/actions/secrets        # DOCKERHUB_* currently absent
git merge-base --is-ancestor origin/stable/3.0.x main && echo FF-OK  # ancestry
```
This file is only lightly edited (checkbox state); it is NOT rewritten.

---

### `.planning/.../06-VERIFICATION.md` (GSD artifact, batch)

**Analog:** `.planning/phases/05.4-github-actions-release-workflow/05.4-VERIFICATION.md`
— same phase family (a release-machinery verification that flips requirement IDs).

**YAML frontmatter shape** (05.4-VERIFICATION.md lines 1-27) — copy this block
structure exactly (fields: `phase`, `verified` ISO8601, `status`, `score`,
`behavior_unverified`, `overrides_applied`, `overrides[]`, `re_verification`,
`gaps[]`, `deferred[]`, `human_verification[]`):
```yaml
---
phase: 06-release-cut-3-0-16
verified: <ISO8601>
status: passed
score: 7/7 must-haves verified
behavior_unverified: 0
overrides_applied: 0
overrides: []
re_verification: null
gaps: []
deferred:
  - truth: "..."
    addressed_in: "..."
    evidence: "..."
human_verification: []
---
```

**Body sections** (copy 05.4's headings): `## Goal Achievement` →
`### Observable Truths (ROADMAP Success Criteria)` table (`# | Truth | Status |
Evidence`), `### Required Artifacts`, `### Key Link Verification`,
`### Behavioral Spot-Checks / Probe Execution`, `### Requirements Coverage`
(the table that flips REL-01..05 / CI-04 / DOCS-03 from Pending→Complete with
evidence), `### Anti-Patterns Found`, `### Human Verification Required`,
`### Gaps Summary`.

**Requirements-coverage row pattern** (05.4-VERIFICATION.md lines 92-100 —
copy this evidence-citation style; Phase 6 turns each `SATISFIED (machinery)`
into a live-run `SATISFIED` with a run-id/`gh release view`/clean-venv proof):
```markdown
| REL-04 | 04 | PyPI publish; installs cleanly 3.10-3.14 | ✓ SATISFIED (machinery) | ... |
```

---

### `.planning/.../06-ANNOUNCEMENT.md` (announcement copy) — NO ANALOG

**Reason:** this is the FIRST automated release; no prior announcement artifact
exists in `.planning/`. The planner should NOT invent fresh prose — per D-14 and
the "Don't Hand-Roll" table, DERIVE the copy from the finalized CHANGELOG.md
highlights paragraph (D-03), keeping one source of truth for "what shipped".
Format and location are Claude's discretion (CONTEXT). Sending stays human
(05.4 D-15). See "No Analog Found" below.

## Shared Patterns

### Conventional Commits + 78-char wrap (all commits this phase)
**Source:** CLAUDE.md "Commit Conventions"
**Apply to:** the release-prep PR commit(s), the `-s ours` ancestry merge message,
planning-artifact commits (`docs(06):` prefix).
```
chore: record stable/3.0.x ancestry for release fast-forward   # D-10 merge msg
docs(06): <planning artifact>                                  # planning commits
```
Subject max 78 chars; body wrapped at 78.

### Branching policy — no direct commits to main
**Source:** CLAUDE.md "Branching Policy"; CONTEXT D-05
**Apply to:** all executable changes. The changelog finalization + VERSION bump
ride ONE release-prep PR (branch e.g. `gsd/phase-6-release-cut`); the user
reviews and merges; the merged main commit is what gets tagged. The lone
exception is the `-s ours` ancestry merge (D-10), which MUST land as a real merge
commit run directly on main by the USER (a squash/rebase PR would destroy the
second parent — Pitfall 1), not via a squashed PR.

### Quality gates hold green (release-prep PR)
**Source:** CLAUDE.md "Key Development Practices"; RESEARCH Validation Architecture
**Apply to:** the release-prep PR before merge.
```bash
make comply        # ruff + mypy
make test          # 100% coverage (needs Redis:6379 + memcached:11211 — MEMORY note)
make audit-public-api   # byte-for-byte green (Phase 3 D-04 lineage)
```
Full PR CI (`gates.yml` via `build_and_test.yml`) must be green before merge.

### `[area]` changelog entry prefix
**Source:** CLAUDE.md "Changelog Maintenance"; existing CHANGELOG.md entries
**Apply to:** every CHANGELOG.md entry — one line, prefixed `[area]`
(`[ext.smtp]`, `[cli]`, `[core.handler]`, `[dev]`). Already correct in the
3.0.15 section; preserve during condensation.

## No Analog Found

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| `.planning/.../06-ANNOUNCEMENT.md` | doc (announcement copy) | transform | First automated release — no prior announcement draft exists in the repo. Per D-14 / "Don't Hand-Roll", derive from the finalized CHANGELOG highlights paragraph (D-03) rather than pattern-matching an analog. Format/location are Claude's discretion. |

Note: the changelog **highlights paragraph** (D-03) is also a first — previous
CHANGELOG sections have no narrative intro. It has no in-repo analog; the four
locked themes (CONTEXT specifics) are the content spec.

## Metadata

**Analog search scope:** `CHANGELOG.md` (section conventions),
`cement/core/backend.py`, `scripts/bump_dev_version.py`, `.planning/phases/**`
(`*-VERIFICATION.md`, `05.4-PROVISIONING.md`, `05.4-05-SUMMARY.md`).
**Files scanned:** ~8 (2 source, 1 script, 5 planning artifacts).
**Pattern extraction date:** 2026-07-12
