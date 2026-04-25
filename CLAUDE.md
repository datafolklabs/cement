# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
- `pdm venv create && pdm install` - Set up local development environment
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

## GitHub Project

This project is hosted at **github.com/datafolklabs/cement**. Use the `gh` CLI to interact with GitHub issues, pull requests, and other project resources.

- `gh issue list -R datafolklabs/cement` - List open issues
- `gh issue view <number> -R datafolklabs/cement` - View a specific issue
- `gh pr list -R datafolklabs/cement` - List open pull requests
- `gh pr view <number> -R datafolklabs/cement` - View a specific PR
- `gh pr checks <number> -R datafolklabs/cement` - View CI status for a PR
- `gh api repos/datafolklabs/cement/pulls/<number>/comments` - View PR review comments
