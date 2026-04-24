# External Integrations

**Analysis Date:** 2026-04-24

## APIs & External Services

**SMTP Mail Service:**
- SMTP protocol via smtplib (Python stdlib)
  - Handler: `cement/ext/ext_smtp.py` (SMTPMailHandler)
  - Configuration: Email headers, authentication, TLS support
  - Development/Testing: Mailpit mock SMTP server (runs in docker-compose)
  - Host env var: `SMTP_HOST`
  - Port env var: `SMTP_PORT`

## Data Storage

**Databases:**
- No built-in database integration
- Applications using Cement handle their own database connections

**Caching:**

**Redis:**
- Cache backend via redis-py library
  - Handler: `cement/ext/ext_redis.py` (RedisCacheHandler)
  - Connection: Environment variable `REDIS_HOST`
  - Client package: `redis` (optional dependency, requires `cement[redis]`)
  - Default config: localhost:6379, db 0
  - Development environment: `redis:latest` service in docker-compose.yml

**Memcached:**
- Cache backend via pylibmc library
  - Handler: `cement/ext/ext_memcached.py` (MemcachedCacheHandler)
  - Connection: Environment variable `MEMCACHED_HOST`
  - Client package: `pylibmc` (optional dependency, requires `cement[memcached]`)
  - Default config: localhost
  - Development environment: `memcached:latest` service in docker-compose.yml, libmemcached in devbox.json

**File Storage:**
- Local filesystem only (no cloud storage integration)
- File system utilities in `cement/utils/fs.py`
- File system event watching via watchdog extension (`cement/ext/ext_watchdog.py`)

## Authentication & Identity

**Auth Provider:**
- Custom/Application-level - Cement does not provide built-in authentication
- Extension support for LDAP via extension pattern (not currently implemented as built-in)
- Applications using Cement implement their own authentication strategies

## Monitoring & Observability

**Error Tracking:**
- Not integrated - Applications handle their own error tracking

**Logs:**
- Python stdlib logging module
  - Handler: `cement/ext/ext_logging.py` (LoggingLogHandler)
  - Color support via `cement/ext/ext_colorlog.py` (ColorLogHandler)
  - Configuration through config handlers
  - Minimal logger utility in `cement/utils/misc.py`

## Configuration Management

**Config File Formats:**
- ConfigParser (INI format)
  - Handler: `cement/ext/ext_configparser.py` (ConfigParserConfigHandler)
- YAML
  - Handler: `cement/ext/ext_yaml.py` (YamlConfigHandler, YamlOutputHandler)
  - Requires `pyyaml` dependency

## Template Rendering

**Template Engines:**
- Jinja2
  - Output handler: `cement/ext/ext_jinja2.py` (Jinja2OutputHandler)
  - Template handler: `cement/ext/ext_jinja2.py` (Jinja2TemplateHandler)
  - Package: `jinja2`
  - Used by CLI: `cement/cli/` templates
- Mustache
  - Handler: `cement/ext/ext_mustache.py` (MustacheTemplateHandler)
  - Package: `pystache`

## File System Monitoring

**Watchdog:**
- File system event monitoring
  - Handler: `cement/ext/ext_watchdog.py` (WatchdogManager)
  - Package: `watchdog`
  - Purpose: Monitor filesystem changes and trigger handlers
  - Default event handler logs to debug log

## Output Formatting

**Tabulate:**
- ASCII table formatting for output
  - Handler: `cement/ext/ext_tabulate.py` (TabulateOutputHandler)
  - Package: `tabulate`

**JSON:**
- JSON output format support
  - Handler: `cement/ext/ext_json.py` (JsonOutputHandler)
  - No external dependency (uses stdlib json)

**YAML:**
- YAML output format support
  - Handler: `cement/ext/ext_yaml.py` (YamlOutputHandler)
  - Package: `pyyaml`

## System Integration

**Daemon Mode:**
- Process daemonization support
  - Handler: `cement/ext/ext_daemon.py` (Environment class)
  - No external dependency
  - Supports: PID files, user/group switching, stdin/stdout/stderr redirection
  - Platform: Unix/Linux only

**Signal Handling:**
- Signal handlers for SIGTERM, SIGINT, SIGHUP
  - Core: `cement/core/foundation.py` (App class)
  - Purpose: Graceful shutdown and reload

**Alarm/Timer System:**
- Simple alarm/timer functionality
  - Handler: `cement/ext/ext_alarm.py`
  - No external dependency

## Plugins & Extensions

**Plugin System:**
- Plugin discovery and loading
  - Handler: `cement/ext/ext_plugin.py` (PluginHandler)
  - Supports loading plugins from directories
  - Framework-level handler resolution

**Code Generation:**
- Project scaffolding/generation
  - Handler: `cement/ext/ext_generate.py`
  - Jinja2 template-based code generation
  - CLI integration in `cement/cli/` for `cement generate` command

## CI/CD & Deployment

**Hosting:**
- Docker images for distribution (Alpine Linux based)
  - Primary: `datafolklabs/cement:latest`
  - Development images for Python 3.9-3.14
  - Image file: `Dockerfile`

**CI Pipeline:**
- Not defined in repository (GitHub Actions or similar would be external)

**Local Development Orchestration:**
- Docker Compose (`docker-compose.yml`):
  - Redis service
  - Memcached service
  - Mailpit (SMTP testing)
  - Cement app containers for Python 3.9, 3.10, 3.11, 3.12, 3.13, 3.14
  - Volume mounts for source code development

## Environment Configuration

**Required Environment Vars (Optional - for extensions):**
- `REDIS_HOST` - Redis server hostname
- `MEMCACHED_HOST` - Memcached server hostname
- `SMTP_HOST` - SMTP server hostname
- `SMTP_PORT` - SMTP server port

**Configuration Sources:**
- Environment variables (preferred)
- Config files (INI, YAML)
- Command-line arguments
- Application defaults
- Handler-specific defaults in `config_defaults` dicts

**Secrets Location:**
- Not integrated - Applications using Cement handle secrets separately
- `.env` files are not checked in (standard Python practice)

## Webhooks & Callbacks

**Incoming:**
- Not a web framework - no built-in HTTP server for webhooks
- Applications using Cement implement their own HTTP endpoints

**Outgoing:**
- Not integrated - Applications handle outbound HTTP calls
- Requests library available in dev dependencies for examples/testing

## Handler/Interface Pattern (Core Architecture)

Cement uses a **pluggable handler system** where:
- **Interfaces** define contracts (mail, cache, config, logging, output, template, etc.)
- **Handlers** implement interfaces (SMTP, Redis, ConfigParser, etc.)
- **Extensions** provide optional handlers via `cement/ext/ext_*.py` files
- Handlers can be swapped at runtime via meta-configuration
- See `cement/core/handler.py` and `cement/core/interface.py` for implementation

This allows applications to choose their own external integrations without framework overhead.

---

*Integration audit: 2026-04-24*
