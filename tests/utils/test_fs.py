
import os
import re
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
    assert "%s.bak" % os.path.basename(tmp.file) == os.path.basename(bkfile)

    bkfile = fs.backup(tmp.file)
    assert "%s.bak.0" % os.path.basename(tmp.file) == os.path.basename(bkfile)

    bkfile = fs.backup(tmp.file)
    assert "%s.bak.1" % os.path.basename(tmp.file) == os.path.basename(bkfile)

    bkdir = fs.backup(tmp.dir)
    assert "%s.bak" % os.path.basename(tmp.dir) == os.path.basename(bkdir)

    assert fs.backup('someboguspath') is None


def test_backup_dir_trailing_slash(tmp):
    # https://github.com/datafolklabs/cement/issues/610
    bkdir = fs.backup("%s/" % tmp.dir)
    assert "%s.bak" % os.path.basename(tmp.dir) == os.path.basename(bkdir)


def test_backup_timestamp(tmp):
    bkfile = fs.backup(tmp.file, timestamp=True)
    assert re.match(r'(.*).bak-[\d]+-[\d]+-[\d]+(.*)', bkfile)  # noqa: W605
