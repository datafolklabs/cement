"""Tests for cement.ext.ext_logging."""

import os
import logging
import shutil
from cement.core import handler, backend, log
from cement.ext import ext_logging
from cement.utils import test
from cement.utils.misc import init_defaults, rando

APP = rando()[:12]


class MyLog(ext_logging.LoggingLogHandler):

    class Meta:
        label = 'mylog'
        level = 'INFO'

    def __init__(self, *args, **kw):
        super(MyLog, self).__init__(*args, **kw)


@test.attr('core')
class LoggingExtTestCase(test.CementExtTestCase):

    def test_alternate_namespaces(self):
        defaults = init_defaults(APP, 'log.logging')
        defaults['log.logging']['to_console'] = False
        defaults['log.logging']['file'] = '/dev/null'
        defaults['log.logging']['level'] = 'debug'
        app = self.make_app(config_defaults=defaults)
        app.setup()
        app.log.info('TEST', extra=dict(namespace=__name__))
        app.log.warning('TEST', extra=dict(namespace=__name__))
        app.log.error('TEST', extra=dict(namespace=__name__))
        app.log.fatal('TEST', extra=dict(namespace=__name__))
        app.log.debug('TEST', extra=dict(namespace=__name__))

        app.log.info('TEST', __name__, extra=dict(foo='bar'))
        app.log.warning('TEST', __name__, extra=dict(foo='bar'))
        app.log.error('TEST', __name__, extra=dict(foo='bar'))
        app.log.fatal('TEST', __name__, extra=dict(foo='bar'))
        app.log.debug('TEST', __name__, extra=dict(foo='bar'))

        app.log.info('TEST', __name__)
        app.log.warning('TEST', __name__)
        app.log.error('TEST', __name__)
        app.log.fatal('TEST', __name__)
        app.log.debug('TEST', __name__)

    def test_deprecated_warn(self):
        defaults = init_defaults(APP, 'log.logging')
        defaults['log.logging']['level'] = 'warn'
        app = self.make_app(config_defaults=defaults)
        app.setup()
        app.log.warn('Warn Message')

    def test_bad_level(self):
        defaults = init_defaults()
        defaults['log.logging'] = dict(
            level='BOGUS',
            to_console=False,
        )
        app = self.make_app(config_defaults=defaults)
        app.setup()
        self.eq(app.log.get_level(), 'INFO')

    def test_clear_loggers(self):
        self.app.setup()

        han = handler.get('log', 'logging')
        Log = han()
        Log.clear_loggers(self.app._meta.label)

        #previous_logger = logging.getLogger(name)
        MyLog = ext_logging.LoggingLogHandler(clear_loggers="%s:%s" %
                                              (self.app._meta.label,
                                               self.app._meta.label))
        MyLog._setup(self.app)

    def test_rotate(self):
        log_file = os.path.join(self.tmp_dir, '%s.log' % APP)
        defaults = init_defaults()
        defaults['log.logging'] = dict(
            file=log_file,
            level='DEBUG',
            rotate=True,
            max_bytes=10,
            max_files=2,
        )
        app = self.make_app(config_defaults=defaults)
        app.setup()
        app.log.info('test log message')
        app.log.info('test log message 2')
        app.log.info('test log message 3')
        app.log.info('test log message 4')

        # check that a second file was created, because this log is over 12
        # bytes.
        self.ok(os.path.exists("%s.1" % log_file))
        self.ok(os.path.exists("%s.2" % log_file))

        # this file should exist because of max files
        self.eq(os.path.exists("%s.3" % log_file), False)

    def test_missing_log_dir(self):
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

        defaults = init_defaults()
        defaults['log.logging'] = dict(
            file=os.path.join(self.tmp_dir, '%s.log' % APP),
        )
        app = self.make_app(config_defaults=defaults)
        app.setup()
