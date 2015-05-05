"""Config Reloader Framework Extension"""

import os
import signal
import pyinotify
from ..core import backend, hook
from ..utils.misc import minimal_logger
from ..utils import shell, fs

LOG = minimal_logger(__name__)
MASK = pyinotify.IN_CLOSE_WRITE
NOTIFIER = None

class ConfigEventHandler(pyinotify.ProcessEvent):
    def __init__(self, app, watched_files, **kw):
        self.app = app
        self.watched_files = watched_files
        super(ConfigEventHandler, self).__init__()

    def process_default(self, event):
        if event.pathname in self.watched_files:
            LOG.debug('Config path modified: mask=%s, path=%s' % \
                              (event.maskname, event.pathname))
            for res in hook.run('pre_reload_config', self.app):
                pass
            self.app.config.parse_file(event.pathname)
            for res in hook.run('post_reload_config', self.app):
                pass


def spawn_watcher(app):
    global NOTIFIER

    # directories to tell inotify to watch
    watched_dirs = []

    # files to actual perform actions on
    watched_files = []

    # watch manager
    wm = pyinotify.WatchManager()

    # watch all config files, and plugin config files
    watched_files = []

    for plugin_dir in app._meta.plugin_config_dirs:
        plugin_dir = fs.abspath(plugin_dir)
        if not os.path.exists(plugin_dir):
            continue

        if plugin_dir not in watched_dirs:
            watched_dirs.append(plugin_dir)

        # just want the first one... looks wierd, but python 2/3 compat
        res = os.walk(plugin_dir)
        for path, dirs, files in os.walk(plugin_dir):
            plugin_config_files = files
            break

        for plugin_config in plugin_config_files:
            full_plugin_path = os.path.join(plugin_dir, plugin_config)
            if full_plugin_path not in watched_files:
                watched_files.append(full_plugin_path)

    for path in app._meta.config_files:
        if os.path.exists(path):
            if path not in watched_files:
                watched_files.append(path)

            this_dir = os.path.dirname(path)
            if this_dir not in watched_dirs:
                watched_dirs.append(this_dir)
            
    for path in watched_dirs:
        wm.add_watch(path, MASK, rec=True)

    # event handler
    eh = ConfigEventHandler(app, watched_files)

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
