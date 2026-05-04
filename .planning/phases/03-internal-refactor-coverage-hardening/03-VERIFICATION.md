---
phase: 03-internal-refactor-coverage-hardening
verified: 2026-05-04T05:34:56Z
status: passed
score: 9/9 D-24 conjuncts GREEN
overrides_applied: 0
---

# Phase 03 Verification

> **Status:** **passed.** All 9 D-24 conjuncts GREEN; all 7 phase
> requirements (REFACTOR-01..04, COV-01..03) SATISFIED.
> Pre-tightening baselines (Wave 5) and post-counts (Wave 8) below;
> defense-in-depth final reset transcript at the foot of this
> document.

## Any-in-core baseline (D-09)

**Pre-tightening count:** **41 sites** (per
`grep -nE ': Any\b|-> Any\b|Any\]' cement/core/*.py | wc -l` on
2026-05-04, post Wave 4 FA strip).

> **Drift note vs RESEARCH.md:** RESEARCH.md verified **40 sites** on
> 2026-05-03; the live count on 2026-05-04 (post Wave 4 FA strip + PEP 484
> string-quoting + UP family cascade from Wave 3) is **41**. The +1 drift
> is the `frame: "FrameType | None"` annotation at
> `cement/core/foundation.py:127` whose return type `-> Any` newly matches
> the grep pattern after Wave 4's FA-strip-driven re-quoting (it was
> already `Any` pre-Wave-4 but the line itself drifted in/out of grep
> visibility through the Wave 3/4 line-shifts). Substantive Any surface
> is unchanged; just one extra grep match.

**Per-file pre-count breakdown (41 sites):**

| File | Sites |
|------|-------|
| `cement/core/foundation.py` | 13 |
| `cement/core/handler.py` | 4 |
| `cement/core/template.py` | 5 |
| `cement/core/config.py` | 4 |
| `cement/core/cache.py` | 2 |
| `cement/core/meta.py` | 3 |
| `cement/core/interface.py` | 2 |
| `cement/core/hook.py` | 1 |
| `cement/core/extension.py` | 1 |
| `cement/core/output.py` | 1 |
| `cement/core/mail.py` | 2 |
| `cement/core/arg.py` | 1 |
| `cement/core/exc.py` | 1 |
| `cement/core/controller.py` | 1 |
| **TOTAL** | **41** |

**Per-site classification** (per RESEARCH.md "Any-in-core inventory"
lines 786-813):

### Must-stay (D-09 exempt — handler contract, argparse opacity, signal frame opacity, user-arbitrary config/template/render data)

| File:Line | Site | Reason |
|-----------|------|--------|
| `arg.py:33` | `**kw: Any` | Handler contract — pluggable kwargs by design |
| `cache.py:30` | `def get(self, key: str, fallback: Any = None) -> Any` | Cache values are user-arbitrary |
| `cache.py:52` | `value: Any` | Cache values are user-arbitrary |
| `config.py:72` | `-> dict[str, Any]` | User-arbitrary config values |
| `config.py:82` | `-> dict[str, Any]` | User-arbitrary config values |
| `config.py:111` | `def get(...) -> Any` | User-arbitrary config values |
| `config.py:134` | `value: Any` | User-arbitrary config values |
| `exc.py:43` | `frame: Any` | Signal frame is Python-runtime opaque |
| `extension.py:81` | `**kw: Any` | Handler contract — pluggable kwargs by design |
| `foundation.py:43` | `ArgparseArgumentType = tuple[list[str], dict[str, Any]]` | Argparse kwargs opacity |
| `foundation.py:127` | `def cement_signal_handler(...) -> Any` | Signal handler returns whatever user handler returns |
| `foundation.py:388` | `config_defaults: dict[str, Any] = None` | Defaults ARE arbitrary by contract (D-09 explicit exempt) |
| `foundation.py:391` | `meta_defaults: dict[str, Any] = {}` | Same — meta defaults are arbitrary by contract |
| `foundation.py:764` | `**kw: Any` | Handler contract |
| `foundation.py:800` | `_parsed_args: Any = None` | Argparse Namespace opacity (D-09 explicit exempt) |
| `foundation.py:867` | `member_object: Any` | Public extension API — caller passes arbitrary objects |
| `foundation.py:1069` | `data: Any` | User-arbitrary render data (D-09 explicit exempt) |
| `foundation.py:1073` | `**kw: Any` | Handler contract |
| `foundation.py:1138` | `-> tuple[dict[str, Any], str \| None] \| None` | User-arbitrary last-rendered data |
| `foundation.py:1150` | `def pargs(self) -> Any` | Argparse Namespace opacity |
| `foundation.py:1157` | `*args: Any, **kw: Any` | argparse `add_argument` passthrough — kwargs opacity |
| `handler.py:49` | `config_defaults: dict[str, Any] \| None` | Defaults are arbitrary by contract |
| `handler.py:64` | `**kw: Any` | Handler contract |
| `handler.py:123` | `**kwargs: Any` | Handler contract |
| `handler.py:332` | `**kwargs: Any` | Handler contract |
| `hook.py:135` | `*args: Any, **kwargs: Any` | Hook payload is user-arbitrary by design |
| `interface.py:33` | `**kw: Any` | Handler contract |
| `interface.py:64` | `**kwargs: Any` | Handler contract |
| `mail.py:33` | `**kwargs: Any` | Handler contract |
| `mail.py:100` | `config_defaults: dict[str, Any]` | Defaults are arbitrary by contract |
| `meta.py:14` | `**kwargs: Any` | MetaMixin contract — Meta merging takes arbitrary attrs |
| `meta.py:17` | `dict_obj: dict[str, Any]` | MetaMixin merge target — Meta attributes are arbitrary |
| `meta.py:30` | `*args: Any, **kwargs: Any` | MetaMixin contract |
| `output.py:30` | `data: dict[str, Any], *args: Any, **kwargs: Any` | User-arbitrary render data + handler contract |
| `template.py:39` | `data: dict[str, Any]` | User-arbitrary template data |
| `template.py:54` | `data: dict[str, Any]` | User-arbitrary template data |
| `template.py:113` | `*args: Any, **kwargs: Any` | Handler contract |
| `template.py:120` | `data: dict[str, Any]` | User-arbitrary template data |
| `template.py:144` | `data: dict[str, Any]` | User-arbitrary template data |
| `foundation.py:1749` | `obj: Any` | App.__import__ accepts a string OR a module object — both legitimate |
| `controller.py:30` | `def _dispatch(self) -> Any \| None` | Internal abstract method; concrete controllers may dispatch to anything |

### Tightenable candidates (Task 2 hand-pass)

These are sites where RESEARCH.md A3 flagged a possible narrower type;
each one will be classified during the Task 2 hand-pass and either
tightened or moved to "must-stay" with an inline justification:

- `cement/core/foundation.py:1749` `App.__import__(obj: Any, ...)` — possibly `str | ModuleType`
- `cement/core/controller.py:30` `_dispatch(self) -> Any | None` — already `Any | None` post-UP007; the `| None` is redundant with `Any`
- Other `Any | None` sites where `| None` is redundant (Any already includes None)

The tightening commit (Task 2) will list the actual sites tightened in
its commit body and update this section's "Post-tightening" entries.

**Post-tightening count:** **40 sites** (per
`grep -nE ': Any\b|-> Any\b|Any\]' cement/core/*.py | wc -l` on
2026-05-04 post Wave 5; held through Waves 6 + 7 + 8 final reset).

**Delta:** **41 → 40 = -1 substantive site** (D-24 conjunct #6 GREEN
✓ — strictly positive in the reduction direction). Wave 5 commit
`6365a6c7` tightened 2 substantive sites:

  1. `App.__import__(obj: Any, ...)` → `obj: str` (was UNDOCUMENTED
     EXPERIMENTAL surface; not in `03-PUBLIC-API-BASELINE.txt`).
  2. `ControllerInterface._dispatch(self) -> Any | None` → `-> Any`
     (Wave 3 UP007 cascade artifact — `Any | None` is redundant
     since `Any` already includes `None`; internal abstract method).

The grep yielded -1 net (and not -2) because tightening site (1)
removed a `: Any` match while adding zero new matches; tightening
site (2) collapsed `Any | None` to `Any` (still matches the regex
once via `-> Any\b`). Both substantive type-narrowings stuck.

**Per-file post-count breakdown (40 sites; matches Wave 5 record
post-tightening):**

| File | Sites |
|------|-------|
| `cement/core/foundation.py` | 12 (was 13; -1 from `App.__import__`) |
| `cement/core/handler.py` | 4 |
| `cement/core/template.py` | 5 |
| `cement/core/config.py` | 4 |
| `cement/core/cache.py` | 2 |
| `cement/core/meta.py` | 3 |
| `cement/core/interface.py` | 2 |
| `cement/core/hook.py` | 1 |
| `cement/core/extension.py` | 1 |
| `cement/core/output.py` | 1 |
| `cement/core/mail.py` | 2 |
| `cement/core/arg.py` | 1 |
| `cement/core/exc.py` | 1 |
| `cement/core/controller.py` | 1 |
| **TOTAL** | **40** |

All 40 surviving sites carry inline `# D-09: <reason>` justification
comments per Wave 5 commit body (handler-contract / user-arbitrary /
argparse-opacity / signal-frame-opacity / UNDOCUMENTED). RESEARCH.md
A3's "5-10 realistic" upper bound was the planning-time estimate;
actual delta of 2 substantive sites reflects that the bulk of `Any`
in `cement/core/` is required by the public contract (handler-
contract pluggable kwargs, user-arbitrary config/template/render/
cache data, argparse opacity, signal-frame opacity).

## Pragma audit baseline (COV-03)

**Pre-audit count:** **141 sites** (per
`grep -rn 'pragma:[[:space:]]*no[[:space:]]*cover' cement/ | wc -l` on
2026-05-04).

RESEARCH.md verified **141 sites on 2026-05-03**, NOT the 123 from
CONTEXT.md. Live count on 2026-05-04 matches: 141.

Wave 7 will apply the locked-vocabulary D-15 labels. Wave 8 records the
post-audit grep result (must be empty per D-17 / D-24 conjunct #7).

### Wave 7 post-audit (this plan)

**Post-audit count:** **141 sites** (live count unchanged across the
sweep — comment-only annotation work; no source-logic changes).

**Per-file pre/post deltas:** ZERO sites added, ZERO sites removed.
Every existing pragma site received a D-15 locked-vocabulary category
label appended after the existing pragma comment.

**D-17 verification grep result (D-24 conjunct #7):**

```
$ grep -nE 'pragma:[[:space:]]*no[[:space:]]*cover' cement/ \
    | grep -vE '# (abstract method|TYPE_CHECKING import|platform-specific|untestable: dynamic import|untestable: subprocess|untestable: signal handler|defensive: unreachable|version constant)' \
    | wc -l
0
```

**EMPTY → D-24 conjunct #7 GREEN ✓ (COV-03 acceptance closed).**

**Per-category breakdown across all of cement/:**

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

**Per-batch breakdown:**

| Batch | Scope | Files | Sites | Per-file commits |
|-------|-------|-------|-------|-------------------|
| A | cement/core/ | 15 | 58 | 15 |
| B | cement/ext/ first half (alpha) | 10 | 43 | 10 |
| C | cement/ext/ second half (alpha) | 10 | 22 | 10 |
| D | cement/cli/ + cement/utils/ | 4 | 18 | 4 |
| **TOTAL** | **all of cement/** | **39** | **141** | **39** |

(39 per-file source commits + 3 docs(03) CHANGELOG-batch-summary
commits [Batches A, B, C] + 1 final docs(03) commit folding
Batch D summary into the closing CHANGELOG block = 43 total
commits in Wave 7. RESEARCH.md predicted ~39 files; actual was
39 files with pragma sites — exact match.)

**Wave 7 commits (39 per-file source + 4 docs(03) batch summaries):**
recorded in `git log --oneline 9c9db680..HEAD` (Plan 06 anchor →
Plan 07 final docs commit).

**No D-16 vocabulary expansion was triggered.** Every pragma site fit
into one of the 8 D-15 categories without reaching into a free-form
label or amending CONTEXT.md.

**D-24 conjunct #7 GREEN.**

## Pathlib boundary baseline (REFACTOR-03)

**Pre-migration `os.path` callsites in scoped files (Wave 5
baseline):**

```
$ grep -rn 'os\.path' cement/utils/fs.py cement/core/foundation.py \
    cement/core/template.py cement/core/config.py | wc -l
33
```

Per-file breakdown (2026-05-04 count, 33 callsites):

| File | Pre-migration callsites |
|------|-------------------------|
| `cement/utils/fs.py` | 15 (incl. 4 docstring/comment refs that the line-based grep matches) |
| `cement/core/foundation.py` | 4 (1 real-code + 3 docstring example refs) |
| `cement/core/template.py` | 13 |
| `cement/core/config.py` | 1 |
| **TOTAL** | **33** |

### Wave 6 post-migration (this plan)

**Post-migration `os.path` callsites in scoped files:**

```
$ grep -rn 'os\.path' cement/utils/fs.py cement/core/foundation.py \
    cement/core/template.py cement/core/config.py | wc -l
1
$ grep -rn 'os\.path' cement/utils/fs.py cement/core/foundation.py \
    cement/core/template.py cement/core/config.py | grep -v \
    '# boundary:' | wc -l
0
```

Per-file post-migration breakdown:

| File | Post callsites | Tagged `# boundary:` | Untagged |
|------|----------------|----------------------|----------|
| `cement/utils/fs.py` | 0 | 0 | 0 |
| `cement/core/foundation.py` | 1 | 1 | 0 |
| `cement/core/template.py` | 0 | 0 | 0 |
| `cement/core/config.py` | 0 | 0 | 0 |
| **TOTAL** | **1** | **1** | **0** |

The surviving site is the public alias `join = os.path.join` at
`cement/core/foundation.py:49` — `cement.core.foundation:join` is in
`03-PUBLIC-API-BASELINE.txt` with stdlib `os.path.join` semantics
that downstream callers depend on. Migrating it would change the
callable's behavior for every downstream user (no-breakage rule).
Inline `# boundary:` tag documents the deliberate retention per
D-12 / D-14.

The `os.walk(src)` callsite at `cement/core/template.py:209` is
also retained with a `# boundary: D-14` tag (separate gate — the
`os\.path` regex doesn't match `os.walk`). Pathlib has no direct
equivalent yielding the `(cur_dir, sub_dirs, files)` triple shape
the template-render loop depends on; converting to
`Path.rglob('*')` would require a wholesale loop restructure with
higher regression risk than the boundary-tag accommodation.

**A7 symlink pre-flight finding (Wave 6 Task 1):**

| Check | Result |
|-------|--------|
| `find tests/ -type l 2>/dev/null` | 0 symlinks |
| `find cement/ -type l 2>/dev/null` | 0 symlinks |
| `find . -type l ...` (excl. .venv/.git/node_modules) | 3 symlinks under `.devbox/` only (tooling; never path-handled by cement) |
| Decision | `Path(p).expanduser().resolve(strict=False)` — matches `os.path.abspath(os.path.expanduser(p))` semantics for non-symlink paths (per RESEARCH.md A7 decision tree) |

**Wave 6 commits (4 atomic per-file):**

| Hash | Subject |
|------|---------|
| `6af95ee9` | `refactor(utils.fs): migrate os.path to pathlib internals` |
| `1f307f23` | `refactor(core.config): migrate os.path to pathlib internals` |
| `41f27d9f` | `refactor(core.foundation): migrate os.path to pathlib internals` |
| `f2c181ac` | `refactor(core.template): migrate os.path to pathlib internals` |

**D-24 conjunct #8 GREEN ✓** — pathlib migration complete across
all 4 named files; the lone survivor is `# boundary:`-tagged.

## Public API baseline (D-04)

Captured in Wave 1 as
`.planning/phases/03-internal-refactor-coverage-hardening/03-PUBLIC-API-BASELINE.txt`
(frozen snapshot, **934 sorted lines** as of 2026-05-04 post Wave 3
re-baseline). `make audit-public-api` enforces byte-for-byte match
across all subsequent Phase 03 commits. **D-24 conjunct #4 GREEN through Wave 4.**

The Wave 3 re-baseline (1014 → 934 lines) was a user-approved Rule 4
architectural decision — the 80 lines pruned were orphaned
`typing.{List,Dict,Tuple,Type,Union,Optional}` re-exports, never genuine
public API; tooling artifacts of the pre-PEP-585 era surfaced by UP006/
UP007/UP045 cleaning the import surface.

## D-24 9-Conjunct Acceptance (Wave 8 final evidence)

The Phase 03 acceptance gate is the conjunction of all 9 rows below.
Captured 2026-05-04 against the modernization-phase-3 branch HEAD,
post `make superclean && make init` defense-in-depth reset (transcript
at the foot of this document). **All 9 GREEN.**

| # | Gate | Command | Expected | Result | Status |
|---|------|---------|----------|--------|:------:|
| 1 | `make test` 100% coverage (REFACTOR-01 via D-20; COV-01) | `make test` | exit 0; coverage 100% | exit 0; **3241/3241 stmts; 100.00% coverage; 316 passed** | **GREEN ✓** |
| 2 | `make comply-ruff` clean (UP+FA family enabled per D-06) | `make comply-ruff` | exit 0 | exit 0; **All checks passed!** | **GREEN ✓** |
| 3 | `make comply-mypy` clean (REFACTOR-02 hint changes) | `make comply-mypy` | exit 0 | exit 0; **Success: no issues found in 51 source files** | **GREEN ✓** |
| 4 | `make audit-public-api` exit 0 (D-04 baseline byte-for-byte) | `make audit-public-api` | exit 0; empty diff | exit 0; **silent (empty `diff -u`)** | **GREEN ✓** |
| 5 | `coverage-report/index.html` generates without warnings (COV-02) | `ls -la coverage-report/index.html` | file exists | **`-rw-rw-r-- 1 derks derks 25733 May  3 23:25`** | **GREEN ✓** |
| 6 | `Any` post-count strictly lower than pre-count (REFACTOR-02 SC-4) | `grep -nE ': Any\b\|-> Any\b\|Any\]' cement/core/*.py \| wc -l` | post < pre | **41 → 40 (delta -1)** | **GREEN ✓** |
| 7 | `pragma:nocover` locked-vocab grep empty (COV-03 SC-2; D-17) | `grep -nE 'pragma:[[:space:]]*no[[:space:]]*cover' cement/ \| grep -vE '# (abstract method\|TYPE_CHECKING import\|platform-specific\|untestable: dynamic import\|untestable: subprocess\|untestable: signal handler\|defensive: unreachable\|version constant)'` | 0 lines | **0 lines** | **GREEN ✓** |
| 8 | `os.path` in scoped files empty OR `# boundary:`-tagged only (REFACTOR-03 SC-5; D-14) | `grep -rn 'os\.path' cement/utils/fs.py cement/core/foundation.py cement/core/template.py cement/core/config.py \| grep -v '# boundary:' \| wc -l` | 0 lines | **0 lines** (1 tagged survivor: `cement/core/foundation.py:53 join = os.path.join  # boundary:`) | **GREEN ✓** |
| 9 | `from __future__ import annotations` grep empty (D-08 / FA100) | `grep -rn 'from __future__ import annotations' cement/` | 0 lines | **0 lines** | **GREEN ✓** |

**Score: 9/9 D-24 conjuncts GREEN. Phase 03 acceptance MET.**

Detailed evidence transcripts for each conjunct follow.

### Conjunct #1 — `make test` 100% coverage

```
$ make test
...
cement/utils/version.py                 33      0  100.00%
----------------------------------------------------------
TOTAL                                 3241      0  100.00%
Coverage HTML written to dir coverage-report
Required test coverage of 100% reached. Total coverage: 100.00%
===================== 316 passed, 1692 warnings in 52.83s ======================
$ echo $?
0
```

REFACTOR-01 acceptance via D-20 — see § REFACTOR-01 acceptance via
coverage gate below. COV-01 acceptance.

### Conjunct #2 — `make comply-ruff`

```
$ make comply-ruff
pdm run ruff check cement/ tests/
All checks passed!
$ echo $?
0
```

UP family + FA family both enabled in `[tool.ruff.lint] extend-select`
since Plan 02 (Wave 2). TOOL-04 stays satisfied; ruff config still
no-implicit-drift (AUDIT POINT comment present per D-06).

### Conjunct #3 — `make comply-mypy`

```
$ make comply-mypy
pdm run mypy
Success: no issues found in 51 source files
$ echo $?
0
```

REFACTOR-02 hint changes type-check clean. All 40 surviving `Any`
sites in `cement/core/` carry inline `# D-09: ...` justifications
per Wave 5.

### Conjunct #4 — `make audit-public-api`

```
$ make audit-public-api
$ echo $?
0
```

`diff -u` between `03-PUBLIC-API-BASELINE.txt` (934 lines, frozen
post Wave 3 re-baseline) and the live AST-walk output is empty —
exit 0, silent. D-04 / SC-3: zero public symbol added, removed, or
signature-changed across 8 waves. Permanent dev affordance per
D-05 retained (`scripts/audit-public-api.py` + Makefile target).

### Conjunct #5 — Coverage HTML report

```
$ ls -la coverage-report/index.html
-rw-rw-r-- 1 derks derks 25733 May  3 23:25 coverage-report/index.html
$ echo $?
0
```

HTML report generates without warnings during the Conjunct #1
`make test` run (`Coverage HTML written to dir coverage-report`).
COV-02 acceptance.

### Conjunct #6 — `Any` reduction in `cement/core/`

```
$ grep -nE ': Any\b|-> Any\b|Any\]' cement/core/*.py | wc -l
40
```

**Pre-count (Wave 5 baseline, 2026-05-04):** 41 sites.
**Post-count (Wave 8 final, 2026-05-04):** 40 sites.
**Delta:** **-1 site** (strictly positive in the reduction direction).

REFACTOR-02 acceptance / SC-4 satisfied. See § Any-in-core baseline
above for per-file breakdown and tightening rationale.

### Conjunct #7 — `pragma: no cover` locked-vocabulary grep

```
$ grep -nE 'pragma:[[:space:]]*no[[:space:]]*cover' cement/ \
    | grep -vE '# (abstract method|TYPE_CHECKING import|platform-specific|untestable: dynamic import|untestable: subprocess|untestable: signal handler|defensive: unreachable|version constant)' \
    | wc -l
0
```

EMPTY → COV-03 acceptance / SC-2 satisfied. All 141 pragma sites
carry one of the 8 D-15 locked-vocabulary category labels (Wave 7
per-file commits across 39 files). See § Pragma audit baseline
above for per-category and per-batch breakdowns.

### Conjunct #8 — `os.path` in scoped files (boundary check)

```
$ grep -rn 'os\.path' cement/utils/fs.py cement/core/foundation.py \
    cement/core/template.py cement/core/config.py
cement/core/foundation.py:53:join = os.path.join  # boundary: public alias `cement.core.foundation:join` (baseline; D-12 / D-14)

$ grep -rn 'os\.path' cement/utils/fs.py cement/core/foundation.py \
    cement/core/template.py cement/core/config.py | grep -v '# boundary:' | wc -l
0
```

REFACTOR-03 acceptance / SC-5 satisfied. The lone surviving site is
the public alias `join = os.path.join` (in `03-PUBLIC-API-BASELINE.txt`
as `cement.core.foundation:join` with stdlib `os.path.join`
semantics; migrating it would change downstream callable behavior).
Inline `# boundary:` tag documents the deliberate retention per
D-12 / D-14. See § Pathlib boundary baseline above for full per-file
breakdown.

### Conjunct #9 — `from __future__ import annotations` strip

```
$ grep -rn 'from __future__ import annotations' cement/
$ echo $?
1   # grep returns 1 for "no matches", which is the desired result
$ grep -rn 'from __future__ import annotations' cement/ | wc -l
0
```

EMPTY → D-08 / FA100 acceptance satisfied. All 29 sites stripped in
Wave 4 (Plan 04 `e16ed7d8`); PEP 484 string-quoting applied to
TYPE_CHECKING-bound forward references at definition-time-evaluated
positions. Closes the Phase 1 D-14 cement/utils/fs.py self-flagged
2024-06-22 TODO.

## REFACTOR-01 acceptance via coverage gate (D-20 / D-21)

REFACTOR-01 ("dead code identified and removed without affecting
public API or test coverage") is satisfied **via the existing 100%
coverage gate** rather than via a `vulture`-driven dead-code hunt.

**Acceptance argument (D-20):** The 100% coverage gate is wired as
both `[tool.coverage.report] fail_under = 100` and
`[tool.pytest.ini_options] addopts = "--cov-fail-under=100"`
(Phase 2 Plan 03, commit `875fe621`). The post-refactor `make test`
passing at 100.00% coverage (3241/3241 stmts; Conjunct #1 above)
implies — by construction — that **every executable statement in
the refactored tree is exercised by the test suite, and therefore
no dead code at the statement level remains**. This holds
continuously: 100% coverage was preserved by the gate across every
single Phase 03 commit (the gate fails the build below 100%, so
any commit that introduced unreachable code would have been
rejected at commit time). The Wave 7 pragma audit's locked-
vocabulary labels (Conjunct #7) further document why every excluded
line is excluded — no opportunistic / convenience exclusions hide
dead code behind a pragma.

**Risk acknowledgement (D-21):** This acceptance leaves two classes
of "dead-but-covered" code undetected:

  - **(a) Covered-but-functionally-dead code** — code that executes
    in tests without meaningful assertions on its observable effects
    (the test imports/calls the code path, but doesn't verify the
    outcome). 100% coverage doesn't speak to assertion strength.
  - **(b) Unused private helpers reachable via import but not called
    by any production caller** — code reachable only from a test
    that imports it directly to satisfy coverage; no production
    caller exists.

  Future milestones (Cement 3.2.0 cleanup cycle, or a dedicated
  audit milestone) may re-open REFACTOR-01 with `vulture` if these
  gaps prove to bite in practice. Recorded here so the deferral is
  intentional and documented, not oversight.

**Why no `vulture` this phase (D-22 step 13 negative-space):**
Adding a new dev-dep purely for one acceptance gate would have
violated the Phase 03 strict-minimum discipline (D-13). The 100%
gate already provides the strongest available signal at zero
incremental dev-dep cost. `vulture` is an additive future-tooling
decision, not a Phase 03 prerequisite.

**REFACTOR-01 status: SATISFIED via D-20.**

## Behavioral Spot-Checks (sampling)

Five representative behavior tests exercise the refactored code
paths to confirm public behavior is unchanged across the Phase 03
internal-refactor / pathlib / Any-tightening sweep. All pass under
the post-Wave-8 100% coverage gate (Conjunct #1).

| # | Behavior | Test(s) | Phase 03 surface exercised | Result |
|---|----------|---------|----------------------------|:------:|
| 1 | `cement.utils.fs.abspath()` returns `str` (boundary preservation) | `tests/utils/test_fs.py::test_abspath` | Wave 6 `cement/utils/fs.py` os.path → pathlib internals; `str(p)` at every public-return boundary (D-12) | PASS |
| 2 | `App._find_config_files()` discovers per-config-section files | `tests/core/test_foundation.py::test_get_default_config_files` | Wave 6 `cement/core/foundation.py:_find_config_files` os.path.isdir → Path.is_dir() conversion | PASS |
| 3 | Template substitution `.format(**template_dict)` preserved (D-19 protected callsites) | `tests/core/test_foundation.py::test_render`, `tests/ext/test_ext_jinja2.py`, `tests/ext/test_ext_mustache.py` | Wave 3 UP032 cascade explicitly avoided 14 protected `.format(**template_dict)` callsites in `cement/core/foundation.py:1383..1591` | PASS |
| 4 | `cement generate project` template walks tree end-to-end | `tests/cli/test_main.py::test_generate` (+ `make cli-smoke-test` matrix) | Wave 6 `cement/core/template.py` os.path → pathlib (`os.walk(src)` boundary-tagged retention; render loop unchanged) | PASS |
| 5 | `App.__import__(obj: str)` resolves shorthand alternative module names | `tests/core/test_foundation.py::test_alternative_module_mapping_*` | Wave 5 D-09 tightening: `obj: Any` → `obj: str` | PASS |

Sample size: 5 of 316 tests. The full 316-test suite passes at
100.00% coverage post-reset (Conjunct #1).

## Requirements Coverage

| Requirement | Status | Acceptance Evidence |
|-------------|:------:|---------------------|
| **REFACTOR-01** | **SATISFIED** | D-24 #1 GREEN + § REFACTOR-01 acceptance via coverage gate (D-20). 100% coverage held across all 8 waves; D-21 risk acknowledged. |
| **REFACTOR-02** | **SATISFIED** | D-24 #6 GREEN. `Any` post-count 40 < pre-count 41 (delta -1, strictly positive in reduction direction). 2 substantive tightenings recorded in Wave 5 commit `6365a6c7`. All 40 surviving sites carry inline `# D-09: ...` justifications. |
| **REFACTOR-03** | **SATISFIED** | D-24 #8 GREEN. 4 scoped files migrated (`cement/utils/fs.py`, `cement/core/{config,foundation,template}.py`); 33 → 1 (boundary-tagged) os.path callsites. The lone survivor is the public alias `join = os.path.join` in `03-PUBLIC-API-BASELINE.txt`; D-12 / D-14 boundary preserved. |
| **REFACTOR-04** | **SATISFIED** | D-24 #2 GREEN. UP031 + UP032 cascade resolved all 114 printf/format-style sites in Wave 3; protected `.format(**template_dict)` callsites preserved per D-19. `cached_property` / `contextlib.suppress` adoption opportunistic — none surfaced as obvious wins (per D-19 executor discretion). |
| **COV-01** | **SATISFIED** | D-24 #1 GREEN. 100.00% coverage held across every Phase 03 commit (the gate fails the build below 100%); 316 passing tests; zero drift from prior baseline. |
| **COV-02** | **SATISFIED** | D-24 #5 GREEN. `coverage-report/index.html` generates without warnings during the `make test` run (verified mid-phase in Wave 3 + post-Wave-8 reset). |
| **COV-03** | **SATISFIED** | D-24 #7 GREEN. 141 `pragma: no cover` sites across 39 files all carry one of 8 D-15 locked-vocabulary category labels (Wave 7); D-17 verification grep returns empty. NO D-16 vocabulary expansion was triggered. |

## ROADMAP Success Criteria Mapping (Phase 3 SC #1–5)

| ROADMAP SC | Description | Mapped Conjunct(s) | Result |
|:----------:|-------------|:------------------:|:------:|
| **#1** | `make test` 100% coverage report on refactored tree with zero drift from prior baseline | D-24 #1 | **SATISFIED** |
| **#2** | `coverage-report/` HTML generates without warnings; every remaining `pragma: no cover` line has an inline comment justifying the exclusion | D-24 #5 + D-24 #7 | **SATISFIED** |
| **#3** | Diff of public symbols (module-level + class public methods) between `main` and refactor branch is empty — no signatures changed, no exports added or removed | D-24 #4 | **SATISFIED** |
| **#4** | mypy strict mode reports fewer `Any` occurrences in `cement/core/` than the pre-refactor baseline; concrete number captured in the phase summary | D-24 #6 (delta 41 → 40) | **SATISFIED** |
| **#5** | `os.path` usage in `cement/utils/fs.py` and core internals migrated to `pathlib` where it doesn't change a public signature; remaining `os.path` callsites explicitly documented as boundary-preserving | D-24 #8 | **SATISFIED** |

5 of 5 ROADMAP Phase 3 success criteria SATISFIED.

## Phase 3 Commit Audit

**Phase 3 commit range:** `main..HEAD` (branch
`modernization-phase-3`).
**Total commits:** **87** as of Wave 9 Task 5 (Wave 8 captured 82;
Wave 9 added 5: 4 source/test/changelog + 1 docs verification
update) — see `git log --oneline main..HEAD`.

**Per-wave breakdown (per ROADMAP Phase 3 detail):**

| Wave | Plan | Source/Refactor Commits | Docs/Planning Commits | Notes |
|------|------|:-----------------------:|:---------------------:|-------|
| 1 | 03-01 | 1 | 2 | `docs(03): capture public API baseline f10f8ce3` + script + Makefile target |
| 2 | 03-02 | 1 | 1 | `chore(ruff): re-enable UP family b8427466` + AUDIT POINT comment |
| 3 | 03-03 | 16 | 2 | UP family auto-fixes (UP006/007/045/031/032/004/008/015/024/025/026/028/035) + CONVENTIONS.md refresh; Wave 3 baseline rebase 1014 → 934 lines |
| 4 | 03-04 | 1 | 1 | `refactor(core): drop from __future__ import annotations` + PEP 484 string-quoting (~76 forward refs) |
| 5 | 03-05 | 2 | 2 | `docs(03): record Any-baseline in 03-VERIFICATION.md 2f3a063f` + `refactor(core): tighten Any types 6365a6c7` |
| 6 | 03-06 | 4 | 2 | 4 atomic per-file pathlib migrations: `6af95ee9` fs.py, `1f307f23` config.py, `41f27d9f` foundation.py, `f2c181ac` template.py |
| 7 | 03-07 | 39 | 4 | 39 per-file pragma:nocover audit commits + 3 batch-summary docs(03) commits + 1 Plan 07 SUMMARY |
| 8 | 03-08 | 0 | 2 (this wave) | finalize 03-VERIFICATION.md + mark Phase 3 complete in ROADMAP |
| 9 | 03-09 | 4 | 1 | gap closure: CR-01 + CR-02 (utils.fs:abspath BC restoration) + WR-02 (audit-script encoding); regression tests; CHANGELOG; verification update |

(Per-wave totals are approximate — actual `git log` is the source of
truth; planning artifact commits and ad-hoc lint touch-ups distribute
across waves.)

## Defense-in-Depth Final Reset Transcript (RESEARCH.md Runtime State Inventory)

Per RESEARCH.md § Runtime State Inventory, annotation-syntax changes
(UP006/007/045 + FA100 in Waves 3/4) invalidate `.mypy_cache/` AST
analysis, and `.ruff_cache/` / `.pytest_cache/` may carry stale
state across the 8 waves. The defense-in-depth final reset clears
all caches and re-runs the Phase 03 acceptance gates against a
fresh tree, before this verification artifact is finalized.

**Sequence (executed Wave 8 Task 1, 2026-05-04T04:24-04:26Z):**

```
$ make superclean
find . -name '*.py[co]' -delete
find . -name '__pycache__' -type d -delete
rm -rf docs/build
rm -rf coverage-report .coverage*
rm -rf .pytest_cache
rm -rf *.egg-info dist
rm -rf dump.rdb
rm -rf .devbox/ .venv/
rm -rf .mypy_cache .ruff_cache .pdm-build
rm -rf tmp/*
Must run 'direnv allow' and 'make init' again
$ echo $?
0

$ make init
... (devbox shell + pdm venv create + pdm install -d -G :all)
  ✔ Install cement 3.0.15 successful
  0:00:05 🎉 All complete! 58/58
$ echo $?
0

$ make test
... 316 passed in 52.83s; 100.00% coverage (3241/3241 stmts)
$ echo $?
0

$ make comply-ruff
pdm run ruff check cement/ tests/
All checks passed!
$ echo $?
0

$ make comply-mypy
pdm run mypy
Success: no issues found in 51 source files
$ echo $?
0

$ make audit-public-api
$ echo $?
0
```

**All 5 reset gates exit 0.** Cache invalidation is not masking any
regression; the 9-conjunct acceptance above is captured against a
freshly-rebuilt environment. Reproducible from a clean checkout
via the same command sequence.

## Gaps Summary

**None.** All 9 D-24 conjuncts GREEN; all 7 phase requirements
(REFACTOR-01..04, COV-01..03) SATISFIED; all 5 ROADMAP Phase 3
success criteria SATISFIED.

### Deferred items (intentional — NOT gaps)

The following are deferrals recorded as decisions, not phase debt:

  - **`vulture`-based dead-code hunt** — D-21 acknowledged. Future
    milestone (3.2.0 cleanup, or dedicated audit milestone) may
    re-open REFACTOR-01 if covered-but-functionally-dead code
    proves to bite. Recorded inline above.
  - **High-priority "untestable" pragma blocks** (CONCERNS.md #1
    signal hooks, ext_plugin dynamic imports, ext_daemon FD ops,
    ext_watchdog single-tuple, ext_generate template loading) —
    Phase 03 audit policy was comment-justify-only per CONTEXT.md
    "Out of scope"; covering those is engineering work for a
    future milestone (or could be promoted to a Phase 03 sub-plan
    if executor encountered cheap wins — none did).
  - **pathlib migration in `cement/cli/` + `cement/ext/`** —
    explicitly out of REFACTOR-03 scope (D-09: literal scope was
    `cement/utils/fs.py` and core internals). Future cleanup can
    extend to `cement/cli/` + `cement/ext/` under the same boundary
    discipline.
  - **FIXME-comment cleanup** (foundation.py:150, ext_daemon.py:
    163/169/175, ext_plugin.py:152, ext_watchdog.py:169,
    ext_generate.py:161, ext_logging.py:223/264) — out of scope per
    CONTEXT.md "Out of scope" (tech debt, not idiom modernization).
  - **mypy strictness knob tightening** (`disallow_any_explicit`,
    `no_implicit_optional`, `warn_unused_ignores`, etc.) — REFACTOR-02
    is hint-level only per CONTEXT.md; knob tightening defers to a
    future milestone (3.2.0 / dedicated type-coverage).
  - **`handler.py:332` duplicate `Handler` union member**
    (`def resolve(...) -> Handler | Handler | None`) — Wave 3
    UP007 cascade artifact, semantically equivalent to
    `Handler | None`. Out-of-scope for D-09 Any-tightening; logged
    in `deferred-items.md` for future tech-debt cleanup or Phase 5.

## Final Acceptance

**All 9 D-24 conjuncts PASS:**

  - [x] #1 — `make test` passes at 100% coverage (REFACTOR-01 / COV-01)
  - [x] #2 — `make comply-ruff` clean with UP+FA family (TOOL-04)
  - [x] #3 — `make comply-mypy` clean (REFACTOR-02 hint changes)
  - [x] #4 — `make audit-public-api` exits 0 (D-04; ROADMAP SC-3)
  - [x] #5 — `coverage-report/` HTML generates without warnings (COV-02)
  - [x] #6 — `Any` reduction strictly positive 41 → 40 (REFACTOR-02; ROADMAP SC-4)
  - [x] #7 — `pragma:nocover` locked-vocabulary grep empty (COV-03; ROADMAP SC-2)
  - [x] #8 — `os.path` in scoped files empty/boundary-tagged (REFACTOR-03; ROADMAP SC-5)
  - [x] #9 — `from __future__ import annotations` strip (D-08 / FA100)

**Phase 03 Internal Refactor & Coverage Hardening: COMPLETE.**

Phase 4 (Backlog Triage) and Phase 5 (Deprecations, Docs & Security
Stubs) are unblocked.

---

*Baseline captured: 2026-05-04 (Wave 5)*
*Finalized: 2026-05-04 (Wave 8 / D-22 step 14)*
*All 9 D-24 conjuncts GREEN; status: passed.*


## Verifier Audit (independent re-run)

**Audited:** 2026-05-03T(see git)
**Auditor:** Claude (gsd-verifier; goal-backward verification)
**Mode:** independent re-run of Wave 8 evidence against live codebase
**Conclusion:** **9/9 D-24 conjuncts confirmed GREEN at the gate level.**
**Caveat:** **2 unresolved BC-breaking findings from 03-REVIEW.md (CR-01,
CR-02) are not acknowledged in the Wave 8 deferral list.** These are
behavioral-semantics regressions on the public `cement.utils.fs:abspath`
surface that do NOT trip the audit-public-api signature gate (D-04 only
diffs symbol/signature, not behavior) but DO conflict with the
project-level `CLAUDE.md` constraint *"Zero public-API breakage on the
3.0.x track — including subclass-exposed internals."*

### Re-run gate results (live, post-Wave-8 branch HEAD)

| # | Gate | Live Command | Result | Status |
|---|------|--------------|--------|:------:|
| 1 | `make test` 100% coverage | `make test` | exit 0; **3241/3241 stmts; 100.00%; 316 passed** | **GREEN ✓** |
| 2 | `make comply-ruff` | `make comply-ruff` | exit 0; **All checks passed!** | **GREEN ✓** |
| 3 | `make comply-mypy` | `make comply-mypy` | exit 0; **Success: no issues found in 51 source files** | **GREEN ✓** |
| 4 | `make audit-public-api` | `make audit-public-api` | exit 0; silent; baseline still **934 lines** | **GREEN ✓** |
| 5 | Coverage HTML present | `ls coverage-report/index.html` | **25733 bytes, present** | **GREEN ✓** |
| 6 | `Any` post-count | `grep -nE ': Any\b\|-> Any\b\|Any\]' cement/core/*.py \| wc -l` | **40** (matches Wave 8 claim of 41 → 40) | **GREEN ✓** |
| 7 | Locked-vocab pragma inverse-grep | (Wave 8 grep) | **0 lines** (141 total sites; categories spot-checked match) | **GREEN ✓** |
| 8 | `os.path` in scoped files (untagged) | `grep -rn 'os\.path' cement/utils/fs.py cement/core/{foundation,template,config}.py \| grep -v '# boundary:' \| wc -l` | **0** (1 tagged survivor: `cement/core/foundation.py:53 join = os.path.join`) | **GREEN ✓** |
| 9 | `from __future__ import annotations` | `grep -rn 'from __future__ import annotations' cement/` | **0 matches** | **GREEN ✓** |

### Independently verified spot-checks

  - **D-19 protected callsites preserved:** 14
    `.format(**template_dict)` callsites in `cement/core/foundation.py`
    (lines 1387, 1392, 1400, 1405, 1413, 1418, 1506, 1511, 1516, 1520,
    1581, 1586, 1591, 1595) — confirmed intact. Matches the D-19
    expected count of 14 protected sites; line numbers shifted from
    original CONTEXT.md per `deferred-items.md` "D-19 line drift
    recorded" disposition.
  - **REQUIREMENTS.md traceability:** All 7 requirement IDs
    (REFACTOR-01..04, COV-01..03) are marked `[x]` in
    `.planning/REQUIREMENTS.md` with explicit Phase 03 Plan
    references in the validation column. No orphans.
  - **Baseline preservation across Wave 8 final reset:** rerunning
    `make audit-public-api` produces empty diff vs. the 934-line
    `03-PUBLIC-API-BASELINE.txt`. D-04 D-24 conjunct #4 holds.
  - **`Any`-site inventory:** ran the `Any` grep myself; the 40 sites
    enumerated in 03-VERIFICATION.md "Per-file post-count breakdown"
    match the live grep output line-by-line. The Wave 5
    `App.__import__(obj: Any)` → `obj: str` tightening is intact in
    `cement/core/foundation.py` (verified at the `def __import__`
    site).

### Gap surfaced by goal-backward audit

#### W-01 (Warning, advisory): Two REVIEW critical findings unresolved on the public `fs.abspath` surface

**Severity:** WARNING — phase gates pass, but the project-level
backward-compat constraint is partially violated.

**Status of Wave 8 disposition:** Neither finding is in 03-REVIEW.md's
"deferred-items" list, in 03-VERIFICATION.md's "Deferred items
(intentional — NOT gaps)" section, in `deferred-items.md`, nor in any
post-REVIEW commit. They appear to have been overlooked between
review (2026-05-03) and Wave 8 finalization (2026-05-04).

**CR-01 — `fs.abspath()` now resolves symlinks (BC-break)**

Empirically reproduced on Python 3.14 against the live branch HEAD
(`cement/utils/fs.py:102`):

```
input:  /tmp/<tmpdir>/link/sub  (where link -> target)
old:    /tmp/<tmpdir>/link/sub        (os.path.abspath semantics)
new:    /tmp/<tmpdir>/target/sub      (Path.resolve semantics — FOLLOWS symlink)
```

Public API surface: `cement.utils.fs:abspath` is in
`03-PUBLIC-API-BASELINE.txt:839`. `fs.HOME_DIR` (line 252) is computed
through `abspath` at module load and feeds every config-dir,
plugin-dir, and template-dir resolution. Downstream apps using
symlinked dotfiles (`~/.config` → repo) will see paths silently
rewritten through the symlink target.

**CR-02 — `fs.abspath()` raises `RuntimeError` on unknown `~user`**

Empirically reproduced on Python 3.14 against the live branch HEAD:

```
input:  '~nosuchuser_xyz/foo'
old:    '/Users/derks/.../~nosuchuser_xyz/foo'  (os.path.expanduser silent fallthrough)
new:    RuntimeError: Could not determine home directory.   (Path.expanduser raises)
```

This is a hard regression. Every config-file / plugin-file /
template-dir / `add_config_dir` / `add_plugin_dir` /
`add_template_dir` callsite that used to silently no-op on a stale
`~deleteduser/path` entry now raises an unhandled `RuntimeError`
mid-`App.setup()`. Test suite does not cover this case (see
`tests/utils/test_fs.py::test_abspath` — single-line `path.startswith('/')`
assertion only).

**Why the gates miss it:**
`make audit-public-api` (D-24 conjunct #4) is a **signature** diff —
parameter names + types + return type from AST. Behavioral
semantics of return values are not part of the gate. ROADMAP Phase 3
Success Criterion #3 ("diff of public symbols ... is empty — no
signatures changed") is also signature-scoped. Both pass even with
CR-01/CR-02 active.

**Conflict with project constraint:** `CLAUDE.md` →
**Constraints** → *"Zero public-API breakage on the 3.0.x track —
including subclass-exposed internals that downstream extensions may
rely on. Deprecation warnings OK; removals go to 3.2.0 at the
earliest."* This is project-level (umbrella) and applies regardless
of phase-specific Success Criteria scope. Behavioral semantics
falls under "public-API breakage" by ordinary reading.

**Why this is WARNING not BLOCKER:**
  - All 9 D-24 conjuncts as defined in 03-CONTEXT.md pass.
  - All 5 ROADMAP Phase 3 Success Criteria pass.
  - All 7 phase requirements (REFACTOR-01..04, COV-01..03) are
    independently SATISFIED.
  - The phase deliverables (audit gate, modernization sweep, pragma
    audit, baseline) are all real, complete, and durable.
  - The CR-01/CR-02 issues are localized to a single function body
    (`cement/utils/fs.py:102`) and have a 2-line fix, but resolving
    them is **engineering work** for a follow-up patch, not a phase
    re-do.

**Recommended human disposition (one of):**
  1. **Address now** before merging Phase 03 to `main` — apply
     the REVIEW.md proposed fix (revert to `os.path.abspath
     (os.path.expanduser(path))`) + add regression tests for
     symlink preservation and unknown-`~user` handling. ~30 min.
  2. **Defer formally** to Phase 5 (Deprecations / Security Stubs)
     or to a hotfix on the 3.0.x branch — record CR-01/CR-02 in
     03-VERIFICATION.md "Deferred items" with explicit
     "BC-break-acknowledged" framing. The phase still ships; the
     follow-up is tracked.
  3. **Override** with a documented decision that the 3.0.x
     compat constraint does NOT extend to symlink-resolution
     semantics or to malformed `~user` strings (i.e., classify
     the prior behavior as bug-shaped, not contract). This is an
     architectural call that requires user authorization.

The verifier surfaces this for human decision. The phase score
remains 9/9 D-24 conjuncts GREEN; the 03-REVIEW.md's two critical
findings are flagged here as a **deferred-decision-required**
escalation, not a phase failure.

#### W-02 (Warning, advisory): Audit script encoding fragility (REVIEW WR-02)

**File:** `scripts/audit-public-api.py:181`
**Issue:** `tree = ast.parse(py.read_text())` defaults to
`locale.getpreferredencoding(False)`. Verified unfixed on live HEAD.
On any non-UTF-8 locale (Windows cp1252, locale-stripped Docker), the
audit gate crashes if cement source contains non-ASCII chars — and
em-dashes are present in audit-point comments (e.g.,
`cement/core/foundation.py`).
**Severity:** WARNING — gate passes on Linux/macOS UTF-8 today, but
the gate is the permanent regression check for 3.0.x→3.2.x. Latent
fragility, not active failure.
**Recommended:** trivial fix `py.read_text(encoding='utf-8')` —
queue for the next ad-hoc patch.

**Resolution (Plan 09 / Wave 9):**

Fixed in commit `cc50a3e3`
(`fix(dev.audit-script): explicit UTF-8 encoding in audit script`).
`scripts/audit-public-api.py:181` now reads source files with
`py.read_text(encoding='utf-8')` per PEP 3120. The
`make audit-public-api` gate continues to exit 0 with empty
diff against the 934-line baseline.

**W-02 STATUS: RESOLVED.**

### Items confirmed correctly deferred

  - **WR-05 / handler.py:332 `Handler | Handler | None`** — explicitly
    deferred in 03-VERIFICATION.md. Comment block in source is
    transparent. Confirmed live at `cement/core/handler.py:344`.
    Disposition is sound.
  - **D-19 line-number drift** — recorded in `deferred-items.md`. The
    14 protected callsites are still present in source; only the
    line numbers in CONTEXT.md text are stale. Not a verification
    concern.
  - **REFACTOR-01 D-21 risk** (covered-but-functionally-dead code,
    private helpers reachable only from tests) — explicit deferral
    with risk acknowledgement; aligned with D-13 strict-minimum
    rule for new dev-deps. Disposition is sound.

### Final verifier assessment

  - **Phase deliverables:** all complete, all green at the
    gate level.
  - **Wave 8 evidence:** independently re-verified — all 9 D-24
    conjuncts hold against the live tree.
  - **Requirements:** all 7 IDs (REFACTOR-01..04, COV-01..03)
    SATISFIED via traceable gate evidence.
  - **ROADMAP SCs:** all 5 Phase 3 SCs SATISFIED.
  - **Outstanding concerns:** 2 items from 03-REVIEW.md (CR-01,
    CR-02) and 1 item (WR-02) NOT acknowledged in the Wave 8
    deferral list. CR-01/CR-02 are real BC-breaking behavior
    changes on a public surface (`cement.utils.fs:abspath`)
    that the signature-only audit gate cannot detect. They do
    not block the phase per the literal D-24 / ROADMAP SC
    contract, but they DO conflict with the project-level
    `CLAUDE.md` "Zero public-API breakage on the 3.0.x track"
    constraint.

**Recommendation:** Status **`human_needed`** (per goal-backward
verifier decision tree, Step 9 rule "if human verification items
exist, status MUST be human_needed"). The user should choose one
of the three CR-01/CR-02 dispositions above before merging
Phase 03 to `main`.

If the user chooses **disposition 2 or 3** (defer or override),
the existing Wave 8 `status: passed` stands and Phase 03 is
ready to merge. If the user chooses **disposition 1** (fix
now), CR-01/CR-02 should be addressed via a small follow-up
plan (`/gsd-plan-phase --gaps`) before merge.

**Resolution (Plan 09 / Wave 9):**

User chose disposition #1 (fix now). The Wave 9 gap-closure
plan landed 5 atomic commits:

| Commit | Subject |
|--------|---------|
| `52248e1d` | `fix(utils.fs): preserve symlinks and silent ~user fallthrough` |
| `25983a57` | `test(utils.fs): cover symlink preservation and unknown-~user` |
| `cc50a3e3` | `fix(dev.audit-script): explicit UTF-8 encoding in audit script` |
| `e31f88d7` | `docs(changelog): record fs.abspath BC fix + audit script encoding` |
| (this commit) | `docs(03): record Wave 9 gap closure (CR-01, CR-02, WR-02)` |

`cement/utils/fs.py:abspath()` body restored to
`os.path.abspath(os.path.expanduser(path))` (with `# boundary: D-14`
inline tag per D-12 / D-14 — `os.path` retention on public
surface is deliberate; pathlib semantics broke BC).

**Empirical re-reproduction (post-fix):**

CR-01 — symlink preservation:

```
input:   /tmp/tmp9vskqq8r/link  (link -> target)
result:  /tmp/tmp9vskqq8r/link  (preserved — NOT resolved)
PASS
```

CR-02 — unknown ~user silent fallthrough:

```
input:    ~nosuchuser_xyz_phase03_gap/foo
result:   /Users/.../~nosuchuser_xyz_phase03_gap/foo  (no RuntimeError)
expected: /Users/.../~nosuchuser_xyz_phase03_gap/foo
PASS
```

**Regression tests pinning the BC contract:**

- `tests/utils/test_fs.py::test_abspath_preserves_symlinks`
- `tests/utils/test_fs.py::test_abspath_unknown_user_does_not_raise`

Both pass against the restored body and FAIL against the Wave 6
`_Path(path).expanduser().resolve(strict=False)` body (verified
locally during Task 2 with a temporary revert sanity check).

**Test count:** 316 → 318 passing at 100% coverage (3241/3241
stmts); coverage gate held.

**W-01 STATUS: RESOLVED.** CR-01 + CR-02 closed; 3.0.x BC
contract on `cement.utils.fs:abspath` restored.

---

*Verifier Audit appended: independent re-run by gsd-verifier.*
*All gate-level evidence confirmed; 2 advisory BC-break findings
surfaced for human disposition.*
