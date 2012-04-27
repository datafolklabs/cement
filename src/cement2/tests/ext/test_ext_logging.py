"""Tests for cement2.ext.ext_logging."""
        
import os
import logging
import unittest
from tempfile import mkstemp
from nose.tools import eq_, raises
from cement2.core import handler, backend, log
from cement2 import test_helper as _t
from cement2.lib import ext_logging

class MyLog(ext_logging.LoggingLogHandler):
    class Meta:
        label = 'mylog'
        level = 'INFO'
    
    def __init__(self, *args, **kw):
        super(MyLog, self).__init__(*args, **kw)
    
class LoggingExtTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep()
        
    def test_rotate(self):
        defaults = backend.defaults()
        defaults['base']['debug'] = True
        defaults['log'] = dict(
            file='/dev/null',
            rotate=True,
            to_console=True
            )
        app = _t.prep(config_defaults=defaults)
        app.setup()    
    
    def test_bad_level(self):
        defaults = backend.defaults()
        defaults['log'] = dict(
            level='BOGUS'
            )
        app = _t.prep(config_defaults=defaults)
        app.setup()            
        eq_(app.log.level(), 'INFO')

    def test_clear_loggers(self):
        self.app.setup()
        han = handler.get('log', 'logging')
        Log = han()
        Log.clear_loggers()

    def test_rotate(self):
        defaults = backend.defaults()
        defaults['log'] = dict(
            file=mkstemp()[1],
            rotate=True,
            )
        app = _t.prep(config_defaults=defaults)
        app.setup()    
        
        # FIX ME: Actually check rotation here
        
    def test_missing_log_dir(self):
        _, tmp_path = mkstemp()
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        
        defaults = backend.defaults()
        defaults['log'] = dict(
            file=os.path.join(tmp_path, 'myapp.log'),
            )
        app = _t.prep(config_defaults=defaults)
        app.setup()
