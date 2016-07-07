"""Tests for cement.ext.ext_daemon."""

# NOTE: A large portion of ext_daemon is tested, but not included in
# Coverage report because nose/coverage lose sight of things after the
# sub-process is forked.

import os
#import tempfile
from random import random
from cement.core import handler, backend, log, hook, exc
from cement.utils import shell
from cement.utils import test
from cement.utils.misc import rando
from cement.ext import ext_daemon

APP = rando()[:12]


class DaemonExtTestCase(test.CementExtTestCase):

    def setUp(self):
        super(DaemonExtTestCase, self).setUp()
        self.app = self.make_app()

    def test_switch(self):
        env = ext_daemon.Environment()
        env.switch()

    def test_switch_with_pid(self):
        os.remove(self.tmp_file)
        env = ext_daemon.Environment(pid_file=self.tmp_file)
        env.switch()
        self.ok(os.path.exists(self.tmp_file))

    @test.raises(exc.FrameworkError)
    def test_pid_exists(self):
        env = ext_daemon.Environment(pid_file=self.tmp_file)
        env.switch()

        try:
            self.ok(os.path.exists(self.tmp_file))
        except exc.FrameworkError as e:
            self.ok(e.msg.startswith('Process already running'))
            raise
        finally:
            env = ext_daemon.Environment()
            env.switch()

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
        os.remove(self.tmp_file)
        from cement.utils import shell

        # Test in a sub-process to avoid Nose hangup
        def target():
            app = self.make_app('test', argv=['--daemon'],
                                extensions=['daemon'])

            app.setup()
            app.config.set('daemon', 'pid_file', self.tmp_file)

            try:
                # FIX ME: Can't daemonize, because nose loses sight of it
                app.daemonize()
                app.run()
            finally:
                app.close()
                ext_daemon.cleanup(app)

        p = shell.spawn_process(target)
        p.join()
        self.eq(p.exitcode, 0)

    def test_daemon_not_passed(self):
        app = self.make_app(APP, extensions=['daemon'])

        app.setup()
        app.config.set('daemon', 'pid_file', None)

        try:
            app.run()
        finally:
            ext_daemon.cleanup(app)
