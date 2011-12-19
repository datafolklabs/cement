"""Tests for cement.core.interface."""

import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, interface, output, handler
from cement2 import test_helper as _t

_t.prep()    

class TestInterface():
    class IMeta:
        label = 'test'

class TestHandler():
    class Meta:
        interface = TestInterface
        label = 'test'
        
class TestHandler2():
    class Meta:
        interface = output.IOutput
        label = 'test2'

class TestHandler3():
    pass
    

@raises(exc.CementInterfaceError)
def test_interface_class():
    i = interface.Interface()

def test_attribute_class():
    i = interface.Attribute('Test attribute')
    eq_(i.__repr__(), "<interface.Attribute - 'Test attribute'>")

def test_validator():
    interface.validate(TestInterface, TestHandler(), [])
    
@raises(exc.CementInterfaceError)
def test_validate_bad_interface():
    interface.validate(TestInterface, TestHandler2(), [])

@raises(exc.CementInterfaceError)
def test_validate_bad_interface_no_Meta():
    interface.validate(TestInterface, TestHandler3(), [])
    
### FIX ME: Remove before Cement2 stable release
class OldInterface(interface.Interface):
    class imeta:
        label = 'old_interface'
        
class OldHandler(object):
    class meta:
        label = 'old_handler'
        interface = OldInterface
        
def test_old_interface_imeta():
    handler.define(OldInterface)
    handler.register(OldHandler)