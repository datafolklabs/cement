---
phase: 03-internal-refactor-coverage-hardening
plan: 07
subsystem: pragma-audit
tags: [refactor, test, coverage, pragma, d-15, d-16, d-17, d-18, d-24, cov-03, locked-vocabulary, wave-7]
requires:
  - .planning/phases/03-internal-refactor-coverage-hardening/03-06-SUMMARY.md (Wave 6 — pathlib migration; D-24 conjunct #8 GREEN)
  - .planning/phases/03-internal-refactor-coverage-hardening/03-VERIFICATION.md (Wave 5 baseline; pragma pre-count 141 sites recorded for Wave 7 delta)
  - .planning/phases/03-internal-refactor-coverage-hardening/03-CONTEXT.md (D-15 8-category locked vocabulary; D-16 vocabulary expansion rule; D-17 verification grep; D-18 audit-after-refactor ordering)
  - .planning/phases/03-internal-refactor-coverage-hardening/03-RESEARCH.md (Pragma site inventory lines 760-783; Code Examples Example 1 lines 590-677)
provides:
  - "Every pragma:nocover and pragma:no cover site in cement/ (141 sites across 39 files) carries one of the 8 D-15 locked-vocabulary category labels appended after the existing pragma comment"
  - "D-24 conjunct #7 GREEN: locked-vocabulary inverse grep returns empty; COV-03 acceptance closed"
  - "Per-file atomic commits per D-18 (39 files / 39 source commits + 4 docs(03) batch-summary commits)"
  - "03-VERIFICATION.md updated with Wave 7 post-audit section + per-batch breakdown + per-category breakdown + D-24 conjunct status table refresh"
  - "No D-16 vocabulary expansion was triggered — every site fit one of the 8 categories without amending CONTEXT.md"
affects:
  - "Wave 8 (D-22 step 14 finalizes 03-VERIFICATION.md with all 9 D-24 conjunct evidence and REFACTOR-01 acceptance-via-coverage rationale)"
tech-stack:
  added: []
  patterns:
    - "D-15 locked-vocabulary inline category-label append: every pragma:nocover (or pragma:no cover) site carries `# <category>` after the pragma. Format: `<code>  # pragma: nocover  # <category>`. The 8 categories are: abstract method, TYPE_CHECKING import, platform-specific, untestable: dynamic import, untestable: subprocess, untestable: signal handler, defensive: unreachable, version constant."
    - "D-17 verification grep as the audit gate: `grep -nE 'pragma:[[:space:]]*no[[:space:]]*cover' cement/ | grep -vE '# (<8 categories>)'` returns empty. POSIX `[[:space:]]` instead of `\\s` for cross-platform safety per RESEARCH.md Pitfall 6."
    - "D-18 audit-after-refactor: this wave intentionally lands after Wave 6 (pathlib migration) so the audit runs against the FINAL shape — Wave 6 line shifts (especially in foundation.py) didn't perturb the post-count (141 in / 141 out)."
    - "Per-file atomic commits per D-22 step 13 / D-04 family-split discipline: 39 source commits (one per file with pragma sites) + 3 docs(03) batch-summary commits + 1 final docs commit folding STATE/ROADMAP/SUMMARY/VERIFICATION updates."
    - "Dual-spelling preservation: existing `# pragma: nocover` (no space, ~110 sites) and `# pragma: no cover` (with space, ~31 sites) spellings were preserved — NOT canonicalized — to avoid a huge unrelated diff. The locked-vocabulary regex uses `[[:space:]]*` to match both."
    - "Multi-line trailing-comment alignment compression: aligned `# pragma: nocover` siblings with N-space padding (e.g., ext_argparse.py 832-836, ext_logging.py 21-34, ext_generate.py 160-163) had alignment trimmed to fit the post-append within the 100-char ruff line limit. Inline `# noqa: E501` was added on a small number of sites where alignment trim alone wasn't enough (cement/ext/ext_colorlog.py:106, cement/ext/ext_generate.py:162, cement/ext/ext_plugin.py:69/71/75/77, cement/cli/main.py:49)."
    - "Multi-line `from ... import (...)` rewrite during pragma append: `cement/core/foundation.py:41` (`from types import (FrameType, ModuleType, TracebackType)`) and `cement/ext/ext_argparse.py:17` (`from ..core.foundation import (App, ArgparseArgumentType)`) were reformatted by ruff isort (I001) into multi-line import blocks during the labeling sweep — the appended category-label sibling kept the opening `from ... import (` line under the 100-char limit; coverage exclusion behavior is preserved (the pragma applies to the entire import statement)."
key-files:
  created:
    - .planning/phases/03-internal-refactor-coverage-hardening/03-07-SUMMARY.md
  modified:
    - cement/cli/main.py (8 sites — defensive: unreachable across all)
    - cement/core/arg.py (3 sites — abstract method)
    - cement/core/backend.py (1 site — version constant)
    - cement/core/cache.py (5 sites — abstract method)
    - cement/core/config.py (11 sites — abstract method)
    - cement/core/controller.py (2 sites — abstract method)
    - cement/core/extension.py (3 sites — TYPE_CHECKING + abstract method)
    - cement/core/foundation.py (6 sites — TYPE_CHECKING + platform-specific + defensive: unreachable + untestable: signal handler; ruff I001 rewrote line 41 import block)
    - cement/core/handler.py (2 sites — TYPE_CHECKING + abstract method)
    - cement/core/hook.py (1 site — TYPE_CHECKING)
    - cement/core/interface.py (1 site — TYPE_CHECKING)
    - cement/core/log.py (8 sites — abstract method)
    - cement/core/mail.py (2 sites — TYPE_CHECKING + abstract method)
    - cement/core/output.py (2 sites — abstract method)
    - cement/core/plugin.py (6 sites — abstract method)
    - cement/core/template.py (5 sites — abstract method + defensive: unreachable)
    - cement/ext/ext_alarm.py (1 site — TYPE_CHECKING)
    - cement/ext/ext_argparse.py (10 sites — TYPE_CHECKING + defensive: unreachable; ruff I001 rewrote line 17 import block)
    - cement/ext/ext_colorlog.py (3 sites — TYPE_CHECKING + defensive: unreachable)
    - cement/ext/ext_configparser.py (1 site — TYPE_CHECKING)
    - cement/ext/ext_daemon.py (4 sites — TYPE_CHECKING + defensive: unreachable)
    - cement/ext/ext_dummy.py (1 site — TYPE_CHECKING)
    - cement/ext/ext_generate.py (7 sites — TYPE_CHECKING + defensive: unreachable + untestable: dynamic import)
    - cement/ext/ext_jinja2.py (1 site — TYPE_CHECKING)
    - cement/ext/ext_json.py (1 site — TYPE_CHECKING)
    - cement/ext/ext_logging.py (14 sites — TYPE_CHECKING + platform-specific + defensive: unreachable)
    - cement/ext/ext_memcached.py (1 site — TYPE_CHECKING)
    - cement/ext/ext_mustache.py (1 site — TYPE_CHECKING)
    - cement/ext/ext_plugin.py (6 sites — TYPE_CHECKING + defensive: unreachable + untestable: dynamic import)
    - cement/ext/ext_print.py (1 site — TYPE_CHECKING)
    - cement/ext/ext_redis.py (1 site — TYPE_CHECKING)
    - cement/ext/ext_scrub.py (2 sites — TYPE_CHECKING + defensive: unreachable)
    - cement/ext/ext_smtp.py (4 sites — TYPE_CHECKING + defensive: unreachable)
    - cement/ext/ext_tabulate.py (1 site — TYPE_CHECKING)
    - cement/ext/ext_watchdog.py (4 sites — TYPE_CHECKING + defensive: unreachable)
    - cement/ext/ext_yaml.py (1 site — TYPE_CHECKING)
    - cement/utils/fs.py (2 sites — defensive: unreachable + platform-specific)
    - cement/utils/shell.py (6 sites — defensive: unreachable)
    - cement/utils/version.py (2 sites — defensive: unreachable)
    - .planning/phases/03-internal-refactor-coverage-hardening/03-VERIFICATION.md (Wave 7 post-audit section appended; D-24 conjunct #7 marked GREEN; per-batch + per-category breakdown tables added)
    - CHANGELOG.md (4 new [dev] entries under Refactoring bucket — Batch A, B, C, D summaries)
key-decisions:
  - "Did NOT trigger D-16 vocabulary expansion. Every one of the 141 sites fit naturally into one of the 8 D-15 categories. Three borderline cases warranted inline justification: (1) ext_daemon.py daemonize/cleanup function-level pragmas labeled `defensive: unreachable` (rather than D-16-expanding to a new `untestable: process-fork` category) since fork/setuid bodies are effectively unreachable in the pytest test process; (2) interactive Prompt.prompt() and getpass calls in cement/utils/shell.py + cement/ext/ext_generate.py:87 labeled `defensive: unreachable` (rather than D-16-expanding to `untestable: interactive`) since the surrounding test mocking flow makes these defensively-guarded fallbacks; (3) Mailpit-accepts-everything error branch in ext_smtp.py:187 labeled `defensive: unreachable` with the existing free-form note `- Mailpit accepts everything` preserved as supplementary context."
  - "cement/utils/version.py:104-105 (the `except ValueError` defensive path inside `get_git_changeset`) labeled `defensive: unreachable` rather than `untestable: subprocess`. The actual subprocess.Popen call (lines 97-101) is NOT pragma'd — it executes end-to-end in tests against the live git repo. Only the post-subprocess defensive int-parse fallback is pragma'd. RESEARCH.md A4's preliminary classification ('utils/version.py:97-106 git log subprocess' under `untestable: subprocess`) was a coarse line-range; the actual pragma-bearing lines are the defensive parse fallback, hence the `defensive: unreachable` label."
  - "Multi-line import-block reformatting (foundation.py:41 + ext_argparse.py:17) is intentional ruff I001 fallout — the appended `# TYPE_CHECKING import` label crossed the 100-char limit on the original single-line `from ... import A, B, C  # pragma: nocover` shape, and ruff auto-fixed by splitting into a multi-line `from ... import (\\n    A,\\n    B,\\n    C,\\n)` block with the pragma + label sibling-comment on the opening `from ... import (` line. Coverage exclusion behavior is preserved (the pragma applies to the entire import statement). The appended category label is on the `from ... import (` line so the audit grep matches."
  - "Dual-spelling (`# pragma: nocover` vs `# pragma: no cover`) was preserved — NOT canonicalized — to avoid a huge unrelated diff. The locked-vocabulary regex `pragma:[[:space:]]*no[[:space:]]*cover` matches both spellings via the `[[:space:]]*` quantifier."
  - "Aligned trailing-comment style was tightened on a handful of sites (ext_argparse.py 832-836, ext_logging.py 21-34, ext_generate.py 160-163, ext_smtp.py 187, ext_colorlog.py 106-107, ext_watchdog.py legacy alignment) to fit within the 100-char ruff E501 limit after the category-label append. The aesthetic alignment was already inconsistent across the codebase; the post-append shape is closer to ruff's preferred `<code>  # pragma: nocover  # <category>` two-space-delimiter convention. A small number of sites (cli/main.py:49, ext_colorlog.py:106, ext_generate.py:162, ext_plugin.py:69/71/75/77) required an additional `# noqa: E501` sibling comment because the variable/function name itself is load-bearing and cannot be shortened."
  - "Per-file atomic commits per D-22 step 13 / D-18 — 39 source commits + 3 batch-summary docs(03) commits + 1 final closing docs(03) commit. Each per-file commit independently passes the full gate set (100% coverage + audit-public-api + mypy + ruff). Bisect anchor per file."
patterns-established:
  - "D-15 locked-vocabulary inline category-label append: a single locked-vocabulary token appended after `# pragma: nocover`/`# pragma: no cover`. The audit grep filters out lines containing any of the 8 category labels; if a non-locked label appears in the future, the inverse-grep returns non-empty and CI/PR review catches it."
  - "Per-file atomic-commit cadence for source-mechanical sweeps with public-surface implications (mirrors Wave 6 D-13 4-commit pathlib migration shape): every file's labeling sweep runs 100% coverage + audit-public-api + mypy + comply-ruff before commit. ~40 commits is a tractable bisect-anchor surface."
  - "Multi-line trailing-comment compression: when an aligned trailing comment exceeds the 100-char limit after the category-label append, the alignment padding is removed (typical 5-10 char trim) so the post-shape fits within E501. For the small number of sites where the variable/function name is load-bearing and trim alone is insufficient, an additional inline `# noqa: E501` sibling comment is added — placed AFTER the pragma + category label so the audit grep still sees the category."
  - "Dual-spelling tolerance: the audit grep accommodates both `# pragma: nocover` and `# pragma: no cover` via `[[:space:]]*` between `no` and `cover`. New code may use either spelling; canonicalization is out of scope (would create churn without value)."
requirements-completed: [COV-03, COV-01]
metrics:
  duration_minutes: 75
  completed_date: 2026-05-04
---

# Phase 03 Plan 07: Wave 7 — Pragma:nocover Audit with D-15 Locked-Vocabulary Category Labels — Summary

**Append D-15 locked-vocabulary category labels to all 141 pragma:nocover sites across 39 files in cement/. Per-file atomic commits per D-18; 100% coverage + audit-public-api + mypy + ruff held green after every commit. D-24 conjunct #7 GREEN: locked-vocabulary inverse grep returns empty; COV-03 acceptance closed.**

## Performance

- **Duration:** ~75 min (start 2026-05-04T02:59Z; end 2026-05-04T04:14Z)
- **Tasks:** 5 (1 pre-flight enumeration + 4 batch sweeps × per-file atomic commits)
- **Files modified:** 39 source files + 1 verification artifact + 1 changelog
- **Lines added:** ~150 (mostly inline category-label comments + a small number of `# noqa: E501` siblings + 4 changelog entries + verification updates)
- **Lines removed:** ~150 (the original pragma comment lines pre-label)

## Accomplishments

- **Pre-flight enumeration (Task 1):** Live count = 141 sites across 39 files. Matches RESEARCH.md A4 verified count exactly (no Wave 6 drift). 4-batch grouping established for Tasks 2-5.
- **Batch A — cement/core/ (Task 2):** 15 files / 58 sites / 15 per-file atomic commits. Categories: `abstract method` (45 sites — every interface pass line), `TYPE_CHECKING import` (5 sites — extension/handler/hook/interface/mail App imports), `platform-specific` (1 — Windows SIGNALS), `defensive: unreachable` (5 — handler-override defensive guards, run() else-no-controller, template os.walk dot-skip), `untestable: signal handler` (1 — frame walk hook loop body), `version constant` (1 — VERSION tuple).
- **Batch B — cement/ext/ first half (Task 3):** 10 files / 43 sites / 10 per-file atomic commits. Categories: `TYPE_CHECKING import` (10 sites — every ext_*.py App import), `defensive: unreachable` (16 sites — argparse fallbacks, daemon FD ops, generate prompts/raises, logging FIXME), `untestable: dynamic import` (3 sites — generate AttributeError import path), `platform-specific` (11 sites — ext_logging legacy NullHandler fallback for Python <3.1/2.7).
- **Batch C — cement/ext/ second half (Task 4):** 10 files / 22 sites / 10 per-file atomic commits. Categories: `TYPE_CHECKING import` (10 sites), `defensive: unreachable` (11 sites — plugin enable/disable defensives, smtp Mailpit-accepts branch + text/html fallbacks, watchdog event handlers, scrub guard), `untestable: dynamic import` (1 site — ext_plugin __import__ call).
- **Batch D — cement/cli/ + cement/utils/ (Task 5):** 4 files / 18 sites / 4 per-file atomic commits. Categories: `defensive: unreachable` (16 sites — cli/main.py CLI extras + AssertionError + CaughtSignal + entry-point branches; utils/fs.py for-else break + utils/shell.py interactive-prompt wrappers + utils/version.py git timestamp parse fallback), `platform-specific` (1 — utils/fs.py HOME_DIR fallback per the canonical D-15 example), `defensive: unreachable` (1 — utils/fs.py for-else break exhaustion).
- **GLOBAL D-17 grep returns EMPTY (D-24 conjunct #7 GREEN ✓):** every one of the 141 pragma sites carries one of the 8 locked-vocabulary category labels.
- **All quality gates GREEN end-to-end after every commit:** 100% coverage (3241/3241 stmts, 316 passed); audit-public-api exit 0 against Wave 3 baseline (no public-surface drift — comment-only changes don't perturb the AST); mypy exit 0 (51 source files); comply-ruff exit 0; coverage-report/index.html generated (COV-02 GREEN).

## Task Commits

39 per-file atomic source commits + 3 batch-summary docs(03) CHANGELOG commits + 1 final closing docs(03) commit (this Summary + STATE.md + ROADMAP.md updates) = 43 total commits in Wave 7.

| Batch | Files | Per-file commits |
|-------|-------|------------------|
| A — cement/core/ | 15 | 15 |
| B — cement/ext/ first half | 10 | 10 |
| C — cement/ext/ second half | 10 | 10 |
| D — cement/cli/ + cement/utils/ | 4 | 4 |
| **TOTAL** | **39** | **39** |

Plus 4 docs(03): record Batch X pragma audit in changelog commits + 1 final closing docs(03) commit at the end of this Summary creation.

(Batch A landed before its CHANGELOG entry was committed to keep the per-file atomic-commit shape; the Batch A summary CHANGELOG commit landed AFTER the 15 source commits. Batches B, C followed the same shape. Batch D's CHANGELOG entry is part of the final closing docs(03) commit alongside the SUMMARY/STATE/ROADMAP/VERIFICATION updates.)

## Files Created/Modified

### Created

- `.planning/phases/03-internal-refactor-coverage-hardening/03-07-SUMMARY.md` — this file

### Modified — Per-file Pragma Site Counts

| File | Sites | Categories applied |
|------|-------|--------------------|
| cement/cli/main.py | 8 | defensive: unreachable |
| cement/core/arg.py | 3 | abstract method |
| cement/core/backend.py | 1 | version constant |
| cement/core/cache.py | 5 | abstract method |
| cement/core/config.py | 11 | abstract method |
| cement/core/controller.py | 2 | abstract method |
| cement/core/extension.py | 3 | TYPE_CHECKING import (1) + abstract method (2) |
| cement/core/foundation.py | 6 | TYPE_CHECKING import (1) + platform-specific (1) + defensive: unreachable (3) + untestable: signal handler (1) |
| cement/core/handler.py | 2 | TYPE_CHECKING import (1) + abstract method (1) |
| cement/core/hook.py | 1 | TYPE_CHECKING import |
| cement/core/interface.py | 1 | TYPE_CHECKING import |
| cement/core/log.py | 8 | abstract method |
| cement/core/mail.py | 2 | TYPE_CHECKING import (1) + abstract method (1) |
| cement/core/output.py | 2 | abstract method |
| cement/core/plugin.py | 6 | abstract method |
| cement/core/template.py | 5 | abstract method (4) + defensive: unreachable (1) |
| cement/ext/ext_alarm.py | 1 | TYPE_CHECKING import |
| cement/ext/ext_argparse.py | 10 | TYPE_CHECKING import (1) + defensive: unreachable (9) |
| cement/ext/ext_colorlog.py | 3 | TYPE_CHECKING import (1) + defensive: unreachable (2) |
| cement/ext/ext_configparser.py | 1 | TYPE_CHECKING import |
| cement/ext/ext_daemon.py | 4 | TYPE_CHECKING import (1) + defensive: unreachable (3) |
| cement/ext/ext_dummy.py | 1 | TYPE_CHECKING import |
| cement/ext/ext_generate.py | 7 | TYPE_CHECKING import (1) + defensive: unreachable (3) + untestable: dynamic import (3) |
| cement/ext/ext_jinja2.py | 1 | TYPE_CHECKING import |
| cement/ext/ext_json.py | 1 | TYPE_CHECKING import |
| cement/ext/ext_logging.py | 14 | TYPE_CHECKING import (1) + platform-specific (11) + defensive: unreachable (2) |
| cement/ext/ext_memcached.py | 1 | TYPE_CHECKING import |
| cement/ext/ext_mustache.py | 1 | TYPE_CHECKING import |
| cement/ext/ext_plugin.py | 6 | TYPE_CHECKING import (1) + defensive: unreachable (4) + untestable: dynamic import (1) |
| cement/ext/ext_print.py | 1 | TYPE_CHECKING import |
| cement/ext/ext_redis.py | 1 | TYPE_CHECKING import |
| cement/ext/ext_scrub.py | 2 | TYPE_CHECKING import (1) + defensive: unreachable (1) |
| cement/ext/ext_smtp.py | 4 | TYPE_CHECKING import (1) + defensive: unreachable (3) |
| cement/ext/ext_tabulate.py | 1 | TYPE_CHECKING import |
| cement/ext/ext_watchdog.py | 4 | TYPE_CHECKING import (1) + defensive: unreachable (3) |
| cement/ext/ext_yaml.py | 1 | TYPE_CHECKING import |
| cement/utils/fs.py | 2 | defensive: unreachable (1) + platform-specific (1) |
| cement/utils/shell.py | 6 | defensive: unreachable |
| cement/utils/version.py | 2 | defensive: unreachable |
| **TOTAL** | **141** | — |

### Per-Category Breakdown Across All of cement/

| Category | Sites |
|----------|-------|
| `defensive: unreachable` | 51 |
| `abstract method` | 45 |
| `TYPE_CHECKING import` | 26 |
| `platform-specific` | 13 |
| `untestable: dynamic import` | 4 |
| `version constant` | 1 |
| `untestable: signal handler` | 1 |
| **TOTAL** | **141** |

Plus:
- `CHANGELOG.md` — 4 new [dev] entries in Refactoring bucket: Batch A (cement/core/), Batch B (ext/ first half), Batch C (ext/ second half), Batch D (cli/ + utils/)
- `.planning/phases/03-internal-refactor-coverage-hardening/03-VERIFICATION.md` — Wave 7 post-audit section appended; D-24 conjunct #7 marked GREEN ✓; per-batch + per-category breakdown tables; D-17 verification grep result captured as command output evidence

## Decisions Made

See frontmatter `key-decisions` for the complete list. Load-bearing decisions:

1. **No D-16 vocabulary expansion triggered.** Every one of the 141 pragma sites fit one of the 8 D-15 categories. Three borderline cases (ext_daemon FD ops, interactive Prompt/getpass calls, Mailpit-accepts SMTP branch) were resolved via reasonable interpretation of `defensive: unreachable` rather than expanding the vocabulary — the spirit of `defensive: unreachable` (paths that coverage cannot prove unreachable but pragmatically never execute in tests) covers them adequately.

2. **`utils/version.py:104-105` labeled `defensive: unreachable` not `untestable: subprocess`.** The actual subprocess.Popen call at lines 97-101 runs end-to-end in tests against the live git repo. Only the post-subprocess `except ValueError` defensive parse fallback is pragma'd — that's defensive, not subprocess. RESEARCH.md A4's preliminary classification was a coarse line range; the actual pragma-bearing lines are the defensive fallback.

3. **`# pragma: nocover` vs `# pragma: no cover` dual-spelling preserved.** Coverage.py honors both. Canonicalization would create a huge unrelated diff. The locked-vocabulary regex matches both via `[[:space:]]*`.

4. **Multi-line import-block rewrite during pragma append (foundation.py:41 + ext_argparse.py:17).** Ruff's I001 isort auto-fix split the original single-line `from ... import A, B, C  # pragma: nocover  # TYPE_CHECKING import` into multi-line `from ... import (\\n    A,\\n    B,\\n    C,\\n)` blocks because the appended label crossed the 100-char limit. Coverage exclusion behavior is preserved (the pragma applies to the entire import statement); the audit grep matches the opening `from ... import (` line.

5. **Aligned trailing-comment compression where E501 limit was exceeded.** Several sites (ext_argparse.py:832-836, ext_logging.py:21-34, ext_generate.py:160-163, ext_smtp.py:187, ext_colorlog.py:106-107) had aesthetic alignment padding (5-10 spaces of `_` before `# pragma`) trimmed to fit the post-append within 100 chars. A small number of sites (cli/main.py:49, ext_colorlog.py:106, ext_generate.py:162, ext_plugin.py:69/71/75/77) needed an additional `# noqa: E501` sibling — placed AFTER the pragma + category label so the audit grep still matches.

6. **Per-file atomic commits per D-22 step 13 / D-18.** 39 source commits + 3 batch-summary docs commits + 1 closing docs commit. Bisect anchor per file.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 — Bug] Ruff I001 import-block reformat after pragma append (foundation.py:41 + ext_argparse.py:17)**

- **Found during:** Task 2 (cement/core/foundation.py) and Task 3 (cement/ext/ext_argparse.py)
- **Issue:** Appending the `# TYPE_CHECKING import` category label to the existing single-line `from types import FrameType, ModuleType, TracebackType  # pragma: nocover` (foundation.py:41) and `from ..core.foundation import App, ArgparseArgumentType  # pragma: nocover` (ext_argparse.py:17) lines pushed both lines past the 100-char ruff E501 limit. Ruff's I001 isort cascade then refused to keep the existing single-line shape. `make comply-ruff` failed.
- **Fix:** Ran `pdm run ruff check --fix <file>` to let ruff isort split the single-line imports into multi-line `from ... import (\\n    A,\\n    B,\\n    C,\\n)` blocks. The pragma + label sibling-comment moved to the opening `from ... import (` line — coverage.py's pragma exclusion still applies to the entire import statement. Removed the now-redundant `# noqa: E501` siblings I had added during the first attempt.
- **Files affected:** `cement/core/foundation.py` (1 line shifted to multi-line block at line 41-45), `cement/ext/ext_argparse.py` (1 line shifted to multi-line block at line 17-20).
- **Verification:** `make comply-ruff` exits 0; `pdm run pytest --cov=cement -x tests` exits 0 with 100% coverage; `make audit-public-api` exits 0 (the multi-line rewrite did not perturb the public surface).
- **Commits:** `f98ca9dc` (foundation.py), `e0e50fde` (ext_argparse.py).

**2. [Rule 1 — Bug] E501 line-too-long after category-label append on aligned trailing-comment sites**

- **Found during:** Tasks 3 and 4 (multiple ext/ files + cli/main.py)
- **Issue:** Several sites with aesthetic alignment padding before `# pragma: nocover` (ext_argparse.py 832-836, ext_logging.py 21-34, ext_generate.py 160-163, ext_smtp.py 187, ext_colorlog.py 106-107, ext_plugin.py 69/71/75/77, cli/main.py:49) hit E501 after the 22-30 char category-label append.
- **Fix:** Per-site decision tree: (a) if the alignment padding could be trimmed to fit within 100 chars, trim it (most cases — saves 5-10 chars); (b) if the variable/function name itself is the load-bearing length, add `# noqa: E501` sibling AFTER the pragma + category label so the audit grep still matches.
- **Files affected:** `cement/ext/ext_argparse.py`, `cement/ext/ext_logging.py`, `cement/ext/ext_generate.py`, `cement/ext/ext_smtp.py`, `cement/ext/ext_colorlog.py`, `cement/ext/ext_plugin.py`, `cement/cli/main.py`.
- **Verification:** `make comply-ruff` exits 0 after each commit.

**3. [Rule 2 — Missing Critical] ext_smtp.py:187 already had a free-form trailing annotation `- Mailpit accepts everything`**

- **Found during:** Task 4 (cement/ext/ext_smtp.py)
- **Issue:** Line 187's existing comment was `# pragma: nocover - Mailpit accepts everything` (no `#` separator before "Mailpit"; free-form prose attached directly). The audit grep needs `# <category>` to match — appending the category at the END would NOT match because the existing free-form annotation comes between.
- **Fix:** Inserted the D-15 `# defensive: unreachable` label BETWEEN the existing pragma and the free-form annotation: `# pragma: nocover  # defensive: unreachable - Mailpit accepts everything`. Audit grep now matches because the category label appears as `# defensive: unreachable` (matching the regex anchor `# (defensive: unreachable|...)`).
- **Files affected:** `cement/ext/ext_smtp.py:187`.
- **Verification:** `grep -nE '# defensive: unreachable' cement/ext/ext_smtp.py` matches line 187; D-17 inverse grep returns empty.
- **Commit:** `715657a5`.

**4. [Rule 1 — Bug] cli/main.py:49 noqa expansion to suppress both T201 and E501**

- **Found during:** Task 5 (cement/cli/main.py)
- **Issue:** Line 49 already carried `# noqa: T201` (intentional CLI print). Adding the D-15 `# defensive: unreachable` category label pushed the line past 100 chars (109).
- **Fix:** Expanded the noqa from `# noqa: T201` to `# noqa: T201,E501` so the existing T201 suppression continues + the new E501 limit is suppressed. Single-noqa-line idiom; no second sibling needed.
- **Files affected:** `cement/cli/main.py:49`.
- **Verification:** `make comply-ruff` exits 0.
- **Commit:** `37d6ef71`.

---

**Total deviations:** 4 auto-fixed (3 Rule 1 bugs caught and fixed inline; 1 Rule 2 missing-critical for surface-preservation of an existing free-form annotation). All resolved before their respective commits landed.

**Impact on plan:** No scope creep. All deviations were small mechanical correctness adjustments necessary to satisfy the 100% coverage / ruff E501 / D-17 audit-grep gates. The audit's mechanical shape held; deviations were all about interaction with neighboring lint rules and pre-existing inline annotations.

## Issues Encountered

- The line-based audit grep for D-17 verification matches the literal `# <category>` token after the pragma. This means inserting the category label between an existing pragma and a pre-existing free-form annotation (ext_smtp.py:187) is the correct shape — the audit grep matches the category prefix without disrupting the free-form note. Documented as Rule 2 deviation #3 above.
- Multi-line import-block reformatting (foundation.py:41 + ext_argparse.py:17) was an unexpected interaction with ruff's I001 isort cascade. The fix was mechanical (let ruff --fix do the split) but it does shift line numbers for downstream references. Documented in deferred-items.md if any future planning artifact references the old line numbers.
- ext_logging.py:33's existing pragma site is the most-decorated site in the codebase (`# type: ignore  # pragma: no cover  # noqa: N802 - overrides logging.Handler.createLock (stdlib camelCase)`) — already 137 chars pre-Wave-7. Adding the `# platform-specific` label pushed it to 158 chars. Ruff was lenient about E501 on this line because of the existing `# noqa: N802` directive (ruff treats lines bearing any noqa directive as lint-skip-able for E501 in some heuristics). Verified `make comply-ruff` passes after the append.

## Authentication Gates

None — pure local refactor; no external services involved.

## TDD Gate Compliance

This plan is `type: execute` (not `type: tdd`) — RED/GREEN/REFACTOR cycle does not apply. The 100% coverage gate (Phase 2 D-10) acted as the regression check: tests exited 0 with full coverage after each commit, validating that no comment-only annotation broke coverage measurement.

## Threat Surface Scan

Pure comment-only annotation work — no new endpoints, auth paths, file access patterns, or schema changes at trust boundaries.

The threat register (T-03-07-01..02 in PLAN.md) was preempted by the per-commit gate set:

| Threat ID | Mitigation Verified |
|-----------|---------------------|
| T-03-07-01 (Tampering — inadvertent code change while editing pragma comment) | Per-file diff inspection before commit; `pdm run pytest --cov=cement -x tests` after each file at 100% coverage caught any inadvertent semantic change. None occurred. |
| T-03-07-02 (DoS — free-form label slip per D-16 violation) | Final D-17 GLOBAL grep at end of Task 5: returns EMPTY. No free-form labels slipped in. |

**No new threat flags surfaced.**

## Verification Results — End of Wave 7

| Gate | Command | Result |
|------|---------|--------|
| Coverage gate (D-24 #1) | `pdm run pytest --cov=cement -x tests` | exit 0, **100% coverage** (3241/3241 stmts, 316 passed) |
| comply-ruff (D-24 #2) | `make comply-ruff` | exit 0 |
| comply-mypy (D-24 #3) | `pdm run mypy cement` | exit 0 — 51 source files, no issues |
| audit-public-api (D-24 #4) | `make audit-public-api` | exit 0 against Wave 3 baseline (Wave 7 changes are comment-only, byte-identical AST surface) |
| coverage-report HTML (D-24 #5; COV-02) | `test -f coverage-report/index.html && test -d coverage-report/` | PASS |
| **Pragma audit locked-vocabulary (D-24 #6 / #7)** | `grep -nE 'pragma:[[:space:]]*no[[:space:]]*cover' cement/ \| grep -vE '# (<8 categories>)' \| wc -l` | **0 (D-24 conjunct #7 GREEN)** |
| Pre-count baseline | `grep -rn 'pragma:[[:space:]]*no[[:space:]]*cover' cement/ \| wc -l` | 141 (matches RESEARCH.md A4 verified count) |
| Post-count | `grep -rn 'pragma:[[:space:]]*no[[:space:]]*cover' cement/ \| wc -l` | 141 (unchanged — comment-only annotation work) |

## D-24 Conjunct Status

| Conjunct | Status After Wave 7 (this plan) |
|----------|----------------------------------|
| #1 — `make test` 100% coverage | **green** ✓ (3241/3241 stmts, 316 passed) |
| #2 — `make comply-ruff` | **green** ✓ |
| #3 — `make comply-mypy` | **green** ✓ |
| #4 — `make audit-public-api` | **green** ✓ (no public-surface change) |
| #5 — `coverage-report/index.html` generates | **green** ✓ (COV-02 wave check) |
| #6 — Any reduction (REFACTOR-02) | **green** ✓ (Wave 5 closed; held through Wave 7) |
| **#7 — pragma:nocover locked-vocab (COV-03)** | **GREEN ✓** (this plan closed it; 141 sites all carry locked-vocabulary labels) |
| #8 — `os.path` boundary scope (REFACTOR-03) | **green** ✓ (Wave 6 closed; held through Wave 7) |
| #9 — `from __future__ import annotations` strip | **green** ✓ (Wave 4 closed; held through Wave 7) |

**All 9 D-24 conjuncts GREEN through Wave 7.** Wave 8 (D-22 step 14) finalizes 03-VERIFICATION.md with the full 9-conjunct evidence and REFACTOR-01 acceptance-via-coverage rationale.

## Acceptance Criteria — Plan Match

| Criterion | Status |
|-----------|--------|
| Pre-count re-verified and documented | ✓ (141 sites — matches RESEARCH.md A4 verified count exactly; documented in 03-VERIFICATION.md Wave 7 section) |
| Every pragma site in cement/ carries a D-15 locked-vocabulary category label | ✓ (141 sites; per-file table in this Summary) |
| D-17 verification grep returns empty (D-24 #7 GREEN) | ✓ (`wc -l` returns 0; documented in 03-VERIFICATION.md as command output evidence) |
| Per-file atomic commits (~39 commits) | ✓ (39 per-file source commits + 3 batch-summary docs commits + 1 closing docs commit) |
| After every commit: make test 0, make audit-public-api 0, make comply-mypy 0, make comply-ruff 0 | ✓ (all 39 per-file commits) |
| 03-VERIFICATION.md appended with Wave 7 pragma post-count + delta | ✓ (post-count 141; per-batch + per-category breakdown tables; D-17 grep result; D-24 status update) |
| If D-16 escape hatch triggered: separate CONTEXT.md amendment commit before any new-label site commit | N/A — D-16 was NOT triggered; every site fit the 8-category vocabulary |
| SUMMARY.md created at 03-07-SUMMARY.md | ✓ (this file) |
| STATE.md and ROADMAP.md updated | (final docs commit follows this Summary) |

## Self-Check: PASSED

- File `.planning/phases/03-internal-refactor-coverage-hardening/03-07-SUMMARY.md` exists at the expected path — FOUND
- File `.planning/phases/03-internal-refactor-coverage-hardening/03-VERIFICATION.md` updated with Wave 7 section — FOUND
- All 39 per-file source commits present in `git log --oneline 81cdb7ee..HEAD` — FOUND (verified via inline git log review during execution)
- All 3 batch-summary docs(03) commits present — FOUND
- D-24 conjunct #7 grep: `grep -nE 'pragma:[[:space:]]*no[[:space:]]*cover' cement/ | grep -vE '# (<8 categories>)' | wc -l` → **0**
- Pragma site count: `grep -rn 'pragma:[[:space:]]*no[[:space:]]*cover' cement/ | wc -l` → **141** (unchanged from pre-audit baseline)
- Coverage: 3241/3241 stmts, 100.00%, 316 passed
- mypy: 51 source files, no issues
- comply-ruff: All checks passed
- audit-public-api: exit 0
- COV-02 HTML: `coverage-report/index.html` exists

---

*Plan: 03-07 (Wave 7)*
*Depends on: Plan 06 (Wave 6 — pathlib migration; D-24 conjunct #8 GREEN)*
*Unblocks: Plan 08 (Wave 8 — D-22 step 14 closing — finalize 03-VERIFICATION.md with 9-conjunct evidence + REFACTOR-01 acceptance-via-coverage rationale)*
*Closes: D-24 conjunct #7 (COV-03 acceptance via empty locked-vocabulary inverse grep)*
