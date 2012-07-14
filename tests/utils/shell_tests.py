"""Tests for cement.utils.shell"""

from cement.utils import shell, test

class ShellUtilsTestCase(test.CementTestCase):
    def test_exec_cmd(self):
        out, err, ret = shell.exec_cmd(['echo', 'KAPLA!'])
        self.eq(ret, 0)
        self.eq(out, b'KAPLA!\n')
        
    def test_exec_cmd2(self):
        ret = shell.exec_cmd2(['echo'])
        self.eq(ret, 0)
        