"""Tests for cement.core.log."""

import sys
from zope import interface
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, backend, handler, log, config

def startup():    
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
    handler.register(log.LoggingLogHandler)
    
    myconfig = config.ConfigParserConfigHandler(backend.defaults())
    myconfig.set('log', 'file', '/dev/null')
    myconfig.set('log', 'to_console', True)
    
    h = handler.get('log', 'logging')

    Log = h(myconfig, 
        level='BOGUS',
        clear_loggers=True,
        )
    

