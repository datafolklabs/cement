"""Tests for cement.core.log."""

import logging
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, backend, handler, log, config
from cement2 import test_helper as _t
_t.prep()

#from cement2.ext import ext_logging, ext_configparser

config = {}
config['log'] = {}
config['log']['file'] = None
config['log']['level'] = 'INFO'
config['log']['to_console'] = True
config['log']['rotate'] = False
config['log']['max_bytes'] = 512000
config['log']['max_files'] = 4
config['log']['file_formatter'] = None
config['log']['console_formatter'] = None
config['log']['clear_loggers'] = True
        
class BogusHandler1(log.CementLogHandler):
    class Meta:
        interface = log.ILog
        label = 'bogus'

@raises(exc.CementInterfaceError)
def test_unproviding_handler():
    try:
        handler.register(BogusHandler1)
    except exc.CementInterfaceError:
        raise

def test_logging():
    app = _t.prep('test')
    app.setup()
    app.config.set('log', 'file', '/dev/null')
    app.config.set('log', 'to_console', True)

    # setup logging again
    app.log.setup(app.config)
    
    app.log.info('Info Message')
    app.log.warn('Warn Message')
    app.log.error('Error Message')
    app.log.fatal('Fatal Message')
    app.log.debug('Debug Message')
    
def test_bogus_log_level():
    app = _t.prep('test')
    app.setup()
    app.config.set('log', 'file', '/dev/null')
    app.config.set('log', 'to_console', True)
    
    # setup logging again
    app.log.setup(app.config)
    app.log.set_level('BOGUS')

def test_console_log():
    app = _t.prep('test')
    app.setup()
    
    app.config.set('base', 'debug', True)
    app.config.set('log', 'file', '/dev/null')
    app.config.set('log', 'to_console', True)
    
    app.log.setup(app.config)
    app.log.info('Tested.')