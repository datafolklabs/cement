"""Tests for cement.core.interface."""

from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, interface, output, handler, meta
from cement2 import test_helper as _t
_t.prep() 

class TestInterface(meta.MetaMixin):
    class IMeta:
        label = 'test'

class TestHandler(meta.MetaMixin):
    class Meta:
        interface = TestInterface
        label = 'test'
        
class TestHandler2(meta.MetaMixin):
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
def test_validate_bad_interface_no_meta():
    interface.validate(TestInterface, TestHandler3(), [])

@raises(exc.CementInterfaceError)
def test_validate_bad_interface_missing_meta():
    interface.validate(TestInterface, TestHandler3(), [], ['missing_meta'])
