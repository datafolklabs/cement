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
3. Rewrites the matching ``backend.VERSION[0..2]`` assertions in
   ``tests/core/test_backend.py``. That test is the "did you bump everything?"
   tripwire every manual bump used to update by hand (see 8f5eaa81, c314892f);
   leaving it behind lands a red ``main`` the moment the dev-bump PR merges.

It deliberately does NOT edit ``pyproject.toml``: ``[tool.pdm.version]``
``source = "call"`` reads ``backend.py`` via ``get_version``, so the version
flows automatically from the tuple above.

Phase 05.4 contract anchors:

* D-12 / REL-05 — post-release dev-version bump. The release workflow runs this
  on ``main`` after publish, then opens a PR (``chore: bump to <next>``), so the
  next development cycle starts immediately.
* T-05.4-02 mitigation — the rewrites are narrow regexes over the numeric
  members only, keep the ``# pragma: nocover`` comment intact, and fail LOUD
  (non-zero) if ``backend.py`` / ``CHANGELOG.md`` / ``test_backend.py`` are not
  shaped as expected, rather than silently producing a malformed bump.

The ``## <ver>`` anchor written here is the inverse of the D-02 release
preflight, which rejects a releasing version still marked ``- DEVELOPMENT``.

Usage:

    python scripts/bump_dev_version.py 3.0.17

Exit codes:

* 0 — bump applied (VERSION rewritten + changelog section prepended)
* 2 — bad invocation or non-semver argument
* 3 — backend.py / CHANGELOG.md / test_backend.py not shaped as expected
  (nothing written)
"""
from __future__ import annotations  # script-internal; doesn't affect cement/

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_PATH = REPO_ROOT / "cement" / "core" / "backend.py"
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"
VERSION_TEST_PATH = REPO_ROOT / "tests" / "core" / "test_backend.py"

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

# Matches `    assert backend.VERSION[2] == 16`, capturing everything up to the
# literal (group 1) and the tuple index (group 2) so only the number is
# rewritten. The `[3] == 'final'` assertion has no numeric literal and so is
# never matched; `[4] == 0` is matched but left alone (always 0).
VERSION_TEST_RE = re.compile(
    r"^(\s*assert\s+backend\.VERSION\[(\d+)\]\s*==\s*)\d+$",
    re.MULTILINE,
)


def _fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)  # noqa: T201


def _render_backend(major: int, minor: int, patch: int) -> str | None:
    """Return the rewritten backend.py text, or None (with error printed)."""
    if not BACKEND_PATH.is_file():
        _fail(f"{BACKEND_PATH} not found")
        return None
    text = BACKEND_PATH.read_text(encoding="utf-8")

    def _repl(match: re.Match[str]) -> str:
        return f"{match.group(1)}({major}, {minor}, {patch}, 'final', 0){match.group(2)}"

    new_text, count = VERSION_RE.subn(_repl, text)
    if count != 1:
        _fail(f"{BACKEND_PATH}: expected exactly one VERSION tuple, found {count}")
        return None
    return new_text


def _render_changelog(version: str) -> str | None:
    """Return the rewritten CHANGELOG.md text, or None (with error printed)."""
    if not CHANGELOG_PATH.is_file():
        _fail(f"{CHANGELOG_PATH} not found")
        return None
    text = CHANGELOG_PATH.read_text(encoding="utf-8")

    if re.search(rf"^## +{re.escape(version)}( |$)", text, re.MULTILINE):
        _fail(f"{CHANGELOG_PATH}: a '## {version}' section already exists")
        return None

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
        _fail(f"{CHANGELOG_PATH}: could not locate '# ChangeLog' header")
        return None
    return new_text


def _render_version_test(major: int, minor: int, patch: int) -> str | None:
    """Return the rewritten test_backend.py text, or None (with error printed)."""
    if not VERSION_TEST_PATH.is_file():
        _fail(f"{VERSION_TEST_PATH} not found")
        return None
    text = VERSION_TEST_PATH.read_text(encoding="utf-8")

    expected = {0: major, 1: minor, 2: patch}
    rewritten: set[int] = set()

    def _repl(match: re.Match[str]) -> str:
        index = int(match.group(2))
        if index not in expected:
            return match.group(0)
        rewritten.add(index)
        return f"{match.group(1)}{expected[index]}"

    new_text = VERSION_TEST_RE.sub(_repl, text)
    missing = sorted(set(expected) - rewritten)
    if missing:
        _fail(
            f"{VERSION_TEST_PATH}: expected backend.VERSION assertions for "
            f"indexes {missing}, found none"
        )
        return None
    return new_text


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

    # Prepare ALL rewrites in memory before writing ANY file, so an exit-3
    # validation failure can never leave the repo half-bumped (the documented
    # "nothing written" contract).
    new_backend = _render_backend(major, minor, patch)
    if new_backend is None:
        return 3
    new_changelog = _render_changelog(version)
    if new_changelog is None:
        return 3
    new_version_test = _render_version_test(major, minor, patch)
    if new_version_test is None:
        return 3

    BACKEND_PATH.write_text(new_backend, encoding="utf-8")
    CHANGELOG_PATH.write_text(new_changelog, encoding="utf-8")
    VERSION_TEST_PATH.write_text(new_version_test, encoding="utf-8")

    print(  # noqa: T201
        f"bumped dev cycle to {version} (backend VERSION + CHANGELOG + version test)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
