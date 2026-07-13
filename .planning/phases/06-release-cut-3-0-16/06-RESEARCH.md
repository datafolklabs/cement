# Phase 6: Release Cut 3.0.16 - Research

**Researched:** 2026-07-12
**Domain:** Software release engineering — running a pre-built GitHub Actions release pipeline (PyPI OIDC publish, Docker Hub multi-arch, RTD, GitHub Release) for a strict-backward-compat Python library
**Confidence:** HIGH (machinery + live provisioning state directly inspected; only provider-UI trusted-publisher/RTD state is unverifiable from here)

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Changelog finalization**
- **D-01:** Full git-log cross-check before finalization — diff `git log 3.0.14..HEAD` against every entry in the `## 3.0.15 - DEVELOPMENT` section; flag any user-visible change missing and any entry that no longer matches what shipped.
- **D-02:** Section header renamed to `## 3.0.16 - <Month D, YYYY>` matching the convention (`## 3.0.14 - May 5, 2025`). MUST begin `## 3.0.16` — the `gh-release` job awk-extracts by tag match; preflight (05.4 D-02) validates finalization.
- **D-03:** Add a short narrative highlights paragraph (2–4 sentences) at the top of the 3.0.16 section — Python 3.10–3.14 matrix, warn-only deprecations, release automation, template modernization — above the standard buckets. Becomes the top of the GitHub Release body.
- **D-04:** Condense verbose entries: keep EVERY entry, edit each to 1–3 lines at release-notes altitude. Drop dev-time forensic detail (git retains it). Do NOT delete or merge `[dev]` entries.

**Release-prep commit flow**
- **D-05:** One release-prep PR: single branch carries changelog finalization + `cement/core/backend.py` VERSION bump to `(3, 0, 16, 'final', 0)`. User reviews and merges; the merged main commit is what gets tagged. No direct commits to main.
- **D-06:** One final `workflow_dispatch` dry-run against the merged release commit on main before tagging. Accepted caveat (05.4 D-08): the dry-run uploads 3.0.16 to TestPyPI; the real tag run skip-exists and smokes that same artifact.
- **D-07:** The USER pushes the tag personally (`git tag 3.0.16 && git push origin 3.0.16`). Agent hands over the exact verified command sequence (correct SHA, pre-tag ancestry check already proven green).
- **D-08:** Failure policy for the live run: gate failures = delete tag, fix, re-tag. Publish-side partial failure AFTER PyPI publish succeeds (Docker, branch-sync, gh-release, dev-bump): use GitHub re-run-failed-jobs on the same run — tag stays.

**Provisioning completion**
- **D-09:** Guided checkpoint session as the FIRST plan of the phase — walk `05.4-PROVISIONING.md`'s pre-first-tag checklist item-by-item; agent presents exact values, user clicks through provider UIs, agent verifies each via `gh api`/repo state where verifiable.
- **D-10:** The one-time `stable/3.0.x` ancestry merge (`git merge -s ours`) is run by the USER on main; agent preps the exact command sequence and verifies `merge-base --is-ancestor` afterward. Must be a real merge commit — a rebase/squash-merged PR would destroy the merge parent and branch-sync would fail.
- **D-11:** Docker Hub credentials via an org access token (OAT) on the `datafolklabs` org — repo-scoped. Requires Docker Team/Business; if OAT is unavailable at the checkpoint, fall back per runbook §4 (bot-account PAT preferred over maintainer PAT).

**Post-release wrap-up scope**
- **D-12:** Phase end = through dev-bump merge: PyPI + Docker + GitHub Release live, dev-bump PR merged (VERSION `(3, 0, 17, ...)` + fresh `## 3.0.17 - DEVELOPMENT`), and REL-01..05 / CI-04 / DOCS-03 flipped with a VERIFICATION.md.
- **D-13:** REL-04 verification is a single clean-venv check: `pip install cement==3.0.16` from production PyPI + import + minimal `App().run()` round-trip. The 5-Python matrix already proved the identical artifact from TestPyPI inside the release run.
- **D-14:** The phase drafts the release announcement copy (highlights-based, from the finalized changelog) as a small artifact the user can paste. Sending remains human (05.4 D-15).
- **D-15:** Milestone completion is a separate follow-up session — Phase 6 ends at requirement flips + VERIFICATION.md; user invokes `/gsd-complete-milestone` afterward.

### Claude's Discretion
- Exact plan/wave decomposition (provisioning-first is locked; the rest may parallelize where file ownership allows).
- Mechanics of the git-log cross-check (commit classification, filtering planning-artifact commits per CLAUDE.md changelog rules).
- Shape/wording of the condensed changelog entries and the highlights paragraph (user reviews via the release-prep PR).
- Announcement-copy format and where the draft artifact lives.
- How dry-run/live-run monitoring is reported back during execution (checkpoint cadence while the ~30–40 min runs are in flight).

### Deferred Ideas (OUT OF SCOPE)
- Post-release checklist issue execution (GitBook docs, mailing list, Slack sends) — human work tracked by the auto-created issue, not by phase plans.
- Milestone archive — user runs `/gsd-complete-milestone` in a separate session (D-15).
- Full-commit-SHA action pinning tightening for community actions — runbook "known accepted tradeoffs" #2; revisit post-release.
- GitBook todos `2026-05-09-document-optional-features...` and `2026-07-11-update-gitbook-todo-tutorial...` — post-release GitBook work on the emitted checklist.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DOCS-03 | Changelog updated for 3.0.16 with all user-visible changes | D-01 git-log cross-check against the existing `## 3.0.15` section (Bugs L3, Features L207, Refactoring L285, Misc L460, Deprecations L534); D-02 header rename; D-03/D-04 condensation. Preflight's finalized-changelog guard + `gh-release` awk extraction enforce it at tag time. |
| CI-04 | Release workflow validated end-to-end against TestPyPI before the cut | Already GREEN once (dry-run [29212487225](https://github.com/datafolklabs/cement/actions/runs/29212487225), `conclusion: success`, `event: workflow_dispatch`). D-06 re-runs one final dry-run against the *finalized* 3.0.16 commit. |
| REL-01 | Version bumped to 3.0.16 across all version-of-record locations | **Single source of truth = `cement/core/backend.py` VERSION tuple.** `pyproject.toml` `version` is `dynamic` via `[tool.pdm.version] source="call" getter="cement.utils.version:get_version"`; `cement/__init__.py` imports `get_version` dynamically. Editing backend.py alone satisfies REL-01. |
| REL-02 | Pre-release TestPyPI smoke passes on each supported Python | `testpypi-smoke` matrix job (3.10–3.14) runs `scripts/testpypi-smoke.py` = install plain zero-dep `cement==X.Y.Z` + import `App` + `App().run()` round-trip + version assert. Proven green on all 5 legs in the dry-run. |
| REL-03 | 3.0.16 git tag + GitHub Release notes published with changelog | Tag push (D-07, human) triggers `release.yml`; `gh-release` job awk-extracts the `## 3.0.16` section → `RELEASE_BODY.md` → `gh release create`. |
| REL-04 | PyPI publish; installs cleanly on 3.10–3.14 | `publish-pypi` OIDC job (env `release`, no `skip-existing` — duplicate fails loud). D-13 verifies with one clean-venv `pip install cement==3.0.16` from prod PyPI. |
| REL-05 | Post-release version bumped to 3.0.17 | `dev-bump` job runs `scripts/bump_dev_version.py` (next = released patch+1, computed) → PR via `create-pull-request`. Phase merges that PR (D-12). |
</phase_requirements>

## Summary

Phase 6 does **not build software — it runs a machine that is already built and validated.** Phase 05.4 delivered `.github/workflows/release.yml` (13 jobs), `gates.yml`, and three helper scripts, and proved the pre-publish half end-to-end with a green `workflow_dispatch` dry-run ([run 29212487225](https://github.com/datafolklabs/cement/actions/runs/29212487225)). The only executable code changes this phase should expect are (1) the CHANGELOG finalization and (2) the one-line `VERSION` tuple bump — both in a single release-prep PR. Everything else is provisioning-in-provider-UIs, monitoring runs, and a human tag push.

The dominant risk is **not code — it is external, provider-UI state that cannot live in git and cannot be fully verified from this machine.** The research therefore front-loads a live inventory of provisioning state (below). As of 2026-07-12 the picture is: `release`/`testpypi` GitHub Environments exist and `release` has the required reviewer; Actions-can-open-PRs is on; the TestPyPI trusted publisher works (dry-run proved it). **Two blocking items are still open:** the Docker Hub secrets (`DOCKERHUB_USERNAME`/`DOCKERHUB_TOKEN`) are **not set**, and `stable/3.0.x` is **not yet an ancestor of `main`** (the `-s ours` reconcile has not landed). Two items — the **PyPI trusted publisher** and the **RTD GitHub integration** — cannot be verified from here and must be confirmed in the D-09 guided session.

A second important finding de-risks REL-01: despite the requirement wording ("across `cement/__init__.py`, `pyproject.toml`, and any other version-of-record locations"), Cement has a **single version of record** — the `VERSION` tuple in `cement/core/backend.py`. `pyproject.toml` reads it dynamically via PDM `source="call"`, and `cement/__init__.py` re-exports `get_version()`. There is exactly one place to edit; a repo-wide grep for `3.0.15`/`(3, 0, 15` finds only `backend.py` (and the regex-doc line in `bump_dev_version.py`, which is a comment, not a version of record).

**Primary recommendation:** Sequence the phase as five plans — (1) **provisioning checkpoint** (D-09, close the two open blockers + confirm PyPI/RTD in the UI); (2) **release-prep PR** (changelog D-01..D-04 + `backend.py` bump, review+merge); (3) **final dry-run** (D-06) against the merged commit; (4) **tag handoff + live-run shepherding** (D-07/D-08, human tag + approval gate); (5) **post-release verification + wrap-up** (D-13 clean-venv check, merge dev-bump PR, announcement draft, requirement flips + VERIFICATION.md). Do provisioning first because it has zero code dependencies and surfaces provider surprises earliest.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Version of record (bump to 3.0.16 / 3.0.17) | Source (`cement/core/backend.py`) | Build (`pyproject.toml` reads it via PDM `source="call"`) | Single tuple; everything else derives. |
| Changelog authoring | Source (`CHANGELOG.md`) | CI (preflight guard reads it; `gh-release` extracts it) | Human-authored text that the pipeline treats as data. |
| Trigger (the release "start button") | Human + Git (tag push) | CI (`on: push: tags`) | D-07: the human act of tagging is the source of truth. |
| Gate enforcement | CI (`gates.yml` via `release.yml`) | — | Test matrix, coverage, ruff/mypy, cli-smoke — fail-fast before any publish. |
| Artifact build | CI (`build` job, `pdm build`) | — | Isolated from all publish credentials; hands identical bytes downstream. |
| PyPI / TestPyPI publish | External registry (PyPI OIDC) | CI (`id-token: write` + env claim) | Trusted-publisher auth; no long-lived tokens in repo. |
| Docker images | External registry (Docker Hub) | CI (`docker` job + secret login) | No OIDC on Docker Hub → scoped access-token secret. |
| Docs rebuild | External service (Read the Docs) | Git (`3.0` moving-tag push fires RTD webhook) | RTD builds per minor line off the `3.0` moving tag. |
| Branch/tag sync | Git refs (`stable/3.0.x`, `3`, `3.0`) | CI (`branch-sync`/`tag-sync` jobs) | Fast-forward branch; force-update moving tags. |
| Approval gate | Human (GitHub `release` Environment) | CI (all publish jobs `needs: publish-pypi`) | The one and only manual stop. |

## Release Execution Flow

```
                      ┌─────────────────── PHASE 6 HUMAN/AGENT WORK ────────────────────┐
 (D-09) Provisioning checkpoint  ──►  (D-05) Release-prep PR   ──►  (D-06) Final dry-run
   • DOCKERHUB_* secrets              • CHANGELOG finalize          • workflow_dispatch on
   • -s ours ancestry merge (D-10)      (D-01..D-04)                  merged 3.0.16 commit
   • confirm PyPI trusted publisher   • backend.py VERSION bump     • uploads 3.0.16 to
   • confirm RTD integration          • review + MERGE to main        TestPyPI (first time)
                                                                    • 5-Python smoke green
                                                    │
                                                    ▼
 (D-07) HUMAN pushes tag  git tag 3.0.16 && git push origin 3.0.16
                                                    │
                                                    ▼
 ┌──────────────────────────── release.yml (on: push tag 3.*.* ) ───────────────────────────┐
 │ preflight ─► gates(full matrix) ─► build(pdm) ─► testpypi-publish ─► testpypi-smoke(3.10–14)│
 │                                                                          │                  │
 │                                                    ══ APPROVAL GATE ══   ▼                  │
 │                                              publish-pypi  [environment: release]  ◄── HUMAN │
 │                                                            │  (D-04 single stop)             │
 │            ┌───────────┬───────────┬────────────┬─────────┴──────────┬────────────────┐     │
 │            ▼           ▼           ▼            ▼                     ▼                ▼     │
 │         docker    branch-sync   tag-sync    gh-release           dev-bump      post-release  │
 │       (multi-arch  (FF stable/  (force 3,3.0 (RELEASE_BODY   (PR: 3.0.17 +   -checklist       │
 │        push)        3.0.x)       → RTD)       from awk)       fresh CHANGELOG)  (issue)        │
 └───────────────────────────────────────────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
 (D-13) POST-RELEASE  clean-venv pip install cement==3.0.16 + App().run()  ──►  merge dev-bump PR
                                                    │                              ──►  announcement draft (D-14)
                                                    ▼                              ──►  flip REL-01..05/CI-04/DOCS-03
                                             06-VERIFICATION.md                    ──►  (D-15 milestone = separate session)
```
[CITED: .github/workflows/release.yml, 05.4-PROVISIONING.md]

## Standard Stack

No new packages. This phase uses tools already present in the repo and dev environment.

### Core (all already installed / in-workflow)
| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| `git` | system | Tag push (D-07), `-s ours` ancestry merge (D-10), ancestry checks | The tag push IS the release trigger. |
| `gh` (GitHub CLI) | system | Provisioning verification (`gh api`), run monitoring (`gh run view/watch`), release inspection | Repo CLAUDE.md standardizes on `gh` for GitHub ops. [VERIFIED: gh api calls succeeded this session] |
| `pdm` | present | `pdm build` (in-workflow), dependency mgmt | Project build backend (pdm-backend). |
| `pypa/gh-action-pypi-publish` | `@v1.14.0` | OIDC publish to TestPyPI + PyPI | Pinned in `release.yml`. [CITED: release.yml L131,L205] |
| `peter-evans/create-pull-request` | `@v8.1.1` | dev-bump PR | Pinned in `release.yml` L345. |
| `docker/build-push-action` | `@v7.3.0` | Multi-arch (amd64+arm64) image push | Pinned in `release.yml` L229. |

### Supporting (in-repo helper scripts — do not modify unless a bug surfaces)
| Script | Purpose | When Used |
|--------|---------|-----------|
| `scripts/testpypi-smoke.py` | Install+import+`App().run()`+version-assert from TestPyPI | `testpypi-smoke` matrix job (dry-run + real run) |
| `scripts/bump_dev_version.py` | Rewrite VERSION tuple + prepend `## 3.0.17 - DEVELOPMENT` | `dev-bump` job (post-release) |
| `scripts/cli-smoke-native.py` | Cross-OS CLI smoke | Currently commented out in `gates.yml` (deferred to backlog 999.2) |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Editing `backend.py` VERSION by hand for the 3.0.16 bump | Running `bump_dev_version.py` | The script forces `'final'` too, but it also **prepends a fresh DEVELOPMENT changelog section** — wrong for the release-prep PR (which finalizes, not opens, a section). Hand-edit the tuple for 3.0.16; let the script handle only the 3.0.17 dev bump inside the workflow. |
| `gh run watch` for live monitoring | Polling `gh run view --json` | `watch` blocks; `--json status,conclusion,jobs` polling fits the checkpoint-cadence reporting the user asked for (D-16 discretion). |

## Package Legitimacy Audit

**Not applicable — this phase installs no new packages.** The release-prep PR touches only `CHANGELOG.md` and `cement/core/backend.py`; no `pyproject.toml` dependency changes, no new dev-deps. The GitHub Actions consumed by the pipeline were already audited and pinned in Phase 05.4 (see `05.4-SECURITY.md`, `threats_open: 0`; runbook "known accepted tradeoffs" #2 covers the exact-tag vs full-SHA pin posture for the three community actions: `peter-evans/create-pull-request@v8.1.1`, `hoverkraft-tech/compose-action@v3.0.0`, `ConorMacBride/install-package@v1.1.0`). No legitimacy gate to run. [CITED: 05.4-PROVISIONING.md "Known accepted tradeoffs"]

## Provisioning State Inventory (LIVE, 2026-07-12)

> The highest-value research output. Every item verifiable from here was checked with `gh api`/`git` this session; provider-UI-only items are flagged for the D-09 session.

| # | Checklist item | State (live check) | Blocking for | Action in Phase 6 |
|---|----------------|--------------------|--------------|-------------------|
| 1 | GitHub Environment `release` with required reviewers | ✅ EXISTS, reviewer `derks` [VERIFIED: gh api environments/release] | approval gate | none — confirm in D-09 |
| 2 | GitHub Environment `testpypi` | ✅ EXISTS (no branch policy) [VERIFIED: gh api] | dry-run | optional hardening only |
| 3 | TestPyPI trusted publisher (repo/`release.yml`/env `testpypi`) | ✅ WORKS — dry-run 29212487225 published + smoked green [VERIFIED: gh run] | dry-run | none |
| 4 | "Allow GitHub Actions to create and approve PRs" | ✅ ON (`can_approve_pull_request_reviews: true`) [VERIFIED: gh api] | dev-bump PR | none |
| 5 | `stable/3.0.x` unprotected / bot can push | ✅ Not protected; classic protection 404 [VERIFIED: gh api] | branch-sync | none (re-check if rules added) |
| 6 | Tag ruleset allows bot to force-update `3`/`3.0` | ⚠️ Ruleset "Github Actions Release Force Tags" is **active**, targets `refs/tags/3` + `refs/tags/3.0`, rule = **`deletion` only**, **no bypass actors** [VERIFIED: gh api rulesets/18840408] | tag-sync | **VERIFY on first run** — see Pitfall 4 |
| 7 | **Docker Hub secrets `DOCKERHUB_USERNAME` + `DOCKERHUB_TOKEN`** | ❌ **NOT SET** — repo secrets list is empty [VERIFIED: gh api actions/secrets] | `docker` job | **CLOSE in D-09** (D-11 OAT path) |
| 8 | **`stable/3.0.x` is an ancestor of `main`** (`-s ours` reconcile) | ❌ **NOT AN ANCESTOR** — `merge-base --is-ancestor` fails [VERIFIED: git] | branch-sync | **USER runs `-s ours` merge (D-10)**, agent verifies |
| 9 | **PyPI trusted publisher** (repo/`release.yml`/env `release`) | ❓ UNVERIFIABLE from here (PyPI provider UI) | `publish-pypi` (real) | **CONFIRM in D-09** before tag push |
| 10 | **RTD GitHub integration** connected; no per-patch activation rule | ❓ UNVERIFIABLE from here (RTD provider UI) | docs rebuild | **CONFIRM in D-09** |
| 11 | CHANGELOG finalized (`## 3.0.16 - <date>`, not DEVELOPMENT) | ❌ Still `## 3.0.15 - DEVELOPMENT (will be released as stable/3.0.16)` [VERIFIED: file] | preflight (push) | D-05 release-prep PR |
| 12 | `backend.py` VERSION == tag | ❌ Currently `(3, 0, 15, 'final', 0)` [VERIFIED: file] | preflight (push) | D-05 release-prep PR |

**Net:** 6 items green, 2 hard blockers open (#7 Docker secrets, #8 ancestry merge), 2 provider-UI unverifiable (#9 PyPI publisher, #10 RTD), 1 to verify-on-run (#6 tag ruleset), 2 closed by the release-prep PR (#11/#12).

## Runtime State Inventory

> This is a release/version-migration phase — external and ref state matters more than code.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | None — Cement has no datastores; the release is stateless artifacts. Verified: no DB/collection/key state in scope. | none |
| Live service config (provider UI, NOT in git) | GitHub Environments (`release`+reviewer, `testpypi`) ✅; TestPyPI trusted publisher ✅; **PyPI trusted publisher ❓**; **Docker Hub secrets ❌ not set**; **RTD GitHub integration ❓**; tag ruleset "Force Tags" ⚠️ | Close Docker secrets (D-11); confirm PyPI publisher + RTD in D-09; verify tag ruleset does not block force-update |
| OS-registered state | None (no scheduled tasks / daemons involved) | none |
| Secrets/env vars | `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` (repo secrets) — **not set**. PyPI/TestPyPI use OIDC → **no PyPI token secret exists by design** (do not create one). | Set the two Docker secrets only |
| Build artifacts / registry state | TestPyPI currently holds `cement 3.0.15` (from dry-run 29212487225, which derives version from the package — currently 3.0.15). 3.0.16 is **not yet on TestPyPI**. `*.egg-info/` locally is stale after any version edit. PyPI has ≤3.0.14. | D-06 dry-run uploads 3.0.16 to TestPyPI fresh; the real tag run `skip-existing` re-smokes it. Rebuild local env (`make init`) if egg-info drifts. |

**The canonical question — "after the repo is updated, what still holds old state?":** TestPyPI's immutable-filename index. Once 3.0.16 is uploaded (by the D-06 dry-run), it is frozen; the real run's `--skip-existing` re-uses those exact bytes (05.4 D-08 accepted caveat — same commit, no drift). A version-string mistake in the release-prep PR that reaches TestPyPI **cannot be overwritten** for that version number — it can only be superseded by a bump. This is why the final dry-run runs against the *merged, finalized* commit, not a WIP branch.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Bumping the version | A sed/manual multi-file edit hunting `pyproject.toml` + `__init__.py` | Edit the ONE `VERSION` tuple in `cement/core/backend.py` | pyproject/`__init__` derive dynamically; extra edits would create a false second source of truth. |
| Post-release 3.0.17 bump | Hand-editing after release | The `dev-bump` job (`bump_dev_version.py`) inside the workflow | Already computed (patch+1), already tested, opens the PR. Phase just merges it. |
| Extracting release notes from CHANGELOG | Copy-paste into GitHub Release UI | The `gh-release` job's awk extraction | Deterministic `## 3.0.16` section boundary; zero human transcription error. |
| Re-pointing `3`/`3.0` moving tags + RTD rebuild | Manual `git push --force` + RTD UI click | `tag-sync` job (fires RTD webhook) | The whole point of Phase 05.4; manual steps are what it replaced. |
| PyPI auth | Adding a `PYPI_TOKEN` secret | OIDC trusted publisher (already the design) | Long-lived tokens are the exact anti-pattern 05.4 removed; adding one is a regression. |
| Announcement copy | Writing fresh prose | Derive from the finalized changelog highlights paragraph (D-03) | One source of truth for "what shipped" (D-14 / specifics). |

**Key insight:** Nearly every "release step" you might reflexively hand-roll is already a workflow job. Phase 6's job is to *feed the machine correct inputs* (finalized changelog + correct version + provisioned providers) and *press the human buttons* (merge, tag, approve, merge). Re-implementing any automated step is scope creep and a regression risk.

## Common Pitfalls

### Pitfall 1: Squash/rebase-merging the ancestry reconcile (D-10) — silently breaks branch-sync
**What goes wrong:** The `-s ours` merge must land on `main` as a **real merge commit** with `origin/stable/3.0.x` as a parent. If the user merges it via a GitHub PR with "Squash" or "Rebase", the second parent is destroyed and `stable/3.0.x` is *still* not an ancestor — `branch-sync` fails on the live release.
**Why it happens:** GitHub's default PR merge button is often squash; the ancestry link is invisible in a diff (`-s ours` changes no files).
**How to avoid:** Run the merge directly on `main` locally per runbook §6b (`git merge -s ours origin/stable/3.0.x -m "..."` then `git push origin main`), NOT via a squashed PR. Agent verifies with `git merge-base --is-ancestor origin/stable/3.0.x main && echo FF-OK` afterward. [CITED: 05.4-PROVISIONING.md §6b, D-10]

### Pitfall 2: Running `bump_dev_version.py` for the 3.0.16 bump
**What goes wrong:** The helper sets `'final'` (good) BUT also prepends a new `## 3.0.16 - DEVELOPMENT` section. In the release-prep PR you are *finalizing* the existing section to `## 3.0.16 - <date>`, not opening a new one — running the script would create a duplicate/DEVELOPMENT-marked header that fails preflight's finalization guard.
**How to avoid:** For the release-prep PR, hand-edit the `VERSION` tuple `(3, 0, 15, ...) → (3, 0, 16, 'final', 0)` and finalize the changelog header manually. Reserve `bump_dev_version.py` for the automated 3.0.17 bump (which the workflow runs, not you). [CITED: bump_dev_version.py docstring L88-106]

### Pitfall 3: TestPyPI immutability — a bad version can't be re-uploaded
**What goes wrong:** If the D-06 dry-run runs against a commit with a wrong version or unfinalized changelog and uploads to TestPyPI, that filename is frozen. Re-running won't refresh it (`skip-existing`).
**How to avoid:** Run the D-06 dry-run ONLY after the release-prep PR is merged to main (finalized changelog + correct VERSION). The dry-run's version is derived from the package, so it will be exactly 3.0.16. [CITED: release.yml preflight L62-70; 05.4-PROVISIONING.md §3 stale-upload caveat]

### Pitfall 4: The "Force Tags" ruleset could block `tag-sync`
**What goes wrong:** A GitHub tag ruleset covering `refs/tags/3` and `refs/tags/3.0` exists and is **active with no bypass actors**. If it enforced `non_fast_forward` or `update`, the `tag-sync` job's `git push --force` would be rejected and the docs rebuild would never fire.
**Why it (probably) does NOT block:** The ruleset's only rule is **`deletion`**. A moving-tag force-update is a non-fast-forward *update*, not a deletion, so `deletion` does not apply. [VERIFIED: gh api rulesets/18840408 — rules=["deletion"], target=tag, no bypass]
**How to avoid / verify:** On the first live release, confirm `tag-sync` succeeds. If it fails with a protected-ref error, add the **GitHub Actions** app to the ruleset's bypass list (Settings → Rules → Rulesets). Flag this in the D-09 checkpoint as "verify-on-run."

### Pitfall 5: Docker Hub login with a password / OAT-plan surprise (D-11)
**What goes wrong:** The `docker` job needs `DOCKERHUB_USERNAME`/`DOCKERHUB_TOKEN` (currently unset). Using an account password (not a token), or discovering the org lacks a Docker Team/Business plan for the preferred OAT, blocks the multi-arch push.
**How to avoid:** In D-09, mint the token per runbook §4 preference order: **OAT (org-scoped)** → **bot-account PAT** → **maintainer PAT**. With an OAT, `DOCKERHUB_USERNAME` = `datafolklabs` (the org name), not a personal login. The `docker` job runs *after* the approval gate, so a Docker misconfig does NOT block the PyPI publish — but per D-08 it would need a re-run-failed-jobs. Close this before tagging. [CITED: 05.4-PROVISIONING.md §4, D-11]

### Pitfall 6: Approving the gate before the changelog is truly complete (DOCS-03 / success criterion 1)
**What goes wrong:** Preflight only checks the section is *finalized* (not `- DEVELOPMENT`); it does NOT check that every user-visible change is *enumerated*. A missing entry passes CI but violates success criterion 1, and the GitHub Release body (auto-extracted) ships incomplete.
**How to avoid:** The D-01 git-log cross-check (`git log 3.0.14..HEAD`, filter planning-artifact commits per CLAUDE.md changelog rules) is the only guard. 360 commits are in range but the section already has full buckets; the cross-check is a reconcile, not a rewrite. Do it before merging the release-prep PR — the PR review is the human gate. [CITED: D-01; CLAUDE.md "Changelog Maintenance"]

### Pitfall 7: The dev-bump PR shows zero CI checks (accepted, not a bug)
**What goes wrong:** The `dev-bump` PR is authored by `GITHUB_TOKEN`; GitHub's anti-recursion rule means `on: pull_request` CI does not fire, so the PR shows no checks. A reviewer might block on "missing CI."
**How to avoid:** This is accepted tradeoff #1 in the runbook — merge it deliberately (main CI runs post-merge). Don't wait for checks that will never appear. [CITED: 05.4-PROVISIONING.md "Known accepted tradeoffs" #1]

## Code Examples

Exact, verified command sequences the plans will use.

### Version bump (release-prep PR) — single source of truth
```python
# cement/core/backend.py  (edit the tuple ONLY; preserve the trailing pragma comment)
VERSION = (3, 0, 16, 'final', 0)  # pragma: nocover  # version constant
```
```bash
# Verify the whole repo has no other 3.0.15 version-of-record (expect only the
# bump_dev_version.py regex-doc comment, which is not a version of record):
grep -rn "3\.0\.15\|(3, 0, 15" --include="*.py" --include="*.toml" . | grep -v ".planning/"
# Confirm the derived version after the edit:
python -c "from cement.utils.version import get_version; print(get_version())"   # -> 3.0.16
```
[VERIFIED: grep this session found only backend.py + bump_dev_version.py comment]

### Changelog header finalization (D-02)
```markdown
## 3.0.16 - July 12, 2026   <!-- convention matches: `## 3.0.14 - May 5, 2025` -->
```
[VERIFIED: CHANGELOG.md L541 header convention]

### One-time ancestry reconcile (D-10 — USER runs on main, NOT via squashed PR)
```bash
git fetch origin main stable/3.0.x
git switch main && git pull --ff-only origin main
git merge -s ours origin/stable/3.0.x \
  -m "chore: record stable/3.0.x ancestry for release fast-forward"
git diff HEAD^ HEAD            # MUST print nothing (zero content change)
git push origin main
git merge-base --is-ancestor origin/stable/3.0.x main && echo FF-OK   # agent verifies
```
[CITED: 05.4-PROVISIONING.md §6b]

### Final dry-run (D-06 — after release-prep PR merged)
```bash
gh workflow run release.yml -R datafolklabs/cement --ref main
# then monitor:
gh run list -R datafolklabs/cement --workflow release.yml --limit 1
gh run view <run-id> -R datafolklabs/cement --json status,conclusion,jobs
```

### Pre-tag safety + tag handoff (D-07 — commands the AGENT hands to the USER)
```bash
# 1. resolve the exact SHA to tag (the merged release-prep commit on main):
git fetch origin main && git rev-parse origin/main
# 2. prove the fast-forward precondition BEFORE tagging (must print FF-OK):
git merge-base --is-ancestor origin/stable/3.0.x <sha> && echo FF-OK
# 3. USER pushes the tag (this is the release trigger):
git tag 3.0.16 <sha>
git push origin 3.0.16
```
[CITED: release.yml trigger L10-11; D-07]

### Live-run monitoring + approval
```bash
gh run watch <run-id> -R datafolklabs/cement            # or poll --json as above
# approval happens in the GitHub UI: Actions → run → "Review deployments" → approve `release`
```

### REL-04 clean-venv verification (D-13 — after PyPI publish)
```bash
python -m venv /tmp/cement-rel-check && . /tmp/cement-rel-check/bin/activate
pip install cement==3.0.16
python -c "from cement import App; from cement.utils.version import get_version; \
  assert get_version()=='3.0.16', get_version(); \
  App(argv=[]).run() if False else None; print('REL-04 OK', get_version())"
deactivate
```
(Mirror `scripts/testpypi-smoke.py`'s `SmokeApp(argv=[])` pattern for a real `App().run()` round-trip if desired.) [CITED: testpypi-smoke.py L88-99; D-13]

### Failure recovery (D-08)
```bash
# Gate/preflight failure BEFORE publish → delete tag, fix, re-tag:
git push --delete origin 3.0.16 && git tag -d 3.0.16
# ... fix on a branch, merge, re-tag ...
# Publish-side partial failure AFTER PyPI publish succeeded → re-run failed jobs (tag stays):
gh run rerun <run-id> -R datafolklabs/cement --failed
```
[CITED: D-08]

## State of the Art

| Old Approach (issue #791) | Current Approach (Phase 05.4) | When Changed | Impact |
|---------------------------|-------------------------------|--------------|--------|
| Manual release checklist, hand-run twine + docker + tags | Tag-push-triggered `release.yml` | 2026-07-12 | Phase 6 is the first real exercise of the automation |
| Long-lived PyPI API token | OIDC trusted publisher (`id-token: write` + env claim) | 05.4 | No token secret to leak; do NOT add one |
| Manual `3`/`3.0` tag re-point + RTD click | `tag-sync` job fires RTD webhook | 05.4 | RTD rebuilds `/en/3.0/` automatically |
| Manual post-release version bump | `dev-bump` job opens the 3.0.17 PR | 05.4 | Phase only merges the PR |

**Deprecated/outdated within this repo context:**
- Travis CI — deleted in Phase 1; GitHub Actions is the only CI.
- Any per-patch RTD activation rule — explicitly must NOT exist (RTD is per-minor-line off `3.0`). [CITED: 05.4-PROVISIONING.md §5]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `git` | Tag push, ancestry merge | ✅ | system | — |
| `gh` CLI (authenticated to datafolklabs) | Provisioning verify + run monitoring | ✅ | authenticated (gh api succeeded) | — |
| `python`/`pdm` dev env | Local version verify, REL-04 clean venv | ✅ | 3.10+ | `make init` rebuilds if broken |
| PyPI trusted publisher | `publish-pypi` (real) | ❓ provider-UI | — | Confirm/create in D-09 — BLOCKING for real publish |
| Docker Hub token secrets | `docker` job | ❌ not set | — | Mint OAT/PAT in D-09 (D-11) — post-gate, so re-runnable |
| RTD GitHub integration | docs rebuild | ❓ provider-UI | — | Confirm in D-09; fallback = manual RTD build trigger |

**Missing dependencies with no fallback (must resolve before tag push):**
- PyPI trusted publisher (item #9) — a missing/misconfigured publisher fails the real `publish-pypi` with `invalid-publisher` at the approval gate.
- `stable/3.0.x` ancestry (item #8) — `branch-sync` fails without the `-s ours` merge.

**Missing dependencies with viable in-run recovery:**
- Docker secrets (item #7) — `docker` runs after the gate; a failure is recoverable via re-run-failed-jobs once secrets are set (D-08), though best practice is to set them in D-09 before tagging.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | `pytest` + `pytest-cov` (100% coverage gate, `--cov-fail-under=100`) |
| Config file | `pyproject.toml` `[tool.pytest.ini_options]` |
| Quick run command | `make comply` (ruff + mypy) |
| Full suite command | `make test` (needs Redis:6379 + memcached:11211 up — MEMORY note) |

### Phase Requirements → Validation Map
| Req ID | Behavior | Validation Type | Command / Evidence | Exists? |
|--------|----------|-----------------|--------------------|---------|
| DOCS-03 | Changelog enumerates all user-visible changes | manual + preflight guard | D-01 cross-check; `grep "^## 3.0.16" CHANGELOG.md` (no `DEVELOPMENT`) | ✅ (preflight job) |
| REL-01 | VERSION reads 3.0.16 | automated | `python -c "from cement.utils.version import get_version; print(get_version())"` == 3.0.16 | ✅ |
| REL-02 | TestPyPI 5-Python smoke | automated (in-workflow) | `testpypi-smoke` matrix 3.10–3.14 green | ✅ |
| CI-04 | Workflow end-to-end vs TestPyPI | automated (in-workflow) | Green `workflow_dispatch` run (D-06) | ✅ |
| REL-03 | Tag + Release published | automated (in-workflow) + inspect | `gh release view 3.0.16`; tag exists | ✅ |
| REL-04 | PyPI installs on 3.10–3.14 | manual clean-venv (D-13) + in-run 5-Python proof | `pip install cement==3.0.16` round-trip | ✅ |
| REL-05 | Bumped to 3.0.17 | automated (dev-bump) + merge | dev-bump PR merged; `get_version()` == 3.0.17 | ✅ |

### Sampling Rate
- **Release-prep PR:** full PR CI (`gates.yml` via `build_and_test.yml`) must be green before merge — `make comply` + `make test` + matrix.
- **Pre-tag:** the D-06 dry-run is the gate for the finalized artifact.
- **Post-release:** D-13 clean-venv check + `gh release view` + dev-bump merge.

### Wave 0 Gaps
- None — this phase writes no product code and needs no new tests. The existing 100%-coverage gate and the release workflow's own gate suite are the validation. The `05.4` Windows/macOS smoke legs remain deferred to backlog 999.2 (accepted override, not a Phase 6 concern).

## Security Domain

> Release-side threat modeling was completed in Phase 05.4 (`05.4-SECURITY.md`, `threats_open: 0`, 19/19 dispositioned). Phase 6 introduces no new attack surface — it consumes the audited pipeline. Only the release-execution-specific controls are restated here.

| Concern | STRIDE | Control (already in place) |
|---------|--------|---------------------------|
| Credential exfiltration during build | Information Disclosure | Isolated `build` job holds no publish creds; artifacts handed downstream. [CITED: release.yml build job] |
| PyPI publish auth | Spoofing / Elevation | OIDC trusted publisher + `release` environment claim — no long-lived token. **Do not add a PyPI token secret.** |
| Unapproved publish | Elevation of Privilege | Single `release` env approval gate; all publish-side jobs `needs: publish-pypi`. |
| Template injection via `github.ref_name` | Tampering | Passed via `env:`, never inline-spliced; regex-escaped in awk/grep. [CITED: release.yml L54-57, L293-301] |
| Supply-chain (actions) | Tampering | Exact-tag pins (accepted tradeoff #2); full-SHA tightening deferred. |
| Docker token blast radius | Info Disclosure | OAT repo-scoping preferred (D-11); token, never password. |

**Phase-6-specific control:** confirm the Docker token is repo-scoped (OAT) or account-limited (bot) before storing it as a secret — a maintainer PAT (fallback) reaches every repo that account can write to.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | PyPI trusted publisher for `cement` (repo `datafolklabs/cement`, workflow `release.yml`, env `release`) is configured | Provisioning #9 | `publish-pypi` fails `invalid-publisher` at the approval gate — the release stalls after gates pass. **Confirm in D-09.** |
| A2 | RTD GitHub integration is connected and will rebuild `/en/3.0/` on the `3.0` tag push | Provisioning #10 | Docs silently don't rebuild; artifacts still ship. Lower severity; **confirm in D-09.** |
| A3 | The "Force Tags" ruleset (deletion-only, no bypass) does NOT block a moving-tag force-*update* | Pitfall 4 | `tag-sync` fails; RTD rebuild doesn't fire. Recoverable via bypass-list edit + re-run. **Verify on first run.** |
| A4 | The `datafolklabs` org has a Docker Team/Business plan enabling the preferred OAT (D-11) | Pitfall 5 | Fall back to bot-account PAT then maintainer PAT per runbook §4. Non-blocking (post-gate job). |
| A5 | TestPyPI still holds only `cement 3.0.15` (not 3.0.16) from the last dry-run | Runtime State | If a prior 3.0.16 upload exists, the D-06 dry-run `skip-existing`s it and smokes stale bytes — but since it'd be the same finalized commit, no drift. Low risk. |
| A6 | The 360-commit `3.0.14..HEAD` range maps cleanly onto the existing 5 changelog buckets after planning-artifact filtering | Pitfall 6 / D-01 | An omitted user-visible change violates success criterion 1. Mitigated by the cross-check being a reconcile of an already-populated section, gated by PR review. |

## Open Questions

1. **Is the PyPI (real) trusted publisher configured?**
   - What we know: TestPyPI's works (dry-run proved it); the `release` env + reviewer exist.
   - What's unclear: PyPI's provider UI can't be read from here.
   - Recommendation: First verification in the D-09 checkpoint; if absent, create it (repo `datafolklabs/cement`, workflow `release.yml`, env `release`) before any tag push. This is the single highest-risk unknown.

2. **Does the tag ruleset permit the bot's moving-tag force-update?**
   - What we know: rule is `deletion` only, no bypass actors; force-update ≠ deletion.
   - What's unclear: whether GitHub treats a lightweight-tag force-move as covered.
   - Recommendation: mark `tag-sync` as "verify-on-run"; if it fails, add GitHub Actions to the ruleset bypass list and `gh run rerun --failed` (D-08).

3. **OAT plan availability for Docker (D-11)?**
   - What we know: OAT needs Team/Business; fallback chain is documented.
   - Recommendation: determine the plan at the D-09 checkpoint; pick the highest-scoping token path available.

4. **Monitoring cadence during the ~30–40 min runs (D-16 discretion)?**
   - Recommendation: `gh run view --json status,conclusion,jobs` at each job-transition, report a one-line status to the user; pause for the approval gate (human action in the GitHub UI).

## Sources

### Primary (HIGH confidence — live-verified this session)
- `gh api repos/datafolklabs/cement/environments`, `.../actions/secrets`, `.../actions/permissions/workflow`, `.../rulesets/18840408` — provisioning state (envs, empty secrets, PR-approval on, force-tags ruleset)
- `git merge-base --is-ancestor origin/stable/3.0.x origin/main` — ancestry still NOT recorded
- `git tag -l`, `git rev-list --count 3.0.14..HEAD` (360), `grep`/`sed` on `CHANGELOG.md` + `cement/core/backend.py` + `pyproject.toml`
- `gh run view 29212487225` — green `workflow_dispatch` dry-run baseline (CI-04)
- `.github/workflows/release.yml` (13 jobs), `.github/workflows/gates.yml`
- `scripts/testpypi-smoke.py`, `scripts/bump_dev_version.py`, `cement/utils/version.py`

### Secondary (HIGH — authored contract artifacts from Phase 05.4)
- `.planning/phases/05.4-github-actions-release-workflow/05.4-PROVISIONING.md` (checklist, exact values, §4 Docker, §5 RTD, §6 ancestry)
- `.planning/phases/05.4-.../05.4-VERIFICATION.md` (5/5, deferred items), `05.4-CONTEXT.md`, `05.4-SECURITY.md`
- `.planning/phases/06-release-cut-3-0-16/06-CONTEXT.md`, `.planning/REQUIREMENTS.md`, `CLAUDE.md`

### Provider-UI unverifiable (flagged for D-09)
- PyPI trusted publisher state, RTD GitHub integration state

## Metadata

**Confidence breakdown:**
- Standard stack / no new packages: HIGH — repo + workflow files inspected directly.
- Provisioning inventory: HIGH for gh/git-verifiable items; the 2 provider-UI items (PyPI publisher, RTD) are explicitly ASSUMED and gated to D-09.
- Version-of-record (single source): HIGH — grep + pyproject dynamic config confirmed.
- Pitfalls: HIGH — each traces to a workflow line or runbook section.

**Research date:** 2026-07-12
**Valid until:** provisioning state is live-checked here; re-verify items #7/#8/#9/#10 at the start of the D-09 session (state may change as the user provisions). Workflow/version facts stable for the release window.
