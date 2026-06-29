# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## CORE Tenants for Agents

1. Ask, don't assume. If something is unclear, ask before writing a single line. Never make silent assumptions about intent, architecture, or requirements. When running unattended, pick the most reasonable interpretation, proceed, and record the assumption rather than blocking.
2. Implement the simplest solution for simple problems, better solutions for harder problems. Do not over-engineer or add flexibility that isn't needed yet.
3. Don't touch unrelated code but please do surface bad code or design smells you discover with me so we can address them as a separate issue.
4. Flag uncertainty explicitly. If you're unsure about something, see point 1 above. If it makes sense to do so, conduct a small, localised and low-risk experiment and bring the hypothesis and results to me to discuss. Confidence without certainty causes more damage than admitting a gap.
5. I'm always open to ideas on better ways to do things. Please don't hesitate to suggest a better way, or one that has long lasting impact over a tactical change. (as a few examples)


## Development Commands

**Testing and Compliance:**
- `make test` - Run full test suite with coverage and PEP8 compliance
- `make test-core` - Run only core library tests
- `make comply` - Run both ruff and mypy compliance checks
- `make comply-ruff` - Run ruff linting
- `make comply-ruff-fix` - Auto-fix ruff issues
- `make comply-mypy` - Run mypy type checking
- `pdm run pytest --cov=cement tests/` - Direct pytest execution
- `pdm run pytest --cov=cement.core tests/core` - Test only core components

**Development Environment:**
- `make init` - Set up local development environment
- `pdm run cement --help` - Run the cement CLI

**Documentation:**
- `make docs` - Build Sphinx documentation

**Build and Distribution:**
- `pdm build` - Build distribution packages

## Architecture Overview

Cement is a CLI application framework built around a handler/interface pattern with the following core concepts:

**Core Application (`cement.core.foundation.App`):**
- The main `App` class in `cement/core/foundation.py` is the central orchestrator
- Uses a Meta class pattern for configuration
- Manages lifecycle through setup(), run(), and close() methods
- Supports signal handling and application reloading

**Handler System:**
- Interface/Handler pattern where interfaces define contracts and handlers provide implementations
- Core handlers: arg, config, log, output, cache, controller, extension, plugin, template
- Handlers are registered and resolved through `HandlerManager`
- Located in `cement/core/` with corresponding modules (arg.py, config.py, etc.)

**Extensions System:**
- Extensions in `cement/ext/` provide additional functionality
- Examples: ext_yaml.py, ext_jinja2.py, ext_argparse.py, etc.
- Optional dependencies managed through pyproject.toml extras

**CLI Structure:**
- Main CLI application in `cement/cli/main.py`
- Uses CementApp class that extends core App
- Includes code generation templates in `cement/cli/templates/`

**Controllers:**
- MVC-style controllers handle command routing
- Base controller pattern in controllers/base.py files
- Support nested sub-commands and argument parsing

## Key Development Practices

- 100% test coverage required (pytest with coverage reporting)
- 100% PEP8 compliance enforced via ruff
- Type annotation compliance via mypy
- PDM for dependency management
- Zero external dependencies for core framework (optional for extensions)

## Testing Notes

- Tests located in `tests/` directory mirroring source structure
- Core tests can run independently via `make test-core`
- Coverage reports generated in `coverage-report/` directory

## Extension Development

When working with extensions:
- Check `cement/ext/` for existing extension patterns
- Optional dependencies declared in pyproject.toml under `[project.optional-dependencies]`
- Extensions follow naming pattern `ext_<name>.py`
- Must implement proper interface contracts

## Commit Conventions

- All commits MUST follow [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, `ci:`)
- Subject line: max 78 characters
- Body lines: max 78 characters (wrap longer prose at 78)
- Use `make commit` (runs `pdm run cz commit`) to author commits interactively

## Branching Policy

- **NEVER commit directly to `main` without explicit consent.** This includes
  implementation, tests, docs, AND planning artifacts (`docs(NN.N):`,
  `docs(state):`, etc.) — planning commits are work too.
- **Branch immediately when work begins** — at the start of planning a phase or
  task, not at execution time. The branch is the unit of consent; everything for
  a phase (plan + execute) belongs on it.
- Branch naming: `gsd/phase-{phase}-{slug}` for phase work; otherwise a short,
  descriptive `feat/...`, `fix/...`, or `docs/...` slug.
- If you discover you are on `main` with uncommitted or committed work that was
  not consented to, STOP and surface it: create a branch capturing the work,
  then propose restoring `main` before doing anything else.
- The GSD `branching_strategy` config defaults to `none`, which keeps work on
  the current branch — do NOT rely on it to branch for you. Branching is a
  standing requirement regardless of that setting; if it is `none`, branch
  manually before the first commit.
- Merging branches into `main` is the user's call (typically via PR) — do not
  fast-forward or merge to `main` without being asked.

## Changelog Maintenance

- Update `CHANGELOG.md` phase-by-phase as work lands; do not defer to release-cut time
- Append entries to the active `## X.Y.Z - DEVELOPMENT` section using the existing buckets: **Bugs**, **Features**, **Refactoring**, **Misc**, **Deprecations**
- Each entry: one line, prefixed with `[area]` — e.g., `[ext.smtp]`, `[cli]`, `[dev]`, `[core.handler]`
- Filter out planning-artifact commits (`docs(NN.N):`, `docs(state):`, `docs(quick-...):`) — they are workflow scaffolding, not user-facing changes
- Filter out commits superseded within the same branch (revert pairs, overwrites) — only the net effect ships in the changelog
- Bucket by Conventional Commit type: `fix:` → Bugs, `feat:` → Features, `refactor:` → Refactoring, `chore:` (deps/tooling/dev-env) → Misc; structural removals (drop Python version, replace toolchain) or substantive structural reshuffles → Refactoring

## GitHub Project

This project is hosted at **github.com/datafolklabs/cement**. Use the `gh` CLI to interact with GitHub issues, pull requests, and other project resources.

- `gh issue list -R datafolklabs/cement` - List open issues
- `gh issue view <number> -R datafolklabs/cement` - View a specific issue
- `gh pr list -R datafolklabs/cement` - List open pull requests
- `gh pr view <number> -R datafolklabs/cement` - View a specific PR
- `gh pr checks <number> -R datafolklabs/cement` - View CI status for a PR
- `gh api repos/datafolklabs/cement/pulls/<number>/comments` - View PR review comments

<!-- GSD:project-start source:PROJECT.md -->
## Project

**Cement**

Cement is a mature, extensible Python CLI application framework built around a handler/interface/extension pattern. It gives Python developers a batteries-included foundation for building CLI apps — argument parsing, config, logging, output rendering, plugins, hooks, and lifecycle management — while staying pluggable enough to swap any piece. This initiative kicks off GSD-driven modernization and long-term maintenance of the Cement 3 line.

**Core Value:** **Cement 3 stays solid, secure, performant, and bug-free under strict backward compatibility — while being continuously maintained against a modern Python and tooling ecosystem.** When tradeoffs arise, stability of the public API wins over everything else; anything that would break a downstream user's app without consent is out of bounds for 3.0.x and 3.2.x release cuts.

### Constraints

- **Compatibility**: Zero public-API breakage on the 3.0.x track — including subclass-exposed internals that downstream extensions may rely on. Deprecation warnings OK; removals go to 3.2.0 at the earliest.
- **Tech stack**: Python 3.10–3.14 after this milestone (3.9 dropped per upstream EOL policy). PDM for dependencies. No new runtime dependencies for the core framework — extensions may add optional deps.
- **Quality gates**: 100% test coverage, PEP8 via ruff, mypy type-checking — all absolute. Every phase must leave these at green.
- **Dependencies — core**: Core framework must remain zero-runtime-dependency. Optional extras handled via `[project.optional-dependencies]`.
- **Release gating**: No release cut until all phases pass, CI is green on the full Python matrix, and the issue backlog is at a known clean state.
- **Policy — Python support**: Drop Python versions on upstream EOL date. Standing rule, enforced in this milestone by dropping 3.9.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- Python 3.9+ - Entire framework and CLI application
## Runtime
- Python (3.9, 3.10, 3.11, 3.12, 3.13, 3.14 supported)
- PDM (Python Dependency Manager)
- Lockfile: `pdm.lock` (present)
## Frameworks
- Cement - Self (CLI application framework with handler/interface pattern)
- Argparse - Command-line argument parsing (extension: `cement/ext/ext_argparse.py`)
- Jinja2 - Template rendering (extension: `cement/ext/ext_jinja2.py`)
- Mustache - Template rendering alternative (extension: `cement/ext/ext_mustache.py`)
- ConfigParser - INI file parsing (extension: `cement/ext/ext_configparser.py`)
- YAML - YAML file parsing (extension: `cement/ext/ext_yaml.py`)
- Python logging stdlib - Core logging framework (extension: `cement/ext/ext_logging.py`)
- ColorLog - Colored console logging (extension: `cement/ext/ext_colorlog.py`)
- pytest 4.3.1+ - Test runner
- pytest-cov 2.6.1+ - Coverage reporting
- coverage 4.5.3+ - Coverage measurement
- mock 5.1.0+ - Object mocking
- ruff 0.3.2+ - Linting and code formatting
- mypy 1.9.0+ - Static type checking
- Sphinx - Documentation builder
- sphinx_rtd_theme - ReadTheDocs theme
- guzzle_sphinx_theme - Alternative theme
- sphinxcontrib-napoleon - Google/NumPy docstring support
- pdm-backend - Build system backend
- PDM - Dependency and package management
## Key Dependencies
- None - Cement core has **zero external dependencies**
- `colorlog` - For colored logging output
- `jinja2` - For Jinja2 template rendering
- `pyyaml` - For YAML config/output support
- `redis` - For Redis-based caching
- `pylibmc` - For Memcached support
- `watchdog` - For file system event watching
- `pystache` - For Mustache template rendering
- `tabulate` - For ASCII table formatting
- `requests` - For HTTP requests (dev dependency)
- `pypng` - For PNG image handling (dev dependency)
## Configuration
- Development environment via Devbox with pre-installed services (Redis, Memcached, Mailpit)
- Docker Compose setup for multi-version testing (Python 3.9 - 3.14)
- Environment variables for service configuration:
- `pyproject.toml` - Primary project configuration
- `pdm.lock` - Dependency lock file
- Ruff config in `pyproject.toml` (`[tool.ruff]`):
- MyPy config in `pyproject.toml` (`[tool.mypy]`):
- Pytest config in `pyproject.toml` (`[tool.pytest.ini_options]`):
## Platform Requirements
- Devbox environment manager with:
- Docker Compose for multi-version testing
- Makefile-based workflow
- Python 3.9 or higher
- No external runtime dependencies required for core framework
- Optional services (Redis, Memcached, SMTP) if using corresponding extensions
- Alpine Linux compatible (see `Dockerfile` for production image)
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- Module files: lowercase with underscores (`foundation.py`, `ext_smtp.py`)
- Classes: PascalCase (e.g., `FrameworkError`, `SMTPMailHandler`, `MetaMixin`)
- Test files: `test_<module>.py` pattern (e.g., `test_foundation.py`, `test_ext_smtp.py`)
- Public methods: lowercase_with_underscores (`parse_file()`, `_setup_arg_handler()`)
- Private/internal methods: leading underscore (`_get_params()`, `_parse_file()`)
- Test functions: `test_<feature>()` pattern (e.g., `test_smtp_send()`, `test_basic()`)
- Constants: UPPERCASE_WITH_UNDERSCORES (environment variables, signal lists)
- Instance variables: lowercase_with_underscores
- Module-level logger: `LOG = minimal_logger(__name__)`
- Use PascalCase for class names
- Type annotations use full form: `Dict[str, Any]`, `Optional[str]`, `List[str]`, `Tuple[int, str]`
- Private Meta attribute annotations: `_meta: MetaClassName  # type: ignore` (see `cement/ext/ext_smtp.py` line 72)
## Code Style
- Tool: `ruff` (v0.3.2+)
- Line length: 100 characters
- Indentation: 4 spaces
- Python target: 3.9+
- Tool: `ruff check cement/ tests/`
- All code must pass without errors before commit
- Run via `make comply-ruff`
## Import Organization
- No centralized alias configuration; use relative imports exclusively (`..core.`, `..utils.`)
## Type Annotations
- mypy config in `pyproject.toml` enforces strict mode:
- Always annotate function parameters and return types: `def send(self, msg: str, **kw: Any) -> Dict[str, Any]:`
- Use `TYPE_CHECKING` block for deferred imports to prevent circular dependencies
- Private Meta attributes require `# type: ignore` due to metaclass pattern (framework constraint)
- Union types: `Union[str, int]` for multiple types
## Error Handling
- `FrameworkError` - General framework (non-application) errors with message passing
- `InterfaceError` - Interface-related errors
- `CaughtSignal(signum, frame)` - Raised when signal is caught
- Raise framework exceptions for framework-level errors
- Custom applications should extend `FrameworkError` for app-specific exceptions
- Always include a message: `raise FrameworkError("descriptive message")`
## Logging
- Module-level logger created as: `LOG = minimal_logger(__name__)`
- No logging.config setup needed; minimal logger is intentionally simple for framework
- Use `LOG.debug()` for framework internals: `LOG.debug(f'hook {hook_spec[0]} not defined')`
- Framework runs silently by default; debug output only when app.debug is True
- No INFO/WARNING/ERROR logging in framework core (by design)
## Comments
- Framework code is internally documented via docstrings; comments for non-obvious logic
- Use `# FIXME:` for known issues that need attention (e.g., line 125 in `foundation.py`)
- Use `# pragma: nocover` for unreachable code in handlers/interfaces (abstract methods)
- Use `# type: ignore` for framework Meta pattern workarounds (mypy limitation)
- Use `# noqa: E501` to suppress line-too-long warnings for long strings (deprecation messages)
## Docstring Style
- Class docstrings: one-line description + Args/Returns sections
- Method docstrings: one-line + Args/Returns if needed
- Abstract methods: `pass    # pragma: nocover`
## Meta Class Pattern
- `MetaMixin` base class provides `self._meta` attribute via MRO merging
- Each class defines nested `Meta` inner class with configuration
- Meta attributes cascade through inheritance: parent Meta → child Meta → kwargs
- Used throughout: `App`, `Handler`, `Interface`, all handler implementations
- Read: `self._meta.label`, `self._meta.config_section`
- Frameworks queries: `handler._meta.interface`, `handler._meta.overridable`
## Handler/Interface Contracts
- Interface defines abstract methods in `InterfaceHandler` base
- Concrete handlers implement interface and subclass `Handler`
- All handlers must define `Meta.label` and `Meta.interface`
## Function Design
- Keep functions focused; multi-responsibility functions are common in setup/teardown (40-60 lines acceptable for setup methods)
- Private helper methods should be small (<30 lines)
- Prefer `**kwargs` for optional parameters (handler/interface pattern)
- Always type all parameters and return values
- Default values for kwargs handled via `Meta.config_defaults` pattern (not function signatures)
- Return types must be explicit (no `-> Any` without reason)
- Boolean returns for success/failure (parse_file returns `bool`)
- Dict/List returns should be typed: `-> Dict[str, Any]`, `-> List[str]`
## Module Design
- Core framework exports via `__all__` lists in main modules (not observed, but interface defines implicit contracts)
- Private functions/classes prefixed with `_`
- Not used; direct imports from submodules preferred
## PEP 8 Compliance
- All code must pass before commit
- Ruff auto-fix available: `make comply-ruff-fix`
- Violations will block CI (see `.github/workflows/build_and_test.yml`)
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## Pattern Overview
- **Interface-driven design:** Core interfaces (`ArgumentInterface`, `ConfigInterface`, `LogInterface`, `OutputInterface`, etc.) define abstract contracts that handlers must implement
- **Handler registry system:** A `HandlerManager` registers, retrieves, and resolves handlers by interface and label (e.g., `app.handler.get('output', 'json')`)
- **Meta class pattern:** Configuration via nested `Meta` classes that are merged through MRO (method resolution order); allows inheritance-based configuration
- **Lifecycle hooks:** Extensible hook system (`pre_setup`, `post_setup`, `pre_run`, `post_run`, `pre_close`, `post_close`, `signal`, `pre_render`, `post_render`) for plugins to inject behavior
- **Extension/Plugin loading:** Dynamic module loading for optional functionality and application-level extensions
## Layers
- Purpose: Main entry point and orchestrator for the framework
- Location: `cement/core/foundation.py` (the `App` class)
- Contains: Application lifecycle methods (`setup()`, `run()`, `close()`), handler setup methods, argument parsing, configuration management, signal handling
- Depends on: All handler interfaces, `HookManager`, `InterfaceManager`, `HandlerManager`
- Used by: CLI applications (e.g., `CementApp` in `cement/cli/main.py`)
- Purpose: Manages registration, resolution, and instantiation of handlers
- Location: `cement/core/handler.py` (`Handler` base class, `HandlerManager`)
- Contains: Base handler class, manager for registering/resolving handlers by interface and label
- Depends on: Interface definitions
- Used by: Application during setup, extensions during registration
- Purpose: Defines abstract contracts for pluggable components
- Location: `cement/core/` (individual interface files: `arg.py`, `config.py`, `output.py`, `log.py`, `controller.py`, `extension.py`, `plugin.py`, `template.py`, `cache.py`, `mail.py`)
- Contains: Interface abstract base classes (e.g., `ArgumentInterface`, `ConfigInterface`) with abstract methods
- Depends on: Abstract base classes (`ABC`)
- Used by: Handler implementations
- Purpose: Default implementations of core interfaces
- Location: `cement/core/` (same files as interfaces, e.g., `ArgumentHandler` in `arg.py`) and `cement/ext/` (optional extensions like `ext_argparse.py`, `ext_configparser.py`, `ext_logging.py`)
- Contains: Concrete handler classes inheriting from both interface and `Handler`
- Examples:
- Depends on: Interface definitions, `Handler` base class
- Purpose: Manages dynamic loading of extensions (handlers and hooks)
- Location: `cement/core/extension.py` (`ExtensionInterface`, `ExtensionHandler`) and `cement/ext/ext_plugin.py`
- Contains: Extension loading mechanism; `load_extension()` imports modules and calls their `load()` function if present
- Pattern: Each extension module (e.g., `cement/ext/ext_json.py`) has a `load(app)` function that registers handlers and hooks
- Depends on: Handler system, hook system
- Used by: Application during setup
- Purpose: Application-level plugins loaded from configuration and plugin directories
- Location: `cement/core/plugin.py` (`PluginInterface`, `PluginHandler`)
- Contains: Plugin discovery and loading from filesystem and config
- Pattern: Plugins are Python modules in designated directories that implement a `load(app)` function
- Depends on: Configuration, filesystem navigation
- Used by: Application during setup
- Purpose: Event-driven extension mechanism for framework and application lifecycle
- Location: `cement/core/hook.py` (`HookManager`)
- Contains: Hook definition, registration, and execution with weight-based ordering
- Pattern: Named hooks (e.g., `pre_setup`, `post_setup`) are defined during `_lay_cement()`, then functions register to them with optional weight (lower weight = higher priority)
- Depends on: Function references
- Used by: Application throughout lifecycle, extensions for behavior injection
- Purpose: Maps command-line arguments to handler functions
- Location: `cement/ext/ext_argparse.py` (`ArgparseController`)
- Contains: Argument parsing via `argparse`, nested controller support, method dispatch based on parsed args
- Pattern: Controllers inherit from `Controller` (alias for `ArgparseController`), use `@expose()` decorator on methods to register them as commands
- Depends on: Argument handler interface
- Used by: Application's `run()` method
- Purpose: Multi-level configuration from files, directories, and environment
- Location: `cement/core/config.py` (interface) and `cement/ext/ext_configparser.py` (ConfigParser impl)
- Contains: Config file parsing, section-based storage, config defaults from handlers
- Precedence: System config → User config → Application config → Command-line overrides
- Depends on: Filesystem, environment
- Used by: Application setup, handler initialization
## Data Flow
- **Application Meta:** Configuration stored in `app._meta` (merged from `App.Meta` class hierarchy and keyword args)
- **Parsed Arguments:** `app.pargs` (set during argument parsing, accessible to controllers)
- **Last Rendered Output:** `app._last_rendered` tuple of `(data, output_text)`
- **Handler State:** Handlers store state in instance attributes (e.g., `config.data`, `log.logger`)
- **Loaded Extensions/Plugins:** Tracked in `app.ext._loaded_extensions`, `app.plugin.get_enabled_plugins()`
## Key Abstractions
- **Purpose:** Abstract interface contracts with concrete implementations
- **Examples:**
- **Pattern:** Interface defines abstract methods; handler implements them. App resolves handlers by interface label + handler label (e.g., `app.handler.get('output', 'json')`).
- **Purpose:** Inheritance-based configuration inheritance
- **Example:**
- **How it works:** `MetaMixin.__init__()` walks MRO, collects all `Meta` classes, merges them (later in MRO overrides earlier), then applies kwargs. Result stored in `self._meta`.
- **Purpose:** Resolve handler definitions (string label, uninstantiated class, or instance) to instantiated, setup handler
- **Process:**
- **Purpose:** Event-driven extension points throughout lifecycle
- **Pattern:** Functions register to named hooks with optional weight; when hook is run, functions execute in weight order (lower weight first)
- **Example:**
- **Built-in hooks:** `pre_setup`, `post_setup`, `pre_run`, `post_run`, `pre_close`, `post_close`, `signal`, `pre_render`, `post_render`
- **Purpose:** Register handlers and hooks in a pluggable way
- **Pattern:** Each extension module (e.g., `cement/ext/ext_json.py`) implements:
- **Load trigger:** `ExtensionHandler.load_extension(module_name)` imports the module, then calls `module.load(app)` if it exists
## Entry Points
- Location: `cement/cli/main.py:main()`
- Triggers: Called from `setuptools` entry point (see `pyproject.toml`)
- Responsibilities:
- Extends: `App` base class
- Meta configuration:
- Extends: `Controller` (alias for `ArgparseController`)
- Meta:
- Methods:
## Error Handling
- **Interface/Handler Errors:** `cement.core.exc.InterfaceError` when interface not defined or handler doesn't implement interface
- **Framework Errors:** `cement.core.exc.FrameworkError` for general framework issues (e.g., missing required config, invalid labels)
- **Caught Signals:** `cement.core.exc.CaughtSignal` raised when signal handler catches SIGTERM/SIGINT/SIGHUP
- **Signal Handling:** Signals trigger `cement_signal_handler()` which runs `signal` hook then raises `CaughtSignal`
- **Config Validation:** `validate_config()` can be overridden to check config after loading
- **Handler Fallback:** `handler.get()` and `handler.resolve()` support optional `fallback` parameter for graceful degradation
## Cross-Cutting Concerns
- Framework uses `minimal_logger()` for internal logging (see `cement/utils/misc.py`)
- App delegates logging to configured `log_handler` (default: `LoggingLogHandler` from `ext_logging`)
- Debug mode enabled via `--debug` flag or `debug=True` in config
- Handlers perform `_validate()` in `_setup()` to ensure proper initialization
- Interfaces define validation hook that subclasses can override
- Application calls `validate_config()` after loading configuration
- Not built into core framework (application responsibility)
- Can be implemented via hooks (e.g., `post_setup` to check credentials)
- Config can store auth-related settings (e.g., API keys in config files)
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
