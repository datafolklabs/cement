"""Tests for cement.ext.ext_colorlog."""

import os
from cement.ext.ext_colorlog import ColorLogHandler
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

    def test_colorized_log_files(self):
        log_file = os.path.join(self.tmp_dir, '%s.log' % APP)
        defaults = init_defaults()
        defaults['log.colorlog'] = dict(
            file=log_file,
            level='DEBUG',
        )
        self.app = self.make_app(APP,
                                 config_defaults=defaults,
                                 extensions=['colorlog'],
                                 log_handler=ColorLogHandler(
                                     colorize_log_files=True),
                                 )
        self.app.setup()
        self.app.run()
        self.app.log.info('this is an info message')
