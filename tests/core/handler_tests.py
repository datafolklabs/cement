"""Tests for cement.core.handler."""

from cement.core import exc, output, meta
from cement.core import interface
from cement.utils import test
from cement.ext.ext_configparser import ConfigParserConfigHandler


class BogusOutputHandler(meta.MetaMixin):

    class Meta:
        #interface = IBogus
        label = 'bogus_handler'


class BogusOutputHandler2(meta.MetaMixin):
    class Meta:
        interface = output.IOutput
        label = 'bogus_handler'


class BogusHandler3(meta.MetaMixin):
    pass


class BogusHandler4(meta.MetaMixin):
    class Meta:
        interface = output.IOutput
        # label = 'bogus4'


class DuplicateHandler(output.CementOutputHandler):
    class Meta:
        interface = output.IOutput
        label = 'dummy'

    def _setup(self, config_obj):
        pass

    def render(self, data_dict, template=None):
        pass


class BogusInterface1(interface.Interface):
    pass


class BogusInterface2(interface.Interface):
    class IMeta:
        pass


class TestInterface(interface.Interface):
    class IMeta:
        label = 'test'


class TestHandler(meta.MetaMixin):
    class Meta:
        interface = TestInterface
        label = 'test'


class HandlerTestCase(test.CementCoreTestCase):
    def setUp(self):
        self.app = self.make_app()

    @test.raises(exc.FrameworkError)
    def test_get_invalid_handler(self):
        self.app.handlers.get('output', 'bogus_handler')

    @test.raises(exc.InterfaceError)
    def test_register_invalid_handler(self):
        self.app.handlers.register(BogusOutputHandler)

    @test.raises(exc.InterfaceError)
    def test_register_invalid_handler_no_meta(self):
        self.app.handlers.register(BogusHandler3)

    @test.raises(exc.InterfaceError)
    def test_register_invalid_handler_no_Meta_label(self):
        self.app.handlers.register(BogusHandler4)

    @test.raises(exc.FrameworkError)
    def test_register_duplicate_handler(self):
        from cement.ext import ext_dummy
        self.app.handlers.register(ext_dummy.DummyOutputHandler)
        try:
            self.app.handlers.register(DuplicateHandler)
        except exc.FrameworkError:
            raise

    @test.raises(exc.InterfaceError)
    def test_register_unproviding_handler(self):
        try:
            self.app.handlers.register(BogusOutputHandler2)
        except exc.InterfaceError:
            raise

    def test_verify_handler(self):
        self.app.setup()
        self.ok(self.app.handlers.registered('output', 'dummy'))
        self.eq(self.app.handlers.registered('output', 'bogus_handler'), False)
        self.eq(self.app.handlers.registered('bogus_type', 'bogus_handler'), False)

    @test.raises(exc.FrameworkError)
    def test_get_bogus_handler(self):
        self.app.handlers.get('log', 'bogus')

    @test.raises(exc.FrameworkError)
    def test_get_bogus_handler_type(self):
        self.app.handlers.get('bogus', 'bogus')

    def test_handler_defined(self):
        for handler_type in ['config', 'log', 'argument', 'plugin',
                             'extension', 'output', 'controller']:
            yield self.is_defined, handler_type

        # and check for bogus one too
        self.eq(self.app.handlers.defined('bogus'), False)

    def test_handler_list(self):
        self.app.setup()
        handler_list = self.app.handlers.get('config').values()
        res = ConfigParserConfigHandler in handler_list
        self.ok(res)

    @test.raises(exc.FrameworkError)
    def test_handler_list_bogus_type(self):
        self.app.setup()
        handler_list = self.app.handlers.get('bogus').values()

    def is_defined(self, handler_type):
        self.eq(self.app.handlers.defined(handler_type), True)

    @test.raises(exc.InterfaceError)
    def test_bogus_interface_no_IMeta(self):
        self.app.handlers.define(BogusInterface1)

    @test.raises(exc.InterfaceError)
    def test_bogus_interface_no_IMeta_label(self):
        self.app.handlers.define(BogusInterface2)

    @test.raises(exc.FrameworkError)
    def test_define_duplicate_interface(self):
        self.app.handlers.define(output.IOutput)
        self.app.handlers.define(output.IOutput)

    def test_interface_with_no_validator(self):
        self.app.handlers.define(TestInterface)
        self.app.handlers.register(TestHandler)

    def test_handler_defined(self):
        self.app.handlers.defined('output')

    def test_handler_not_defined(self):
        self.eq(self.app.handlers.defined('bogus'), False)

    def test_handler_registered(self):
        self.app.setup()
        self.eq(self.app.handlers.registered('output', 'dummy'), True)

    def test_handler_get_fallback(self):
        self.app.setup()
        self.eq(self.app.handlers.get('log', 'foo', 'bar'), 'bar')
