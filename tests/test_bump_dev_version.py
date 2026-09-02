
# Guards scripts/bump_dev_version.py, which release.yml runs on main after a
# publish. Its first version (3.0.16 -> 3.0.17) rewrote backend.py and
# CHANGELOG.md but not tests/core/test_backend.py, so merging the dev-bump PR
# left main red on `assert backend.VERSION[2] == 16`.

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / 'scripts' / 'bump_dev_version.py'

BACKEND_SRC = """\"\"\"Cement core backend module.\"\"\"

VERSION = (3, 0, 16, 'final', 0)  # pragma: nocover  # version constant
"""

CHANGELOG_SRC = """# ChangeLog

## 3.0.16 - July 13, 2026

Bugs:
"""

VERSION_TEST_SRC = """
from cement.core import backend


def test_version():
    # ensure that we bump things properly on version changes
    assert backend.VERSION[0] == 3
    assert backend.VERSION[1] == 0
    assert backend.VERSION[2] == 16
    assert backend.VERSION[3] == 'final'
    assert backend.VERSION[4] == 0
"""


def load_script():
    # Loaded by path: scripts/ is not an importable package.
    spec = importlib.util.spec_from_file_location('bump_dev_version', SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def bump(tmp_path, monkeypatch):
    """The script pointed at a throwaway repo mirroring the real layout."""
    backend = tmp_path / 'cement' / 'core' / 'backend.py'
    changelog = tmp_path / 'CHANGELOG.md'
    version_test = tmp_path / 'tests' / 'core' / 'test_backend.py'

    backend.parent.mkdir(parents=True)
    version_test.parent.mkdir(parents=True)
    backend.write_text(BACKEND_SRC)
    changelog.write_text(CHANGELOG_SRC)
    version_test.write_text(VERSION_TEST_SRC)

    module = load_script()
    monkeypatch.setattr(module, 'BACKEND_PATH', backend)
    monkeypatch.setattr(module, 'CHANGELOG_PATH', changelog)
    monkeypatch.setattr(module, 'VERSION_TEST_PATH', version_test)
    return module, backend, changelog, version_test


def test_bump_rewrites_all_three_files(bump):
    module, backend, changelog, version_test = bump

    assert module.main(['bump_dev_version.py', '3.0.17']) == 0

    assert "VERSION = (3, 0, 17, 'final', 0)" in backend.read_text()
    assert '# pragma: nocover  # version constant' in backend.read_text()
    assert '## 3.0.17 - DEVELOPMENT' in changelog.read_text()

    # The tripwire assertions track the bump; 'final' and the trailing 0 do not.
    text = version_test.read_text()
    assert 'assert backend.VERSION[0] == 3' in text
    assert 'assert backend.VERSION[1] == 0' in text
    assert 'assert backend.VERSION[2] == 17' in text
    assert "assert backend.VERSION[3] == 'final'" in text
    assert 'assert backend.VERSION[4] == 0' in text


def test_bump_across_minor(bump):
    module, backend, _, version_test = bump

    assert module.main(['bump_dev_version.py', '3.2.0']) == 0

    assert "VERSION = (3, 2, 0, 'final', 0)" in backend.read_text()
    text = version_test.read_text()
    assert 'assert backend.VERSION[1] == 2' in text
    assert 'assert backend.VERSION[2] == 0' in text


def test_unshaped_version_test_writes_nothing(bump):
    module, backend, changelog, version_test = bump
    version_test.write_text('def test_version():\n    pass\n')

    assert module.main(['bump_dev_version.py', '3.0.17']) == 3

    # All-or-nothing: the two well-shaped files must be untouched.
    assert BACKEND_SRC == backend.read_text()
    assert CHANGELOG_SRC == changelog.read_text()


def test_missing_version_test_writes_nothing(bump):
    module, backend, changelog, version_test = bump
    version_test.unlink()

    assert module.main(['bump_dev_version.py', '3.0.17']) == 3
    assert BACKEND_SRC == backend.read_text()
    assert CHANGELOG_SRC == changelog.read_text()


def test_bad_version_argument(bump):
    module, _, _, _ = bump
    assert module.main(['bump_dev_version.py', '3.0']) == 2
    assert module.main(['bump_dev_version.py']) == 2


def test_script_is_importable_by_path():
    assert SCRIPT_PATH.is_file()
    assert load_script().main is not None
    sys.modules.pop('bump_dev_version', None)
