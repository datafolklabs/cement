# Architecture

**Analysis Date:** 2026-04-24

## Pattern Overview

**Overall:** Handler/Interface/Extension Plugin Architecture

Cement is built around a pluggable handler system where abstract interfaces define contracts and concrete handler implementations provide functionality. The framework orchestrates initialization, runtime dispatch, and signal handling through a central `App` class that manages handlers, hooks, and extensions.

**Key Characteristics:**
- **Interface-driven design:** Core interfaces (`ArgumentInterface`, `ConfigInterface`, `LogInterface`, `OutputInterface`, etc.) define abstract contracts that handlers must implement
- **Handler registry system:** A `HandlerManager` registers, retrieves, and resolves handlers by interface and label (e.g., `app.handler.get('output', 'json')`)
- **Meta class pattern:** Configuration via nested `Meta` classes that are merged through MRO (method resolution order); allows inheritance-based configuration
- **Lifecycle hooks:** Extensible hook system (`pre_setup`, `post_setup`, `pre_run`, `post_run`, `pre_close`, `post_close`, `signal`, `pre_render`, `post_render`) for plugins to inject behavior
- **Extension/Plugin loading:** Dynamic module loading for optional functionality and application-level extensions

## Layers

**Application Layer:**
- Purpose: Main entry point and orchestrator for the framework
- Location: `cement/core/foundation.py` (the `App` class)
- Contains: Application lifecycle methods (`setup()`, `run()`, `close()`), handler setup methods, argument parsing, configuration management, signal handling
- Depends on: All handler interfaces, `HookManager`, `InterfaceManager`, `HandlerManager`
- Used by: CLI applications (e.g., `CementApp` in `cement/cli/main.py`)

**Handler System Layer:**
- Purpose: Manages registration, resolution, and instantiation of handlers
- Location: `cement/core/handler.py` (`Handler` base class, `HandlerManager`)
- Contains: Base handler class, manager for registering/resolving handlers by interface and label
- Depends on: Interface definitions
- Used by: Application during setup, extensions during registration

**Interface Definition Layer:**
- Purpose: Defines abstract contracts for pluggable components
- Location: `cement/core/` (individual interface files: `arg.py`, `config.py`, `output.py`, `log.py`, `controller.py`, `extension.py`, `plugin.py`, `template.py`, `cache.py`, `mail.py`)
- Contains: Interface abstract base classes (e.g., `ArgumentInterface`, `ConfigInterface`) with abstract methods
- Depends on: Abstract base classes (`ABC`)
- Used by: Handler implementations

**Core Handler Implementations:**
- Purpose: Default implementations of core interfaces
- Location: `cement/core/` (same files as interfaces, e.g., `ArgumentHandler` in `arg.py`) and `cement/ext/` (optional extensions like `ext_argparse.py`, `ext_configparser.py`, `ext_logging.py`)
- Contains: Concrete handler classes inheriting from both interface and `Handler`
- Examples:
  - `cement/ext/ext_argparse.py`: `ArgparseArgumentHandler`, `ArgparseController` (command dispatch)
  - `cement/ext/ext_configparser.py`: Configuration parsing handler
  - `cement/ext/ext_logging.py`: Logging handler
  - `cement/ext/ext_json.py`: JSON output handler
  - `cement/ext/ext_dummy.py`: No-op handlers (fallback)
- Depends on: Interface definitions, `Handler` base class

**Extension System:**
- Purpose: Manages dynamic loading of extensions (handlers and hooks)
- Location: `cement/core/extension.py` (`ExtensionInterface`, `ExtensionHandler`) and `cement/ext/ext_plugin.py`
- Contains: Extension loading mechanism; `load_extension()` imports modules and calls their `load()` function if present
- Pattern: Each extension module (e.g., `cement/ext/ext_json.py`) has a `load(app)` function that registers handlers and hooks
- Depends on: Handler system, hook system
- Used by: Application during setup

**Plugin System:**
- Purpose: Application-level plugins loaded from configuration and plugin directories
- Location: `cement/core/plugin.py` (`PluginInterface`, `PluginHandler`)
- Contains: Plugin discovery and loading from filesystem and config
- Pattern: Plugins are Python modules in designated directories that implement a `load(app)` function
- Depends on: Configuration, filesystem navigation
- Used by: Application during setup

**Hook System:**
- Purpose: Event-driven extension mechanism for framework and application lifecycle
- Location: `cement/core/hook.py` (`HookManager`)
- Contains: Hook definition, registration, and execution with weight-based ordering
- Pattern: Named hooks (e.g., `pre_setup`, `post_setup`) are defined during `_lay_cement()`, then functions register to them with optional weight (lower weight = higher priority)
- Depends on: Function references
- Used by: Application throughout lifecycle, extensions for behavior injection

**Controller/Dispatch Layer:**
- Purpose: Maps command-line arguments to handler functions
- Location: `cement/ext/ext_argparse.py` (`ArgparseController`)
- Contains: Argument parsing via `argparse`, nested controller support, method dispatch based on parsed args
- Pattern: Controllers inherit from `Controller` (alias for `ArgparseController`), use `@expose()` decorator on methods to register them as commands
- Depends on: Argument handler interface
- Used by: Application's `run()` method

**Configuration/State Management:**
- Purpose: Multi-level configuration from files, directories, and environment
- Location: `cement/core/config.py` (interface) and `cement/ext/ext_configparser.py` (ConfigParser impl)
- Contains: Config file parsing, section-based storage, config defaults from handlers
- Precedence: System config → User config → Application config → Command-line overrides
- Depends on: Filesystem, environment
- Used by: Application setup, handler initialization

## Data Flow

**Initialization Flow (setup() → run() → close()):**

1. **Application Creation** (`App.__init__()`):
   - Validates application label
   - Sets argv (or uses `sys.argv[1:]`)
   - Initializes framework structures via `_lay_cement()`
   - Detects debug/quiet flags in argv

2. **_lay_cement()** (Framework Foundation):
   - Creates `InterfaceManager`, `HandlerManager`, `HookManager`
   - Defines framework hooks: `pre_setup`, `post_setup`, `pre_run`, `post_run`, `pre_close`, `post_close`, `signal`, `pre_render`, `post_render`
   - Registers core hook functions (handler override logic)
   - Defines core interfaces from `App.Meta.core_interfaces`
   - Registers extension handler (only built-in handler, can't be loaded as extension)
   - Registers handlers from `App.Meta.handlers`

3. **setup()** (Handler Initialization):
   - Runs `pre_setup` hook
   - Calls `_setup_X_handler()` for each interface in order:
     - `_setup_extension_handler()`: Loads `core_extensions` then `App.Meta.extensions`
     - `_setup_config_handler()`: Parses config files and directories
     - `_setup_mail_handler()`, `_setup_log_handler()`: Resolve and setup
     - `_setup_plugin_handler()`: Discovers and loads plugins
     - `_setup_arg_handler()`, `_setup_output_handler()`, `_setup_template_handler()`: Setup remaining handlers
     - `_setup_controllers()`: Register controller handlers
   - Reruns `__retry_hooks__` (hooks registered in Meta but defined after setup)
   - Runs `post_setup` hook (includes `add_handler_override_options`)

4. **Extension Load Pattern** (during `_setup_extension_handler()`):
   ```
   for each extension module (string like 'cement.ext.ext_json'):
     - Call ExtensionHandler.load_extension(ext_module)
     - Import the module if not already loaded
     - If module has load(app) function, call it
     - load(app) registers handlers and hooks via:
       - app.handler.register(SomeHandler)
       - app.hook.register('hook_name', some_function)
   ```

5. **run()** (Execution):
   - Runs `pre_run` hook
   - Calls `self.controller._dispatch()` if a controller is set
   - Controller parses arguments and dispatches to appropriate method
   - Runs `post_run` hook
   - Returns result of controller method

6. **Controller Dispatch** (ArgparseController._dispatch()):
   - Parses `self.app.argv` via argparse
   - Sets `self.app.pargs` to parsed arguments object
   - Runs `post_argument_parsing` hook (includes handler override)
   - Looks up method name from parsed args (or calls `_default()`)
   - Dispatches to the method via reflection
   - Returns method result

7. **close()** (Cleanup):
   - Runs `pre_close` hook
   - Restores stdout/stderr if in quiet mode
   - Runs `post_close` hook
   - Calls `_unlay_cement()` to reset framework
   - Optionally calls `sys.exit()` if `exit_on_close=True`

**State Management:**
- **Application Meta:** Configuration stored in `app._meta` (merged from `App.Meta` class hierarchy and keyword args)
- **Parsed Arguments:** `app.pargs` (set during argument parsing, accessible to controllers)
- **Last Rendered Output:** `app._last_rendered` tuple of `(data, output_text)`
- **Handler State:** Handlers store state in instance attributes (e.g., `config.data`, `log.logger`)
- **Loaded Extensions/Plugins:** Tracked in `app.ext._loaded_extensions`, `app.plugin.get_enabled_plugins()`

## Key Abstractions

**Interface/Handler Contract:**
- **Purpose:** Abstract interface contracts with concrete implementations
- **Examples:**
  - `ArgumentInterface` → `ArgparseArgumentHandler` (CLI argument parsing)
  - `ConfigInterface` → `ConfigParserConfigHandler` (file-based config)
  - `OutputInterface` → `JsonOutputHandler`, `DummyOutputHandler` (output rendering)
  - `ControllerInterface` → `ArgparseController` (command dispatch)
- **Pattern:** Interface defines abstract methods; handler implements them. App resolves handlers by interface label + handler label (e.g., `app.handler.get('output', 'json')`).

**Meta Class Pattern:**
- **Purpose:** Inheritance-based configuration inheritance
- **Example:**
  ```python
  class App(MetaMixin):
      class Meta:
          label = 'myapp'
          debug = False
          config_handler = 'configparser'
  
  class MyApp(App):
      class Meta:
          label = 'customapp'  # overrides
  ```
- **How it works:** `MetaMixin.__init__()` walks MRO, collects all `Meta` classes, merges them (later in MRO overrides earlier), then applies kwargs. Result stored in `self._meta`.

**HandlerManager Resolution:**
- **Purpose:** Resolve handler definitions (string label, uninstantiated class, or instance) to instantiated, setup handler
- **Process:**
  1. Input: `interface` (e.g., 'output'), `handler_def` (e.g., 'json' string or `JsonOutputHandler` class)
  2. Lookup: If string, get registered handler class from `__handlers__[interface][label]`
  3. Instantiate: Create instance, apply `meta_defaults` from `App.Meta.meta_defaults`
  4. Setup: Call `_setup(app)` if `setup=True`, which sets `handler.app = app` and merges config defaults
  5. Return: Instantiated, setup handler ready to use

**Hook System Execution:**
- **Purpose:** Event-driven extension points throughout lifecycle
- **Pattern:** Functions register to named hooks with optional weight; when hook is run, functions execute in weight order (lower weight first)
- **Example:**
  ```python
  app.hook.register('post_setup', my_setup_function, weight=0)
  # Later:
  for result in app.hook.run('post_setup', app):
      pass  # Process each result if needed
  ```
- **Built-in hooks:** `pre_setup`, `post_setup`, `pre_run`, `post_run`, `pre_close`, `post_close`, `signal`, `pre_render`, `post_render`

**Extension Module Pattern:**
- **Purpose:** Register handlers and hooks in a pluggable way
- **Pattern:** Each extension module (e.g., `cement/ext/ext_json.py`) implements:
  - Handler class(es) inheriting from interface + `Handler`
  - Optional hook functions (e.g., `suppress_output_before_run()`)
  - `load(app)` function that registers handlers and hooks
- **Load trigger:** `ExtensionHandler.load_extension(module_name)` imports the module, then calls `module.load(app)` if it exists

## Entry Points

**Cement Framework CLI** (`cement/cli/main.py`):
- Location: `cement/cli/main.py:main()`
- Triggers: Called from `setuptools` entry point (see `pyproject.toml`)
- Responsibilities:
  1. Import optional dependencies (YAML, Jinja2)
  2. Create `CementApp` instance with context manager
  3. Call `app.run()`
  4. Catch `CaughtSignal` and `AssertionError` exceptions
  5. Set exit code and let context manager call `app.close()`

**CementApp Class** (`cement/cli/main.py`):
- Extends: `App` base class
- Meta configuration:
  - `label = 'cement'`
  - `controller = 'base'` (dispatch to `Base` controller)
  - `extensions = ['generate', 'yaml', 'jinja2']` (optional)
  - `handlers = [Base]` (CLI command handler)
  - `config_handler = 'yaml'` (uses YAML config)
  - `template_handler = 'jinja2'` (Jinja2 templates)

**Base Controller** (`cement/cli/controllers/base.py`):
- Extends: `Controller` (alias for `ArgparseController`)
- Meta:
  - `label = 'base'`
  - `description = 'Cement Framework Developer Tools'`
  - `arguments = [version option]`
- Methods:
  - `_default()`: Called if no command specified; prints help
  - Additional commands via `@expose()` decorator (defined by extensions)

**User Application Flow:**
1. Create `App` subclass with custom `Meta`
2. Call `app.setup()` to initialize handlers
3. Call `app.run()` to execute (parses args, dispatches controller)
4. Call `app.close()` (or use context manager `with app as app:`)

## Error Handling

**Strategy:** Exceptions indicate framework or configuration errors; applications catch and handle domain errors.

**Patterns:**
- **Interface/Handler Errors:** `cement.core.exc.InterfaceError` when interface not defined or handler doesn't implement interface
- **Framework Errors:** `cement.core.exc.FrameworkError` for general framework issues (e.g., missing required config, invalid labels)
- **Caught Signals:** `cement.core.exc.CaughtSignal` raised when signal handler catches SIGTERM/SIGINT/SIGHUP
- **Signal Handling:** Signals trigger `cement_signal_handler()` which runs `signal` hook then raises `CaughtSignal`
- **Config Validation:** `validate_config()` can be overridden to check config after loading
- **Handler Fallback:** `handler.get()` and `handler.resolve()` support optional `fallback` parameter for graceful degradation

## Cross-Cutting Concerns

**Logging:** 
- Framework uses `minimal_logger()` for internal logging (see `cement/utils/misc.py`)
- App delegates logging to configured `log_handler` (default: `LoggingLogHandler` from `ext_logging`)
- Debug mode enabled via `--debug` flag or `debug=True` in config

**Validation:**
- Handlers perform `_validate()` in `_setup()` to ensure proper initialization
- Interfaces define validation hook that subclasses can override
- Application calls `validate_config()` after loading configuration

**Authentication/Authorization:**
- Not built into core framework (application responsibility)
- Can be implemented via hooks (e.g., `post_setup` to check credentials)
- Config can store auth-related settings (e.g., API keys in config files)

**Configuration Precedence:**
1. Code defaults in interface/handler `Meta.config_defaults`
2. System-level config files (`/etc/{label}/`)
3. User-level config files (`~/.config/{label}/`, `~/.{label}/`)
4. Application-specific config files
5. Config directories (`.d/` subdirs loaded in order)
6. Command-line argument overrides via Meta options
7. Application config override settings (`App.Meta.meta_override`)

---

*Architecture analysis: 2026-04-24*
