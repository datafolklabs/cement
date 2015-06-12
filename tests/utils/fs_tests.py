"""Tests for cement.utils.fs"""

import os
import tempfile
from cement.utils import fs, test


class FsUtilsTestCase(test.CementCoreTestCase):

    def test_abspath(self):
        path = fs.abspath('.')
        self.ok(path.startswith('/'))

    def test_backup(self):
        _, tmpfile = tempfile.mkstemp()
        bkfile = fs.backup(tmpfile)
        self.eq("%s.bak" % os.path.basename(tmpfile), os.path.basename(bkfile))
        bkfile = fs.backup(tmpfile)
        self.eq("%s.bak.0" %
                os.path.basename(tmpfile), os.path.basename(bkfile))
        bkfile = fs.backup(tmpfile)
        self.eq("%s.bak.1" %
                os.path.basename(tmpfile), os.path.basename(bkfile))

        tmpdir = tempfile.mkdtemp()
        bkdir = fs.backup(tmpdir)
        self.eq("%s.bak" % os.path.basename(tmpdir), os.path.basename(bkdir))

        res = fs.backup('someboguspath')
        self.eq(res, None)
