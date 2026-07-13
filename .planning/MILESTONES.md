# Milestones

## 3.0.16 Clean & Green (Shipped: 2026-07-13)

**Delivered:** Cement 3.0.16 — a maintenance/modernization release on the
strict no-public-API-breakage 3.0.x track, live on PyPI/Docker Hub/GitHub with
a fully automated release pipeline and main advanced to the 3.0.17 dev cycle.

**Stats:** 11 phases, 50 plans, 99 tasks, 7 quick tasks · 2026-04-24 →
2026-07-13 (81 days) · release SHA `1173c469` · release run 29263984129

**Key accomplishments:**

- Modernized the entire quality toolchain — ruff `~=0.15.12` (185 violations
  resolved across 8 new rule families), mypy `~=1.20.2`, pytest 9.x — dropped
  EOL Python 3.9, and expanded the CI matrix to 3.10–3.14 + pypy3.10/3.11,
  holding the absolute 100% coverage gate green through every commit.
- Refreshed the dependency baseline: lockfile regenerated (redis 7.4, watchdog
  6.0, sphinx 8.1 et al.), pip-audit CVE disposition (11 CVEs, all accepted as
  dev/docs transitives — core stays zero-runtime-dependency), GitHub Actions
  pinned to exact tags with Dependabot backstop.
- Internal-only refactor under a new byte-for-byte public-API audit gate
  (`make audit-public-api`, 1014-entry frozen baseline): pathlib migration,
  `__future__` annotations strip, Any-tightening, and a locked-vocabulary
  audit of all 141 `pragma: nocover` sites — zero public-API drift.
- Rebuilt the `generate` extension's variable engine (#782): unified typed
  variables (`type: string|boolean|choice`) with `extend:` conditional
  effects and `requires:` gating; all 5 CLI templates modernized to
  pdm-backend packaging, fully typed, comply/test-green out of the box, and
  enforced by a new cli-smoke-test CI matrix.
- Shipped an automated GitHub Actions release pipeline (reusable `gates.yml`
  + `release.yml`): OIDC trusted publishing, TestPyPI dry-run path with
  5-Python smoke, single release-environment approval gate, Docker multi-arch
  publish, branch/tag sync, changelog-derived GitHub Release, and automated
  dev-bump PR — replacing the manual release checklist (#791).
- Cut 3.0.16 live end-to-end: warn-only deprecations signposted for 3.2.0,
  finalized changelog, tag-triggered publish to PyPI (verified via
  independent clean-venv install), GitHub Release, `stable/3.0.x`
  fast-forward, moving tags `3`/`3.0`, and dev cycle reopened as 3.0.17.

**Known deferrals (not gaps):** post-release notification checklist (issue
#797, paste-ready copy in the phase 6 announcement draft); `release.yml`
post-release-checklist job fix + RTD force-tag trigger check (phase 6
`deferred-items.md`); GitBook todo-tutorial pdm-backend update (pending todo,
docs-sweep candidate).

**Archives:**
- `.planning/milestones/3.0.16-ROADMAP.md`
- `.planning/milestones/3.0.16-REQUIREMENTS.md`

**Release markers:** product tag `3.0.16` (no separate GSD milestone tag —
the product tag is the release marker).
