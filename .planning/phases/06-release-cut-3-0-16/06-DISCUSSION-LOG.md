# Phase 6: Release Cut 3.0.16 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-07-12
**Phase:** 6-release-cut-3-0-16
**Areas discussed:** Changelog finalization, Release-prep commit flow, Provisioning completion, Post-release wrap-up scope

---

## Todo Cross-Reference (pre-discussion)

| Option | Description | Selected |
|--------|-------------|----------|
| Keep both deferred | GitBook todos stay on the auto-emitted post-release checklist issue (05.4 D-16) | ✓ |
| Fold #778 GitBook features doc | Make it a tracked Phase 6 deliverable | |
| Fold todo-tutorial GitBook update | Make it a tracked Phase 6 deliverable | |

**User's choice:** Keep both deferred (recommended).

---

## Changelog finalization

| Option | Description | Selected |
|--------|-------------|----------|
| Full git-log cross-check | Diff `git log 3.0.14..HEAD` against every entry; flag missing user-visible changes and stale entries | ✓ |
| Light structural pass | Trust phase-by-phase maintenance; verify buckets + formatting only | |
| You decide | Claude picks audit depth during planning | |

**User's choice:** Full git-log cross-check.

| Option | Description | Selected |
|--------|-------------|----------|
| Pure buckets | Match 3.0.x convention exactly — no prose intro | |
| Add highlights paragraph | 2–4 sentence intro summarizing release themes above the buckets; also tops the GitHub Release body | ✓ |

**User's choice:** Add highlights paragraph — deviates from the recommended pure-bucket convention; user wants the narrative summary.

| Option | Description | Selected |
|--------|-------------|----------|
| Condense verbose entries | Keep every entry, edit to 1–3 lines at release-notes altitude | ✓ |
| Preserve entries as-is | Only audit completeness + formatting | |
| Condense + trim dev-only entries | Also fold `[dev]` tooling entries into consolidated lines | |

**User's choice:** Condense verbose entries (keep all entries, including `[dev]`).

---

## Release-prep commit flow

| Option | Description | Selected |
|--------|-------------|----------|
| One release-prep PR | Single branch: changelog finalization + VERSION bump; user merges; merge commit gets tagged | ✓ |
| Two PRs: changelog, then bump | Isolate the subjective edit from the mechanical one | |
| Direct to main with consent | Skip PR overhead with explicit authorization | |

**User's choice:** One release-prep PR.

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, final dry-run | `workflow_dispatch` against the merged release commit; validates preflight against real finalized changelog + version; D-08 skip-existing caveat accepted | ✓ |
| No, tag directly | CI-04 dry-run already green; preflight failure is cheap (delete/re-tag) | |

**User's choice:** Yes, final dry-run.

| Option | Description | Selected |
|--------|-------------|----------|
| You push it yourself | Agent hands over verified commands; human act of tagging stays the source of truth (05.4 D-01) | ✓ |
| Agent pushes at a checkpoint | Executor tags/pushes after explicit approval | |

**User's choice:** User pushes the tag personally.

| Option | Description | Selected |
|--------|-------------|----------|
| Re-run failed jobs | GitHub re-run-failed-jobs on the same run; tag stays; manual fallback only if unrecoverable | ✓ |
| Manual completion | Finish downstream steps by hand after any post-PyPI failure | |
| You decide | Claude picks per-job recovery during planning | |

**User's choice:** Re-run failed jobs (gate failures remain delete/re-tag per 05.4 D-01).

---

## Provisioning completion

| Option | Description | Selected |
|--------|-------------|----------|
| Guided checkpoint session | Agent walks the runbook item-by-item; user clicks provider UIs; agent verifies via gh api where possible | ✓ |
| I'll do it offline | User completes runbook solo and confirms | |
| Hybrid | Agent configures everything CLI-reachable; only provider-UI items go to the user | |

**User's choice:** Guided checkpoint session.

| Option | Description | Selected |
|--------|-------------|----------|
| You run it, agent preps | Agent hands exact `-s ours` merge + push commands; user executes on main | ✓ |
| Agent runs it with consent | One-time authorized direct push to main by the agent | |
| PR merged via merge-commit | Preserves ancestry only if the merge method isn't rebase/squash | |

**User's choice:** User runs the ancestry merge; agent preps and verifies.

| Option | Description | Selected |
|--------|-------------|----------|
| Maintainer PAT | Simplest; full account scope | |
| Bot-account PAT | Machine account with repo-only push rights | |
| Org access token (OAT) | Repo-scoped org token; requires Docker Team/Business | ✓ |
| Decide during provisioning | Pick at the checkpoint in the Docker Hub UI | |

**User's choice:** Org access token (OAT) — deviates from the maintainer-PAT recommendation; fallback per runbook §4 if the org plan doesn't support OAT.

| Option | Description | Selected |
|--------|-------------|----------|
| First plan of the phase | Full checklist up front; surprises surface earliest | ✓ |
| Parallel with changelog work | Sibling plans in the same wave | |
| Just-in-time before tag | Provisioning as the last step pre-tag | |

**User's choice:** First plan of the phase.

---

## Post-release wrap-up scope

| Option | Description | Selected |
|--------|-------------|----------|
| Through dev-bump merge | Publish + Release live + dev-bump PR merged + requirement flips + VERIFICATION.md | ✓ |
| End at publish | Dev-bump merge and flips as post-phase housekeeping | |
| Include post-release checklist | Phase open until GitBook/notifications done | |

**User's choice:** Through dev-bump merge.

| Option | Description | Selected |
|--------|-------------|----------|
| Single clean-venv check | One venv, pip install from PyPI, import + App().run() round-trip | ✓ |
| Full 5-Python matrix | Repeat on 3.10–3.14 docker legs against production PyPI | |

**User's choice:** Single clean-venv check.

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, draft the copy | Agent drafts announcement from finalized changelog; sending stays human | ✓ |
| No, fully human | Announcements entirely in the user's voice | |

**User's choice:** Yes, draft the announcement copy.

| Option | Description | Selected |
|--------|-------------|----------|
| Separate session | Phase ends at flips + VERIFICATION.md; user invokes /gsd-complete-milestone later | ✓ |
| Chain it into the phase | Hand directly into milestone completion | |

**User's choice:** Separate session.

---

## Claude's Discretion

- Plan/wave decomposition beyond provisioning-first
- Git-log cross-check mechanics (commit classification, planning-artifact filtering)
- Condensed-entry wording and highlights paragraph (reviewed via the release-prep PR)
- Announcement-copy format and artifact location
- Dry-run/live-run monitoring cadence during execution

## Deferred Ideas

- Post-release checklist issue execution (GitBook docs, mailing list, Slack) — human work tracked by the auto-created issue
- Milestone archive via `/gsd-complete-milestone` — separate follow-up session
- Full-commit-SHA pinning for community actions — runbook accepted-tradeoff #2, revisit post-release
- Reviewed todos not folded: `2026-05-09-document-optional-features-in-gitbook-post-3-0-16.md`, `2026-07-11-update-gitbook-todo-tutorial-for-pdm-backend.md` (both post-release GitBook work)
