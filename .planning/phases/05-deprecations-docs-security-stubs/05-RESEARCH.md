# Phase 5: Deprecations, Docs & Security Stubs - Research

**Researched:** 2026-05-07
**Domain:** Documentation-only sweep (Sphinx zero-warnings, registry pins,
in-repo markdown, planning intel)
**Confidence:** HIGH

## Summary

CONTEXT.md for Phase 5 is unusually concrete: every file path, line number,
and decision is locked. This research validates the locked decisions
against the live repo state, surfaces the implementation gotchas that
could trip the executor, and pre-runs the validation surfaces (`make docs`,
`make audit-public-api`, the DOCS-04 grep) so the planner can encode
deterministic acceptance criteria rather than open-ended checks.

**Key validated findings:**

1. **All 4 sphinx warnings reproduce verbatim** [VERIFIED: `pdm run sphinx-build`].
2. **DOCS-04 grep returns ZERO docstring hits in `cement/`** — commit step
   12 in CONTEXT.md D-16 is **0 commits**, not N. [VERIFIED: live grep]
3. **`audit-public-api.py` is annotation-blind** — it walks AST names only,
   never serializes annotations. The string-quote in
   `InterfaceManager.list` (D-08 #3) cannot affect the audit.
   [VERIFIED: read scripts/audit-public-api.py + simulated AST walk]
4. **`conf.py` has a duplicate `html_theme_options` dict** — line 51-53
   silently overwrites the line 19-33 dict. Naive "remove only the `logo`
   key" leaves `html_theme_options = {}` and drops all toc-config. The
   correct fix is to delete the entire second assignment (lines 51-53),
   restoring the original dict. [VERIFIED: read docs/source/conf.py]
5. **The codebase already has a sibling-consistent pattern for
   `def list() -> ...` methods**: `import builtins` + `builtins.list[T]`.
   Used in `cement/core/{hook,handler,extension}.py`. CONTEXT.md D-08 #3
   picks string-quote; the planner has Claude's discretion to revisit
   (see Open Question 1). [VERIFIED: grep across cement/core]
6. **GitBook anchor format is `#3.0.X-Y` (dotted), NOT `#3-0-X-Y`**.
   `cement/core/deprecations.py:15` and `foundation.py:610` both confirm.
   [VERIFIED: grep + read]
7. **DEPREC-03 is already-satisfied** — 4 deprecations / 4 assertions:
   `tests/core/test_deprecations.py` covers `3.0.8-1`, `3.0.8-2`,
   `3.0.10-1`; `tests/ext/test_ext_smtp.py:631` covers `3.0.16-1`.
   [VERIFIED: grep]

**Primary recommendation:** Plan the 14 commits in CONTEXT.md D-16 as
written. The string-quote workaround in D-08 #3 is safe; the only real
risk is the `conf.py` duplicate-dict gotcha (Pitfall 2 below). Wave the
docstring edits BEFORE the `-W` flag flip so an unrelated docstring
warning doesn't blindside the gate (Pitfall 5).

## User Constraints (from CONTEXT.md)

> CONTEXT.md is the locked source of truth. The decisions below are
> non-negotiable for the planner. Reproduced verbatim from
> `05-CONTEXT.md` <decisions> for plan-time reference; if these
> conflict with anything else in this RESEARCH.md, CONTEXT.md wins.

### Locked Decisions

- **D-01:** No net-new `DeprecationWarning` entries this milestone.
- **D-02:** Audit + tighten existing messages — single
  `refactor(core.deprecations): tighten removal-version language`
  commit pinning `3.0.10-1` and `3.0.16-1` to v3.2.0. DEPREC-03
  already-satisfied.
- **D-03:** Pin both vague messages → 3.2.0 (NOT 4.0).
- **D-04:** Adjacent docstring sweep at
  `cement/ext/ext_logging.py:146-147,368-369` and
  `cement/ext/ext_smtp.py` `send()`. NOT in scope:
  `cement/core/foundation.py:608` (already correct).
- **D-05:** No `docs/source/deprecations.rst` page. Sphinx is
  API-reference only.
- **D-06:** In-repo touchpoint = top-level `DEPRECATIONS.md` (sibling
  of `README.md`).
- **D-07:** Per-deprecation H2 block format: surface, since-version,
  removal-version, migration guidance, GitBook link.
- **D-08:** Fix all 4 sphinx warnings + flip `make docs` to
  `sphinx-build -W ./source ./build`.
- **D-09:** `-W` flag is permanent + AUDIT POINT comment.
- **D-10:** README + CONTRIBUTING — targeted edits only. Two commits.
- **D-11:** DOCS-04 = fix-on-find sweep, not formal sample.
- **D-12:** CONVENTIONS.md PEP 604/585 refresh — single commit.
- **D-13:** SEC-01..03 = in-place expansion in REQUIREMENTS.md.
  NOT SECv2-04.
- **D-14:** Phase-shaped scope notes per stub: tool, Makefile target,
  CI placement, config-file shape, dev-dep, exit behavior, anchor.
- **D-15:** Single commit for the SEC expansion.
- **D-16:** Atomic per-concern, Conventional Commits, 78-char wrap.
  14-commit suggested sequence.
- **D-17:** GSD artifact commits as `docs(05): ...`.
- **D-18:** 12-conjunct acceptance gate (see CONTEXT.md).

### Claude's Discretion

- Specific commit-message body phrasing within D-16 sequence.
- Order of `docs(sphinx): ...` commits within steps 5-9 (independent).
- Whether the api/index.rst toctree fix (D-08 #2) is solved by
  fold-into-index OR by `:hidden:` toctree.
- Whether docstring grep (D-11) yields 0/1/N hits — pre-confirmed
  here as **0** (see <code_examples> below).
- Whether to author commits via `make commit` (cz) or `git commit`.
- Exact wording of inline `# autodoc:` comment in
  `cement/core/interface.py:102`.
- Pre-flight `make audit-public-api` check around the
  `InterfaceManager.list` string-quote — pre-confirmed here as
  **safe (no baseline rebase)** (see Pitfall 1 below).

### Deferred Ideas (OUT OF SCOPE)

- `yaml.load()` fallback deprecation
  (`cement/ext/ext_yaml.py:160` + `cement/ext/ext_generate.py:43`).
- `shell=True` default deprecation in `cement/utils/shell.py:cmd()`.
- `fs.Tmp.dir/.file` `str` → `pathlib.Path` flip (Cement 4 candidate).
- `pytest --doctest-modules` formal sample on representative modules.
- CI integration of `make docs -W` (local-only this phase).
- Cement 4 forward-signaling in README/CONTRIBUTING.
- `.planning/backlog/` directory convention.
- `SECURITY.md` repo-root file (SECv2-04, distinct concern).
- Walkthrough verification of README install/run path.

## Phase Requirements

> Each requirement maps to specific decisions and validation surfaces
> below. The planner uses this table to wire `acceptance_criteria`
> on tasks.

| ID | Description | Research Support |
|----|-------------|------------------|
| DEPREC-01 | Surfaces flagged for removal in 3.2.0 / Cement 4 emit `DeprecationWarning` with migration guidance in the message | D-02/D-03 — pin `3.0.10-1` + `3.0.16-1` to v3.2.0 in `cement/core/deprecations.py` (4-entry dict; verified live state below) |
| DEPREC-02 | Each new deprecation is documented in the changelog and a dedicated `docs/source/deprecations.rst` page | **Reinterpreted per D-05/D-06** — Sphinx is API-only; in-repo touchpoint = top-level `DEPRECATIONS.md`. Per-block format per D-07. |
| DEPREC-03 | Test suite asserts each deprecation warning fires | **Already-satisfied** — `tests/core/test_deprecations.py` (3 of 4 IDs) + `tests/ext/test_ext_smtp.py:631` (`3.0.16-1`). No new test work this phase (D-02). |
| DOCS-01 | `make docs` builds Sphinx docs without warnings or broken cross-references | D-08 — 4 known warnings (verified verbatim below). D-09 — `-W` flag wired permanently with AUDIT POINT comment. |
| DOCS-02 | README, CONTRIBUTING, and getting-started examples accurate against the 3.0.16 release | D-10 — Travis link/badge dropped from README; CONTRIBUTING aligned to Conventional Commits + `make commit`. Two atomic commits per file. |
| DOCS-04 | Public API docstrings reviewed for staleness; broken/outdated examples corrected | D-04 (adjacent sweep) + D-11 (fix-on-find grep — pre-verified to return 0 docstring hits in `cement/`). D-12 closes the deferred CONVENTIONS.md refresh. |
| SEC-01 | Backlog item recorded for adding `pip-audit` to CI | D-13/D-14 — expand `SECv2-01` in REQUIREMENTS.md to phase-shaped scope (tool, Makefile target, CI lane, config, dev-dep, exit behavior). Anchor: `02-PIP-AUDIT.md`. |
| SEC-02 | Backlog item recorded for adding `bandit` static analysis | D-13/D-14 — expand `SECv2-02`. Tool: `pdm run bandit -r cement/`. Target: `make audit-bandit`. Config: `.bandit` allowlist. |
| SEC-03 | Backlog item recorded for evaluating CodeQL or Semgrep SAST coverage | D-13/D-14 — expand `SECv2-03`. Tool TBD (CodeQL or Semgrep evaluation). Target: `make audit-sast`. Config: `.semgrep.yml` or equivalent. |

## Architectural Responsibility Map

> Phase 5 is documentation-only. There is no application-tier mapping
> per se, but each capability still maps to an artifact tier owner —
> source code (cement/), API docs (docs/source/), in-repo developer
> docs (repo root), planning intel (.planning/), CI/build
> infrastructure (Makefile, .github/). The map disambiguates which
> artifact owner each commit touches.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Deprecation registry message text | source code (`cement/core/deprecations.py`) | — | Runtime warning text; the "primary" source-of-truth for what `deprecate()` emits. |
| Adjacent deprecation docstrings | source code (`cement/ext/ext_logging.py`, `cement/ext/ext_smtp.py`) | API docs (autodoc) | Source-of-truth lives in source; autodoc renders into API docs at build-time. |
| Top-level `DEPRECATIONS.md` | in-repo developer docs (repo root) | — | Mirrors GitBook narrative for in-repo discoverability. NOT a sphinx page (D-05). |
| Sphinx warning fixes (`conf.py`, `api/index.rst`, `interface.py:102`, `shell.py` docstring) | API docs (`docs/source/`) + source code (cross-cutting) | — | conf.py + RST live in API docs; the interface.py/shell.py fixes are source-code edits whose effect is visible only via autodoc. |
| `make docs -W` flag | CI/build infrastructure (`Makefile`) | API docs gate | Permanent local-fail-fast gate; CI integration deferred. |
| README + CONTRIBUTING refresh | in-repo developer docs (repo root, `.github/`) | — | User-facing markdown; not autogenerated. |
| Docstring fix-on-find sweep | source code (`cement/`) | API docs | Source edits surface in autodoc. Pre-verified 0 hits — no actual edits. |
| `.planning/codebase/CONVENTIONS.md` PEP 604/585 refresh | planning intel (`.planning/`) | — | In-repo planning intel only; not user-facing, not GitBook. |
| SECv2-01..03 stub expansion | planning intel (`.planning/REQUIREMENTS.md`) | — | Backlog stub for future security milestone. |
| CHANGELOG entries (per commit) | in-repo developer docs (repo root) | — | Append phase-by-phase to active `## 3.0.15 - DEVELOPMENT` section per CLAUDE.md. |

## Project Constraints (from CLAUDE.md)

| Directive | How Phase 5 Honors It |
|-----------|----------------------|
| 78-char subject + body wrap on commits | All 14 commits in D-16 sequence respect this. Use `make commit` (cz) or hand-format with HEREDOC. |
| Conventional Commits prefix | D-16 sequence prescribes `refactor(...)`, `docs(...)`, `fix(...)`, `chore(...)` — all conformant. |
| Phase-by-phase CHANGELOG updates | D-16 explicitly lands per-commit entries to `## 3.0.15 - DEVELOPMENT`. NOT deferred to release-cut (Phase 6 owns DOCS-03). |
| Filter planning-artifact commits from CHANGELOG | The `docs(05): ...` artifact commits (RESEARCH/PLAN/CONTEXT) are workflow scaffolding — DO NOT add changelog entries for them. Only land entries for commits that touch user-visible surfaces (`cement/`, `README.md`, `CHANGELOG.md`, `Makefile`, `.github/CONTRIBUTING.md`, `DEPRECATIONS.md`). |
| Bucket by Conventional Commit type | `refactor:` → Refactoring; `docs:` → Misc (or Features for new files like `DEPRECATIONS.md` — D-16 calls this judgment, leans Misc); `fix:` → Bugs; `chore:` → Misc. |
| 100% test coverage absolute | Phase 5 is doc-only; coverage MUST stay 100% on every commit (verified by `make test`). |
| Zero new runtime deps for core | Phase 5 adds none; SECv2 stub expansion only documents future dev-deps. |
| Project skills not configured | `.agents/skills/`, `.claude/skills/` absent — no skill files to load. [VERIFIED: ls] |

## Standard Stack

> Phase 5 is documentation-only — no new libraries are introduced.
> The "standard stack" here is the existing build/lint/audit tooling
> already pinned in `pyproject.toml` that Phase 5 leans on.

### Core (already installed, version-confirmed against live env)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| sphinx | 8.1.3 | API doc builder | Pinned in `[project.optional-dependencies] docs`; Phase 03 captured baseline. [VERIFIED: `pdm run sphinx-build --version`] |
| sphinx_rtd_theme | 3.1.0 | HTML theme | Active theme (`html_theme = "sphinx_rtd_theme"` in conf.py:17). The `'logo'` key (D-08 #1) is the unsupported option to drop. [VERIFIED: `pdm run python -c "import sphinx_rtd_theme; print(sphinx_rtd_theme.__version__)"`] |
| guzzle_sphinx_theme | latest | Listed but inactive | Listed in `[project.optional-dependencies] docs` but commented-out in conf.py:35-85. **No nuisance warnings from guzzle** (it's never imported). [VERIFIED: read docs/source/conf.py] |
| sphinxcontrib-napoleon | latest | Google-style docstring support | Listed in docs extras; not directly invoked by Phase 5 fixes. |
| docutils | bundled-with-sphinx | RST parser | Source of "Inline literal start-string without end-string" warning at `cement/utils/shell.py` cmd() docstring. [VERIFIED] |

### Supporting (re-used, no new deps)

| Library | Purpose | When to Use |
|---------|---------|-------------|
| make / Makefile | Target wrapper | Phase 5 only modifies the `docs:` target. No new targets added (D-09: `-W` flag, AUDIT POINT comment). |
| `scripts/audit-public-api.py` | AST-walk public-API surface enumerator | D-18 #3 acceptance gate; `make audit-public-api` exit 0 required around the `interface.py:102` change. **Pre-verified safe** (Pitfall 1). |
| `pytest` + `pytest-cov` | Test runner + coverage gate | `make test` must stay 100% on every commit. Phase 5 is doc-only — no test changes (DEPREC-03 already-satisfied). |
| `ruff` 0.15.x + `mypy` 1.20.x | Compliance gates | `make comply` must stay clean on every commit (D-18 #2). |
| `commitizen` (cz) | Conventional-Commits commit authoring | `make commit` is the project's canonical interactive commit path (CLAUDE.md). |

### Alternatives Considered (and rejected per CONTEXT.md)

| Instead of | Could Use | Tradeoff (and why CONTEXT.md rejected) |
|------------|-----------|----------------------------------------|
| String-quote `"list[str]"` workaround in `interface.py:102` (D-08 #3) | `import builtins` + `builtins.list[str]` (matches sibling pattern in `hook.py`/`handler.py`/`extension.py`) | Sibling-consistent, but adds `cement.core.interface:builtins` to public-API surface — requires baseline rebase. CONTEXT.md picks string-quote (zero-rebase). See Open Question 1. |
| Top-level `DEPRECATIONS.md` (D-06) | `docs/source/deprecations.rst` (literal REQUIREMENTS.md DEPREC-02 wording) | Sphinx is API-only per `docs/source/index.rst` note. Reinterpreted per D-05. |
| Fix-on-find grep sweep (D-11) | `pytest --doctest-modules` permanent regression gate | Would multiply scope past phase boundary. Deferred to a future milestone. |
| In-place REQUIREMENTS.md expansion (D-13) | `.planning/backlog/` directory + GitHub issues | New convention overhead; the planning tree IS the single source of truth. |

**Installation:** No new packages required; Phase 5 uses only what's
already in the environment.

**Version verification:** [VERIFIED 2026-05-07]
- `pdm run sphinx-build --version` → `sphinx-build 8.1.3`
- `pdm run python -c "import sphinx_rtd_theme; print(sphinx_rtd_theme.__version__)"` → `3.1.0`
- `pdm run python scripts/audit-public-api.py` → exit 0, baseline diff empty.

## Architecture Patterns

### Doc-only phase data flow

Phase 5 has no runtime data flow — it's a documentation/registry sweep.
What follows is the **artifact-flow diagram** the planner needs:

```
[planner picks commit order from D-16 sequence (14 steps)]
            |
            v
[per-commit: edit source/docs/markdown] -----> [stage]
            |                                     |
            v                                     v
[per-commit: append CHANGELOG entry] -----> [stage CHANGELOG.md]
            |
            v
[run gates: make comply + make test + make audit-public-api]
            |        (steps 1-3, 7-9 also: make docs)
            v
[commit (cz or git, Conventional + 78-char wrap)]
            |
            v
[next commit]  -----> [end of 14-commit sequence]
            |
            v
[final phase gate: D-18 12-conjunct acceptance]
            |
            v
[gsd-verify-work / phase complete]
```

### Recommended commit order (D-16 verbatim, with research annotations)

```
1.  refactor(core.deprecations): tighten removal-version language
2.  refactor(ext.logging): tighten FATAL deprecation removal version in docstrings
3.  refactor(ext.smtp): document send() bool-return removal in v3.2.0
4.  docs: add top-level DEPRECATIONS.md
5.  docs(sphinx): drop unsupported 'logo' theme option from conf.py
        ! See Pitfall 2 — delete the duplicate dict (lines 51-53), NOT just the 'logo' key
6.  docs(sphinx): wire api/index into top-level toctree
        ! Choose fold-into-index OR :hidden: toctree (Discretion)
7.  fix(core.interface): string-quote list[str] return annotation for autodoc compatibility
        ! Pre-flight make audit-public-api — confirmed safe (Pitfall 1)
8.  docs(utils.shell): fix inline-literal RST in cmd() docstring
9.  chore(make): wire -W into make docs (zero-warnings gate)
        ! Order steps 1-8 BEFORE this so an unrelated docstring warning doesn't blindside the gate flip (Pitfall 5)
10. docs(readme): drop Travis CI link (moved to GitHub Actions)
        ! Two surfaces: line 5 badge + line 60 list-item link
11. docs(contributing): align with Conventional Commits + atomic-per-concern discipline
12. docs(<area>): drop stale <thing> reference (per docstring grep hit)
        ! Pre-verified: 0 hits in cement/ — this step is **0 commits**
13. docs(codebase): refresh CONVENTIONS to PEP 604/585 syntax
        ! CONVENTIONS.md ALREADY in PEP 604/585 form (verified live).
        ! Single residual surface: line 35 ruff `target-version = "py39"` literal
        ! See Pitfall 6
14. docs(05): expand SECv2-01..03 with phase-shaped scope notes
```

### Pattern 1: Atomic-per-concern Conventional Commit (carries from Phases 1-3)

**What:** One concern per commit. Subject ≤ 78 chars. Body wraps at 78.
Conventional prefix maps to one CHANGELOG bucket.

**When to use:** Every Phase 5 commit.

**Example:** [Source: existing `CHANGELOG.md` 3.0.15 section, line 290-330]
```
refactor(core.deprecations): tighten removal-version language

Pin 3.0.10-1 (FATAL logging) and 3.0.16-1 (SMTPMailHandler.send bool
return) to v3.2.0 in DEPRECATIONS dict. Aligns with the existing
3.0.8-1 / 3.0.8-2 policy. Removal target is the next breakage-allowed
minor; downstream apps that have ignored the warning since 3.0.10 have
had ample time.

DEPREC-01 acceptance criterion #5: every entry in
cement/core/deprecations.py:DEPRECATIONS now names a removal version.
DEPREC-03 already-satisfied — existing tests assert by ID, not by
message text.
```

### Pattern 2: AUDIT POINT inline comment (carries from Phase 1 D-08)

**What:** A grep-able inline comment marking a deliberate
configuration choice so a future cleanup doesn't silently re-introduce
drift.

**When to use:** D-09 — at the `make docs` `-W` flag site in `Makefile`.

**Example:** [Source: existing pyproject.toml `[tool.ruff]` AUDIT POINT
comment from Phase 1 D-08]
```makefile
docs:
	# AUDIT POINT: -W enforces zero docs warnings. If a future
	# warning is acceptable, suppress it explicitly via conf.py
	# suppress_warnings rather than reverting -W. Pattern carries
	# from Phase 1 D-08 / Phase 2 D-10/D-11 (no implicit drift).
	cd docs; pdm run sphinx-build -W ./source ./build; cd ..
	@echo
	@echo DOC: "file://"$$(echo `pwd`/docs/build/html/index.html)
	@echo
```

### Pattern 3: Pre-flight gate verification before changing source

**What:** Before any commit that COULD shift `make audit-public-api`
output, run the audit; apply the change; rerun; confirm diff empty.

**When to use:** D-18 #3 — around commit 7 (`fix(core.interface): ...`).

**Example flow:**
```bash
make audit-public-api && echo OK_BEFORE                # exit 0 expected
# apply edit to cement/core/interface.py:102
make audit-public-api && echo OK_AFTER                 # MUST stay exit 0
git add cement/core/interface.py
git commit -m "..."
```

**Pre-verified result for Phase 5:** AST walker is annotation-blind;
string-quote does NOT change audit output. (See Pitfall 1.)

### Anti-Patterns to Avoid

- **Editing `html_theme_options` line 51 only.** Deleting just the
  `'logo'` key leaves `html_theme_options = {}` and clobbers all the
  toc-config (collapse_navigation, navigation_depth, titles_only,
  etc.). Correct fix: delete lines 51-53 entirely. (Pitfall 2.)
- **Flipping `-W` before fixing all 4 known warnings.** The flag
  becomes fail-fast the moment it's wired; if any warning is still
  emitting, `make docs` (and any CI lane that ever calls it) breaks.
  D-16 ordering puts `-W` flip at commit 9, after all 4 fixes land.
- **Adding tests for DEPREC-03.** Already-satisfied. Adding
  redundant tests inflates coverage line-count and adds noise.
- **Treating `docs(05): ...` artifact commits as user-visible.** They
  are GSD planning scaffolding. CHANGELOG entries DO NOT land for
  RESEARCH/PLAN/CONTEXT/VERIFICATION commits — only for source/doc
  changes that ship in 3.0.16. Anchor: CLAUDE.md
  §"Changelog Maintenance" — "Filter out planning-artifact commits".
- **Re-deriving CONTEXT.md decisions.** This research validates and
  elaborates; it does not re-decide.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| RST inline-literal validation | Custom regex check | docutils via `sphinx-build` (already wired through `make docs`) | docutils' parser is the canonical RST validator; rolling your own catches a different subset of warnings. |
| Public-API drift detection across the `interface.py:102` change | Custom name diff or grep | `scripts/audit-public-api.py` + `make audit-public-api` (Phase 03 D-04) | The script is the project's permanent dev affordance for exactly this — Phase 5 reuses, doesn't duplicate. |
| GitBook anchor URL construction in `DEPRECATIONS.md` | New URL format | `https://docs.builtoncement.com/release-information/deprecations#<id>` (the format `cement/core/deprecations.py:15` and `foundation.py:610` already use) | Round-trip navigation between in-repo `DEPRECATIONS.md` and the GitBook narrative depends on the anchors matching. The convention is locked. |
| Per-commit CHANGELOG bucketing logic | Custom mapping | The existing `Bugs / Features / Refactoring / Misc / Deprecations` buckets, populated in the active `## 3.0.15 - DEVELOPMENT` section | The buckets are stable across cement's CHANGELOG history; the mapping rule (`refactor:` → Refactoring, `docs:` → Misc, etc.) is in CLAUDE.md §"Changelog Maintenance". |

**Key insight:** Phase 5 is doc-only and the project already has the
audit/build/test/lint scaffolding it needs. Don't build new tools;
chain the existing gates.

## Common Pitfalls

### Pitfall 1: `audit-public-api` baseline rebase confusion (D-08 #3 + D-18 #3)

**What goes wrong:** The planner reads the CONTEXT.md `<code_context>`
"Known refactor risk surfaces" warning verbatim and assumes the
string-quote MIGHT change audit output. They build the plan to
include a "rebase baseline" fallback path, which complicates the
plan and may panic the executor when they see the change is
"risky".

**Why it happens:** A reasonable misreading of the CONTEXT.md prose
("the AST-walk audit script may serialize `"list[str]"` differently
from `list[str]`"). The hedge was honest planning-time uncertainty;
this research VERIFIED it by reading the script.

**Reality:** [VERIFIED: read `scripts/audit-public-api.py` lines
59-152] The script enumerates AST `Name`, `FunctionDef`, `ClassDef`,
`AnnAssign.target`, `Assign.targets`, and `ImportFrom`/`Import` node
NAMES only. It NEVER serializes annotations. Adding or removing
quotes around a return annotation has zero effect on the script
output. Simulated AST walk on quoted vs unquoted forms produced
identical method-name enumeration.

**How to avoid:** Plan the change as a single straightforward
commit. Pre-flight verification (`make audit-public-api` before/after)
is still good hygiene — but the planner should treat it as
**confirmation**, not as a branch point. Document in the plan:
"Pre-flight check expected to be no-op; if it surprises us, escalate
to user."

**Warning signs:** Plan explicitly carving a "if audit fails"
fallback into a separate task; commit message hedging on whether
the change is "really" public-API-safe.

### Pitfall 2: `conf.py` duplicate `html_theme_options` dict (D-08 #1)

**What goes wrong:** The planner writes a task that says "remove the
unsupported `'logo'` key from `html_theme_options`". The executor
reads the file, finds the `'logo'` key on line 52 inside the dict
on lines 51-53, deletes that line, and leaves
`html_theme_options = {}` — silently clobbering the **other**
`html_theme_options` dict on lines 19-33 that contains the active
toc-config (`collapse_navigation`, `navigation_depth`, `titles_only`,
etc.). The site builds without the `'logo'` warning, but the
navigation rendering quietly degrades.

**Why it happens:** Python evaluates `html_theme_options = {...}` at
line 19, then re-binds the name at line 51 to a new dict — the
line-19 dict is discarded. The reader scanning top-down may not
register that the second assignment is a full overwrite, not a
merge. The `'logo'` key is the only key in the second dict, so the
naive fix removes the only key, leaving the empty dict in place.

**How to avoid:** The correct fix is to **delete lines 51-53
entirely** (the whole second `html_theme_options = {...}` assignment).
Lines 19-33 then become the live config. Encode this in the task
text explicitly: "delete lines 51-53 in `docs/source/conf.py` (the
duplicate `html_theme_options` assignment that contains only the
unsupported `'logo'` key)" — NOT "remove the `'logo'` key".

**Warning signs:** Task wording that says "remove the 'logo' key"
without specifying line numbers; verification step that only checks
"the `logo` warning no longer fires" without checking that
`navigation_depth` etc. are still in effect.

### Pitfall 3: Inline-literal RST fix wording (D-08 #4)

**What goes wrong:** The planner assumes the RST fix is "add a
backtick somewhere"; the executor adds a stray backtick in the wrong
position, creating a different RST warning ("inline emphasis
start-string without end-string", or a bold/literal mismatch).

**Why it happens:** The current docstring at
`cement/utils/shell.py:35-39` reads:
```
        tuple: When ``capture==True``, returns the ``(stdout, stderror,
            return_code)`` of the command. ``stdout`` and ``stderror`` are
            ``bytes`` (the ``Popen`` default); decode with the appropriate
            encoding if string output is needed, or pass ``text=True`` /
            ``encoding=...`` through ``**kwargs``.
```
The docutils warning at line 19 of the docstring traces to
`` ``text=True`` / ``encoding=...`` ``. The slash between two
inline-literal closing/opening backticks confuses the parser — it
reads the trailing `` `` `` of `` ``text=True`` `` and the leading
`` `` `` of `` ``encoding=...`` `` as a continuous run, fails to
close the literal at the slash boundary.

**How to avoid:** Reformat as separate prose, e.g.:
```
            ``bytes`` (the ``Popen`` default); decode with the
            appropriate encoding if string output is needed, or pass
            ``text=True`` or ``encoding=...`` through ``**kwargs``.
```
The single word `or` between the two literals gives docutils enough
breathing room. Two equally valid alternatives: (a) a sentence break
("...if string output is needed. Pass ``text=True`` or
``encoding=...`` through ``**kwargs``."); (b) a comma+space
("``text=True``, ``encoding=...``").

**Warning signs:** A different inline-literal warning fires after
the fix; or `make docs` exits clean but the rendered HTML shows raw
backticks.

### Pitfall 4: api/index.rst toctree fix — duplicating the toctree

**What goes wrong:** The planner picks "fold api/index.rst into
top-level index.rst" as the fix shape, but doesn't delete
`api/index.rst` itself — leaving an orphan file. OR picks
":hidden: toctree" but adds it to the wrong file, double-listing
the api/core/index, api/utils/index, api/ext/index entries.

**Why it happens:** Both `docs/source/index.rst` (lines 8-13) and
`docs/source/api/index.rst` (lines 9-14) contain a toctree pointing
at the same three child indexes (`core/index`, `utils/index`,
`ext/index`). They're near-duplicates; the warning is that
`api/index.rst` is not referenced from any toctree.

**How to avoid:** Either (a) delete `docs/source/api/index.rst` and
keep the existing top-level `docs/source/index.rst` toctree (which
already references `api/core/index`, `api/utils/index`,
`api/ext/index` directly — verified read above); OR (b) add
`api/index` as a `:hidden:` toctree entry in `docs/source/index.rst`
and let `api/index.rst` carry its own visible toctree.

**Recommendation:** Pick (a) — it's the smaller diff and the
top-level index already has all three entries. After deleting
`docs/source/api/index.rst`, `make docs` should drop the "document
isn't included in any toctree" warning. Note that **option (a)
shrinks the doc surface by one orphan page** — confirm no external
links land on `api/index.html` (they don't; the live site renders
from the top-level `index.html`).

**Warning signs:** Three toctree references to `api/core/index`
appearing on the rendered page; `api/index.html` 404 in
`docs/build/html/` after delete (expected).

### Pitfall 5: Flipping `-W` before all 4 fixes land (D-09)

**What goes wrong:** Planner orders the `-W` flip (commit 9) BEFORE
the docstring sweep (commits 2-3). Commit 9 succeeds locally because
the docstring sweep is already in-tree; but if the planner reverses
the order, commit 9 lands `-W` while a docstring warning is still
emitting → `make docs` exits non-zero → developer has to chase the
warning before they can land any subsequent commit.

**Why it happens:** Both commits are independent and can be
reordered freely; the planner may shuffle for grouping (e.g., put
all `chore(make):` style commits together).

**How to avoid:** Lock the order: docstring fixes (commits 2-3) and
all 4 sphinx fixes (commits 5-8) MUST land before commit 9 (`-W`
flip). D-16 ordering already encodes this; the planner should
preserve it.

**Warning signs:** Commit 9 in the plan placed before commit 8;
plan comment "reorder for clarity" near the docs commits.

### Pitfall 6: CONVENTIONS.md PEP 604/585 refresh — already partially done

**What goes wrong:** The planner writes a task assuming
`.planning/codebase/CONVENTIONS.md` still uses old-form `Dict`,
`List`, `Optional`, `Union` annotations. They draft a wholesale
rewrite. The executor opens the file and finds it ALREADY uses
PEP 604/585 syntax in the "Type annotations" section (line 24-26
and 94-95) — the rewrite is a no-op.

**Why it happens:** The "Phase 3 D-22 step 5 deferral" framing in
CONTEXT.md D-12 implies the refresh hasn't happened. But Phase 3
Plan 03's UP cascade already touched the doc when it landed.
Verified live: lines 24-26 and 94-95 already say
"PEP 585 builtin generics" and "PEP 604 union syntax" with the
`dict[str, Any]` / `str | None` examples.

**Reality:** [VERIFIED: read CONVENTIONS.md] The body of the
"Type annotations" section IS already in modern syntax. The single
residual stale surface is **line 35**:
```
target-version = "py39"
```
inside the Ruff Configuration code block. This is a copy-paste
of the historical `[tool.ruff]` config — the live `pyproject.toml`
target-version is presumably `py310` post-Phase-1 PYVER-01.
**Verify and update line 35 if needed**; no other edits required.

**How to avoid:** Pre-task verification step: `grep -n
'Dict\[\|List\[\|Optional\[\|Union\[\|target-version' \
.planning/codebase/CONVENTIONS.md`. The grep should return only
line 35's `target-version = "py39"` (and any matches inside example
block prose, which can stay as illustrative). If the grep returns
the body-text Dict/List/etc. references, the doc was reverted —
do the wholesale refresh. If it returns only line 35, the task is a
**1-line edit**, not a wholesale rewrite. Keep the commit subject
honest: `docs(codebase): refresh CONVENTIONS ruff target-version
example to py310` if that's the only edit.

**Warning signs:** Plan task description estimates "rewrite the
entire Type annotations paragraph"; commit diff exceeds 5 lines.

### Pitfall 7: CHANGELOG bucket mismatch

**What goes wrong:** Planner instructs executor to add a
`refactor(core.deprecations): ...` commit's CHANGELOG entry under
`Misc:` instead of `Refactoring:`. Or adds an entry for a
`docs(05): ...` planning-artifact commit (which should NOT be in
the CHANGELOG at all per CLAUDE.md "Filter out planning-artifact
commits").

**Why it happens:** CLAUDE.md's bucket-mapping rule (`refactor:` →
Refactoring, `docs:` → Misc, etc.) is implicit; the executor may not
re-derive it for every commit.

**How to avoid:** Encode the bucket-per-commit mapping in the plan
task acceptance criteria. Per D-16:

| Commit | CHANGELOG Bucket | Entry shape |
|--------|------------------|-------------|
| 1. refactor(core.deprecations) | Refactoring | `[core.deprecations] Pin 3.0.10-1 and 3.0.16-1 removal version to v3.2.0` |
| 2. refactor(ext.logging) | Refactoring | `[ext.logging] Tighten FATAL deprecation removal version in docstrings` |
| 3. refactor(ext.smtp) | Refactoring | `[ext.smtp] Document send() bool-return removal in v3.2.0` |
| 4. docs (DEPRECATIONS.md) | Misc | `[docs] Add top-level DEPRECATIONS.md mirroring GitBook narrative` |
| 5. docs(sphinx) conf.py | Misc | `[docs] Drop unsupported 'logo' theme option from sphinx conf` |
| 6. docs(sphinx) toctree | Misc | `[docs] Wire api/index into top-level toctree` |
| 7. fix(core.interface) | Bugs | `[core.interface] String-quote list[str] return annotation for autodoc compatibility` |
| 8. docs(utils.shell) | Misc | `[docs] Fix inline-literal RST in shell.cmd() docstring` |
| 9. chore(make) | Misc | `[dev] Wire -W into make docs (zero-warnings gate)` |
| 10. docs(readme) | Misc | `[docs] Drop Travis CI link/badge (CI moved to GitHub Actions)` |
| 11. docs(contributing) | Misc | `[docs] Align CONTRIBUTING with Conventional Commits + atomic-per-concern` |
| 12. docs(<area>) | Misc (if any) | n/a — pre-verified 0 commits |
| 13. docs(codebase) | (none — planning-artifact) | DO NOT add — `.planning/` is planning intel, not user-visible |
| 14. docs(05) SECv2 | (none — planning-artifact) | DO NOT add — `.planning/REQUIREMENTS.md` is planning intel |

**Subtle point:** Commits 13 and 14 are `docs:` Conventional, but they
edit `.planning/` files, which CLAUDE.md filters out as
"planning-artifact commits". The bucket is "no entry", not "Misc".
This must be explicit in the plan.

**Warning signs:** A 14-row CHANGELOG diff (executor blindly added
all 14); a `[planning] ...` or `[.planning] ...` line in the
CHANGELOG (executor added an entry for the planning artifacts).

### Pitfall 8: GitBook anchor format mismatch in `DEPRECATIONS.md`

**What goes wrong:** Author writes the GitBook back-link as
`https://docs.builtoncement.com/release-information/deprecations#3-0-10-1`
(GitHub-style hyphen-slugged anchor). Round-trip navigation breaks
because the GitBook page anchors use the dotted format.

**Why it happens:** GitHub auto-converts `.` to `-` in markdown
heading anchors. A reader familiar with GitHub's convention may
assume the same applies on GitBook.

**Reality:** [VERIFIED: grep `cement/core/deprecations.py:15` and
`cement/core/foundation.py:610`] Cement's `deprecate()` helper emits
`#{deprecation_id}` literally — i.e., `#3.0.8-2`. GitBook accepts
the dot-separated form. The format is `<major>.<minor>.<patch>-<n>`.

**How to avoid:** In `DEPRECATIONS.md`, every back-link uses the
**exact deprecation ID** as the anchor:
```markdown
## 3.0.8-1
...
[GitBook reference](https://docs.builtoncement.com/release-information/deprecations#3.0.8-1)
```
NOT `#3-0-8-1`. Encode the literal string in the task acceptance
criteria.

**Warning signs:** Anchors with hyphens between version digits;
clicked back-link 404s on GitBook.

## Code Examples

> Verified patterns from existing project source. The examples below
> are minimal-diff replacement text the executor can use directly.

### Example 1: `cement/core/deprecations.py` — D-02 pin

[Source: `cement/core/deprecations.py` lines 4-9, current content]
```python
DEPRECATIONS = {
    '3.0.8-1': "Environment variable CEMENT_FRAMEWORK_LOGGING is deprecated in favor of CEMENT_LOG, and will be removed in Cement v3.2.0",  # noqa: E501
    '3.0.8-2': "App.Meta.framework_logging will be changed or removed in Cement v3.2.0",  # noqa: E501
    '3.0.10-1': "The FATAL logging facility is deprecated in favor of CRITICAL, and will be removed in future versions of Cement.",  # noqa: E501
    '3.0.16-1': "SMTPMailHandler.send() returning bool is deprecated. It will return the smtplib senderrs dict in a future version of Cement",  # noqa: E501
}
```

**Replacement (minimal-diff):**
```python
DEPRECATIONS = {
    '3.0.8-1': "Environment variable CEMENT_FRAMEWORK_LOGGING is deprecated in favor of CEMENT_LOG, and will be removed in Cement v3.2.0",  # noqa: E501
    '3.0.8-2': "App.Meta.framework_logging will be changed or removed in Cement v3.2.0",  # noqa: E501
    '3.0.10-1': "The FATAL logging facility is deprecated in favor of CRITICAL, and will be removed in Cement v3.2.0.",  # noqa: E501
    '3.0.16-1': "SMTPMailHandler.send() returning bool is deprecated. It will return the smtplib senderrs dict in Cement v3.2.0",  # noqa: E501
}
```

Diff: two lines changed; both swap "future versions/version of Cement"
for "Cement v3.2.0". Period preserved on `3.0.10-1` (it had one);
absent on `3.0.16-1` (it didn't).

### Example 2: `cement/ext/ext_logging.py:146-147` — set_level docstring

[Source: live file, lines 146-147]
```python
        As of Cement 3.0.10, the FATAL facility is deprecated and will be
        removed in future versions of Cement. Please us `CRITICAL` instead.
```

**Replacement (minimal-diff):**
```python
        As of Cement 3.0.10, the FATAL facility is deprecated and will be
        removed in Cement v3.2.0. Please use ``CRITICAL`` instead.
```

Three changes: (1) "future versions of Cement" → "Cement v3.2.0";
(2) "us" → "use" (typo carry-over); (3) single-backtick `CRITICAL` →
double-backtick (RST inline-literal — single backticks render as
emphasis in RST, not inline-literal). The `use` typo and backtick
fix are both inline cleanups; if the planner wants strictest scope,
they can defer #2 and #3 — but they're zero-risk and keep the
adjacent docstring sweep clean.

### Example 3: `cement/ext/ext_logging.py:368-369` — fatal() docstring

[Source: live file, lines 368-369]
```python
        As of Cement 3.0.10, this method is deprecated and will be removed in
        future versions of Cement. Please us `critical()` instead.
```

**Replacement (minimal-diff):**
```python
        As of Cement 3.0.10, this method is deprecated and will be removed in
        Cement v3.2.0. Please use ``critical()`` instead.
```

Same three changes as Example 2.

### Example 4: `cement/ext/ext_smtp.py` — send() docstring add deprecation note

[Source: live file, lines 116-158, focus on the `Returns:` block at
140-141]
```python
        Returns:
            bool:``True`` if message is sent successfully, ``False`` otherwise

        Example:
```

**Replacement (minimal-diff, adds Deprecated note before Example):**
```python
        Returns:
            bool: ``True`` if message is sent successfully, ``False`` otherwise

        .. deprecated:: 3.0.16
            The ``bool`` return is deprecated and will change to the
            ``smtplib`` senderrs ``dict`` in Cement v3.2.0. See
            ``DEPRECATIONS['3.0.16-1']``.

        Example:
```

Notes:
- Inserted blank line + `.. deprecated::` directive (RST/Sphinx
  built-in; renders as a "Deprecated since version 3.0.16" admonition
  in autodoc output).
- Also fixes the `bool:` formatting (was `bool:``True``` with no
  space) — minor docstring rendering improvement; zero-risk.
- Existing `# Deprecation: bool return will change to senderrs dict`
  comment at lines 189-190 stays (it's the runtime callsite anchor,
  not the docstring).

### Example 5: `cement/utils/shell.py:35-39` — cmd() docstring RST fix

[Source: live file, lines 35-39]
```python
        tuple: When ``capture==True``, returns the ``(stdout, stderror,
            return_code)`` of the command. ``stdout`` and ``stderror`` are
            ``bytes`` (the ``Popen`` default); decode with the appropriate
            encoding if string output is needed, or pass ``text=True`` /
            ``encoding=...`` through ``**kwargs``.
```

**Replacement (minimal-diff):**
```python
        tuple: When ``capture==True``, returns the ``(stdout, stderror,
            return_code)`` of the command. ``stdout`` and ``stderror`` are
            ``bytes`` (the ``Popen`` default); decode with the appropriate
            encoding if string output is needed, or pass ``text=True`` or
            ``encoding=...`` through ``**kwargs``.
```

Single change: `` / `` between the two inline literals → `` or ``.
The slash was the docutils trip; `or` is the simplest separator that
parses cleanly. NOTE: identical reasoning applies to the same prose
in `exec_cmd()` docstring at lines 88-91 — but that one is NOT in
the live warning list (no `:docstring of cement.utils.shell.exec_cmd`
warning currently). The planner can either fix only the cmd()
instance (strictest scope, matches D-08 #4 wording exactly) or do
both at once for consistency. CONTEXT.md D-08 #4 names only `cmd()`;
defer the exec_cmd parallel fix to Pitfall 9 below.

### Example 6: `cement/core/interface.py:102` — D-08 #3 string-quote

[Source: live file, line 102]
```python
    def list(self) -> list[str]:
```

**Replacement (CONTEXT.md D-08 #3 wording — string-quote):**
```python
    def list(self) -> "list[str]":  # autodoc: PEP 585 + method-name-shadow workaround
```

Notes:
- The string-quote defers annotation evaluation past method-name
  binding, so autodoc's `inspect.signature()` introspection no longer
  attempts `list[str]` against `self.list` (the method object).
- Inline `# autodoc: ...` comment is grep-able per CONTEXT.md
  Discretion item.
- Audit-public-api safe: AST script enumerates names only, never
  serializes annotations. [VERIFIED via simulation]

**Alternative (sibling-consistent, if the planner picks Open Q1
option B):**
```python
import builtins  # add at top of file (line ~5)
...
    def list(self) -> builtins.list[str]:  # autodoc: PEP 585 + method-name-shadow workaround (matches hook.py / handler.py / extension.py)
```

This requires a baseline rebase (adds `cement.core.interface:builtins`
to the audit output). Single line edit to
`.planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt`.

### Example 7: `Makefile` `docs:` target with `-W`

[Source: live `Makefile` lines 62-66]
```makefile
docs:
	cd docs; pdm run sphinx-build ./source ./build; cd ..
	@echo
	@echo DOC: "file://"$$(echo `pwd`/docs/build/html/index.html)
	@echo
```

**Replacement (D-09 — adds `-W` + AUDIT POINT comment):**
```makefile
docs:
	# AUDIT POINT: -W enforces zero docs warnings. If a future
	# warning is acceptable, suppress it explicitly via conf.py
	# suppress_warnings rather than reverting -W. Mirrors Phase 1
	# D-08 / Phase 2 D-10 (no implicit drift).
	cd docs; pdm run sphinx-build -W ./source ./build; cd ..
	@echo
	@echo DOC: "file://"$$(echo `pwd`/docs/build/html/index.html)
	@echo
```

### Example 8: `DEPRECATIONS.md` per-block format (D-07)

```markdown
# Cement Deprecations

This document mirrors the canonical GitBook narrative at
[docs.builtoncement.com/release-information/deprecations](https://docs.builtoncement.com/release-information/deprecations)
for in-repo discoverability. Each deprecation has an H2 section with
its registry ID. New IDs append at the bottom under their
since-version section.

For runtime behavior, the `cement.core.deprecations.deprecate()`
helper emits a `DeprecationWarning` whose message includes a
back-link to the corresponding GitBook anchor.

## 3.0.8-1

**Surface:** Environment variable `CEMENT_FRAMEWORK_LOGGING`
**Since:** Cement 3.0.8
**Removal:** Cement v3.2.0

Use `CEMENT_LOG` instead. Single-pass migration:

```bash
# Before
export CEMENT_FRAMEWORK_LOGGING=true

# After
export CEMENT_LOG=true
```

[GitBook reference](https://docs.builtoncement.com/release-information/deprecations#3.0.8-1)

## 3.0.8-2

**Surface:** `App.Meta.framework_logging`
**Since:** Cement 3.0.8
**Removal:** Cement v3.2.0

Will be changed or removed. The current attribute path is preserved
through 3.0.x but plan to migrate to the `CEMENT_LOG` environment
variable surface (see `3.0.8-1`).

[GitBook reference](https://docs.builtoncement.com/release-information/deprecations#3.0.8-2)

## 3.0.10-1

**Surface:** `cement.ext.ext_logging.LoggingLogHandler.fatal()` /
`set_level('FATAL')`
**Since:** Cement 3.0.10
**Removal:** Cement v3.2.0

Use `critical()` / `set_level('CRITICAL')` instead.

```python
# Before
app.log.fatal('something broke')
app.log.set_level('FATAL')

# After
app.log.critical('something broke')
app.log.set_level('CRITICAL')
```

[GitBook reference](https://docs.builtoncement.com/release-information/deprecations#3.0.10-1)

## 3.0.16-1

**Surface:** `cement.ext.ext_smtp.SMTPMailHandler.send()` return type
**Since:** Cement 3.0.16
**Removal:** Cement v3.2.0

The `bool` return value is deprecated; in v3.2.0 the method will
return the `smtplib` senderrs `dict` (see
[smtplib docs](https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.send_message)).

```python
# Before (3.0.x)
ok = app.mail.send('hello')
if not ok:
    handle_error()

# After (3.2.0+)
errs = app.mail.send('hello')
if errs:
    handle_error_per_recipient(errs)
```

[GitBook reference](https://docs.builtoncement.com/release-information/deprecations#3.0.16-1)
```

### Example 9: `.github/CONTRIBUTING.md` — replacement for the
"Guidelines for Code Contributions" section (D-10)

[Source: live `.github/CONTRIBUTING.md` lines 33-80]

**Replacement** (full section; preserves the `[Open Source Initiative]`,
`[issue tracker]`, `[PEP8]`, `[Commit Guidelines]` link references at
the bottom of the file):
```markdown
## Guidelines for Code Contributions

All contributors should attempt to abide by the following:

- Contributors fork the project on GitHub onto their own account
- All changes should be committed and pushed to their repository
- All pull requests are from a topic branch, not an existing Cement
  branch
- Contributors make every effort to comply with [PEP8]
- Before starting on a new feature or bug fix, do the following:
    - `git pull --rebase` to get latest changes from upstream
    - Checkout a new branch. For example:
        - `git checkout -b feature/slug-name`
        - `git checkout -b bug/github-issue-number`
- Code must include the following:
    - All tests pass successfully (`make test`)
    - Coverage reports 100% code coverage (`make test`)
    - Compliance passes (`make comply` — runs `ruff` and `mypy`)
    - New features are documented in the appropriate API docstring
    - User-visible changes are recorded in `CHANGELOG.md` under the
      active development section, in one of the standard buckets
      (`Bugs`, `Features`, `Refactoring`, `Misc`, `Deprecations`)
- All contributions should be associated with at least one issue in
  GitHub. If the issue does not exist, create one (per the
  guidelines above).
- Contributors should add their full name or handle to the
  `CONTRIBUTORS` file.

### Commit Conventions

Cement follows [Conventional Commits] for all commit messages.
Commits are atomic per concern — one logical change per commit, not
"a single commit per issue" (which often lumps unrelated edits).

- **Subject line:** `<type>(<area>): <imperative summary>`
  (max 78 chars)
- **Type:** `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`
- **Body:** wrap at 78 chars; explain the *why*, not just the *what*
- **Authoring:** Run `make commit` to use the project's
  `commitizen` (`cz`) interactive prompt. It enforces the format and
  the wrap.

Example:
```
fix(ext.smtp): correct timeout passed as local_hostname

The SMTP/SMTP_SSL constructors take ``timeout`` as the second
positional argument and ``local_hostname`` as a keyword. The
previous code passed ``timeout`` positionally where Popen-style
ordering happened to align with ``local_hostname`` for some
overloads, masking the bug under tests.

Resolves #1234.
```

See [`CLAUDE.md`](../CLAUDE.md) §"Commit Conventions" for the
canonical commit-shape doc.

[Conventional Commits]: https://www.conventionalcommits.org/
```

(Reference link target `[Conventional Commits]` added at the bottom
of the existing reference link block.)

### Example 10: `.planning/REQUIREMENTS.md` SECv2-01..03 expansion (D-13/D-14)

[Source: live `REQUIREMENTS.md` lines 89-94]
```markdown
### Security Audit Tooling Implementation

- **SECv2-01**: `pip-audit` integrated into CI on every PR
- **SECv2-02**: `bandit` integrated into CI on every PR with project-tuned ruleset
- **SECv2-03**: SAST tool (CodeQL or Semgrep) selected and integrated into CI
- **SECv2-04**: Documented security disclosure process (`SECURITY.md`)
```

**Replacement** (expand the first three; leave SECv2-04 untouched
per D-13):

```markdown
### Security Audit Tooling Implementation

- **SECv2-01**: `pip-audit` integrated into CI on every PR
    - **Tool:** `pdm run pip-audit` (read deps from `pdm.lock`)
    - **Make target:** `make audit-deps` — independent target, NOT
      chained into `make test` or `make comply` (matches Phase 03
      D-03 `audit-public-api` discipline)
    - **CI placement:** new dedicated workflow file
      `.github/workflows/security.yml`, triggers on `pull_request`
      + weekly `cron`. NOT serialized into `build_and_test.yml`
      (mirrors Phase 02 D-16 fail-fast vs feedback-time tradeoff)
    - **Config:** none initially; `pip-audit --skip` for accepted
      CVEs documented inline if any surface
    - **New dev-dep:** `pip-audit` (PyPI; latest stable)
    - **Exit behavior:** advisory on first run (Phase 02 D-03
      one-shot precedent — capture accepted CVEs in an in-repo
      artifact mirroring `02-PIP-AUDIT.md`); flip to blocking once
      baseline is clean
    - **Anchor:** `.planning/phases/02-dependencies-ci-pipeline/02-CONTEXT.md`
      D-03 + `02-PIP-AUDIT.md` capture artifact

- **SECv2-02**: `bandit` integrated into CI on every PR with project-tuned ruleset
    - **Tool:** `pdm run bandit -r cement/`
    - **Make target:** `make audit-bandit` — independent target
    - **CI placement:** same `.github/workflows/security.yml` lane
      as SECv2-01 (one workflow, three jobs)
    - **Config:** `.bandit` allowlist file at repo root —
      project-tuned to skip false positives on framework-intentional
      patterns (e.g., `subprocess` call sites in `cement/utils/shell.py`
      that are deliberate per the public API contract)
    - **New dev-dep:** `bandit` (PyPI; latest stable)
    - **Exit behavior:** advisory on first run; flip to blocking
      once `.bandit` allowlist is curated
    - **Anchor:** `02-CONTEXT.md` D-03 (same one-shot precedent)

- **SECv2-03**: SAST tool (CodeQL or Semgrep) selected and integrated into CI
    - **Tool:** TBD per evaluation; candidates are CodeQL (GitHub-
      native, free for public repos, deeper Python rules) and
      Semgrep (rule customization, more permissive licensing)
    - **Make target:** `make audit-sast` (only if CLI-runnable;
      CodeQL is GitHub-Actions-only)
    - **CI placement:** dedicated job in `security.yml`; weekly
      cron preferred over per-PR (run-time cost)
    - **Config:** `.semgrep.yml` (Semgrep) OR
      `.github/codeql/codeql-config.yml` (CodeQL) — rule selection
      pinned to Python OWASP top-N + cement-specific patterns
    - **New dev-dep:** `semgrep` if Semgrep selected; none if
      CodeQL (GitHub-hosted)
    - **Exit behavior:** advisory on first run; per-finding triage
      before any blocking flip
    - **Anchor:** `02-CONTEXT.md` D-03

- **SECv2-04**: Documented security disclosure process (`SECURITY.md`)
```

(SECv2-04 line stays as-is per D-13 — distinct concern, separate
future-milestone work.)

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `Dict[str, Any]`, `List[str]`, `Optional[str]`, `Union[int, str]` | `dict[str, Any]`, `list[str]`, `str \| None`, `int \| str` (PEP 604/585) | Phase 03 Plan 03 (UP006/UP007/UP045 ruff cascade); Python 3.10 floor in Phase 1 | `.planning/codebase/CONVENTIONS.md` body already in the new form. D-12 closeout is a 1-line ruff `target-version` example fix at line 35 (or no-op if already updated). |
| `from __future__ import annotations` (file-level deferred eval) | Direct PEP 585/604 generics + targeted PEP 484 string-quoting at definition-time-evaluated sites | Phase 03 Plan 04 (D-08 file-level removal across cement/) | The string-quote in `interface.py:102` is a **local** workaround for a **method-name-shadow** issue — NOT a file-level rollback. Inline `# autodoc:` comment makes the rationale grep-able. |
| Single `html_theme_options` dict per Sphinx convention | Two competing dicts (line 19 + line 51); second wins | Pre-cement-3.0.0 — long-standing latent bug | D-08 #1 fix is to delete the duplicate (lines 51-53), not just the `'logo'` key. (Pitfall 2.) |
| `.travis.yml` + Travis CI badges | GitHub Actions workflows (`build_and_test.yml`, `pdm.yml`, etc.) | Phase 1 (`.travis.yml` deleted) + Phase 2 (CI matrix on GitHub Actions) | README.md still has the link/badge (line 5 + line 60); D-10 drops both. |
| "Single commit per issue" CONTRIBUTING guidance | Atomic per concern + Conventional Commits + 78-char wrap + `make commit` (cz) | Phases 1-3 established the discipline through D-04/D-22/D-17 patterns | D-10 second commit aligns CONTRIBUTING.md with the actual project discipline. |

**Deprecated/outdated (in repo today, due for removal in Phase 5):**
- README.md `[![Continuous Integration Status]](https://app.travis-ci.com/...)` badge (line 5).
- README.md `[Travis CI](https://travis-ci.org/datafolklabs/cement/)` link (line 60).
- `.github/CONTRIBUTING.md` "A single commit per issue" guidance (line 55).
- `docs/source/conf.py` lines 51-53 (duplicate `html_theme_options` with unsupported `'logo'` key).
- `docs/source/api/index.rst` (orphan file; consider deleting per Pitfall 4 option (a)).

## Assumptions Log

> All claims in this RESEARCH.md were verified against the live
> repo state, the existing planning intel, or by simulation. The
> table below records claims that lean on assumed external
> behavior (Sphinx, GitBook, third-party tooling) — these are not
> "unverified" but they're worth flagging.

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `sphinx_rtd_theme` 3.1.0 will continue rejecting the `'logo'` theme option as unsupported in future versions [ASSUMED — verified against current 3.1.0 build only] | Pitfall 2, Example 7 | Low — even if 3.1.x adds `'logo'` support, the Phase 5 fix is to delete the duplicate dict, not the `'logo'` key. The duplicate clobbering line 19's config is the actual bug. |
| A2 | GitBook accepts dotted-version anchors (`#3.0.8-1`) as the canonical anchor format [VERIFIED via existing live-site usage by `cement/core/deprecations.py:15` `deprecate()` URL] | Pitfall 8, Example 8 | Low — the `deprecate()` runtime warning has been emitting this URL since Cement 3.0.8. Downstream users have been clicking these for years. |
| A3 | `make audit-public-api` baseline file at `.planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt` is the authoritative public-API surface, byte-for-byte [VERIFIED — `make audit-public-api` exits 0 with empty diff against live `pdm run python scripts/audit-public-api.py` output] | Pitfall 1, Example 6 | None — verified live. |
| A4 | The 4 sphinx warnings reproduce verbatim against `sphinx-build 8.1.3` + `sphinx_rtd_theme 3.1.0` [VERIFIED 2026-05-07] | Summary, Pitfalls 2-5 | None — verified live. If a future Sphinx upgrade surfaces additional warnings, the `-W` gate will catch them at the next `make docs` run. |
| A5 | DOCS-04 grep `grep -rn -i 'travis\|python 3\.9\|setup\.py' cement/ --include='*.py'` returns 0 docstring hits [VERIFIED 2026-05-07] | Summary, Pitfall 6, Example for D-11 | None — verified live. If a future commit reintroduces a stale reference before phase 5 lands, re-run the grep at executor-time. |
| A6 | `.planning/codebase/CONVENTIONS.md` is already in PEP 604/585 form except for line 35's ruff `target-version = "py39"` example [VERIFIED — read CONVENTIONS.md] | Pitfall 6 | None — verified live. The "deferred CONVENTIONS refresh" framing in CONTEXT.md D-12 turns out to be largely already-done. |

**If this table is empty:** N/A — 6 entries above; all VERIFIED.

## Open Questions

### 1. Should D-08 #3 use string-quote (CONTEXT.md) OR `import builtins` (sibling-consistent)?

- **What we know:** CONTEXT.md D-08 #3 specifies `def list(self) -> "list[str]":` (string-quote). The codebase has an established sibling-consistent pattern for the same problem: `import builtins` + `def list(self) -> builtins.list[T]` in `cement/core/{hook,handler,extension}.py` (verified). Both fixes resolve the autodoc warning.
- **What's unclear:** CONTEXT.md picks string-quote with the rationale "no baseline rebase". The `builtins` pattern would add `cement.core.interface:builtins` to the audit output, requiring a 1-line baseline edit. Is the sibling-consistency worth the rebase?
- **Recommendation:** Follow CONTEXT.md verbatim — string-quote — because:
    1. The decision is locked in CONTEXT.md (the planner must not re-decide).
    2. The string-quote is fully scope-local (single character pair); no import added; no audit baseline to rebase.
    3. The inline `# autodoc:` comment is grep-able for future cleanup.
- **Escalation path:** If the executor or the user objects to the inconsistency with the sibling files, a follow-up commit can refactor all four (`interface.py` + the three siblings) to a single convention in a future quick task. NOT this phase's scope.

### 2. Pitfall 4 toctree fix: option (a) delete vs. option (b) `:hidden:`?

- **What we know:** Both options resolve the warning. Option (a) deletes `docs/source/api/index.rst` (one less file in the repo). Option (b) preserves `api/index.rst` and adds a `:hidden:` toctree to `docs/source/index.rst`.
- **What's unclear:** Are there any external links pointing at `docs/build/html/api/index.html` (e.g., from the GitBook site, README, or third-party docs)? If yes, option (a) breaks those links.
- **Recommendation:** Pre-flight check: `grep -rn 'api/index' .planning/ docs/ README.md` to find references. If the only references are within `docs/source/` itself (the parent toctree), option (a) is safe. Otherwise, default to option (b) for link-preservation.
- **Default if no escalation:** option (a) — smaller diff, matches CONTEXT.md "planner picks the cleaner shape" Discretion text.

### 3. Should the DOCS-04 sweep grep extend to `tests/` and `scripts/`?

- **What we know:** CONTEXT.md D-11 specifies `cement/ --include='*.py'`. Pre-verified 0 hits in `cement/`.
- **What's unclear:** Does the sweep semantically extend to `tests/` (test docstrings) and `scripts/` (audit-public-api.py docstring, cli-smoke-test.sh comments)?
- **Recommendation:** Stay strict to CONTEXT.md scope (`cement/` only). Tests and scripts are dev-internal; a stale reference there doesn't ship to downstream users. If the user wants to expand scope, they can request a follow-up quick task.
- **Default:** scope locked to `cement/` per CONTEXT.md.

### 4. Does the planner need to file a follow-up planning entry for the deferred items?

- **What we know:** CONTEXT.md `<deferred>` lists 9 deferred items (yaml.load, shell=True, fs.Tmp.dir/.file, doctest sample, CI integration of `make docs -W`, Cement 4 README signaling, .planning/backlog/ convention, SECURITY.md, README walkthrough verification).
- **What's unclear:** Does Phase 5 land tracking entries for these in REQUIREMENTS.md v2 or a new file, or does it rely on `<deferred>` in CONTEXT.md as the system-of-record?
- **Recommendation:** No new tracking entries this phase. CONTEXT.md `<deferred>` is the canonical record per Phase 4 precedent (manual close with note). Future milestones discover deferreds via `grep -rn '<deferred>' .planning/phases/`.
- **Default:** CONTEXT.md `<deferred>` IS the system-of-record. No additional tracking work in Phase 5.

## Environment Availability

> Verified 2026-05-07 against the local devbox + pdm venv.

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `sphinx-build` | DOCS-01 build | ✓ | 8.1.3 | — |
| `sphinx_rtd_theme` | conf.py | ✓ | 3.1.0 | — |
| `pdm` | All `pdm run` invocations | ✓ | (devbox-pinned) | — |
| `pytest` | `make test` | ✓ | 9.0.x | — |
| `ruff` | `make comply-ruff` | ✓ | 0.15.x | — |
| `mypy` | `make comply-mypy` | ✓ | 1.20.x | — |
| `cz` (commitizen) | `make commit` | ✓ | (pinned) | hand-format `git commit` (CLAUDE.md Discretion) |
| `make` | All Makefile targets | ✓ | — | — |
| `git` | Commits | ✓ | — | — |
| `python` (3.10+) | All script execution | ✓ | 3.10–3.14 matrix | — |

**Missing dependencies with no fallback:** None.

**Missing dependencies with fallback:** None.

**Doc-only phase:** No external service / runtime / database dependencies.

## Validation Architecture

> `nyquist_validation: true` per `.planning/config.json`. Phase 5 is
> doc-only — validation is grep assertions, build exits, and existing
> test/audit gates. No new test files needed (DEPREC-03 already-
> satisfied).

### Test Framework

| Property | Value |
|----------|-------|
| Framework | `pytest` 9.0.x + `pytest-cov` 7.x + `coverage` 7.13.x |
| Config file | `pyproject.toml` (`[tool.pytest.ini_options]`, `[tool.coverage.run]`, `[tool.coverage.report]`) |
| Quick run command | `pdm run pytest --cov=cement.core tests/core` (core-only, ~10s) |
| Full suite command | `make test` (runs `make comply` then `pdm run pytest --cov=cement tests`) |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| DEPREC-01 | Each entry in `cement/core/deprecations.py:DEPRECATIONS` names a removal version | grep assertion | `grep -E '"3\.[0-9]+\.[0-9]+-[0-9]+":' cement/core/deprecations.py \| wc -l` returns 4; further `grep -c 'v3.2.0\|v4.0' cement/core/deprecations.py` returns 4 | ✅ live grep |
| DEPREC-01 | Existing deprecation tests still pass after pin tightening (regression hold) | unit | `pdm run pytest tests/core/test_deprecations.py -x` | ✅ exists |
| DEPREC-02 | `DEPRECATIONS.md` exists at repo root with one H2 per ID | grep | `test -f DEPRECATIONS.md && grep -cE '^## 3\.0\.' DEPRECATIONS.md` returns 4 | ❌ Wave 0 (file does not exist yet — created in commit 4) |
| DEPREC-02 | Each H2 block contains a GitBook back-link with the dotted-anchor format | grep | `grep -E 'docs.builtoncement.com/release-information/deprecations#3\.0\.' DEPRECATIONS.md \| wc -l` returns ≥4 | ❌ Wave 0 |
| DEPREC-03 | Each existing deprecation warning fires (no regression) | unit | `pdm run pytest tests/core/test_deprecations.py tests/ext/test_ext_smtp.py::TestSMTPMailHandler::test_send_returns_true_on_success -x` (and the other smtp test that hits 3.0.16-1) | ✅ exists |
| DOCS-01 | `make docs` exits 0 with `-W` enabled, zero warnings | shell exit | `make docs && echo OK` | ✅ Makefile target exists; D-09 flips the flag |
| DOCS-01 | All 4 known sphinx warnings resolved | grep | `make docs 2>&1 \| grep -iE 'warning' \| wc -l` returns 0 | ✅ live verification |
| DOCS-02 (a) | README contains no `travis-ci.org` or `app.travis-ci.com` reference | grep | `grep -E 'travis-ci' README.md \| wc -l` returns 0 | ✅ |
| DOCS-02 (b) | CONTRIBUTING references "Conventional Commits" and `make commit` | grep | `grep -cE 'Conventional Commits' .github/CONTRIBUTING.md` returns ≥1 AND `grep -c 'make commit' .github/CONTRIBUTING.md` returns ≥1 | ✅ |
| DOCS-04 (a) | Adjacent docstring sweep applied | grep | `grep -E 'removed in (Cement )?v3\.2\.0' cement/ext/ext_logging.py \| wc -l` returns ≥2 | ✅ |
| DOCS-04 (b) | Fix-on-find grep returns no docstring hits | grep | `grep -rn -i 'travis\|python 3\.9\|setup\.py' cement/ --include='*.py' \| wc -l` returns 0 | ✅ pre-verified live |
| DOCS-04 (c) | CONVENTIONS.md "Type annotations" body uses PEP 604/585 syntax | grep | `grep -nE 'PEP 585\|PEP 604\|str \| None\|dict\[str' .planning/codebase/CONVENTIONS.md \| wc -l` returns ≥2 | ✅ pre-verified |
| SEC-01/02/03 | REQUIREMENTS.md SECv2-01..03 are multi-line with all 6 D-14 properties | grep | `awk '/SECv2-01/,/SECv2-04/' .planning/REQUIREMENTS.md \| grep -cE 'Tool:\|Make target:\|CI placement:\|Config:\|New dev-dep:\|Exit behavior:'` returns ≥18 (6 properties × 3 stubs) | ❌ Wave 0 (REQUIREMENTS.md edit lands in commit 14) |
| All commits | `make audit-public-api` exit 0 (D-18 #3) | shell exit | `make audit-public-api && echo OK` | ✅ |
| All commits | `make comply` exit 0 (D-18 #2) | shell exit | `make comply && echo OK` | ✅ |
| All commits | `make test` exit 0 with 100% coverage (D-18 #1) | shell exit | `make test && echo OK` | ✅ |

### Sampling Rate

- **Per task commit:** `make comply` + `pdm run pytest --cov=cement.core tests/core` (quick) for source edits; `make docs` for any docs/* edit. ~30 seconds end-to-end.
- **Per "wave" (group of 3-4 related commits):** `make test` (full suite + coverage) + `make audit-public-api` + `make docs` (with `-W` once flipped). ~60 seconds.
- **Phase gate:** Full D-18 12-conjunct gate before `/gsd-verify-work` (all `make` targets + grep assertions + file existence checks).

### Wave 0 Gaps

- [ ] `DEPRECATIONS.md` does not exist yet — created in commit 4
  (no test file needed; grep assertion on the artifact suffices).
- [ ] No new framework/install needed — pytest/pytest-cov/coverage
  already wired.
- [ ] No new test files — DEPREC-03 already-satisfied;
  `tests/core/test_deprecations.py` and
  `tests/ext/test_ext_smtp.py:631` cover all 4 IDs.
- [ ] REQUIREMENTS.md SECv2-01..03 expansion is the artifact for
  SEC-01/02/03 — the test is a grep assertion against
  `.planning/REQUIREMENTS.md`, not a unit test.

*All gaps closed by commits 4 and 14 in the D-16 sequence.*

## Security Domain

> `security_enforcement` is not explicitly disabled in
> `.planning/config.json`, so treat as enabled. Phase 5 is
> documentation-only — there are no new code paths to threat-model
> against. The "security" surfaces this phase touches are:
> (a) the SECv2-01..03 stub expansion (planning intel, not runtime);
> (b) the deprecation-warning text (no escape-route or input
> handling).

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no | n/a — no auth surfaces in this phase |
| V3 Session Management | no | n/a |
| V4 Access Control | no | n/a |
| V5 Input Validation | no | n/a — `DEPRECATIONS.md` is read-only markdown; `DEPRECATIONS` dict is module-scope literal |
| V6 Cryptography | no | n/a |
| V7 Errors & Logging | partial | DeprecationWarning emission via `warnings.warn()` (stdlib) — already wired in `cement/core/deprecations.py:16`. Phase 5 only edits the message strings, not the emission mechanism. |
| V14 Configuration | partial | `Makefile` `-W` flag is a build-time hardening. AUDIT POINT comment per D-09 is the configuration-discipline anchor. |

### Known Threat Patterns for {stack}

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Stale URL in `DEPRECATIONS.md` GitBook back-link → user lands on 404 or wrong content | I (Information disclosure / wrong-info delivery) | Anchor format locked to `#3.0.X-Y` (verified against live `deprecate()` runtime URL); CONTEXT.md D-06 anchors on the same convention. |
| Markdown injection in `DEPRECATIONS.md` (e.g., user-controlled deprecation IDs in a future workflow) | T (Tampering) | Phase 5's `DEPRECATIONS.md` is hand-authored repo-root markdown; no user-input pipeline. Future automated generation (out of scope) would need to escape `<`, `>`, `_` in IDs — but IDs are constrained to `\d+\.\d+\.\d+-\d+` per the existing convention. |
| Sphinx build emits HTML with stale Travis CI link | I (Information disclosure / wrong-info) | D-10 drops both surfaces in README. `make docs` runs against `docs/source/`, NOT `README.md`, so the link does not propagate to API docs. |

**Phase 5 does NOT introduce any new attack surface.** The only
"security-domain" deliverable is the SECv2-01..03 stub expansion
(D-13/D-14) — which is **planning intel for a future security
milestone**, not runtime code.

## Sources

### Primary (HIGH confidence)

- **Live repo files** (verified 2026-05-07):
    - `cement/core/deprecations.py` (DEPRECATIONS dict, deprecate())
    - `cement/core/interface.py:102` (InterfaceManager.list)
    - `cement/core/{hook.py,extension.py,handler.py}` (sibling
      `builtins.list[T]` pattern)
    - `cement/core/foundation.py:608` (framework_logging — already
      correct, NOT in scope per D-04)
    - `cement/ext/ext_logging.py:140-167, 364-383` (set_level +
      fatal docstrings)
    - `cement/ext/ext_smtp.py:116-198` (send() docstring + line
      189-190 inline comment)
    - `cement/utils/shell.py:16-66` (cmd() docstring with RST
      issue at lines 35-39)
    - `docs/source/conf.py` (duplicate `html_theme_options`)
    - `docs/source/index.rst` + `docs/source/api/index.rst`
      (toctree)
    - `Makefile:62-66` (docs target)
    - `README.md:5,60` (Travis surfaces)
    - `.github/CONTRIBUTING.md:33-80` ("single commit per issue")
    - `.planning/codebase/CONVENTIONS.md:24-26,35,94-95` (PEP
      604/585 — already mostly done)
    - `.planning/REQUIREMENTS.md:91-94` (SECv2-01..03)
    - `.planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt:297-311`
      (interface.py audit baseline)
    - `CHANGELOG.md` `## 3.0.15 - DEVELOPMENT` (active section
      with 5 bucket headers)
    - `tests/core/test_deprecations.py:16,25,32` (3 of 4 ID
      assertions)
    - `tests/ext/test_ext_smtp.py:631` (3.0.16-1 assertion)

- **`scripts/audit-public-api.py`** — read in full; confirmed
  AST walker is annotation-blind.

- **`make docs` live build** — captured the 4 verbatim warnings:
    - `WARNING: Failed to get a method signature for cement.core.interface.InterfaceManager.list: 'function' object is not subscriptable`
    - `cement/utils/shell.py:docstring of cement.utils.shell.cmd:19: WARNING: Inline literal start-string without end-string. [docutils]`
    - `checking consistency... .../docs/source/api/index.rst: WARNING: document isn't included in any toctree`
    - `preparing documents... WARNING: unsupported theme option 'logo' given`
    - Build summary: `build succeeded, 4 warnings.`

- **CONTEXT.md** (`.planning/phases/05-deprecations-docs-security-stubs/05-CONTEXT.md`)
  — locked source of truth for all 18 D-numbered decisions.

- **CLAUDE.md** — project-wide constraint reference (Commit
  Conventions, Changelog Maintenance, Project Skills discovery).

- **`.planning/config.json`** — `nyquist_validation: true`,
  `model_profile: quality`, no `security_enforcement` override.

### Secondary (MEDIUM confidence)

- **Phase 1/2/3 CONTEXT and VERIFICATION docs** — referenced from
  CONTEXT.md `<canonical_refs>` for precedent (atomic-commit shape,
  AUDIT POINT pattern, audit-public-api gate, pip-audit one-shot
  precedent).

### Tertiary (LOW confidence)

- None — all claims in this research were verified against live
  repo state, simulation, or read of the canonical source.

## Metadata

**Confidence breakdown:**

- **Standard stack:** HIGH — versions verified live; no new deps.
- **Architecture (commit sequence + flow):** HIGH — D-16 is locked in
  CONTEXT.md; this research validated each step against live files.
- **Pitfalls:** HIGH — all 8 pitfalls were either reproduced live
  (Pitfall 1: AST simulation; Pitfalls 2-5: live build) or derived
  from VERIFIED reads of the source.
- **Code examples:** HIGH — every replacement string was drafted
  against the verbatim live source; minimal-diff intent preserved.
- **Validation architecture:** HIGH — every grep assertion was
  pre-run; every command path verified.
- **Open questions:** MEDIUM — Q1 (string-quote vs builtins) is a
  Discretion item; Q2 (toctree fix shape) is a Discretion item;
  Q3 (sweep scope) and Q4 (deferred-tracking) are conservative
  defaults the planner can confirm or override.

**Research date:** 2026-05-07

**Valid until:** 2026-06-07 (30 days; doc-only phase, no
fast-moving deps). Re-run the `make docs` warning capture and the
DOCS-04 grep at executor-time if the phase doesn't ship by 2026-05-21
(2 weeks) — between now and then, an unrelated commit could
introduce new docstring warnings or stale references.
