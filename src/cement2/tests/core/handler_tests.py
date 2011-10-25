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

class BogusHandler4(object):
    class meta:
        interface = output.IOutput
        # label = 'bogus4'

class DuplicateHandler(object):
    class meta:
        interface = output.IOutput
        label = 'cement'
        
class BogusInterface1(object):
    pass
    
class BogusInterface2(object):
    class imeta:
        pass
    
class TestInterface(object):
    class imeta:
        label = 'test'
        
class TestHandler(object):
    class meta:
        interface = TestInterface
        label = 'test'
        
@raises(exc.CementRuntimeError)
def test_get_invalid_handler():
    _t.prep('test')
    handler.get('output', 'bogus_handler')

@raises(exc.CementInterfaceError)
def test_register_invalid_handler():
    _t.prep('test')
    handler.register(BogusOutputHandler)

@raises(exc.CementInterfaceError)
def test_register_invalid_handler_no_meta():
    _t.prep()
    handler.register(BogusHandler3)

@raises(exc.CementInterfaceError)
def test_register_invalid_handler_no_meta_label():
    _t.prep()
    handler.register(BogusHandler4)
    
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

@raises(exc.CementRuntimeError)
def test_get_bogus_handler():
    _t.prep()
    handler.get('log', 'bogus')

@raises(exc.CementRuntimeError)
def test_get_bogus_handler_type():
    _t.prep()
    handler.get('bogus', 'bogus')

def test_handler_defined():
    _t.prep()
    for handler_type in ['config', 'log', 'argument', 'plugin', 'extension', 
                         'output', 'controller']:
        yield is_defined, handler_type

    # and check for bogus one too
    eq_(handler.defined('bogus'), False)
    
def is_defined(handler_type):
    eq_(handler.defined(handler_type), True)

@raises(exc.CementInterfaceError)
def test_bogus_interface_no_imeta():
    handler.define(BogusInterface1)

@raises(exc.CementInterfaceError)
def test_bogus_interface_no_imeta_label():
    handler.define(BogusInterface2)

@raises(exc.CementRuntimeError)
def test_define_duplicate_interface():
    handler.define(output.IOutput)
    handler.define(output.IOutput)

def test_interface_with_no_validator():
    _t.prep()
    handler.define(TestInterface)
    handler.register(TestHandler)
    
    