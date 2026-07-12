#!/usr/bin/env python3
"""
testpypi-smoke.py — install cement==X.Y.Z from TestPyPI, import, round-trip.

Installs PLAIN ``cement==<version>`` from the TestPyPI simple index (the
zero-dependency core resolves from TestPyPI alone — this deliberately does NOT
install the ``[cli]`` extra, whose jinja2/pyyaml deps live only on real PyPI),
imports ``App``, runs a minimal ``App().run()`` round-trip, and asserts that
``cement.utils.version.get_version()`` equals the requested version.

Phase 05.4 contract anchors:

* D-07 / REL-02 — TestPyPI install-smoke round-trip. Runs per matrix Python
  (3.10-3.14) after the release publishes to TestPyPI and before the real-PyPI
  publish, proving the artifact installs + imports + runs on a clean env.
* Installs from the TestPyPI simple index ONLY
  (``-i https://test.pypi.org/simple/``). Plain ``cement==X.Y.Z`` (no ``[cli]``
  extra) keeps the install to the zero-dep core and avoids widening the
  dependency-confusion surface (threat T-05.4-01 mitigation).

This file lives under ``scripts/`` and is NOT listed in ``pyproject.toml``
``[tool.pdm.build] includes``, so it ships nowhere and stays outside the
coverage-measured surface (it is only lint/type checked).

Usage:

    python scripts/testpypi-smoke.py 3.0.16

Exit codes:

* 0 — smoke passed (installed, imported, ran, version asserted)
* 2 — bad invocation (wrong argument count)
* non-zero — pip install / import / App round-trip / version-assert failure
"""
from __future__ import annotations  # script-internal; doesn't affect cement/

import subprocess
import sys
import time
from typing import ClassVar

# Per-attempt pip timeout (seconds): fail fast instead of hanging until the
# GitHub Actions job-level timeout on a stalled network / unresponsive index.
INSTALL_TIMEOUT = 300
# TestPyPI index propagation can lag the publish by a short window; retry the
# install a few times before declaring the smoke failed.
INSTALL_ATTEMPTS = 3
RETRY_DELAY = 30


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: testpypi-smoke.py <version>", file=sys.stderr)  # noqa: T201
        return 2
    version = argv[1]

    # (1) Install PLAIN cement from TestPyPI. The zero-dependency core resolves
    # from TestPyPI alone; do NOT install the [cli] extra (its jinja2/pyyaml
    # deps live only on real PyPI and would force an extra real-PyPI index,
    # widening the dependency-confusion surface — Pitfall 2 / T-05.4-01).
    for attempt in range(1, INSTALL_ATTEMPTS + 1):
        try:
            subprocess.run(
                [
                    sys.executable, "-m", "pip", "install",
                    "-i", "https://test.pypi.org/simple/",
                    f"cement=={version}",
                ],
                check=True,
                timeout=INSTALL_TIMEOUT,
            )
            break
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            if attempt == INSTALL_ATTEMPTS:
                raise
            print(  # noqa: T201
                f"install attempt {attempt}/{INSTALL_ATTEMPTS} failed "
                f"(index propagation?); retrying in {RETRY_DELAY}s",
                file=sys.stderr,
            )
            time.sleep(RETRY_DELAY)

    # (2) Import proof + minimal round-trip. Import inside main() so the
    # freshly-installed cement is exactly what we exercise.
    from cement import App
    from cement.utils.version import get_version

    class SmokeApp(App):
        class Meta:
            label = "smoke"
            exit_on_close = False
            # Do NOT inherit this wrapper script's sys.argv — App.run() parses
            # argv[1:] by default, and the version argument passed to THIS
            # script ('3.0.15') would be rejected by the app's argparse
            # ("unrecognized arguments").
            argv: ClassVar[list[str]] = []

    with SmokeApp() as app:
        app.run()

    # (3) Assert the installed version is exactly what we asked to install.
    installed = get_version()
    assert installed == version, (installed, version)

    python_ver = ".".join(str(part) for part in sys.version_info[:3])
    print(f"TestPyPI smoke OK: cement {version} on Python {python_ver}")  # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
