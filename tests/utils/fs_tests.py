"""Tests for cement.utils.fs"""

import unittest
from nose.tools import with_setup, ok_, eq_, raises
from cement.utils import fs

class FsUtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_abspath(self):
        path = fs.abspath('.')
        ok_(path.startswith('/'))