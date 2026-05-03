# Phase 03: Internal Refactor & Coverage Hardening - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or
> execution agents. Decisions are captured in 03-CONTEXT.md — this log
> preserves the alternatives considered.

**Date:** 2026-05-03
**Phase:** 03-internal-refactor-coverage-hardening
**Areas discussed:** API contract scope, Type-hint modernization, pathlib migration, Coverage exclusion audit policy, Modern stdlib idioms, Dead code

---

## API contract scope

### Q1: Definition of public surface for diff-empty check

| Option | Description | Selected |
|--------|-------------|----------|
| Anything not _-prefixed | Public = every module-level name + class attribute/method NOT prefixed with `_` across cement/__init__.py, cement/core/*, cement/ext/*, cement/utils/*. Includes `Meta.<attr>` names, interface abstract methods, handler public methods. Excludes `_setup`, `_validate`, `_meta`. Strongest backward-compat guarantee. | ✓ |
| Including underscore-protected hooks | Above PLUS `_setup`/`_validate`/`_get_*`/`_parse_*`/`_make_*` patterns subclasses override. Strictest; refactor freedom shrinks; signal-handler refactor becomes out of scope. | |
| Module-level + class public methods only | Loosest scope — no `Meta.<attr>` lock. Risk: subclass-set attrs still work runtime but typecheckers/IDE on downstream apps may break. | |

**User's choice:** Anything not _-prefixed (Recommended)
**Notes:** Strongest backward-compat guarantee that doesn't paralyze the refactor. Subclass-hook renaming remains permissible if needed for clarity.

### Q2: Mechanical verification approach

| Option | Description | Selected |
|--------|-------------|----------|
| AST-walk script + commit | `scripts/audit_public_api.py` walks AST of every cement/ module, dumps non-underscore surface to sorted text file, diff against committed baseline. Reusable across phases; reviewer-readable. | ✓ |
| stub-based mypy check | `stubgen` baseline + diff. Heavier tooling; harder to read in PR review. | |
| Manual git-grep checklist | Hand-verify each public symbol survives. Cheapest but not reproducible. | |

**User's choice:** AST-walk script + commit (Recommended)

### Q3: Script location and lifecycle

| Option | Description | Selected |
|--------|-------------|----------|
| scripts/, retained | Drop in `scripts/`, commit alongside baseline. Future phases reuse. | |
| scripts/, retained + Makefile target | Above PLUS `make audit-public-api` target wired into local dev loops. | ✓ (with refinements) |
| .planning/phases/03-.../, throwaway | One-shot script inside phase dir; deleted after Phase 03. | |

**User's choice:** Option 2 with two refinements:
1. Script must be **dash-named** (`audit-public-api.py`), NOT snake_case
2. Script header must include commentary about its purpose
3. `make audit-public-api` is **independent** — NOT included in `make test` or any other make action

**Notes:** This is a strong signal about make-target hygiene — one-tool-one-job. Public-API audit is a deliberate dev-loop check, not a coverage/lint side effect.

### Q4: Baseline snapshot storage

| Option | Description | Selected |
|--------|-------------|----------|
| Phase artifact, sorted text | `.planning/phases/03-.../03-PUBLIC-API-BASELINE.txt`, captured FIRST commit (`docs(03): capture public API baseline`). Re-baseline only at intentional API change windows (3.2.0, 4.0). | ✓ |
| In-source snapshot | `cement/_public_api_baseline.txt` or `tests/data/`. Risk: leaks internal artifact into source tree. | |
| Git tag reference | Compute baseline from `main` HEAD pre-Phase-3. Flaky if Phase 4 (parallel) lands first. | |

**User's choice:** Phase artifact, sorted text (Recommended)

---

## Type-hint modernization scope

### Q1: ruff `UP` family enablement and migration scope

| Option | Description | Selected |
|--------|-------------|----------|
| Ruff UP family, all of cement/ + tests/ | Add `UP` to `extend-select` with AUDIT POINT comment. Auto-fix via `make comply-ruff-fix` handles UP006/UP007/UP045 mechanically. Lands as `fix(lint): resolve UPxxx ...` per Phase 1 D-04. | ✓ |
| Ruff UP family, cement/ only | Same config but tests/ excluded via `per-file-ignores`. Source-vs-tests inconsistency. | |
| Manual core-only sweep, no ruff UP | Hand-edit cement/core/*.py only. Drops the mechanization advantage; biggest inconsistency. | |

**User's choice:** Ruff UP family, all of cement/ (Recommended)
**Notes:** Phase 1 D-07 explicitly banned UP/SIM. Phase 03 lifts the UP ban; SIM stays out (per Phase 1 D-13 strict-minimum precedent).

### Q2: `from __future__ import annotations` cleanup

| Option | Description | Selected |
|--------|-------------|----------|
| Drop in same phase | Strip from all 28 files. Companion ruff `FA100`/`FA102` mechanizes detection. Removal lands AFTER UP006/UP007/UP045 so migration is single-step. | ✓ |
| Keep — forward-compat insurance | Leave in place. Cruft once 3.10+; modernization stays half-done. | |
| Drop in core/ only | Strip from cement/core/* (8 files) only. Inconsistent across the tree. | |

**User's choice:** Drop in same phase (Recommended)
**Notes:** Phase 1 D-14 explicitly deferred this work to Phase 03. fs.py:3-4 self-flagged comment ("remove after 3.9 is EOL?") closes here.

### Q3: `Any` reduction measurement and aggressiveness

| Option | Description | Selected |
|--------|-------------|----------|
| Capture baseline + opportunistic tightening | First commit captures `grep -E ': Any\|-> Any\|Any]' cement/core/ \| wc -l` baseline (~25). Hand-tighten where actual narrower type is known. Each surviving `Any` carries inline justification. Acceptance: post-count strictly lower than pre. | ✓ |
| Strict zero-Any in cement/core/ | Eliminate every `Any`. Risks public-API changes if interface signatures tighten. | |
| Tighten only Dict[str, Any] in core | Narrowest target. Function `**kw: Any` and locals stay. | |

**User's choice:** Capture baseline + opportunistic tightening (Recommended)

### Q4: Mypy strictness knob tightening

| Option | Description | Selected |
|--------|-------------|----------|
| Type hints only, knobs untouched | REFACTOR-02 = hint-level. Knobs (disallow_any_explicit, no_implicit_optional, warn_unused_ignores) stay as Phase 1 left them. Knob-tightening surfaces NEW errors and risks no-breakage rule. | ✓ |
| Tighten one knob: warn_unused_ignores | Same as above PLUS one bounded knob to surface orphan `# type: ignore`. | |
| Tighten multiple strictness knobs | Hardest mode; many new errors. Not recommended for no-breakage maintenance phase. | |

**User's choice:** Type hints only, knobs untouched (Recommended)

---

## pathlib migration depth

### Q1: Migration scope (which files)

| Option | Description | Selected |
|--------|-------------|----------|
| fs.py + cement/core/* | utils/fs.py + core/foundation.py + core/template.py (~25 sites) + core/config.py. cement/cli/, cement/ext/* stay on os.path. Mirrors Phase 1 D-10 cement/-only mypy scope precedent. | ✓ |
| fs.py + core/* + ext/* | Above PLUS ext_logging, ext_generate. Biggest blast; touches ext_smtp active-refactor territory. | |
| fs.py only | Strictest minimum. May fail ROADMAP success criterion #5 ("core internals" in scope). | |

**User's choice:** fs.py + cement/core/* (Recommended)

### Q2: Boundary-preservation rule

| Option | Description | Selected |
|--------|-------------|----------|
| Internal-only Path; boundary stays str | Locals are Path for clarity; every public return goes through `str(p)`. HOME_DIR stays str constant. Tmp.dir/Tmp.file stay str instance attrs. Zero-byte change to public type signatures. | ✓ |
| Path returns + str compat shims | Convert returns to Path. Downstream typecheckers will see new errors. Violates no-breakage rule. | |
| Add Path-returning siblings | Keep abspath() str-returning; add abspath_p() Path-returning. Adds public surface — violates D-04 diff-empty rule. | |

**User's choice:** Internal-only Path; boundary stays str (Recommended)

### Q3: Commit shape for migration

| Option | Description | Selected |
|--------|-------------|----------|
| Single atomic commit per file | Four commits: `refactor(utils.fs): ...`, `refactor(core.foundation): ...`, `refactor(core.template): ...`, `refactor(core.config): ...`. Bisect anchor per file. | ✓ |
| Commit per logical block | Split template.py into multiple commits per private helper. Tighter bisection but partial-migration in-flight is harder to reason about. | |
| Single commit for all four files | One sweeping commit. Hardest to review. Regression of D-04 atomic-per-concern. | |

**User's choice:** Single atomic commit per file (Recommended)

### Q4: Boundary callsite documentation

| Option | Description | Selected |
|--------|-------------|----------|
| Inline `# boundary: str` comment | Each remaining `os.path.*` callsite in scoped files gets `# boundary: keeps str signature` inline. Grep-able as `grep -n 'boundary:' cement/`. | ✓ |
| Phase artifact list | Maintain `03-OS-PATH-AUDIT.md` listing each callsite with rationale. Drifts from source. | |
| Comment only on the boundary returns | Comment only on `return str(p)` lines; don't comment surviving `os.path` sites. Lighter touch. | |

**User's choice:** Inline `# boundary: str` comment (Recommended)

---

## Coverage exclusion audit policy

### Q1: pragma:nocover audit policy

| Option | Description | Selected |
|--------|-------------|----------|
| Category labels everywhere | Every site gets a short inline category label. ~6-8 distinct categories cover all 123 sites. Mechanical, reviewer-friendly, grep-able. Lands as one or two atomic commits. | ✓ |
| Justify-or-close: also test the 'untestable' | Above PLUS write mock-based tests for High/Medium-priority untestable items in CONCERNS.md (signal hooks, ext_plugin imports, ext_daemon FD ops, ext_watchdog tuple, ext_generate template loading). May surface bugs; expands phase by several plans. | |
| Justify-or-close, signal hooks only | Category-label everything PLUS test signal hooks specifically. Bounded scope; addresses highest-priority gap. | |

**User's choice:** Category labels everywhere (Recommended)

### Q2: Vocabulary lock

| Option | Description | Selected |
|--------|-------------|----------|
| Lock vocabulary in CONTEXT | CONTEXT.md enumerates canonical category set: `abstract method`, `TYPE_CHECKING import`, `platform-specific`, `untestable: dynamic import`, `untestable: subprocess`, `untestable: signal handler`, `defensive: unreachable`, `version constant`. New categories require CONTEXT amendment. Grep-verified. | ✓ |
| Free-form per-site | Executor writes whatever justification fits each site. Less audit consistency. | |

**User's choice:** Lock vocabulary in CONTEXT (Recommended)

### Q3: Audit commit sequencing

| Option | Description | Selected |
|--------|-------------|----------|
| After refactor, single audit pass | Refactor commits land first (may add/remove pragma sites as side effect). Single `refactor(test): audit pragma:nocover sites` commit sweeps the final shape. Matches Phase 1 D-04 "fix the fallout last". | ✓ |
| Before refactor | Sweep all 123 sites first. Refactor churn requires second sweep anyway. | |
| Per-file alongside refactor | Each refactor commit fixes its file's pragma comments. Mixes two concerns in one commit — violates D-04 atomic-per-concern. | |

**User's choice:** After refactor, single audit pass (Recommended)

---

## Modern stdlib idioms (REFACTOR-04 closeout)

### Q1: Idiom modernization scope

| Option | Description | Selected |
|--------|-------------|----------|
| Ruff-driven only | Enable UP032 (printf → f-string) part of UP family. ~14 LOG.debug %-formatting sites. `cached_property`/`contextlib.suppress` opportunistic only. `.format()` template substitution in foundation.py:1359+ NOT touched. FIXME comments stay. | ✓ |
| Ruff UP032 + active cached_property/contextlib hunt | Plus scoped hunt for property recomputes and try-except → contextlib.suppress. Larger blast; risk of touching subclass surface. | |
| Strict minimum: just LOG.debug f-string conversion | Hand-convert ~14 sites only. No ruff UP032 globally. Smallest blast. | |

**User's choice:** Ruff-driven only (Recommended)
**Notes:** `.format(**template_dict)` calls in foundation.py and template.py are cement's own template substitution path, NOT log formatting. UP032 must NOT auto-rewrite these.

---

## Dead code (REFACTOR-01)

### Q1: Detection workflow

| Option | Description | Selected |
|--------|-------------|----------|
| vulture + hand-review | Add `vulture` to dev deps. Run at confidence 80-90%. Hand-review findings; whitelist file for false-positives. Vulture stays available post-Phase-03. | |
| Skip vulture; manual inspection | Hand-grep for private symbols. Misses cross-module dead code. | |
| Mark REFACTOR-01 satisfied at 100% coverage today | Argue 100% coverage implies zero unreachable code → REFACTOR-01 is no-op. Risk: covered-but-functionally-dead code and unused private helpers reachable via import remain undetected. | ✓ |

**User's choice:** Mark REFACTOR-01 satisfied at 100% coverage today
**Notes:** User chose with full awareness of the flagged risks. Acceptance via post-refactor `make test` passing at 100% coverage.

### Q2: Risk acknowledgement

| Option | Description | Selected |
|--------|-------------|----------|
| Lock as stated | REFACTOR-01 acceptance via `make test` 100% coverage. No vulture. Rationale in CONTEXT.md and 03-VERIFICATION.md. | |
| Lock + capture risk acknowledgement | Same as above PLUS one-line note in CONTEXT.md that this leaves "covered-but-functionally-dead code" and "unused private helpers reachable via import" undetected. Future milestones can re-open with vulture. | ✓ |

**User's choice:** Lock + capture risk acknowledgement
**Notes:** Captured in CONTEXT.md as D-21.

---

## Claude's Discretion

Listed in 03-CONTEXT.md "Claude's Discretion" subsection under
`<decisions>`. Summary:
- Specific commit-message body phrasing within the D-22 split
- Whether to use `make commit` vs `git commit` directly
- Order of UP-family fix commits (no semantic dependency)
- Whether to split D-22 step 8 (Any tightening) per file
- Whether to split D-22 step 13 (pragma audit) per file
- Whether `cached_property`/`contextlib.suppress` yields opportunistic
  commits beyond the UP032 sweep
- Exact wording of inline `# boundary: str` and `Any` justification
  comments

## Deferred Ideas

Listed in 03-CONTEXT.md `<deferred>` section. Summary:
- vulture-based dead-code audit (D-20/D-21 deferral)
- Closing High-priority untestable pragma:nocover blocks
- Signal-handler refactor (CONCERNS.md tech-debt #1)
- Logging handler cross-contamination (CONCERNS.md tech-debt #2)
- Mypy strictness knob tightening
- pathlib migration in cement/cli/, cement/ext/*
- FIXME-comment cleanup
- CONVENTIONS.md type-annotation refresh (recommended here, fallback
  to Phase 5 DOCS-04)
- `cached_property`/`contextlib.suppress` opportunistic adoption
