# Testing Patterns

**Analysis Date:** 2026-04-24

## Test Framework

**Runner:**
- pytest v4.3.1+ (via `pdm run pytest`)
- Config: `pyproject.toml` [tool.pytest.ini_options]

**Assertion Library:**
- pytest's built-in assertions (e.g., `assert x == y`)
- pytest context managers: `with raises(ExceptionType, match="pattern"):`

**Run Commands:**
```bash
make test              # Run all tests (runs comply first, then tests with coverage)
make test-core         # Run only cement.core tests (skips extensions)
make comply            # Run ruff + mypy (prerequisite before test)
pdm run pytest --cov=cement tests/
pdm run pytest --cov=cement.core tests/core
```

**Coverage Requirements:**
- 100% coverage enforced (no exceptions)
- Command: `pdm run pytest --cov=cement tests/`
- Reports generated: HTML in `coverage-report/` directory
- Config: `pyproject.toml` [tool.coverage.report] with precision=2

## Test File Organization

**Location:**
- Tests mirror source structure exactly: `cement/` → `tests/`
- Extension tests: `tests/ext/test_ext_<name>.py`
- Core tests: `tests/core/test_<module>.py`
- Utility tests: `tests/utils/test_<module>.py`
- CLI tests: `tests/cli/test_<module>.py`

**Naming:**
- Test modules: `test_<module>.py` (e.g., `test_foundation.py`, `test_exc.py`)
- Test functions: `test_<feature>()` or `test_<class>_<method>()`
- Test classes: `TestClassName` pattern (e.g., `TestExceptions`, `TestMetaMixin`)

**Structure:**
```
tests/
├── conftest.py                 # Pytest fixtures (scope='function')
├── __init__.py                 # Sets CEMENT_TEST=1 environment var
├── core/
│   ├── __init__.py
│   ├── test_foundation.py      (812 lines - largest)
│   ├── test_exc.py             (20 lines - exception testing)
│   ├── test_deprecations.py    (32 lines - deprecation warning testing)
│   └── ...
├── ext/
│   ├── test_ext_smtp.py        (629 lines - integration tests with real SMTP)
│   ├── test_ext_argparse.py    (599 lines)
│   └── ...
└── utils/
    └── test_*.py
```

## Test Structure

**Suite Organization:**
```python
# Pattern from tests/core/test_exc.py
class TestExceptions(object):
    def test_frameworkerror(self):
        with raises(FrameworkError, match=".*framework exception.*"):
            raise FrameworkError("test framework exception message")
    
    def test_interfaceerror(self):
        # ...
```

**Module-level Tests:**
```python
# Pattern from tests/core/test_arg.py
# module tests
class TestArgumentInterface(object):
    def test_interface(self):
        assert ArgumentInterface.Meta.interface == 'argument'

# app functionality and coverage tests
class TestArgumentHandler(object):
    def test_subclassing(self):
        # ...
```

**Setup/Teardown:**
- Use pytest fixtures (no class-based setup/teardown)
- Fixtures defined in `tests/conftest.py` with `@pytest.fixture(scope="function")`

**Patterns:**
```python
# From tests/conftest.py - fixture example
@pytest.fixture(scope="function")
def tmp(request):
    t = fs.Tmp()
    yield t
    # cleanup
    if os.path.exists(t.dir) and t.cleanup is True:
        shutil.rmtree(t.dir)

# Usage in tests
def test_something(tmp):
    # tmp is available for test
    pass
```

## Mocking

**Framework:** `unittest.mock` (or `mock` package via `from mock import ...`)

**Patterns** (from `tests/core/test_foundation.py`):
```python
from unittest.mock import Mock, MagicMock

# Simple mock
app.args.add_argument = Mock()
assert not app.args.add_argument.called

# Magic mock with return value
mframe = Mock()
mframe.f_globals.values = MagicMock(return_value=[TestApp()])
mframe.f_globals.values.assert_called()
```

**What to Mock:**
- External service calls (SMTP, HTTP, cache backends)
- Filesystem operations in unit tests (use `tmp` fixture for integration tests)
- System operations (signals, sys.argv)

**What NOT to Mock:**
- Core framework functionality (`HandlerManager`, `HookManager`, etc.)
- Application setup/teardown (test real initialization)
- Configuration loading/parsing
- Handler resolution

## Fixtures and Factories

**Test Data** (from `tests/conftest.py`):
```python
@pytest.fixture(scope="function")
def key(request):
    yield _rando()

@pytest.fixture(scope="function")
def rando(request):
    yield _rando()[:12]
```

**Location:** `tests/conftest.py`
- Shared fixtures for all tests
- Per-module conftest.py for module-specific fixtures (not present currently)

**Built-in Test App** (from `cement.utils.test`):
- `TestApp` class extends `App` for testing
- Minimal defaults for quick test execution
- Supports context manager: `with TestApp() as app:`

**App Configuration Patterns** (from `tests/ext/test_ext_smtp.py`):
```python
def _get_defaults(subject=None):
    defaults = init_defaults('mail.smtp')
    defaults['mail.smtp']['host'] = 'mailpit'
    defaults['mail.smtp']['port'] = 1025
    return defaults

class SMTPApp(TestApp):
    class Meta:
        extensions = ['smtp']
        mail_handler = 'smtp'

# Usage
with SMTPApp(config_defaults=defaults) as app:
    app.run()
    app.mail.send(...)
```

## Coverage

**Requirements:** 100% coverage (no exceptions)

**View Coverage:**
```bash
make test              # Generates coverage-report/index.html
open coverage-report/index.html
```

**Configuration** (pyproject.toml):
```
[tool.coverage.report]
precision = 2
```

**Coverage Exclusions:**
- `# pragma: nocover` - Used for abstract methods, handlers in interfaces, TYPE_CHECKING blocks
- Non-testable code (abstract methods, interface definitions)

**Strategy:**
- Framework core (cement/core/) must be 100% covered
- Extensions may have lower coverage for optional dependencies (e.g., missing smtp/jinja2 libs)
- Tests disabled in CI for optional deps: `if 'SMTP_HOST' in os.environ.keys()`

## Test Types

**Unit Tests:**
- Scope: Individual classes/functions in isolation
- Approach: Test Meta classes, exception handling, utility functions
- Example: `tests/core/test_meta.py` - Tests `Meta` and `MetaMixin` classes
- Pattern: Quick, no external dependencies

**Integration Tests:**
- Scope: Full application lifecycle with handler system
- Approach: Create TestApp, setup, run, verify handler interaction
- Example: `tests/core/test_foundation.py` - Tests App class setup/run/close
- Pattern: Uses fixtures, mocks external services but not framework

**E2E/Service Tests:**
- Framework: Real service containers (mailpit for SMTP, redis, memcached)
- Docker: `docker/compose-services-only.yml` provides services
- Example: `tests/ext/test_ext_smtp.py` - Tests against real mailpit server
- Pattern: Tests in CI verify against actual services
- Environment: `SMTP_HOST=mailpit` (localhost if not in docker)

**Test Command Dependencies:**
- `make test` requires: `comply` first, then pytest with coverage
- `make test-core` runs only `cement/core/` tests (faster for core-only changes)
- Full test suite runs in CI against multiple Python versions (3.9-3.14, PyPy3.10)

## Common Patterns

**Async Testing:**
- Cement has no async support; not applicable

**Error/Exception Testing** (from `tests/core/test_exc.py`):
```python
from pytest import raises

with raises(FrameworkError, match=".*framework exception.*"):
    raise FrameworkError("test framework exception message")

# With exception inspection
with raises(CaughtSignal, match=".*Caught signal.*") as e:
    raise CaughtSignal(1, 2)
assert e.value.signum == 1
assert e.value.frame == 2
```

**Deprecation/Warning Testing** (from `tests/core/test_deprecations.py`):
```python
import warnings

with warnings.catch_warnings(record=True) as w:
    app.run()
    assert "3.0.8-1" in str(w[-1].message)
```

**App Context Manager Pattern** (from `tests/ext/test_ext_smtp.py`):
```python
def test_smtp_send(rando):
    defaults = _get_defaults(subject=rando)
    
    with SMTPApp(config_defaults=defaults) as app:
        app.run()
        app.mail.send(f"{rando}",
                      to=[f'to-{rando}@localhost'],
                      from_addr=f'from-{rando}@localhost')
        # Assertions on behavior
        assert len(data['messages']) == 1
```

**Fixture Usage Pattern** (from `tests/ext/test_ext_smtp.py`):
```python
def test_smtp_send(rando):              # rando fixture injected
    # rando is a random 12-char string for unique test data
    defaults = _get_defaults(subject=rando)
    # Use rando to isolate test data
```

**Handler/Class Definition Testing** (from `tests/core/test_arg.py`):
```python
class TestArgumentHandler(object):
    def test_subclassing(self):
        class MyArgumentHandler(ArgumentHandler):
            class Meta:
                label = 'my_argument_handler'
            
            def add_argument(self, *args, **kw):
                pass
            
            def parse(self, *args, **kw):
                pass
        
        h = MyArgumentHandler()
        assert h._meta.interface == 'argument'
        assert h._meta.label == 'my_argument_handler'
```

## Test Environment

**Environment Variables** (from `tests/__init__.py`):
- `CEMENT_TEST=1` - Set globally in `tests/__init__.py` to enable test mode

**CI Environment** (from `.github/workflows/build_and_test.yml`):
```yaml
env:
  SMTP_HOST: localhost
  SMTP_PORT: 1025
  MEMCACHED_HOST: localhost
  REDIS_HOST: localhost
```

**Service Dependencies:**
- Test containers via `hoverkraft-tech/compose-action@v2.0.1`
- Services: mailpit (SMTP), redis, memcached
- Skipped if service unavailable (graceful degradation)

## Coverage Report Output

**Generated Artifacts:**
- HTML report: `coverage-report/index.html` (viewable in browser)
- Terminal output: Summary in `make test` output
- Precision: 2 decimal places (e.g., 99.50%)

**Checking Coverage:**
```bash
# After running tests
open coverage-report/index.html
# Look for uncovered lines (highlighted in red)
```

---

*Testing analysis: 2026-04-24*
