# Requirements: Cement 3.0.16 — Clean & Green

**Defined:** 2026-04-24
**Core Value:** Cement 3 stays solid, secure, performant, and bug-free under strict backward compatibility — while being continuously maintained against a modern Python and tooling ecosystem.

## v1 Requirements

Requirements for the Clean & Green milestone (releases as Cement 3.0.16). Each maps to a roadmap phase. Every requirement must hold backward compatibility — no public API changes.

### Tooling Baseline

- [x] **TOOL-01**: Latest stable `ruff` adopted; `make comply-ruff` exits clean across `cement/` and `tests/`
- [x] **TOOL-02**: Latest stable `mypy` adopted; `make comply-mypy` exits clean with project's strict configuration
- [x] **TOOL-03**: `pytest`, `pytest-cov`, `coverage` upgraded to current stable; `make test` runs without deprecation warnings from the test framework itself
- [x] **TOOL-04**: `ruff` and `mypy` rule configuration in `pyproject.toml` reviewed and codified (no implicit rule drift on next tool bump)

### Dependencies

- [ ] **DEPS-01**: `pdm.lock` regenerated against current package indexes; lockfile matches latest non-breaking versions
- [ ] **DEPS-02**: Optional-extras dependencies (yaml, jinja2, mustache, colorlog, redis, memcached, watchdog, etc.) upgraded to current stable releases compatible with Python 3.10–3.14
- [ ] **DEPS-03**: Any runtime dep with a known unpatched CVE is resolved or pinned with documented rationale
- [ ] **DEPS-04**: Scheduled `pdm update` GitHub Action unblocked — runs cleanly to completion against the new baseline

### CI Pipeline

- [ ] **CI-01**: GitHub Actions test matrix runs Python 3.10, 3.11, 3.12, 3.13, 3.14 — all green
- [ ] **CI-02**: Compliance jobs (ruff, mypy) run on every PR and pass
- [ ] **CI-03**: Coverage job enforces 100% coverage gate on every PR — fails build below 100%
- [ ] **CI-04**: Release workflow validated end-to-end against TestPyPI before the 3.0.16 cut
- [ ] **CI-05**: Action versions (checkout, setup-python, etc.) pinned to current and updated where outdated

### Python Version Policy

- [x] **PYVER-01**: Python 3.9 removed from `pyproject.toml` `python-requires` and CI matrix (EOL Oct 2025 per upstream policy)
- [x] **PYVER-02**: Python 3.10 declared as minimum supported version across pyproject, docs, README, and CI
- [x] **PYVER-03**: No 3.9-only compat shims remain in source (verified by grep + linter pass)

### Test Coverage

- [x] **COV-01**: `make test` produces 100% coverage report; any drift from prior 100% baseline is closed before milestone completion — Validated in Phase 03 Plan 01 (audit gate installed; coverage at 100% with 316 passing tests)
- [x] **COV-02**: Coverage HTML report (`coverage-report/`) generates without warnings — Verified mid-phase in Phase 03 Plan 03 (Wave 3 wave-end check: `coverage-report/index.html` exists; `pytest --cov=cement` exits 0 with 100% coverage 3290/3290 stmts)
- [ ] **COV-03**: `pragma: no cover` exclusions audited — each remaining one has a code comment justifying it

### Documentation

- [ ] **DOCS-01**: `make docs` builds Sphinx docs without warnings or broken cross-references
- [ ] **DOCS-02**: README, CONTRIBUTING, and getting-started examples accurate against the 3.0.16 release
- [ ] **DOCS-03**: Changelog updated for 3.0.16 with all user-visible changes (deprecations, dep bumps, Python matrix)
- [ ] **DOCS-04**: Public API docstrings reviewed for staleness; broken/outdated examples corrected

### Issue Backlog Triage

- [ ] **TRIAGE-01**: Open GitHub issues exported and bucketed (close-stale, close-wontfix, close-duplicate, real-bug, feature-request, question)
- [ ] **TRIAGE-02**: User-approved batch closures applied with consistent comment template explaining policy
- [ ] **TRIAGE-03**: Surviving issues labeled (`bug`, `cement-3-fix`, `cement-4-candidate`, `docs`, `help-wanted`) and prioritized
- [ ] **TRIAGE-04**: Real bugs discovered during triage either fixed in this milestone or recorded as backlog items with explicit deferral rationale

### Internal Refactor

- [ ] **REFACTOR-01**: Dead code identified (vulture / coverage diff) and removed without affecting public API or test coverage
- [x] **REFACTOR-02**: Type hints tightened in `cement/core/` — fewer `Any`, more precise generics where mypy strict mode allows
- [x] **REFACTOR-03**: `os.path` usage in `cement/utils/fs.py` and core internals migrated to `pathlib` where it doesn't change public signatures — Closed in Phase 03 Plan 06 (Wave 6 — pathlib migration). 33 → 1 (tagged) os.path callsites across the 4 named files (cement/utils/fs.py, cement/core/config.py, cement/core/foundation.py, cement/core/template.py); the 1 surviving site is the public alias `join = os.path.join` in cement/core/foundation.py:48 (in 03-PUBLIC-API-BASELINE.txt with stdlib semantics — retained per D-12/D-14 with inline `# boundary:` tag). os.walk(src) in cement/core/template.py also retained with `# boundary: D-14` (no pathlib equivalent for triple-tuple yield). D-24 conjunct #8 GREEN.
- [x] **REFACTOR-04**: Modern stdlib idioms applied where backward-compatible (f-strings everywhere, contextlib helpers, `functools.cached_property`) — Closed mechanically in Phase 03 Plan 03 (UP031 + UP032 cascade resolved all printf-style and `.format()` callsites; protected `.format(**template_dict)` template-substitution sites preserved per D-19; `cached_property` / `contextlib.suppress` adoption was opportunistic per D-19 — none surfaced as obvious wins)

### Deprecations

- [ ] **DEPREC-01**: Surfaces flagged for removal in 3.2.0 / Cement 4 emit `DeprecationWarning` with migration guidance in the message
- [ ] **DEPREC-02**: Each new deprecation is documented in the changelog and a dedicated `docs/source/deprecations.rst` page
- [ ] **DEPREC-03**: Test suite asserts each deprecation warning fires (so removal in 3.2.0 has a concrete test failure as its cue)

### Security Audit Tooling (Stubbed)

- [ ] **SEC-01**: Backlog item recorded for adding `pip-audit` to CI — phase-shaped specification, not implemented this milestone
- [ ] **SEC-02**: Backlog item recorded for adding `bandit` static analysis — phase-shaped specification, not implemented this milestone
- [ ] **SEC-03**: Backlog item recorded for evaluating CodeQL or Semgrep SAST coverage — phase-shaped specification, not implemented this milestone

### Release

- [ ] **REL-01**: Version bumped to `3.0.16` across `cement/__init__.py`, `pyproject.toml`, and any other version-of-record locations
- [ ] **REL-02**: Pre-release smoke-test on TestPyPI passes (install + import + minimal app round-trip on each supported Python)
- [ ] **REL-03**: `3.0.16` git tag created, GitHub release notes published with changelog
- [ ] **REL-04**: PyPI publish completed; version installs cleanly on Python 3.10–3.14
- [ ] **REL-05**: Post-release version bumped to `3.0.17` (odd = next dev cycle)

## v2 Requirements

Deferred to a later milestone (likely the 3.2.0 breakage-allowed cycle or a dedicated security/perf milestone).

### Security Audit Tooling Implementation

- **SECv2-01**: `pip-audit` integrated into CI on every PR
- **SECv2-02**: `bandit` integrated into CI on every PR with project-tuned ruleset
- **SECv2-03**: SAST tool (CodeQL or Semgrep) selected and integrated into CI
- **SECv2-04**: Documented security disclosure process (`SECURITY.md`)

### Performance Pass

- **PERF-01**: Profile App.setup() / App.run() / handler dispatch hot paths; benchmark against 3.0.14 baseline
- **PERF-02**: Address measured regressions with backward-compatible optimizations
- **PERF-03**: Add benchmarking suite to CI as a regression detector

### Cement 3.2.0 Breakage Cycle

- **BREAK-01**: Remove all surfaces deprecated in 3.0.16 per their migration guidance
- **BREAK-02**: Apply breaking-allowed cleanups blocked by no-breakage in 3.0.x
- **BREAK-03**: Bump to 3.2.0 release per odd/even convention

## Out of Scope

| Feature | Reason |
|---------|--------|
| Public API breaking changes | 3.0.x track is strict no-breakage; reserved for 3.2.0 / Cement 4 |
| Major architectural refactors | Cement 4 territory only; even 3.2.0 holds the architecture line |
| Cement 4 rewrite work | Separate future effort with zero compat constraints |
| New framework features | This is a maintenance/cleanup milestone; features defer to dedicated milestones |
| Removing currently deprecated APIs | Land removals in 3.2.0; this cycle only adds new warnings |
| Rolling out audit tooling (pip-audit / bandit / SAST) | Stubbed as a follow-up milestone — adding to red-baseline CI multiplies noise |
| Performance optimization beyond regressions | Reserved for a dedicated performance milestone |
| Migrating away from PDM | PDM is working; not in scope |
| Migrating from argparse to click/typer | Public API would change; out of scope on 3.0.x |

## Traceability

Populated by the roadmapper during phase mapping.

| Requirement | Phase | Status |
|-------------|-------|--------|
| TOOL-01 | Phase 1 | Complete |
| TOOL-02 | Phase 1 | Complete |
| TOOL-03 | Phase 1 | Complete |
| TOOL-04 | Phase 1 | Complete |
| DEPS-01 | Phase 2 | Pending |
| DEPS-02 | Phase 2 | Pending |
| DEPS-03 | Phase 2 | Pending |
| DEPS-04 | Phase 2 | Pending |
| CI-01 | Phase 2 | Pending |
| CI-02 | Phase 2 | Pending |
| CI-03 | Phase 2 | Pending |
| CI-04 | Phase 6 | Pending |
| CI-05 | Phase 2 | Pending |
| PYVER-01 | Phase 1 | Complete |
| PYVER-02 | Phase 1 | Complete |
| PYVER-03 | Phase 1 | Complete |
| COV-01 | Phase 3 | Validated (Phase 03 Plan 01) |
| COV-02 | Phase 3 | Verified mid-phase (Phase 03 Plan 03) |
| COV-03 | Phase 3 | Pending |
| DOCS-01 | Phase 5 | Pending |
| DOCS-02 | Phase 5 | Pending |
| DOCS-03 | Phase 6 | Pending |
| DOCS-04 | Phase 5 | Pending |
| TRIAGE-01 | Phase 4 | Pending |
| TRIAGE-02 | Phase 4 | Pending |
| TRIAGE-03 | Phase 4 | Pending |
| TRIAGE-04 | Phase 4 | Pending |
| REFACTOR-01 | Phase 3 | Pending |
| REFACTOR-02 | Phase 3 | Complete |
| REFACTOR-03 | Phase 3 | Validated (Phase 03 Plan 06) |
| REFACTOR-04 | Phase 3 | Closed (Phase 03 Plan 03 — UP031+UP032 cascade) |
| DEPREC-01 | Phase 5 | Pending |
| DEPREC-02 | Phase 5 | Pending |
| DEPREC-03 | Phase 5 | Pending |
| SEC-01 | Phase 5 | Pending |
| SEC-02 | Phase 5 | Pending |
| SEC-03 | Phase 5 | Pending |
| REL-01 | Phase 6 | Pending |
| REL-02 | Phase 6 | Pending |
| REL-03 | Phase 6 | Pending |
| REL-04 | Phase 6 | Pending |
| REL-05 | Phase 6 | Pending |

**Coverage:**
- v1 requirements: 42 total
- Mapped to phases: 42
- Unmapped: 0

---
*Requirements defined: 2026-04-24*
*Last updated: 2026-04-24 after roadmap mapping*
