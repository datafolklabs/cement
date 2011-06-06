"""Tests for cement.core.log."""

import sys
import logging
from zope import interface
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, backend, handler, log, config

if not handler.defined('log'):
    handler.define('log', log.ILogHandler)
if not handler.defined('config'):
    handler.define('config', config.IConfigHandler)
from cement2.ext.ext_logging import LoggingLogHandler
from cement2.ext.ext_configparser import ConfigParserConfigHandler

def startup():    
    if not handler.defined('log'):
        handler.define('log', log.ILogHandler)

def teardown():
    if backend.handlers.has_key('log'):
        del backend.handlers['log']
        
class BogusHandler1(object):
    __handler_type__ = 'log'
    __handler_label__ = 'bogus'
    interface.implements(log.ILogHandler)

@raises(exc.CementInterfaceError)
@with_setup(startup, teardown)
def test_unproviding_handler():
    try:
        handler.register(BogusHandler1)
    except exc.CementInterfaceError:
        del backend.handlers['log']
        raise

@with_setup(startup, teardown)
def test_logging():
    handler.register(LoggingLogHandler)
    
    myconfig = ConfigParserConfigHandler()
    myconfig.setup(backend.defaults())
    myconfig.set('log', 'file', '/dev/null')
    myconfig.set('log', 'to_console', True)
    
    h = handler.get('log', 'logging')

    Log = h(
        level='WARN',
        clear_loggers=True,
        )
    Log.setup(myconfig)
    Log.info('Info Message')
    Log.warn('Warn Message')
    Log.error('Error Message')
    Log.fatal('Fatal Message')
    Log.debug('Debug Message')
    
@with_setup(startup, teardown)
def test_bogus_test_level():
    handler.register(LoggingLogHandler)
    
    myconfig = ConfigParserConfigHandler()
    myconfig.setup(backend.defaults())
    myconfig.set('log', 'file', '/dev/null')
    myconfig.set('log', 'to_console', True)
    
    h = handler.get('log', 'logging')

    Log = h(
        level='WARN',
        clear_loggers=True,
        )
    Log.setup(myconfig)
    Log.set_level('BOGUS')

@with_setup(startup, teardown)
def test_console_log():
    handler.register(LoggingLogHandler)

    myconfig = ConfigParserConfigHandler()
    myconfig.setup(backend.defaults())
    
    myconfig.set('base', 'debug', True)
    myconfig.set('log', 'file', '/dev/null')
    myconfig.set('log', 'to_console', True)
    
    h = handler.get('log', 'logging')
    Log = h(
        clear_loggers=True,
        console_formatter=logging.Formatter("%(levelname)s: %(message)s")
        )
    Log.setup(myconfig)
