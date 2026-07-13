# Deferred Items — Phase 06 (release-cut-3-0-16)

Out-of-scope discoveries logged during execution. Do NOT fix inline; address as
separate issues/tasks.

## 1. release.yml `post-release-checklist` job cannot create its issue

- **Found during:** Plan 06-04 Task 2 (live 3.0.16 release run 29263984129)
- **Symptom:** Job fails with `failed to run git: fatal: not a git repository`
  at the `gh issue create` step; run conclusion flips to `failure` even though
  every release-critical job succeeded.
- **Root cause:** The job (by design) has no `actions/checkout` step, and
  `gh issue create` is invoked without `-R`/`GH_REPO`, so the gh CLI tries to
  infer the repository from a git checkout that does not exist.
- **Fix (future):** Add `-R "$GITHUB_REPOSITORY"` to the `gh issue create`
  invocation (or set `GH_REPO: ${{ github.repository }}` in the step env) in
  `.github/workflows/release.yml`. Deterministic bug — `gh run rerun --failed`
  cannot recover it (same workflow snapshot).
- **Manual completion applied (D-08):** Checklist issue created by hand as
  https://github.com/datafolklabs/cement/issues/797 with the exact body the
  job would have emitted (NEXT=3.0.17). The 3.0.16 tag stays.

## 2. RTD did not auto-rebuild on force-updated moving tags (3 / 3.0)

- **Found during:** Plan 06-04/06-05 (live 3.0.16 release, post `tag-sync`)
- **Symptom:** The `tag-sync` job force-repointed the moving tags `3` and
  `3.0` to the release SHA, but Read the Docs did not trigger a rebuild of
  the corresponding versioned docs; the user ran a manual RTD build to
  publish them.
- **Root cause (suspected):** RTD's webhook/automation-rule path may not
  fire (or may be ignored) for force-updated existing tags, as opposed to
  newly created tags/branches. Trigger path unverified.
- **Fix (future):** Before the next release cut, verify RTD's automation
  rules and GitHub webhook handle force-updated tags; adjust the rule or
  add an explicit RTD build-trigger step to release.yml if needed.
- **Operational note:** If a stale build persists after a manual trigger,
  wipe the RTD build cache (Builds -> wipe) before rebuilding.
