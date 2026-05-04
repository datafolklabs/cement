
import os
import re
import sys

from pytest import raises

from cement.utils import fs


def test_abspath(tmp):
    path = fs.abspath('.')
    assert path.startswith('/')


def test_join(tmp, rando):
    full_path = os.path.abspath(os.path.join(tmp.dir, rando))
    assert fs.join(tmp.dir, rando) == full_path


def test_join_exists(tmp, rando):
    full_path = os.path.abspath(os.path.join(tmp.dir, rando))

    res = fs.join_exists(tmp.dir, rando)
    assert res[0] == full_path
    assert res[1] is False

    with open(full_path, 'w') as f:
        f.write('data')

    res = fs.join_exists(tmp.dir, rando)
    assert res[1] is True


def test_ensure_dir_exists(tmp, rando):
    fs.ensure_dir_exists(fs.join(tmp.dir, rando))
    assert os.path.exists(fs.join(tmp.dir, rando))

    with raises(AssertionError, match='(.*)exists but is not a directory(.*)'):
        fs.ensure_dir_exists(tmp.file)


def test_ensure_parent_dir_exists(tmp, rando):
    fs.ensure_parent_dir_exists(fs.join(tmp.dir, 'parent', rando))
    assert os.path.exists(fs.join(tmp.dir, 'parent'))


def test_tmp(tmp, rando):
    t1 = fs.Tmp()
    assert os.path.exists(t1.dir)
    assert os.path.exists(t1.file)

    with fs.Tmp() as t2:
        pass

    assert not os.path.exists(t2.dir)
    assert not os.path.exists(t2.file)


def test_backup(tmp):
    bkfile = fs.backup(tmp.file)
    assert f"{os.path.basename(tmp.file)}.bak" == os.path.basename(bkfile)

    bkfile = fs.backup(tmp.file)
    assert f"{os.path.basename(tmp.file)}.bak.0" == os.path.basename(bkfile)

    bkfile = fs.backup(tmp.file)
    assert f"{os.path.basename(tmp.file)}.bak.1" == os.path.basename(bkfile)

    bkdir = fs.backup(tmp.dir)
    assert f"{os.path.basename(tmp.dir)}.bak" == os.path.basename(bkdir)

    assert fs.backup('someboguspath') is None


def test_backup_dir_trailing_slash(tmp):
    # https://github.com/datafolklabs/cement/issues/610
    bkdir = fs.backup(f"{tmp.dir}/")
    assert f"{os.path.basename(tmp.dir)}.bak" == os.path.basename(bkdir)


def test_backup_timestamp(tmp):
    bkfile = fs.backup(tmp.file, timestamp=True)
    assert re.match(r'(.*).bak-[\d]+-[\d]+-[\d]+(.*)', bkfile)  # noqa: W605


def test_abspath_preserves_symlinks(tmp):
    # Phase 03 Wave 9 (CR-01 regression test): fs.abspath() MUST
    # NOT follow symlinks. Pre-Wave-6 used os.path.abspath which
    # preserves symlink paths; Wave 6 briefly used Path.resolve
    # which followed symlinks; Wave 9 restored os.path semantics.
    # Skip on Windows where symlink creation needs admin.
    if sys.platform == 'win32':
        return  # pragma: nocover  # platform-specific

    target_dir = os.path.join(tmp.dir, 'target')
    link_path = os.path.join(tmp.dir, 'link')
    os.makedirs(target_dir)
    os.symlink(target_dir, link_path)

    result = fs.abspath(link_path)

    # The result MUST be the symlink path itself, not the
    # resolved target. This is the BC contract the 3.0.x track
    # requires (CLAUDE.md > Constraints: zero public-API
    # breakage).
    assert result == link_path
    assert 'link' in result
    assert 'target' not in os.path.basename(result)


def test_abspath_unknown_user_does_not_raise(tmp):
    # Phase 03 Wave 9 (CR-02 regression test): fs.abspath() with
    # an unknown ~user prefix MUST silently fall through and
    # return the input as-is (os.path.expanduser semantics),
    # NOT raise RuntimeError (Path.expanduser semantics).
    # Stale ~deleteduser/path entries in user config files
    # otherwise crash App.setup() mid-flight.
    bogus = '~nosuchuser_xyz_phase03_gap/foo'

    # Must not raise
    result = fs.abspath(bogus)

    # Must match os.path semantics verbatim (silent fallthrough
    # then absolute-path normalization)
    assert result == os.path.abspath(bogus)
