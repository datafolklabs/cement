# ChangeLog

## 3.0.15 - DEVELOPMENT (will be released as stable/3.0.16)

Bugs:

- `[core.foundation]` Fix `extensions` config-override to honor
  `Meta.config_section` when it differs from `Meta.label` (was silently
  using `label`, mirroring the `template_dirs` fix from PR #760) —
  resolves #777
- `[ext.smtp]` Fix `timeout` passed as `local_hostname` in SMTP constructors
- `[ext.smtp]` Fix stale variable reference in `_get_params` for per-message headers
- `[ext.smtp]` Fix SMTP connection leak when send fails with an exception
- `[ext.smtp]` Fix unconditional error log on every send (now only logs on errors)
- `[ext.smtp]` Fix header encoding incorrectly affected by `body_encoding` setting
- `[cli]` Generated `cement generate project` output now builds under pip's
  default PEP 517 isolation on Python 3.10+ — the legacy `setup.py` self-imported
  the package being built, which fails inside isolated build envs
- `[core.handler]` Resolve mypy union-attr false-positive in handler resolution
- `[ext.redis]` Resolve mypy union-attr/arg-type/misc errors surfaced by
  redis 7 typing changes (sync client return-type unions)
- `[ext.watchdog]` Drop now-unused `# type: ignore` comments on Observer
  schedule/start/stop calls — watchdog 6 ships precise type stubs
- `[utils.fs]` Restore `os.path` semantics in `abspath()` —
  preserves symlink paths and silently falls through on unknown
  `~user` prefixes (regression introduced by the Phase 03 Wave 6
  pathlib migration; restores 3.0.x BC contract on the public
  `cement.utils.fs:abspath` surface)
- `[dev]` Use explicit `encoding='utf-8'` in
  `scripts/audit-public-api.py` so the
  `make audit-public-api` regression gate is portable across
  non-UTF-8 locales (Windows cp1252, locale-stripped Docker, etc.)
- `[dev]` Fix `scripts/cli-smoke-test.sh` capturing the container's
  `mktemp -d` path via `docker exec -t` — the pseudo-TTY made Docker
  emit CRLF, and command substitution kept the trailing `\r`, so
  every derived `$tmp/...` path carried an embedded carriage return
  (`/tmp/tmp.XXXX\r/myapp/...`) and broke pdm/venv on the first
  Python version. Drop `-t` on that one capture (the other `-t`
  execs only feed `grep`, where a trailing `\r` is harmless)
- `[dev]` Fix `scripts/cli-smoke-test.sh` `pdm install` of the
  generated project failing to resolve the dev cement pin
  (`cement==<unreleased>`) — `pdm install` resolves in a fresh
  isolated venv against PyPI, where the in-development version is not
  yet published, so it could not satisfy the exact pin. Inject a
  find_links `[[tool.pdm.source]]` pointing at the mounted
  `/src/dist` so the locally-built cement resolves. Harness-only
  shim (real users install a published cement from PyPI); ruff/mypy/
  pytest ignore the source table so the project gates are unaffected
- `[core.interface]` Widen `InterfaceManager.get` `fallback`
  parameter to `Any` to match the documented public contract and
  the existing test that passes a string fallback (the parameter
  was mechanically narrowed to `type[Interface] | None` by the
  Phase 03 UP045 sweep; the runtime always accepted arbitrary
  fallback values per the `cache.get` sibling pattern)
- `[ext.smtp]` Type the message body and `**params` correctly across
  `SMTPMailHandler.send`, `_build_body_parts`, `_make_message`, and
  the related private helpers (`_header`, `_build_charsets`,
  `_build_mime_structure`, `_set_headers`, `_attach_body`,
  `_attach_files`). Introduce a private `_BodyType =
  str | tuple[str, str] | dict[str, str]` alias so the dict body
  shape (`{'text': ..., 'html': ...}`), already supported at runtime
  by `_build_body_parts`, is now reflected in the static type.
  Convert seven `**params: dict[str, Any]` annotations to
  `**params: Any` (the prior form declared each kwarg VALUE as a
  dict, the wrong meta-type for var-kwargs); this lets callers pass
  arbitrary keyword values per the documented contract. As a
  follow-on cleanup, drop nine now-unused `# type: ignore`
  suppressions at `params[...]` callsites that were papering over
  the wrong meta-typing, and add a `part: MIMEBase` annotation in
  `_attach_files` so the `MIMEImage`/`MIMEBase` branches type-check
  cleanly. Public-API surface byte-identical (`_BodyType` is private
  so `make audit-public-api` stays at exit 0)
- `[utils.shell]` Correct `cmd` and `exec_cmd` return-type
  annotations from `tuple[str, str, int]` to
  `tuple[bytes, bytes, int]` (and `cmd`'s union return to
  `tuple[bytes, bytes, int] | int`) — `subprocess.Popen` returns
  `bytes` from `communicate()` by default, and the existing tests
  already assert `out == b'KAPLA!\n'` (literal bytes). The prior
  `str` annotation was a type/runtime mismatch that mypy could
  not catch (the bytes return was bidirectionally compatible
  with the declared `str` via `Any` upcasting in dependent
  context). Docstrings updated to call out that `stdout`/
  `stderr` are bytes and to point at `text=True` / `encoding=`
  through `**kwargs` for callers wanting `str` output. Runtime
  behavior unchanged; this is documentation/type honesty only,
  not a behavior shift
- `[utils.shell]` Correct `Prompt.Meta.options` annotation from
  `dict | None` to `list[str] | None` — the runtime treats
  `options` as a list of strings (iteration in
  `Prompt._prompt`, `str.join` in the non-numbered branch,
  integer indexing via `options[int(...) - 1]` in the numbered
  branch, `in`-membership checks in the case-insensitive and
  case-sensitive branches), all of which the prior `dict`
  annotation actively misled. mypy didn't flag this previously
  because `dict` without parameters resolves to
  `dict[Any, Any]`, and `Any` silenced the type errors at every
  callsite. All existing tests pass `options=['y', 'n']`-style
  list literals, so the new concrete type matches actual usage
- `[ext.yaml]` Replace implicit-Optional `template: str = None` on
  `YamlOutputHandler.render()` with the explicit
  `template: str | None = None` (PEP 484 / ruff RUF013), mirroring
  the `[ext.mustache]` fix above. The handler ignores the
  `template` parameter at runtime (per docstring), so no
  follow-on `# type: ignore[arg-type]` was needed — the prior
  signature-line `# type: ignore` is removed entirely. Public
  signature byte-identical from the audit-public-api perspective.
  Sister handlers (`ext.jinja2`, `ext.json`) carry the same
  pattern and remain on the implicit-Optional form pending a
  follow-up
- `[ext.mustache]` Replace implicit-Optional `template: str = None`
  on `MustacheOutputHandler.render()` with the explicit
  `template: str | None = None` (PEP 484 / ruff RUF013). The
  `# type: ignore` previously placed at the signature line is
  removed (the implicit-Optional violation it was suppressing no
  longer fires) and a scoped `# type: ignore[arg-type]` is added
  at the `self.templater.load(template)` callsite to document
  that the `None` default is well-defined at runtime
  (`TemplateHandler.load` guards `if not template_path:` and
  raises `FrameworkError`). Public signature byte-identical from
  the audit-public-api perspective. Sister handlers
  (`ext.jinja2`, `ext.yaml`, `ext.json`) carry the same pattern
  and remain on the implicit-Optional form pending a follow-up
- `[utils.misc]` Make `MinimalLogger.__init__` idempotent — guard
  the `self.backend.addHandler(console)` call on
  `not self.backend.handlers` so a second `minimal_logger(ns)`
  call for the same namespace does not stack a duplicate
  `StreamHandler` on the shared backend logger
  (`logging.getLogger(ns)` returns the same instance per name, so
  the previous unconditional add produced as many handlers as
  callers — every log emit would print N times)
- `[ext.daemon]` Remove the duplicate
  `LOG = minimal_logger(__name__)` assignment at module scope
  (a back-to-back redundant rebind that, combined with the prior
  `MinimalLogger.__init__` non-idempotency, attached a second
  `StreamHandler` to the `cement.ext.ext_daemon` backend logger
  on import — covered by the `[utils.misc]` hardening above but
  the redundant line is dropped for clarity)
- `[core.template]` Replace fragile bare `assert` in
  `TemplateHandler.copy()` source-path check with an explicit
  `NotADirectoryError` raise. The previous code had two failure
  modes: (1) bare `assert` is stripped under `python -O`/`-OO`,
  so apps running cement under optimization lost the runtime check
  entirely and `os.walk` would silently iterate over a
  non-existent path; and (2) `Path.exists()` returned True for
  files too, so passing a regular file as `src` made the assert
  pass and `os.walk` yield nothing — silent no-op with no
  diagnostic. The new check uses `is_dir()` (covers both missing
  paths and non-directories in one branch) and raises
  unconditionally regardless of optimization level.
  **Behavioral compatibility note:** the exception type changes
  from `AssertionError` to `NotADirectoryError`. Downstream code
  catching `AssertionError` to detect a missing/invalid `src`
  must switch to catching `NotADirectoryError` (or a parent like
  `OSError`). Gating runtime contracts on `AssertionError` was
  already fragile under `-O`, so this is a robustness fix
  rather than a contract regression on a load-bearing surface.
- `[core.interface]` String-quote list[str] return annotation for
  autodoc compatibility
- `[core.deprecations]` Drop trailing period from the `3.0.10-1`
  deprecation message — `deprecate()` appends `". See: ..."`, so a
  pre-existing trailing period rendered as `..` in the runtime
  warning. The other three entries already follow the implicit
  no-trailing-period invariant
- `[dev]` `make docs` zero-warnings gate now uses `&&` (was `;`),
  so the recipe correctly fails on Sphinx warnings instead of
  silently succeeding via the trailing `cd ..` exit code
- `[ext.generate]` Fix `variables` default from `{}` to `[]` — the
  generate flow iterates `variables` as a list of dicts, so the dict
  default would have produced an empty key-iteration on templates
  that omit the key
- `[ext.generate]` Narrow the dynamic-template-module `except` from
  bare `AttributeError` to `(AttributeError, ModuleNotFoundError)`
  with a `name`-match guard, so transitive `ModuleNotFoundError`s
  raised inside the user's template module propagate normally
  instead of being silently swallowed as "module not found"
- `[ext.generate]` `type: boolean` template variables now emit a real
  Python bool at the top level of the render context (`data[name]`),
  so `{% if feature_x %}` works in jinja2/mustache; the boolean prompt
  uses a vars-style `[(Y)es/(N)o] [default]:` format and all variables
  prompt in a single declaration-order pass — resolves #782 (the
  former `features:` namespace and pre-pass are removed)
- `[cli]` Generated `cement generate todo-tutorial` output now builds
  under pip's default PEP 517 isolation on Python 3.10+ — the legacy
  `setup.py` self-imported the package being built, which fails inside
  isolated build envs (mirrors the `generate project` fix; #735)
- `[cli]` Fix `NameError` in generated `todo/main.py` — the `TodoError`
  handler referenced an undefined name; now `except TodoError as e:`
  (#735)
- `[cli]` Fix false-green assertion in the generated project test
  template — `assert output.find(...)` (str.find() returns -1, which is
  truthy, so it never fails) is now membership `assert '...' in output`,
  so the test genuinely fails on wrong or empty rendered output (#735)
- `[cli]` Generated todo-tutorial imports are now isort-clean and its
  `[tool.ruff]` is scoped to the `todo/` package, so the shipped
  `make comply` (ruff) is green out of the box (#735)
- `[cli]` Constrain the cement dependency in generated `project` and
  `todo-tutorial` templates to the backward-compatible 3.0.x stable line.
  `project` previously used an exact `cement==<generating version>` pin,
  which made a freshly generated project uninstallable whenever the
  generating cement was an unreleased dev version (`pdm install` could not
  resolve it from PyPI); it now renders a compatible-release range
  (`cement[...]~={{ cement.major_version }}.{{ cement.minor_version }}.0`,
  e.g. `~=3.0.0` → `>=3.0.0,<3.1`). `todo-tutorial` previously used an
  uncapped `>=3.0`; it is now capped to a literal `>=3.0,<3.1` (that
  template is copied verbatim, so it cannot use rendered version vars).
  Both install any backward-compatible patch on the same stable minor
  line (#735)

Features:

- `[core.foundation]` Support config override of `App.Meta.template_dirs`
  via the `[<app>]` section. Accepts a list (under config handlers with
  native list support, e.g. `ext_yaml` or `ext_json`) or a comma-separated
  string (required for the default `ext_configparser` / INI handler).
  String form is split + whitespace-trimmed, parallel to the existing
  `extensions` config handling.
  - [Issue #746](https://github.com/datafolklabs/cement/issues/746)
- `[ext.generate]` Add optional features support to generate templates
  with conditional variables, exclude/ignore patterns, and dependency
  resolution via `requires` (with transitive cascade when a required
  feature is disabled). Resolution is order-independent — features may
  declare `requires` against features defined later in the YAML.
  - [Issue #743](https://github.com/datafolklabs/cement/issues/743)
- `[ext.generate]` Add `prompt_mode: select` for multi-valued feature
  prompts. A select-mode feature presents a numbered picker (delegated
  to `cement.utils.shell.Prompt`) and dispatches the chosen value into
  one of N `options` branches — each branch may declare its own
  `ignore` / `exclude` / `variables` (incl. silent `prompt: false`
  variables). `prompt_mode` defaults to `boolean` (legacy behavior,
  byte-identical when key absent).
  - [Issue #779](https://github.com/datafolklabs/cement/issues/779)
- `[ext.generate]` Add `type: choice` template variables — a numbered
  `cement.utils.shell.Prompt` picker that emits the chosen option string
  at the top level of the render context. `options:` accepts a scalar
  list or per-option `{value, prompt}` objects; per-option effects live
  in `extend:` rules keyed by `when: <value>`. Misconfig (empty options,
  option missing `value`, default not in options, duplicate labels) is
  fail-fast `ValueError`.
- `[ext.generate]` `type: boolean` `prompt:` is now polymorphic —
  in addition to the framework-owned string form and the silent
  `prompt: false` form, an object form `{text, accept, reject}` lets the
  template author own the full prompt text and supply case-insensitive
  `accept:`/`reject:` token lists that map input to a real bool. Input
  matching neither asserts and aborts (`Invalid Response`), mirroring
  `validate:`. A bool-like `accept:`/`reject:` token that YAML 1.1
  coerced to a Python bool raises `ValueError` telling the author to
  quote it.
- `[ext.generate]` `extend.when` now composes three match forms — a
  scalar value (equality), an in-list membership (`when: [a, b]`), and a
  string-type regex (`re.match`, string variables only) — and multiple
  matching rules all fire, accumulating their `variables`/`exclude`/
  `ignore`. `extend.variables` are nested and prompted depth-first in
  place only when their parent rule fires. A new top-level `requires:`
  key gates a variable using the same match vocabulary (`[name]` →
  truthy, `{name: value}` → equality, `{name: [v1, v2]}` → in-list),
  AND-ed across keys and resolved order-independently via lazy
  recursion. A requires-gated-out variable is set to its `default` (so
  templates never `KeyError`) and its `extend` rules do not fire. The
  unified schema also addresses the PR #780 review feedback: features
  prompt after vars in declaration order, with custom per-feature
  prompt text and vars-style input.
  - [Issue #782](https://github.com/datafolklabs/cement/issues/782)
  - [PR #780](https://github.com/datafolklabs/cement/pull/780)
- `[ext.argparse]` Add a read-only `_command_meta` property on
  `ArgparseController` so an exposed command can read its own `CommandMeta`
  (label, `parser_options['help']`, etc.) from inside its body via
  `self._command_meta`, replacing the brittle
  `getattr(self, ...).__cement_meta__` dance. Returns `None` outside a
  dispatched command and never raises. Additive — the `func()` dispatch
  signature is unchanged.
  - [Issue #670](https://github.com/datafolklabs/cement/issues/670)
- `[ext.argparse]` Add a companion read-only `_default_command_meta`
  property on `ArgparseController` that resolves the controller's default
  sub-command meta (via `Meta.default_func`), since `_command_meta` is
  `None` while the default function runs (argparse has no native default
  sub-command). Returns `None` when `default_func` is `None` or points to a
  non-exposed function (e.g. the stock `_default`); never raises.
  - [Issue #670](https://github.com/datafolklabs/cement/issues/670)
- `[utils.misc]` Add optional `CEMENT_FRAMEWORK_LOG_FILE` env var — when
  framework logging is enabled, framework/extension debug output is also
  written to the given file (in addition to the console). Purely additive:
  the variable alone does not enable logging, repeated calls do not stack
  duplicate handlers, and an unwritable/invalid path is ignored rather
  than raising.
  - [Issue #593](https://github.com/datafolklabs/cement/issues/593)

Refactoring:

- `[ext.generate]` Remove the unreleased `features:` schema
  (`prompt_mode`, `enabled:`/`disabled:` blocks, select `options:`
  effects) wholesale — everything it expressed is now a `type:
  boolean`/`type: choice` variable carrying `extend:`/`requires:`. The
  legacy compatibility bridge is deleted; `features:` is no longer read
  by the engine (#782).

- `[dev]` Migrate the `demo/generate-features/` webapp template to the
  unified `type:`/`extend:`/`requires:` schema (off the removed
  `features:` schema) and demonstrate the #782 fix — `{% if docker %}`
  and `{% if web_framework == ... %}` now render against the top-level
  bool/choice exposure
- `[ext.smtp]` PEP 8 naming, idiomatic string methods, and cleaner type validation
- `[ext.smtp]` Refactor `_make_message` into focused private methods
- `[ext.smtp]` Simplify X-header normalization and preserve original casing
- `[dev]` Python 3.14 Default Development Target
- `[dev]` Remove Support for Python 3.8 (EOL)
- `[dev]` Remove Support for Python 3.9 (EOL)
- `[cli]` Migrate `cement generate project` template from setuptools+setup.py
  to pdm-backend with full PEP 621 metadata; deps moved to
  `[project].dependencies` and `[dependency-groups].dev` (PEP 735); generated
  `version.py` simplified to literal `__version__` + wrapper (no build-time
  cement import)
- `[cli]` Generated project `README.md` now documents system requirements
  (Python 3.10+); end-user install uses `pip install .` / `pip install
  <label>`; development section calls out PDM as an additional requirement
  and uses `make setup` + `pdm run <label>`; generated `Makefile`
  `virtualenv` target renamed to `setup` and reduced to `pdm install`
  (drops redundant `pdm venv create` and the manual `eval $(pdm venv
  activate)` hint)
- `[core]` Modernize type annotations to PEP 585 builtin generics
  (UP006: `List` → `list`, `Dict` → `dict`, `Tuple` → `tuple`,
  `Type` → `type`); orphaned `typing` re-export imports pruned in the
  same pass (F401)
- `[core]` Modernize union types to PEP 604 syntax (UP007:
  `Union[X, Y]` → `X | Y`); orphaned `typing.Union` imports pruned
- `[core]` Modernize Optional types to PEP 604 syntax (UP045:
  `Optional[X]` → `X | None`); orphaned `typing.Optional` imports
  pruned
- `[core]` Move `Callable` / `Generator` imports from `typing` to
  `collections.abc` (UP035 — deprecated-import path).
- `[core]` Convert printf-style format strings to modern format
  (UP031 — `'%s' % x` → `f"{x}"` / `"{}".format(x)`). Protected
  `.format(**template_dict)` template-substitution callsites in
  cement/core/foundation.py preserved untouched per Phase 03 D-19.
  REFACTOR-04 closeout.
- `[core]` Drop redundant `(object)` base class (UP004); Python 3
  classes inherit from object implicitly.
- `[core]` Simplify `super()` calls (UP008 — drop `super(__class__,
  self)` boilerplate; Python 3 zero-arg form).
- `[core]` Drop redundant `'r'` mode argument from `open()` calls
  (UP015 — `'r'` is the default).
- `[core]` Replace `IOError` alias with `OSError` (UP024) in
  cement/core/template.py — `IOError` is an alias since Python 3.3.
- `[dev]` Drop legacy `u"..."` unicode literal prefix in test code
  (UP025) — Python 3 strings are already Unicode.
- `[dev]` Replace deprecated `mock` import with `unittest.mock`
  (UP026) in tests/ext/test_ext_smtp.py + tests/utils/test_shell.py.
- `[core]` Replace `for x in iterable: yield x` with `yield from`
  (UP028) in cement/core/hook.py + tests/core/test_hook.py.
- `[core]` Convert `.format()` calls to f-strings (UP032 cascade
  surfaced after UP031). Protected `.format(**template_dict)`
  template-substitution callsites in cement/core/foundation.py
  preserved untouched (verified by body-diff against pre-fix state).
  UP family fully clean after this commit.
- `[core]` Tighten `Any` types in cement/core/ where narrower types are
  provably correct; surviving Any carries inline justification per D-09
  (delta: 41 → 40, 2 substantive tightenings — `App.__import__(obj: Any)`
  → `obj: str` since the body always passes `obj` to stdlib `__import__`
  against `alternative_module_mapping: dict[str, str]`; and
  `ControllerInterface._dispatch() -> Any | None` → `-> Any` dropping
  the redundant `| None` Wave 3 UP007 cascade artifact).
- `[dev]` Refresh CONVENTIONS.md type-annotation guidance to
  PEP 585 / PEP 604 modern syntax (Phase 03 plan 03 landing point).
- `[core]` Wrap long log/error messages introduced by UP032 f-string
  conversion to satisfy E501 (line-too-long); reorder imports
  introduced by UP006/UP035 to satisfy I001 (import sorting).
- `[core]` Drop `from __future__ import annotations` from all 29
  files in cement/ (Phase 1 D-14 deferral closed). PEP 604/585
  syntax (UP006/UP007/UP045 from the prior wave) is native in
  Python 3.10+; the future-import is no longer needed. Forward
  references to TYPE_CHECKING-bound names (App, FrameType,
  ModuleType, TracebackType, ArgparseArgumentType,
  ArgparseController) converted to PEP 484 string annotations
  where evaluated at class/function definition time. Closes the
  cement/utils/fs.py self-flagged 2024-06-22 TODO.
- `[utils.fs]` Migrate `cement/utils/fs.py` os.path internals to
  pathlib (Phase 03 D-11). Public functions still return `str` via
  `str(p)` at every boundary (D-12 boundary preservation);
  `HOME_DIR` stays a `str` constant; `Tmp.dir` / `Tmp.file` stay
  `str` instance attributes. `pathlib.Path` aliased as `_Path`
  module-level to avoid expanding the public surface
  (audit-public-api stays exit 0). Lays foundation for
  cement/core/* migrations.
- `[core.config]` Migrate `cement/core/config.py` os.path.exists
  callsite in `parse_file` to pathlib (Phase 03 D-11 scope
  continuation). `import os` retained as a no-op (now `# noqa:
  F401`) because `cement.core.config:os` is in
  `03-PUBLIC-API-BASELINE.txt` — removing it would have shrunk
  the public surface (D-12). Smallest of the four pathlib
  commits (1 callsite); natural warm-up after fs.py per D-13.
- `[core.foundation]` Migrate `cement/core/foundation.py`
  os.path.isdir callsite in `_find_config_files` to pathlib
  (Phase 03 D-11). The public alias `join = os.path.join` (line
  48) retained per D-12/D-14 with `# boundary:` tag — it is part
  of the public-API baseline (`cement.core.foundation:join`)
  with stdlib semantics that downstream callers depend on.
  D-19 protected `.format(**template_dict)` callsites at lines
  1383, 1388, 1396, 1401, 1409, 1414, 1502, 1507, 1512, 1516,
  1577, 1582, 1587, 1591 (14 total) untouched. A docstring
  example referencing `os.path.dirname` / `os.path.exists` /
  `os.makedirs` updated to pathlib idioms for consistency.
- `[core.template]` Migrate `cement/core/template.py` os.path
  internals to pathlib (Phase 03 D-11; ~13 callsites — biggest
  single-file blast in the pathlib scope). Boundary-preservation
  rule (D-12) held; internal locals are Path; values crossing
  the loop iteration go back through `str()` because the
  surrounding loop variables (`cur_dir_dest`, `sub_dir_dest`,
  `_file`, `_file_dest`, `full_path`) are passed to legacy
  string-typed APIs (`fs.abspath`, `self.render`, `open`). The
  `os.walk(src)` callsite is retained with an inline `# boundary:`
  comment per D-14 — pathlib has no direct equivalent yielding
  the `(cur_dir, sub_dirs, files)` triple shape this loop
  depends on; converting to `Path.rglob('*')` would require a
  wholesale loop restructure with higher regression risk than
  the boundary-tag accommodation. Closes the D-11 pathlib scope
  across all 4 named files; D-24 conjunct #8 GREEN
  (`grep -rn 'os\.path' cement/utils/fs.py cement/core/* | grep
  -v '# boundary:' | wc -l` returns 0).
- `[dev]` Audit `pragma:nocover` sites in `cement/core/` with
  D-15 locked-vocabulary category labels (Phase 03 Wave 7
  Batch A — 16 files / per-file atomic commits). Categories
  applied: `abstract method`, `TYPE_CHECKING import`,
  `platform-specific`, `defensive: unreachable`,
  `untestable: signal handler`, `version constant`. Coverage
  exclusion behavior unchanged; pragma comments now carry
  audit-grep-friendly category labels per D-15.
- `[dev]` Audit `pragma:nocover` sites in `cement/ext/` first
  half (ext_alarm, ext_argparse, ext_colorlog, ext_configparser,
  ext_daemon, ext_dummy, ext_generate, ext_jinja2, ext_json,
  ext_logging) with D-15 locked-vocabulary category labels
  (Phase 03 Wave 7 Batch B — 10 files / per-file atomic
  commits). Categories applied: `TYPE_CHECKING import`,
  `defensive: unreachable`, `untestable: dynamic import`,
  `platform-specific`.
- `[dev]` Audit `pragma:nocover` sites in `cement/ext/` second
  half (ext_memcached, ext_mustache, ext_plugin, ext_print,
  ext_redis, ext_scrub, ext_smtp, ext_tabulate, ext_watchdog,
  ext_yaml) with D-15 locked-vocabulary category labels
  (Phase 03 Wave 7 Batch C — 10 files / per-file atomic
  commits). Categories applied: `TYPE_CHECKING import`,
  `defensive: unreachable`, `untestable: dynamic import`.
- `[dev]` Audit `pragma:nocover` sites in `cement/cli/` +
  `cement/utils/` (cli/main.py, utils/fs.py, utils/shell.py,
  utils/version.py) with D-15 locked-vocabulary category
  labels (Phase 03 Wave 7 Batch D — 4 files / per-file
  atomic commits). Closes COV-03 / D-24 conjunct #7 across
  all of cement/: `grep -nE 'pragma:[[:space:]]*no[[:space:]]*cover' cement/ | grep -vE '# (<8 categories>)'`
  returns empty (141 sites all carry locked-vocabulary
  category labels).
- `[core.deprecations]` Pin 3.0.10-1 and 3.0.16-1 removal version to v3.2.0
- `[ext.logging]` Tighten FATAL deprecation removal version in docstrings
- `[ext.smtp]` Document send() bool-return removal in v3.2.0
- `[cli]` Migrate `cement generate todo-tutorial` template from
  setup.py/setup.cfg/requirements*.txt/MANIFEST.in to pdm-backend with
  full PEP 621 metadata and a PEP 735 dev group (mirrors the `generate
  project` migration; #735)
- `[cli]` Ship `[tool.ruff]` / `[tool.mypy]` / `[tool.pytest]` gate
  config in the generated project and todo-tutorial `pyproject.toml` so
  `make comply` and `make test` are green out of the box (#735)
- `[cli]` Type-annotate all generated templates (project/script/
  extension/plugin/todo) and modernize idioms to f-strings (#735)

Misc:

- `[ci]` Add automated release workflow (`release.yml`) — tag-triggered
  pipeline: preflight guard → full gate suite → isolated build → TestPyPI
  publish + 5-Python install smoke → environment-gated OIDC PyPI publish
  (single human approval) → post-approval fan-out (Docker Hub multi-arch
  images, `stable/3.0.x` fast-forward, RTD docs-tag re-point, GitHub
  Release from changelog, dev-version-bump PR, post-release checklist
  issue); `workflow_dispatch` runs the same pipeline as a dry run
- `[ci]` Refactor PR gate chain into reusable `gates.yml`
  (`workflow_call`) shared by PR CI and the release workflow; add new
  Windows core-test and macOS/Windows native CLI smoke gates
- `[dev]` Add release dev-tooling scripts: `testpypi-smoke.py`
  (TestPyPI install round-trip), `cli-smoke-native.py` (cross-platform
  CLI smoke), `bump_dev_version.py` (post-release dev-cycle bump)
- `[ext.smtp]` Isolate test defaults to prevent cross-test state pollution
- `[dev]` Bump ruff to 0.15.x; codify rule sets explicitly; resolve all
  surfacing lint findings (I001, B*, A*, C901, N*, PT*, T201, YTT203)
- `[dev]` Bump mypy to ~=1.20.2; codify type-check surface (audit-point comment)
- `[dev]` Bump pytest 9.0.3, pytest-cov 7.1.0, coverage 7.13.5
- `[dev]` Add `make cli-smoke-test` target — runs generated-project install
  smoke test across Python 3.10–3.14 in Docker
- `[dev]` Bump dev/extras lockfile to current non-breaking versions (redis
  7.4, watchdog 6.0, tabulate 0.10, sphinx 8.1, requests 2.33, others)
- `[dev]` Wire 100% coverage gate via `[tool.coverage.report]`
  `fail_under` + `--cov-fail-under` addopts; explicit
  `[tool.coverage.run] source/omit`
- `[ci]` Pin GitHub Actions to exact tags (checkout v6.0.2,
  setup-python v6.2.0, setup-pdm v4.4, install-package v1.1.0,
  compose-action v2.6.0, update-deps-action v1.12)
- `[ci]` Add PyPy 3.11 to CI test matrix (alongside existing PyPy 3.10)
- `[ci]` Enable Dependabot for github-actions ecosystem (weekly)
- `[ci]` Add workflow_dispatch trigger to pdm.yml
- `[dev]` Add `make audit-public-api` target + AST-walk public surface enumerator + baseline snapshot (Phase 03 D-02..D-05).
- `[dev]` Enable ruff `UP` (pyupgrade) and `FA` (flake8-future-annotations) families in extend-select with refreshed AUDIT POINT comment (Phase 03 D-06).
- `[dev]` Capture Phase 03 Any-in-core baseline (D-09) + pragma + pathlib pre-counts in `03-VERIFICATION.md` (in-progress; finalized in Wave 8).
- `[dev]` Phase 03 verification finalized: all 9 D-24 conjuncts GREEN;
  REFACTOR-01..04 + COV-01..03 satisfied; record in
  `03-VERIFICATION.md`.
- `[dev]` Phase 03 (Internal Refactor & Coverage Hardening) complete:
  REFACTOR-01..04 + COV-01..03 satisfied; ROADMAP updated.
- `[docs]` Drop unsupported 'logo' theme option from sphinx conf
- `[docs]` Remove orphan `docs/source/api/index.rst`; the top-level
  `docs/source/index.rst` toctree references `api/core/index`,
  `api/utils/index`, and `api/ext/index` directly
- `[docs]` Rename `display_version` theme option to `version_selector`
  (sphinx_rtd_theme 3.x rename)
- `[docs]` Fix inline-literal RST in shell.cmd() docstring
- `[docs]` Add top-level DEPRECATIONS.md mirroring GitBook narrative
- `[dev]` Wire -W into make docs (zero-warnings gate)
- `[docs]` Drop Travis CI link/badge (CI moved to GitHub Actions)
- `[docs]` Align CONTRIBUTING with Conventional Commits +
  atomic-per-concern
- `[docs]` Expose `cement.core.deprecations` in the Sphinx API
  reference (was missing) — adds `docs/source/api/core/deprecations.rst`
  + toctree entry, plus minimal docstrings on the module,
  `DEPRECATIONS` dict, and `deprecate()` so the autodoc page renders
  meaningful content rather than an empty stub
- `[docs]` Fix `stderror` → `stderr` typo in `cement.utils.shell:cmd()`
  and `exec_cmd()` Returns docstrings (4 occurrences). Example
  variables and runtime code already used the correct spelling
- `[docs]` Remove orphaned `[Commit Guidelines]` reference-link
  definition from `.github/CONTRIBUTING.md` (no body callsites
  remained after the Plan 05-05 Conventional Commits rewrite)
- `[dev]` Extend the CI `cli-smoke-test` to gate the generated
  project's own `make comply` + `make test` and to build/install the
  generated todo-tutorial (#735)
- `[dev]` Add a generated-todo ruff-clean regression guard to cement's
  test suite (`test_generate_todo_ruff_clean`) — generates
  todo-tutorial and re-runs ruff against the rendered output (#735)

Deprecations:

- `[ext.smtp]` `SMTPMailHandler.send()` returning `bool` is deprecated; will return `senderrs` dict in a future version


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
