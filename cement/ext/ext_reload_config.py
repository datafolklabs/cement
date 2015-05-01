"""Config Reloader Framework Extension"""

import os
import pyinotify
import signal
from ..core import backend, hook
from ..utils.misc import minimal_logger
from ..utils import shell

LOG = minimal_logger(__name__)
MASK = pyinotify.IN_CLOSE_WRITE
NOTIFIER = None

class ConfigEventHandler(pyinotify.ProcessEvent):
    def __init__(self, app, watched_paths, **kw):
        self.app = app
        self.watched_paths = watched_paths
        super(ConfigEventHandler, self).__init__()

    def process_default(self, event):
        if event.pathname in self.watched_paths:
            self.app.log.debug('Config path modified: mask=%s, path=%s' % \
                              (event.maskname, event.pathname))
            self.app.log.info('Reloading configuration...')
            for res in hook.run('pre_reload_config', self.app):
                pass
            self.app._setup_config_handler()
            for res in hook.run('post_reload_config', self.app):
                pass


def spawn_watcher(app):
    global NOTIFIER
    watched_dirs = []
    watched_paths = []

    # watch manager
    wm = pyinotify.WatchManager()
    for path in app._meta.config_files:
        if os.path.exists(path):
            watched_paths.append(path)

            this_dir = os.path.dirname(path)
            if this_dir not in watched_dirs:
                watched_dirs.append(this_dir)
            
            wm.add_watch(this_dir, MASK, rec=True)

    # event handler
    eh = ConfigEventHandler(app, watched_paths)

    # notifier
    NOTIFIER = pyinotify.ThreadedNotifier(wm, eh)
    NOTIFIER.start()
    
def kill_watcher(app):
    if NOTIFIER.isAlive():
        NOTIFIER.stop()

def signal_handler(signum, frame):
    if signum in [signal.SIGTERM, signal.SIGINT]:
        if NOTIFIER.isAlive():
            NOTIFIER.stop()

def load(app):
    hook.define('pre_reload_config')
    hook.define('post_reload_config')
    hook.register('pre_run', spawn_watcher)
    hook.register('pre_close', kill_watcher)
    hook.register('signal', signal_handler)
