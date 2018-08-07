# NOTE: A large portion of ext_daemon is tested, but not included in
# Coverage report because nose/pytest/coverage lose sight of things after the
# sub-process is forked.

import os
from unittest.mock import patch
from pytest import raises
from cement.core.foundation import TestApp
from cement.core.exc import FrameworkError
from cement.ext import ext_daemon


class FakeUser(object):
    def __init__(self):
        self.pw_uid = 'BogusId'
        self.pw_dir = 'BogusDir'


class FakeGroup(object):
    def __init__(self):
        self.gr_gid = 'BogusGroupId'


@patch('os.chdir')
@patch('os.setgid')
@patch('os.setuid')
def test_switch(set_uid, set_gid, chdir):
    assert not set_gid.called
    assert not chdir.called
    env = ext_daemon.Environment()
    env.user = FakeUser()
    env.group = FakeGroup()
    env.switch()
    set_uid.assert_called_once_with('BogusId')
    set_gid.assert_called_once_with('BogusGroupId')
    assert chdir.called


def test_switch_with_pid(tmp):
    os.remove(tmp.file)
    env = ext_daemon.Environment(pid_file=tmp.file)
    env.switch()
    assert os.path.exists(tmp.file)

    # reset
    env = ext_daemon.Environment()
    env.switch()


def test_pid_exists(tmp):
    with raises(FrameworkError, match="Process already running"):
        env = ext_daemon.Environment(pid_file=tmp.file)
        env.switch()

    # reset
    env = ext_daemon.Environment()
    env.switch()


def test_bogus_user(rando):
    with raises(FrameworkError, match='Daemon user'):
        env = ext_daemon.Environment(user='cement_test_user%s' % rando)

    # reset
    env = ext_daemon.Environment()
    env.switch()

# @test.raises(exc.FrameworkError)


def test_bogus_group(rando):
    with raises(FrameworkError, match='Daemon group'):
        env = ext_daemon.Environment(group='cement_test_group%s' % rando)

    # reset
    env = ext_daemon.Environment()
    env.switch()


def test_daemon(tmp):
    os.remove(tmp.file)
    from cement.utils import shell

    # Test in a sub-process to avoid hangup
    def target():
        with TestApp(argv=['--daemon'], extensions=['daemon']) as app:
            app.config.set('daemon', 'pid_file', tmp.file)

            try:
                # FIX ME: Can't daemonize, because nose/pytest lose sight of it
                app.daemonize()
                app.run()
            finally:
                app.close()
                ext_daemon.cleanup(app)

    p = shell.spawn_process(target)
    p.join()
    assert p.exitcode == 0


def test_daemon_not_passed():
    with TestApp(extensions=['daemon']) as app:
        app.config.set('daemon', 'pid_file', None)

        try:
            app.run()
        finally:
            ext_daemon.cleanup(app)
