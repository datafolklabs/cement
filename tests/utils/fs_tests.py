"""Tests for cement.utils.fs"""

import os
import shutil
from cement.utils import fs, test


class FsUtilsTestCase(test.CementCoreTestCase):

    def test_abspath(self):
        path = fs.abspath('.')
        self.ok(path.startswith('/'))

    def test_backup(self):
        tmp_file = os.path.join(self.tmp_dir, 'test.file')
        tmp_dir = os.path.join(self.tmp_dir, 'test.dir')
        open(tmp_file, 'w').close()
        os.makedirs(tmp_dir)

        bkfile = fs.backup(tmp_file)
        self.eq("%s.bak" % os.path.basename(tmp_file), 
                                            os.path.basename(bkfile))
        bkfile = fs.backup(tmp_file)
        self.eq("%s.bak.0" %
                os.path.basename(tmp_file), os.path.basename(bkfile))
        bkfile = fs.backup(tmp_file)
        self.eq("%s.bak.1" %
                os.path.basename(tmp_file), os.path.basename(bkfile))

        bkdir = fs.backup(tmp_dir)
        self.eq("%s.bak" % os.path.basename(tmp_dir), 
                                            os.path.basename(bkdir))

        res = fs.backup('someboguspath')
        self.eq(res, None)
