
import os
import shutil
from cement.utils import fs


def test_abspath():
    path = fs.abspath('.')
    assert path.startswith('/')

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
