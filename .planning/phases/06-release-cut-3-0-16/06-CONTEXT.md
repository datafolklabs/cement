# Phase 6: Release Cut 3.0.16 - Context

**Gathered:** 2026-07-12
**Status:** Ready for planning

<domain>
## Phase Boundary

Run the 3.0.16 release using the machinery Phase 05.4 built and dry-run-validated
(run 29212487225 GREEN end-to-end). The phase: complete the pre-first-tag
provisioning checklist, audit and finalize the changelog, bump the version of
record to 3.0.16, rehearse once more via `workflow_dispatch` dry-run, hand the
user the tag-push commands, shepherd the live release run through the single
approval gate, verify the published artifacts, merge the dev-bump PR (3.0.17),
draft announcement copy, and flip the milestone requirement IDs
(REL-01..05, CI-04, DOCS-03). Locked by ROADMAP success criteria (not re-decided
here): changelog enumerates all user-visible changes; TestPyPI install proof on
3.10–3.14; version-of-record reads 3.0.16 at tag time and 3.0.17 after; tag +
GitHub Release + clean `pip install cement==3.0.16`; the workflow runs
end-to-end with no manual intervention beyond the approved publish step.

Locked by Phase 05.4 (carry forward, do not re-litigate): tag push is the
canonical trigger with unprefixed tags (D-01/D-09); one approval stop via the
`release` GitHub Environment (D-03/D-04); TestPyPI inline with `--skip-existing`
idempotency (D-05/D-08); dry-run never publishes (D-06); dev-bump lands as an
automated PR (D-12); notifications stay human steps on the emitted post-release
checklist issue (D-15/D-16).

</domain>

<decisions>
## Implementation Decisions

### Changelog finalization
- **D-01:** Full git-log cross-check before finalization — diff
  `git log 3.0.14..HEAD` against every entry in the `## 3.0.15 - DEVELOPMENT`
  section; flag any user-visible change that's missing and any entry that no
  longer matches what shipped. Success criterion 1 demands complete enumeration.
- **D-02:** Section header renamed to `## 3.0.16 - <Month D, YYYY>` matching
  the established convention (`## 3.0.14 - May 5, 2025`). The header MUST
  begin `## 3.0.16` — the release workflow's `gh-release` job awk-extracts the
  section by tag match, and preflight (05.4 D-02) validates it is finalized.
- **D-03:** Add a short narrative highlights paragraph (2–4 sentences) at the
  top of the 3.0.16 section — Python 3.10–3.14 matrix, new warn-only
  deprecations, release automation, template modernization — above the
  standard buckets. It becomes the top of the GitHub Release body.
- **D-04:** Condense verbose entries at finalization: keep EVERY entry, edit
  each to 1–3 lines at release-notes altitude (what changed + why it matters
  to users); drop dev-time forensic detail — git history retains it. Do NOT
  delete or merge `[dev]` entries.

### Release-prep commit flow
- **D-05:** One release-prep PR: a single branch (e.g. `gsd/phase-6-release-cut`)
  carries changelog finalization + `cement/core/backend.py` VERSION bump to
  `(3, 0, 16, 'final', 0)`. User reviews and merges; the resulting main commit
  is what gets tagged. No direct commits to main.
- **D-06:** One final `workflow_dispatch` dry-run against the merged release
  commit on main before tagging — first validation of preflight against the
  real finalized changelog + version. Accepted caveat (05.4 D-08): the dry-run
  uploads 3.0.16 to TestPyPI; the real tag run skip-exists and smokes that
  artifact — same commit, so no content drift.
- **D-07:** The user pushes the tag personally (`git tag 3.0.16 && git push
  origin 3.0.16`). The agent hands over the exact verified command sequence —
  correct SHA, pre-tag ancestry check (`git merge-base --is-ancestor
  origin/stable/3.0.x <sha>`) already proven green. Matches 05.4 D-01: the
  human act of tagging is the source of truth.
- **D-08:** Failure policy for the live run: gate failures = delete tag, fix,
  re-tag (05.4 D-01, unchanged). Publish-side partial failure AFTER PyPI
  publish succeeds (Docker buildx, branch-sync, gh-release, dev-bump): use
  GitHub's re-run-failed-jobs on the same run — the tag stays; manual
  completion only if a re-run cannot recover.

### Provisioning completion
- **D-09:** Guided checkpoint session as the FIRST plan of the phase — walk
  `05.4-PROVISIONING.md`'s pre-first-tag checklist item-by-item: agent
  presents exact values to enter, user clicks through provider UIs
  (PyPI, Docker Hub, RTD, GitHub settings), agent verifies each item via
  `gh api`/repo state where verifiable and checks it off in the runbook.
  Provisioning has no code dependencies, so surprises surface earliest.
- **D-10:** The one-time `stable/3.0.x` ancestry merge (`git merge -s ours`)
  is run by the USER on main; the agent preps the exact command sequence and
  verifies `merge-base --is-ancestor` afterward. Must be a real merge commit —
  a rebase/squash-merged PR would destroy the merge parent and branch-sync
  would fail.
- **D-11:** Docker Hub credentials via an org access token (OAT) on the
  `datafolklabs` org — repo-scoped, cleanest blast radius. Requires Docker
  Team/Business; if the plan turns out not to support OAT at the checkpoint,
  fall back per runbook section 4 (bot-account PAT preferred over maintainer
  PAT).

### Post-release wrap-up scope
- **D-12:** Phase end = through dev-bump merge: PyPI + Docker + GitHub Release
  live, dev-bump PR merged (VERSION `(3, 0, 17, ...)` + fresh
  `## 3.0.17 - DEVELOPMENT` section), and REL-01..05 / CI-04 / DOCS-03 flipped
  with a VERIFICATION.md. The emitted post-release checklist issue (GitBook
  docs, notifications) stays open beyond the phase.
- **D-13:** REL-04 verification is a single clean-venv check: `pip install
  cement==3.0.16` from production PyPI + import + minimal `App().run()`
  round-trip. The 5-Python matrix already proved the identical artifact from
  TestPyPI inside the release run.
- **D-14:** The phase drafts the release announcement copy (highlights-based,
  from the finalized changelog) as a small artifact the user can paste into
  the mailing list / Slack. Sending remains human (05.4 D-15 unchanged).
- **D-15:** Milestone completion is a separate follow-up session — Phase 6
  ends at requirement flips + VERIFICATION.md; the user invokes
  `/gsd-complete-milestone` afterward.

### Claude's Discretion
- Exact plan/wave decomposition (provisioning-first is locked; the rest may
  parallelize where file ownership allows).
- Mechanics of the git-log cross-check (commit classification, filtering
  planning-artifact commits per CLAUDE.md changelog rules).
- Shape/wording of the condensed changelog entries and the highlights
  paragraph (user reviews via the release-prep PR).
- Announcement-copy format and where the draft artifact lives.
- How dry-run/live-run monitoring is reported back during execution
  (checkpoint cadence while the ~30–40 min runs are in flight).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Release machinery & runbook (Phase 05.4 outputs — the contract this phase executes)
- `.planning/phases/05.4-github-actions-release-workflow/05.4-PROVISIONING.md` —
  the pre-first-tag checklist D-09's guided session walks, provider-exact
  values, Docker Hub token paths (§4), RTD moving-tag model (§5),
  `stable/3.0.x` ancestry merge procedure (§6), known accepted tradeoffs.
- `.planning/phases/05.4-github-actions-release-workflow/05.4-CONTEXT.md` —
  locked release-flow decisions D-01..D-16 carried into this phase.
- `.github/workflows/release.yml` — the pipeline this phase runs: preflight →
  gates → build → TestPyPI publish + smoke → approval → publish side
  (PyPI, Docker, tag-sync, branch-sync, gh-release, dev-bump, checklist issue).
- `.github/workflows/gates.yml` — reusable gate suite invoked by both PR CI
  and the release run.
- `scripts/testpypi-smoke.py`, `scripts/bump_dev_version.py` — smoke and
  dev-bump mechanics referenced by the run.

### Version & changelog (the files the release-prep PR touches)
- `CHANGELOG.md` — `## 3.0.15 - DEVELOPMENT` section (~540 lines) to audit,
  condense, and rename per D-01..D-04; header convention from
  `## 3.0.14 - May 5, 2025`.
- `cement/core/backend.py` — `VERSION = (3, 0, 15, 'final', 0)` is the single
  version of record (pyproject reads it via `[tool.pdm.version]` source=call);
  bump to `(3, 0, 16, 'final', 0)` in the release-prep PR.

### Project-level constraints
- `.planning/ROADMAP.md` — Phase 6 goal + 5 locked success criteria.
- `.planning/REQUIREMENTS.md` — REL-01..REL-05, CI-04, DOCS-03 definitions and
  the traceability table this phase flips.
- `CLAUDE.md` — changelog maintenance rules (bucket taxonomy, planning-artifact
  filtering) governing the D-01 cross-check, branching policy governing D-05.

### External
- https://github.com/datafolklabs/cement/issues/791 — the manual checklist the
  automation replaces; the post-release checklist issue mirrors its style.
- https://github.com/datafolklabs/cement/actions/runs/29212487225 — the GREEN
  CI-04 dry-run baseline (what "working" looks like).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- The entire release pipeline is built and validated — this phase RUNS it; no
  workflow code changes are expected. If a workflow bug surfaces, fixes follow
  the 05.4 precedent (small PR, re-dispatch dry-run).
- `workflow_dispatch` dry-run mode (05.4 D-06) is the rehearsal vehicle for
  D-06's final pre-tag validation.
- `scripts/bump_dev_version.py` handles the post-release 3.0.17 bump inside
  the workflow's dev-bump job — the phase only merges the resulting PR.
- Provisioned already: `testpypi` GitHub Environment + TestPyPI trusted
  publisher (the two dry-run items). Everything else on the pre-first-tag
  checklist is open as of 2026-07-12.

### Established Patterns
- Conventional Commits + 78-char wrap; `docs(06):` prefix for planning
  artifacts; no direct commits to main (D-05/D-10 both respect this).
- `make audit-public-api` byte-for-byte green across every commit (Phase 3
  D-04 lineage) — applies to the release-prep PR too.
- 100% coverage + ruff + mypy gates hold; the release-prep PR triggers full
  PR CI (gates.yml) before merge.
- Checkpoint/human-verify pattern from 05.4-05 (provisioning confirmed via
  checkpoint) — D-09's guided session reuses it.

### Integration Points
- Tag `3.0.16` on main → `release.yml` (trigger pattern matches unprefixed
  `3.*` tags).
- `release` GitHub Environment approval = the user, in the GitHub UI, at the
  single publish gate.
- Dev-bump PR is `GITHUB_TOKEN`-authored → shows zero CI checks
  (anti-recursion; accepted tradeoff #1 in the runbook) — merging it is a
  deliberate human step; main CI runs post-merge.
- `stable/3.0.x` fast-forward and RTD moving tags `3`/`3.0` are handled by
  the workflow's branch-sync/tag-sync jobs — but only AFTER the D-10 ancestry
  merge lands.

</code_context>

<specifics>
## Specific Ideas

- Highlights paragraph themes (D-03): Python 3.10–3.14 matrix, warn-only
  deprecations with 3.2.0 removals signposted, automated release workflow,
  fully-typed modernized `cement generate` templates.
- "The human act of tagging is the source of truth" — the agent's job is to
  make that act zero-risk (verified SHA, green pre-checks, exact commands),
  not to perform it.
- Announcement copy should read from the finalized changelog highlights, not
  be written fresh — one source of truth for what shipped.

</specifics>

<deferred>
## Deferred Ideas

- Post-release checklist issue execution (GitBook docs, mailing list, Slack
  sends) — human work that outlives the phase; tracked by the auto-created
  issue, not by phase plans.
- Milestone archive — user runs `/gsd-complete-milestone` in a separate
  session after Phase 6 verifies (D-15).
- Full-commit-SHA action pinning tightening for community actions — runbook
  "known accepted tradeoffs" #2; revisit post-release if desired.

### Reviewed Todos (not folded)
- `2026-05-09-document-optional-features-in-gitbook-post-3-0-16.md` — GitBook
  developer docs for ext.generate optional features (#778). Stays on the
  emitted post-release checklist (05.4 D-16); blocked on the release itself.
- `2026-07-11-update-gitbook-todo-tutorial-for-pdm-backend.md` — GitBook
  todo-tutorial walkthrough update for pdm-backend. Same disposition:
  post-release GitBook work on the emitted checklist.

</deferred>

---

*Phase: 06-release-cut-3-0-16*
*Context gathered: 2026-07-12*
