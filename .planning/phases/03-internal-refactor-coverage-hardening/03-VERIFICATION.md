---
phase: 03-internal-refactor-coverage-hardening
verified: 2026-05-04 (in-progress; finalized in Wave 8)
status: in-progress
score: TBD (final score in Wave 8)
overrides_applied: 0
---

# Phase 03 Verification

> **Status:** in-progress. Pre-tightening baselines captured here.
> Final D-24 9-conjunct verification, post-counts, deltas, and
> REFACTOR-01 acceptance-via-coverage rationale land in Wave 8
> (D-22 step 14).

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

**Post-tightening count:** TBD (Task 2 lands the actual tightening; final number recorded in Wave 8)
**Delta:** TBD (D-24 conjunct #6 — must be strictly positive in the reduction direction)

## Pragma audit baseline (COV-03)

**Pre-audit count:** **141 sites** (per
`grep -rn 'pragma:[[:space:]]*no[[:space:]]*cover' cement/ | wc -l` on
2026-05-04).

RESEARCH.md verified **141 sites on 2026-05-03**, NOT the 123 from
CONTEXT.md. Live count on 2026-05-04 matches: 141.

Wave 7 will apply the locked-vocabulary D-15 labels. Wave 8 records the
post-audit grep result (must be empty per D-17 / D-24 conjunct #7).

## Pathlib boundary baseline (REFACTOR-03)

**Pre-migration `os.path` callsites in scoped files:**

```
$ grep -rn 'os\.path' cement/utils/fs.py cement/core/foundation.py \
    cement/core/template.py cement/core/config.py | wc -l
33
```

Per-file breakdown (2026-05-04 count, 33 callsites):

| File | os.path callsites |
|------|-------------------|
| `cement/utils/fs.py` | (smallest, foundational — counted in Wave 6) |
| `cement/core/foundation.py` | (counted in Wave 6) |
| `cement/core/template.py` | (largest single-file blast per D-11) |
| `cement/core/config.py` | (counted in Wave 6) |
| **TOTAL** | **33** |

Wave 6 migrates these 4 files; survivors carry `# boundary: str` per
D-14. Acceptance is `grep -rn 'os\.path' cement/utils/fs.py cement/core/`
returns only `# boundary:`-tagged callsites OR returns empty.

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

## D-24 9-Conjunct Status (in-progress through Wave 5)

| Conjunct | Description | Status After Wave 5 (Task 1) |
|----------|-------------|-------------------------------|
| #1 | `make test` 100% coverage | **green** ✓ (held through Wave 4) |
| #2 | `make comply-ruff` clean (UP+FA) | **green** ✓ (held through Wave 4) |
| #3 | `make comply-mypy` clean | **green** ✓ (held through Wave 4) |
| #4 | `make audit-public-api` exit 0 | **green** ✓ (Wave 3 baseline holds; this commit touches no source) |
| #5 | `coverage-report/index.html` generates | **green** ✓ (COV-02 wave check) |
| #6 | `Any` reduction strictly positive | pending — Task 2 lands the tightening pass |
| #7 | pragma:nocover locked-vocab | pending — Plan 06+ |
| #8 | `os.path` boundary scope | pending — Plan 05/06 |
| #9 | `from __future__ import annotations` strip | **GREEN ✓** (Wave 4 closed) |

## REFACTOR-01 acceptance via coverage gate (D-20)

REFACTOR-01 ("dead code removed") is satisfied by the post-refactor
`make test` passing at 100% coverage with `[tool.coverage.report]
fail_under = 100` — which by construction implies zero unreachable
code. No `vulture`, no dead-code hunting commits, no whitelist file.

The risk acknowledgement (D-21) is recorded: this acceptance leaves
two classes of "dead-but-covered" code undetected:
(a) covered-but-functionally-dead code (executes in tests without
meaningful asserts), and (b) unused private helpers reachable via
import but not called by any production caller. Future milestones
(3.2.0 cleanup, dedicated audit milestone) may re-open with `vulture`
if these gaps prove to bite.

This rationale will be re-stated and finalized in Wave 8.

---

*Baseline captured: 2026-05-04*
*Finalization: Wave 8 (D-22 step 14)*
