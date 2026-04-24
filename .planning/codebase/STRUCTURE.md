# Codebase Structure

**Analysis Date:** 2026-04-24

## Directory Layout

```
cement/
├── cement/
│   ├── __init__.py           # Main package exports (App, Handler, Interface, etc.)
│   ├── core/                 # Core framework (interfaces, handlers, managers)
│   │   ├── foundation.py     # App class (central orchestrator)
│   │   ├── interface.py      # Interface and InterfaceManager
│   │   ├── handler.py        # Handler base class and HandlerManager
│   │   ├── hook.py           # HookManager (event system)
│   │   ├── meta.py           # Meta and MetaMixin (configuration pattern)
│   │   ├── arg.py            # ArgumentInterface
│   │   ├── config.py         # ConfigInterface
│   │   ├── log.py            # LogInterface
│   │   ├── output.py         # OutputInterface
│   │   ├── template.py       # TemplateInterface
│   │   ├── controller.py     # ControllerInterface
│   │   ├── extension.py      # ExtensionInterface and ExtensionHandler
│   │   ├── plugin.py         # PluginInterface
│   │   ├── cache.py          # CacheInterface
│   │   ├── mail.py           # MailInterface
│   │   ├── exc.py            # Exception classes
│   │   └── deprecations.py   # Deprecation warnings
│   │
│   ├── ext/                  # Extensions (optional handlers)
│   │   ├── __init__.py
│   │   ├── ext_argparse.py   # ArgparseArgumentHandler, ArgparseController
│   │   ├── ext_configparser.py # ConfigParserConfigHandler
│   │   ├── ext_logging.py    # LoggingLogHandler
│   │   ├── ext_json.py       # JsonOutputHandler
│   │   ├── ext_yaml.py       # YamlOutputHandler, YamlConfigHandler
│   │   ├── ext_jinja2.py     # Jinja2TemplateHandler
│   │   ├── ext_dummy.py      # DummyOutputHandler, DummyTemplateHandler, DummyMailHandler
│   │   ├── ext_plugin.py     # CementPluginHandler (plugin discovery/loading)
│   │   ├── ext_colorlog.py   # ColorLogHandler
│   │   ├── ext_smtp.py       # SmtpMailHandler
│   │   ├── ext_redis.py      # RedisOutputHandler, RedisCacheHandler
│   │   ├── ext_memcached.py  # MemcachedCacheHandler
│   │   ├── ext_tabulate.py   # TabulateOutputHandler
│   │   ├── ext_scrub.py      # Data scrubbing utilities
│   │   ├── ext_daemon.py     # Daemon mode support
│   │   ├── ext_alarm.py      # Signal-based timeouts
│   │   ├── ext_watchdog.py   # File watching (reload on changes)
│   │   ├── ext_mustache.py   # Mustache template handler
│   │   ├── ext_print.py      # Print output handler
│   │   └── ext_generate.py   # Code generation extension
│   │
│   ├── cli/                  # Cement framework CLI application
│   │   ├── main.py           # CementApp (extends App), main() entry point
│   │   ├── controllers/      # CLI command controllers
│   │   │   ├── __init__.py
│   │   │   └── base.py       # Base controller (help, version)
│   │   └── templates/        # Code generation templates
│   │       └── generate/     # Project templates (todo-tutorial, etc.)
│   │
│   ├── utils/                # Utility functions
│   │   ├── __init__.py
│   │   ├── misc.py           # minimal_logger(), init_defaults(), is_true(), etc.
│   │   ├── fs.py             # File system utilities (abspath, HOME_DIR, etc.)
│   │   ├── shell.py          # Shell execution utilities
│   │   ├── scrub.py          # Data scrubbing (PII redaction)
│   │   └── version.py        # Version handling
│   │
│   └── backends/             # (If present) Backend-specific implementations
│
├── tests/                    # Test suite (mirrors source structure)
│   ├── conftest.py          # Pytest fixtures
│   ├── core/                # Tests for cement/core modules
│   │   ├── test_foundation.py
│   │   ├── test_handler.py
│   │   ├── test_interface.py
│   │   ├── test_hook.py
│   │   ├── test_arg.py
│   │   ├── test_config.py
│   │   ├── test_output.py
│   │   ├── test_log.py
│   │   ├── test_controller.py
│   │   ├── test_extension.py
│   │   └── test_plugin.py
│   ├── ext/                 # Tests for cement/ext extensions
│   │   ├── test_ext_argparse.py
│   │   ├── test_ext_configparser.py
│   │   ├── test_ext_json.py
│   │   ├── test_ext_yaml.py
│   │   └── ... (one test per extension)
│   ├── cli/                 # Tests for cement/cli
│   ├── utils/               # Tests for cement/utils
│   ├── data/                # Test fixtures and data
│   │   ├── config/          # Sample config files
│   │   └── templates/       # Sample templates
│   └── conftest.py          # Shared test configuration
│
├── docs/                    # Sphinx documentation
├── .planning/codebase/      # This directory (codebase maps)
├── pyproject.toml           # Package config, dependencies, entry points
├── Makefile                 # Development commands (test, comply, docs, build)
└── CLAUDE.md                # Project instructions for Claude
```

## Directory Purposes

**cement/core/:**
- Purpose: Core framework abstractions and the central `App` orchestrator
- Contains: Interface definitions, handler base classes, managers (interface, handler, hook), lifecycle control
- Key files: `foundation.py` (the `App` class is here)
- Imports: Uses only Python stdlib (intentionally zero external dependencies for core)

**cement/ext/:**
- Purpose: Optional handler implementations and extensions
- Contains: Concrete handler classes (output, config, logging, etc.), extension loading mechanics
- Pattern: Each file named `ext_<name>.py` implements handler(s) for a specific interface and provides `load(app)` function
- Dependencies: Vary by extension (e.g., `ext_yaml.py` requires `pyyaml`, `ext_jinja2.py` requires `jinja2`)

**cement/cli/:**
- Purpose: The Cement framework's own CLI application (separate from user applications)
- Contains: `CementApp` (extends `App`), CLI controllers for code generation, help, etc.
- Key files:
  - `main.py`: Entry point, `CementApp` class definition
  - `controllers/base.py`: Base command handler
  - `templates/generate/`: Project templates for `cement generate` command

**cement/utils/:**
- Purpose: Shared utility functions not specific to handlers
- Contains: Logging setup, filesystem paths, shell commands, data scrubbing, version info
- Key functions:
  - `minimal_logger()`: Framework's internal logger
  - `init_defaults()`: Generate default config structure
  - `abspath()`, `HOME_DIR`: Path manipulation
  - `is_true()`: Parse boolean config values

**tests/:**
- Purpose: 100% test coverage required (enforced by CI)
- Structure: Mirrors `cement/` source structure for easy navigation
- Key:
  - `conftest.py`: Pytest fixtures including `TestApp`, isolated test app instances
  - Tests use `TestApp` which extends `App` with `exit_on_close=False`, no config files by default
  - Each test file tests one module (e.g., `test_foundation.py` tests `foundation.py`)

**docs/:**
- Purpose: Sphinx documentation (API docs, user guide, developer guide)
- Generated: Via `make docs`, output in `docs/build/`

## Key File Locations

**Entry Points:**
- `cement/__init__.py`: Main package, exports `App`, `Handler`, `Interface`, `Controller`, exceptions
- `cement/cli/main.py`: Cement CLI application entry point, `main()` function
- `pyproject.toml`: Defines `cement` console script entry point to `cement.cli.main:main`

**Configuration:**
- `cement/core/foundation.py`: `App.Meta` class defines all config options and defaults
- `pyproject.toml`: Package metadata, dependencies, entry points, test config

**Core Logic:**
- `cement/core/foundation.py`: `App` class (1500+ lines) — the orchestrator
- `cement/core/handler.py`: `HandlerManager` — registration and resolution
- `cement/core/interface.py`: `InterfaceManager` — interface registration
- `cement/core/hook.py`: `HookManager` — event system

**Handler Implementations:**
- `cement/ext/ext_argparse.py`: Argument parsing and controller dispatch
- `cement/ext/ext_configparser.py`: ConfigParser-based config handler
- `cement/ext/ext_logging.py`: Python logging module integration
- `cement/ext/ext_json.py`, `ext_yaml.py`: Output formatters
- `cement/ext/ext_jinja2.py`: Template rendering
- `cement/ext/ext_plugin.py`: Plugin loading from filesystem

**Testing:**
- `tests/conftest.py`: Pytest fixtures, `TestApp` class
- `tests/core/test_foundation.py`: App lifecycle and handler setup tests
- `tests/ext/test_ext_argparse.py`: Argument parsing and controller dispatch tests

## Naming Conventions

**Files:**
- Source files: `lowercase_with_underscores.py` (PEP 8)
- Extension files: `ext_<feature>.py` (e.g., `ext_json.py`, `ext_yaml.py`)
- Test files: `test_<module>.py` mirroring source (e.g., `test_foundation.py` for `foundation.py`)

**Directories:**
- Package directories: `lowercase` (e.g., `core/`, `ext/`, `cli/`)
- Directory names match their purpose (e.g., `cli/` for CLI-related code)

**Classes:**
- Handler classes: `<Feature><Interface>Handler` (e.g., `ArgparseArgumentHandler`, `JsonOutputHandler`)
- Interface classes: `<Feature>Interface` (e.g., `ArgumentInterface`, `OutputInterface`)
- Manager classes: `<Thing>Manager` (e.g., `HandlerManager`, `InterfaceManager`, `HookManager`)
- App subclasses: `<App>App` (e.g., `CementApp`, `TestApp`)

**Functions:**
- camelCase for class methods
- snake_case for module-level functions
- Handler setup: `_setup_<interface>_handler()` (e.g., `_setup_config_handler()`)
- Hooks: `pre_<event>`, `post_<event>` (e.g., `pre_setup`, `post_argument_parsing`)

**Methods in Handlers:**
- Private framework methods: `_setup()`, `_validate()`
- Public interface methods: Named per interface (e.g., `render()` for `OutputInterface`)

**Constants:**
- UPPERCASE (e.g., `SIGNALS`, `HOME_DIR`)

## Where to Add New Code

**New Feature (Output Format):**
- Primary code: Create `cement/ext/ext_<format>.py`
- Handler class: Inherit from both `OutputInterface` and `Handler`, set `Meta.label = '<format>'`
- Registration: Implement `load(app)` function to call `app.handler.register(YourHandler)`
- Tests: Create `tests/ext/test_ext_<format>.py`
- Pattern example: See `cement/ext/ext_json.py`

**New Handler Interface:**
- Definition: Create method in `cement/core/<new_interface>.py`
- Interface class: Define `<Feature>Interface` with abstract methods
- Base handler: Define `<Feature>Handler(Interface, Handler)` as base for implementations
- Manager: Integrate into `App._lay_cement()` to define the interface
- Tests: Create `tests/core/test_<new_interface>.py`

**New Controller Command:**
- Location: Create file in `cement/cli/controllers/<command>.py` (or add method to existing controller)
- Class: Extend `Controller` (alias for `ArgparseController`)
- Methods: Use `@ex()` decorator (alias for `@expose()`) to register command methods
- Registration: Add to `CementApp.Meta.handlers` list or via `app.handler.register()`
- Tests: Add test in `tests/cli/test_controllers.py`
- Pattern example: See `cement/cli/controllers/base.py`

**New Utility Function:**
- Location: Add to `cement/utils/<module>.py` (or create new if category-specific)
- Export: Add to `cement/utils/__init__.py` if framework-level
- Tests: Add test function to `tests/utils/test_<module>.py`

**Plugin (Application-Level):**
- Location: Create in application's `<app>/plugins/<plugin_name>.py` or `<app>/plugins/<plugin_name>/__init__.py`
- Implementation: Define a `load(app)` function that registers handlers/hooks
- Activation: List in config under `[<app>]` section `plugins = comma,separated,list` or enable via plugin config file
- Tests: Add to application test suite

**Hooks (Application/Extension):**
- Definition: Call `app.hook.define('my_hook')` during `pre_setup` or before
- Registration: Call `app.hook.register('my_hook', my_function, weight=0)` before hook is run
- Execution: Hook names follow pattern `pre_<event>` or `post_<event>`
- Location: Define in extension's `load(app)` or application's `bootstrap.py`

## Special Directories

**cement/.planning/codebase/:**
- Purpose: Codebase analysis documents (this directory)
- Generated: Via `/gsd-map-codebase` command
- Committed: Yes (helps future Claude instances understand the codebase)
- Contains: ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md, TESTING.md, STACK.md, INTEGRATIONS.md, CONCERNS.md

**tests/data/:**
- Purpose: Test fixtures (config files, templates, data)
- Generated: No (manually created test data)
- Committed: Yes
- Subdirs:
  - `config/`: Sample config files for testing config handlers
  - `templates/`: Sample templates for testing template handlers
  - `templates/generate/`: Project templates for code generation tests

**cement/cli/templates/:**
- Purpose: Code generation templates for `cement generate` command
- Generated: No (shipped with Cement)
- Committed: Yes
- Subdirs:
  - `generate/`: Contains project templates (e.g., `todo-tutorial/`)

**docs/:**
- Purpose: Sphinx documentation source
- Generated: `make docs` builds HTML output in `docs/build/`
- Committed: Source checked in, build output is not

**coverage-report/:**
- Purpose: Test coverage report HTML
- Generated: Yes (via `pytest --cov`)
- Committed: No

---

*Structure analysis: 2026-04-24*
