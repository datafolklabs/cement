# Phase 5: Deprecations, Docs & Security Stubs - Context

**Gathered:** 2026-05-07
**Status:** Ready for planning

<domain>
## Phase Boundary

Tighten removal-version language across the existing deprecation surface
(no new `DeprecationWarning` entries this milestone), refresh user-facing
in-repo docs (README, CONTRIBUTING.md, CHANGELOG entries; `make docs`
zero-warnings gate enforced via `-W`; new top-level `DEPRECATIONS.md`
mirroring the canonical GitBook narrative), close out Phase 3's deferred
PEP 604/585 refresh of `.planning/codebase/CONVENTIONS.md`, and expand
REQUIREMENTS.md `SECv2-01..03` with phase-shaped scope notes so a future
security-tooling milestone can pick up `pip-audit` / `bandit` / SAST
without re-discovery.

**In scope:**
- **Deprecation registry tightening (DEPREC-01):** Edit
  `cement/core/deprecations.py` so every `DEPRECATIONS` entry names its
  removal version. `3.0.10-1` and `3.0.16-1` get pinned to **v3.2.0**
  (matches the policy already locked into `3.0.8-1` / `3.0.8-2`). No new
  IDs added; no new `deprecate()` callsites; no new test cases (DEPREC-03
  already-satisfied — `tests/core/test_deprecations.py` covers 3 of 4 and
  `tests/ext/test_ext_smtp.py:631` covers `3.0.16-1`).
- **Adjacent docstring sweep (Area 1 D-04):** Tighten the *adjacent*
  docstrings whose vague language is the source of the registry-message
  vagueness:
  - `cement/ext/ext_logging.py:146-147` (`set_level` docstring; "removed in
    future versions of Cement" → "removed in v3.2.0")
  - `cement/ext/ext_logging.py:368-369` (`fatal()` docstring; same)
  - `cement/ext/ext_smtp.py` `send()` docstring — add a "Deprecated since
    3.0.16; bool return changes to senderrs dict in v3.2.0" note inline
    with the existing inline comment at line 189-190.
- **Top-level `DEPRECATIONS.md` (DEPREC-02 in-repo touchpoint):** New
  repo-root markdown file (sibling of `README.md`, `CHANGELOG.md`,
  `CONTRIBUTORS.md`). Per-deprecation block format (one section per ID:
  surface, since-version, removal-version, migration guidance, GitBook
  link). Mirrors the GitBook narrative for in-repo discoverability. NOT
  a sphinx page — see <decisions> D-05 for the docs-split rationale.
- **Sphinx zero-warnings gate (DOCS-01):** Fix all 4 known warnings:
  - `docs/source/conf.py` — drop the unsupported `'logo'` theme option
  - `docs/source/api/index.rst` — fold into `docs/source/index.rst` (or
    add a hidden toctree)
  - `cement/core/interface.py:102` — string-quote the return annotation
    on `InterfaceManager.list` to dodge the autodoc-vs-PEP-585
    name-shadow bug (preserves Phase 3 D-08 `from __future__ import
    annotations` removal — the string quote is local, not a file-level
    rollback)
  - `cement/utils/shell.py` `cmd()` docstring — fix the inline-literal
    RST around `text=True` / `encoding=...` (line 38-39 in the docstring)
  Then flip `Makefile` `docs:` target to `sphinx-build -W ./source ./build`
  so future docs warnings fail-fast (mirrors Phase 1 D-08 / Phase 2 D-10
  "no implicit drift" discipline).
- **README + CONTRIBUTING refresh (DOCS-02):** Two targeted edits, one
  commit per file:
  - `README.md` — drop the Travis CI link/badge (CI moved to GitHub
    Actions in Phase 2)
  - `.github/CONTRIBUTING.md` — replace the "single commit per issue"
    guidance with the project's actual discipline: Conventional Commits,
    atomic-per-concern, 78-char wrap, `make commit` (cz). Anchor on
    `CLAUDE.md` §"Commit Conventions".
- **Fix-on-find docstring sweep (DOCS-04):** No formal N-module sample
  — the Phase 5 work already touches the load-bearing docstrings (Area 1
  sweep + DOCS-01 source-code RST fix). In addition: grep
  `cement/**/*.py` for stale `Travis`, `setup.py`, `python 3.9`, and
  obvious year-stale references in docstrings and fix any hit. Not a
  comprehensive audit — the goal is "no obvious lies still shipped"
  (ROADMAP success criterion #4 sampling round-trip semantics).
- **Phase 3 deferred CONVENTIONS.md refresh (DOCS-04 closeout):** Update
  `.planning/codebase/CONVENTIONS.md` "Type annotations use full form"
  paragraph to PEP 604 (`X | None`) + PEP 585 (`list/dict/tuple/type`)
  syntax. In-repo planning intel only — not user-facing — but ties off
  Phase 3 D-22 step 5 / D-19 deferral. One commit:
  `docs(codebase): refresh CONVENTIONS to PEP 604/585 syntax`.
- **Security stub expansion (SEC-01..03):** Edit
  `.planning/REQUIREMENTS.md` `### Security Audit Tooling Implementation`
  section. Expand the existing one-liner `SECv2-01` (pip-audit),
  `SECv2-02` (bandit), `SECv2-03` (SAST) entries to multi-line
  phase-shaped scope notes per Area 4 D-09: tool command, Makefile/CI
  invocation target, where it runs (existing `build_and_test.yml` lane
  vs new workflow), config-file shape, new dev-dep, expected outputs,
  and the Phase 2 D-03 `pip-audit` one-shot precedent as the anchor. No
  new artifact files; no new GitHub issues; no `SECURITY.md` (that's
  `SECv2-04`, distinct concern, not in this phase's `SEC-01..03` mapping).
- **CHANGELOG entries:** Phase 5 lands `[core.deprecations]` Misc, `[docs]`
  Misc, and `[dev]` Misc lines into the active `## 3.0.15 - DEVELOPMENT
  (will be released as stable/3.0.16)` section as each commit lands —
  per CLAUDE.md §"Changelog Maintenance", phase-by-phase, not at
  release-cut time (Phase 6 owns DOCS-03).

**Out of scope:**
- Net-new `DeprecationWarning` callsites or `DEPRECATIONS` IDs — see Area
  1 D-01 ("None this phase"). The yaml.load() fallback, `shell=True`
  default in `cmd()`, and `fs.Tmp.dir/.file` str-vs-Path candidates are
  all deferred to a future milestone (see <deferred>).
- A `docs/source/deprecations.rst` sphinx page — explicitly OUT per the
  in-repo Sphinx-is-API-only rule (D-05). The literal wording in
  REQUIREMENTS.md DEPREC-02 is reinterpreted, NOT followed verbatim.
- `SECURITY.md` repo-root file — that's `SECv2-04`, scoped for the future
  security-tooling milestone, not Phase 5's SEC-01..03 trio.
- CHANGELOG cut and the 3.0.16 changelog body — Phase 6 work (DOCS-03).
- Walkthrough verification of README install/run path — already covered
  by the `cli-smoke-test` CI job (Phase 01.1 / Phase 2). Re-running it
  manually is duplicative.
- Comprehensive doctest sample on N representative modules — Area 3 D-08
  picked fix-on-find over a formal sample; the rigor cost would push the
  phase past its narrow shape.
- Forward-signaling Cement 4 in README/CONTRIBUTING — explicitly NOT
  picked in Area 3 D-07 (PROJECT.md "Out of Scope" already says this).
- TRIAGE-01..04 (Phase 4 — closed manually 2026-05-05).
- DOCS-03 (changelog cut for the 3.0.16 release — Phase 6).
- CI-04 / REL-01..05 (Phase 6 release-cut work).
- Public-API surface changes — D-01 in Phase 3 absolute. The
  `InterfaceManager.list` annotation string-quote (DOCS-01 fix) is a
  *type-hint* representation change, NOT a public-API change; the AST
  audit (Phase 3 D-04) tracks names and signatures, not annotation form.
- Mypy strictness knob tightening — Phase 3 D-10 still applies.

</domain>

<decisions>
## Implementation Decisions

### Deprecation target selection (Area 1)

- **D-01:** **No net-new `DeprecationWarning` entries this milestone.**
  Phase 5 surfaces only the 4 existing IDs (`3.0.8-1`, `3.0.8-2`,
  `3.0.10-1`, `3.0.16-1`). Three plausible candidates are explicitly
  deferred: (a) `yaml.load()` fallback in `cement/ext/ext_yaml.py:160`
  + `cement/ext/ext_generate.py:43`; (b) `shell=True` default in
  `cement/utils/shell.py:cmd()`; (c) `fs.Tmp.dir/.file` `str`-vs-`Path`
  flip. All three are real candidates flagged in
  `.planning/codebase/CONCERNS.md` but the user opted to lock the phase
  to documentation-only work. See <deferred>.
- **D-02:** **Audit + tighten existing messages.** Sweep
  `cement/core/deprecations.py` so every `DEPRECATIONS` entry names its
  removal version. `3.0.10-1` ("removed in future versions of Cement")
  and `3.0.16-1` ("future version of Cement") both get pinned to
  **v3.2.0**. `3.0.8-1` and `3.0.8-2` already say `v3.2.0` — left as-is.
  Lands as a single `refactor(core.deprecations): tighten
  removal-version language` commit. **DEPREC-03 already-satisfied** —
  no new test cases needed; existing assertions test by ID, not by
  message text.
- **D-03:** **Pin both vague messages → 3.2.0.** Aligns with the policy
  already locked into `3.0.8-1` and `3.0.8-2`. The 3.0.x track is
  no-breakage; 3.2.0 is the next breakage-allowed minor and the natural
  removal target. **NOT 4.0** — the user explicitly chose 3.2.0 for
  alignment over saving 3.0.16-1 for a bigger break. Acknowledged risk:
  retroactively pinning a long-vague deprecation (3.0.10-1, deprecated
  since Cement 3.0.10) to v3.2.0 narrows the previously-open horizon for
  downstream apps. Mitigated by the changelog entry making the change
  visible; downstream apps that have ignored the warning since 3.0.10
  have had ample time.
- **D-04:** **Adjacent-docstring sweep scope = registry + adjacent
  docstrings.** Beyond `cement/core/deprecations.py`, the audit also
  tightens these docstrings whose vague language motivated the registry
  vagueness:
  - `cement/ext/ext_logging.py:146-147` (`set_level` docstring)
  - `cement/ext/ext_logging.py:368-369` (`fatal()` docstring)
  - `cement/ext/ext_smtp.py` `send()` docstring — add a "Deprecated since
    3.0.16; bool return changes to senderrs dict in v3.2.0" note in the
    Returns section, paired with the existing inline `# Deprecation:
    bool return will change to senderrs dict` comment at line 189-190.
  One commit per file: `refactor(ext.logging): tighten FATAL deprecation
  removal version in docstrings`, `refactor(ext.smtp): document send()
  bool-return removal in v3.2.0`. Mirrors Phase 3 D-22 atomic-per-file
  shape. NOT in scope: rewriting the `framework_logging` docstring at
  `cement/core/foundation.py:608` — it already says `v3.2.0` correctly.

### deprecations.rst + DOCS-01 scope (Area 2)

- **D-05:** **No `docs/source/deprecations.rst` sphinx page.** The
  in-repo Sphinx site is **strictly API reference** per
  `docs/source/index.rst` ("This documentation is strictly for API
  reference. For more complete developer documentation, please visit
  the official site http://builtoncement.com."). Free-form developer
  docs — including deprecation narratives, migration guides, and release
  information — live on the GitBook site at `builtoncement.com`. The
  literal wording in `.planning/REQUIREMENTS.md` DEPREC-02 ("a dedicated
  `docs/source/deprecations.rst` page") was authored without this docs-
  split context and is **reinterpreted** here, not followed verbatim.
- **D-06:** **In-repo touchpoint = top-level `DEPRECATIONS.md` (sibling
  of `README.md`).** New repo-root markdown file. NOT a sphinx page; not
  inside `docs/source/`. Mirrors the canonical GitBook narrative for
  in-repo discoverability so a downstream developer reading the source
  tree finds it without needing to leave the repo. Anchor on the GitBook
  URL convention (`docs.builtoncement.com/release-information/
  deprecations#<id>`) — every entry includes a back-link to its GitBook
  anchor for round-trip navigation.
- **D-07:** **Per-deprecation block structure** in `DEPRECATIONS.md`.
  One H2 section per deprecation ID. Each section carries: surface
  (file:line + symbol), since-version, removal-version, migration
  guidance (concrete code-edit example), GitBook link. Stable structure
  — new IDs append at the bottom under their since-version section
  without re-grouping. Avoids the "regroup when removal pin moves"
  churn that the per-removal-version structure would create.
- **D-08:** **Fix all 4 sphinx warnings + wire `-W` permanently.**
  `make docs` flips from `sphinx-build ./source ./build` to
  `sphinx-build -W ./source ./build` so future warnings fail-fast.
  Mirrors Phase 1 D-08 (no implicit drift) + Phase 2 D-10/D-11 (belt-
  and-braces gate enforcement). Specific fixes:
  1. `docs/source/conf.py` — drop the unsupported `'logo'` key from
     `html_theme_options` (sphinx_rtd_theme rejected it as of 1.x).
  2. `docs/source/api/index.rst` — fold into `docs/source/index.rst`'s
     toctree (the orphan file currently isn't reachable). The simplest
     fix is to make `index.rst` reference `api/index` directly and
     delete the duplicate top-level toctree, OR add `:hidden:` toctree
     to absorb it; planner picks the cleaner shape.
  3. `cement/core/interface.py:102` — change
     `def list(self) -> list[str]:` → `def list(self) -> "list[str]":`.
     Method named `list` shadows the builtin in autodoc's introspection,
     so the unquoted PEP 585 generic tries to subscript the *method*.
     String-quoting defers evaluation. Phase 3 D-08 removed file-level
     `from __future__ import annotations` — this single-symbol string
     quote is a local workaround, NOT a file-level rollback. Add an
     inline `# autodoc: PEP 585 + method-name-shadow workaround` comment
     so it isn't "fixed" again in a future cleanup.
  4. `cement/utils/shell.py` `cmd()` docstring — fix the inline-literal
     RST around `text=True` / `encoding=...`. The slash between two
     adjacent inline literals (`` ``text=True`` / ``encoding=...`` ``)
     trips docutils. Reformat as separate sentences or use a different
     separator (e.g., "or").
  Lands as 4-5 atomic commits per Phase 3 D-22 shape.
- **D-09:** **`make docs` -W flag is permanent.** Not a one-shot
  verification — it stays in the Makefile so all subsequent docs builds
  enforce zero warnings. Documented inline with an AUDIT POINT-style
  comment (`# AUDIT POINT: -W enforces zero docs warnings; if a future
  warning is acceptable, suppress it explicitly via conf.py
  suppress_warnings`). Pattern carries from Phase 1 D-08 / Phase 2 D-10.

### DOCS-02/04 refresh depth (Area 3)

- **D-10:** **README + CONTRIBUTING — targeted edits only.** No
  walkthrough verification; the install/run path is already covered by
  the `cli-smoke-test` CI job (Phase 01.1 / Phase 2). No Cement 4
  forward-signaling additions (PROJECT.md "Out of Scope" already names
  Cement 4 as future work; no need to re-state in the README). Two
  commits:
  - `docs(readme): drop Travis CI link (moved to GitHub Actions)` —
    deletes the `[Travis CI](https://travis-ci.org/...)` line from
    `README.md` "More Information" section, plus the
    `app.travis-ci.com` badge near the top if still present.
  - `docs(contributing): align with Conventional Commits + atomic-per-
    concern discipline` — rewrite `.github/CONTRIBUTING.md` "Guidelines
    for Code Contributions" section: replace "single commit per issue"
    with "atomic per concern, Conventional Commits subject + 78-char
    wrap, `make commit` (cz)"; add a pointer to `CLAUDE.md` §"Commit
    Conventions" as the canonical commit-shape doc.
- **D-11:** **DOCS-04 = fix-on-find sweep, not formal sample.** No new
  Makefile target; no `pytest --doctest-modules` wiring. The DEPREC
  docstring tightening (D-04) already covers the load-bearing surfaces.
  Beyond that, run a grep sweep for stale references and fix anything
  that surfaces:
  ```bash
  grep -rn -i 'travis\|python 3\.9\|setup\.py\b' cement/ --include='*.py'
  ```
  Any docstring hit gets fixed in a `docs(<area>): drop stale <thing>
  reference` commit. **Acceptance:** the grep returns no docstring
  hits (code references — e.g., the `setup.py` template under
  `cement/cli/templates/generate/project/` — are excluded from the grep
  intent because they're scaffolding, not docstrings).
- **D-12:** **Phase 3 CONVENTIONS.md refresh lands here.** Update
  `.planning/codebase/CONVENTIONS.md` "Type annotations use full form:
  `Dict[str, Any]`, `Optional[str]`, `List[str]`, `Tuple[int, str]`"
  paragraph (and any other lingering full-form references) to PEP 604
  + PEP 585 syntax: `dict[str, Any]`, `str | None`, `list[str]`,
  `tuple[int, str]`. Single commit: `docs(codebase): refresh
  CONVENTIONS to PEP 604/585 syntax`. Closes the deferral path
  documented in Phase 3 D-22 step 5 / D-19. In-repo planning intel
  only — not GitBook, not user-facing.

### SEC-01/02/03 backlog stub format (Area 4)

- **D-13:** **In-place expansion in `.planning/REQUIREMENTS.md`.**
  REQUIREMENTS.md already has a `### Security Audit Tooling
  Implementation` section under v2 with one-liner entries `SECv2-01`
  (pip-audit), `SECv2-02` (bandit), `SECv2-03` (SAST), `SECv2-04`
  (`SECURITY.md`). Phase 5 expands the first three entries (NOT
  SECv2-04 — that's the separate "documented disclosure process"
  concern, mapped to `SECv2-04` only and out of `SEC-01..03` scope).
  No new file under `.planning/backlog/`; no new GitHub issues; no
  cross-referencing. Single source of truth in the planning tree.
- **D-14:** **Phase-shaped scope notes — tool + invocation + CI
  placement.** Each expanded entry contains:
  - Tool command (`pdm run pip-audit`, `pdm run bandit -r cement/`,
    SAST tool TBD per evaluation)
  - Makefile target name (`make audit-deps`, `make audit-bandit`,
    `make audit-sast`) — each independent, NOT chained into `make
    test` or `make comply` (mirrors Phase 3 D-03 audit-public-api
    discipline)
  - CI placement: existing `build_and_test.yml` lane vs new workflow.
    Default suggestion: new dedicated workflow file
    (`.github/workflows/security.yml`) running on `pull_request` +
    weekly cron, NOT serialized into the existing comply/test chain
    (mirrors Phase 2 D-16 fail-fast vs feedback-time tradeoff).
  - Config-file shape: e.g., `.bandit` (bandit allowlist),
    `.semgrep.yml` (rule selection), or equivalent for the chosen SAST
  - New dev-deps to add: `pip-audit`, `bandit`, SAST CLI (TBD)
  - Expected exit behavior (advisory vs blocking on first run; user
    chose Phase 2 D-03 "one-shot, document accepted CVEs" precedent
    for pip-audit — future milestone may flip to blocking once the
    baseline is clean)
  - Anchor: `.planning/phases/02-dependencies-ci-pipeline/02-CONTEXT.md`
    D-03 (one-shot pip-audit precedent) + `02-PIP-AUDIT.md` capture
    artifact pattern.
  ~6-10 lines per stub. Lean enough that the future-milestone discuss-
  phase can refine without pre-committing decisions; rich enough that
  no re-discovery is needed (ROADMAP success criterion #5).
- **D-15:** **Single commit for the SEC expansion.**
  `docs(05): expand SECv2-01..03 with phase-shaped scope notes` — one
  REQUIREMENTS.md edit covering all three. Atomic-per-concern shape;
  the *concern* is "make the security-tooling backlog actionable",
  which is one concern even though it touches three line items.

### Commit shape (carries Phase 1/2/3 conventions)

- **D-16:** **Atomic per-concern, Conventional Commits, 78-char wrap**
  (CLAUDE.md + Phase 1 D-02/D-04 + Phase 2 D-17 + Phase 3 D-22).
  Suggested commit sequence (planner refines order/granularity):
  1. `refactor(core.deprecations): tighten removal-version language`
     — pin 3.0.10-1 and 3.0.16-1 to v3.2.0 in `DEPRECATIONS` dict.
  2. `refactor(ext.logging): tighten FATAL deprecation removal version
     in docstrings` — set_level + fatal() docstring fixes.
  3. `refactor(ext.smtp): document send() bool-return removal in v3.2.0`
     — send() docstring note.
  4. `docs: add top-level DEPRECATIONS.md`
  5. `docs(sphinx): drop unsupported 'logo' theme option from conf.py`
  6. `docs(sphinx): wire api/index into top-level toctree`
  7. `fix(core.interface): string-quote list[str] return annotation
     for autodoc compatibility`
  8. `docs(utils.shell): fix inline-literal RST in cmd() docstring`
  9. `chore(make): wire -W into make docs (zero-warnings gate)`
  10. `docs(readme): drop Travis CI link (moved to GitHub Actions)`
  11. `docs(contributing): align with Conventional Commits + atomic-
      per-concern discipline`
  12. `docs(<area>): drop stale <thing> reference` — per docstring
      grep hit (zero or more)
  13. `docs(codebase): refresh CONVENTIONS to PEP 604/585 syntax`
  14. `docs(05): expand SECv2-01..03 with phase-shaped scope notes`
  Plus per-commit CHANGELOG entries appended to `## 3.0.15 -
  DEVELOPMENT (will be released as stable/3.0.16)` per CLAUDE.md
  §"Changelog Maintenance".
- **D-17:** **GSD artifact commits** follow `docs(05): ...` shape
  (mirrors Phase 1 / 01.1 / Phase 2 / Phase 3 patterns).

### Acceptance

- **D-18:** Phase 5 acceptance is the conjunction of:
  1. `make test` passes at 100% coverage (Phase 2 D-10 absolute gate
     stays green).
  2. `make comply` passes (ruff + mypy clean).
  3. `make audit-public-api` exits 0 — the
     `InterfaceManager.list` string-quote (D-08 #3) MUST NOT change
     the audit-public-api output. **Pre-flight verification:**
     before committing the change, run `make audit-public-api`,
     apply the change, rerun, and confirm the diff is empty.
     `audit-public-api.py` walks AST signatures; quoting an
     annotation may serialize differently — if so, address by
     baseline-update (planner judgment) since the public surface
     hasn't actually changed.
  4. `make docs` exits 0 with `-W` enabled — zero warnings, no
     broken cross-references (DOCS-01 success).
  5. `cement/core/deprecations.py` `DEPRECATIONS` dict: every entry
     names a removal version (`grep -E '"3\.[0-9]+\.[0-9]+-[0-9]+":'
     cement/core/deprecations.py` returns 4 lines, each containing
     either `v3.2.0` or `v4.0`).
  6. `tests/core/test_deprecations.py` and
     `tests/ext/test_ext_smtp.py:631` still assert each warning fires
     (DEPREC-03 already-satisfied; no regression).
  7. Repo root contains `DEPRECATIONS.md` with one H2 section per
     deprecation ID and a GitBook back-link in each section (DEPREC-02
     in-repo touchpoint).
  8. `README.md` no longer contains `travis-ci.org` or
     `app.travis-ci.com` (DOCS-02 part 1).
  9. `.github/CONTRIBUTING.md` references "Conventional Commits"
     and `make commit` (DOCS-02 part 2).
  10. `grep -rn -i 'travis\|python 3\.9' cement/ --include='*.py'`
      returns no docstring hits (DOCS-04 fix-on-find acceptance).
  11. `.planning/codebase/CONVENTIONS.md` "Type annotations" paragraph
      uses PEP 604/585 lowercase-builtin syntax (DOCS-04 closeout).
  12. `.planning/REQUIREMENTS.md` `SECv2-01..03` are multi-line entries
      with tool / invocation / CI placement / config / dev-dep / exit
      behavior (SEC-01/02/03 acceptance).

### Claude's Discretion

- Specific commit-message body phrasing within the D-16 sequence
  (planner picks).
- Order of `docs(sphinx): ...` commits within step 5-9 — they're
  independent fixes; planner can interleave.
- Whether the api/index.rst toctree fix (D-08 #2) is solved by
  fold-into-index OR by adding a `:hidden:` toctree — planner picks
  the smaller diff.
- Whether the docstring grep sweep (D-11) finds 0, 1, or N hits — if
  N, planner splits per file (D-16 step 12 may multiply).
- Whether to author commits via `make commit` (cz) or directly via
  `git commit` (either satisfies CLAUDE.md as long as the result
  matches Conventional Commits + 78-char wrap).
- Exact wording of inline `# autodoc:` comment in
  `cement/core/interface.py:102` (D-08 #3) — must be grep-able as
  "autodoc:" but text is open.
- Pre-flight `make audit-public-api` check around the
  `InterfaceManager.list` string-quote (D-18 #3) — if the AST
  serialization actually does change, planner decides whether to
  rebase the baseline or use a different workaround (e.g.,
  `:type:` annotation in the docstring instead of a return
  annotation).

### Folded Todos

None — `gsd-sdk list-todos` not invoked (workflow.cross_reference_todos
is unconfigured for this project per `quick/` directory inspection;
TODOs surface organically through ROADMAP/REQUIREMENTS instead).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project intent and constraints

- `.planning/PROJECT.md` — Core Value, no-breakage rule on 3.0.x
  (including subclass-exposed internals), Constraints block, Key
  Decisions table. **Out of Scope** specifically defers
  pip-audit/bandit/SAST CI rollout to a later milestone (Phase 5
  SEC-01..03 only stubs the backlog).
- `.planning/REQUIREMENTS.md` §"Documentation" (DOCS-01, DOCS-02,
  DOCS-04 — note DOCS-03 is Phase 6), §"Deprecations" (DEPREC-01..03),
  §"Security Audit Tooling (Stubbed)" (SEC-01..03), §"Security Audit
  Tooling Implementation" v2 (SECv2-01..04 — Phase 5 expands the first
  three).
- `.planning/ROADMAP.md` §"Phase 5: Deprecations, Docs & Security
  Stubs" — goal, dependencies (Phase 3), 5 success criteria,
  requirement mapping. D-18 acceptance criteria above map 1:1 against
  ROADMAP success criteria.
- `.planning/ROADMAP.md` §"Phase 6: Release Cut 3.0.16" — Phase 6
  scope (changelog cut DOCS-03, release work) deliberately out of
  Phase 5.

### Precedent — same project, same scope discipline

- `.planning/phases/01-tooling-baseline-python-matrix/01-CONTEXT.md`
  — D-02/D-04 atomic-commit shape, D-08 hybrid AUDIT POINT pattern
  (Phase 5 D-09 reuses for `-W`).
- `.planning/phases/02-dependencies-ci-pipeline/02-CONTEXT.md` —
  D-03 (`pip-audit` one-shot precedent — anchor for Phase 5 D-14
  `SECv2-01` expansion), D-10/D-11 (coverage gate; Phase 5 must
  preserve), D-17 commit-shape continuity.
- `.planning/phases/02-dependencies-ci-pipeline/02-PIP-AUDIT.md` —
  capture-artifact pattern for one-shot security-tool runs.
- `.planning/phases/03-internal-refactor-coverage-hardening/03-CONTEXT.md`
  — D-04 (audit-public-api gate that Phase 5 D-18 #3 rides on),
  D-08 (`from __future__ import annotations` removal — Phase 5 D-08
  #3 string-quote is local workaround NOT a file-level rollback),
  D-22 commit sequence shape.
- `.planning/phases/04-backlog-triage/04-NOTE.md` — manual-pass
  precedent showing GSD artifacts can be skipped when a single-pass
  hand-edit is the better tool. Phase 5 inverts: full GSD artifacts,
  but the SEC stub (D-13) lands as a single-line REQUIREMENTS.md edit
  consistent with that lighter shape.

### Existing codebase intel

- `.planning/codebase/CONVENTIONS.md` — Phase 5 D-12 refreshes this
  doc's "Type annotations" paragraph to PEP 604/585 syntax.
- `.planning/codebase/CONCERNS.md` §"Security Considerations",
  §"Deprecations in Flight" — flagged candidates that informed Area 1
  D-01 deferral (yaml.load fallback, shell=True default,
  fs.Tmp.dir/.file str-vs-Path).
- `.planning/codebase/STRUCTURE.md` — confirms `docs/source/` layout
  (`api/core`, `api/utils`, `api/ext` only) supporting D-05 sphinx-
  is-API-only rule.

### In-repo files this phase will touch

- **New (repo root):** `DEPRECATIONS.md` — top-level markdown,
  per-deprecation block format (D-07).
- **Modified (cement/):**
  - `cement/core/deprecations.py` — `DEPRECATIONS` dict version pins
    (D-02, D-03).
  - `cement/core/interface.py:102` — string-quote `list[str]` return
    annotation (D-08 #3).
  - `cement/ext/ext_logging.py:146-147,368-369` — adjacent docstring
    sweep (D-04).
  - `cement/ext/ext_smtp.py` `send()` docstring — adjacent docstring
    sweep (D-04).
  - `cement/utils/shell.py` `cmd()` docstring — inline-literal RST
    fix (D-08 #4).
  - Anything caught by the docstring grep sweep (D-11) — zero or N.
- **Modified (docs/):**
  - `docs/source/conf.py` — drop `'logo'` theme option (D-08 #1).
  - `docs/source/index.rst` and/or `docs/source/api/index.rst` —
    toctree wiring (D-08 #2).
- **Modified (config/repo-root):**
  - `Makefile` — `docs:` target → `sphinx-build -W ./source ./build`
    plus AUDIT POINT comment (D-09).
  - `README.md` — drop Travis CI badge + link (D-10).
  - `.github/CONTRIBUTING.md` — Conventional Commits alignment (D-10).
  - `CHANGELOG.md` — append entries to `## 3.0.15 - DEVELOPMENT`
    section per CLAUDE.md §"Changelog Maintenance".
- **Modified (.planning/):**
  - `.planning/codebase/CONVENTIONS.md` — PEP 604/585 refresh (D-12).
  - `.planning/REQUIREMENTS.md` `SECv2-01..03` — phase-shaped scope
    notes (D-13, D-14, D-15).
- **NOT modified:** `cement/core/foundation.py:608` (`framework_logging`
  docstring already says `v3.2.0` correctly); any net-new
  `deprecate()` callsite or `DEPRECATIONS` ID; `docs/source/*.rst`
  beyond conf.py + toctree wiring (sphinx is API-only — D-05);
  `SECURITY.md` (out of `SEC-01..03` scope; SECv2-04 is its own
  future-milestone concern).

### External docs and sites

- **GitBook (canonical developer narrative):**
  `docs.builtoncement.com/release-information/deprecations` — the
  `deprecate()` warning URL points here. Phase 5 does NOT modify the
  GitBook content; the user updates it off-band when version pins
  change.
- **Sphinx warnings reference:**
  - `'logo'` theme option deprecation:
    https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
  - Inline-literal start-without-end docutils warning:
    https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#inline-markup
  - Autodoc PEP 585 method-name-shadow gotcha tracked upstream at
    https://github.com/sphinx-doc/sphinx/issues — string-quote is the
    accepted workaround pattern.
- **Conventional Commits:** https://www.conventionalcommits.org/ —
  CONTRIBUTING.md alignment target (D-10).
- **PEP 604 / PEP 585:** https://peps.python.org/pep-0604/ +
  https://peps.python.org/pep-0585/ — CONVENTIONS.md refresh anchor
  (D-12).
- **pip-audit:** https://pypi.org/project/pip-audit/ — SECv2-01 stub
  expansion anchor.
- **bandit:** https://bandit.readthedocs.io/ — SECv2-02 stub
  expansion anchor.
- **CodeQL / Semgrep:** https://codeql.github.com/ +
  https://semgrep.dev/ — SECv2-03 evaluation candidates.

### Conventions

- `CLAUDE.md` §"Commit Conventions" — Conventional Commits, 78-char
  subject + body wrap, `make commit` (`pdm run cz commit`) for
  interactive authoring.
- `CLAUDE.md` §"Changelog Maintenance" — append entries to active
  `## 3.0.15 - DEVELOPMENT` section. Phase 5 produces:
  - `[core.deprecations]` removal-version pins (Refactoring or Misc)
  - `[ext.logging]` deprecation docstring tightening (Misc)
  - `[ext.smtp]` send() docstring deprecation note (Misc)
  - `[docs]` add DEPRECATIONS.md (Features or Misc — judgment call;
    new file, modest scope → Misc)
  - `[docs]` Sphinx zero-warnings gate (Misc)
  - `[docs]` README + CONTRIBUTING refresh (Misc)
  - `[dev]` make docs -W gate (Misc)
  Phase 5 lands these phase-by-phase, not at release-cut time
  (Phase 6 owns the changelog cut DOCS-03).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `cement/core/deprecations.py` `DEPRECATIONS` dict + `deprecate(id)`
  helper — established in 3.0.x. Phase 5 only edits string values, no
  new IDs, no new callsites, no helper signature change.
- `tests/core/test_deprecations.py` (3 tests) +
  `tests/ext/test_ext_smtp.py:631` (1 assertion) — DEPREC-03 is
  already-satisfied; no new test work needed.
- `make comply` / `make comply-ruff` / `make comply-mypy` /
  `make test` / `make audit-public-api` — existing entry points; no
  new make targets except the modified `docs:` target (D-09).
- Phase 2 `02-PIP-AUDIT.md` — existing capture-artifact for one-shot
  security tool runs; SECv2-01 stub references this as the precedent.
- Phase 3 `scripts/audit-public-api.py` + `make audit-public-api` —
  permanent dev affordance (Phase 3 D-05). Phase 5 D-18 #3 leans on
  this gate to verify the `InterfaceManager.list` string-quote doesn't
  change public surface.

### Established Patterns

- **Hybrid AUDIT POINT pattern** (Phase 1 D-08, reused Phase 2 D-12,
  Phase 3 D-06) — Phase 5 D-09 reuses for `make docs -W`.
- **Atomic-per-concern commits** (Phase 1 D-02/D-04, 01.1 D-15,
  Phase 2 D-17, Phase 3 D-22) — Phase 5 D-16 carries forward.
- **In-place ratification of "already-satisfied" requirements** —
  Phase 4 TRIAGE-01..04 set the precedent (manual pass, mark closed
  with note). Phase 5 DEPREC-03 follows the same shape (already-
  satisfied; CONTEXT.md notes it; no new work).
- **REQUIREMENTS.md re-interpretation when wording is mis-shaped** —
  not a prior-phase precedent; established here in D-05 for DEPREC-02.
  The pattern: surface the conflict in CONTEXT.md `<domain>`, document
  the reinterpretation in `<decisions>`, write the in-repo artifact in
  the correct shape (D-06: `DEPRECATIONS.md` not
  `docs/source/deprecations.rst`).
- **Coverage hold-the-line** (Phase 2 D-10/D-11, Phase 3) — every
  Phase 5 commit lands with `make test` green at 100% coverage.

### Integration Points

- **CI gate:** `.github/workflows/build_and_test.yml` runs `make
  comply` (ruff + mypy) + `make test` (pytest + coverage at 100%) +
  `cli-smoke-test` on every PR. Phase 5 must not regress any of these.
  `make docs` is NOT in CI today; D-09 wires `-W` for local fail-fast,
  not CI integration. (CI integration of docs build is a candidate for
  Phase 6 / a future milestone — not required for the 3.0.16 cut.)
- **Changelog flow:** Each Phase 5 commit appends a one-line entry to
  the active `## 3.0.15 - DEVELOPMENT` section in `CHANGELOG.md` per
  CLAUDE.md §"Changelog Maintenance". Phase 6 cuts the section header
  (DOCS-03 + REL-01) — Phase 5 does NOT.
- **GitBook integration:** `deprecate()` warning URL format is
  `https://docs.builtoncement.com/release-information/deprecations#<id>`
  — preserved across the registry tightening (D-02). Phase 5 does NOT
  modify the GitBook content; user updates off-band.

### Known refactor risk surfaces

- **`InterfaceManager.list` string-quote interaction with audit-public-
  api gate** (D-08 #3, D-18 #3): the AST-walk audit script may
  serialize `"list[str]"` differently from `list[str]` when emitting
  signature lines. Pre-flight verification REQUIRED — apply the change,
  run `make audit-public-api`, confirm exit 0. If the audit fails:
  either rebase the baseline (planner judgment, with an explicit
  rationale commit `docs(03): rebase audit-public-api baseline for
  string-quote workaround`) OR use an alternative workaround (e.g.,
  pull the return type into a Sphinx `:rtype:` directive in the
  docstring instead of a return annotation).
- **`ext_logging.py` `set_level` deprecation docstring change**: the
  docstring is autodoc'd into the API reference. Re-running `make
  docs -W` after the docstring edit MUST stay clean. Pre-flight: run
  the docstring edits BEFORE flipping `-W` so an unrelated docstring
  warning doesn't surprise the gate flip.
- **CONTRIBUTING.md "single commit per issue" change** (D-10): existing
  external contributor PRs may be in flight against the old
  guidance. The replacement language should preserve the spirit (one
  logical change per commit) while adopting Conventional Commits
  vocabulary. NOT a hard cut-over for in-flight PRs — the maintainer
  reviews the substance, the doc is forward-looking.

</code_context>

<specifics>
## Specific Ideas

- The user's framing on Area 2 was sharp and fast: "sphinx docs are
  strictly api code docs ... not developer/free-form docs" + "we have
  a gitbook site for developer docs, and deprecations are documented
  there." This drove D-05 (no `docs/source/deprecations.rst`) and D-06
  (top-level `DEPRECATIONS.md`). The constraint is durable across the
  Cement project — saved as a project-level memory note for future
  conversations.
- The user explicitly chose **lock the phase to documentation-only
  deprecation work** (Area 1 D-01) over picking any of the three
  plausible candidates I surfaced (yaml.load fallback, shell=True
  default, fs.Tmp.dir/.file str-vs-Path). All three remain viable
  candidates for a future milestone; Phase 5 deliberately doesn't
  pre-commit. Recorded in <deferred>.
- The user picked **3.2.0 for both vague pins** (Area 1 D-03) over
  staggering 3.0.16-1 to 4.0. Choice was about consistency with the
  existing `3.0.8-*` pins, not about minimizing breakage scope. Future-
  self note: if a downstream maintainer reports their app silently
  pinned around 3.0.10-1 expecting a long horizon and now sees
  v3.2.0, point them at the changelog entry as the visibility surface.
- The user picked **fix-on-find docstring sweep** (Area 3 D-11) over a
  formal `pytest --doctest-modules` sample. Matches their established
  preference for **strict-minimum boundaries** (Phase 1 D-13, Phase 3
  D-19) — don't volunteer scope unless a tool literally fails on it.
- The user picked **expand REQUIREMENTS.md SECv2-01..03 in place**
  (Area 4 D-13) over the GitHub-issues alternative (which Phase 4 used
  for triage). The distinction: triage was a one-shot live-state pass
  on real issue-tracker objects; SEC stubs are forward-looking
  planning entries that belong in the planning tree alongside the v1
  requirements they extend. Single-source-of-truth preserved.

</specifics>

<deferred>
## Deferred Ideas

- **`yaml.load()` fallback deprecation** — `cement/ext/ext_yaml.py:160`
  + `cement/ext/ext_generate.py:43` fall back to unsafe `yaml.load()`
  when `yaml.full_load` doesn't exist (PyYAML <5.1; shipped 2019).
  Flagged in `.planning/codebase/CONCERNS.md` as a security item.
  Future milestone may add a deprecation warning + a `pyyaml >= 5.1`
  optional-extras floor. Phase 5 D-01 explicitly defers.
- **`shell=True` default in `cement/utils/shell.py:cmd()`** —
  CONCERNS.md flagged. Modern best practice prefers list-based exec.
  A future milestone may deprecate the default with migration guidance
  to pass `shell=False` explicitly. Phase 5 D-01 explicitly defers.
- **`fs.Tmp.dir/.file` `str` → `pathlib.Path`** — public attrs return
  `str` per Phase 3 D-12 (boundary-preserving). A 4.0-direction
  warning would announce the flip to `Path`. Wide blast radius —
  widely used by downstream apps. Phase 5 D-01 explicitly defers; this
  is a Cement 4 candidate, not a 3.2.0 deprecation.
- **`pytest --doctest-modules` sample on representative modules** —
  Area 3 D-11 picked fix-on-find over a formal sample. Future
  milestone may add the doctest sample as a permanent regression gate
  (`make docs-doctest`) once the docstring surface is closer to
  doctest-clean.
- **CI integration of `make docs` (`-W`)** — D-09 wires `-W` locally
  but does NOT add `make docs` to `.github/workflows/build_and_test.yml`.
  Future milestone (likely Phase 6 or a follow-up) may add it as a
  separate CI lane. Phase 5 keeps the gate local-only.
- **Cement 4 forward-signaling in README/CONTRIBUTING** — Area 3 D-10
  rejected. PROJECT.md "Out of Scope" already says Cement 4 is future
  work; no need to re-state in the README. Future milestone (likely
  the Cement 4 kickoff) is the natural home.
- **`.planning/backlog/` directory convention** — Area 4 D-13 rejected
  in favor of in-place REQUIREMENTS.md expansion. Future milestone
  may introduce the convention if the planning tree grows to need it.
- **`SECURITY.md` repo-root file (SECv2-04)** — distinct from the
  `pip-audit` / `bandit` / SAST trio (`SECv2-01..03`). Mapped only to
  v2; future security-tooling milestone delivers it. Phase 5 D-13
  explicitly excludes from `SEC-01..03` scope.
- **Walkthrough verification of README install/run + CONTRIBUTING
  workflow** — Area 3 D-10 rejected (cli-smoke-test already covers
  install/run). Future milestone may want a manual walkthrough as
  part of release-cut polish.

### Reviewed Todos (not folded)

None — `gsd-sdk list-todos` not invoked (no project-todo system
configured for this milestone; TODOs surface organically through
ROADMAP/REQUIREMENTS).

</deferred>

---

*Phase: 05-deprecations-docs-security-stubs*
*Context gathered: 2026-05-07*
