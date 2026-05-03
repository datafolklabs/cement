---
description: Create a clean PR from the current branch — code-only diff for review, plus a follow-up archive commit for the .planning/ artifacts after merge.
---

# /pr — Create a PR (code-clean) + archive plan

Produces the four things BJ wants every time:

1. **PR title** — under 70 chars, Conventional-Commits style.
2. **PR body** — markdown, written to `/tmp/<branch>-pr-body.md`.
3. **Clean PR branch** — `<branch>-pr` with transient `.planning/` files
   filtered out (only code + structural planning state remains).
4. **Two commands** the user runs themselves:
   - The `gh pr create` for the code PR.
   - The post-merge archive command for `.planning/phases/...`.

Never auto-pushes, never auto-creates the PR, never auto-pushes the archive.

## Process

### 1. Detect state
- Confirm we're on a feature branch (not `main`).
- Confirm there are commits ahead of `main`.
- If working tree is dirty, stop and ask the user to resolve first.

### 2. Read the work
- Read the relevant `.planning/phases/<phase>/<phase>-VERIFICATION.md`
  (or whichever artifact captures phase acceptance) for body source-of-truth.
- Read `git log main..HEAD --reverse --format='%h %s'` to enumerate commits.
- Read the commit-by-commit diff stat for body grounding (no guessing).

### 3. Run /gsd-pr-branch
Invoke the skill at `~/.claude/get-shit-done/workflows/pr-branch.md` to
build `<branch>-pr` from `main`. **Important fix vs the raw skill:**
when filtering transient `.planning/` paths during cherry-pick, only
`git reset HEAD --` paths the cherry-pick **added** (don't blanket
`git rm --cached` whole directories — that deletes pre-existing phase
archives like `01-...` and `01.1-...`).

Verify post-build:
```bash
git diff --name-only main..<branch>-pr | grep -E '^\.planning/(phases|quick|research|threads|todos|debug|seeds|codebase|ui-reviews)/'
# expect: empty
```

### 4. Write the PR body
- Write to `/tmp/<branch>-pr-body.md`.
- Sections: `## Summary`, themed groupings of changes (use the phase
  plan's wave/plan structure), `## Acceptance status` table if the
  phase has D-NN acceptance, `## Files touched`, `## Test plan` checklist.
- Keep it concrete. Reference plan numbers, commit themes, exact
  versions when relevant. No marketing fluff.

### 5. Print the deliverables

Print, in this order:

1. **PR title** (one line, no quoting).
2. **PR body location** (`/tmp/<branch>-pr-body.md`).
3. **Code PR command** — exact `gh pr create` invocation:
   ```bash
   gh pr create -R <owner>/<repo> \
     --base main --head <branch>-pr \
     --title "<title>" \
     --body-file /tmp/<branch>-pr-body.md
   ```
4. **Post-merge archive command** — exact 3-line recipe to land the
   filtered-out planning commits on `main` after the PR merges:
   ```bash
   # Run AFTER the code PR is merged:
   git checkout main && git pull
   git checkout <original-branch> -- .planning/phases/<phase-dir>/
   git commit -m "docs(<phase-tag>): archive planning artifacts" && git push
   ```
   Replace `<phase-dir>` with the actual phase directory; commit-message
   tag follows the phase's existing `docs(...)` prefix style.

### 6. Stop
Do not push. Do not run `gh pr create`. Do not push the archive. The
user runs both commands themselves so the PR / push / merge cadence
stays in their hands.

## Why two commands

The code PR is what reviewers look at — `.planning/` noise dilutes
review. The planning archive is write-once history that lives on `main`
for future reference (matches how phase 01 / 01.1 archives sit on `main`
today). They're separate concerns; merging them into one PR re-creates
the noise problem.

## Triggers

User phrases that should invoke this:
- "create a pr"
- "suggest a pr"
- "open a pr"
- "ship this" (when not invoking `/gsd-ship`)

If the user says `/gsd-ship`, defer to that skill instead — it has its
own review/merge orchestration.
