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
    try:
        i = interface.Interface()
    except exc.CementInterfaceError as e:
        eq_(e.msg, "Interfaces can not be used directly.")
        raise

def test_attribute_class():
    i = interface.Attribute('Test attribute')
    eq_(i.__repr__(), "<interface.Attribute - 'Test attribute'>")

def test_validator():
    interface.validate(TestInterface, TestHandler(), [])
    
@raises(exc.CementInterfaceError)
def test_validate_bad_interface():
    han = TestHandler2()
    try:
        interface.validate(TestInterface, han, [])
    except exc.CementInterfaceError as e:
        eq_(e.msg, "%s does not implement %s." % (han, TestInterface))
        raise
        
@raises(exc.CementInterfaceError)
def test_validate_bad_interface_no_meta():
    han = TestHandler3()
    try:
        interface.validate(TestInterface, han, [])
    except exc.CementInterfaceError as e:
        eq_(e.msg, "Invalid or missing: ['_meta'] in %s" % han)
        raise 

@raises(exc.CementInterfaceError)
def test_validate_bad_interface_missing_meta():
    han = TestHandler()
    try:
        interface.validate(TestInterface, han, [], ['missing_meta'])
    except exc.CementInterfaceError as e:
        eq_(e.msg, "Invalid or missing: ['_meta.missing_meta'] in %s" % han)
        raise
