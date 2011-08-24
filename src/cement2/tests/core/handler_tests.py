"""Tests for cement.core.handler."""

import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, backend, handler, handler, output
from cement2 import test_helper as _t

_t.prep('test')

from cement2.ext import ext_cement_output

class BogusOutputHandler(object):
    class meta:
        #interface = IBogus
        label = 'bogus_handler'

class BogusOutputHandler2(object):
    class meta:
        interface = output.IOutput
        label = 'bogus_handler'

class BogusHandler3(object):
    pass   

class DuplicateHandler(object):
    class meta:
        interface = output.IOutput
        label = 'cement'
        
@raises(exc.CementRuntimeError)
def test_get_invalid_handler():
    _t.prep('test')
    handler.get('output', 'bogus_handler')

@raises(exc.CementInterfaceError)
def test_register_invalid_handler():
    _t.prep('test')
    handler.register(BogusOutputHandler)

@raises(exc.CementRuntimeError)
def test_register_duplicate_handler():
    _t.prep('test')
    handler.register(ext_cement_output.CementOutputHandler)
    try:
        handler.register(DuplicateHandler)
    except exc.CementRuntimeError:
        raise
    
@raises(exc.CementInterfaceError)
def test_register_unproviding_handler():
    _t.prep('test')
    try:
        handler.register(BogusOutputHandler2)
    except exc.CementInterfaceError:
        del backend.handlers['output']
        raise

def test_verify_handler():
    _t.prep('test')
    handler.register(ext_cement_output.CementOutputHandler)
    ok_(handler.enabled('output', 'cement'))
    eq_(handler.enabled('output', 'bogus_handler'), False)
    eq_(handler.enabled('bogus_type', 'bogus_handler'), False)
    
