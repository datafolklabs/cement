# 06-01 Task 1 — Live Provisioning Re-Inventory

**Refreshed:** 2026-07-13 (start of the D-09 guided session)
**Method:** read-only `gh api` / `git` checks against `datafolklabs/cement`.
No provisioning state was changed by this task (feeds Task 2/3).

## Verbatim check output

```
# gh api repos/datafolklabs/cement/environments --jq '.environments[].name'
copilot
release
testpypi

# gh api .../environments/release  (protection_rules)
{"name":"release","rules":[{"reviewers":["derks"],"type":"required_reviewers"}]}

# gh api .../actions/secrets --jq '.secrets[].name'
(empty — no repo secrets set)

# gh api .../actions/permissions/workflow
{"default_workflow_permissions":"write","can_approve_pull_request_reviews":true}

# gh api .../rulesets/18840408
name="Github Actions Release Force Tags" enforcement=active target=tag
conditions.ref_name.include=["refs/tags/3","refs/tags/3.0"]
rules=["deletion"]  bypass=[]

# gh api .../rulesets  (all)
{id:797205,  name:"Default",                         enforcement:disabled, target:branch}
{id:18840408,name:"Github Actions Release Force Tags",enforcement:active,   target:tag}

# gh api .../branches/stable%2F3.0.x/protection
404 "Branch not protected"

# git fetch origin main stable/3.0.x
# git merge-base --is-ancestor origin/stable/3.0.x origin/main ; echo $?
1            # non-zero == NOT an ancestor == ancestry OPEN
# git rev-parse origin/stable/3.0.x -> 0679bf51e4c24d900528979884e66c5e14f28ef1
# git rev-parse origin/main         -> c4dc2df23ffc6a5e120a714b2343e372bba0716f

# CHANGELOG.md header
## 3.0.15 - DEVELOPMENT (will be released as stable/3.0.16)

# cement/core/backend.py
VERSION = (3, 0, 15, 'final', 0)  # pragma: nocover  # version constant
```

## 12-row state table (maps RESEARCH inventory #1–#12)

| # | Checklist item | Status | Evidence |
|---|----------------|--------|----------|
| 1 | GitHub Env `release` + required reviewers | GREEN | reviewer `derks` present |
| 2 | GitHub Env `testpypi` | GREEN | env exists |
| 3 | TestPyPI trusted publisher | UNVERIFIABLE-FROM-HERE | provider-UI; proven green by dry-run 29212487225 |
| 4 | Allow Actions create/approve PRs | GREEN | `can_approve_pull_request_reviews: true` |
| 5 | `stable/3.0.x` unprotected / bot can push | GREEN | 404 not protected; no `stable/*` ruleset (only disabled "Default") |
| 6 | Tag ruleset allows bot force-update `3`/`3.0` | GREEN (verify-on-run) | active, rules=`["deletion"]` only, no bypass — deletion ≠ force-update |
| 7 | Docker secrets `DOCKERHUB_USERNAME` + `DOCKERHUB_TOKEN` | **OPEN (blocker)** | secrets list empty — both ABSENT |
| 8 | `stable/3.0.x` is an ancestor of `main` | **OPEN (blocker)** | `merge-base --is-ancestor` exit 1 |
| 9 | PyPI trusted publisher (repo/`release.yml`/env `release`) | UNVERIFIABLE-FROM-HERE | provider-UI; confirm in D-09 |
| 10 | RTD GitHub integration; no per-patch activation rule | UNVERIFIABLE-FROM-HERE | provider-UI; confirm in D-09 |
| 11 | CHANGELOG finalized (`## 3.0.16 - <date>`) | OPEN (closed by Plan 02) | still `## 3.0.15 - DEVELOPMENT` |
| 12 | `backend.py` VERSION == tag | OPEN (closed by Plan 02) | currently `(3, 0, 15, 'final', 0)` |

## Net

State unchanged since 2026-07-12 research. Two hard blockers OPEN for this plan:
- **#7 Docker Hub secrets** — close in the Task 2 guided session (D-11 token order).
- **#8 `stable/3.0.x` ancestry** — close in Task 3 via the USER's `-s ours` merge (D-10).

Two provider-UI items (#9 PyPI publisher, #10 RTD) remain UNVERIFIABLE from the
repo and must be user-confirmed in the Task 2 session. Item #6 stays "verify on
first live run." A new `copilot` GitHub environment has appeared since research —
harmless (unused by `release.yml`), noted only for completeness.
