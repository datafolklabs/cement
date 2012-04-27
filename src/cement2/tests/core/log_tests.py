"""Tests for cement.core.log."""

import unittest
import logging
from nose.tools import eq_, raises
from cement2.core import exc, backend, handler, log
from cement2 import test_helper as _t

class BogusHandler1(log.CementLogHandler):
    class Meta:
        interface = log.ILog
        label = 'bogus'

class LogTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep()
        
    @raises(exc.CementInterfaceError)
    def test_unproviding_handler(self):
        try:
            handler.register(BogusHandler1)
        except exc.CementInterfaceError:
            raise

    def test_logging(self):
        defaults = backend.defaults()
        defaults['log'] = dict(
            file='/dev/null',
            to_console=True
            )
        app = _t.prep(config_defaults=defaults)
        app.setup()
        app.log.info('Info Message')
        app.log.warn('Warn Message')
        app.log.error('Error Message')
        app.log.fatal('Fatal Message')
        app.log.debug('Debug Message')
    
    def test_bogus_log_level(self):
        app = _t.prep('test')
        app.setup()
        app.config.set('log', 'file', '/dev/null')
        app.config.set('log', 'to_console', True)
    
        # setup logging again
        app.log._setup(app)
        app.log.set_level('BOGUS')

    def test_console_log(self):
        app = _t.prep('test', debug=True)
        app.setup()
    
        app.config.set('log', 'file', '/dev/null')
        app.config.set('log', 'to_console', True)
    
        app.log._setup(app)
        app.log.info('Tested.')