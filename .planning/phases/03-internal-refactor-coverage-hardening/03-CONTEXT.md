# Phase 03: Internal Refactor & Coverage Hardening - Context

**Gathered:** 2026-05-03
**Status:** Ready for planning

<domain>
## Phase Boundary

Run a cleanup-only internal refactor across the cement framework while
holding the absolute 100% coverage gate Phase 2 wired in. Specifically:
tighten type hints in `cement/core/`, modernize annotation syntax across
all of `cement/` + `tests/` (PEP 604 unions / PEP 585 builtin generics)
via ruff `UP` family, migrate `os.path` to `pathlib` internals in
`cement/utils/fs.py` + `cement/core/*` (boundary-preserving — public
funcs still return `str`), and audit every `# pragma: nocover` site so
the 100% gate is meaningful, not papered over. Capture a public-API
baseline up front and gate the phase on a diff-empty audit (no public
symbol added, removed, or signature-changed).

**In scope:**
- Capture `.planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt`
  (sorted text, one `module:ClassName.method` per line) BEFORE any
  refactor commit lands; commit as `docs(03): capture public API
  baseline` first.
- Add `scripts/audit-public-api.py` (dash-named) walking the AST of
  every module under `cement/` and emitting non-underscore public
  surface; script header documents purpose. Add `make audit-public-api`
  Makefile target — INDEPENDENT, NOT chained into `make test`,
  `make comply`, or any other make action.
- Re-enable ruff `UP` family in `[tool.ruff.lint] extend-select` (Phase
  1 D-08 hybrid pattern: explicit `extend-select` + AUDIT POINT comment
  naming the family list as the audit point on the next ruff bump).
  Apply across `cement/` + `tests/`. UP006/UP007/UP045 do the bulk
  mechanically via `make comply-ruff-fix`. Ruff `FA100`/`FA102` covers
  detection of `from __future__ import annotations` removability.
- Strip `from __future__ import annotations` from all 28 files where
  it currently appears (Phase 1 D-14 explicitly deferred this to Phase
  03). Removal MUST come AFTER UP006/UP007/UP045 land so the migration
  is single-step coherent.
- Capture baseline `Any`-in-`cement/core/` count
  (`grep -E ': Any\b|-> Any\b|Any\]' cement/core/*.py | wc -l`,
  ~25 today) in `03-VERIFICATION.md` first commit. Opportunistically
  hand-tighten where actual narrower type is known. `**kw: Any` and
  argparse `_parsed_args: Any` may stay (handler contract / argparse
  opacity). Acceptance: post-count STRICTLY LOWER than pre-count, AND
  every surviving `Any` carries an inline comment justifying it.
- Migrate `os.path` → `pathlib.Path` *internals* in:
  - `cement/utils/fs.py`
  - `cement/core/foundation.py`
  - `cement/core/template.py` (~25 sites — biggest single-file blast)
  - `cement/core/config.py`
  Public funcs in fs.py still return `str` via `str(p)` at the
  boundary. `HOME_DIR` stays a `str` constant. `Tmp.dir`/`Tmp.file`
  stay `str` instance attributes. Public type signatures: ZERO bytes
  changed.
- Modern stdlib idioms via ruff `UP032` (printf-style → f-string).
  Handles the ~14 `LOG.debug('%s' % ...)` sites and other %-formatting
  mechanically. `cached_property` and `contextlib.suppress` adoption
  is opportunistic only — no requirement.
- Audit all 123 `# pragma: nocover` sites with category labels from a
  fixed vocabulary (see D-13 below). Lands as a single
  `refactor(test): audit pragma:nocover sites with category labels`
  pass AFTER refactor commits (or one commit per file if blast
  radius is large).
- Phase verification artifact (`03-VERIFICATION.md`) captures: pre/post
  `Any` count + delta, baseline-vs-post audit-public-api diff (must be
  empty), `make audit-public-api` exit-status, REFACTOR-01
  acceptance-via-coverage rationale.

**Out of scope:**
- Public API changes (signatures, names, exports) — the no-breakage
  rule on the 3.0.x track is absolute (PROJECT.md Constraints). The
  AST-walk audit gate enforces this.
- Subclass-extension hooks (`_setup`, `_validate`, `_get_*`,
  `_parse_*`, `_make_*`) — Phase 03 may rename/touch these per Area 1
  decision (anything not `_`-prefixed is the public surface), but the
  signal-handler refactor flagged in CONCERNS.md tech-debt (#1) is
  explicitly NOT this phase's work — it's a behavior change, not a
  cleanup.
- Mypy strictness knob tightening (`disallow_any_explicit`,
  `no_implicit_optional`, `warn_unused_ignores`, etc.) — defer to a
  future milestone (3.2.0 / dedicated type-coverage). REFACTOR-02 is
  hint-level only.
- Dead-code hunting via `vulture` or similar — REFACTOR-01 is
  satisfied via the existing 100% coverage gate (D-19 below). No new
  dev-dep added; no whitelist file.
- pathlib migration in `cement/cli/`, `cement/ext/*` — those are
  extension/CLI internals, less core, not named in REFACTOR-03's
  literal scope. Mirrors Phase 1 D-10 (mypy scope held at
  `cement/`-only by skipping `tests/`).
- Closing the High-priority "untestable" `pragma: nocover` blocks
  flagged in CONCERNS.md (signal hooks, ext_plugin dynamic imports,
  ext_daemon FD ops, ext_watchdog single-tuple, ext_generate template
  loading) — the audit policy here is comment-justify-only; covering
  those is engineering work for a future milestone (or could be
  promoted to a Phase 03 sub-plan if executor encounters cheap wins).
- Touching the `.format()` calls in foundation.py:1359+ (template
  substitution, NOT log formatting). UP032 must NOT auto-rewrite
  these; verify per-file.
- FIXME-comment cleanup (foundation.py:150, ext_daemon.py:163/169/175,
  ext_plugin.py:152, ext_watchdog.py:169, ext_generate.py:161,
  ext_logging.py:223/264) — those are tech debt, not idiom
  modernization.
- DEPREC-01..03 (Phase 5), DOCS-01..04 (Phase 5), TRIAGE-01..04
  (Phase 4) — explicitly mapped to other phases per ROADMAP.

</domain>

<decisions>
## Implementation Decisions

### Public API contract (Area 1)

- **D-01:** **Public surface = anything not `_`-prefixed.** Every
  module-level name AND every class attribute/method NOT prefixed with
  `_` across `cement/__init__.py`, `cement/core/*`, `cement/ext/*`,
  `cement/utils/*`, `cement/cli/*`. Includes `App.Meta.<attr>` names
  that subclasses set (`config_defaults`, `extensions`, `handlers`,
  `meta_override`, `core_interfaces`, etc.), interface abstract
  methods, handler public methods, exception classes. Excludes
  `_setup`, `_validate`, `_meta`, `_get_*`, `_parse_*`, `_make_*`.
  This is the strongest backward-compat guarantee that doesn't
  paralyze the refactor (subclass-hook renaming remains permissible
  if needed for clarity, though no current decision requires it).
- **D-02:** **AST-walk audit script** — `scripts/audit-public-api.py`
  (dash-named per user direction). Walks the AST of every `.py`
  module under `cement/`, dumps non-underscore module-level names,
  class names, class public attributes, and class public method
  names to stdout (sorted). Script header MUST include commentary
  about its purpose. Uses stdlib `ast` only — no new dev-dep.
- **D-03:** **`make audit-public-api` Makefile target** — INDEPENDENT.
  NOT chained into `make test`, `make comply`, or any other make
  action. User can run on demand to verify. Exit non-zero on diff
  vs the committed baseline.
- **D-04:** **Baseline snapshot** — sorted text file
  `.planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt`,
  one `module:ClassName.method` (or `module:NAME` for module-level)
  per line. Captured BEFORE any refactor commit lands as the FIRST
  phase commit `docs(03): capture public API baseline`. Acceptance:
  `make audit-public-api` exits 0 (post-refactor surface matches
  committed baseline byte-for-byte after sort). Re-baseline only
  happens at intentional API change windows (Cement 3.2.0, Cement
  4.0).
- **D-05:** **Audit script + Makefile target are retained as
  permanent dev affordances** post-Phase-03. Future phases (Phase 5
  deprecations, Phase 6 release cut, all 3.0.x patch work) reuse
  them as a regression check. Pattern: same shape as
  `scripts/cli-smoke-test.sh` from quick task `260430-i7q` —
  permanent affordance, not phase-throwaway.

### Type-hint modernization (Area 2)

- **D-06:** **Re-enable ruff `UP` family** in
  `[tool.ruff.lint] extend-select` per Phase 1 D-08 hybrid pattern.
  Add a sibling AUDIT POINT comment naming the `UP` family addition
  as the audit point on the NEXT ruff bump (so a future UP rule
  graduating from preview lands as a deliberate config decision,
  not silent CI red). Phase 1 D-07 explicitly banned `UP`/`SIM` —
  Phase 03 lifts the `UP` ban; `SIM` stays out.
- **D-07:** **UP migration scope = all of `cement/` + `tests/`.**
  Auto-fix via `make comply-ruff-fix` covers UP006 (List → list),
  UP007 (Union → |), UP045 (Optional → X | None), UP032 (printf
  → f-string), and the rest of the `UP` rule set. Lands as
  `fix(lint): resolve UPxxx <name>` commits per Phase 1 D-04
  family-split discipline (one commit per `UP` rule code).
- **D-08:** **Drop `from __future__ import annotations`** from all
  28 files in this phase. Removal MUST land AFTER UP006/UP007/UP045
  land (so the modernization is a single coherent migration). Ruff
  `FA100`/`FA102` family in `extend-select` mechanizes detection.
  Lands as `fix(lint): resolve FA100 future-annotations imports`
  (or similar) atomic commit. Risk acknowledgement: native
  evaluation may surface forward-ref bugs that string-deferred
  annotations papered over — TYPE_CHECKING blocks already handle
  the known circular-import edges (verified by Phase 1 D-13's
  preserve pass).
- **D-09:** **`Any` reduction in `cement/core/`** —
  baseline-and-tighten approach. First commit captures the count
  via `grep -E ': Any\b|-> Any\b|Any\]' cement/core/*.py | wc -l`
  (~25 today); record it in `03-VERIFICATION.md`. Hand-tighten per
  file where actual narrower type is known: `Dict[str, Any]` →
  `Dict[str, str]` if strictly true; `**kw: Any` and argparse
  `_parsed_args: Any` may stay (handler contract / argparse
  opacity). Each surviving `Any` carries an inline comment
  justifying it (mirrors COV-03 pragma policy). Acceptance:
  post-count STRICTLY LOWER than pre-count; phase summary names
  the delta (e.g., "25 → 14").
- **D-10:** **Mypy strictness knobs untouched.** REFACTOR-02 is
  hint-level only. `disallow_any_explicit`, `no_implicit_optional`,
  `warn_unused_ignores`, etc. all stay exactly as Phase 1 left
  them. Knob-tightening surfaces NEW errors and risks the
  no-breakage rule; out of scope here.

### pathlib migration (Area 3)

- **D-11:** **Migration scope = `cement/utils/fs.py` +
  `cement/core/*`.** Specifically: `cement/utils/fs.py`,
  `cement/core/foundation.py`, `cement/core/template.py` (~25
  sites — biggest single-file blast), `cement/core/config.py`.
  `cement/cli/`, `cement/ext/*` (ext_logging, ext_generate,
  ext_smtp, etc.) stay on `os.path`. Mirrors Phase 1 D-10
  precedent (`cement/`-only mypy scope by skipping `tests/`).
- **D-12:** **Boundary-preservation rule = internal-only Path; str
  at the boundary.** Inside fs.py, locals are `Path` for clarity
  (`p = Path(path).expanduser().resolve()`) but every public return
  goes back through `str(p)`. `HOME_DIR` stays a `str` constant.
  `Tmp.dir`/`Tmp.file` stay `str` instance attributes. **ZERO**
  bytes change to public type signatures (D-01 contract). The
  audit-public-api gate (D-04) verifies this.
- **D-13:** **Atomic commit per migrated file.** Four commits:
  - `refactor(utils.fs): migrate os.path to pathlib internals`
  - `refactor(core.foundation): migrate os.path to pathlib internals`
  - `refactor(core.template): migrate os.path to pathlib internals`
  - `refactor(core.config): migrate os.path to pathlib internals`
  Matches Phase 1 D-04 atomic-per-concern shape. Bisect anchor per
  file. Order: utils.fs FIRST (smallest, foundational), then core
  files in any order (they don't depend on each other for path
  semantics).
- **D-14:** **Inline `# boundary: str` comment** on any remaining
  `os.path.*` callsite in scoped files (none expected
  post-migration; if any survive, e.g., a `__fspath__`-equivalent
  edge, they get this marker). Out-of-scope files
  (`cement/cli/`, `cement/ext/*`) have no comment requirement —
  they're untouched. Grep verification: any `os.path` call in
  scoped files that is NOT followed by `# boundary:` on the same
  or adjacent line is a finding. ROADMAP success criterion #5
  is satisfied by this convention.

### pragma: nocover audit (Area 4 — COV-03)

- **D-15:** **Category labels from a locked vocabulary** on every
  one of the 123 sites. Canonical category set:
  - `# abstract method` — interface `pass` lines (e.g.,
    `cement/core/cache.py:49`, `cement/core/arg.py:62`, etc.)
  - `# TYPE_CHECKING import` — deferred-import lines under
    `if TYPE_CHECKING:` (e.g., `cement/core/foundation.py:48`,
    every ext_*.py importing App for type hints only)
  - `# platform-specific` — env/platform fallbacks (e.g.,
    `cement/utils/fs.py:245` HOME-fallback)
  - `# untestable: dynamic import` — runtime
    `__import__()`/`importlib.import_module()` paths (e.g.,
    `cement/ext/ext_plugin.py:150-153`)
  - `# untestable: subprocess` — shell/git subprocess calls
    (e.g., `cement/utils/version.py:97`)
  - `# untestable: signal handler` — signal-handler internals
    (e.g., `cement/core/foundation.py:123-125`)
  - `# defensive: unreachable` — fallback else branches that
    `coverage.py` cannot prove unreachable (e.g.,
    `cement/utils/fs.py:237` backup() else branch)
  - `# version constant` — module-level version tuples
    (e.g., `cement/core/backend.py:3`)
- **D-16:** **Vocabulary expansion requires CONTEXT amendment.** If
  the executor encounters a site that doesn't fit any category, the
  fix is to add a category to D-15 in this CONTEXT.md (atomic
  `docs(03): expand pragma vocabulary` commit), NOT to invent a
  free-form label. Maintains audit consistency.
- **D-17:** **Grep verification** —
  ```bash
  grep -nE 'pragma:\s*no\s*cover' cement/ \
    | grep -vE '# (abstract method|TYPE_CHECKING import|platform-specific|untestable: dynamic import|untestable: subprocess|untestable: signal handler|defensive: unreachable|version constant)'
  ```
  must return empty. Captured in `03-VERIFICATION.md`.
- **D-18:** **Audit lands AFTER refactor commits in a single sweep.**
  Refactor commits (dead code, type hints, pathlib, idioms) may add
  or remove pragma sites as a side effect — sweeping after means
  the audit runs against the final shape. Lands as
  `refactor(test): audit pragma:nocover sites with category labels`
  (or one commit per file if blast radius warrants splitting).
  Mirrors Phase 1 D-04 "fix the fallout last" shape.

### Modern stdlib idioms (REFACTOR-04 closeout)

- **D-19:** **Ruff-driven only.** UP032 (printf → f-string) handles
  the ~14 `LOG.debug('%s' % ...)` sites mechanically. `cached_property`
  and `contextlib.suppress` adoption is opportunistic only — if a
  helper appears that obviously fits, executor adds it; otherwise no
  requirement. **The `.format()` calls in `cement/core/foundation.py`
  lines 1359, 1364, 1372, 1377, 1385, 1390, 1478, 1483, 1488, 1492,
  1553, 1558, 1563, 1567 MUST NOT be touched** — they're cement's
  own template substitution path (`**template_dict`), not log
  formatting. Verify per file before committing the UP032 sweep.
  FIXME comments throughout the codebase are tech debt, NOT idiom
  modernization, and stay untouched.

### Dead code (REFACTOR-01)

- **D-20:** **Acceptance via existing 100% coverage gate.**
  REFACTOR-01 is satisfied because the post-refactor `make test`
  passes at 100% coverage with `fail_under = 100`, which implies
  zero unreachable code. No `vulture`, no dead-code hunting commits,
  no whitelist file. Rationale recorded in `03-VERIFICATION.md`.
- **D-21:** **Risk acknowledgement** (per user direction): D-20
  leaves two classes of "dead-but-covered" code undetected:
  (a) covered-but-functionally-dead code (executes in tests
  without meaningful asserts), and (b) unused private helpers
  reachable via import but not called by any production
  caller. Future milestones (3.2.0 cleanup, dedicated audit
  milestone) may re-open with `vulture` if these gaps prove to
  bite. Recorded here so the deferral is intentional, not
  oversight.

### Commit shape (carries Phase 1/2 conventions)

- **D-22:** **Atomic per-concern, Conventional Commits, 78-char
  wrap** (CLAUDE.md + Phase 1 D-02/D-04 + Phase 2 D-17). Suggested
  commit sequence (planner refines):
  1. `docs(03): capture public API baseline` (artifact +
     `audit-public-api.py` script + Makefile target)
  2. `chore(ruff): re-enable UP family with AUDIT POINT comment`
  3. `fix(lint): resolve UP006 List → list`
  4. `fix(lint): resolve UP007 Union → |`
  5. `fix(lint): resolve UP045 Optional → X | None`
  6. `fix(lint): resolve UP032 printf → f-string`
  7. `fix(lint): resolve FA100 future-annotations imports`
     (drops `from __future__ import annotations` from 28 files;
     LANDS AFTER UP006/UP007/UP045 per D-08)
  8. `refactor(core): tighten Any types in cement/core/` (or split
     per file if too large; surviving `Any` carries inline
     justification per D-09)
  9. `refactor(utils.fs): migrate os.path to pathlib internals`
  10. `refactor(core.foundation): migrate os.path to pathlib
      internals`
  11. `refactor(core.template): migrate os.path to pathlib
      internals`
  12. `refactor(core.config): migrate os.path to pathlib
      internals`
  13. `refactor(test): audit pragma:nocover sites with category
      labels` (single sweep per D-18, or split per file)
  14. `docs(03): record Any-baseline + REFACTOR-01 verification`
      (`03-VERIFICATION.md`)
- **D-23:** **GSD artifact commits** follow `docs(03): ...` shape
  (mirrors Phase 1 / 01.1 / Phase 2 patterns).

### Acceptance

- **D-24:** Phase 03 acceptance is the conjunction of:
  1. `make test` passes at 100% coverage (REFACTOR-01 acceptance
     via D-20; COV-01).
  2. `make comply-ruff` passes with `UP` family enabled
     (TOOL-04 stays satisfied; ruff config still
     no-implicit-drift).
  3. `make comply-mypy` passes (REFACTOR-02 hint changes type-check
     clean).
  4. `make audit-public-api` exits 0 (D-04 baseline matches
     post-refactor surface; ROADMAP success criterion #3
     satisfied).
  5. `coverage-report/` HTML generates without warnings (COV-02).
  6. Pre/post `Any`-in-`cement/core/` count delta is strictly
     positive in the reduction direction; recorded in
     `03-VERIFICATION.md` (REFACTOR-02 acceptance; ROADMAP success
     criterion #4).
  7. `grep -nE 'pragma:\s*no\s*cover' cement/ | grep -vE '# (abstract method|TYPE_CHECKING import|platform-specific|untestable: dynamic import|untestable: subprocess|untestable: signal handler|defensive: unreachable|version constant)'`
     returns empty (COV-03 acceptance; ROADMAP success criterion
     #2 — strict locked-vocabulary form).
  8. `grep -rn 'os\.path' cement/utils/fs.py cement/core/` returns
     only callsites tagged with `# boundary: str` on the same or
     adjacent line, OR returns empty (REFACTOR-03 acceptance;
     ROADMAP success criterion #5).
  9. `from __future__ import annotations` returns no matches across
     `cement/` (D-08 / FA100 acceptance).

### Claude's Discretion

- Specific message-body phrasing within the D-22 commit split (the
  planner picks).
- Whether to author commits via `make commit` or `git commit`
  directly (either satisfies CLAUDE.md as long as the result
  matches Conventional Commits + 78-char wrap).
- Order of UP-family fix commits (UP006 vs UP007 vs UP045 — they're
  family siblings, no semantic dependency between them).
- Whether to split D-22 step 8 (`refactor(core): tighten Any
  types`) per file or land it as a single commit — depends on the
  realized blast radius.
- Whether to split D-22 step 13 (pragma audit) per file — same
  judgment call.
- Whether `cached_property` or `contextlib.suppress` adoption
  yields any opportunistic commits beyond the UP032 sweep —
  executor decides per encountered helper.
- Exact wording of inline `# boundary: str` comments where they
  appear (just must be grep-able as `boundary:`).
- Exact wording of inline `Any` justification comments per D-09.

### Folded Todos

None — `gsd-sdk list-todos` returned `count: 0` at discussion time.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project intent and constraints

- `.planning/PROJECT.md` — Core Value, no-breakage rule on 3.0.x
  including subclass-exposed internals, Constraints block (zero new
  runtime deps for core, 100% coverage absolute), Key Decisions
  table. **Out of Scope** specifically defers Cement 4 architectural
  seams (D-01 contract preserves this discipline).
- `.planning/REQUIREMENTS.md` §"Internal Refactor" (REFACTOR-01..04),
  §"Test Coverage" (COV-01..03). DEPREC-01..03 (Phase 5),
  DOCS-01..04 (Phase 5), TRIAGE-01..04 (Phase 4) are explicitly
  OTHER phases.
- `.planning/ROADMAP.md` §"Phase 3: Internal Refactor & Coverage
  Hardening" — goal, dependencies (Phase 2), 5 success criteria,
  requirement mapping. D-24 acceptance criteria above map 1:1
  against ROADMAP success criteria.

### Precedent — same project, same scope discipline

- `.planning/phases/01-tooling-baseline-python-matrix/01-CONTEXT.md`
  — D-02 atomic-commit shape, D-04 one-commit-per-rule-family
  pattern, D-07 UP/SIM ban (Phase 03 lifts the UP ban; SIM stays
  out), D-08 hybrid AUDIT POINT pattern (D-06 reuses), D-13
  strict-minimum boundary, D-14 explicit deferral of
  `from __future__ import annotations` cleanup to Phase 03 (this
  phase honors it via D-08).
- `.planning/phases/01-tooling-baseline-python-matrix/01-RESEARCH.md`
  — Phase 1 lint research and rule-family decisions; Phase 03
  inherits the rule-family list and adds `UP` (and `FA`) to
  extend-select.
- `.planning/phases/02-dependencies-ci-pipeline/02-CONTEXT.md` —
  D-10/D-11/D-12 coverage gate wiring; Phase 03's COV-01/02 ride
  on this baseline. D-17 commit-shape continuity.
- `.planning/phases/01.1-generated-project-template-build-modernization/01.1-CONTEXT.md`
  — D-15 multiple-atomic-commits-per-branch shape (matches D-22
  here).

### Existing codebase intel

- `.planning/codebase/CONVENTIONS.md` — current type-annotation
  full-form convention (Optional/Union/List/Tuple/Dict). Phase 03
  REPLACES this convention with PEP 604 + PEP 585 modern syntax
  via UP006/UP007/UP045. CONVENTIONS.md SHOULD be updated as
  part of Phase 5 docs work (DOCS-04) or via a small `docs:` commit
  here if convenient.
- `.planning/codebase/STRUCTURE.md` — directory layout; pathlib
  scope (D-11) maps to `cement/utils/fs.py` + `cement/core/*` per
  this map.
- `.planning/codebase/TESTING.md` — pytest invocation surface,
  100% coverage gate (already wired by Phase 2). Phase 03 does
  NOT change test-runner config; just the coverage exclusion
  comments.
- `.planning/codebase/CONCERNS.md` — known tech debt and
  pragma:nocover gaps. D-15 vocabulary maps onto
  CONCERNS.md "Test Coverage Gaps" categories. Phase 03 does
  NOT close the High-priority untestable items (signal hooks,
  ext_plugin dynamic imports, etc.) — those defer to a future
  milestone (acknowledged in D-21).

### Files this phase will touch

- **New:** `scripts/audit-public-api.py` (dash-named per user
  direction; stdlib `ast` only)
- **New:** `.planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt`
- **New:** `.planning/phases/03-internal-refactor-coverage-hardening/03-VERIFICATION.md`
- **Modified:** `Makefile` — add `audit-public-api` target;
  STANDALONE, not chained.
- **Modified:** `pyproject.toml` — `[tool.ruff.lint] extend-select`
  gains `UP` and `FA` family codes with sibling AUDIT POINT
  comment.
- **Modified:** annotation modernization across `cement/` +
  `tests/` (28 files lose `from __future__ import annotations`;
  most files lose Optional/Union/List/Dict/Tuple typing imports).
- **Modified:** `cement/utils/fs.py`, `cement/core/foundation.py`,
  `cement/core/template.py`, `cement/core/config.py` — pathlib
  internal migration (D-11..D-14).
- **Modified:** every file with a `# pragma: nocover` site —
  category-label sweep (D-15..D-18).
- **NOT modified:** `cement/core/foundation.py` lines 1359, 1364,
  1372, 1377, 1385, 1390, 1478, 1483, 1488, 1492, 1553, 1558,
  1563, 1567 (`.format()` template substitution — D-19).
- **NOT modified:** any `_setup`, `_validate`, `_get_*`, `_parse_*`,
  `_make_*` semantics (signal-handler refactor and similar are
  out of scope per D-01 boundary clarification).

### External docs

- ruff `UP` rule family: https://docs.astral.sh/ruff/rules/#pyupgrade-up
- ruff `FA` rule family: https://docs.astral.sh/ruff/rules/#flake8-future-annotations-fa
- PEP 604 (X | Y union syntax): https://peps.python.org/pep-0604/
- PEP 585 (builtin generic types): https://peps.python.org/pep-0585/
- pathlib stdlib docs: https://docs.python.org/3/library/pathlib.html
- coverage.py exclusion config: https://coverage.readthedocs.io/en/latest/excluding.html
- Python `ast` module: https://docs.python.org/3/library/ast.html

### Conventions

- `CLAUDE.md` §"Commit Conventions" — Conventional Commits, 78-char
  subject + body wrap, `make commit` (`pdm run cz commit`) for
  interactive authoring.
- `CLAUDE.md` §"Changelog Maintenance" — append entries to active
  `## 3.0.16 - DEVELOPMENT` section. Phase 03 produces:
  - `[dev]` ruff UP family adoption (Misc)
  - `[core]` `os.path` → pathlib internal migration (Refactoring)
  - `[core]` Modern type-hint syntax (PEP 604/585) adoption
    (Refactoring)
  - `[dev]` `make audit-public-api` target + baseline (Misc)
  - `[dev]` pragma:nocover audit with category vocabulary
    (Refactoring)
  Phase 03 lands these phase-by-phase, not at release-cut time.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `make comply`, `make comply-ruff`, `make comply-ruff-fix`,
  `make comply-mypy`, `make test` — existing entry points; no new
  make targets required this phase EXCEPT the standalone
  `make audit-public-api` (D-03).
- `[tool.ruff.lint] extend-select` already follows Phase 1 D-08
  hybrid pattern with AUDIT POINT comment — Phase 03 adds `UP` and
  `FA` family codes alongside the existing entries with their own
  AUDIT POINT sibling comment.
- `make comply-ruff-fix` already drives `ruff check --fix`; the UP
  auto-fix sweep (D-07) lands via this single command followed by
  reviewing-and-committing the per-rule diff.
- `[tool.coverage.report] fail_under = 100` (Phase 2 D-10) keeps
  the coverage gate fail-fast against any drift introduced by the
  refactor — REFACTOR-01 D-20 acceptance rides directly on this.
- `[tool.coverage.run] omit` (Phase 2 D-12) excludes
  `cement/cli/templates/*` and `cement/cli/contrib/*` — Phase 03
  pathlib scope (D-11) excludes `cement/cli/` consistent with this.

### Established Patterns

- **Hybrid AUDIT POINT pattern** (Phase 1 D-08) — every ruff /
  mypy / coverage config addition gets a sibling comment naming
  itself as the audit point on the next tool bump. Phase 03 D-06
  reuses for `UP`+`FA` family additions.
- **Atomic-per-concern commits** (Phase 1 D-02/D-04, 01.1 D-15,
  Phase 2 D-17) — D-22 carries forward.
- **D-15 coupling** (Phase 1) — pin and bump are inseparable for
  drift detection. Phase 03 has no version pins to bump (Phase 1
  set them; Phase 2 didn't move ruff/mypy versions). The
  config-knob equivalent is D-06 — the `extend-select` change
  lands in the same commit as the AUDIT POINT comment.
- **"Strict-minimum" deferrals** (Phase 1 D-13/D-14) — Phase 03
  is where those deferrals come due (annotation modernization,
  `from __future__` cleanup, type-hint tightening).
- **Coverage hold-the-line** (Phase 2 D-10/D-11) — every commit in
  Phase 03 must land with `make test` green at 100% coverage.
  Sampling per task; full `make test` per logical wave.

### Integration Points

- **CI gate**: `.github/workflows/build_and_test.yml` runs
  `make comply` (ruff + mypy + 100% coverage gate) on every PR.
  Phase 03's PR must turn this gate green end-to-end across the
  7-lane matrix (Python 3.10/3.11/3.12/3.13/3.14, pypy-3.10,
  pypy-3.11). The audit-public-api target is NOT wired into CI
  per D-03 (standalone only).
- **Public API audit**: D-04 baseline travels with the planning
  artifacts, NOT the source tree (per Area 1 final question).
  Future phases reference it by relative path. The script lives
  in `scripts/` so it can run standalone without pulling planning
  artifacts.
- **Coverage gate vs pragma audit**: D-15..D-18 changes don't
  alter coverage measurements (pragma comments are a coverage.py
  exclusion mechanism, not test logic). Coverage stays at 100%
  by construction.

### Known refactor risk surfaces

- **`cement/core/foundation.py` `.format()` template substitution**
  (lines 1359..1567) — UP032 must NOT touch these. Verify
  per-file diff before committing the UP032 sweep. Add a `# noqa:
  UP032` if ruff misclassifies (unlikely — these use `**dict` not
  `%`).
- **`cement/utils/fs.py:3-4` self-flagged `from __future__ import
  annotations`** with comment `# derks@2024-06-22: remove after
  3.9 is EOL?` — D-08 closes this loop.
- **`Tmp.__exit__` signature** (`cement/utils/fs.py:75-79`) uses
  `type[BaseException] | None` — already PEP 604. Phase 03 just
  needs to ensure this style is consistent post-UP migration.
- **`cement/core/template.py` `.format(**template_dict)` calls**
  (lines 359..) — same template substitution pattern as
  foundation.py. UP032 must NOT touch these.
- **CONVENTIONS.md drift** — the document still says
  "Type annotations use full form: `Dict[str, Any]`,
  `Optional[str]`, `List[str]`, `Tuple[int, str]`". After this
  phase that's wrong. Either update the doc here or in Phase 5
  DOCS-04. Recommend updating here in a small `docs(codebase):
  refresh CONVENTIONS to PEP 604/585 syntax` commit alongside
  D-22 step 5 (UP045) so the source-of-truth doc never lies.

</code_context>

<specifics>
## Specific Ideas

- The user-articulated direction on D-03 was sharp:
  `make audit-public-api` is **independent**, NOT chained into
  `make test` or any other make action. Reflects the user's
  preference (visible in Phase 1/2 commit shapes) for one-tool-one-
  job — coverage gates run in `make test`, lint runs in
  `make comply`, public-API audit runs in `make audit-public-api`.
  Mixing concerns into a single target obscures which gate failed.
- Script naming: `audit-public-api.py` (dash-named) per user
  direction, NOT `audit_public_api.py` (snake_case). Note: this
  diverges from CONVENTIONS.md "Module files: lowercase with
  underscores" — but this is a `scripts/` utility, not a Python
  module imported by cement. The dash matches the Makefile target
  name (`make audit-public-api`) for symmetry. Script header MUST
  document purpose (downstream operators land on this file via
  `make audit-public-api` and need to understand its job
  immediately).
- The user's REFACTOR-01 call (D-20) "100% coverage implies zero
  unreachable code" is a deliberate trade. They acknowledged the
  risks (D-21) and chose to defer rather than add `vulture`.
  Future-self note: if a downstream user reports a "function
  exists but does nothing" bug in a 3.0.x patch cycle, that's
  the signal to revisit D-20.
- The pragma vocabulary lock (D-15..D-17) — user chose
  `Lock vocabulary in CONTEXT (Recommended)` over free-form. This
  matches their established preference for grep-able audit
  surfaces (Phase 1 D-08 AUDIT POINT, Phase 2 D-12 omit-list).
  Future audit phases get a clean `grep` invocation as the gate.

</specifics>

<deferred>
## Deferred Ideas

- **vulture-based dead-code audit** — D-20/D-21 explicitly defer.
  Re-open if covered-but-functionally-dead or unused-private-helper
  bugs surface in 3.0.x patches. Future milestone (3.2.0 cleanup
  or dedicated audit milestone) is the natural home.
- **Closing High-priority untestable `pragma: nocover` blocks** —
  signal hooks (`tests/core/test_hook.py:112` TODO), ext_plugin
  dynamic imports (lines 150-153), ext_daemon FD ops (lines
  156-170), ext_watchdog single-tuple path (line 166),
  ext_generate template loading errors (lines 158-162). Phase 03
  D-15 only category-labels these. Future milestone may attempt
  mock-based coverage; not in scope now.
- **Signal-handler refactor** (CONCERNS.md tech-debt #1) —
  `cement/core/foundation.py:125-127` frame-globals search is
  brittle but works. Refactoring to a decorator pattern is a
  behavior change, not a cleanup, and is out of scope for the
  no-breakage 3.0.x track. Cement 4 territory.
- **Logging handler cross-contamination** (CONCERNS.md tech-debt
  #2) — `ext_logging.py` `_clear_loggers()` FIXME (lines 221, 262).
  Behavior bug, not a cleanup. Defer.
- **Mypy strictness knob tightening** —
  `disallow_any_explicit`, `no_implicit_optional`,
  `warn_unused_ignores`, etc. Out of scope per D-10. Future
  milestone (3.2.0 / dedicated type-coverage).
- **pathlib migration in `cement/cli/`, `cement/ext/*`** — out of
  scope per D-11. Future milestone if a downstream contributor
  picks it up; not blocking on Clean & Green.
- **FIXME-comment cleanup** — 9 outstanding `# FIXME` comments in
  core+ext. Tech debt, not idiom modernization. Defer to a
  dedicated tech-debt phase or address via Phase 4 backlog
  triage if the user closes the underlying issue.
- **CONVENTIONS.md type-annotation refresh** (full form →
  PEP 604/585) — recommended landing here per D-23 / commit
  step 5 (UP045 sibling), but if it crosses into Phase 5 DOCS-04
  scope the planner can punt. Tracked as deferred-but-cheap.
- **`cached_property` / `contextlib.suppress` opportunistic
  adoption** — D-19 keeps these opportunistic only (executor's
  call). Not a phase requirement.

</deferred>

---

*Phase: 03-internal-refactor-coverage-hardening*
*Context gathered: 2026-05-03*
