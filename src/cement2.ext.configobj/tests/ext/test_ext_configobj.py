"""Tests for cement2.ext.ext_configobj."""

import sys
import unittest
from tempfile import mkstemp
from nose.tools import eq_, raises
from nose import SkipTest
from cement2.core import handler, backend, log
from cement2 import test_helper as _t

if sys.version_info[0] < 3:
    import configobj
else:
    raise SkipTest('ConfigObj does not support Python 3') # pragma: no cover

app = _t.prep()
from cement2.ext import ext_configobj

def import_configobj():
    from cement2.ext import ext_configobj
    handler.register(ext_configobj.ConfigObjConfigHandler)
    
CONFIG = """
[my_section]
my_param = my_value
"""

class ConfigObjExtTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep('myapp', 
            extensions=['configobj'],
            config_handler='configobj',
            argv=[]
            )
        import_configobj()
        
    def test_configobj(self):
        self.app.setup()    

    def test_has_key(self):
        self.app.setup()
        self.app.config.has_key('bogus_section', 'bogus_key')
            
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