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
    def test_alternate_namespaces(self):
        defaults = backend.defaults('cement-testapp', 'log')
        defaults['log']['to_console'] = False
        defaults['log']['file'] = '/dev/null'
        defaults['log']['level'] = 'debug'
        app = self.make_app(config_defaults=defaults)
        app.setup()            
        app.log.info('TEST', extra=dict(namespace=__name__))
        app.log.warn('TEST', extra=dict(namespace=__name__))
        app.log.error('TEST', extra=dict(namespace=__name__))
        app.log.fatal('TEST', extra=dict(namespace=__name__))
        app.log.debug('TEST', extra=dict(namespace=__name__))
        
        app.log.info('TEST', __name__, extra=dict(foo='bar'))
        app.log.warn('TEST', __name__, extra=dict(foo='bar'))
        app.log.error('TEST', __name__, extra=dict(foo='bar'))
        app.log.fatal('TEST', __name__, extra=dict(foo='bar'))
        app.log.debug('TEST', __name__, extra=dict(foo='bar'))
        
        app.log.info('TEST', __name__)
        app.log.warn('TEST', __name__)
        app.log.error('TEST', __name__)
        app.log.fatal('TEST', __name__)
        app.log.debug('TEST', __name__)
        
    def test_bad_level(self):
        defaults = backend.defaults()
        defaults['log'] = dict(
            level='BOGUS'
            )
        app = self.make_app(config_defaults=defaults)
        app.setup()            
        self.eq(app.log.get_level(), 'INFO')

    def test_clear_loggers(self):
        self.app.setup()
        han = handler.get('log', 'logging')
        Log = han()
        Log.clear_loggers()

    def test_rotate(self):
        log_file = mkstemp()[1]
        defaults = backend.defaults()
        defaults['log'] = dict(
            file=log_file,
            level='DEBUG',
            rotate=True,
            max_bytes=10,
            max_files=2,
            )
        app = self.make_app(config_defaults=defaults)
        app.setup()    
        app.log.info('test log message')
        
        # check that a second file was created, because this log is over 12
        # bytes.
        self.ok(os.path.exists("%s.1" % log_file))
        self.ok(os.path.exists("%s.2" % log_file))
        
        # this file should exist because of max files
        self.eq(os.path.exists("%s.3" % log_file), False)
        
    def test_missing_log_dir(self):
        _, tmp_path = mkstemp()
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        
        defaults = backend.defaults()
        defaults['log'] = dict(
            file=os.path.join(tmp_path, 'cement-testapp.log'),
            )
        app = self.make_app(config_defaults=defaults)
        app.setup()
