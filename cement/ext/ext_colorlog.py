"""Colorlog Framework Extension"""

import os
import sys
import logging
from colorlog import ColoredFormatter
from ..core import handler
from ..ext.ext_logging import LoggingLogHandler


class ColorLogHandler(LoggingLogHandler):

    """
    This class implements the :ref:`ILog <cement.core.log>`
    interface.  It is a sub-class of LoggingLogHandler based on the standard
    logging library, and adds colorized console output using the
    `ColorLog <https://pypi.python.org/pypi/colorlog>`_ library.  Please
    see the developer documentation on
    :ref:`Log Handling <dev_log_handling>`.

    **Note** This extension has an external dependency on ``colorlog``.  You
    must include ``colorlog`` in your applications dependencies as Cement
    explicitly does **not** include external dependencies for optional
    extensions.

    Usage:

    .. code-block:: python

        from cement.core.foundation import CementApp

        class MyApp(CementApp):
            class Meta:
                label = 'myapp'
                extensions = ['colorlog']
                log_handler = 'colorlog'

        with MyApp() as app:
            app.run()
            app.log.debug('This is my debug message')
            app.log.info('This is my info message')
            app.log.warn('This is my warning message')
            app.log.error('This is my error message')
            app.log.critical('This is my critical message')


    The colors can be customized by overriding the
    ``ColorLogHandler.Meta.colors`` meta-data:

    .. code-block:: python

        from cement.core.foundation import CementApp
        from cement.ext.ext_colorlog import ColorLogHandler

        class MyCustomLog(ColorLogHandler):
            class Meta:
                label = 'my_custom_log'
                colors = {
                    'DEBUG':    'white',
                    'INFO':     'green',
                    'WARNING':  'yellow',
                    'ERROR':    'red',
                    'CRITICAL': 'red',
                    }

        class MyApp(CementApp):
            class Meta:
                label = 'myapp'
                log_handler = MyCustomLog



    Configuration:

    This handler honors all of the same configuration settings as the
    ``LoggingLogHandler`` including:

        * level
        * file
        * to_console
        * rotate
        * max_bytes
        * max_files


    A sample config section (in any config file) might look like:

    .. code-block:: text

        [log.colorlog]
        file = /path/to/config/file
        level = info
        to_console = true
        rotate = true
        max_bytes = 512000
        max_files = 4


    """
    class Meta:
        label = "colorlog"

        #: Color mapping for each log level
        colors = {
            'DEBUG':    'white',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red',
        }

    def __init__(self, *args, **kw):
        super(ColorLogHandler, self).__init__(*args, **kw)
        if sys.stdout.isatty() or 'CEMENT_TEST' in os.environ:
            console_format = "%(log_color)s" + self._meta.console_format
            debug_format = "%(log_color)s" + self._meta.debug_format
            self._meta.console_format = console_format
            self._meta.debug_format = debug_format

    def _get_formatter(self, format):
        return ColoredFormatter(format, log_colors=self._meta.colors)


def load(app):
    handler.register(ColorLogHandler)
