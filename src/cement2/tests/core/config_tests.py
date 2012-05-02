"""Tests for cement.core.config."""

import os
import unittest
from tempfile import mkstemp
from nose.tools import ok_, eq_, raises
from cement2.core import exc, config, handler, backend
from cement2 import test_helper as _t

CONFIG = """
[my_section]
my_param = my_value
"""

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
        ok_(self.app.config.has_section(self.app._meta.config_section))
        self.app.setup()
        
    def test_config_override(self):
        defaults = dict()
        defaults['test'] = dict()
        defaults['test']['debug'] = False
        self.app = _t.prep(config_defaults=defaults, argv=['--debug'])
        self.app.setup()
        self.app.run()
        eq_(self.app.config.get('test', 'debug'), True)

    def test_parse_file_bad_path(self):
        self.app._meta.config_files = ['./some_bogus_path']
        self.app.setup()
        
    def test_parse_file(self):
        _, tmppath = mkstemp()
        f = open(tmppath, 'w+')
        f.write(CONFIG)
        f.close()
        self.app._meta.config_files = [tmppath]
        self.app.setup()
        eq_(self.app.config.get('my_section', 'my_param'), 'my_value')
