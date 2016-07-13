"""
The Watchdog Framework Extension enables applications Built on Cement
(tm) to easily monitor, and react to, changes in filesystem paths based on the
filesystem events monitoring library
`Watchdog <https://pypi.python.org/pypi/watchdog>`_.

On application startup, the Watchdog Observer is automatically started and
then upon application close, the observer thread is properly stopped and
joined with the parent process before exit.

This is a simplified wrapper around the functionality of the Watchdog library.
For full usage, please see the
`Watchdog API Documentation <http://pythonhosted.org/watchdog/index.html>`_.

Requirements
------------

 * Watchdog (``pip install watchdog``)


Features
--------

 * Cross platform support for Linux, OSX, Windows, etc.


Configuration
-------------

This extension honors the following application meta-data settings:

 * **watchdog_paths** - A List of tuples that are passed directly as arguments
   to ``WatchdogManager.add()`` (shortcut equivalent of
   ``app.watchdog.add(...)``.


Hooks
-----

This extension defines the following hooks:

watchdog_pre_start
^^^^^^^^^^^^^^^^^^

Run first when ``CementApp.watchdog.start()`` is called.  The application
object is passed as an argument.  Nothing is expected in return.

watchdog_post_start
^^^^^^^^^^^^^^^^^^^

Run last when ``CementApp.watchdog.start()`` is called.  The application
object is passed as an argument.  Nothing is expected in return.

watchdog_pre_stop
^^^^^^^^^^^^^^^^^

Run first when ``CementApp.watchdog.stop()`` is called.  The application
object is passed as an argument.  Nothing is expected in return.

watchdog_post_stop
^^^^^^^^^^^^^^^^^^

Run last when ``CementApp.watchdog.stop()`` is called.  The application
object is passed as an argument.  Nothing is expected in return.

watchdog_pre_join
^^^^^^^^^^^^^^^^^

Run first when ``CementApp.watchdog.join()`` is called.  The application
object is passed as an argument.  Nothing is expected in return.

watchdog_post_join
^^^^^^^^^^^^^^^^^^

Run last when ``CementApp.watchdog.join()`` is called.  The application
object is passed as an argument.  Nothing is expected in return.


Usage
-----

The following example uses the default ``WatchdogEventHandler`` that simply
logs all events to ``debug``:

.. code-block:: python

    from time import sleep
    from cement.core.foundation import CementApp
    from cement.core.exc import CaughtSignal
    from cement.ext.ext_watchdog import WatchdogEventHandler


    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['watchdog']
            watchdog_paths = [
                ('./tmp/', WatchdogEventHandler),
            ]


    with MyApp() as app:
        app.run()

        try:
            while True:
                sleep(1)
        except CaughtSignal as e:
            print(e)


In the above example, nothing is printed to console however you will see 
something like the following via debug logging:

.. # noqa
.. code-block:: console

    $ python myapp.py --debug 2>&1 | grep -i watchdog
    cement.core.extension : loading the 'cement.ext.ext_watchdog' framework extension
    cement.core.hook : defining hook 'watchdog_pre_start'
    cement.core.hook : defining hook 'watchdog_post_start'
    cement.core.hook : defining hook 'watchdog_pre_stop'
    cement.core.hook : defining hook 'watchdog_post_stop'
    cement.core.hook : defining hook 'watchdog_pre_join'
    cement.core.hook : defining hook 'watchdog_post_join'
    cement.core.hook : registering hook 'watchdog_extend_app' from cement.ext.ext_watchdog into hooks['post_setup']
    cement.core.hook : registering hook 'watchdog_add_paths' from cement.ext.ext_watchdog into hooks['post_setup']
    cement.core.hook : registering hook 'watchdog_start' from cement.ext.ext_watchdog into hooks['pre_run']
    cement.core.hook : registering hook 'watchdog_cleanup' from cement.ext.ext_watchdog into hooks['pre_close']
    cement.core.hook : running hook 'post_setup' (<function watchdog_extend_app at 0x103c991e0>) from cement.ext.ext_watchdog
    cement.core.foundation : extending appication with '.watchdog' (<cement.ext.ext_watchdog.WatchdogManager object at 0x103f83ef0>)
    cement.core.hook : running hook 'post_setup' (<function watchdog_add_paths at 0x103ddd6a8>) from cement.ext.ext_watchdog
    cement.ext.ext_watchdog : adding path /path/to/tmp with event handler <class 'cement.ext.ext_watchdog.WatchdogEventHandler'>
    cement.core.hook : running hook 'pre_run' (<function watchdog_start at 0x103ddd598>) from cement.ext.ext_watchdog
    cement.ext.ext_watchdog : starting watchdog observer
    myapp : Watchdog Event: <FileDeletedEvent: src_path='/path/to/tmp/test2'>
    myapp : Watchdog Event: <FileDeletedEvent: src_path='/path/to/tmp/test4'>
    myapp : Watchdog Event: <FileDeletedEvent: src_path='/path/to/tmp/test3'>
    myapp : Watchdog Event: <FileDeletedEvent: src_path='/path/to/tmp/dir1/test'>
    myapp : Watchdog Event: <FileDeletedEvent: src_path='/path/to/tmp/test'>
    myapp : Watchdog Event: <DirDeletedEvent: src_path='/path/to/tmp/dir1'>
    myapp : Watchdog Event: <DirModifiedEvent: src_path='/path/to/tmp'>
    myapp : Watchdog Event: <DirModifiedEvent: src_path='/path/to/tmp'>
    myapp : Watchdog Event: <DirCreatedEvent: src_path='/path/to/tmp/dir1'>
    myapp : Watchdog Event: <FileCreatedEvent: src_path='/path/to/tmp/dir1/test.file'>
    myapp : Watchdog Event: <DirModifiedEvent: src_path='/path/to/tmp/dir1'>
    cement.core.hook : running hook 'pre_close' (<function watchdog_cleanup at 0x10e930620>) from cement.ext.ext_watchdog
    cement.ext.ext_watchdog : stopping watchdog observer
    cement.ext.ext_watchdog : joining watchdog observer
    cement.core.foundation : closing the myapp application


To expand on the above example, we can add our own event handlers:

.. code-block:: python

    class MyEventHandler(WatchdogEventHandler):
        def on_any_event(self, event):
            # do something with the ``event`` object
            print("The modified path was: %s" % event.src_path)


    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['watchdog']
            watchdog_paths = [
                ('./tmp/', MyEventHandler),
            ]

.. code-block:: console

    $ python myapp.py
    The modified path was: /path/to/tmp/test.file

Note that the ``WatchdogEventHandler`` could be replaced with any other event
handler classes (i.e. those available from ``watchdog`` directly), however
to play nicely with Cement, we sub-class them first in order to pass in our
application object:

.. code-block:: python

    from watchdog.events import FileSystemEventHandler

    class MyEventHandler(FileSystemEventHandler):
        def __init__(self, app, *args, **kw):
            super(MyEventHandler, self).__init__(*args, **kw)
            self.app = app


For full usage of Watchdog event handlers, refer to the 
`Watchdog API Documentation <http://pythonhosted.org/watchdog/index.html>`_.
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
    ``CementApp.extend()``.

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

        :param path: A directory path to monitor (str)
        :param event_handler: An event handler class used to handle events for
         ``path`` (class)
        :param recursive: Whether to monitor the ``path`` recursively (bool)
        :return: Returns ``True`` if the path is added, ``False`` otherwise.
         (bool)
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
            if isinstance(path_spec, str):
                app.watchdog.add(path_spec)
            elif isinstance(path_spec, tuple):
                app.watchdog.add(*path_spec)
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
