# Phase 2 — pip-audit Spot Check

**Run date:** 2026-05-02 (post-`pdm update` from Plan 01 commit `9f0f8627`)
**Scope:** dev venv synced to Plan 01's `pdm.lock` (cement + dev group +
`[colorlog,jinja2,yaml,redis,memcached,mustache,tabulate,watchdog,docs]`
extras as resolved by `pdm install`)
**Tool:** pip-audit 2.10.0 (ad-hoc — see CONTEXT.md D-03; NOT a permanent
dev dep, NOT a Makefile target, NOT a recurring CI job — Phase 5 SEC-01
owns those surfaces)
**Sources:** PyPI Advisory DB (default vulnerability service)
**Invocation path:** `pdm run python -m pip install pip-audit && pdm run
pip-audit --format markdown && pdm run python -m pip uninstall -y
pip-audit` (Path A from RESEARCH.md § "pip-audit Invocation Mechanics" —
recommended; pipx and uv unavailable on this host). `pdm.lock` confirmed
byte-identical pre/post-run via `git status pdm.lock`.

## Pre-update baseline (informational)

Captured in RESEARCH.md § "pip-audit Pre-Update Snapshot" against
pre-`pdm update` venv (2026-05-02): **16 known vulnerabilities in 6
packages**.

| Pkg      | Ver     | CVE             | Fix Versions    | Notes                          |
| -------- | ------- | --------------- | --------------- | ------------------------------ |
| certifi  | 2024.2.2 | PYSEC-2024-230  | 2024.7.4        | transitive (requests, sphinx)  |
| idna     | 3.6     | PYSEC-2024-60   | 3.7             | transitive (requests, sphinx)  |
| pip      | 25.3    | CVE-2026-1703   | 26.0            | build env tool                 |
| pip      | 25.3    | CVE-2026-3219   | -               | NO FIX — accept; build env     |
| pygments | 2.17.2  | CVE-2026-4539   | 2.20.0          | transitive (sphinx, pytest)    |
| requests | 2.31.0  | CVE-2024-35195  | 2.32.0          | dev dep                        |
| requests | 2.31.0  | CVE-2024-47081  | 2.32.4          | dev dep                        |
| requests | 2.31.0  | CVE-2026-25645  | 2.33.0          | dev dep                        |
| urllib3  | 2.2.1   | CVE-2024-37891  | 1.26.19, 2.2.2  | transitive (requests, sphinx)  |
| urllib3  | 2.2.1   | CVE-2025-50182  | 2.5.0           | transitive (requests, sphinx)  |
| urllib3  | 2.2.1   | CVE-2025-50181  | 2.5.0           | transitive (requests, sphinx)  |
| urllib3  | 2.2.1   | CVE-2025-66418  | 2.6.0           | transitive (requests, sphinx)  |
| urllib3  | 2.2.1   | CVE-2025-66471  | 2.6.0           | transitive (requests, sphinx)  |
| urllib3  | 2.2.1   | CVE-2026-21441  | 2.6.3           | transitive (requests, sphinx)  |

## Post-update results

`pdm run pip-audit --format markdown` against post-Plan-01 venv (commit
`9f0f8627`): **13 known vulnerabilities in 5 packages** (down from 16
in 6). The duplicate certifi/idna rows are pip-audit reporting the
same package once per `[dependency-groups]` membership (`dev` + `docs`)
— the unique-CVE count is **11 across 5 packages**.

Name | Version | ID | Fix Versions
--- | --- | --- | ---
certifi | 2024.2.2 | PYSEC-2024-230 | 2024.7.4
certifi | 2024.2.2 | PYSEC-2024-230 | 2024.7.4
idna | 3.6 | PYSEC-2024-60 | 3.7
idna | 3.6 | PYSEC-2024-60 | 3.7
pip | 25.3 | CVE-2026-1703 | 26.0
pip | 25.3 | CVE-2026-3219 |
pygments | 2.17.2 | CVE-2026-4539 | 2.20.0
urllib3 | 2.2.1 | CVE-2024-37891 | 1.26.19,2.2.2
urllib3 | 2.2.1 | CVE-2025-50182 | 2.5.0
urllib3 | 2.2.1 | CVE-2025-50181 | 2.5.0
urllib3 | 2.2.1 | CVE-2025-66418 | 2.6.0
urllib3 | 2.2.1 | CVE-2025-66471 | 2.6.0
urllib3 | 2.2.1 | CVE-2026-21441 | 2.6.3

Name   | Skip Reason
------ | --------------------------------------------------------------
cement | Dependency not found on PyPI and could not be audited (3.0.15)

## Accepted vulnerabilities

**Disposition rationale (applies to ALL 11 unique findings below):**
The cement core has `dependencies = []` (PROJECT.md / CLAUDE.md "zero
external runtime dependencies for the core framework"). The flagged
packages enter the install graph EXCLUSIVELY via `[dependency-groups].dev`
(local development) and `[project.optional-dependencies].docs` (sphinx
docs-build extra). No downstream `pip install cement[<extra>]` for the
runtime extras (`colorlog`, `jinja2`, `yaml`, `redis`, `memcached`,
`mustache`, `tabulate`, `watchdog`, `cli`) pulls any of these packages.
Verified via `pdm list --tree`: certifi/idna/urllib3 are transitive of
`requests` (dev-group) and `sphinx` (docs-extra) only; pygments is
transitive of `sphinx` (docs-extra) and `pytest` (dev-group) only;
pip is the build-env tool itself (not a dep).

Per CONTEXT.md D-03, these qualify for the Accepted disposition: "DEV-ONLY
... document in 02-PIP-AUDIT.md 'Accepted' section with rationale
'dev-only; not shipped to downstream users'. DO NOT pin-around in
pyproject.toml." Re-evaluation cadence: Phase 5 SEC-01 (security tooling
rollout) — that phase will install pip-audit permanently and run on every
PR, at which point the Accepted set gets re-litigated against the
then-current advisory DB. Until then, no runtime CVE ships in the 3.0.16
release cut.

**Per-finding entries:**

- **pip CVE-2026-3219** — no upstream fix available; build-environment
  tool, not a runtime dep. Re-evaluate at Phase 5 SEC-01 stub work or
  when pip publishes a release containing the patch. (Source: pip
  security advisories — no patched release as of 2026-05-02.)
- **pip CVE-2026-1703** (fix 26.0) — build-environment tool, not a
  runtime dep. PDM provisions the venv pip; users `pip install cement`
  use their own pip. Bumping the venv pip to 26.x is a build-env hygiene
  task, not a runtime mitigation; deferred to Phase 5 SEC-01 alongside
  the recurring pip-audit CI surface.
- **certifi PYSEC-2024-230** (fix 2024.7.4) — transitive only via
  `requests` (dev-group test fixtures) and `sphinx` (docs-extra build).
  Not in any downstream runtime graph. `requests 2.33.1` (Plan 01) does
  not enforce a newer certifi floor; `pdm update --update-reuse` (the
  default strategy that produced Plan 01's lockfile) preserves the
  existing 2024.2.2 pin because no specifier change forces a bump.
- **idna PYSEC-2024-60** (fix 3.7) — same shape as certifi: dev/docs
  transitive only.
- **pygments CVE-2026-4539** (fix 2.20.0) — transitive only via `sphinx`
  (docs-extra) and `pytest` (dev-group). Not in any downstream runtime
  graph. `sphinx 8.1.3` (Plan 01) and `pytest 9.0.3` (Phase 1 D-12 floor)
  both accept pygments >=2.17 but `--update-reuse` preserves 2.17.2.
- **urllib3 CVE-2024-37891** (fix 1.26.19, 2.2.2) — transitive only via
  `requests` (dev) and `sphinx` (docs).
- **urllib3 CVE-2025-50182** (fix 2.5.0) — same shape.
- **urllib3 CVE-2025-50181** (fix 2.5.0) — same shape.
- **urllib3 CVE-2025-66418** (fix 2.6.0) — same shape.
- **urllib3 CVE-2025-66471** (fix 2.6.0) — same shape.
- **urllib3 CVE-2026-21441** (fix 2.6.3) — same shape. urllib3 is upper-
  bounded by `requests <3,>=1.26`, so all listed fix versions (2.x
  series) are reachable in principle; preserved at 2.2.1 by
  `--update-reuse` because no specifier change forced a bump.

## Resolutions applied via Plan 01 `chore(deps): pdm update`

- **requests 2.31.0 -> 2.33.1** (closes CVE-2024-35195, CVE-2024-47081,
  CVE-2026-25645 — 3 dev-dep CVEs from the pre-update baseline). Verified
  in pdm.lock: `name = "requests"` block shows `version = "2.33.1"`.
- **(no other automatic transitive resolutions)** — `pdm update --update-
  reuse` preserved the existing pins for certifi/idna/urllib3/pygments
  because the `requests 2.31->2.33` and `sphinx 7.1->8.1` bumps did not
  tighten their lower bounds enough to force re-resolution. RESEARCH.md
  § "pip-audit Pre-Update Snapshot" optimistically projected these would
  also lift; the actual resolver behavior preserved them under the
  default reuse strategy.

## Pin-arounds applied this plan

(none — all post-update findings are dev-only and/or docs-build-only
transitives; pip CVE-2026-3219 has no upstream fix; remaining urllib3 /
pygments / certifi / idna CVEs documented as Accepted with dev/docs-only
rationale per CONTEXT.md D-03. No `chore(deps): pin <pkg>` commits
landed; no CHANGELOG `[deps]` Misc entries appended; `pyproject.toml`
and `pdm.lock` byte-identical to Plan 01 output.)

## Notes

Phase 2's pip-audit is one-shot — this is NOT a recurring CI surface.
CI integration is Phase 5 SEC-01 territory (PROJECT.md "Out of Scope" and
CONTEXT.md D-03). When that phase lands, the Accepted set above must be
re-litigated against the then-current advisory DB; any then-still-
unfixed CVE either gets a pin-around (if a fix exists upstream) or stays
Accepted with refreshed rationale.

The `--update-reuse` reuse strategy that preserved the dev/docs
transitive pins is the resolver's default. A future phase wishing to
clear these dev-side findings without a downstream-observable change
could run `pdm update --update-eager` against the dev/docs groups
(scoped by `-G dev` / `-G docs`), which would aggressively bump every
non-pinned transitive to its current candidate. That's a hygiene task,
not a 3.0.16 release-cut blocker, and explicitly out of scope per D-03.

D-19 acceptance #4 evidence: this artifact exists; every flagged finding
has explicit disposition (Resolutions applied: 3; Accepted: 11; Pin-
arounds: 0). No silent omissions.
