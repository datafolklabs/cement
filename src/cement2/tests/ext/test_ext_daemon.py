"""Tests for cement2.ext.ext_daemon."""

import os
import tempfile
import unittest
from random import random
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest
from cement2.core import handler, backend, log, hook, exc
from cement2 import test_helper as _t

app = _t.prep()
from cement2.ext import ext_daemon

def import_daemon():
    from cement2.ext import ext_daemon
    hook.register()(ext_daemon.cement_post_setup_hook)
    hook.register()(ext_daemon.cement_on_close_hook)

class DaemonExtTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep()
        
    def test_switch(self):
        import_daemon()
        env = ext_daemon.Environment()
        env.switch()
    
    def test_switch_with_pid(self):
        (_, tmpfile) = tempfile.mkstemp()
        os.remove(tmpfile)
        import_daemon()
        env = ext_daemon.Environment(pid_file=tmpfile)
        env.switch()
    
        try:
            ok_(os.path.exists(tmpfile))
        finally:
            os.remove(tmpfile)

    @raises(exc.CementRuntimeError)
    def test_pid_exists(self):
        (_, tmpfile) = tempfile.mkstemp()

        import_daemon()
        env = ext_daemon.Environment(pid_file=tmpfile)
        env.switch()
    
        try:
            ok_(os.path.exists(tmpfile))
        except exc.CementRuntimeError as e:
            ok_(e.msg.startswith('Process already running'))
            raise
        finally:
            env = ext_daemon.Environment()
            env.switch()
            os.remove(tmpfile)

    @raises(exc.CementRuntimeError)
    def test_bogus_user(self):
        rand = random()
        import_daemon()
    
        try:
            env = ext_daemon.Environment(user_name='cement_test_user%s' % rand)
        except exc.CementRuntimeError as e:
            ok_(e.msg.startswith('Daemon user'))
            raise
        finally:
            env = ext_daemon.Environment()
            env.switch()
        
    @raises(exc.CementRuntimeError)
    def test_bogus_group(self):
        rand = random()
        import_daemon()
    
        try:
            env = ext_daemon.Environment(group_name='cement_test_group%s' % rand)
        except exc.CementRuntimeError as e:
            ok_(e.msg.startswith('Daemon group'))
            raise
        finally:
            env = ext_daemon.Environment()
            env.switch()

    def test_daemon(self):
        (_, tmpfile) = tempfile.mkstemp()
        os.remove(tmpfile)
    
        app = _t.prep('myapp')
        import_daemon()
    
        app.argv = ['--daemon']
        app.setup()    
        app.config.set('daemon', 'pid_file', tmpfile)
    
        try:
            ### FIX ME: Can't daemonize, because now loses sight of it
            app.daemonize()
            app.run()
        finally:
            ext_daemon.cement_on_close_hook(app)

    def test_daemon_not_passed(self):
        app = _t.prep('myapp')
        import_daemon()
    
        app.argv = []
        app.setup()    
        app.config.set('daemon', 'pid_file', None)
    
        try:
            app.run()
        finally:
            ext_daemon.cement_on_close_hook(app)
