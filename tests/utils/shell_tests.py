"""Tests for cement.utils.shell"""

import time
from cement.utils import shell, test

def add(a, b):
    return a + b
    
class ShellUtilsTestCase(test.CementCoreTestCase):
    def test_exec_cmd(self):
        out, err, ret = shell.exec_cmd(['echo', 'KAPLA!'])
        self.eq(ret, 0)
        self.eq(out, b'KAPLA!\n')
        
    def test_exec_cmd_shell_true(self):
        out, err, ret = shell.exec_cmd(['echo KAPLA!'], shell=True)
        self.eq(ret, 0)
        self.eq(out, b'KAPLA!\n')
        
    def test_exec_cmd2(self):
        ret = shell.exec_cmd2(['echo'])
        self.eq(ret, 0)
        
    def test_exec_cmd2_shell_true(self):
        ret = shell.exec_cmd2(['echo johnny'], shell=True)
        self.eq(ret, 0)
    
    def test_exec_cmd_bad_command(self):
        out, err, ret = shell.exec_cmd(['false'])
        self.eq(ret, 1)
    
    def test_exec_cmd2_bad_command(self):
        ret = shell.exec_cmd2(['false'])
        self.eq(ret, 1)
    
    def test_spawn_process(self):
        p = shell.spawn_process(add, args=(23, 2))
        p.join()
        self.eq(p.exitcode, 0)
        
        p = shell.spawn_process(add, join=True, args=(23, 2))
        self.eq(p.exitcode, 0)
        
    def test_spawn_thread(self):
        t = shell.spawn_thread(time.sleep, args=(10))
        
        # before joining it is alive
        res = t.is_alive()
        self.eq(res, True)
        
        t.join()
        
        # after joining it is not alive
        res = t.is_alive()
        self.eq(res, False)
        
        t = shell.spawn_thread(time.sleep, join=True, args=(10))
        res = t.is_alive()
        self.eq(res, False)
