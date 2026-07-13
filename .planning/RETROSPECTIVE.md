# Retrospective: Cement

Living document — one section per milestone, appended at each milestone close.

## Milestone: 3.0.16 — Clean & Green

**Shipped:** 2026-07-13
**Phases:** 11 (6 planned + 5 inserted decimals) | **Plans:** 50 (+7 quick tasks)
**Timeline:** 2026-04-24 → 2026-07-13 (81 days)

### What Was Built

A maintenance/modernization release on the strict no-breakage 3.0.x track:
current ruff/mypy/pytest toolchain, Python 3.9 dropped (matrix 3.10–3.14 +
pypy), dependencies refreshed with CVE disposition, an internal refactor held
byte-for-byte by a new public-API audit gate, a rebuilt typed-variables engine
for the generate extension (#782), all 5 CLI templates modernized and
CI-enforced, warn-only deprecations signposted for 3.2.0, and a fully
automated GitHub Actions release pipeline that shipped 3.0.16 live to
PyPI/Docker/GitHub on its first real run.

### What Worked

- **Baseline-first sequencing** — unblocking tooling/deps/CI before refactor
  meant every later phase inherited a green gate instead of fighting it.
- **The public-API audit gate** (`make audit-public-api`, frozen baseline) —
  converted "don't break downstream" from a review judgment into a
  byte-for-byte mechanical check; the whole refactor shipped with zero drift.
- **Provisioning-first release phase (D-09)** — doing provider-UI setup as
  Plan 1 of the release phase surfaced both hard blockers (Docker secrets,
  branch ancestry) days before the tag, and caught a wrong-scope secret
  placement that would have failed the live Docker job.
- **Dry-run against finalized bytes (D-06/Pitfall 3)** — the TestPyPI
  immutability constraint forced the discipline of only dry-running the
  merged commit, so the live run re-smoked identical artifacts.
- **Human-gated checkpoints for live actions** — tag push, environment
  approval, and merges stayed with the user; agents proved preconditions and
  verified outcomes. No irreversible action was automated.

### What Was Inefficient

- **Verification claims vs. live behavior** — the demo README's expected
  output tree contradicted shipped `requires:` gating semantics and survived
  until a post-release doc task ran the artifact for real. Lesson feeds the
  planned docs-sweep: verify doc claims by execution, not by reading.
- **Stale tracking debt at close** — two long-done quick tasks and one done
  todo were still "open" at milestone close because older summary formats
  lacked `status:` frontmatter; cost a cleanup pass during close.
- **Release workflow's only failure was its own notification job** — the
  `post-release-checklist` job shipped with an untested `gh issue create`
  invocation (no checkout/`-R`); it was unrecoverable by rerun and needed
  manual completion. Notification-only paths deserve dry-run coverage too.
- **RTD rebuild didn't auto-trigger** on force-updated moving tags; the
  3.0.16 docs needed a manual build. Trigger path unverified before the cut.

### Patterns Established

- Conventional Commits with per-concern atomicity; `[area]` CHANGELOG
  entries maintained phase-by-phase, finalized (not written) at release cut.
- AUDIT POINT comments codifying tool-surface decisions in pyproject.toml.
- Locked-vocabulary `pragma: nocover` categorization (141 sites).
- Reusable `gates.yml` as the single source of truth for PR CI and release
  gates; release preflight guards (changelog finalized, version==tag).
- Evidence-cited verification: every requirement flip carries a run id /
  release URL / clean-venv proof.

### Key Lessons

1. Release provisioning is live state — re-verify it at execution time even
   when research checked it days earlier (secrets moved scope between).
2. GitHub environment secrets are invisible to jobs that don't declare the
   environment; repository scope is the right home for cross-job secrets.
3. A `requires:`-gated variable resolves to its default (extend rules
   skipped) — cascade cleanup belongs on the prerequisite's decline branch.
4. Squash-merging a phase branch then continuing on it needs an immediate
   reset onto the squash commit, or the next `git pull` creates a rebase
   mess (happened once; recovered cleanly).

### Cost Observations

- Executor model: opus for all plan execution; sonnet for verification.
- Phase 6 ran ~5 subagent plan executions + independent verifier + code
  review, with all human gates (provisioning, PR merges, tag push, release
  approval) turned around same-day.

## Cross-Milestone Trends

| Milestone | Phases | Plans | Days | Notable |
|-----------|--------|-------|------|---------|
| 3.0.16 Clean & Green | 11 | 50 | 81 | First GSD-run milestone; first automated release |
