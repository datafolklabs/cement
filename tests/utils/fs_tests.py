"""Tests for cement.utils.fs"""

import os
import unittest
import tempfile
from nose.tools import with_setup, ok_, eq_, raises
from cement.utils import fs

class FsUtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_abspath(self):
        path = fs.abspath('.')
        ok_(path.startswith('/'))
    
    def test_backup(self):
        _, tmpfile = tempfile.mkstemp()
        bkfile = fs.backup(tmpfile)
        eq_("%s.bak" % os.path.basename(tmpfile), os.path.basename(bkfile))
        bkfile = fs.backup(tmpfile)
        eq_("%s.bak.0" % os.path.basename(tmpfile), os.path.basename(bkfile))
        bkfile = fs.backup(tmpfile)
        eq_("%s.bak.1" % os.path.basename(tmpfile), os.path.basename(bkfile))
        
        tmpdir = tempfile.mkdtemp()
        bkdir = fs.backup(tmpdir)
        eq_("%s.bak" % os.path.basename(tmpdir), os.path.basename(bkdir))
        
        res = fs.backup('someboguspath')
        eq_(res, None)