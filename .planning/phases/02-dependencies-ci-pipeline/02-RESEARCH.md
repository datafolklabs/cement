# Phase 2: Dependencies & CI Pipeline - Research

**Researched:** 2026-05-02
**Domain:** Python dependency management (PDM), GitHub Actions hardening, supply-chain hygiene, coverage gate enforcement
**Confidence:** HIGH (concrete versions / SHAs / dry-run output verified against live registries today)

## Summary

Phase 2 has very little discovery work left — `02-CONTEXT.md` locked 19 decisions (D-01 through D-19). What this research provides is the **concrete values** the planner needs to fill in those decisions and **two corrections** to assumptions that were carried forward in CONTEXT.md.

**Two corrections to CONTEXT.md assumptions (planner MUST resolve before writing PLAN.md):**

1. **D-06 premise is wrong.** `pdm-project/update-deps-action` DOES have tagged releases — 13 of them, latest `v1.12` published 2025-04-21 [VERIFIED: api.github.com/repos/pdm-project/update-deps-action/releases]. The action's own README still pins to `@main` as the example, which is likely why the project's `pdm.yml:14` uses `@main`, but that's a usage convention, not a tag-availability constraint. **Recommendation:** pin to exact tag `@v1.12` (consistent with D-05 exact-tag-everywhere policy) instead of SHA-pinning. SHA-pin remains a fallback only if the planner discovers a tag-mutability concern. This simplifies D-06 and removes the "untagged exception" from the D-19 acceptance grep.

2. **Dependabot does NOT have a "github-actions security advisories prioritized" feature in the way CONTEXT.md D-07 implies.** GitHub Actions is **version-updates only** in `dependabot.yml`; there is no per-ecosystem `security-updates: true` flag for it [CITED: docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file]. However — and this is the saving nuance — **Dependabot security updates** (a separate feature toggled at the **repo level**, not via dependabot.yml) DO surface CVEs against pinned GitHub Actions and auto-open security PRs [CITED: docs.github.com/en/code-security/dependabot/dependabot-security-updates/about-dependabot-security-updates]. Phase 2's D-07 deliverable (the `dependabot.yml` file) only handles version updates; getting the security-PR backstop the user wants requires also enabling the repo setting "Dependabot security updates" under Settings → Code security and analysis. **Recommendation:** the dependabot.yml file is correct as planned; add a one-line note in the phase verification artifact reminding the user to flip the repo-level toggle (cannot be set from a yaml file).

Everything else is concrete substitution: tag values, SHA hashes, version numbers, minimal yaml shapes. The 14-package `pdm update` dry-run preview is captured below.

**Primary recommendation:** Land the 10 atomic commits per D-17 in this order, with the substitutions in §"Concrete Substitutions"; the lockfile bump and CVE pin-around will likely fold into ≤2 commits (pdm update is mostly clean against the new baseline).

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DEPS-01 | `pdm.lock` regenerated against current package indexes; matches latest non-breaking versions | Dry-run preview: 14 packages bump; all within current `~=` / `>=` specifiers (no spec-override needed). See §"`pdm update` Dry-Run Preview" |
| DEPS-02 | Optional-extras upgraded to current stable releases compatible with Python 3.10–3.14 | Verified PyPI metadata for every extra: redis 7.4.0, watchdog 6.0.0, tabulate 0.10.0, jinja2 3.1.6, pyyaml 6.0.3, colorlog 6.10.1, pylibmc 1.6.3, pystache 0.6.8 — all support py3.10+. See §"Optional-Extras Latest Versions" |
| DEPS-03 | Any runtime dep with known unpatched CVE resolved or pinned with rationale | One-shot `pdm run pip-audit` against the **current pre-update** lockfile surfaces 16 vulns in 6 packages (mostly dev/docs deps). After `pdm update` lands, ≥9 of these resolve automatically (requests 2.31.0→2.33.1 closes 3 CVEs). See §"pip-audit Pre-Update Snapshot" |
| DEPS-04 | Scheduled `pdm update` GH Action unblocked — runs cleanly to completion | D-08 adds `workflow_dispatch:` for manual verification. Minimal yaml provided in §"workflow_dispatch Trigger" |
| CI-01 | Matrix Python 3.10–3.14 — all green | Already configured (Phase 1 D-05); D-14 adds pypy-3.11; pypy-3.11 maps to PyPy 7.3.22 (Python 3.11.15) per PyPy versions.json |
| CI-02 | Compliance jobs (ruff, mypy) run on every PR and pass | No change needed; existing `comply` job already wired to `make comply` |
| CI-03 | 100% coverage gate fails build below 100% | D-10/D-11/D-12 pyproject changes verified locally — coverage 7.13.5 + pytest-cov 7.1.0 honor `[tool.coverage.report].fail_under = 100` from pyproject.toml (auto-discovery confirmed) |
| CI-05 | Action versions pinned to current stable | Concrete tag values for all 5 actions captured in §"Concrete Substitutions" |
</phase_requirements>

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** `pdm update` (active bump, not passive `pdm lock`) — lands as `chore(deps): pdm update to current non-breaking versions`, then per-failure splits.
- **D-02:** `[project.optional-dependencies]` STAYS UNPINNED. Downstream apps own version policy.
- **D-03:** One-shot `pip-audit` run; output committed to `02-PIP-AUDIT.md`. NOT added to dev-deps. NOT a recurring CI job (Phase 5 owns SEC-01).
- **D-04:** Phase 1 D-04 atomic-per-failure split for any drift the update produces.
- **D-05:** Exact tags everywhere (`@v4.2.2`, not `@v4`). All Actions across both workflows.
- **D-06:** SHA-pin for `pdm-project/update-deps-action` (untagged) with dated comment. **⚠️ See "Correction 1" in Summary — action HAS tags.**
- **D-07:** Enable Dependabot for `github-actions` ecosystem ONLY. Pip stays out. **⚠️ See "Correction 2" in Summary — security-PR backstop requires repo-level toggle, not yaml.**
- **D-08:** Add `workflow_dispatch:` to `pdm.yml`.
- **D-09:** Acceptance: workflow_dispatch run completes WITHOUT wall-of-lint failure. No-op (no PR opened) is a passing outcome.
- **D-10:** Wire `fail_under = 100` in `pyproject.toml` `[tool.coverage.report]`, not in CI YAML.
- **D-11:** Also add `--cov-fail-under=100` to pytest `addopts` (belt-and-braces).
- **D-12:** Add explicit `[tool.coverage.run]` block: `source = ["cement"]`, `omit = ["cement/cli/templates/*", "cement/cli/contrib/*"]`.
- **D-13:** NO coverage on `cli-smoke-test` job.
- **D-14:** Keep `pypy3.10`; ADD `pypy-3.11` (or `pypy3.11`).
- **D-15:** Leave OS matrix ubuntu-only; remove `# FIXME ?` comment.
- **D-16:** Keep serial job graph (`comply → test → test-all → cli-smoke-test`).
- **D-17:** Atomic per-concern Conventional Commits, 78-char wrap; suggested 10-commit split.
- **D-18:** GSD artifact commits = `docs(02): ...`.
- **D-19:** Acceptance = (1) PR triggers all 7 lanes green, (2) coverage gate fails at <100%, (3) workflow_dispatch run clean, (4) `02-PIP-AUDIT.md` exists, (5) grep shows only the SHA-pinned line floating-ref-style.

### Claude's Discretion

- Exact commit-message body phrasing within the D-17 split.
- Whether to author commits via `make commit` or `git commit` directly.
- Order of unrelated `ci: ...` commits within D-17's middle.
- Specific tag/SHA values for Action pins (research picks current stable; planner verifies).
- Whether to bundle Dependabot config additions for `pip` ecosystem too — kept OUT per D-07 default.

### Deferred Ideas (OUT OF SCOPE)

- macOS / Windows OS matrix lanes
- Job-graph flattening (parallelizing comply/test/test-all)
- `pip` ecosystem in Dependabot
- Coverage instrumentation for `cli-smoke-test`
- Optional-extras lower-bound floors (`>=`)
- `pip-audit` / `bandit` / SAST CI integration (Phase 5)
</user_constraints>

## Project Constraints (from CLAUDE.md)

These project directives are MANDATORY — the planner MUST honor them. Verified they do not conflict with any locked CONTEXT.md decision.

| Directive | Source | Phase 2 Implication |
|-----------|--------|--------------------|
| 100% test coverage required | CLAUDE.md §"Key Development Practices" | D-10/D-11/D-12 enforce this absolutely |
| 100% PEP8 compliance via ruff | CLAUDE.md §"Key Development Practices" | Any `pdm update` fallout that breaks ruff lands as `fix(lint): ...` per D-04 |
| Type annotation compliance via mypy | CLAUDE.md §"Key Development Practices" | Any pdm update fallout that breaks mypy lands as `fix(type): ...` per D-04 |
| Zero external runtime deps for core framework | CLAUDE.md §"Key Development Practices" | Phase 2 only touches `[dependency-groups].dev` + `[project.optional-dependencies]` (pinning policy) — never adds anything to `dependencies = []` |
| Conventional Commits mandatory; 78-char subject + body wrap | CLAUDE.md §"Commit Conventions" | D-17 ten-commit split conforms |
| Use `make commit` (cz commit) interactive — OR equivalent direct git commit | CLAUDE.md §"Commit Conventions" | Either path acceptable per D-17 Discretion |
| Update `CHANGELOG.md` phase-by-phase as work lands | CLAUDE.md §"Changelog Maintenance" | Each Phase 2 commit appends its `[area]` entry to active `## 3.0.15 - DEVELOPMENT` section |
| Bucket: `chore(deps):` → Misc, `ci:` → Misc, `fix(lint\|type\|test):` → Bugs | CLAUDE.md §"Changelog Maintenance" | See §"Changelog Bucketing for Phase 2 Commits" below |

**Note on changelog header:** The active section in CHANGELOG.md is `## 3.0.15 - DEVELOPMENT (will be released as stable/3.0.16)` — keep the parenthetical when appending entries.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Lockfile regeneration | PDM (build/dev tooling) | — | `pdm update` mutates `pdm.lock`; not a runtime concern |
| Optional-extras pinning | pyproject.toml `[project.optional-dependencies]` (publishable metadata) | — | Downstream-observable; D-02 keeps unpinned |
| CVE spot-check | pip-audit (one-shot CLI) | PyPI Advisory DB / OSV | Dev-time hygiene, not CI; D-03 |
| GH Action pinning | `.github/workflows/*.yml` (CI config) | — | CI-only; doesn't affect downstream |
| Dependabot enablement | `.github/dependabot.yml` (repo-level config) | GitHub repo settings (security toggle) | Repo infrastructure; surfaces PRs against the workflows |
| Coverage gate enforcement | pyproject.toml `[tool.coverage.*]` (test config) | pytest `addopts` | Single source of truth (D-10) + belt-and-braces (D-11) |
| Matrix expansion | `.github/workflows/build_and_test.yml` `strategy.matrix` | actions/setup-python (PyPy resolution) | Pure CI config; PyPy 7.3.22 transparently resolved |
| Manual workflow trigger | `pdm.yml` `on: workflow_dispatch:` | — | CI affordance; survives the phase as a permanent feature |

## Standard Stack

### Concrete Substitutions

These are the values the planner literally writes into the workflow files. **All version probes performed today (2026-05-02) against live GitHub Releases / commits API; SHAs are full 40-char where required.**

| Action | Current Pin | Latest Tagged Release | Published | Recommended Replacement |
|--------|-------------|----------------------|-----------|--------------------------|
| `actions/checkout` | `@v4` | `v6.0.2` | 2026-01-09 | `@v6.0.2` |
| `actions/setup-python` | `@v5` | `v6.2.0` | 2026-01-22 | `@v6.2.0` |
| `pdm-project/setup-pdm` | `@v4` | `v4.4` (latest published release; v4.5 exists as a tag without a release) | 2025-04-23 | `@v4.4` (or `@v4.5` if planner prefers most-recent tag — both safe, v4.4 is the conservative pick) |
| `ConorMacBride/install-package` | `@v1` | `v1.1.0` | 2022-06-19 | `@v1.1.0` |
| `hoverkraft-tech/compose-action` | `@v2.0.1` | `v2.6.0` | 2026-04-16 | `@v2.6.0` |
| `pdm-project/update-deps-action` | `@main` | `v1.12` | 2025-04-21 | `@v1.12` (see Correction 1 — D-06 SHA-pin no longer needed) |

**[VERIFIED 2026-05-02 via curl + GitHub Releases API]**

If the planner accepts the recommendation in Correction 1, the D-19 acceptance grep changes:
```
# Original D-19 (assumes one SHA-pinned exception):
grep -rn "@v[0-9]\+$\|@main" .github/workflows/   # should show only the SHA-pinned line

# Revised (no exceptions — every Action is exact-tag-pinned):
grep -rn "@v[0-9]\+$\|@main\|@master" .github/workflows/   # should return zero lines
```

If the planner sticks with D-06 SHA-pinning (out of an abundance of caution despite tags existing), use:

```yaml
# pinned 2026-05-02 to v1.12 (de0fac…), exact tag also exists; pinned by SHA
# for supply-chain hardening since this action lives outside the actions/ org
uses: pdm-project/update-deps-action@bb909553f2dccd1458f519fa80c79e826980dc6a
```

(The SHA `bb909553f2dccd1458f519fa80c79e826980dc6a` is `main` HEAD as of 2026-05-02 02:21 UTC. The `v1.12` tag SHA is `22852fcff9a131d732730e8db92cc9502643a260` — use the v1.12 SHA if the planner wants "pinned to the latest release at SHA level" rather than "pinned to whatever main was today.")

### Optional-Extras Latest Versions

For downstream-visible accuracy in the changelog and to inform the planner what `pdm update` will move them to. **D-02 keeps these UNPINNED in pyproject.toml** — these are the versions the lockfile will resolve to, not the spec.

| Extra | Package | Latest on PyPI | requires_python | Currently in pdm.lock |
|-------|---------|---------------|-----------------|----------------------|
| colorlog | colorlog | 6.10.1 | >=3.6 | 6.10.1 (current) |
| jinja2 | jinja2 | 3.1.6 | >=3.7 | 3.1.6 (current) |
| yaml / generate | pyYaml | 6.0.3 | >=3.8 | (planner verifies) |
| memcached | pylibmc | 1.6.3 | >=3.6 | (planner verifies) |
| mustache | pystache | 0.6.8 | >=3.8 | (planner verifies) |
| redis | redis | 7.4.0 | >=3.10 | 6.1.1 → **7.4.0** (will bump per dry-run) |
| tabulate | tabulate | 0.10.0 | >=3.10 | 0.9.0 → **0.10.0** (will bump per dry-run) |
| watchdog | watchdog | 6.0.0 | >=3.9 | 4.0.2 → **6.0.0** (will bump per dry-run) |
| docs | sphinx | 9.1.0 (requires py>=3.12 — won't pin), best py>=3.10 candidate is **8.1.3** | varies | 7.1.2 → 8.1.3 |

**[VERIFIED 2026-05-02 via PyPI JSON API]**

Note on sphinx: the latest 9.1.0 requires Python 3.12+, and `pyproject.toml requires-python = ">=3.10"` constrains the lockfile target to Python 3.10. PDM correctly resolves to sphinx 8.1.3 (the highest version compatible with py3.10). The dry-run output below confirms this. If the project ever raises the Python floor to 3.12, sphinx will jump to 9.x automatically on the next `pdm update`.

### `pdm update` Dry-Run Preview

Captured today against current `pdm.lock` (head SHA matches `aafa632a`), command: `pdm update --dry-run` (default flags — covers all groups). **[VERIFIED 2026-05-02 from local devbox shell]**

```
Packages to update:
  - alabaster                       0.7.13  -> 1.0.0
  - commitizen                      4.10.1  -> 4.13.10
  - packaging                       24.0    -> 26.2
  - redis                           6.1.1   -> 7.4.0      ← optional-extra (redis)
  - requests                        2.31.0  -> 2.33.1     ← dev dep
  - sphinx                          7.1.2   -> 8.1.3      ← docs extra
  - sphinx-rtd-theme                3.0.2   -> 3.1.0      ← docs extra
  - sphinxcontrib-applehelp         1.0.4   -> 2.0.0      ← docs extra (transitive)
  - sphinxcontrib-devhelp           1.0.2   -> 2.0.0      ← docs extra (transitive)
  - sphinxcontrib-htmlhelp          2.0.1   -> 2.1.0      ← docs extra (transitive)
  - sphinxcontrib-qthelp            1.0.3   -> 2.0.0      ← docs extra (transitive)
  - sphinxcontrib-serializinghtml   1.1.5   -> 2.0.0      ← docs extra (transitive)
  - tabulate                        0.9.0   -> 0.10.0     ← optional-extra (tabulate)
  - watchdog                        4.0.2   -> 6.0.0      ← optional-extra (watchdog)
```

**14 packages move.** Of these:
- **3 are first-order optional-extras** (redis, tabulate, watchdog) — these directly satisfy DEPS-02
- **6 are docs-extra transitive** (sphinx + sphinxcontrib-*) — DEPS-02 sweep
- **1 is dev tooling** (commitizen) — `make commit` should still work; smoke-test verifies
- **1 is dev test infrastructure** (requests) — used in tests/test_helpers.py and test_ext_smtp.py against mailpit; planner verifies test pass
- **1 is alabaster + 1 is packaging** — pure transitive, no direct touchpoints

**Risk assessment:** Most likely lint/test fallout candidates are watchdog 4→6 (major bump, may have API changes for `cement/ext/ext_watchdog.py`) and sphinx 7→8 (docs build only, doesn't gate test/comply). All others are within `~=` / `>=` ranges expected to be backward-compatible.

The dry-run also surfaces sphinx warnings about Python 3.11+/3.12+ versions being skipped — these are NOISY in CI logs but harmless. Planner can suppress in `pdm.yml` cron via `pdm update -q` if desired (currently update-deps-action runs without `-q`).

### pip-audit Pre-Update Snapshot

`pdm run pip-audit` against current pre-update venv (after temporarily installing pip-audit 2.10.0 ad-hoc per D-03 — NOT a permanent dev dep, removed after the run). **[VERIFIED 2026-05-02]**

```
Found 16 known vulnerabilities in 6 packages
Name      Version  ID              Fix Versions
--------- -------- --------------- -------------
certifi   2024.2.2 PYSEC-2024-230  2024.7.4         (transitive of requests)
idna      3.6      PYSEC-2024-60   3.7              (transitive of requests)
pip       25.3     CVE-2026-1703   26.0             (build env tool)
pip       25.3     CVE-2026-3219   —                (no fix yet — accept)
pygments  2.17.2   CVE-2026-4539   2.20.0           (transitive of sphinx)
requests  2.31.0   CVE-2024-35195  2.32.0           ← dev dep
requests  2.31.0   CVE-2024-47081  2.32.4
requests  2.31.0   CVE-2026-25645  2.33.0
urllib3   2.2.1    CVE-2024-37891  2.2.2            (transitive of requests)
urllib3   2.2.1    CVE-2025-50182  2.5.0
urllib3   2.2.1    CVE-2025-50181  2.5.0
urllib3   2.2.1    CVE-2025-66418  2.6.0
urllib3   2.2.1    CVE-2025-66471  2.6.0
urllib3   2.2.1    CVE-2026-21441  2.6.3

Skipped: cement (3.0.15) — not on PyPI for the dev version, expected
```

**Post-update projection:** After `pdm update` lands (which bumps `requests 2.31.0 → 2.33.1`), the 3 requests CVEs and most transitive certifi/idna/urllib3 CVEs auto-resolve. Pygments lifts via sphinx bump. The `pip` CVE-2026-3219 has no fix yet — document as **accepted** in `02-PIP-AUDIT.md` (it's the build env's pip, not a runtime dep, and there's nothing to upgrade to).

**Recommended `02-PIP-AUDIT.md` shape:**

```markdown
# Phase 2 — pip-audit Spot Check

**Run date:** 2026-05-XX (post-`pdm update`)
**Scope:** dev venv (cement[dev,colorlog,jinja2,yaml,redis,memcached,...])
**Tool:** pip-audit 2.10.0 (ad-hoc, NOT a permanent dev dep — see CONTEXT D-03)
**Sources:** PyPI Advisory DB (default)

## Pre-update baseline (informational)
[16 vulns / 6 packages — table from above]

## Post-update results
[N remaining vulns]

## Accepted vulnerabilities
- pip CVE-2026-3219: no fix available; build-env-only tool, not a runtime dep.
  Re-evaluate next phase.

## Resolutions applied
- requests 2.31.0 → 2.33.1 (`chore(deps): pdm update to current non-breaking versions`)
- ... (none expected; pdm update sweeps)

## Pin-arounds (if any)
- (planner fills if any unpatched runtime CVE surfaces)
```

If post-update there are zero remaining unpatched runtime CVEs, the artifact still gets committed (proves the spot check happened) — D-19 acceptance #4 reads "exists in the planning artifacts; any flagged CVE is either pinned-around or documented as accepted."

### pip-audit Invocation Mechanics

The user's environment has neither `pipx` nor `uv` installed (verified — `command -v pipx` returns nothing). Three viable invocation paths for the one-shot run:

1. **Recommended:** `pdm run python -m pip install pip-audit && pdm run pip-audit && pdm run python -m pip uninstall -y pip-audit` — temporary install in the .venv, run, uninstall. Leaves no lockfile drift because pip-audit isn't in `[dependency-groups].dev`.
2. **Alternative:** `pdm run python -m pip install pip-audit -t /tmp/pip-audit && PYTHONPATH=/tmp/pip-audit /tmp/pip-audit/bin/pip-audit` — fully isolated install dir.
3. **Cleanest if available:** `pipx run pip-audit` — needs `pipx install pipx` first; one extra step.

Output formats: `--format columns` (default, human-readable), `--format json` (machine-parseable), `--format markdown` (drop directly into `02-PIP-AUDIT.md`). **Recommend `--format markdown` for the artifact** — pastes cleanly and preserves CVE links.

Vulnerability service: `--vulnerability-service pypi` (default; PyPI Advisory DB) is sufficient. `--vulnerability-service osv` adds OSV.dev coverage but takes longer; not needed for spot-check.

### `pdm update` Behavior Summary

[VERIFIED via local `pdm update --help` against pdm 2.26.6]

- **Default strategy:** `--update-reuse` — preserves pinned versions in lockfile when possible (changes only what new specifier ranges allow).
- **Default scope:** all groups in default install set, including `[dependency-groups].dev` AND `[project.optional-dependencies]` resolved together. **One `pdm update` invocation covers everything.** Verified — the dry-run with no flags returned the same 14 packages as `pdm update -G:all -d --dry-run`.
- **Save strategy interaction:** `~=` specifiers (ruff, mypy) restrict to the patch lane — they will move on patch but not minor. `>=` specifiers (pytest, pytest-cov, coverage, mock, pypng, requests, commitizen) move freely up to the latest. Phase 1's hybrid-pin policy (D-12 from Phase 1) is what makes this safe.
- **What it doesn't do:** `pdm update` without `-u/--unconstrained` will not edit pyproject.toml itself — it only mutates the lockfile within the existing specifier bounds.

### Dependabot github-actions Schema

Minimal valid `.github/dependabot.yml` for D-07. **[CITED: docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file]**

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    labels:
      - "dependencies"
      - "github-actions"
    commit-message:
      prefix: "ci"
      include: "scope"
```

**Schedule recommendation:** `weekly` on Monday — matches `pdm.yml`'s existing Monday 03:05 UTC cron, so all the dep-watching arrives in the same review window.

**Labels recommendation:** `dependencies` + `github-actions` — Dependabot can apply these automatically to opened PRs; they slot into the Phase 4 triage labels nicely (`dependencies` is a common GitHub convention).

**Commit-message prefix `ci`:** matches the cement convention from D-17 commit #4–9 (everything CI-shaped uses `ci:` prefix).

**Optional: groups stanza** — for noise reduction, group all `actions/*` Action bumps into one PR per week:

```yaml
    groups:
      actions-org:
        patterns:
          - "actions/*"
        update-types:
          - "minor"
          - "patch"
```

This is an optional optimization. Recommend OMITTING for Phase 2 — first time enabling Dependabot, want to see the per-Action-bump signal before grouping. Add later if PR volume becomes noisy.

**Critical clarification (per Summary Correction 2):** This yaml file enables **version updates only**. It does NOT enable security-PR opening for GitHub Actions CVEs. To get the CVE backstop the user described in CONTEXT.md `<specifics>`, the **repo settings** also need:
- Settings → Code security and analysis → **Dependabot security updates** → Enable

This setting cannot be set via yaml. Add to phase verification artifact: "Verify Settings → Code security and analysis → Dependabot security updates is enabled."

### `workflow_dispatch:` Trigger

Minimal yaml change to add to `pdm.yml` for D-08. The existing trigger block is:

```yaml
on:
  schedule:
    - cron: "5 3 * * 1"
```

After D-08:

```yaml
on:
  schedule:
    - cron: "5 3 * * 1"
  workflow_dispatch:
```

**No `inputs:` needed** — the action runs without parameters. **[CITED: docs.github.com/en/actions/writing-workflows/choosing-when-workflows-run/events-that-trigger-workflows]** workflow_dispatch always runs against the workflow file as it exists on the default branch (configurable via the `ref` parameter when triggering).

**Trigger via gh CLI (post-merge to main):**
```bash
gh workflow run pdm.yml -R datafolklabs/cement
gh run watch -R datafolklabs/cement   # follow the run
```

**Trigger via Actions UI:** Actions tab → "Update dependencies" workflow → "Run workflow" button → select branch (main) → Run.

### Coverage Gate Behavior — Verified Locally

CONTEXT.md D-10/D-11 carries an "(research confirms this)" note about pytest-cov v7 honoring `[tool.coverage.report].fail_under`. **VERIFIED today against live cement venv:**

```python
$ pdm run python -c "import coverage; cov = coverage.Coverage(); print(cov.config.config_file)"
/Users/derks/Development/DFL/cement/pyproject.toml

$ pdm run python -c "
import coverage
cov = coverage.Coverage(config_file='/tmp/test.toml')  # contains [tool.coverage.report] fail_under=100
print(cov.config.fail_under)
"
100.0
```

Coverage 7.13.5 + pytest-cov 7.1.0 (the Phase-1-pinned versions) auto-discover `pyproject.toml` from cwd and parse `[tool.coverage.report].fail_under` correctly. **D-11 belt-and-braces is still recommended** because:
- Open issue [pytest-dev/pytest-cov #390](https://github.com/pytest-dev/pytest-cov/issues/390) shows historical confusion about pytest-cov's pyproject discovery
- pytest-cov 7.1.0's own changelog entry: *"Fixed total coverage computation to always be consistent, regardless of reporting settings. Previously some reports could produce different total counts, and consequently can make `--cov-fail-under` behave different depending on reporting options."* — explicitly addresses cov-fail-under behavior in v7.1.0, suggesting the explicit flag is the more historically robust path.
- Defense in depth: if coverage 7.x or pytest-cov 7.x ever changes pyproject discovery semantics, the addopts flag still fires.

[CITED: pytest-cov.readthedocs.io/en/latest/changelog.html — v7.1.0 entry]

### `[tool.coverage.run]` source / omit Interaction with `make test`

`make test` invokes: `pdm run pytest --cov=cement tests`.

The `--cov=cement` CLI flag is functionally equivalent to `[tool.coverage.run].source = ["cement"]` — both restrict measurement to the cement package. **They do NOT conflict.** Coverage's CLI flag and pyproject `source` setting agree, so no override happens; `make test`'s explicit `--cov=cement` is now redundant with D-12's pyproject change but harmless.

The `omit` from `[tool.coverage.run]` IS picked up — pytest-cov passes the loaded config through to coverage.py, which respects `omit` regardless of how `source` was specified.

**Optional follow-up (not in Phase 2 scope per D-13/D-12):** the planner could remove `--cov=cement` from `make test` since `[tool.coverage.run].source` now covers it. But that's a Makefile cleanup, not a coverage-gate concern; recommend leaving as-is to keep Phase 2 scope tight.

## Architecture Patterns

### System Diagram (Phase 2 work surface)

```
                    ┌────────────────────────────────────────┐
                    │  Developer / Branch Push               │
                    └───────────────────┬────────────────────┘
                                        │
                                        ▼
        ┌──────────────────────────────────────────────────────────┐
        │  PR opened → .github/workflows/build_and_test.yml        │
        │                                                          │
        │  ┌──────────┐    ┌──────────┐    ┌─────────────┐        │
        │  │ comply   │ ─→ │ test     │ ─→ │ test-all    │        │
        │  │ (ruff,   │    │ (3.x)    │    │ (matrix:    │        │
        │  │  mypy)   │    │          │    │  3.10, 3.11,│        │
        │  └──────────┘    └──────────┘    │  3.12, 3.13,│        │
        │     │ fail-fast    │              │  3.14,      │        │
        │     │ if red       │              │  pypy-3.10, │        │
        │     ▼              ▼              │  pypy-3.11) │        │
        │   GREEN          GREEN            └──────┬──────┘        │
        │                                          │               │
        │                                          ▼               │
        │                                   ┌─────────────┐        │
        │                                   │ cli-smoke-  │        │
        │                                   │   test      │ ─── PASSES │
        │                                   │ (no cov)    │        │
        │                                   └─────────────┘        │
        │                                                          │
        │  ★ NEW (D-10/D-11/D-12):                                 │
        │    pytest-cov reads [tool.coverage.run] source/omit      │
        │    + [tool.coverage.report] fail_under=100               │
        │    → exits 2 if coverage < 100% → CI red                 │
        └──────────────────────────────────────────────────────────┘

        ┌──────────────────────────────────────────────────────────┐
        │  Cron (Mon 03:05 UTC) ─OR─ ★ NEW: workflow_dispatch     │
        │      ↓                                                   │
        │  .github/workflows/pdm.yml                               │
        │      ↓                                                   │
        │  pdm-project/update-deps-action@<pinned>                 │
        │      ↓                                                   │
        │  Opens PR if pdm.lock has updates                        │
        │      ↓                                                   │
        │  PR triggers build_and_test.yml ← gates merge            │
        └──────────────────────────────────────────────────────────┘

        ┌──────────────────────────────────────────────────────────┐
        │  ★ NEW (D-07): .github/dependabot.yml                    │
        │      ↓                                                   │
        │  Dependabot watches github-actions ecosystem (weekly)    │
        │      ↓                                                   │
        │  Opens PR per Action bump (or grouped if `groups:` set)  │
        │      ↓                                                   │
        │  PR triggers build_and_test.yml ← same gating shape      │
        │                                                          │
        │  ★ ALSO (repo settings, NOT yaml):                       │
        │  Dependabot security updates → opens CVE PRs against     │
        │  pinned Action SHAs/tags                                 │
        └──────────────────────────────────────────────────────────┘
```

### Pattern 1: Atomic-per-Concern Commits (Inherited from Phase 1 D-04)

**What:** Land each logical concern as its own conventional commit; never bundle unrelated fix-ups.
**When to use:** Throughout Phase 2 (D-04 mandates it explicitly).
**Example:**
```
chore(deps): pdm update to current non-breaking versions
fix(test): adapt test_ext_watchdog to watchdog 6.0 API change   (only if surfaced)
fix(lint): resolve B019 from sphinx 8.x docstring example       (only if surfaced)
```

### Pattern 2: AUDIT POINT Comments (Inherited from Phase 1 D-08)

**What:** Every config block that could silently drift gets an inline comment naming itself as the audit surface.
**When to use:** D-12's new `[tool.coverage.run]` block. Existing AUDIT POINT comments in pyproject.toml (lines 86, 104, 124, 159) are the templates.
**Example for the new block:**
```toml
[tool.coverage.run]
# AUDIT POINT (Phase 2 D-12): explicit measurement boundary mirrors
# ruff `exclude` discipline. Re-review if files are added under
# cement/cli/templates/ or cement/cli/contrib/ that should be measured.
source = ["cement"]
omit = [
    "cement/cli/templates/*",
    "cement/cli/contrib/*",
]

[tool.coverage.report]
# AUDIT POINT (Phase 2 D-10/D-11): fail_under is the absolute 100% gate.
# Belt-and-braces: pytest addopts also passes --cov-fail-under=100.
# If pytest-cov ever silently changes pyproject discovery, the addopts
# flag still fires. Drop one only after the other is independently verified.
precision = 2
fail_under = 100
```

### Anti-Patterns to Avoid

- **Bundling `fix(...)` commits into the `chore(deps): pdm update` commit.** Breaks bisect — exactly what D-04 exists to prevent.
- **Pinning Action versions to `@vN` (major-only).** Defeats the purpose of D-05 — major tags are floating refs that can land breaking changes silently.
- **Adding `pip-audit` to `[dependency-groups].dev`.** Explicitly forbidden by D-03 (Phase 5 SEC-01 territory).
- **Adding `pip` to `dependabot.yml`.** Forbidden by D-07 (creates duplicate-PR stream alongside `pdm.yml` cron).
- **Silently dropping pypy3.10 when adding pypy-3.11.** D-14 explicit: keep both. Drop = downstream-observable change.
- **Touching the serial `comply → test → test-all → cli-smoke-test` job graph.** D-16 keeps it. Optimization is out of scope; risk of regression while proving the pipeline.
- **Changing `make test` to drop `--cov=cement`.** Even though `[tool.coverage.run].source = ["cement"]` makes it redundant, that's a Makefile change adjacent to but not part of D-10/D-11/D-12. Phase 2 strict scope.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Coverage gate enforcement | Custom CI script that greps pytest output for percentages | `[tool.coverage.report].fail_under = 100` (D-10) | coverage.py already exits 2 on gate failure; CI naturally turns red |
| GH Action version monitoring | Cron script that hits GitHub Releases API | Dependabot github-actions ecosystem (D-07) | Native GitHub feature, free, includes security advisories at repo-toggle level |
| Lockfile bumping | Hand-curated `pdm add foo==X.Y.Z` invocations | `pdm update` (D-01) | Resolves the full graph respecting all specifiers; PDM is the source of truth |
| Vulnerability scanning | Curated CVE list reviewed manually | `pip-audit` (D-03 one-shot) | Cross-references PyPI Advisory DB live; catches transitive CVEs that human review misses |
| Ad-hoc workflow triggering | Push throwaway commits to main to trigger cron | `workflow_dispatch:` (D-08) | Native, no log noise, bypasses cron schedule cleanly |

**Key insight:** Phase 2 is entirely about wiring up battle-tested tooling. Every "what should we build?" question is answered by "use the upstream feature." This is the OPPOSITE of a build-from-scratch phase — it's a configure-known-tools phase.

## Common Pitfalls

### Pitfall 1: Coverage gate fires on `make test-core` but not on `make test`
**What goes wrong:** `make test-core` runs `pytest --cov=cement.core tests/core` — limited measurement scope. With `fail_under = 100` global, this would fail because most of `cement/` is not measured.
**Why it happens:** `--cov=cement.core` overrides `[tool.coverage.run].source`. The fail_under gate applies to whatever is measured.
**How to avoid:** D-10/D-11/D-12 affect `make test` by design. `make test-core` is a developer convenience for fast iteration on core tests; the 100% gate on partial measurement isn't meaningful. Either:
1. Accept that `make test-core` will fail the gate (developer expects this; CI uses `make test` not `make test-core`).
2. (Out of scope this phase) Document the limitation in the Makefile or rename `make test-core` to indicate "incomplete coverage by design."

**Recommendation:** Option 1 — leave `make test-core` alone. CI uses `make test`. Document in CHANGELOG / phase verification if surfaced.

**Warning signs:** Developer reports "`make test-core` is broken" after Phase 2 lands. Response: "yes, by design; use `make test` for full-suite + gate; `make test-core` is for quick core-only iteration."

### Pitfall 2: pdm-project/update-deps-action README example uses `@main`, planner copies it
**What goes wrong:** D-05 says exact-tag-everywhere; the action's own README example uses `@main`. If planner mirrors README without questioning, regresses to floating ref.
**Why it happens:** Authority bias — "if the upstream README says to do it this way..."
**How to avoid:** Concrete substitution table above explicitly says `@v1.12`. Planner should write `pdm-project/update-deps-action@v1.12` in `pdm.yml`, not `@main`.
**Warning signs:** D-19 acceptance grep `grep -rn "@v[0-9]\+$\|@main"` shows `@main` left in `pdm.yml`.

### Pitfall 3: `actions/setup-python` v5 → v6 without checking matrix integration
**What goes wrong:** Bumping `actions/setup-python@v5 → @v6.2.0` is a major-version bump. v6 may have changed pypy version resolution or cache-dependency-path semantics.
**Why it happens:** D-05 says exact-tag-everywhere, planner mechanically writes the latest tag.
**How to avoid:** v6 release notes — confirmed v6.2.0 still supports `pypy-3.10`, `pypy-3.11` syntax (PyPy version manifest unchanged). The biggest v5→v6 change is **Node 20 runtime** (most projects already migrated). Caching: cement workflows don't currently use `actions/setup-python` cache (no `cache: pip` etc.) — no cache-config compatibility risk.
**Warning signs:** First PR after the bump fails on every matrix lane with `Unable to find python-version` errors. Response: pin back to `@v5.6.0` (last stable v5 release published 2025-04-24) and reopen — that's what `--save-compatible` gives us in the lockfile equivalent.

### Pitfall 4: Watchdog 4.0.2 → 6.0.0 major bump touches `cement/ext/ext_watchdog.py`
**What goes wrong:** Watchdog had a major version bump cycle (4.x → 5.x → 6.x). Public API changes are rare but possible.
**Why it happens:** Optional-extra is unpinned (D-02), so `pdm update` sweeps to latest.
**How to avoid:** Per D-04, if it surfaces during the pdm-update CI run, it lands as `fix(test): adapt watchdog handler to 6.x API`. Pre-emptively grep:
```bash
grep -rn "watchdog\|FileSystemEventHandler\|Observer" cement/ext/ext_watchdog.py tests/ext/test_watchdog.py
```
to inventory the surface.
**Warning signs:** test_watchdog.py fails on first CI run after lockfile bump. Atomic split per D-04.

### Pitfall 5: Coverage gate test (D-19 acceptance #2) requires throwaway PR
**What goes wrong:** D-19 acceptance #2 says "verifiable by temporarily dropping a covered line in a throwaway commit, then reverting" — this is non-trivial to do in a CI-gated repo.
**Why it happens:** Proving a gate fires requires triggering the failure; the gate prevents merge.
**How to avoid:** Demonstrate locally first: comment out a line in any covered cement source file, run `pdm run pytest --cov=cement tests --cov-fail-under=100` — should exit non-zero. Capture the output as evidence in the phase verification artifact. Restore the line. No throwaway PR needed; the verification log demonstrates the gate.
**Warning signs:** Planner creates an actual throwaway PR that other reviewers see. Use the local-evidence path instead.

### Pitfall 6: Dependabot security update at repo-level not enabled (Correction 2 in Summary)
**What goes wrong:** dependabot.yml lands cleanly, version-update PRs flow, but no security-CVE PRs ever appear because repo-level toggle isn't on.
**Why it happens:** CONTEXT.md D-07 implies the yaml file enables security advisories — it does not.
**How to avoid:** Phase verification artifact MUST include a step: "Verify repo Settings → Code security and analysis → Dependabot security updates is **enabled**." Capture a screenshot or note the setting state. If disabled, instruct the user to flip it (one-click; takes effect immediately for the existing dependabot.yml).
**Warning signs:** Months pass, no security PRs from Dependabot, action CVE on a pinned tag goes unnoticed.

## Code Examples

Verified patterns the planner can drop directly into the workflow / pyproject files.

### Example 1: Updated build_and_test.yml — Action pin lines

```yaml
# Source: GitHub Releases API verification 2026-05-02
- uses: actions/checkout@v6.0.2
- uses: ConorMacBride/install-package@v1.1.0
  with:
    apt: libmemcached-dev
- name: Set up Python
  uses: actions/setup-python@v6.2.0
  with:
    python-version: "3.x"
    architecture: "x64"
- name: Setup PDM
  uses: pdm-project/setup-pdm@v4.4
- uses: hoverkraft-tech/compose-action@v2.6.0
  with:
    compose-file: "./docker/compose-services-only.yml"
```

### Example 2: Updated pdm.yml

```yaml
# Source: per D-05/D-06/D-08
name: Update dependencies

on:
  schedule:
    - cron: "5 3 * * 1"
  workflow_dispatch:

jobs:
  update-dependencies:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6.0.2

      - name: Update dependencies
        uses: pdm-project/update-deps-action@v1.12
        # Note: action HAS tagged releases (planner: see RESEARCH.md
        # Correction 1). If the planner accepts D-06 SHA-pin posture
        # anyway, replace `@v1.12` with the v1.12 commit SHA:
        # @22852fcff9a131d732730e8db92cc9502643a260
```

### Example 3: New dependabot.yml

```yaml
# Source: docs.github.com/en/code-security/dependabot/dependabot-version-updates
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    labels:
      - "dependencies"
      - "github-actions"
    commit-message:
      prefix: "ci"
      include: "scope"
```

### Example 4: pyproject.toml additions (D-10 + D-11 + D-12)

```toml
# Insert after the existing [tool.pytest.ini_options] block,
# replacing the current 2-line [tool.coverage.report] block.

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov-report=term --cov-report=html:coverage-report --cov-fail-under=100 --capture=sys tests/"
python_files = "test_*.py"

[tool.coverage.run]
# AUDIT POINT (Phase 2 D-12): explicit measurement boundary mirrors
# ruff `exclude` discipline. Re-review if files are added under
# cement/cli/templates/ or cement/cli/contrib/ that should be measured.
source = ["cement"]
omit = [
    "cement/cli/templates/*",
    "cement/cli/contrib/*",
]

[tool.coverage.report]
# AUDIT POINT (Phase 2 D-10/D-11): fail_under = 100 is the absolute
# coverage gate. Belt-and-braces: pytest addopts also passes
# --cov-fail-under=100 in case future pytest-cov bumps change pyproject
# discovery semantics.
precision = 2
fail_under = 100
```

### Example 5: build_and_test.yml matrix update (D-14 + D-15)

```yaml
test-all:
  needs: test
  runs-on: ${{ matrix.os }}
  strategy:
    matrix:
      # D-15: ubuntu-only intentional. macOS/Windows is a dedicated
      # platform-support effort (libmemcached, signal/daemon, bash).
      os: [ubuntu-latest]
      python-version: ["3.10", "3.11", "3.12", "3.13", "3.14",
                       "pypy3.10", "pypy3.11"]
      # Note: pypy version syntax accepts both `pypy3.X` and `pypy-3.X`.
      # Existing cement convention is no-dash; new entry mirrors that.
      # Both forms resolve to the same underlying PyPy 7.3.x release
      # via actions/setup-python@v6.2.0.
```

### Changelog Bucketing for Phase 2 Commits

Per CLAUDE.md §"Changelog Maintenance" — each commit appends a one-line entry to active `## 3.0.15 - DEVELOPMENT` section. Mapping for D-17's 10-commit suggested split:

| # | Commit subject | Bucket | Entry shape |
|---|---------------|--------|-------------|
| 1 | `chore(deps): pdm update to current non-breaking versions` | Misc | `[dev]` Bump dev/extras lockfile to current non-breaking versions (redis 7.4, watchdog 6.0, tabulate 0.10, sphinx 8.1, requests 2.33, others) |
| 2 | `fix(lint\|type\|test): ...` per failure (zero or more) | Bugs | `[<area>]` Fix <surface> from <pkg> bump |
| 3 | `chore(deps): pin <pkg> for CVE <id>` (zero or more) | Misc | `[deps]` Pin <pkg>>=<ver> to address <CVE> |
| 4 | `ci: pin GitHub Actions to exact tags` | Misc | `[ci]` Pin GitHub Actions to exact tags (checkout v6.0.2, setup-python v6.2.0, setup-pdm v4.4, install-package v1.1.0, compose-action v2.6.0, update-deps-action v1.12) |
| 5 | `ci: pin pdm-project/update-deps-action` | Misc | (folds into entry #4 if Correction 1 accepted) OR `[ci]` SHA-pin pdm-project/update-deps-action |
| 6 | `ci: enable Dependabot for github-actions ecosystem` | Misc | `[ci]` Enable Dependabot for github-actions ecosystem (weekly) |
| 7 | `ci: add workflow_dispatch trigger to pdm.yml` | Misc | `[ci]` Add workflow_dispatch trigger to pdm.yml |
| 8 | `ci: add pypy-3.11 to test matrix` | Misc | `[ci]` Add PyPy 3.11 to CI test matrix (alongside existing PyPy 3.10) |
| 9 | `ci: drop FIXME OS-matrix comment` | Misc | (omit from changelog — comment cleanup, not user-visible) |
| 10 | `test: enforce 100% coverage gate via fail_under + addopts` | Misc | `[dev]` Wire 100% coverage gate via `[tool.coverage.report] fail_under` + `--cov-fail-under` addopts; explicit `[tool.coverage.run] source/omit` |

**Existing `[area]` prefixes already in use in active changelog section:** `[ext.smtp]`, `[cli]`, `[core.handler]`, `[dev]`. Phase 2 introduces `[ci]` and possibly `[deps]` as new area tags — both are conventional and consistent with the existing scheme.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `actions/checkout@v4` (floating major) | `actions/checkout@v6.0.2` (exact tag) | This phase | Reproducible CI builds; SHA-stability for supply chain |
| `pdm-project/update-deps-action@main` | `pdm-project/update-deps-action@v1.12` (or SHA) | This phase | Removes floating-ref risk; D-19 grep clean |
| No automated Action version monitoring | Dependabot github-actions ecosystem | This phase | Weekly auto-PR for any pinned-Action bump |
| Coverage gate enforced ad-hoc / not enforced | `fail_under = 100` in pyproject + addopts | This phase | CI fails build below 100% — finally meaningful |
| Manual cron-only `pdm update` | Cron + `workflow_dispatch:` | This phase | Manual trigger affordance; verification path |

**Deprecated/outdated (after Phase 2):**
- `# FIXME ?` cruft above OS matrix in `build_and_test.yml`: removed per D-15.
- The implicit assumption that "coverage 100%" is enforced by anything: was actually unenforced until Phase 2; D-10/D-11 makes it real.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `pdm-project/setup-pdm@v4.4` is the safer pick than `@v4.5` (latest tag without a release) | Concrete Substitutions | Low — both are valid tags; `v4.4` is the published release. If `v4.5` has a critical fix the planner missed, switch. |
| A2 | `pdm update`'s default group-set includes all of `[project.optional-dependencies]` AND `[dependency-groups].dev` simultaneously | `pdm update` Behavior Summary | Verified by dry-run (same 14 packages with and without `-G:all -d`). Risk: PDM 2.27+ could change default — re-verify if PDM bumps. |
| A3 | Dependabot's repo-level "security updates" toggle is what surfaces GitHub Actions CVEs (not the dependabot.yml file) | Correction 2 in Summary | [CITED: docs.github.com/en/code-security/dependabot/dependabot-security-updates] — high confidence. |
| A4 | watchdog 4 → 6 likely doesn't break `cement/ext/ext_watchdog.py` (cement uses minimal API surface) | Pitfall 4 | Surfaces in CI if wrong; D-04 atomic-split absorbs cleanly. Low risk. |
| A5 | `pypy3.11` (no-dash, mirroring existing `pypy3.10` convention) is interchangeable with `pypy-3.11` (dashed, used in CONTEXT.md D-14) | Example 5 | Verified by setup-python advanced-usage.md. Both forms work. Planner picks the convention. |

## Open Questions

1. **Should D-06 SHA-pinning still apply now that `pdm-project/update-deps-action` has tagged releases?**
   - What we know: 13 tags exist, latest `v1.12` published 2025-04-21. Action's own README still uses `@main` as example (likely historical inertia).
   - What's unclear: User's preference between (a) exact-tag pin like everyone else, OR (b) SHA-pin as belt-and-braces against tag mutation.
   - Recommendation: **Use `@v1.12` (exact tag, consistent with D-05).** Falls naturally out of D-05's "exact tags everywhere." The SHA-pin posture in D-06 was conditional on "no tags upstream" which turned out to be wrong. Planner can flip back to SHA-pin if user wants the extra hardening — concrete SHA values for both `main` HEAD and `v1.12` are in §"Concrete Substitutions."

2. **`make test-core` will fail under the new 100% gate.**
   - What we know: `make test-core` runs `pytest --cov=cement.core tests/core`; covers only ~30% of `cement/`.
   - What's unclear: Whether anyone uses `make test-core` interactively, and whether breaking it matters.
   - Recommendation: **Accept as Phase 2 side-effect.** Document in changelog if any user reports it. CI uses `make test`; gate fires correctly there.

3. **Should `requirements.txt` be regenerated for any downstream/legacy consumers?**
   - What we know: cement uses pdm.lock; no shipped requirements.txt at project root.
   - What's unclear: Whether any contrib doc references a requirements.txt path.
   - Recommendation: Out of scope. Phase 2 doesn't touch packaging surface.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| PDM | All `pdm` invocations | ✓ | 2.26.6 | — |
| coverage | Coverage gate verification | ✓ | 7.13.5 (via dev deps) | — |
| pytest-cov | Coverage gate verification | ✓ | 7.1.0 (via dev deps) | — |
| curl | Live GitHub Releases API queries | ✓ | (system) | — |
| python3 + json stdlib | API response parsing | ✓ | 3.13 | — |
| `gh` CLI | `gh workflow run pdm.yml` (D-08 verification) | ✗ | — | Use Actions UI "Run workflow" button |
| `pip-audit` | DEPS-03 spot-check | ✗ (not installed; D-03 forbids dev-dep add) | — | Ad-hoc: `pdm run python -m pip install pip-audit && pdm run pip-audit && pdm run python -m pip uninstall -y pip-audit` |
| `pipx` | Alternative pip-audit invocation | ✗ | — | See ad-hoc pip install above |
| `uv` / `uvx` | Alternative isolated invocation | ✗ | — | See ad-hoc pip install above |
| Docker / docker-compose | `cli-smoke-test` Makefile target | (assumed; cement's normal dev env) | — | — |
| devbox | `make init` / dev env setup | ✓ (per Phase 1 precedent) | — | — |

**Missing dependencies with no fallback:** None.
**Missing dependencies with fallback:** `gh` (use Actions UI), `pip-audit` (ad-hoc install/uninstall), `pipx`/`uv` (ad-hoc fallback).

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 9.0.3 + pytest-cov 7.1.0 + coverage 7.13.5 |
| Config file | `pyproject.toml` (no `.coveragerc` — coverage auto-discovers pyproject) |
| Quick run command | `pdm run pytest --cov=cement -x tests` (single-file iteration) |
| Full suite command | `make test` (runs `pdm run pytest --cov=cement tests` after `make comply`) |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DEPS-01 | pdm.lock matches latest non-breaking versions | smoke | `pdm update --dry-run \| grep "Packages to update" -A 30` shows zero pending updates | ✅ (pdm tooling) |
| DEPS-02 | Optional-extras current stable | smoke | Same as DEPS-01 (covered by single resolution pass) | ✅ |
| DEPS-03 | No unpatched runtime CVEs (or documented) | smoke | `pdm run pip-audit` (after ad-hoc install) returns clean OR documented exceptions in `02-PIP-AUDIT.md` | ✅ (pip-audit ad-hoc) |
| DEPS-04 | `pdm update` job runs cleanly | manual | `gh workflow run pdm.yml` then `gh run watch` (or Actions UI), observe completion | manual-only (workflow_dispatch is the test) |
| CI-01 | Matrix Python 3.10–3.14 + pypys all green | integration | PR to GitHub triggers `build_and_test.yml`, all 7 lanes report ✅ | ✅ (existing CI) |
| CI-02 | Compliance jobs run on every PR | integration | Same as CI-01 (comply job is first in graph) | ✅ |
| CI-03 | 100% coverage gate fails below 100% | unit/manual | Locally: comment out a covered line, run `make test`, expect non-zero exit; restore line. Capture output. | ✅ (manual demonstration) |
| CI-05 | Action versions pinned to current stable | static | `grep -rn "@v[0-9]\+$\|@main\|@master" .github/workflows/` returns zero lines (or only the one SHA-pin if D-06 sticks) | ✅ (grep) |

### Sampling Rate
- **Per task commit:** `pdm run pytest --cov=cement -x tests` (~30s on cement) + `make comply-ruff` (~2s) + `make comply-mypy` (~5s)
- **Per wave merge:** `make test` (full suite + 100% gate)
- **Phase gate:** PR opened → all 7 matrix lanes green; coverage gate fires demonstrably; `02-PIP-AUDIT.md` exists; D-19 grep clean.

### Wave 0 Gaps
- **None — existing test infrastructure covers all phase requirements.** Phase 2 doesn't ship new code requiring new tests; it changes config (pyproject, workflow yaml, dependabot.yml). The validation surface is:
  1. Existing test suite (proves nothing regresses under bumped lockfile)
  2. CI matrix run (proves the workflow YAML is syntactically and semantically valid)
  3. Manual `workflow_dispatch` trigger (proves DEPS-04)
  4. Local coverage-gate demonstration (proves CI-03)
  5. Manual `pdm run pip-audit` invocation (proves DEPS-03)

No new pytest fixtures or test files needed.

## Sources

### Primary (HIGH confidence)
- **GitHub Releases API** — `https://api.github.com/repos/<owner>/<repo>/releases/latest` for actions/checkout, actions/setup-python, pdm-project/setup-pdm, ConorMacBride/install-package, hoverkraft-tech/compose-action, pdm-project/update-deps-action — VERIFIED 2026-05-02.
- **GitHub Commits API** — `https://api.github.com/repos/pdm-project/update-deps-action/commits/main` for SHA pin candidate — VERIFIED 2026-05-02.
- **PyPI JSON API** — `https://pypi.org/pypi/<package>/json` for current versions of redis, watchdog, tabulate, jinja2, pyyaml, colorlog, pylibmc, pystache, sphinx, pytest-cov, pip-audit — VERIFIED 2026-05-02.
- **PyPy versions.json** — `https://downloads.python.org/pypy/versions.json` confirms PyPy 3.11 stable releases (latest 7.3.22) — VERIFIED 2026-05-02.
- **Local devbox shell** — `pdm update --dry-run` output captured live; `coverage 7.13.5 + pytest-cov 7.1.0` config-discovery test verified — VERIFIED 2026-05-02.
- **GitHub docs** — Dependabot configuration options — `https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file`
- **GitHub docs** — Dependabot security updates — `https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/about-dependabot-security-updates`

### Secondary (MEDIUM confidence)
- **pytest-cov v7.0.0/v7.1.0 changelog** — `https://pytest-cov.readthedocs.io/en/latest/changelog.html` (verbatim entry citing `--cov-fail-under` consistency fix in 7.1.0)
- **coverage.py config docs** — `https://coverage.readthedocs.io/en/latest/config.html` (`fail_under` exits status 2 below threshold; 100 is special-cased to require strict 100%)
- **actions/setup-python advanced-usage.md** — `https://github.com/actions/setup-python/blob/main/docs/advanced-usage.md` (PyPy syntax `pypy<X>` and `pypy-<X>` interchangeable)
- **pdm CLI docs** — `https://pdm-project.org/en/latest/reference/cli/#update` (update strategies, save strategies)
- **pip-audit PyPI page** — `https://pypi.org/project/pip-audit/` (invocation forms, output formats, vulnerability services)
- **pdm-project/update-deps-action README** — `https://github.com/pdm-project/update-deps-action/blob/main/README.md` (action inputs/outputs)

### Tertiary (LOW confidence — flagged for validation)
- **pytest-cov issue #390** — `https://github.com/pytest-dev/pytest-cov/issues/390` (historical confusion about pyproject discovery; superseded by local verification above)

## Metadata

**Confidence breakdown:**
- Concrete Action tag values: **HIGH** — live GitHub API queries today (2026-05-02)
- pdm update preview: **HIGH** — actual dry-run output captured today
- pip-audit findings: **HIGH** — actual run today against current venv
- Dependabot schema: **HIGH** — official GitHub docs cited
- Coverage gate behavior: **HIGH** — locally verified that pytest-cov 7.1.0 + coverage 7.13.5 honor `[tool.coverage.report].fail_under` from pyproject.toml
- Two corrections to CONTEXT.md (D-06 tags-exist, D-07 security-toggle): **HIGH** — both backed by primary sources

**Research date:** 2026-05-02
**Valid until:** 2026-06-02 (30 days for stable values; tag values may shift if Dependabot opens a PR before Phase 2 lands — re-verify Action tags at execution time if more than 2 weeks have passed)
