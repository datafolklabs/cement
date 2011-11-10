"""
This module provides any dynamically loadable code for the Daemon 
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_daemon.
    
"""

import os
import sys
import pwd
import grp
import signal
from cement2.core import handler, hook, backend
from cement2.lib.ext_daemon import Environment

Log = backend.minimal_logger(__name__)
CEMENT_DAEMON_ENV = None
           
def signal_handler(signum, frame):
    """
    This handler attempts to clean up the pid file (if it is set, and exists)
    when called.  It will then exit with a code of '0' (clean).
    """
    global CEMENT_DAEMON_ENV
    
    Log.debug('Caught signal %s, shutting down clean...' % signum)
    if CEMENT_DAEMON_ENV and CEMENT_DAEMON_ENV.pid_file:
        if os.path.exists(CEMENT_DAEMON_ENV.pid_file):
            os.remove(CEMENT_DAEMON_ENV.pid_file)
    
    sys.exit(0)
    
@hook.register()
def cement_post_setup_hook(app):
    """
    Adds the '--daemon' argument to the argument object.
    
    """
    app.args.add_argument('--daemon', dest='daemon', 
                          action='store_true', help='daemonize the process')

    # Add default config
    user = pwd.getpwnam(os.environ['USER'])
    group = grp.getgrgid(user.pw_gid)
    
    defaults = dict()
    defaults['daemon'] = dict()
    defaults['daemon']['user'] = user.pw_name
    defaults['daemon']['group'] = group.gr_name
    defaults['daemon']['pid_file'] = None
    defaults['daemon']['dir'] = os.curdir
    app.config.merge(defaults, override=False)

@hook.register()
def cement_pre_run_hook(app):
    """
    Before the application runs, this hook switches the running user/group
    to that configured in config['daemon']['user'] and 
    config['daemon']['group'].  The default user is os.environ['USER'] and the
    default group is that user's primary group.  A pid_file and directory
    to run in is also passed to the environment.
    
    It is important to note that with the daemon extension enabled, the 
    environment will switch user/group/set pid/etc regardless of whether
    the --daemon option was passed at command line or not.  However, the 
    process will only 'daemonize' if the option is passed to do so.  This 
    allows the program to run exactly the same in forground or background.
    
    """
    # We want to honor the runtime user/group/etc even if --daemon is not
    # passed... but only daemonize if it is.
    global CEMENT_DAEMON_ENV 
    
    CEMENT_DAEMON_ENV = Environment(
        user_name=app.config.get('daemon', 'user'),
        group_name=app.config.get('daemon', 'group'),
        pid_file=app.config.get('daemon', 'pid_file'),
        dir=app.config.get('daemon', 'dir')
        )
    
    # register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    CEMENT_DAEMON_ENV.switch()
    
    if '--daemon' in app.argv:
        CEMENT_DAEMON_ENV.daemonize()
    
@hook.register()
def cement_post_run_hook(app):
    """
    After application run time, this hook just attempts to clean up the
    pid_file if one was set, and exists.
    
    """
    global CEMENT_DAEMON_ENV
    
    if CEMENT_DAEMON_ENV and CEMENT_DAEMON_ENV.pid_file:
        if os.path.exists(CEMENT_DAEMON_ENV.pid_file):
            os.remove(CEMENT_DAEMON_ENV.pid_file)

