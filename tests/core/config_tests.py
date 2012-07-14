"""Tests for cement.core.config."""

import os
from tempfile import mkstemp
from cement.core import exc, config, handler, backend
from cement.utils import test

CONFIG = """
[my_section]
my_param = my_value
"""

class BogusConfigHandler(config.CementConfigHandler):
    class Meta:
        label = 'bogus'

class ConfigTestCase(test.CementTestCase):        
    @test.raises(exc.CementInterfaceError)
    def test_invalid_config_handler(self):
        handler.register(BogusConfigHandler)
    
    def test_has_key(self):
        self.app.setup()
        self.ok(self.app.config.has_section(self.app._meta.config_section))
        
    def test_config_override(self):
        defaults = dict()
        defaults['test'] = dict()
        defaults['test']['debug'] = False
        self.app = self.make_app(config_defaults=defaults, argv=['--debug'])
        self.app.setup()
        self.app.run()
        self.eq(self.app.config.get('test', 'debug'), True)

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
        self.eq(self.app.config.get('my_section', 'my_param'), 'my_value')
