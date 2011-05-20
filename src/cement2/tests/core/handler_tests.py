"""Tests for cement.core.handler."""

import sys
from zope import interface
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, backend, handler, handler, output

def startup():    
    pass

def teardown():
    pass
        
class BogusOutputHandler(object):
    #__handler_type__ = 'output'
    __handler_label__ = 'bogus_handler'
    interface.implements(output.IOutputHandler)
    pass

class BogusOutputHandler2(object):
    __handler_type__ = 'output'
    __handler_label__ = 'bogus_handler'
    #interface.implements(output.IOutputHandler)
    pass
    

@raises(exc.CementRuntimeError)
@with_setup(startup, teardown)    
def test_get_invalid_handler():
    handler.get('output', 'bogus_handler')

@raises(exc.CementInterfaceError)
def test_register_invalid_handler():
    handler.register(BogusOutputHandler)

@raises(exc.CementRuntimeError)
def test_register_duplicate_handler():
    handler.define('output', output.IOutputHandler)
    handler.register(output.CementOutputHandler)
    try:
        handler.register(output.CementOutputHandler)
    except exc.CementRuntimeError:
        del backend.handlers['output']
        raise
    
@raises(exc.CementInterfaceError)
def test_register_unproviding_handler():
    handler.define('output', output.IOutputHandler)
    try:
        handler.register(BogusOutputHandler2)
    except exc.CementInterfaceError:
        del backend.handlers['output']
        raise

def test_verify_handler():
    handler.define('output', output.IOutputHandler)
    handler.register(output.CementOutputHandler)
    ok_(handler.enabled('output', 'cement'))
    eq_(handler.enabled('output', 'bogus_handler'), False)
    eq_(handler.enabled('bogus_type', 'bogus_handler'), False)
    