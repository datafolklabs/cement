"""Tests for cement.ext.ext_daemon."""

import os
import tempfile
from random import random
from cement.core import handler, backend, log, hook, exc
from cement.utils import test
from cement.ext import ext_daemon

class DaemonExtTestCase(test.CementExtTestCase):
    def setUp(self):
        self.app = self.make_app()
        
    def test_switch(self):
        env = ext_daemon.Environment()
        env.switch()
    
    def test_switch_with_pid(self):
        (_, tmpfile) = tempfile.mkstemp()
        os.remove(tmpfile)
        env = ext_daemon.Environment(pid_file=tmpfile)
        env.switch()
    
        try:
            self.ok(os.path.exists(tmpfile))
        finally:
            os.remove(tmpfile)

    @test.raises(exc.FrameworkError)
    def test_pid_exists(self):
        (_, tmpfile) = tempfile.mkstemp()

        env = ext_daemon.Environment(pid_file=tmpfile)
        env.switch()
    
        try:
            self.ok(os.path.exists(tmpfile))
        except exc.FrameworkError as e:
            self.ok(e.msg.startswith('Process already running'))
            raise
        finally:
            env = ext_daemon.Environment()
            env.switch()
            os.remove(tmpfile)

    @test.raises(exc.FrameworkError)
    def test_bogus_user(self):
        rand = random()
    
        try:
            env = ext_daemon.Environment(user='cement_test_user%s' % rand)
        except exc.FrameworkError as e:
            self.ok(e.msg.startswith('Daemon user'))
            raise
        finally:
            env = ext_daemon.Environment()
            env.switch()
        
    @test.raises(exc.FrameworkError)
    def test_bogus_group(self):
        rand = random()
    
        try:
            env = ext_daemon.Environment(group='cement_test_group%s' % rand)
        except exc.FrameworkError as e:
            self.ok(e.msg.startswith('Daemon group'))
            raise
        finally:
            env = ext_daemon.Environment()
            env.switch()

    def test_daemon(self):
        (_, tmpfile) = tempfile.mkstemp()
        os.remove(tmpfile)
    
        app = self.make_app('test', argv=['--daemon'], extensions=['daemon'])
    
        app.setup()    
        app.config.set('daemon', 'pid_file', tmpfile)
    
        try:
            ### FIX ME: Can't daemonize, because nose loses sight of it
            #app.daemonize()
            app.run()
        finally:
            app.close()
            ext_daemon.cleanup(app)

    def test_daemon_not_passed(self):
        app = self.make_app('myapp', extensions=['daemon'])
    
        app.setup()    
        app.config.set('daemon', 'pid_file', None)
    
        try:
            app.run()
        finally:
            ext_daemon.cleanup(app)