"""Tests for cement.core.interface."""

from cement.core import exc, interface, output, meta
from cement.core.handler import CementBaseHandler
from cement.utils import test


class TestInterface(interface.Interface):

    class IMeta:
        label = 'test'


class TestHandler(CementBaseHandler):

    class Meta:
        interface = TestInterface
        label = 'test'


class TestHandler2(CementBaseHandler):

    class Meta:
        interface = output.IOutput
        label = 'test2'


class TestHandler3():
    pass


class InterfaceTestCase(test.CementCoreTestCase):

    def setUp(self):
        super(InterfaceTestCase, self).setUp()
        self.app = self.make_app()

    @test.raises(exc.InterfaceError)
    def test_interface_class(self):
        try:
            i = interface.Interface()
        except exc.InterfaceError as e:
            self.eq(e.msg, "Interfaces can not be used directly.")
            raise

    def test_attribute_class(self):
        i = interface.Attribute('Test attribute')
        self.eq(i.__repr__(), "<interface.Attribute - 'Test attribute'>")

    def test_validator(self):
        interface.validate(TestInterface, TestHandler(), [])

    @test.raises(exc.InterfaceError)
    def test_validate_bad_interface(self):
        han = TestHandler2()
        try:
            interface.validate(TestInterface, han, [])
        except exc.InterfaceError as e:
            self.eq(e.msg, "%s does not implement %s." % (han, TestInterface))
            raise

    @test.raises(exc.InterfaceError)
    def test_validate_bad_interface_no_meta(self):
        han = TestHandler3()
        try:
            interface.validate(TestInterface, han, [])
        except exc.InterfaceError as e:
            self.eq(e.msg, "Invalid or missing: ['_meta'] in %s" % han)
            raise

    @test.raises(exc.InterfaceError)
    def test_validate_bad_interface_missing_meta(self):
        han = TestHandler()
        try:
            interface.validate(TestInterface, han, [], ['missing_meta'])
        except exc.InterfaceError as e:
            self.eq(
                e.msg, "Invalid or missing: ['_meta.missing_meta'] in %s" % han)
            raise

    def test_interface_list(self):
        res = 'output' in interface.list()
        self.ok(res)
