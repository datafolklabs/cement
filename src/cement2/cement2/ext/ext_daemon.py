"""
This module provides any dynamically loadable code for the JSON 
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_json.
    
"""

import os
import sys
import pwd
import grp
import signal
from cement2.core import handler, hook, backend
from cement2.lib.ext_daemon import Context

Log = backend.minimal_logger(__name__)
CEMENT_DAEMON_CTX = None
           
def signal_handler(signum, frame):
    global CEMENT_DAEMON_CTX
    
    Log.debug('Caught signal %s, shutting down clean...' % signum)
    if CEMENT_DAEMON_CTX and CEMENT_DAEMON_CTX.pid_file:
        if os.path.exists(CEMENT_DAEMON_CTX.pid_file):
            os.remove(CEMENT_DAEMON_CTX.pid_file)
    
    sys.exit()
    
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
    # pargs aren't available in pre_run... so we just do a little dirty hack
    # here with argv
    if not '--daemon' in app.argv:
        return
    global CEMENT_DAEMON_CTX 
    
    CEMENT_DAEMON_CTX = Context(
        user_name=app.config.get('daemon', 'user'),
        group_name=app.config.get('daemon', 'group'),
        pid_file=app.config.get('daemon', 'pid_file'),
        dir=app.config.get('daemon', 'dir')
        )
    
    # register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    CEMENT_DAEMON_CTX.switch()
    
    if not os.environ.get('CEMENT_TEST'):
        CEMENT_DAEMON_CTX.daemonize()
    
@hook.register()
def cement_post_run_hook(app):
    global CEMENT_DAEMON_CTX
    
    if CEMENT_DAEMON_CTX and CEMENT_DAEMON_CTX.pid_file:
        if os.path.exists(CEMENT_DAEMON_CTX.pid_file):
            os.remove(CEMENT_DAEMON_CTX.pid_file)

