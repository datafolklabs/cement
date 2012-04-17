"""Tests for cement.core.config."""

import unittest
from nose.tools import ok_, eq_, raises
from cement2.core import exc, config, handler
from cement2 import test_helper as _t

class BogusConfigHandler(config.CementConfigHandler):
    class Meta:
        label = 'bogus'

class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep()

    @raises(exc.CementInterfaceError)
    def test_invalid_config_handler(self):
        handler.register(BogusConfigHandler)
    
    def test_has_key(self):
        self.app.setup()
        ok_(self.app.config.has_key('base', 'debug'))
        eq_(self.app.config.get('base', 'debug'), False)
