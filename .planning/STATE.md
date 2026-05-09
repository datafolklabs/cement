---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: executing
stopped_at: Phase 5 context gathered
last_updated: "2026-05-08T00:20:22.717Z"
last_activity: 2026-05-08
progress:
  total_phases: 7
  completed_phases: 5
  total_plans: 28
  completed_plans: 28
  percent: 100
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-04-24)

**Core value:** Cement 3 stays solid, secure, performant, and bug-free under strict backward compatibility — while being continuously maintained against a modern Python and tooling ecosystem.
**Current focus:** Phase 05 — deprecations-docs-security-stubs

## Current Position

Phase: 6
Plan: Not started
Status: Executing Phase 05
Last activity: 2026-05-08 - Completed quick task 260507-to4: rewrite PR #760 (template_dirs config override)

Progress: [██████████] 100% (21/21 plans completed across Phases 1, 01.1, 2, 3 — Phases 4-6 plan counts TBD)

## Performance Metrics

**Velocity:**

- Total plans completed: 12
- Average duration: —
- Total execution time: 0 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01 | 4 | - | - |
| 01.1 | 1 | - | - |
| 05 | 6 | - | - |

**Recent Trend:**

- Last 5 plans: —
- Trend: —

*Updated after each plan completion*
| Phase 01-tooling-baseline-python-matrix P01 | 2 min | 1 tasks | 9 files |
| Phase 01-tooling-baseline-python-matrix P02 | 20 min | 9 tasks | 91 files |
| Phase 01-tooling-baseline-python-matrix P03 | 3 min | 2 tasks tasks | 2 files files |
| Phase 01-tooling-baseline-python-matrix P04 | 11 | 1 tasks | 1 files |
| Phase 01.1 P01 | 12 min | 7 tasks | 6 files |
| Phase 03-internal-refactor-coverage-hardening P01 | 4 min | 3 tasks | 4 files |
| Phase 03-internal-refactor-coverage-hardening P02 | 5 min | 1 tasks tasks | 2 files files |
| Phase 03-internal-refactor-coverage-hardening P03 | 60 min | 16 commits | 73 files |
| Phase 03-internal-refactor-coverage-hardening P04 | 7 min | 1 atomic commit (Rule 4) | 30 files |
| Phase 03-internal-refactor-coverage-hardening P05 | 17 min | 2 atomic commits | 16 files |
| Phase 03-internal-refactor-coverage-hardening P06 | 16 min | 4 atomic commits | 5 files |
| Phase 03-internal-refactor-coverage-hardening P07 | 75 min | 39 atomic commits + 3 batch-summary docs | 39 files |
| Phase 03-internal-refactor-coverage-hardening P08 | 7 min | 2 atomic commits | 4 files |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Initialization: Anchor priority is Clean & Green (lint/types/deps/CI/coverage) — unblock the baseline before chasing security/performance.
- Initialization: Deprecations OK in 3.0.x; removals deferred to 3.2.0.
- Initialization: Internal refactor is cleanup-only; no Cement 4 architectural seams.
- Initialization: Python 3.9 dropped this milestone (EOL Oct 2025) per standing policy.
- Initialization: Release cut as 3.0.16 (even-patch convention); current dev = 3.0.15.
- [Phase 01-tooling-baseline-python-matrix]: D-05 atomic-commit pattern proven on a 9-file change: all Python 3.9 traces dropped in a single conventional commit (chore: drop python 3.9 from supported matrix, 00d37e16) without splitting. — Validates D-05: ALL 3.9 traces simultaneously. Bisect anchor is clean — before this commit 3.9 supported, after it dropped. PYVER-03 audit grep returned empty on first pass.
- [Phase 01-tooling-baseline-python-matrix]: Travis CI configuration deleted entirely (.travis.yml) rather than partially edited to drop 3.8/3.9 entries. — Travis is no longer cement's CI; GitHub Actions is. Per RESEARCH.md Pitfall 7 + Open Question 2, keeping a non-active CI definition is dead infrastructure and a future-grep liability. Deletion satisfies D-05 ALL-3.9-traces cleanly.
- [Phase 01-tooling-baseline-python-matrix]: D-13/D-14 strict-minimum upheld: cement/utils/fs.py from __future__ import annotations and the self-flagged remove-after-3.9-EOL comment stay in place this phase. — Phase 1 is mechanical-removal-only; modernization-style cleanup defers to Phase 3 REFACTOR-04. The PYVER-03 audit grep filter explicitly excludes the __future__ line for this reason.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 02]: D-15 coupling held — ruff pin (~=0.15.12) + preview flip + 11-family extend-select + AUDIT POINT comment all land in ONE chore: bump ruff to 0.15 commit. Pin and bump are inseparable for D-08 hybrid drift detection.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 02]: A001/A002 absorbed via broad-ignore in [tool.ruff.lint] ignore (Option C from plan). 18 sites cluster across 5 files in framework-intentional builtin-shadowing patterns matching Python stdlib conventions (logging.Formatter format kwarg, Tmp.__init__ dir kwarg). Same posture attrs uses for the same reason; per-call noqa rejected as polluting too many sites for a structurally pervasive pattern.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 02]: C901 absorbed in [tool.ruff.lint] ignore with Phase 3 REFACTOR-01/02 cross-reference (RESEARCH.md Open Question 3 explicit recommendation). 12 hot-spot functions in cement/core/foundation.py + handler.py exceed default complexity 10; refactoring violates D-13 strict-minimum. Adding C90 family to extend-select keeps the signal active for new code.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 02]: D-04 one-commit-per-rule-family proven across 8 families (185 violations resolved in 8 atomic fix(lint): commits). Each commit is independently revertable, each fix is annotated with the rule code in the commit subject, and bisect can pinpoint exactly which family's fix introduced any regression.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 02]: PT013 ruff 0.15 reversed its preference (now wants 'import pytest' instead of 'from pytest import raises') vs the existing cement convention (cited at tests/core/test_exc.py). Absorbed via per-file-ignore on tests/**/*.py rather than mass-rewriting the convention — mass-rewrite would itself be a D-13 strict-minimum violation. Documented as deviation from RESEARCH.md prediction.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 03]: D-15 coupling pattern repeated — mypy pin (~=1.20.2) + AUDIT POINT comment land in single chore: bump mypy to 1.20 commit. Same shape as Plan 02's chore: bump ruff. Pattern generalized across both ruff and mypy.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 03]: D-11 strict preservation held — ZERO mypy strictness knob value changed; the only [tool.mypy] addition was the 4-line AUDIT POINT comment block. Knob tightening explicitly deferred to Phase 3 REFACTOR-02.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 03]: D-13 strict-minimum on handler.py:394 — chose # type: ignore append over narrowing assertion. Mirrors framework's established sibling pattern at lines 387/389/390/393/395 (all use # type: ignore for the same MetaMixin/Meta union-attr pattern). Phase 3 REFACTOR-02 may revisit.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 03]: Line drift acknowledged — RESEARCH.md cited line 392; Plan 02 lint fixes shifted union-attr site to line 394. Same code, same fix. Plan anticipated this with read-line-numbers-first directive.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 04]: D-15 coupling generalized to floor-only test-tool family — pytest, pytest-cov, coverage all bumped (>=) in single chore: bump pytest+pytest-cov+coverage commit. Pattern now proven across both ~= (ruff/mypy) and >= (pytest-family) pin types.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 04]: D-13 strict-minimum honored absolutely — ZERO test-config or test-code modernization. [tool.pytest.ini_options] untouched. RESEARCH.md prediction (cement test surface bug-clean against pytest 9.0/pytest-cov 7.0/coverage 7.13) verified — no fix(test): commits needed.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 04]: Pitfall 3 (pytest-cov 7.0 subprocess-measurement removal) verified no-op for cement — cement/utils/shell.py 129/0/100% and cement/cli/main.py 28/0/100% pre/post-bump identical. Per-module Miss=0 held across cement/ tree. TOTAL stmt-count drift (3311->3285) is coverage 7.6->7.13 detection-heuristics internal, not a coverage regression.
- [Phase ?]: [Phase 01-tooling-baseline-python-matrix Plan 04]: Phase 1 implementation COMPLETE — all 5 ROADMAP cumulative success criteria GREEN (PYVER-01/02, TOOL-01/02/03/04). 13 atomic phase-1 commits across 4 plans. CI matrix (3.10/3.11/3.12/3.13/3.14/pypy3.10) is the final verification gate on PR open.
- [Phase ?]: [Phase 01.1 Plan 01]: pdm-backend migration green on full Python 3.10-3.14 matrix; build-time cement dependency removed; setup.py-era files (5) deleted; PEP 735 dev deps via [dependency-groups].
- [Phase ?]: [Phase 01.1 Plan 01]: Rule 1 deviation auto-fixed: tests/cli/test_main.py::test_generate updated to assert pyproject.toml exists (was setup.py). Regression caught in Task 7 acceptance check after Task 4 deletion; mechanical one-line fix preserves end-to-end behavior validation.
- [Phase 03 Plan 01]: AST walker extended beyond RESEARCH.md canonical pattern to include `ast.ImportFrom` and `ast.Import` re-exports — required to surface `cement/__init__.py`'s 14 `__all__` entries (Open Question 4 / Assumption A6). Without this extension the walker would have emitted ZERO public symbols for the `cement:` namespace, defeating the audit gate.
- [Phase 03 Plan 01]: AST walker filters `from __future__ import` and collapses `<pkg>/__init__.py` module names to drop the `__init__` suffix — both deviations were necessary to produce a faithful "what users `from cement import` against" surface.
- [Phase 03 Plan 01]: D-04 audit gate is now ENFORCING (1014-line baseline, byte-for-byte). Every subsequent Phase 03 commit MUST keep `make audit-public-api` exit 0. Permanent dev affordance per D-05; mirrors `scripts/cli-smoke-test.sh` precedent from quick task `260430-i7q`.
- [Phase 03 Plan 01]: Sort discipline is Python's `sorted()` (ASCII byte order = `LC_ALL=C sort`). Shell `sort -c` under default locale flags `Optional` < `main` as disorder; irrelevant for the gate which uses `diff -u` byte-for-byte against the captured baseline.
- [Phase ?]: [Phase 03 Plan 02]: D-15 coupling pattern reused for config-knob — UP+FA family addition + AUDIT POINT comment refresh land atomically in chore(ruff): re-enable UP family (b8427466). 491 UP+FA findings surfaced (378 auto-fixable) — Wave 3 expected fix volume captured in 03-02-SUMMARY.md per-rule breakdown.
- [Phase ?]: [Phase 03 Plan 02]: FA family currently surfaces ZERO findings — confirms D-08 ordering rationale (FA100 strip is gated on UP006/UP007/UP045 landing first; once typing imports prune to modern surface, FA100 surfaces naturally for Wave 4).
- [Phase 03 Plan 03]: User-approved mid-execution Rule 4 architectural decision: re-baseline `03-PUBLIC-API-BASELINE.txt` per UP commit when the rule prunes orphaned typing re-exports. Phase 03 IS the intentional API change window per D-04 reinterpretation. The 51+ orphaned `typing.{List,Dict,Tuple,Type,Union,Optional}` re-exports being pruned were never genuine public API — they were tooling artifacts of the pre-PEP-585 era. Applied to UP006/UP007/UP045 commits (1014 → 934 baseline lines); UP035 / UP031 / UP004 / UP008 / UP015 / UP024 / UP025 / UP026 / UP028 / UP032 left audit byte-for-byte green and required no rebase (preserves audit signal).
- [Phase 03 Plan 03]: D-19 protected `.format(**template_dict)` callsite line numbers (CONTEXT.md cites 1359..1567) drifted by 1-7 lines during Wave 3 due to UP006/UP007/UP045/UP032 line-length changes. Verified protection via body-diff (line numbers stripped) rather than literal line-number diff. All 14 sites byte-for-byte preserved at lines 1352, 1357, 1365, 1370, 1378, 1383, 1471, 1476, 1481, 1485, 1546, 1551, 1556, 1560 (post Wave 3). Recorded in deferred-items.md.
- [Phase 03 Plan 03]: REFACTOR-04 mechanically closed. UP031 (printf → modern format) + UP032 cascade (.format → f-string) together resolved all 114 printf/format-style sites. UP family fully clean end-to-end. FA family still ZERO findings — Wave 4 may have minimal work.
- [Phase ?]: [Phase 03 Plan 04]: Plan body's ruff FA100 --fix mechanism does NOT remove from __future__ import annotations — FA100 only adds. User-approved Rule 4: hand-strip + targeted PEP 484 string-quoting in one atomic commit. 76 forward-reference sites quoted (App, FrameType, ModuleType, TracebackType, ArgparseArgumentType, ArgparseController) at definition-time-evaluated annotation positions only. Local annotations in method bodies left unquoted per PEP 526; ruff UP037 confirms via auto-fix.
- [Phase ?]: [Phase 03 Plan 04]: RESEARCH.md A2 'HIGH confidence safe' claim was incomplete — TYPE_CHECKING import safety and annotation-runtime-evaluation safety are orthogonal concerns. A2 verified the former; the latter required PEP 484 string-quoting at definition-time-evaluated sites once the future import was removed.
- [Phase ?]: [Phase 03 Plan 04]: D-24 conjunct #9 GREEN; Phase 1 D-14 deferral closed; cement/utils/fs.py self-flagged 2024-06-22 TODO removed. D-24 conjuncts #1/#2/#3/#4/#5/#9 GREEN through Wave 4; #6, #7, #8 deferred to Plans 05+.
- [Phase 03 Plan 05]: Conservative D-09 tightening discipline applied — only `App.__import__` (dunder, EXPERIMENTAL UNDOCUMENTED, not in 03-PUBLIC-API-BASELINE.txt) and `_dispatch` (internal underscore-prefixed abstract method) tightened. Everything in the public-API baseline keeps its declared type per D-12. RESEARCH.md A3's "5-10 realistic" upper bound was the planning-time estimate; actual delta of 2 substantive sites reflects that the bulk of Any in cement/core/ is required by the public contract (handler-contract pluggable kwargs, user-arbitrary config/template/render/cache data, argparse opacity, signal-frame opacity).
- [Phase 03 Plan 05]: Pre-baseline +1 drift recorded (RESEARCH.md verified 40 on 2026-05-03; live count 41 on 2026-05-04). Drift traced to grep visibility of the post-Wave-4 PEP 484 string-quoted signal-handler signature at foundation.py:127 — substantive Any surface unchanged.
- [Phase 03 Plan 05]: D-09 inline justification convention established — every surviving Any in cement/core/ (40 sites) carries a `# D-09: ...` comment placed at the function definition (or class-level attribute) tagging it as handler-contract / user-arbitrary / argparse-opacity / signal-frame-opacity / UNDOCUMENTED. Mirrors COV-03 pragma policy and Phase 1 D-08 AUDIT POINT pattern.
- [Phase 03 Plan 05]: Comment text MUST avoid the literal grep regex (`Any]`, `: Any`, `-> Any`) so justification prose doesn't pollute the post-count. Early drafts triggered 3 false-positive matches; reworded to use plain English. Pattern recorded for future inventory-style audits.
- [Phase 03 Plan 05]: D-24 conjunct #6 GREEN (Any post < pre — 41 → 40, REFACTOR-02 acceptance). #1/#2/#3/#4/#5/#6/#9 GREEN through Wave 5; #7, #8 deferred to Plans 06/07.
- [Phase 03 Plan 05]: Deferred item logged inline at handler.py:332 — `def resolve(...) -> Handler | Handler | None` carries a duplicate `Handler` union member (Wave 3 UP007 cascade artifact, semantically equivalent to `Handler | None`). Out-of-scope for D-09 Any-tightening; defer to a future tech-debt cleanup or Phase 5.
- [Phase ?]: [Phase 03 Plan 06]: Pathlib migration completed across 4 named files (cement/utils/fs.py + cement/core/{config,foundation,template}.py). 33 -> 1 (tagged) os.path callsites; D-24 conjunct #8 GREEN. _Path private alias convention: from pathlib import Path as _Path keeps audit-public-api baseline byte-identical (a public Path import would surface as a new public symbol per D-01). Used in all 4 migrated files.
- [Phase ?]: [Phase 03 Plan 06]: Surviving public alias join = os.path.join in cement/core/foundation.py:48 retained per D-12/D-14 with inline # boundary: tag — it is in 03-PUBLIC-API-BASELINE.txt (cement.core.foundation:join) with stdlib semantics that downstream callers depend on. os.walk(src) in cement/core/template.py:209 retained per Task 5 plan decision (pathlib has no triple-tuple equivalent; restructure too risky). Both decisions cement the # boundary: D-14 inline-tag pattern as the audit-grep-friendly convention.
- [Phase ?]: [Phase 03 Plan 06]: import os retained in cement/core/config.py with # noqa: F401 # boundary: ... (D-12). cement.core.config:os is in the public-API baseline; removing the now-unused import would have shrunk the public surface (downstream code doing 'from cement.core.config import os' would have broken). Same surface-preservation discipline as the join alias decision; generalizable pattern for future migrations.
- [Phase ?]: [Phase 03 Plan 06]: A7 symlink pre-flight executed (find tests/ -type l + find cement/ -type l) — 0 symlinks in scope. Decision: Path(p).expanduser().resolve(strict=False) — matches os.path.abspath(os.path.expanduser(p)) semantics for non-symlink paths per RESEARCH.md A7 decision tree. Recorded in cement/utils/fs.py commit body (6af95ee9) for auditability.
- [Phase 03 Plan 07]: D-15 locked-vocabulary pragma audit completed across 141 sites / 39 files in cement/. Per-file atomic commits per D-18 (39 source commits + 3 batch-summary docs commits). Per-category breakdown: defensive: unreachable=51, abstract method=45, TYPE_CHECKING import=26, platform-specific=13, untestable: dynamic import=4, version constant=1, untestable: signal handler=1, total=141. D-24 conjunct #7 GREEN.
- [Phase 03 Plan 07]: NO D-16 vocabulary expansion triggered. Three borderline cases — ext_daemon FD ops (daemonize/cleanup function-level pragmas), interactive Prompt/getpass calls (cement/utils/shell.py + cement/ext/ext_generate.py:87), Mailpit-accepts-everything SMTP error branch (ext_smtp.py:187) — all resolved as `defensive: unreachable` via reasonable interpretation rather than expanding the locked vocabulary. The spirit of `defensive: unreachable` (paths coverage cannot prove unreachable but pragmatically never execute in tests) covers them adequately.
- [Phase 03 Plan 07]: utils/version.py:104-105 labeled `defensive: unreachable` not `untestable: subprocess`. The actual subprocess.Popen call at lines 97-101 runs end-to-end in tests; only the post-subprocess `except ValueError` defensive parse fallback is pragma'd. RESEARCH.md A4's preliminary classification was a coarse line range; refined here.
- [Phase 03 Plan 07]: Multi-line import-block rewrite during pragma append (foundation.py:41 + ext_argparse.py:17) — ruff I001 isort auto-fix split single-line `from ... import A, B, C  # pragma: nocover` into multi-line `from ... import (...)` blocks because the appended `# TYPE_CHECKING import` label crossed the 100-char limit. Coverage exclusion behavior preserved (pragma applies to entire import statement). Pattern generalizable for future label-append work where the original import was at-or-near 100 chars pre-append.
- [Phase 03 Plan 07]: Aligned trailing-comment compression for E501 — sites with aesthetic alignment padding before `# pragma` had alignment trimmed (5-10 char trim) to fit the post-append within 100 chars. A small subset (cli/main.py:49, ext_colorlog.py:106, ext_generate.py:162, ext_plugin.py:69/71/75/77) needed an additional `# noqa: E501` sibling AFTER the pragma + category label so the audit grep still matches.
- [Phase 03 Plan 07]: Dual-spelling preservation — both `# pragma: nocover` and `# pragma: no cover` spellings preserved (NOT canonicalized) per RESEARCH.md state-of-the-art note. Audit regex matches both via `[[:space:]]*` quantifier between `no` and `cover`.
- [Phase 03 Plan 08]: REFACTOR-01 accepted via D-20 (100% coverage gate) — NOT via vulture. Adding vulture purely for one acceptance gate would have violated Phase 03 D-13 strict-minimum dev-dep policy. The 100% coverage gate (`fail_under = 100` + `--cov-fail-under=100`) provides the strongest available signal at zero incremental dev-dep cost. D-21 risk acknowledged in 03-VERIFICATION.md: covered-but-functionally-dead code (executes in tests without meaningful asserts) and unused private helpers reachable only from tests remain undetected; future milestones (3.2.0 cleanup or dedicated audit milestone) may re-open with vulture if these gaps prove to bite.
- [Phase 03 Plan 08]: Defense-in-depth final reset (make superclean && make init && full gate suite) executed BEFORE 03-VERIFICATION.md status flips to passed. Per RESEARCH.md Runtime State Inventory, annotation-syntax changes (UP006/007/045 + FA100 in Waves 3/4) invalidate `.mypy_cache/` AST analysis; running the full gate suite against fresh caches confirms no cache pollution is masking a regression. All 5 reset gates exit 0; 9-conjunct evidence captured against the freshly-rebuilt environment. Pattern generalizes for any multi-wave refactor phase touching annotation syntax or import structure.
- [Phase 03 Plan 08]: Two atomic commits at phase close (verification artifact + ROADMAP/REQUIREMENTS/CHANGELOG roll-up), NOT one mega-commit. Preserves bisect granularity — the verification artifact change is independent of the milestone-tracking flip; either could be reverted alone if a downstream issue surfaces. REQUIREMENTS.md folded into the docs(roadmap): commit (not its own commit) because flipping REFACTOR-01 [ ] → [x] is itself a milestone-tracking change directly supported by the verification artifact.
- [Phase 03 Plan 08]: Plan 08 D-24 9-Conjunct Acceptance evidence shape (# | Gate | Command | Expected | Result | Status) generalizes from Phase 1 + Phase 2 D-19 acceptance gate patterns — downstream phases (Phase 4, 5, 6) can reuse this exact table shape. Inline per-conjunct evidence transcripts (### subsection per conjunct with actual command + actual exit + actual stdout snippet) provide forensic-grade evidence vs. summary-only acceptance tables, favored when the phase has multiple acceptance gates with non-trivial output.
- [Phase 03 Plan 08]: Phase 3 closed: 84 total commits on modernization-phase-3 branch across 8 waves (Wave 1: 3 / Wave 2: 2 / Wave 3: 18 / Wave 4: 2 / Wave 5: 4 / Wave 6: 6 / Wave 7: 43 / Wave 8: 4 — including planning artifacts and ad-hoc lint touch-ups). All 7 phase requirements (REFACTOR-01..04, COV-01..03) SATISFIED with traceability into 03-VERIFICATION.md. All 5 ROADMAP Phase 3 success criteria SATISFIED. 100% coverage gate held continuously across every commit. 03-PUBLIC-API-BASELINE.txt (934 lines) byte-identical with live AST walk. Permanent dev affordances (scripts/audit-public-api.py + Makefile target + ruff UP+FA family + locked-vocabulary pragma audit + D-15 categories + boundary-tag convention) retained for future regression checks across all subsequent 3.0.x patch work.

### Roadmap Evolution

- Phase 01.1 inserted after Phase 1: Generated Project Template Build Modernization (URGENT) — PEP 517 build isolation fails because the generated `cement generate project` template imports cement at build time via setup.py → version.py. Blocks Phase 2 CI-green goal; smoke test cannot pass on the matrix until template no longer requires cement (or any runtime dep) at build time.

### Pending Todos

- [`2026-05-08-resolve-issue-777-extensions-config-section`](./todos/pending/2026-05-08-resolve-issue-777-extensions-config-section.md) — analyze and resolve [#777](https://github.com/datafolklabs/cement/issues/777) (extensions config-override uses `Meta.label` instead of `Meta.config_section`; pickup after #760 merges)
- [`2026-05-09-document-optional-features-in-gitbook-post-3-0-16`](./todos/pending/2026-05-09-document-optional-features-in-gitbook-post-3-0-16.md) — author GitBook developer guide for `ext.generate` optional features ([#778](https://github.com/datafolklabs/cement/issues/778)); **blocked on 3.0.16 release cut**

### Plan-Phase Gate Overrides

- **Phase 2 / 2026-05-02 / decision-coverage gate** — D-16 (negative-space rule: "keep the serial job graph") and D-18 (meta convention governing `docs(02):` plan-artifact commits) are not explicitly cited in any plan's `must_haves`/`truths` block. User chose "Proceed anyway" — both decisions are correctly handled (D-16 by omission, no task touches the job graph; D-18 by the GSD workflow's own `docs(02): create phase plan` commit). Re-surface in `/gsd-verify-work` if the decisions are mis-handled at execution time.

### Blockers/Concerns

- Stalled `pdm update` GitHub Action (the user's pain point): drowning in ruff lint on each run. Phase 1 directly unblocks this.
- 100% coverage gate is absolute and must hold across every phase — no temporary relaxations.
- Public API surface includes subclass-exposed internals (downstream extensions may subclass); refactor must assume unknown third-party subclasses.

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 260430-3b0 | fix scripts/cli-smoke-test.sh — drop py3.9 default and modernize generated-project install path (phase-1 gap closure) | 2026-04-30 | 020ec7b7 | [260430-3b0-fix-scripts-cli-smoke-test-sh-drop-py3-9](./quick/260430-3b0-fix-scripts-cli-smoke-test-sh-drop-py3-9/) |
| 260430-i7q | add cli-smoke-test Makefile target wiring scripts/cli-smoke-test.sh | 2026-04-30 | 786a440e | [260430-i7q-add-cli-smoke-test-target-to-makefile-th](./quick/260430-i7q-add-cli-smoke-test-target-to-makefile-th/) |
| 260507-to4 | rewrite PR #760 — template_dirs config override via core_meta_override (resolves #746) | 2026-05-08 | c25562d5 | [260507-to4-rewrite-pr-760-template-dirs-config-over](./quick/260507-to4-rewrite-pr-760-template-dirs-config-over/) |

## Session Continuity

Last session: 2026-05-07T19:57:50.715Z
Stopped at: Phase 5 context gathered
Resume file: .planning/phases/05-deprecations-docs-security-stubs/05-CONTEXT.md
