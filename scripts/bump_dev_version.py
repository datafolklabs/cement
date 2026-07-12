#!/usr/bin/env python3
"""
bump_dev_version.py — open the next development cycle after a release.

Given the next dev version (e.g. ``3.0.17``) this transform:

1. Rewrites the ``VERSION`` tuple in ``cement/core/backend.py`` to
   ``(major, minor, patch, 'final', 0)``, replacing ONLY the numeric tuple
   members and preserving the exact trailing
   ``# pragma: nocover  # version constant`` comment verbatim (the coverage
   pragma must not be disturbed).
2. Prepends a fresh ``## <next-version> - DEVELOPMENT`` section — seeded with the
   standard CLAUDE.md changelog buckets — directly under the ``# ChangeLog`` H1
   in ``CHANGELOG.md``.

It deliberately does NOT edit ``pyproject.toml``: ``[tool.pdm.version]``
``source = "call"`` reads ``backend.py`` via ``get_version``, so the version
flows automatically from the tuple above.

Phase 05.4 contract anchors:

* D-12 / REL-05 — post-release dev-version bump. The release workflow runs this
  on ``main`` after publish, then opens a PR (``chore: bump to <next>``), so the
  next development cycle starts immediately.
* T-05.4-02 mitigation — the rewrite is a narrow regex over the numeric tuple
  members only, keeps the ``# pragma: nocover`` comment intact, and fails LOUD
  (non-zero) if ``backend.py`` / ``CHANGELOG.md`` are not shaped as expected,
  rather than silently producing a malformed bump.

The ``## <ver>`` anchor written here is the inverse of the D-02 release
preflight, which rejects a releasing version still marked ``- DEVELOPMENT``.

Usage:

    python scripts/bump_dev_version.py 3.0.17

Exit codes:

* 0 — bump applied (VERSION rewritten + changelog section prepended)
* 2 — bad invocation or non-semver argument
* 3 — backend.py / CHANGELOG.md not shaped as expected (nothing written)
"""
from __future__ import annotations  # script-internal; doesn't affect cement/

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_PATH = REPO_ROOT / "cement" / "core" / "backend.py"
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"

# Matches `VERSION = (3, 0, 15, 'final', 0)<trailing>` and captures the leading
# `VERSION = ` (group 1) and everything after the closing paren (group 2, the
# `# pragma: nocover  # version constant` comment) so both survive verbatim.
VERSION_RE = re.compile(
    r"^(VERSION\s*=\s*)"
    r"\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*'[^']*'\s*,\s*\d+\s*\)"
    r"(.*)$",
    re.MULTILINE,
)

# The changelog H1 the fresh section is inserted beneath.
CHANGELOG_HEADER_RE = re.compile(r"\A(# ChangeLog\n\n)")


def _fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)  # noqa: T201
    return 3


def _bump_backend(major: int, minor: int, patch: int) -> int:
    if not BACKEND_PATH.is_file():
        return _fail(f"{BACKEND_PATH} not found")
    text = BACKEND_PATH.read_text(encoding="utf-8")

    def _repl(match: re.Match[str]) -> str:
        return f"{match.group(1)}({major}, {minor}, {patch}, 'final', 0){match.group(2)}"

    new_text, count = VERSION_RE.subn(_repl, text)
    if count != 1:
        return _fail(
            f"{BACKEND_PATH}: expected exactly one VERSION tuple, found {count}"
        )
    BACKEND_PATH.write_text(new_text, encoding="utf-8")
    return 0


def _prepend_changelog(version: str) -> int:
    if not CHANGELOG_PATH.is_file():
        return _fail(f"{CHANGELOG_PATH} not found")
    text = CHANGELOG_PATH.read_text(encoding="utf-8")

    if re.search(rf"^## +{re.escape(version)}( |$)", text, re.MULTILINE):
        return _fail(f"{CHANGELOG_PATH}: a '## {version}' section already exists")

    section = (
        f"## {version} - DEVELOPMENT\n\n"
        "Bugs:\n\n"
        "Features:\n\n"
        "Refactoring:\n\n"
        "Misc:\n\n"
        "Deprecations:\n\n"
    )

    new_text, count = CHANGELOG_HEADER_RE.subn(
        lambda m: m.group(1) + section, text
    )
    if count != 1:
        return _fail(f"{CHANGELOG_PATH}: could not locate '# ChangeLog' header")
    CHANGELOG_PATH.write_text(new_text, encoding="utf-8")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: bump_dev_version.py <next-version>", file=sys.stderr)  # noqa: T201
        return 2
    version = argv[1]
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
    if match is None:
        print(f"error: '{version}' is not a strict X.Y.Z version", file=sys.stderr)  # noqa: T201
        return 2
    major, minor, patch = int(match.group(1)), int(match.group(2)), int(match.group(3))

    rc = _bump_backend(major, minor, patch)
    if rc != 0:
        return rc
    rc = _prepend_changelog(version)
    if rc != 0:
        return rc

    print(f"bumped dev cycle to {version} (backend VERSION + CHANGELOG)")  # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
