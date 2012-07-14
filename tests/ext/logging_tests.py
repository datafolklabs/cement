"""Tests for cement.ext.ext_logging."""
        
import os
import logging
from tempfile import mkstemp
from cement.core import handler, backend, log
from cement.utils import test
from cement.ext import ext_logging

class MyLog(ext_logging.LoggingLogHandler):
    class Meta:
        label = 'mylog'
        level = 'INFO'
    
    def __init__(self, *args, **kw):
        super(MyLog, self).__init__(*args, **kw)
    
class LoggingExtTestCase(test.CementTestCase):
    def test_rotate(self):
        defaults = backend.defaults()
        defaults['base']['debug'] = True
        defaults['log'] = dict(
            file='/dev/null',
            rotate=True,
            to_console=True
            )
        app = self.make_app(config_defaults=defaults)
        app.setup()    
    
    def test_bad_level(self):
        defaults = backend.defaults()
        defaults['log'] = dict(
            level='BOGUS'
            )
        app = self.make_app(config_defaults=defaults)
        app.setup()            
        self.eq(app.log.level(), 'INFO')

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
        app = self.make_app(config_defaults=defaults)
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
        app = self.make_app(config_defaults=defaults)
        app.setup()
