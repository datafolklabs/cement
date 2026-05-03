# Phase 2 — Acceptance Verification

**Phase:** 02-dependencies-ci-pipeline
**Verified:** 2026-05-03 (static checks); D-19 #1 + #3 pending PR / post-merge
**Verifier:** BJ Dierkes <derks@datafolklabs.com>
**Phase PR:** _pending — fill in after PR open (Task 2)_
**Phase merge SHA:** _pending — fill in after merge (Task 3); current branch
HEAD at static-check time was `fe20cb48` on `modernization-phase-2`_

> **Status legend.** Three of the five D-19 conditions are evidenceable
> entirely from the local merged Phase 2 working tree (#2 wiring, #4
> artifact existence, #5 floating-ref grep). Two require live GitHub
> infrastructure (#1 PR-CI green, #3 post-merge `workflow_dispatch`)
> and are filled in by Task 2 / Task 3 of this plan after the PR is
> opened and merged. The skeleton below is complete; the two pending
> sections show exactly what evidence to capture and where to paste it.

## D-19 Acceptance Conditions

### #1 — All 7 matrix lanes green on fresh PR

**Status:** PENDING (requires PR open — Task 2 of this plan)

**Evidence to capture (Task 2 fills these in):**

  - PR URL: `https://github.com/datafolklabs/cement/pull/<NNN>`
  - Run-summary URL:
    `https://github.com/datafolklabs/cement/pull/<NNN>/checks`
  - `gh pr checks <PR> -R datafolklabs/cement` output (paste the
    relevant lane rows; full output may include other contexts):

    ```
    comply                       pass
    test                         pass
    test-all (3.10)              pass
    test-all (3.11)              pass
    test-all (3.12)              pass
    test-all (3.13)              pass
    test-all (3.14)              pass
    test-all (pypy3.10)          pass
    test-all (pypy3.11)          pass
    cli-smoke-test               pass
    ```

  - Expected lane count: 7 matrix lanes (3.10, 3.11, 3.12, 3.13, 3.14,
    pypy3.10, pypy3.11) plus `comply`, `test`, `cli-smoke-test`.

**Pre-PR static prerequisites verified locally (this plan, Task 1):**

  - 7-lane matrix declared in `.github/workflows/build_and_test.yml`:

    ```
    python-version: ["3.10", "3.11", "3.12", "3.13", "3.14",
                     "pypy3.10", "pypy3.11"]
    ```

    (Plan 05 SUMMARY commit `6ecfbc65`; FIXME comment removed in
    `4b5160a8` — Plan 05 Task 2 cleanup.)

  - All 5 distinct Actions in `build_and_test.yml` exact-tag-pinned
    (Plan 04 commit `529df89c`); zero floating refs (D-19 #5 below).

  - `comply` job invokes `make comply` (ruff + mypy); `test` job
    invokes `make test` which carries the 100% coverage gate
    (Plan 03 commit `875fe621`; D-19 #2 below).

### #2 — 100% coverage gate fires below 100%

**Status:** PASS

**Evidence:**

  - **Local gate-fires demo (D-19 #2 evidence captured by Plan 03
    Task 2 — see `02-03-SUMMARY.md` § "D-19 Acceptance #2 Evidence
    — Gate-Fires Demonstration"):**

    ```
    cement/utils/version.py                 36      1  97.22%
    TOTAL                                 3287      1  99.97%
    FAIL Required test coverage of 100% not reached. Total coverage: 99.97%
    make: *** [Makefile:29: test] Error 1
    ```

    Exit code: 2 (coverage.py `fail-under` non-zero gate fired as
    designed). Demo file restored to baseline before Plan 03 commit;
    user explicitly approved this snippet as satisfying D-19 #2.

  - **Wiring intact post-merge (Task 1 re-verification):**

    | Check | Command | Result |
    |---|---|---|
    | `fail_under = 100` | `grep -F 'fail_under = 100' pyproject.toml` | 1 line |
    | `--cov-fail-under=100` | `grep -F -- '--cov-fail-under=100' pyproject.toml` | 1 line |
    | `source = ["cement"]` | `grep -F 'source = ["cement"]' pyproject.toml` | 1 line |
    | `templates` omit | `grep -F '"cement/cli/templates/*"' pyproject.toml` | 1 line |
    | `contrib` omit | `grep -F '"cement/cli/contrib/*"' pyproject.toml` | 1 line |

  - Per RESEARCH.md Pitfall 5, the demonstration is local-only — the
    wired gate does not need a throwaway-PR demo to satisfy the
    acceptance check.

### #3 — workflow_dispatch run of pdm.yml clean

**Status:** PENDING (requires post-merge `gh workflow run` — Task 3 of
this plan)

**Evidence to capture (Task 3 fills these in):**

  - **Trigger time:** YYYY-MM-DD HH:MM UTC
  - **Run URL:**
    `https://github.com/datafolklabs/cement/actions/runs/<RUN-ID>`
  - **Outcome:** one of (BOTH passing per CONTEXT.md D-09):
    - **Outcome A** — no-op no-PR-opened (`pdm update` is a no-op
      against Plan 01's bumped baseline; cron path proves clean
      end-to-end with no changes to propose). Likely outcome.
    - **Outcome B** — PR-opened (`pdm-project/update-deps-action`
      proposes one or more upstream bumps that arrived since
      Plan 01). Also passing — proves the action's PR-opening
      pipeline is healthy.
  - **Failure mode (NOT acceptable):** wall-of-lint output mid-run
    (the historic failure mode this plan must close). If this
    surfaces, Phase 2 stays open until atomic `fix(...)` follow-up
    commits land.

**Pre-merge static prerequisite verified locally (Task 1):**

  - `workflow_dispatch:` trigger present in
    `.github/workflows/pdm.yml` (Plan 07 commit `a3078b84`):

    ```
    $ grep -E '^\s*workflow_dispatch:' .github/workflows/pdm.yml
      workflow_dispatch:
    ```

  - Both Actions in `pdm.yml` exact-tag-pinned (Plan 04 + Plan 07
    invariant preserved):
    - `actions/checkout@v6.0.2` (1 site)
    - `pdm-project/update-deps-action@v1.12` (1 site; SHA fallback
      `22852fcff9a131d732730e8db92cc9502643a260` documented in
      Plan 04 commit body for tag-mutability defense per D-06
      deviation acknowledgment)

### #4 — 02-PIP-AUDIT.md exists with disposition

**Status:** PASS

**File:** `.planning/phases/02-dependencies-ci-pipeline/02-PIP-AUDIT.md`
(167 lines; created in Plan 02 commit `69da9e14`).

**Section presence (all 5 mandatory headings verified):**

  - `# Phase 2` (top-level title) — present
  - `## Post-update results` — present
  - `## Accepted vulnerabilities` — present
  - `## Resolutions applied via Plan 01 chore(deps): pdm update` — present
  - `## Pin-arounds applied this plan` — present

**Per-CVE disposition summary (cross-referenced from
`02-02-SUMMARY.md` § "Per-CVE Disposition Summary"):**

  - **Resolved by Plan 01 `requests 2.31.0 -> 2.33.1`:** 3 CVEs
    (CVE-2024-35195, CVE-2024-47081, CVE-2026-25645)
  - **Pinned-around:** 0
  - **Accepted:** 11 unique CVEs across 5 packages (certifi PYSEC-
    2024-230, idna PYSEC-2024-60, pip CVE-2026-1703, pip
    CVE-2026-3219 [no upstream fix], pygments CVE-2026-4539, urllib3
    CVE-2024-37891, urllib3 CVE-2025-50182, urllib3 CVE-2025-50181,
    urllib3 CVE-2025-66418, urllib3 CVE-2025-66471, urllib3
    CVE-2026-21441) — all dev/docs-only transitives; cement core has
    `dependencies = []` so none enter the runtime install graph for
    downstream `pip install cement[<runtime-extra>]` users
  - **Re-evaluation cadence:** Phase 5 SEC-01 (permanent pip-audit CI
    surface) — at that time the 11 Accepted findings get re-litigated
    against the then-current advisory DB

  Total: 14 baseline-snapshot CVEs traced (3 Resolutions + 11
  Accepted). 0 silent omissions.

### #5 — No floating Action refs in workflows

**Status:** PASS

**Evidence (Task 1 re-verification):**

  ```
  $ grep -rEcn '@v[0-9]+$|@main|@master' .github/workflows/ \
      | awk -F: '{s+=$NF} END{print s+0}'
  0
  ```

  Zero lines summed across both workflow files. Per RESEARCH.md
  Correction 1, the original CONTEXT.md D-19 #5 acceptance text
  assumed one SHA-pinned exception for `pdm-project/update-deps-
  action`; the revised acceptance grep (above) requires zero matches,
  and the working tree complies — `pdm-project/update-deps-action` is
  exact-tag-pinned to `@v1.12` (Plan 04 commit `529df89c`), unifying
  policy with D-05.

  **Cross-check — every Action+repo pair pinned to an exact tag:**

  | Action | Workflow | Tag | Sites |
  |---|---|---|---|
  | `actions/checkout` | `build_and_test.yml` | `@v6.0.2` | 4 |
  | `actions/checkout` | `pdm.yml` | `@v6.0.2` | 1 |
  | `ConorMacBride/install-package` | `build_and_test.yml` | `@v1.1.0` | 3 |
  | `actions/setup-python` | `build_and_test.yml` | `@v6.2.0` | 2 |
  | `pdm-project/setup-pdm` | `build_and_test.yml` | `@v4.4` | 3 |
  | `hoverkraft-tech/compose-action` | `build_and_test.yml` | `@v2.6.0` | 3 |
  | `pdm-project/update-deps-action` | `pdm.yml` | `@v1.12` | 1 |

  17 total exact-tag-pin sites across 7 distinct Action+repo pairs.

## Repo-level Settings (per RESEARCH.md Correction 2 + Pitfall 6)

- **Dependabot security updates:** ENABLED (per Plan 06 Task 2
  human-verify checkpoint — `02-06-SUMMARY.md` § "Task 2 — Human-
  Verify Result (Repo-Level Toggle)" embeds the user's verbatim
  confirmation: _"User confirmed: Dependabot security updates toggle
  is already ON / turned ON at https://github.com/datafolklabs/cement/
  settings/security_analysis"_).

  This dual-gate completes CI-05 closure: Plan 04 static pin baseline
  + Plan 06 yaml (`.github/dependabot.yml` weekly version-update PRs
  for `github-actions` ecosystem) + repo-level toggle for security-
  CVE-driven PRs from GitHub Security Advisories.

  Verification method: UI-only (GitHub does not expose this toggle
  via public REST/GraphQL API). User's confirmation is the
  authoritative signal per Plan 06 Task 2 specification.

## Phase 2 Commit Audit

**Phase 2 commit range:** `aafa632a..HEAD` (anchor: `aafa632a`,
`docs(state): record phase 2 context session`)

**Total commits in range:** 34 (27 non-merge + 7 `chore: merge
executor worktree` from worktree-mode parallel execution).

**By Conventional-Commit type (non-merge):**

  | Type | Count | Plans |
  |---|---:|---|
  | `chore(deps)` | 1 | Plan 01 lockfile bump (`9f0f8627`) |
  | `fix(type)` | 2 | Plan 01 sub-step B drift-fixes (`bf567f2b`, `54253244`) |
  | `test` | 1 | Plan 03 coverage gate wiring (`875fe621`) |
  | `ci` | 5 | Plan 04 (`529df89c`); Plan 05 (`6ecfbc65`, `4b5160a8`); Plan 06 (`dfb9abba`); Plan 07 (`a3078b84`) |
  | `docs(02...)` | 12 | per-plan SUMMARYs + planning artifacts |
  | `docs(phase-02)` | 6 | post-wave tracking updates |
  | merges | 7 | parallel-executor worktree merges (no payload) |

**Commit-shape compliance (CLAUDE.md § "Commit Conventions"):**

  | Check | Command | Result |
  |---|---|---|
  | Subject ≤78 chars | `git log aafa632a..HEAD --format=%s | awk 'length>78 {bad++} END {exit (bad?1:0)}'` | PASS (longest 65 chars) |
  | Body ≤78 chars | `git log aafa632a..HEAD --format=%b | awk 'length>78 {bad++} END {exit (bad?1:0)}'` | PASS (longest 72 chars) |
  | Conventional Commits | every non-merge subject matches `^(chore|fix|test|ci|docs)(\(...?\))?:` | PASS |

  Longest subject: `fix(type): drop unused type-ignores in
  ext_watchdog vs watchdog 6` (65 chars). Longest body line:
  `Warning 4: 02-04 brittle line-number annotations replaced with
  grep note` (72 chars). Both well under the 78-char cap.

## CHANGELOG Audit

`## 3.0.15 - DEVELOPMENT` section in `CHANGELOG.md` gained the
following Phase 2 entries (cross-referenced against each plan's
SUMMARY):

  | Plan | Bucket | Entry | Status |
  |---|---|---|:---:|
  | Plan 01 | Misc | `` `[dev]` Bump dev/extras lockfile to current non-breaking versions (redis 7.4, watchdog 6.0, tabulate 0.10, sphinx 8.1, requests 2.33, others) `` | OK |
  | Plan 01 (drift) | Bugs | `` `[ext.redis]` Resolve mypy union-attr/arg-type/misc errors surfaced by redis 7 typing changes `` | OK |
  | Plan 01 (drift) | Bugs | `` `[ext.watchdog]` Drop now-unused `# type: ignore` comments on Observer schedule/start/stop calls `` | OK |
  | Plan 02 | (none) | (no pin-arounds fired; all 11 unique CVEs Accepted per CONTEXT.md D-03 — no `[deps]` Misc entry expected) | n/a |
  | Plan 03 | Misc | `` `[dev]` Wire 100% coverage gate via `[tool.coverage.report]` `fail_under` + `--cov-fail-under` addopts; explicit `[tool.coverage.run] source/omit` `` | OK |
  | Plan 04 | Misc | `` `[ci]` Pin GitHub Actions to exact tags (checkout v6.0.2, setup-python v6.2.0, setup-pdm v4.4, install-package v1.1.0, compose-action v2.6.0, update-deps-action v1.12) `` | OK |
  | Plan 05 | Misc | `` `[ci]` Add PyPy 3.11 to CI test matrix (alongside existing PyPy 3.10) `` | OK |
  | Plan 05 (cleanup) | (none) | (FIXME-drop is comment cleanup, no CHANGELOG entry per CLAUDE.md filter rule) | n/a |
  | Plan 06 | Misc | `` `[ci]` Enable Dependabot for github-actions ecosystem (weekly) `` | OK |
  | Plan 07 | Misc | `` `[ci]` Add workflow_dispatch trigger to pdm.yml `` | OK |

  **Mandatory entries present:** 6 of 6 (`[dev]` lockfile, `[dev]`
  coverage gate, `[ci]` Action pins, `[ci]` PyPy 3.11, `[ci]`
  Dependabot, `[ci]` workflow_dispatch). All grep-verified.

  **Conditional entries present:** 2 of 2 Plan 01 drift-fix Bugs
  entries (`[ext.redis]`, `[ext.watchdog]`); 0 Plan 02 pin-around
  Misc entries (intentionally — Sub-step B did not fire).

  **Filter-rule compliance:** No `docs(02...)` or `docs(phase-02)`
  planning-artifact commit touched `CHANGELOG.md` (per CLAUDE.md §
  "Changelog Maintenance" filter rule — planning scaffolding is not
  user-facing). Verified via spot-checks against Plan 02 / Plan 06
  / Plan 07 SUMMARYs which each independently re-confirm.

## Plan-by-Plan Deliverable Verification (S.4 audit)

  | Plan | Deliverable | Verification | Result |
  |---|---|---|:---:|
  | Plan 01 | `pdm.lock` bumped within Phase 1 specifiers | 14 packages updated; `pdm update --dry-run` returns "All packages are synced" | OK (per `02-01-SUMMARY.md`) |
  | Plan 02 | `02-PIP-AUDIT.md` w/ 5 sections + dispositions | All 5 mandatory headings + 11 unique CVEs all Accepted | OK |
  | Plan 03 | `pyproject.toml` coverage wiring | `fail_under = 100`, `--cov-fail-under=100`, `source = ["cement"]`, both omit globs | OK |
  | Plan 04 | 7 distinct Action+repo pairs exact-tag-pinned | 17 sites total — see § "#5" cross-check table | OK |
  | Plan 05 | 7-lane matrix, FIXME removed | matrix line `["3.10", "3.11", "3.12", "3.13", "3.14", "pypy3.10", "pypy3.11"]`; `grep -c 'FIXME ?'` returns 0 | OK |
  | Plan 06 | `.github/dependabot.yml` (github-actions only) | file exists; ecosystem `github-actions` present; `pip` ecosystem absent (D-07) | OK |
  | Plan 07 | `workflow_dispatch:` in `pdm.yml` | present as sibling of `schedule:` cron | OK |

## Final Acceptance

**All 5 D-19 conditions PASS:** [ ] YES (pending Tasks 2 + 3 sign-off)

  - [ ] #1 — All 7 matrix lanes green on fresh PR (PENDING — Task 2)
  - [x] #2 — 100% coverage gate fires below 100% (PASS — Plan 03
    local demo + post-merge wiring re-verified)
  - [ ] #3 — workflow_dispatch run of pdm.yml clean (PENDING — Task 3)
  - [x] #4 — `02-PIP-AUDIT.md` exists with disposition (PASS)
  - [x] #5 — No floating Action refs in workflows (PASS)

**Phase 2 status:** PENDING (3/5 conditions PASS locally; 2/5
require live GitHub evidence). Will flip to COMPLETE after Task 2
captures PR-CI green and Task 3 captures clean workflow_dispatch
run + updates STATE.md.

**Hand-off to Phase 3:** Internal Refactor & Coverage Hardening
(REFACTOR-01..04, COV-01..03). The 100% coverage gate is wired
(Plan 03) and CI is pre-confirmed green via local `make test` (316
passed, 100% coverage, 0 lint, 0 mypy) at every wave handoff
through Phase 2 — Phase 3 inherits the green starting line it
needed.

---

## Notes — Side-effects acknowledged (Phase 2 carry-forward)

- **`make test-core` will now fail under the gate** (per RESEARCH.md
  Open Question 2 + Pitfall 1; recorded in `02-03-SUMMARY.md` §
  "Side-Effects / Pitfalls Acknowledged"). `make test-core` scopes
  coverage to `cement.core` only (~30% of `cement/`); under
  `fail_under = 100` it now reports ~30% and exits non-zero.
  Accepted as a Phase-2 side-effect — CI uses `make test`, not
  `make test-core`. Future maintainer-facing work to either restore
  `make test-core` semantics or document its post-gate behavior is
  Phase 3 / Phase 4 territory.

- **Wave-7 (this plan) gating posture:** Tasks 2 + 3 below are
  human-verify checkpoints by design — they require live GitHub
  evidence that cannot be evidenced from the local working tree
  alone. The orchestrator opens the Phase 2 PR and dispatches Task
  2; after merge it dispatches Task 3 to fire `gh workflow run
  pdm.yml` and finalize this artifact.
