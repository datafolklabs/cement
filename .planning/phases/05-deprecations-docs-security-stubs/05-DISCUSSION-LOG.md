# Phase 5: Deprecations, Docs & Security Stubs - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-07
**Phase:** 05-deprecations-docs-security-stubs
**Areas discussed:** Deprecation target selection, deprecations.rst + DOCS-01 scope, DOCS-02/04 refresh depth, SEC-01/02/03 backlog stub format

---

## Deprecation target selection

### Q1 — Which deprecation candidates land warn-only DeprecationWarning calls?

| Option | Description | Selected |
|--------|-------------|----------|
| yaml.load() fallback (ext_yaml + ext_generate) | Deprecate the unsafe-load fallback codepath in favor of yaml.safe_load. Flagged in CONCERNS.md. | |
| shell=True default in shell.cmd() | Deprecate the default with migration guidance to pass shell=False explicitly. Flagged in CONCERNS.md. | |
| fs.Tmp.dir/.file as str (vs pathlib.Path) | Announce intent to flip to Path. Wide blast radius. | |
| None this phase — doc existing only | Lock to the 4 existing IDs (3.0.8-1, 3.0.8-2, 3.0.10-1, 3.0.16-1); skip net-new DEPREC-01 work. | ✓ |

**User's choice:** None this phase — doc existing only
**Notes:** Tightens the phase to documentation-only deprecation work. All three plausible candidates remain viable for a future milestone but Phase 5 deliberately does not pre-commit to any of them.

### Q2 — How should the existing 4 deprecation messages be handled?

| Option | Description | Selected |
|--------|-------------|----------|
| Audit + tighten messages | Sweep cement/core/deprecations.py: every message names its removal version. | ✓ |
| Leave as-is, ratify in REQUIREMENTS.md | Mark DEPREC-01..03 closed-in-place; drop DEPREC-* work entirely. | |
| Audit + leave 3.0.10-1 alone | Tighten only 3.0.16-1; leave the older 3.0.10-1 vague to avoid retroactive horizon-narrowing. | |

**User's choice:** Audit + tighten messages (Recommended)
**Notes:** Closes the spirit of DEPREC-01 even with no new IDs — migration guidance becomes concrete via explicit removal versions.

### Q3 — What removal version for the two vague messages?

| Option | Description | Selected |
|--------|-------------|----------|
| Both → 3.2.0 | Pin 3.0.10-1 and 3.0.16-1 both to v3.2.0. Aligns with the policy already locked into 3.0.8-1 and 3.0.8-2. | ✓ |
| 3.0.10-1 → 3.2.0; 3.0.16-1 → 4.0 | Stagger: old FATAL deprecation to 3.2.0, SMTP send bool-return to 4.0. | |
| Both → 4.0 | Defer all to Cement 4.0; keep the 3.2.0 surface narrow. | |

**User's choice:** Both → 3.2.0 (Recommended)
**Notes:** Consistency over horizon-preservation; downstream apps that ignored the warning since 3.0.10 had ample time.

### Q4 — Audit-tighten scope beyond cement/core/deprecations.py?

| Option | Description | Selected |
|--------|-------------|----------|
| Registry + adjacent docstrings | Update cement/core/deprecations.py AND tighten ext_logging.py:146-147, :368-369, ext_smtp.py send() docstring. One commit per concern. | ✓ |
| Registry only | Tighten only the runtime warning text; leave docstrings vague. Strict-minimum boundary. | |
| Registry + docstrings + sphinx autodoc check | Same as Recommended PLUS run make docs to confirm no new sphinx warnings surface. | |

**User's choice:** Registry + adjacent docstrings (Recommended)
**Notes:** The DOCS-01 sphinx-warnings check is already covered separately in Area 2; bundling here would have been duplicative.

---

## deprecations.rst + DOCS-01 scope

### Q1 — In-repo touchpoint for DEPREC-02 (given GitBook is canonical)?

**User clarification first:** "where is deprecations.rst? is this new?" → confirmed it does not exist. Then: "nah ... sphinx docs are strictly api code docs ... not developer/free-form docs" → load-bearing constraint, saved as project-level memory note. Then: "we have a gitbook site for developer docs, and deprecations are documented there" → reinforces.

| Option | Description | Selected |
|--------|-------------|----------|
| CHANGELOG.md only | Each phase's deprecation activity lands as a `[core.deprecations]` line in the active 3.0.16-DEVELOPMENT section; GitBook updated off-band. No new in-repo doc file. | |
| Top-level DEPRECATIONS.md (sibling of README) | New repo-root markdown file mirroring GitBook content for in-repo discoverability. Lives outside docs/source/. | ✓ |
| Inline cement/core/deprecations.py expansion | Expand the DEPRECATIONS dict comment/docstring to fully spell out each entry: ID, surface, since, removal, migration. | |

**User's choice:** Top-level DEPRECATIONS.md (sibling of README)
**Notes:** Mirrors GitBook for in-repo discoverability; not a sphinx page; respects the docs-split rule.

### Q2 — DOCS-01 zero-warnings gate scope?

| Option | Description | Selected |
|--------|-------------|----------|
| Fix all 4 + wire -W into make docs | Fix theme 'logo', api/index.rst toctree, InterfaceManager.list autodoc, shell.cmd inline literal. THEN flip make docs to sphinx-build -W permanently. | ✓ |
| Fix all 4, leave make docs unflagged | Same source fixes; -W applied as one-shot verification only. Lower long-term enforcement. | |
| Fix only the easy 3 (config + RST) | Skip the InterfaceManager.list autodoc-vs-PEP-585 issue; document it as accepted. | |

**User's choice:** Fix all 4 + wire -W into make docs (Recommended)
**Notes:** Mirrors Phase 1 D-08 / Phase 2 D-10 'no implicit drift' discipline. Permanent fail-fast.

### Q3 — Structure of new DEPRECATIONS.md?

| Option | Description | Selected |
|--------|-------------|----------|
| Per-deprecation block | One H2 section per ID (3.0.8-1, 3.0.8-2, 3.0.10-1, 3.0.16-1) with surface/since/removal/migration/GitBook-link. Stable structure; new IDs append. | ✓ |
| Per-removal-version sections | Group by REMOVAL version. Reader-friendly for migration planning; re-grouping required when removal pins move. | |
| Flat table | Single Markdown table: ID | Surface | Since | Removal | Migration. Compact and grep-able. | |

**User's choice:** Per-deprecation block (Recommended)
**Notes:** Mirrors the deprecate() ID-based URL anchor so the GitBook page can link back symmetrically.

---

## DOCS-02/04 refresh depth

### Q1 — DOCS-02 README + CONTRIBUTING refresh depth?

| Option | Description | Selected |
|--------|-------------|----------|
| Targeted fixes | README: drop dead Travis CI link. CONTRIBUTING.md: replace 'single commit per issue' with Conventional Commits + atomic-per-concern + 78-char wrap + `make commit`. One commit per file. No walkthrough verification. | ✓ |
| Targeted + walkthrough verification | Same edits PLUS run README install + CONTRIBUTING workflow end-to-end on a clean Python 3.10/3.14 venv. ~20-30 min extra. | |
| Targeted + Cement 4 forward signal | Targeted edits PLUS add a section noting Cement 3.0.x is in maintenance mode and Cement 4 is the future-breakage target. | |

**User's choice:** Targeted fixes (Recommended)
**Notes:** cli-smoke-test already covers install/run path; walkthrough would be duplicative. Cement 4 already in PROJECT.md Out of Scope; no need to re-state.

### Q2 — DOCS-04 docstring sweep approach?

| Option | Description | Selected |
|--------|-------------|----------|
| Fix-on-find sweep | DEPREC-02 docstring tightening + DOCS-01 RST fix already cover load-bearing surfaces; grep cement/**/*.py for stale Travis/setup.py/Python-3.9 references and fix any hit. No formal sample. | ✓ |
| doctest sample on representative modules | Pick 4-5 representative modules; wire pytest --doctest-modules; add `make docs-doctest`. Most rigorous; most scope expansion. | |
| No active sweep; ratify in REQUIREMENTS.md | Mark DOCS-04 closed-in-place: Phase 3 type-hint refresh + Phase 5 DEPREC-02 + DOCS-01 satisfy the spirit. | |

**User's choice:** Fix-on-find sweep (Recommended)
**Notes:** Matches the strict-minimum boundary established in Phase 1 D-13 / Phase 3 D-19.

### Q3 — Phase 3 deferred CONVENTIONS.md PEP 604/585 refresh?

| Option | Description | Selected |
|--------|-------------|----------|
| Land here | Update .planning/codebase/CONVENTIONS.md "Type annotations" paragraph from full form (Dict/Optional/List/Tuple) to PEP 604/585 lowercase-builtin form. Single commit. | ✓ |
| Punt to a future milestone | CONVENTIONS.md is planning intel, not user-facing; wrong text doesn't hurt downstream apps. Defer. | |

**User's choice:** Land here (Recommended)
**Notes:** Ties off Phase 3 D-22 step 5 / D-19 deferral cleanly.

---

## SEC-01/02/03 backlog stub format

### Q1 — Where do SEC-01/02/03 backlog stubs live, and what shape?

| Option | Description | Selected |
|--------|-------------|----------|
| Expand SECv2-01..03 in REQUIREMENTS.md | REQUIREMENTS.md already has v2 SECv2-01..04 entries as one-liners; expand the first three to multi-line phase-shaped scope notes. Single source of truth in the planning tree. | ✓ |
| GitHub issues + REQUIREMENTS.md cross-ref | Create 3 issues on datafolklabs/cement labeled per Phase 4 TRIAGE-03 vocabulary; cross-ref from REQUIREMENTS.md. Higher external visibility. | |
| .planning/backlog/SEC-*.md per stub | New `.planning/backlog/` dir with self-contained mini-phase outlines. Adds a new planning convention. | |
| Both: expand REQUIREMENTS.md AND open GH issues | Belt-and-braces. Highest visibility + highest upkeep cost. | |

**User's choice:** Expand SECv2-01..03 in REQUIREMENTS.md (Recommended)
**Notes:** Triage was a one-shot live-state pass on issue-tracker objects (Phase 4); SEC stubs are forward-looking planning entries that belong with v1/v2 requirements they extend.

### Q2 — What goes in each expanded SECv2 entry?

| Option | Description | Selected |
|--------|-------------|----------|
| Tool + invocation + CI placement | Tool command, Makefile target name, CI lane, config-file shape, new dev-dep, expected exit behavior, Phase 2 D-03 precedent anchor. ~6-10 lines per stub. | ✓ |
| Tool + full mini-phase outline | Recommended PLUS goal, success criteria (3-5 items), dependency chain, estimated plan count, risks, research links. ~25-40 lines per stub. | |
| Tool + CI placement only | Just tool name, command, CI lane. ~3-4 lines per stub. Lowest scope. | |

**User's choice:** Tool + invocation + CI placement (Recommended)
**Notes:** Lean enough that the future-milestone discuss-phase can refine without pre-committing decisions; rich enough that no re-discovery is needed (ROADMAP success criterion #5).

---

## Claude's Discretion

- Specific commit-message body phrasing within the D-16 commit sequence (planner picks).
- Order of `docs(sphinx): ...` commits within steps 5-9 — independent fixes; planner can interleave.
- Whether the api/index.rst toctree fix (D-08 #2) is solved by fold-into-index OR by adding a `:hidden:` toctree — planner picks the smaller diff.
- Whether the docstring grep sweep (D-11) finds 0, 1, or N hits — planner splits per file if N is large.
- Whether to author commits via `make commit` (cz) or directly via `git commit` (either satisfies CLAUDE.md).
- Exact wording of the inline `# autodoc:` comment in `cement/core/interface.py:102` (D-08 #3).
- Pre-flight `make audit-public-api` check around the `InterfaceManager.list` string-quote (D-18 #3) — if AST serialization changes, planner decides between baseline rebase and alternative workaround.

## Deferred Ideas

- yaml.load() fallback deprecation (CONCERNS.md security item)
- shell=True default in shell.cmd() deprecation (CONCERNS.md)
- fs.Tmp.dir/.file `str` → `pathlib.Path` (Cement 4 candidate)
- pytest --doctest-modules sample on representative modules (future regression gate)
- CI integration of `make docs -W` (Phase 5 keeps the gate local-only)
- Cement 4 forward-signaling in README/CONTRIBUTING (Cement 4 kickoff milestone)
- `.planning/backlog/` directory convention (introduce when planning tree grows to need it)
- `SECURITY.md` repo-root file (SECv2-04 — distinct from SEC-01..03 scope; future security-tooling milestone)
- Walkthrough verification of README install/run + CONTRIBUTING workflow (release-cut polish, future milestone)
