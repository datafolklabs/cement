"""Tests for cement2.ext.ext_logging."""

import logging
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import handler, backend, log

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

@with_setup(startup, teardown)
def test_rotate():
    handler.register(LoggingLogHandler)

    myconfig = ConfigParserConfigHandler()
    myconfig.setup(backend.defaults())
    
    myconfig.set('base', 'debug', True)
    myconfig.set('log', 'file', '/dev/null')
    myconfig.set('log', 'rotate', True)
    myconfig.set('log', 'to_console', True)
    
    h = handler.get('log', 'logging')
    Log = h(
        clear_loggers=True,
        console_formatter=logging.Formatter("%(levelname)s: %(message)s")
        )
    Log.setup(myconfig)

@with_setup(startup, teardown)
def test_bad_level():
    handler.register(LoggingLogHandler)

    myconfig = ConfigParserConfigHandler()
    myconfig.setup(backend.defaults())
    
    myconfig.set('log', 'file', '/dev/null')
    myconfig.set('log', 'rotate', True)
    myconfig.set('log', 'to_console', True)
    myconfig.set('log', 'level', 'BOGUS')
    
    h = handler.get('log', 'logging')
    Log = h(
        clear_loggers=True,
        console_formatter=logging.Formatter("%(levelname)s: %(message)s"),
        )
    Log.setup(myconfig)