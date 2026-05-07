# Coding Conventions

**Analysis Date:** 2026-04-24

## Naming Patterns

**Files:**
- Module files: lowercase with underscores (`foundation.py`, `ext_smtp.py`)
- Classes: PascalCase (e.g., `FrameworkError`, `SMTPMailHandler`, `MetaMixin`)
- Test files: `test_<module>.py` pattern (e.g., `test_foundation.py`, `test_ext_smtp.py`)

**Functions:**
- Public methods: lowercase_with_underscores (`parse_file()`, `_setup_arg_handler()`)
- Private/internal methods: leading underscore (`_get_params()`, `_parse_file()`)
- Test functions: `test_<feature>()` pattern (e.g., `test_smtp_send()`, `test_basic()`)

**Variables:**
- Constants: UPPERCASE_WITH_UNDERSCORES (environment variables, signal lists)
- Instance variables: lowercase_with_underscores
- Module-level logger: `LOG = minimal_logger(__name__)`

**Types:**
- Use PascalCase for class names
- Use **PEP 585 builtin generics** (Python 3.10+): `dict[str, Any]`, `list[str]`, `tuple[int, str]`, `type[Handler]`
- Use **PEP 604 union syntax** (Python 3.10+): `str | None`, `int | str`, `dict[str, Any] | None`
- Phase 03 D-06 enabled ruff `UP` family enforcement; UP006/UP007/UP045 mechanically rewrite legacy syntax to the modern forms on every `make comply-ruff-fix`
- Private Meta attribute annotations: `_meta: MetaClassName  # type: ignore` (see `cement/ext/ext_smtp.py` line 72)

## Code Style

**Formatting:**
- Tool: `ruff` (v0.3.2+)
- Line length: 100 characters
- Indentation: 4 spaces
- Python target: 3.9+

**Ruff Configuration** (`pyproject.toml` [tool.ruff]):
```
target-version = "py310"
line-length = 100
indent-width = 4
preview = true
extend-select = ["E", "F", "W"]  # PEP8, Pyflakes, warnings
fixable = ["ALL"]
```

**Linting:**
- Tool: `ruff check cement/ tests/`
- All code must pass without errors before commit
- Run via `make comply-ruff`

## Import Organization

**Order** (strictly enforced):
1. Standard library imports (`os`, `sys`, `signal`, `platform`, `importlib`)
2. Third-party library imports (if any)
3. Relative imports from cement (`from ..core`, `from ..utils`)
4. TYPE_CHECKING block (deferred type imports to avoid circular dependencies)

**Example** from `cement/core/foundation.py`:
```python
from __future__ import annotations
import os
import platform
import signal
import sys
from importlib import reload as reload_module
from time import sleep
from typing import (IO, Any, Callable, Dict, List, Optional, TextIO, Tuple,
                    Type, Union, TYPE_CHECKING)
from ..core import (arg, cache, config, controller, exc, extension, log, mail,
                    meta, output, plugin, template)
from ..core.deprecations import deprecate
from ..utils.misc import is_true, minimal_logger

if TYPE_CHECKING:
    from types import FrameType, ModuleType, TracebackType  # pragma: nocover
```

**Path Aliases:**
- No centralized alias configuration; use relative imports exclusively (`..core.`, `..utils.`)

## Type Annotations

**Strictness:** Full type annotation compliance required
- mypy config in `pyproject.toml` enforces strict mode:
  - `disallow_untyped_calls = true`
  - `disallow_untyped_defs = true`
  - `disallow_incomplete_defs = true`
  - `warn_return_any = true`

**Patterns:**
- Always annotate function parameters and return types: `def send(self, msg: str, **kw: Any) -> dict[str, Any]:`
- Use **PEP 585 builtin generics** (Python 3.10+): `dict[str, Any]`, `list[str]`, `tuple[int, str]`, `type[Handler]`
- Use **PEP 604 union syntax** (Python 3.10+): `str | None`, `int | str`, `dict[str, Any] | None`
- Use `TYPE_CHECKING` block for deferred imports to prevent circular dependencies
- Private Meta attributes require `# type: ignore` due to metaclass pattern (framework constraint)
- Phase 03 D-06 enabled ruff `UP` family enforcement; UP006/UP007/UP045 mechanically rewrite legacy syntax to the modern forms on every `make comply-ruff-fix`. Phase 03 plan 03 landed the bulk migration.

**Example** from `cement/ext/ext_smtp.py` (post Phase 03):
```python
def _get_params(self, **kw: Any) -> dict[str, Any]:
    params = dict()
    # ...
    return params
```

## Error Handling

**Framework Exceptions** (from `cement/core/exc.py`):
- `FrameworkError` - General framework (non-application) errors with message passing
- `InterfaceError` - Interface-related errors
- `CaughtSignal(signum, frame)` - Raised when signal is caught

**Pattern:**
- Raise framework exceptions for framework-level errors
- Custom applications should extend `FrameworkError` for app-specific exceptions
- Always include a message: `raise FrameworkError("descriptive message")`

**Exception Testing** (from `tests/core/test_exc.py`):
```python
with raises(FrameworkError, match=".*framework exception.*"):
    raise FrameworkError("test framework exception message")
```

## Logging

**Framework:** `cement.utils.misc.minimal_logger()`
- Module-level logger created as: `LOG = minimal_logger(__name__)`
- No logging.config setup needed; minimal logger is intentionally simple for framework

**Patterns:**
- Use `LOG.debug()` for framework internals: `LOG.debug(f'hook {hook_spec[0]} not defined')`
- Framework runs silently by default; debug output only when app.debug is True
- No INFO/WARNING/ERROR logging in framework core (by design)

**Example** from `cement/core/foundation.py`:
```python
LOG = minimal_logger(__name__)
# ...
LOG.debug(f"extending application with '.{member_name}' ({member_object})")
```

## Comments

**When to Comment:**
- Framework code is internally documented via docstrings; comments for non-obvious logic
- Use `# FIXME:` for known issues that need attention (e.g., line 125 in `foundation.py`)
- Use `# pragma: nocover` for unreachable code in handlers/interfaces (abstract methods)
- Use `# type: ignore` for framework Meta pattern workarounds (mypy limitation)
- Use `# noqa: E501` to suppress line-too-long warnings for long strings (deprecation messages)

**Example** from `cement/core/deprecations.py`:
```python
DEPRECATIONS = {
    '3.0.8-1': "...",  # noqa: E501
    '3.0.8-2': "...",  # noqa: E501
}
```

## Docstring Style

**Format:** Google-style docstrings (RST-compatible)
- Class docstrings: one-line description + Args/Returns sections
- Method docstrings: one-line + Args/Returns if needed
- Abstract methods: `pass    # pragma: nocover`

**Example** from `cement/core/config.py`:
```python
def parse_file(self, file_path: str) -> bool:
    """
    Parse config file settings from ``file_path``.  Returns True if the
    file existed, and was parsed successfully.  Returns False otherwise.

    Args:
        file_path (str): The path to the config file to parse.

    Returns:
        bool: ``True`` if the file was parsed, ``False`` otherwise.

    """
    pass    # pragma: nocover
```

## Meta Class Pattern

**Cement's Core Pattern** (from `cement/core/meta.py`):
- `MetaMixin` base class provides `self._meta` attribute via MRO merging
- Each class defines nested `Meta` inner class with configuration
- Meta attributes cascade through inheritance: parent Meta → child Meta → kwargs
- Used throughout: `App`, `Handler`, `Interface`, all handler implementations

**Implementation** (from `cement/ext/ext_smtp.py`):
```python
class SMTPMailHandler(mail.MailHandler):
    class Meta(mail.MailHandler.Meta):
        """Handler meta-data."""
        label = 'smtp'
        config_defaults = {...}
    
    _meta: Meta  # type: ignore
```

**Accessing Meta:**
- Read: `self._meta.label`, `self._meta.config_section`
- Frameworks queries: `handler._meta.interface`, `handler._meta.overridable`

## Handler/Interface Contracts

**Pattern:**
- Interface defines abstract methods in `InterfaceHandler` base
- Concrete handlers implement interface and subclass `Handler`
- All handlers must define `Meta.label` and `Meta.interface`

**Example** from `cement/core/config.py`:
```python
class ConfigInterface(Interface):
    # ... abstract methods ...
    @abstractmethod
    def parse_file(self, file_path: str) -> bool:
        pass    # pragma: nocover

class ConfigHandler(ConfigInterface, Handler):
    class Meta(Handler.Meta):
        pass  # pragma: nocover
    
    @abstractmethod
    def _parse_file(self, file_path: str) -> bool:
        """Implementation method for subclasses."""
```

## Function Design

**Size:** 
- Keep functions focused; multi-responsibility functions are common in setup/teardown (40-60 lines acceptable for setup methods)
- Private helper methods should be small (<30 lines)

**Parameters:**
- Prefer `**kwargs` for optional parameters (handler/interface pattern)
- Always type all parameters and return values
- Default values for kwargs handled via `Meta.config_defaults` pattern (not function signatures)

**Return Values:**
- Return types must be explicit (no `-> Any` without reason)
- Boolean returns for success/failure (parse_file returns `bool`)
- Dict/list returns should be typed: `-> dict[str, Any]`, `-> list[str]`

## Module Design

**Exports:**
- Core framework exports via `__all__` lists in main modules (not observed, but interface defines implicit contracts)
- Private functions/classes prefixed with `_`

**Barrel Files:**
- Not used; direct imports from submodules preferred

## PEP 8 Compliance

**Command:** `make comply-ruff` (runs `ruff check cement/ tests/`)
- All code must pass before commit
- Ruff auto-fix available: `make comply-ruff-fix`
- Violations will block CI (see `.github/workflows/build_and_test.yml`)

---

*Convention analysis: 2026-04-24*
