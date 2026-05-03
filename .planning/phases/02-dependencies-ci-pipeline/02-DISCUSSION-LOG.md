# Phase 2: Dependencies & CI Pipeline - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-01
**Phase:** 02-dependencies-ci-pipeline
**Areas discussed:** Lockfile/extras/CVE check, pdm.yml verification & Action pinning, Coverage gate enforcement, CI matrix scope

---

## Lockfile, extras & CVE check

### Q1: How aggressive should the lockfile refresh be?

| Option | Description | Selected |
|--------|-------------|----------|
| pdm update | Bumps every dep to latest non-breaking version per current specifiers; single commit, then per-failure splits. | ✓ |
| Targeted per-extra bumps | `pdm update <package>` per extra in separate commits; bisect-friendly but ~10+ commits. | |
| Stay on 0cca6f88 baseline | Treat the post-py39-drop relock as DEPS-01 satisfied; lean on cron for future bumps. | |

**User's choice:** pdm update (Recommended)
**Notes:** Doing manually now proves the baseline is clean and gives the cron job nothing to do on its first post-merge run.

### Q2: Pin policy for `[project.optional-dependencies]`?

| Option | Description | Selected |
|--------|-------------|----------|
| Leave unpinned | Keep `colorlog = ["colorlog"]` shape; downstream apps own version policy. | ✓ |
| Add `>=` floors per extra | Document minimum tested version; mid-floor bumps later become a deprecation conversation. | |
| Floor + upper-bound per extra | `jinja2>=3.1,<4`; maximally protective but cement owns ratchet burden. | |

**User's choice:** Leave unpinned (Recommended)
**Notes:** Most consistent with backward-compat constraint and the zero-runtime-dep ethos.

### Q3: Form of the DEPS-03 CVE spot-check?

| Option | Description | Selected |
|--------|-------------|----------|
| One-shot pip-audit, output committed | `pdm run pip-audit` once locally; capture to 02-PIP-AUDIT.md; pin-around or document any CVE. | ✓ |
| Manual lockfile review | Eyeball pdm.lock vs GHSA/OSV; no tooling commitment. | |
| Add pip-audit to dev deps + Makefile target | Faster path but overlaps Phase 5 SEC-01 stub. | |

**User's choice:** One-shot pip-audit, output committed (Recommended)
**Notes:** Doesn't add pip-audit to dev deps or CI — keeps the Phase 5 SEC-01 stub clean.

### Q4: Response policy if `pdm update` produces failures?

| Option | Description | Selected |
|--------|-------------|----------|
| Phase 1 D-04 split: chore(deps): bump + fix(...) per failure | Atomic per-concern; CI may go red intermediate; PR-level acceptance gates merge. | ✓ |
| Single combined commit | CI green at every commit boundary but loses bisect granularity. | |
| Hold the bump if anything fails | Pin around; most conservative; fights against the unblock-the-cron goal. | |

**User's choice:** Phase 1 D-04 split (Recommended)
**Notes:** Mirrors Phase 1's bisect-friendly atomic shape exactly.

---

## pdm.yml verification & Action pinning

### Q1: How tight should the Action pin policy be?

| Option | Description | Selected |
|--------|-------------|----------|
| Exact tags everywhere | Pin all Actions to exact tags (`@v4.2.2`); reproducible; satisfies CI-05 literally. | ✓ |
| SHA-pinned everywhere | Pin to commit SHAs with tag comment; maximally secure but verbose. | |
| Major-tag with @main eradication | Keep `@v4`/`@v5` major-tag style; only fix the `@main` ref. | |

**User's choice:** Exact tags everywhere (Recommended)
**Notes:** Matches the AUDIT-POINT discipline from Phase 1's D-08 — explicit values, no floating refs.

### Q2: How do we PROVE the scheduled `pdm update` job is unblocked?

| Option | Description | Selected |
|--------|-------------|----------|
| Add `workflow_dispatch:` trigger + run-and-observe | Manual trigger via `gh workflow run`; capture evidence. Permanent affordance. | ✓ |
| Local dry-run only | Trust that GH Action wraps the same `pdm update` command. | |
| Wait for next Monday cron | Cleanest but blocks Phase 6 readiness on a multi-day cycle. | |

**User's choice:** Add `workflow_dispatch:` trigger + run-and-observe (Recommended)
**Notes:** workflow_dispatch becomes a permanent affordance, not just verification scaffolding.

### Q3: Closing the upstream-monitoring gap for Actions (clarification thread)?

User raised: with exact-tag pinning, security patches in upstream Actions don't auto-flow.

| Option | Description | Selected |
|--------|-------------|----------|
| Exact tags + Dependabot for github-actions | Pin exact + add `.github/dependabot.yml`; Dependabot opens PRs with security advisories prioritized. | ✓ |
| Major-tag pins (revise prior decision) | Walk back exact tags; trade reproducibility for free upstream patches. | |
| Exact tags + manual quarterly review | Add a recurring task to review GHSA against pinned Actions. Same shape as the ruff/pdm-update problem we're solving. | |

**User's choice:** Exact tags + Dependabot for github-actions (Recommended)
**Notes:** This pairing is the load-bearing decision — exact-tag pins ARE the right call only because Dependabot backstops them.

### Q4: Pin shape for the untagged `pdm-project/update-deps-action`?

| Option | Description | Selected |
|--------|-------------|----------|
| SHA-pin with date comment | `@<sha>  # pinned 2026-05-XX, no tagged release upstream`; Dependabot still tracks SHA-pinned Action branch HEAD. | ✓ |
| Allow @main as documented exception | Inline comment; smaller delta but creates an exception to the no-floating-refs rule. | |
| Fork into datafolklabs and tag there | Maximum control but adds maintenance surface for marginal benefit. | |

**User's choice:** SHA-pin with date comment (Recommended)
**Notes:** Bumps land as Dependabot PRs like any other.

---

## Coverage gate enforcement

### Q1: Where should the 100% coverage gate be wired?

| Option | Description | Selected |
|--------|-------------|----------|
| pyproject `[tool.coverage.report] fail_under = 100` | Single source of truth; applies anywhere `coverage report` runs. | ✓ |
| pytest addopts `--cov-fail-under=100` | Same effect but lives in pytest config; redundant placement. | |
| Dedicated CI step with `coverage report --fail-under=100` | Most visible in CI logs but only enforced in CI; local drift possible. | |

**User's choice:** pyproject `[tool.coverage.report] fail_under = 100` (Recommended)
**Notes:** Final D-11 also adds `--cov-fail-under=100` to addopts as belt-and-braces.

### Q2: How to ensure fail_under actually fires under pytest-cov?

| Option | Description | Selected |
|--------|-------------|----------|
| Add `--cov-report=term --cov-fail-under=100` to addopts | Pytest-cov honors fail_under from `[tool.coverage.report]` when generating term report. Term report already requested. | ✓ |
| Belt-and-braces: Makefile runs `coverage report` after pytest | Independent of pytest-cov behavior; explicit invocation. | |
| Trust pytest-cov default + add a verification test | Most robust validation but adds CI artifact complexity. | |

**User's choice:** Add `--cov-report=term --cov-fail-under=100` to addopts (Recommended)
**Notes:** Research confirms pytest-cov v7 honors `[tool.coverage.report].fail_under`; the explicit addopts flag is belt-and-braces against future pytest-cov default shifts.

### Q3: Add explicit `[tool.coverage.run]` source/omit block?

| Option | Description | Selected |
|--------|-------------|----------|
| Add explicit source + omit | Mirror ruff's `exclude` discipline (D-08 audit-point pattern); insulate against future template files. | ✓ |
| Rely on implicit `--cov=cement` from Makefile | Smaller delta but no audit-point parity with ruff/mypy. | |
| Defer to Phase 3 COV-03 | Phase 3 owns pragma audit + coverage hardening. Add fail_under in Phase 2; defer scope/omit to Phase 3. | |

**User's choice:** Add explicit `[tool.coverage.run]` source + omit (Recommended)
**Notes:** Mirrors Phase 1's AUDIT POINT comment pattern.

### Q4: Coverage on the `cli-smoke-test` job?

| Option | Description | Selected |
|--------|-------------|----------|
| Leave cli-smoke-test as smoke-only | Black-box install/run test by design; out of scope for COV-01. | ✓ |
| Add coverage to cli-smoke-test too | Surface CLI generation + template rendering coverage paths. | |

**User's choice:** Leave cli-smoke-test as smoke-only (Recommended)
**Notes:** Phase 01.1 set this job up specifically as a smoke test; coverage instrumentation would change what the test measures.

---

## CI matrix scope

### Q1: pypy3.10 — keep, drop, or modernize?

| Option | Description | Selected |
|--------|-------------|----------|
| Keep pypy3.10 in matrix | Cement supports pypy as a downstream value-add; removing is downstream-observable. | |
| Drop pypy3.10 from matrix | Reduce CI surface; treat pypy as undocumented happenstance. | |
| Drop pypy3.10, add pypy3.11 | Modernize the pypy lane; same surface (one pypy job). | |

**User's choice:** Free-text — "keep pypy3.10 and add pypy3.11"
**Notes:** Both lanes. Avoids any downstream-observable change while modernizing. `actions/setup-python@v5` supports `pypy-3.11`. Matrix grows from 6 to 7 lanes.

### Q2: Tackle the OS matrix `# FIXME ?` comment?

| Option | Description | Selected |
|--------|-------------|----------|
| Leave ubuntu-only + remove the FIXME comment | macOS/Windows lanes are out of scope for Clean & Green; clean up cruft. | ✓ |
| Add macOS lane | libmemcached via Homebrew; doubles CI runtime; surfaces real platform differences. | |
| Add macOS + Windows lanes | Full cross-platform matrix; almost certainly surfaces blockers. | |
| Leave the FIXME comment in place | Status quo; smallest delta. | |

**User's choice:** Leave ubuntu-only + remove the FIXME comment (Recommended)
**Notes:** macOS/Windows support is a separate dedicated effort.

### Q3: Job graph — keep serial or flatten?

| Option | Description | Selected |
|--------|-------------|----------|
| Keep serial sequencing | Intentional fail-fast; don't burn 7 matrix lanes if mypy/ruff is red. | ✓ |
| Flatten: comply, test, test-all in parallel | Faster PR feedback (~15 min) but burns more compute. | |
| Partial flatten: comply gates, test+test-all parallel | Compromise; smaller delta than full flatten. | |

**User's choice:** Keep serial sequencing (Recommended)
**Notes:** Touching the job graph risks regressions while we're trying to prove it works.

---

## Claude's Discretion

- Exact commit-message body phrasing within the D-17 split (planner picks).
- Whether to author commits via `make commit` or directly via `git commit`.
- Order of unrelated `ci: ...` commits within D-17's middle (Dependabot enablement, workflow_dispatch trigger, pypy-3.11 add, FIXME drop) — planner can interleave.
- Specific tag/SHA values for Action pins (research picks current stable; planner verifies via `gh api repos/<owner>/<repo>/releases`).
- Whether to bundle Dependabot config additions for `pip` ecosystem too (kept OUT per D-07; planner can revisit if research surfaces a strong reason).

## Deferred Ideas

- macOS / Windows OS matrix lanes — dedicated platform-support effort; out of scope for Clean & Green.
- Job-graph flattening — cement isn't a high-PR-velocity project; deferred indefinitely.
- `pip` ecosystem in Dependabot — `pdm.yml` cron handles it; revisit if pdm.yml is ever retired.
- Coverage instrumentation for `cli-smoke-test` — revisit if a coverage gap analysis shows the smoke path covers something unit tests miss.
- Optional-extras lower-bound floors — revisit on a 3.2.0 breakage-allowed milestone if there's a real pain point.
- `pip-audit` / `bandit` / SAST CI integration — Phase 5 SEC-01/02/03 stubs.
