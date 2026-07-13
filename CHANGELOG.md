# ChangeLog

## 3.0.16 - July 13, 2026

This release modernizes Cement against the current Python ecosystem while
holding the 3.0.x public API stable. Python 3.8 and 3.9 are dropped (EOL) and
the supported matrix is now Python 3.10–3.14. Every deprecation in this release
is warn-only, with removals signposted for 3.2.0 so downstream apps have a clear
upgrade window. A new automated GitHub Actions release workflow replaces the
manual release checklist, and the `cement generate` project and todo-tutorial
templates are now fully typed, PEP 517-buildable, and green under `make comply`
and `make test` out of the box.

Bugs:

- `[core]` Add an explicit `__all__` to `cement/__init__.py` so
  `from cement import *` exports only the intended public surface (App,
  TestApp, Interface, Handler, Controller, the framework exceptions, and
  the documented helpers) instead of leaking every transitively imported
  name — #756
- `[core.foundation]` Honor `Meta.config_section` (not `Meta.label`) when
  applying the `extensions` config override, mirroring the `template_dirs`
  fix — resolves #777
- `[ext.smtp]` Fix `timeout` being passed as `local_hostname` in the SMTP
  constructors
- `[ext.smtp]` Fix a stale variable reference in `_get_params` for
  per-message headers
- `[ext.smtp]` Fix an SMTP connection leak when a send fails with an
  exception
- `[ext.smtp]` Only log on send errors (was logging unconditionally on
  every send)
- `[ext.smtp]` Fix header encoding being incorrectly affected by the
  `body_encoding` setting
- `[cli]` Generated `cement generate project` output now builds under pip's
  default PEP 517 isolation on Python 3.10+ (the legacy `setup.py`
  self-imported the package being built, which fails in isolated build
  envs)
- `[core.handler]` Resolve a mypy union-attr false-positive in handler
  resolution
- `[ext.redis]` Resolve mypy union-attr/arg-type/misc errors surfaced by
  redis 7 typing changes
- `[ext.watchdog]` Drop now-unused `# type: ignore` comments on the
  Observer calls — watchdog 6 ships precise type stubs
- `[utils.fs]` Restore `os.path` semantics in `abspath()` — preserve
  symlink paths and fall through on unknown `~user` prefixes (regression
  from the Phase 03 pathlib migration; restores the 3.0.x BC contract)
- `[dev]` Use explicit `encoding='utf-8'` in `scripts/audit-public-api.py`
  so the `make audit-public-api` gate is portable across non-UTF-8 locales
- `[dev]` Fix `scripts/cli-smoke-test.sh` capturing a CRLF-tainted temp
  path from `docker exec -t` that broke pdm/venv on the first Python
  version (drop `-t` on that one capture)
- `[dev]` Fix `scripts/cli-smoke-test.sh` `pdm install` failing to resolve
  the unreleased dev cement pin by injecting a local find_links source
  (`/src/dist`); harness-only, the project gates are unaffected
- `[core.interface]` Widen the `InterfaceManager.get` `fallback` parameter
  back to `Any` to match the documented contract (it was mechanically
  narrowed by the Phase 03 UP045 sweep; the runtime always accepted
  arbitrary fallback values)
- `[ext.smtp]` Type the message body and `**params` correctly across
  `send`/`_make_message` and the related private helpers (new private
  `_BodyType` alias reflects the dict body shape); drop nine now-unused
  `# type: ignore` suppressions. Public API byte-identical
- `[utils.shell]` Correct the `cmd`/`exec_cmd` return annotations from
  `str` to `bytes` — `subprocess.Popen` returns bytes by default and the
  existing tests assert byte literals; docstrings now point at
  `text=True`/`encoding=` for `str` output (runtime unchanged)
- `[utils.shell]` Correct the `Prompt.Meta.options` annotation from
  `dict | None` to `list[str] | None` to match actual runtime usage
- `[ext.yaml]` Use explicit `template: str | None = None` (PEP 484 /
  RUF013) in `render()` and drop the signature-line `# type: ignore`
- `[ext.mustache]` Use explicit `template: str | None = None` (PEP 484 /
  RUF013) in `render()`; scope the remaining `# type: ignore` to the load
  callsite
- `[utils.misc]` Make `MinimalLogger.__init__` idempotent — guard the
  console-handler add on `not self.backend.handlers` so repeated
  `minimal_logger(ns)` calls no longer stack duplicate handlers (which
  caused log output to repeat N times)
- `[ext.daemon]` Remove a duplicate module-scope
  `LOG = minimal_logger(__name__)` rebind
- `[core.template]` Replace the fragile bare `assert` in
  `TemplateHandler.copy()` with an explicit `NotADirectoryError` (the
  assert was stripped under `python -O` and passed for regular files).
  **Compatibility note:** the raised exception type changes from
  `AssertionError` to `NotADirectoryError`
- `[core.interface]` String-quote a `list[str]` return annotation for
  autodoc compatibility
- `[core.deprecations]` Drop a trailing period from the `3.0.10-1`
  deprecation message (it rendered as `..` once `deprecate()` appended
  its suffix)
- `[dev]` `make docs` zero-warnings gate now uses `&&` (was `;`) so it
  fails on Sphinx warnings
- `[ext.generate]` Fix the `variables` default from `{}` to `[]` — the
  generate flow iterates `variables` as a list of dicts
- `[ext.generate]` Narrow the dynamic-template-module `except` to
  `(AttributeError, ModuleNotFoundError)` with a name guard so transitive
  import errors in a user's template module propagate normally
- `[ext.generate]` `type: boolean` variables now emit a real Python bool
  at the top level (`data[name]`) so `{% if feature_x %}` works; boolean
  prompts use a vars-style `[(Y)es/(N)o]` format in a single
  declaration-order pass — resolves #782 (the `features:` namespace is
  removed)
- `[cli]` Generated `cement generate todo-tutorial` output now builds under
  PEP 517 isolation on Python 3.10+ (mirrors the `generate project` fix) —
  #735
- `[cli]` Fix a `NameError` in generated `todo/main.py` (now
  `except TodoError as e:`) — #735
- `[cli]` Fix a false-green assertion in the generated project test
  template — a membership check replaces `str.find()`, which returned a
  truthy `-1` and never failed — #735
- `[cli]` Generated todo-tutorial imports are isort-clean and its
  `[tool.ruff]` is scoped to `todo/`, so the shipped `make comply` is green
  out of the box — #735
- `[cli]` Constrain the cement dependency in generated `project` and
  `todo-tutorial` templates to a compatible 3.0.x range (`~=3.0.0` /
  `>=3.0,<3.1`) so freshly generated projects install even when generated
  by an unreleased dev cement — #735

Features:

- `[core.foundation]` Support config override of `App.Meta.template_dirs`
  via the `[<app>]` section — accepts a list (native-list config handlers)
  or a comma-separated string (the INI handler), parallel to the existing
  `extensions` handling.
  - [Issue #746](https://github.com/datafolklabs/cement/issues/746)
- `[ext.generate]` Add optional features support to generate templates —
  conditional variables, exclude/ignore patterns, and order-independent
  `requires` dependency resolution (with transitive cascade).
  - [Issue #743](https://github.com/datafolklabs/cement/issues/743)
- `[ext.generate]` Add `prompt_mode: select` for multi-valued feature
  prompts — a numbered picker dispatching the chosen value into one of N
  `options` branches, each with its own `ignore`/`exclude`/`variables`;
  defaults to `boolean` (byte-identical when absent).
  - [Issue #779](https://github.com/datafolklabs/cement/issues/779)
- `[ext.generate]` Add `type: choice` template variables — a numbered
  picker that emits the chosen option string at the top level; `options:`
  accepts scalars or `{value, prompt}` objects with per-option effects in
  `extend:` rules; misconfig is fail-fast `ValueError`.
- `[ext.generate]` `type: boolean` `prompt:` is now polymorphic — an object
  form `{text, accept, reject}` lets the template author own the prompt
  text and supply the token lists that map input to a real bool; unmatched
  input aborts with `Invalid Response`.
- `[ext.generate]` `extend.when` now composes scalar-equality, in-list
  membership, and string-regex match forms (all matching rules fire) with
  nested depth-first `extend.variables`; a new top-level `requires:` key
  gates variables using the same vocabulary, AND-ed and resolved
  order-independently, defaulting gated-out variables so templates never
  `KeyError`. Also addresses the PR #780 review feedback (features prompt
  after vars, custom prompt text, vars-style input).
  - [Issue #782](https://github.com/datafolklabs/cement/issues/782)
  - [PR #780](https://github.com/datafolklabs/cement/pull/780)
- `[ext.argparse]` Add a read-only `_command_meta` property on
  `ArgparseController` so an exposed command can read its own `CommandMeta`
  from inside its body; returns `None` outside a dispatched command and
  never raises. Additive — the `func()` dispatch signature is unchanged.
  - [Issue #670](https://github.com/datafolklabs/cement/issues/670)
- `[ext.argparse]` Add a companion read-only `_default_command_meta`
  property that resolves the controller's default sub-command meta (via
  `Meta.default_func`); returns `None` when there is no exposed default and
  never raises.
  - [Issue #670](https://github.com/datafolklabs/cement/issues/670)
- `[utils.misc]` Add an optional `CEMENT_FRAMEWORK_LOG_FILE` env var — when
  framework logging is enabled, debug output is also written to the given
  file. Purely additive: no duplicate handlers on repeat calls, and an
  invalid path is ignored rather than raising.
  - [Issue #593](https://github.com/datafolklabs/cement/issues/593)

Refactoring:

- `[ext.generate]` Remove the unreleased `features:` schema wholesale —
  everything it expressed is now a `type: boolean`/`type: choice` variable
  carrying `extend:`/`requires:`; the legacy compatibility bridge is
  deleted (#782)
- `[dev]` Migrate the `demo/generate-features/` webapp template to the
  unified `type:`/`extend:`/`requires:` schema and demonstrate the #782 fix
  (top-level `{% if docker %}` / `{% if web_framework == ... %}`)
- `[ext.smtp]` PEP 8 naming, idiomatic string methods, and cleaner type
  validation
- `[ext.smtp]` Refactor `_make_message` into focused private methods
- `[ext.smtp]` Simplify X-header normalization and preserve original casing
- `[dev]` Python 3.14 default development target
- `[dev]` Remove support for Python 3.8 (EOL)
- `[dev]` Remove support for Python 3.9 (EOL)
- `[cli]` Migrate the `cement generate project` template from
  setuptools+`setup.py` to pdm-backend with full PEP 621 metadata and PEP
  735 dev deps; generated `version.py` no longer imports cement at build
  time
- `[cli]` Generated project `README.md`/`Makefile` now document Python
  3.10+ and PDM, use `pip install .` for end users, and rename the
  `virtualenv` target to `setup` (`pdm install`)
- `[core]` Modernize type annotations to PEP 585 builtin generics (UP006:
  `List`→`list`, `Dict`→`dict`, `Tuple`→`tuple`, `Type`→`type`); prune
  orphaned `typing` re-exports
- `[core]` Modernize union types to PEP 604 syntax (UP007: `Union[X, Y]`→
  `X | Y`); prune orphaned `typing.Union` imports
- `[core]` Modernize Optional types to PEP 604 syntax (UP045:
  `Optional[X]`→`X | None`); prune orphaned `typing.Optional` imports
- `[core]` Move `Callable`/`Generator` imports from `typing` to
  `collections.abc` (UP035)
- `[core]` Convert printf-style format strings to modern format (UP031);
  protected `.format(**template_dict)` template callsites preserved
- `[core]` Drop redundant `(object)` base classes (UP004)
- `[core]` Simplify `super()` calls to the zero-arg form (UP008)
- `[core]` Drop the redundant `'r'` mode argument from `open()` calls
  (UP015)
- `[core]` Replace the `IOError` alias with `OSError` (UP024)
- `[dev]` Drop the legacy `u"..."` unicode literal prefix in test code
  (UP025)
- `[dev]` Replace the deprecated `mock` import with `unittest.mock` (UP026)
- `[core]` Replace `for x in iterable: yield x` with `yield from` (UP028)
- `[core]` Convert `.format()` calls to f-strings (UP032); protected
  template callsites preserved
- `[core]` Tighten `Any` types in `cement/core/` where narrower types are
  provably correct; surviving `Any` carries inline justification
- `[dev]` Refresh CONVENTIONS.md type-annotation guidance to PEP 585 / PEP
  604 syntax
- `[core]` Wrap long log/error messages (E501) and reorder imports (I001)
  surfaced by the UP sweeps
- `[core]` Drop `from __future__ import annotations` from all 29 `cement/`
  files (native on 3.10+); convert affected forward references to PEP 484
  string annotations
- `[utils.fs]` Migrate `cement/utils/fs.py` internals to pathlib while
  preserving `str` return boundaries (public surface unchanged)
- `[core.config]` Migrate the `config.py` `parse_file` os.path callsite to
  pathlib; retain `import os` as a no-op to keep the public surface intact
- `[core.foundation]` Migrate the `foundation.py` `_find_config_files`
  os.path callsite to pathlib; retain the public `join = os.path.join`
  alias and leave protected template callsites untouched
- `[core.template]` Migrate `template.py` os.path internals to pathlib;
  retain the `os.walk(src)` callsite (no direct pathlib equivalent for the
  triple-tuple loop)
- `[dev]` Audit `pragma: nocover` sites in `cement/core/` with
  locked-vocabulary category labels
- `[dev]` Audit `pragma: nocover` sites in `cement/ext/` (first half) with
  locked-vocabulary category labels
- `[dev]` Audit `pragma: nocover` sites in `cement/ext/` (second half) with
  locked-vocabulary category labels
- `[dev]` Audit `pragma: nocover` sites in `cement/cli/` and
  `cement/utils/` with locked-vocabulary category labels
- `[core.deprecations]` Pin the `3.0.10-1` and `3.0.16-1` deprecation
  removal versions to v3.2.0
- `[ext.logging]` Tighten the FATAL deprecation removal version in
  docstrings
- `[ext.smtp]` Document the `send()` bool-return removal in v3.2.0
- `[cli]` Migrate the `cement generate todo-tutorial` template to
  pdm-backend with full PEP 621 metadata and a PEP 735 dev group (mirrors
  `generate project`; #735)
- `[cli]` Ship `[tool.ruff]`/`[tool.mypy]`/`[tool.pytest]` gate config in
  the generated project and todo-tutorial so `make comply`/`make test` are
  green out of the box (#735)
- `[cli]` Type-annotate all generated templates
  (project/script/extension/plugin/todo) and modernize idioms to f-strings
  (#735)

Misc:

- `[ci]` Add GitHub Actions PR CI (`build_and_test.yml`) running the test
  suite on pull requests with minimal permissions — #757
- `[ci]` Add an automated release workflow (`release.yml`) — tag-triggered:
  preflight guard → gate suite → isolated build → TestPyPI publish +
  5-Python install smoke → environment-gated OIDC PyPI publish →
  post-approval fan-out (Docker Hub multi-arch, `stable/3.0.x` sync, RTD
  re-point, GitHub Release, dev-bump PR, checklist issue);
  `workflow_dispatch` runs it as a dry run
- `[ci]` Refactor the PR gate chain into a reusable `gates.yml`
  (`workflow_call`) shared by PR CI and release; wire the matrix Python
  versions; add (disabled) Windows core-test and macOS/Windows native smoke
  gates
- `[dev]` Add release dev-tooling scripts: `testpypi-smoke.py`,
  `cli-smoke-native.py`, `bump_dev_version.py`
- `[dev]` Add devbox/direnv development-environment configuration for
  reproducible local setup
- `[ext.smtp]` Isolate test defaults to prevent cross-test state pollution
- `[dev]` Bump ruff to 0.15.x; codify rule sets explicitly and resolve all
  surfacing lint findings
- `[dev]` Bump mypy to ~=1.20.2 and codify the type-check surface
- `[dev]` Bump pytest 9.0.3, pytest-cov 7.1.0, coverage 7.13.5
- `[dev]` Add a `make cli-smoke-test` target — generated-project install
  smoke across Python 3.10–3.14 in Docker
- `[dev]` Bump the dev/extras lockfile to current non-breaking versions
  (redis 7.4, watchdog 6.0, tabulate 0.10, sphinx 8.1, requests 2.33,
  others)
- `[dev]` Wire the 100% coverage gate via `[tool.coverage.report]`
  `fail_under` + `--cov-fail-under`
- `[ci]` Pin GitHub Actions to exact tags
- `[ci]` Add PyPy 3.11 to the CI test matrix (alongside PyPy 3.10)
- `[ci]` Enable Dependabot for the github-actions ecosystem (weekly)
- `[ci]` Add a `workflow_dispatch` trigger to `pdm.yml`
- `[dev]` Add a `make audit-public-api` target + AST-walk public-surface
  enumerator + baseline snapshot
- `[dev]` Enable ruff `UP` (pyupgrade) and `FA` (flake8-future-annotations)
  families
- `[dev]` Capture the Phase 03 Any-in-core / pragma / pathlib baselines in
  `03-VERIFICATION.md`
- `[dev]` Finalize Phase 03 verification (all D-24 conjuncts green;
  REFACTOR-01..04 + COV-01..03 satisfied)
- `[dev]` Complete Phase 03 (Internal Refactor & Coverage Hardening);
  ROADMAP updated
- `[docs]` Drop the unsupported `logo` theme option from the Sphinx config
- `[docs]` Remove the orphan `docs/source/api/index.rst`
- `[docs]` Rename `display_version` to `version_selector` (sphinx_rtd_theme
  3.x)
- `[docs]` Fix inline-literal RST in the `shell.cmd()` docstring
- `[docs]` Add a top-level DEPRECATIONS.md mirroring the GitBook narrative
- `[dev]` Wire `-W` into `make docs` (zero-warnings gate)
- `[docs]` Drop the Travis CI link/badge (CI moved to GitHub Actions)
- `[docs]` Align CONTRIBUTING with Conventional Commits + atomic-per-concern
- `[docs]` Expose `cement.core.deprecations` in the Sphinx API reference
  (was missing)
- `[docs]` Fix a `stderror` → `stderr` typo in the `cement.utils.shell`
  `cmd()`/`exec_cmd()` Returns docstrings
- `[docs]` Remove an orphaned `[Commit Guidelines]` reference-link
  definition from `.github/CONTRIBUTING.md`
- `[dev]` Extend the CI `cli-smoke-test` to gate the generated project's own
  `make comply`/`make test` and to build/install the generated todo-tutorial
  (#735)
- `[dev]` Add a generated-todo ruff-clean regression guard
  (`test_generate_todo_ruff_clean`) (#735)

Deprecations:

- `[ext.smtp]` `SMTPMailHandler.send()` returning `bool` is deprecated
  (warn-only); it will return a `senderrs` dict, with removal targeted for
  v3.2.0


## 3.0.14 - May 5, 2025

Bugs:

- `[ext_jinja2]` Refactor hard-coded reference to `jinja2` template handler.
  - [Issue #749](https://github.com/datafolklabs/cement/issues/749)
- `[ext_smtp]` Misc fixes and updates to better support content types.
  - [PR #742](https://github.com/datafolklabs/cement/pull/742)

Features:

- None

Refactoring:

- None

Misc:

- None

Deprecations:

- None


## 3.0.12 - Nov 10, 2024

Bugs:

- None


Features:

- None


Refactoring:

- `[dev]` Refactor String Substitutions (`%s`) with F-Strings
    - [Issue #733](https://github.com/datafolklabs/cement/issues/733)
- `[dev]` Allow line lengths up to 100 characters (previously 78)
- `[dev]` Modernize Packaging (pyproject.toml, PDM)
    - [Issue #680](https://github.com/datafolklabs/cement/issues/680)
    - [PR #681](https://github.com/datafolklabs/cement/pull/681)
- `[dev]` Implement Ruff for Code Compliance (replaces Flake8)
    - [Issue #671](https://github.com/datafolklabs/cement/issues/671)
    - [PR #681](https://github.com/datafolklabs/cement/pull/681)
- `[dev]` Remove Python 3.5, 3.6, 3.7 Docker Dev Targets
- `[dev]` Added Python 3.13 Dev Target
- `[dev]` Testing now requires typing compliance (`make test` -> `make comply-mypy`)
- `[dev]` Type Annotations (related: [PR #628](https://github.com/datafolklabs/cement/pull/628))
    - `[core.arg]` [Issue #692](https://github.com/datafolklabs/cement/issues/692)
    - `[core.cache]` [Issue #693](https://github.com/datafolklabs/cement/issues/693)
    - `[core.config]` [Issue #694](https://github.com/datafolklabs/cement/issues/694)
    - `[core.controller]` [Issue #695](https://github.com/datafolklabs/cement/issues/695)
    - `[core.deprecations]` [Issue #696](https://github.com/datafolklabs/cement/issues/696)
    - `[core.exc]` [Issue #697](https://github.com/datafolklabs/cement/issues/697)
    - `[core.extension]` [Issue #698](https://github.com/datafolklabs/cement/issues/698)
    - `[core.foundation]` [Issue #699](https://github.com/datafolklabs/cement/issues/699)
    - `[core.handler]` [Issue #700](https://github.com/datafolklabs/cement/issues/700)
    - `[core.hook]` [Issue #700](https://github.com/datafolklabs/cement/issues/701)
    - `[core.interface]` [Issue #702](https://github.com/datafolklabs/cement/issues/702)
    - `[core.log]` [Issue #703](https://github.com/datafolklabs/cement/issues/703)
    - `[core.mail]` [Issue #704](https://github.com/datafolklabs/cement/issues/704)
    - `[core.meta]` [Issue #705](https://github.com/datafolklabs/cement/issues/705)
    - `[core.output]` [Issue #706](https://github.com/datafolklabs/cement/issues/706)
    - `[core.plugin]` [Issue #707](https://github.com/datafolklabs/cement/issues/707)
    - `[core.template]` [Issue #708](https://github.com/datafolklabs/cement/issues/708)
    - `[ext.alarm]` [Issue #709](https://github.com/datafolklabs/cement/issues/709)
    - `[ext.argparse]` [Issue #710](https://github.com/datafolklabs/cement/issues/710)
    - `[ext.colorlog]` [Issue #711](https://github.com/datafolklabs/cement/issues/711)
    - `[ext.configparser]` [Issue #712](https://github.com/datafolklabs/cement/issues/712)
    - `[ext.daemon]` [Issue #713](https://github.com/datafolklabs/cement/issues/713)
    - `[ext.dummy]` [Issue #714](https://github.com/datafolklabs/cement/issues/714)
    - `[ext.generate]` [Issue #715](https://github.com/datafolklabs/cement/issues/715)
    - `[ext.jinja2]` [Issue #716](https://github.com/datafolklabs/cement/issues/716)
    - `[ext.json]` [Issue #717](https://github.com/datafolklabs/cement/issues/717)
    - `[ext.logging]` [Issue #718](https://github.com/datafolklabs/cement/issues/718)
    - `[ext.memcached]` [Issue #719](https://github.com/datafolklabs/cement/issues/719)
    - `[ext.mustache]` [Issue #720](https://github.com/datafolklabs/cement/issues/720)
    - `[ext.plugin]` [Issue #721](https://github.com/datafolklabs/cement/issues/721)
    - `[ext.print]` [Issue #722](https://github.com/datafolklabs/cement/issues/722)
    - `[ext.redis]` [Issue #723](https://github.com/datafolklabs/cement/issues/723)
    - `[ext.scrub]` [Issue #724](https://github.com/datafolklabs/cement/issues/724)
    - `[ext.smtp]` [Issue #725](https://github.com/datafolklabs/cement/issues/725)
    - `[ext.tabulate]` [Issue #726](https://github.com/datafolklabs/cement/issues/726)
    - `[ext.watchdog]` [Issue #727](https://github.com/datafolklabs/cement/issues/727)
    - `[ext.yaml]` [Issue #728](https://github.com/datafolklabs/cement/issues/728)
    - `[utils.fs]` [Issue #688](https://github.com/datafolklabs/cement/issues/688)
    - `[utils.misc]` [Issue #689](https://github.com/datafolklabs/cement/issues/689)
    - `[utils.shell]` [Issue #690](https://github.com/datafolklabs/cement/issues/690)
    - `[utils.version]` [Issue #691](https://github.com/datafolklabs/cement/issues/691)



Misc:

- [cli] Move CLI dependencies to `cement[cli]` extras package, and remove included/nexted `contrib` sources.  See note on 'Potential Upgrade Incompatibility'
  - [Issue #679](https://github.com/datafolklabs/cement/issues/679)


Deprecations:

- None


Special Recognitions:

Many thanks to [@sigma67](https://github.com/sigma67) for their contributions in modernizing the packaging system. Cement was started in 2009, and has some lingering technical debt that is now being addressed. Their contribution was a major help in moving off of setuptools and on to PDM and `pyproject.toml`, along with initial implementations of Ruff for a new generation of code compliance. I sincerely appreciate your help!

Many thanks to [@rednar](https://github.com/rednar) for their contributions toward adding type annotations in [PR #628](https://github.com/datafolklabs/cement/pull/628). This PR was too large to merge directly, but it is serving as a guide to finally begin work toward adding type annotations to Cement. This was a massive effort, and is very helpful to have this work available to guide the effort even if it will not be merged directly.


Potential Upgrade Incompatibility:

This update removes included `contrib` libraries that are dependencies for the `cement` command line tool to function (PyYAML, and Jinja2). The dependencies are now included via the `cement[cli]` extras package.

This is not an upgrade incompatibility in the core Cement code, and it would not affect any applications that are built on Cement. That said, it does have the potential to break any automation or other uses of the `cement` command line tool.

Resolution:

```
pip install cement[cli]
```


## 3.0.10 - Feb 28, 2024

Bugs:

- `[ext.logging]` Support `logging.propagate` to avoid duplicate log entries
    - [Issue #310](https://github.com/datafolklabs/cement/issues/310)
- `[core.foundation]` Quiet mode file is never closed
    - [Issue #653](https://github.com/datafolklabs/cement/issues/653)
- `[ext.smtp]` Ability to Enable TLS without SSL
    - [Issue #667](https://github.com/datafolklabs/cement/issues/667)
- `[ext.smtp]` Empty (wrong) addresses sent when CC/BCC is `None`
    - [Issue #668](https://github.com/datafolklabs/cement/issues/668)


Features:

- `[utils.fs]` Add Timestamp Support to fs.backup
    - [Issue #611](https://github.com/datafolklabs/cement/issues/611)
- `[ext.smtp]` Support for sending file attachements.
    - [PR #669](https://github.com/datafolklabs/cement/pull/669)
- `[ext.smtp]` Support for sending both Plain Text and HTML
    - [PR #669](https://github.com/datafolklabs/cement/pull/669)


Refactoring:

- `[core.plugin]` Deprecate the use of `imp` in favor of `importlib`
    - [Issue #386](https://github.com/datafolklabs/cement/issues/386)
- `[ext.smtp]` Actually test SMTP against a real server (replace mocks)


Misc:

- `[dev]` Add Smoke tests for Python 3.11, 3.12
- `[dev]` Make Python 3.12 the default development target
- `[dev]` Drop support for Python 3.7
    - [Issue #658](https://github.com/datafolklabs/cement/issues/658)
- `[docker]` Base official Docker image on Python 3.12
- `[utils.version]` Resolve deprecated `datetime.utcfromtimestamp()`
    - [Issue #661](https://github.com/datafolklabs/cement/issues/661)
- `[dev]` Add `comply-typing` to make helpers, start working toward typing.
    - [Issue #599](https://github.com/datafolklabs/cement/issues/661)
    - [PR #628](https://github.com/datafolklabs/cement/pull/628)
- `[dev]` Add `mailpit` service to docker-compose development config.

Deprecations:

- `[ext.logging]` Deprecate FATAL facility in favor of CRITICAL.
    - [Issue #533](https://github.com/datafolklabs/cement/issues/533)


## 3.0.8 - Aug 18, 2022

Bugs:

- `[cli]` Cement CLI broken on Python 3.10
    - [Issue #619](https://github.com/datafolklabs/cement/issues/619)
- `[cli]` Generated script returns version of Cement
    - [Issue #632](https://github.com/datafolklabs/cement/issues/632)
- `[cli]` Generated script should allow dash/underscore
    - [Issue #614](https://github.com/datafolklabs/cement/issues/614)
- `[core.foundation]` App.render() not suppressed in quiet mode
    - [Issue #636](https://github.com/datafolklabs/cement/issues/636)
- `[core.foundation]` Console log not suppressed by output handler override (JSON/YAML)
    - [Issue #637](https://github.com/datafolklabs/cement/issues/637)


Features:

- `[utils.shell]` Support `suppress` meta option on `Prompt` to suppress user input.
    - [Issue #621](https://github.com/datafolklabs/cement/issues/621)
- `[ext]` Use `extras_require` for optional extensions
    - [Issue #604](https://github.com/datafolklabs/cement/issues/604)

Refactoring:

- `[utils.misc]` Use SHA256 instead of MD5 in `rando()` to support Redhap/FIPS compliance
    - [Issue #626](https://github.com/datafolklabs/cement/issues/626)
- `[core.foundation]` Make quiet/debug options configurable
    - [Issue #613](https://github.com/datafolklabs/cement/issues/613)

Misc:

- `[dev]` Cement CLI smoke tests
    - [Issue #620](https://github.com/datafolklabs/cement/issues/620)
- `[dev]` Add Python 3.10 to Travis CI tests
    - [Issue #618](https://github.com/datafolklabs/cement/issues/618)
- `[core.deprecations]` Implement Cement deprecation warnings
    - [Issue #631](https://github.com/datafolklabs/cement/issues/631)


Deprecations:

- `[core.foundation]` Deprecate CEMENT_FRAMEWORK_LOGGING in favor of CEMENT_LOG.
    - [Issue #638](https://github.com/datafolklabs/cement/issues/638)


## 3.0.6 - Dec 18, 2021

Bugs:

- `[ext.argparse]` Parser (`self._parser`) not accessible inside `_pre_argument_parsing` when `stacked_type = 'embedded'`
    - [Issue #569](https://github.com/datafolklabs/cement/issues/569)
- `[ext.configparser]` Overriding config options with environment variables doesn't work correctly with surrounding underscore characters
    - [Issue #590](https://github.com/datafolklabs/cement/issues/590)
- `[utils.fs]` Fix bug where trailing slash was not removed in `fs.backup()` of a directory.
    - [Issue #610](https://github.com/datafolklabs/cement/issues/610)
- `[cement.cli]` Generated README contains incorrect installation instructions.
    - [Issue #588](https://github.com/datafolklabs/cement/issues/588)

Features:

- None


Refactoring:

- `[ext.colorlog]` Support subclassing of ext_colorlog.
    - [Issue #571](https://github.com/datafolklabs/cement/issues/571)


Misc:

- `[dev]` Update to Python 3.10 for default development / Docker version.
- `[dev]` Remove Python 3.5/3.6 from Travis CI tests.


## 3.0.4 - May 17, 2019

Bugs:

- `[ext.yaml]` YamlConfigHandler uses unsafe load method
   - [Issue #553](https://github.com/datafolklabs/cement/issues/553)
- `[ext.configparser]` Configparser 'getboolean' exception
   - [Issue #558](https://github.com/datafolklabs/cement/issues/558)


Features:

- `[utils.misc]` Support `y` as a truth boolean in `utils.misc.is_true`
    - [Issue #542](https://github.com/datafolklabs/cement/issues/542)


## 3.0.2 - November 6, 2018

Bugs:

- `[cli]` Generate Variable Mishap in Project Template
    - [Issue #532](https://github.com/datafolklabs/cement/issues/532)
- `[ext.generator]` Error class is malformed
    - [Issue #535](https://github.com/datafolklabs/cement/issues/535)
- `[core.template]` MemoryError during 'cement generate project'
    - [Issue #531](https://github.com/datafolklabs/cement/issues/531)
- `[core.foundation]` Contents of plugin_dirs is printed to console
    - [Issue #538](https://github.com/datafolklabs/cement/issues/538)


Features:

- `[ext.argparse]` Command name override
    - [Issue #529](https://github.com/datafolklabs/cement/issues/529)


## 3.0.0 - August 21, 2018

Bugs:

- `[ext.redis]` Unable To Set Redis Host
    - [Issue #440](https://github.com/datafolklabs/cement/issues/440)
- `[ext.argparse]` Empty Sub-Commands List
    - [Issue #444](https://github.com/datafolklabs/cement/issues/444)
- `[core.foundation]` Handler Override Options Do Not Honor Meta Defaults
    - [Issue #513](https://github.com/datafolklabs/cement/issues/513)

Features:

- `[core]` Add Docker / Docker Compose Support
    - [Issue #439](https://github.com/datafolklabs/cement/issues/439)
- `[core]` Add ability to override the output handler used when `app.render()` is called.
    - [Issue #471](https://github.com/datafolklabs/cement/issues/471)
- `[ext.print]` Add the Print Extension to be used as a drop in replacement for the standard ``print()``, but allowing the developer to honor framework features like `pre_render` and `post_render` hooks.
- `[ext.scrub]` Add Scrub Extension to easily obfuscate sensitive data from rendered output.
    - [Issue #469](https://github.com/datafolklabs/cement/issues/469)
- `[core]` Add ability to override config settings via environment variables.
    - [Issue #437](https://github.com/datafolklabs/cement/issues/437)
- `[ext.argparse]` Add ability to get list of exposed commands
    - [Issue #455](https://github.com/datafolklabs/cement/issues/455)
- `[core]` Add Template Interface
    - [Issue #464](https://github.com/datafolklabs/cement/issues/464)
- `[ext.mustache]` Add MustacheTemplateHandler
- `[ext.handlebars]` Add HandlebarsTemplateHandler
- `[ext.jinja2]` Add Jinja2TemplateHandler
- `[ext.generate]` Add Generate Extension
    - [Issue #487](https://github.com/datafolklabs/cement/issues/487)
- `[ext.logging]` Add `-l LEVEL` command line option to override log level
    - [Issue #497](https://github.com/datafolklabs/cement/issues/497)
- `[cli]` Add Cement CLI (includes ability to generate apps, plugins,
    extensions, and scripts using the Generate Extension)
    - [Issue #490](https://github.com/datafolklabs/cement/issues/490)
- `[core]` Added clear separation between Interfaces and Handlers
    - [Issue #506](https://github.com/datafolklabs/cement/issues/506)
- `[utils.fs]` - Added several helpers include `fs.Tmp` for creation and cleanup of temporary directory and file.

Refactoring:

- *Too many to reference*


Incompatible:

- `[core]` Replace Interfaces with ABC Base Classes
    - [Issue #192](https://github.com/datafolklabs/cement/issues/192)
- `[core.foundation]` Rename `CementApp` to `App`.
- `[core.foundation]` Drop deprecated `App.Meta.override_arguments`
- `[core.foundation]` Remove `App.Meta.plugin_config_dir` and `App.Meta.plugin_config_dirs` in favor of `App.Meta.config_dirs`
    - [Issue #521](https://github.com/datafolklabs/cement/issues/521)
- `[core.founcation]` Rename `App.Meta.plugin_bootstrap` as `App.Meta.plugin_module`
    - [Issue #523](https://github.com/datafolklabs/cement/issues/523)
- `[core.handler]` Rename `CementBaseHandler` to `Handler`
- `[core.handler]` Drop deprecated backend globals
- `[core.hook]` Drop deprecated backend globals
- `[core.controller]` Drop `CementBaseController`
- `[ext.logging]` Drop deprecated `warn` facility (use `warning`)
- `[ext.argcomplete]` Drop ArgComplete Extension
- `[ext.reload_config]` Drop Reload Config Extension
- `[ext.configobj]` Drop ConfigObj Extension
- `[ext.json]` Disable `overridable` option by default
- `[ext.yaml]` Disable `overridable` option by default
- `[ext.json_configobj]` Drop JSON ConfigObj Extension
- `[ext.yaml_configobj]` Drop YAML ConfigObj Extension
- `[ext.handlebars]` Drop Handlebars Extension
- `[ext.genshi]` Drop Genshi Extension
- `[ext.argparse]` `ArgparseController.Meta.default_func` is now `_default`, and will print help info and exit.  Can now set this to `None` as well to pass/exit.
    - [Issue #426](https://github.com/datafolklabs/cement/issues/426)
- `[ext.plugin]` All plugin configuration sections must start with `plugin.`.
    For example, `[plugin.myplugin]`.
- `[core.foundation]` Renamed `App.Meta.config_extension` to `App.Meta.config_file_suffix`
    - [Issue #445](https://github.com/datafolklabs/cement/issues/445)
- `[core.foundation]` Drop `App.Meta.arguments_override_config`
    - [Issue #493](https://github.com/datafolklabs/cement/issues/493)

Deprecation:

- *Everything with deprecation notices in Cement < 3*
