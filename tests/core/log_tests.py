"""Tests for cement.core.log."""

import logging
from cement.core import exc, backend, log
from cement.utils import test
from cement.utils.misc import init_defaults


class BogusHandler1(log.CementLogHandler):

    class Meta:
        interface = log.ILog
        label = 'bogus'


class LogTestCase(test.CementCoreTestCase):

    def setUp(self):
        super(LogTestCase, self).setUp()
        self.app = self.make_app()

    @test.raises(exc.InterfaceError)
    def test_unproviding_handler(self):
        try:
            self.app.handler.register(BogusHandler1)
        except exc.InterfaceError:
            raise

    def test_logging(self):
        defaults = init_defaults()
        defaults['log.logging'] = dict(
            file='/dev/null',
            to_console=True
        )
        app = self.make_app(config_defaults=defaults)
        app.setup()
        app.log.info('Info Message')
        app.log.warning('Warning Message')
        app.log.error('Error Message')
        app.log.fatal('Fatal Message')
        app.log.debug('Debug Message')

    def test_bogus_log_level(self):
        app = self.make_app('test')
        app.setup()
        app.config.set('log.logging', 'file', '/dev/null')
        app.config.set('log.logging', 'to_console', True)

        # setup logging again
        app.log._setup(app)
        app.log.set_level('BOGUS')

    def test_get_level(self):
        self.app.setup()
        self.eq('INFO', self.app.log.get_level())

    def test_console_log(self):
        app = self.make_app('test', debug=True)
        app.setup()

        app.config.set('log.logging', 'file', '/dev/null')
        app.config.set('log.logging', 'to_console', True)

        app.log._setup(app)
        app.log.info('Tested.')
