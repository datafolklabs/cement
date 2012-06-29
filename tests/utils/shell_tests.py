"""Tests for cement.utils.shell"""

import unittest
from nose.tools import with_setup, ok_, eq_, raises
from cement.utils import shell

class ShellUtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_exec_cmd(self):
        out, err, ret = shell.exec_cmd(['echo', 'KAPLA!'])
        eq_(ret, 0)
        eq_(out, b'KAPLA!\n')
        
    def test_exec_cmd2(self):
        ret = shell.exec_cmd2(['echo'])
        eq_(ret, 0)
        