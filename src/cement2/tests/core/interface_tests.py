"""Tests for cement.core.interface."""

import unittest
from nose.tools import eq_, raises
from cement2.core import exc, interface, output, handler, meta
from cement2 import test_helper as _t

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
    
class InterfaceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep()
        
    @raises(exc.CementInterfaceError)
    def test_interface_class(self):
        try:
            i = interface.Interface()
        except exc.CementInterfaceError as e:
            eq_(e.msg, "Interfaces can not be used directly.")
            raise

    def test_attribute_class(self):
        i = interface.Attribute('Test attribute')
        eq_(i.__repr__(), "<interface.Attribute - 'Test attribute'>")

    def test_validator(self):
        interface.validate(TestInterface, TestHandler(), [])
    
    @raises(exc.CementInterfaceError)
    def test_validate_bad_interface(self):
        han = TestHandler2()
        try:
            interface.validate(TestInterface, han, [])
        except exc.CementInterfaceError as e:
            eq_(e.msg, "%s does not implement %s." % (han, TestInterface))
            raise
        
    @raises(exc.CementInterfaceError)
    def test_validate_bad_interface_no_meta(self):
        han = TestHandler3()
        try:
            interface.validate(TestInterface, han, [])
        except exc.CementInterfaceError as e:
            eq_(e.msg, "Invalid or missing: ['_meta'] in %s" % han)
            raise 

    @raises(exc.CementInterfaceError)
    def test_validate_bad_interface_missing_meta(self):
        han = TestHandler()
        try:
            interface.validate(TestInterface, han, [], ['missing_meta'])
        except exc.CementInterfaceError as e:
            eq_(e.msg, "Invalid or missing: ['_meta.missing_meta'] in %s" % han)
            raise
