"""
Cement watchdog extension module.
"""

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ..core.meta import MetaMixin
from ..core.exc import FrameworkError
from ..utils.misc import minimal_logger
from ..utils import fs

LOG = minimal_logger(__name__)


class WatchdogEventHandler(FileSystemEventHandler):
    """
    Default event handler used by Cement, that logs all events to the
    application's debug log.  Additional ``*args`` and ``**kwargs`` are passed
    to the parent class.

    :param app: The application object

    """

    def __init__(self, app, *args, **kw):
        super(WatchdogEventHandler, self).__init__(*args, **kw)
        self.app = app

    def on_any_event(self, event):
        self.app.log.debug("Watchdog Event: %s" % event)  # pragma: nocover


class WatchdogManager(MetaMixin):
    """
    The manager class that is attached to the application object via
    ``App.extend()``.

    Usage:

    .. code-block:: python

        with MyApp() as app:
            app.watchdog.start()
            app.watchdog.stop()
            app.watchdog.join()

    """
    class Meta:
        #: The observer class to use on the backend
        observer = Observer

        #: The default event handler class to use if none is provided
        default_event_handler = WatchdogEventHandler

    def __init__(self, app, *args, **kw):
        super(WatchdogManager, self).__init__(*args, **kw)
        self.app = app
        self.paths = []
        self.observer = self._meta.observer()

    def add(self, path, event_handler=None, recursive=True):
        """
        Add a directory path and event handler to the observer.

        Args:
            path (str): A directory path to monitor (str)

        Keyword Args:
            event_handler (class): An event handler class used to handle events
                for ``path`` (class)
            recursive (bool): Whether to monitor the ``path`` recursively

        Returns:
            bool: ``True`` if the path is added, ``False`` otherwise.

        """
        path = fs.abspath(path)
        if not os.path.exists(path):
            LOG.debug('watchdog path %s does not exist... ignoring' % path)
            return False

        if event_handler is None:
            event_handler = self._meta.default_event_handler
        LOG.debug('adding path %s with event handler %s' %
                  (path, event_handler))
        self.observer.schedule(event_handler(self.app),
                               path, recursive=recursive)
        return True

    def start(self, *args, **kw):
        """
        Start the observer.  All ``*args`` and ``**kwargs`` are passed down
        to the backend observer.
        """

        for res in self.app.hook.run('watchdog_pre_start', self.app):
            pass
        LOG.debug('starting watchdog observer')
        self.observer.start(*args, **kw)
        for res in self.app.hook.run('watchdog_post_start', self.app):
            pass

    def stop(self, *args, **kw):
        """
        Stop the observer.  All ``*args`` and ``**kwargs`` are passed down
        to the backend observer.
        """

        for res in self.app.hook.run('watchdog_pre_stop', self.app):
            pass
        LOG.debug('stopping watchdog observer')
        self.observer.stop(*args, **kw)
        for res in self.app.hook.run('watchdog_post_stop', self.app):
            pass

    def join(self, *args, **kw):
        """
        Join the observer with the parent process.  All ``*args`` and
        ``**kwargs`` are passed down to the backend observer.
        """

        for res in self.app.hook.run('watchdog_pre_join', self.app):
            pass
        LOG.debug('joining watchdog observer')
        self.observer.join(*args, **kw)
        for res in self.app.hook.run('watchdog_post_join', self.app):
            pass


def watchdog_extend_app(app):
    app.extend('watchdog', WatchdogManager(app))


def watchdog_start(app):
    app.watchdog.start()


def watchdog_cleanup(app):
    if app.watchdog.observer.is_alive():
        app.watchdog.stop()
        app.watchdog.join()


def watchdog_add_paths(app):
    if hasattr(app._meta, 'watchdog_paths'):
        for path_spec in app._meta.watchdog_paths:
            # odd... if a tuple is a single item it ends up as a str?
            # FIXME: coverage gets lots in testing
            if isinstance(path_spec, str):
                app.watchdog.add(path_spec)  # pragma: nocover
            elif isinstance(path_spec, tuple):
                app.watchdog.add(*path_spec)  # pragma: nocover
            else:
                raise FrameworkError(
                    "Watchdog path spec must be a tuple, not '%s' in: %s" %
                    (type(path_spec).__name__, path_spec)
                )


def load(app):
    app.hook.define('watchdog_pre_start')
    app.hook.define('watchdog_post_start')
    app.hook.define('watchdog_pre_stop')
    app.hook.define('watchdog_post_stop')
    app.hook.define('watchdog_pre_join')
    app.hook.define('watchdog_post_join')
    app.hook.register('post_setup', watchdog_extend_app, weight=-1)
    app.hook.register('post_setup', watchdog_add_paths)
    app.hook.register('pre_run', watchdog_start)
    app.hook.register('pre_close', watchdog_cleanup)
