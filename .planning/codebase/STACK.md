# Technology Stack

**Analysis Date:** 2026-04-24

## Languages

**Primary:**
- Python 3.9+ - Entire framework and CLI application

## Runtime

**Environment:**
- Python (3.9, 3.10, 3.11, 3.12, 3.13, 3.14 supported)

**Package Manager:**
- PDM (Python Dependency Manager)
- Lockfile: `pdm.lock` (present)

## Frameworks

**Core:**
- Cement - Self (CLI application framework with handler/interface pattern)

**CLI & Arguments:**
- Argparse - Command-line argument parsing (extension: `cement/ext/ext_argparse.py`)

**Templating:**
- Jinja2 - Template rendering (extension: `cement/ext/ext_jinja2.py`)
- Mustache - Template rendering alternative (extension: `cement/ext/ext_mustache.py`)

**Configuration:**
- ConfigParser - INI file parsing (extension: `cement/ext/ext_configparser.py`)
- YAML - YAML file parsing (extension: `cement/ext/ext_yaml.py`)

**Logging:**
- Python logging stdlib - Core logging framework (extension: `cement/ext/ext_logging.py`)
- ColorLog - Colored console logging (extension: `cement/ext/ext_colorlog.py`)

**Testing:**
- pytest 4.3.1+ - Test runner
- pytest-cov 2.6.1+ - Coverage reporting
- coverage 4.5.3+ - Coverage measurement
- mock 5.1.0+ - Object mocking

**Code Quality:**
- ruff 0.3.2+ - Linting and code formatting
- mypy 1.9.0+ - Static type checking

**Documentation:**
- Sphinx - Documentation builder
- sphinx_rtd_theme - ReadTheDocs theme
- guzzle_sphinx_theme - Alternative theme
- sphinxcontrib-napoleon - Google/NumPy docstring support

**Build/Dev:**
- pdm-backend - Build system backend
- PDM - Dependency and package management

## Key Dependencies

**Critical:**
- None - Cement core has **zero external dependencies**

**Optional (Pluggable Extensions):**
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

**Environment:**
- Development environment via Devbox with pre-installed services (Redis, Memcached, Mailpit)
- Docker Compose setup for multi-version testing (Python 3.9 - 3.14)
- Environment variables for service configuration:
  - `REDIS_HOST` - Redis server hostname
  - `MEMCACHED_HOST` - Memcached server hostname
  - `SMTP_HOST` - SMTP server hostname
  - `SMTP_PORT` - SMTP server port

**Build:**
- `pyproject.toml` - Primary project configuration
- `pdm.lock` - Dependency lock file
- Ruff config in `pyproject.toml` (`[tool.ruff]`):
  - Target Python 3.9+
  - Line length: 100 characters
  - Indent width: 4 spaces
- MyPy config in `pyproject.toml` (`[tool.mypy]`):
  - Strict type checking enabled
  - Type annotation requirements enforced
- Pytest config in `pyproject.toml` (`[tool.pytest.ini_options]`):
  - Test paths: `tests/`
  - Coverage reporting to HTML

## Platform Requirements

**Development:**
- Devbox environment manager with:
  - Python 3.14
  - PDM (latest)
  - libmemcached (latest)
  - Redis (latest)
  - Memcached (latest)
  - Mailpit (SMTP testing)
  - process-compose (latest)
- Docker Compose for multi-version testing
- Makefile-based workflow

**Production:**
- Python 3.9 or higher
- No external runtime dependencies required for core framework
- Optional services (Redis, Memcached, SMTP) if using corresponding extensions
- Alpine Linux compatible (see `Dockerfile` for production image)

---

*Stack analysis: 2026-04-24*
