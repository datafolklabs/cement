"""Tests for cement.ext.ext_colorlog."""

import os
import logging
from cement.ext.ext_colorlog import ColorLogHandler, ColoredFormatter
from cement.utils import test
from cement.utils.misc import rando, init_defaults

APP = rando()[:12]


class ColorLogExtTestCase(test.CementExtTestCase):

    def setUp(self):
        super(ColorLogExtTestCase, self).setUp()
        log_file = os.path.join(self.tmp_dir, '%s.log' % APP)
        defaults = init_defaults()
        defaults['log.colorlog'] = dict(
            file=log_file,
            level='DEBUG',
        )
        self.app = self.make_app(APP,
                                 config_defaults=defaults,
                                 extensions=['colorlog'],
                                 log_handler='colorlog',
                                 )

    def test_colorlog(self):
        self.app.setup()
        self.app.run()
        self.app.log.info('this is an info message')
        self.app.close()

    def test_colorize_file_log(self):
        # first test with colorize_file_log=true
        log_file = os.path.join(self.tmp_dir, '%s.log' % APP)
        defaults = init_defaults()
        defaults['log.colorlog'] = dict(
            file=log_file,
            level='DEBUG',
            colorize_file_log=True,
        )
        app = self.make_app(APP,
                            config_defaults=defaults,
                            extensions=['colorlog'],
                            log_handler='colorlog',
                            )
        with app:
            app.run()
            app.log.info('this is an info message')
            klass = app.log._get_file_formatter(app.log._meta.file_format)
            self.ok(isinstance(klass, ColoredFormatter))

        # then test with colorize_file_log=false
        self.reset_backend()
        defaults['log.colorlog']['colorize_file_log'] = False
        app = self.make_app(APP,
                            config_defaults=defaults,
                            extensions=['colorlog'],
                            log_handler='colorlog',
                            )
        with app:
            app.run()
            app.log.info('this is an info message')
            klass = app.log._get_file_formatter(app.log._meta.file_format)
            self.ok(isinstance(klass, logging.Formatter))

    def test_colorize_console_log(self):
        # first test with colorize_file_log=true
        log_file = os.path.join(self.tmp_dir, '%s.log' % APP)
        defaults = init_defaults()
        defaults['log.colorlog'] = dict(
            file=log_file,
            level='DEBUG',
            colorize_console_log=True,
        )
        app = self.make_app(APP,
                            config_defaults=defaults,
                            extensions=['colorlog'],
                            log_handler='colorlog',
                            )
        with app:
            app.run()
            app.log.info('this is an info message')
            format = app.log._meta.console_format
            klass = app.log._get_console_formatter(format)
            self.ok(isinstance(klass, ColoredFormatter))

        # then test with colorize_file_log=false
        self.reset_backend()
        defaults['log.colorlog']['colorize_console_log'] = False
        app = self.make_app(APP,
                            config_defaults=defaults,
                            extensions=['colorlog'],
                            log_handler='colorlog',
                            )
        with app:
            app.run()
            app.log.info('this is an info message')
            klass = app.log._get_console_formatter(format)
            self.ok(isinstance(klass, logging.Formatter))
