#!/usr/bin/env python3
"""
cli-smoke-native.py — cross-platform cement CLI smoke (no Docker, no build tool).

Drives the ``cement`` CLI on the runner's OWN Python via ``subprocess`` and
asserts a platform-agnostic version banner, so the same smoke passes on the
Linux, macOS, and Windows GitHub-hosted runners. This is the LIGHTER
CLI + generate + install-generated check; the heavy generated-project
comply/test depth (services + POSIX build tooling) stays Linux-Docker-only in
``scripts/cli-smoke-test.sh`` — those targets and backing services are not
available on the macOS/Windows runners. Tier explicitly.

Ported assertions (re-expressed from ``scripts/cli-smoke-test.sh`` grep checks
as string-membership asserts):

* ``cement --version``      → "Cement Framework 3.0.", "Python 3.", and a
  platform banner that matches ANY of Linux/Darwin/Windows/macOS. This is the
  load-bearing fix: the shell script greps a Linux-only banner (line 34), which
  fails on Darwin/Windows (Pitfall 3). ``platform.platform()`` (the banner
  source in ``cement/utils/version.py:get_version_banner``) reports "macOS-..."
  on modern macOS, so that token is accepted too.
* ``cement --help`` / ``-h`` → "Cement Framework Developer Tools", "generate"
* ``cement generate -h``    → project, todo-tutorial, plugin, script, extension
* ``cement generate project -D <tmp>/myapp`` → install the generated project →
  ``myapp --version`` → same OS-agnostic banner

Phase 05.4 contract anchors:

* D-14 — cross-platform native CLI smoke for the macOS/Windows release gates.
  Shells out to ``cement``/``pip`` on the runner's own interpreter ONLY; it
  never invokes a GNU build-tool target (Pitfall 5) and never touches Docker
  (Pitfall 3).

This file lives under ``scripts/`` and is NOT in ``pyproject.toml``
``[tool.pdm.build] includes``, so it ships nowhere and stays outside the
coverage-measured surface (lint/type checked only).

Usage:

    python scripts/cli-smoke-native.py

Exit codes:

* 0 — smoke passed (CLI + generate + install-generated all asserted)
* non-zero — a subprocess exited non-zero or an assertion failed
"""
from __future__ import annotations  # script-internal; doesn't affect cement/

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# platform.platform() (the banner source) reports the running OS. Accept every
# host the release matrix runs on; "macOS" covers modern Darwin runners whose
# platform string is "macOS-...". Note: NO Linux-only banner hard-require here —
# that single-OS assertion is exactly the Pitfall-3 bug this script fixes.
ACCEPTED_PLATFORMS = ("Linux", "Darwin", "Windows", "macOS")


def _resolve(name: str) -> str:
    """Resolve an executable on PATH (finds console scripts, .exe on Windows)."""
    path = shutil.which(name)
    if path is None:
        raise RuntimeError(f"executable {name!r} not found on PATH")
    return path


def _run(cmd: list[str], cwd: str | None = None) -> str:
    """Run a command, fail loud on non-zero, return combined stdout+stderr.

    timeout: fail fast if a subprocess hangs (e.g. waiting on stdin) instead
    of blocking until the CI job-level timeout.
    """
    proc = subprocess.run(
        cmd, check=True, capture_output=True, text=True, cwd=cwd, timeout=300
    )
    return proc.stdout + proc.stderr


def _assert_version_banner(output: str, prog: str) -> None:
    assert "Cement Framework 3.0." in output, (prog, output)
    assert "Python 3." in output, (prog, output)
    assert "Platform " in output, (prog, output)
    assert any(token in output for token in ACCEPTED_PLATFORMS), (prog, output)


def main() -> int:
    cement = _resolve("cement")

    # cement --version — the OS-agnostic banner assertion (Pitfall-3 fix).
    _assert_version_banner(_run([cement, "--version"]), "cement --version")

    # cement --help / -h — top-level dev-tools help lists the generate command.
    for flag in ("--help", "-h"):
        out = _run([cement, flag])
        assert "Cement Framework Developer Tools" in out, (flag, out)
        assert "generate" in out, (flag, out)

    # cement generate -h — every generator subcommand is present.
    generate_help = _run([cement, "generate", "-h"])
    for sub in ("project", "todo-tutorial", "plugin", "script", "extension"):
        assert sub in generate_help, (sub, generate_help)

    # Generate a project with defaults, install it, and smoke its own CLI.
    with tempfile.TemporaryDirectory() as tmp:
        app_dir = Path(tmp) / "myapp"
        _run([cement, "generate", "project", "-D", str(app_dir)])
        _run([sys.executable, "-m", "pip", "install", "."], cwd=str(app_dir))
        myapp = _resolve("myapp")
        _assert_version_banner(_run([myapp, "--version"]), "myapp --version")

    python_ver = ".".join(str(part) for part in sys.version_info[:3])
    print(f"native CLI smoke OK on Python {python_ver}")  # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main())
