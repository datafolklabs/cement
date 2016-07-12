"""Tests for cement.core.handler."""

from cement.core import exc, backend, handler, output, meta
from cement.core import interface
from cement.utils import test
from cement.ext import ext_dummy
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
        super(HandlerTestCase, self).setUp()
        self.app = self.make_app()

    @test.raises(exc.FrameworkError)
    def test_get_invalid_handler(self):
        self.app.handler.get('output', 'bogus_handler')

    @test.raises(exc.InterfaceError)
    def test_register_invalid_handler(self):
        self.app.handler.register(BogusOutputHandler)

    @test.raises(exc.InterfaceError)
    def test_register_invalid_handler_no_meta(self):
        self.app.handler.register(BogusHandler3)

    @test.raises(exc.InterfaceError)
    def test_register_invalid_handler_no_Meta_label(self):
        self.app.handler.register(BogusHandler4)

    @test.raises(exc.FrameworkError)
    def test_register_duplicate_handler(self):
        self.app.handler.register(ext_dummy.DummyOutputHandler)
        try:
            self.app.handler.register(DuplicateHandler)
        except exc.FrameworkError:
            raise

    def test_register_force(self):
        class MyDummy(ext_dummy.DummyOutputHandler):
            pass

        # register once, verify
        self.app.handler.register(ext_dummy.DummyOutputHandler)
        res = self.app.handler.get('output', 'dummy')
        self.eq(res, ext_dummy.DummyOutputHandler)

        # register again with force, and verify we get new class back
        self.app.handler.register(MyDummy, force=True)
        res = self.app.handler.get('output', 'dummy')
        self.eq(res, MyDummy)

    def test_register_force_deprecated(self):
        class MyDummy(ext_dummy.DummyOutputHandler):
            pass

        # register once, verify
        handler.register(ext_dummy.DummyOutputHandler)
        res = self.app.handler.get('output', 'dummy')
        self.eq(res, ext_dummy.DummyOutputHandler)

        # register again with force, and verify we get new class back
        handler.register(MyDummy, force=True)
        res = self.app.handler.get('output', 'dummy')
        self.eq(res, MyDummy)

    @test.raises(exc.InterfaceError)
    def test_register_unproviding_handler(self):
        try:
            self.app.handler.register(BogusOutputHandler2)
        except exc.InterfaceError:
            del backend.__handlers__['output']
            raise

    def test_verify_handler(self):
        self.app.setup()
        self.ok(self.app.handler.registered('output', 'dummy'))
        self.eq(self.app.handler.registered('output', 'bogus_handler'), False)
        self.eq(self.app.handler.registered('bogus_type', 'bogus_handler'), False)

    @test.raises(exc.FrameworkError)
    def test_get_bogus_handler(self):
        self.app.handler.get('log', 'bogus')

    @test.raises(exc.FrameworkError)
    def test_get_bogus_handler_type(self):
        self.app.handler.get('bogus', 'bogus')

    def test_handler_defined(self):
        for handler_type in ['config', 'log', 'argument', 'plugin',
                             'extension', 'output', 'controller']:
            yield is_defined, handler_type

        # and check for bogus one too
        self.eq(self.app.handler.defined('bogus'), False)

    def test_handler_list(self):
        self.app.setup()
        handler_list = self.app.handler.list('config')
        res = ConfigParserConfigHandler in handler_list
        self.ok(res)

    @test.raises(exc.FrameworkError)
    def test_handler_list_bogus_type(self):
        self.app.setup()
        handler_list = self.app.handler.list('bogus')

    def is_defined(handler_type):
        self.eq(self.app.handler.defined(handler_type), True)

    @test.raises(exc.InterfaceError)
    def test_bogus_interface_no_IMeta(self):
        self.app.handler.define(BogusInterface1)

    @test.raises(exc.InterfaceError)
    def test_bogus_interface_no_IMeta_label(self):
        self.app.handler.define(BogusInterface2)

    @test.raises(exc.FrameworkError)
    def test_define_duplicate_interface(self):
        self.app.handler.define(output.IOutput)
        self.app.handler.define(output.IOutput)

    def test_interface_with_no_validator(self):
        self.app.handler.define(TestInterface)
        self.app.handler.register(TestHandler)

    def test_handler_defined(self):
        self.app.handler.defined('output')

    def test_handler_not_defined(self):
        self.eq(self.app.handler.defined('bogus'), False)

    def test_handler_registered(self):
        self.app.setup()
        self.eq(self.app.handler.registered('output', 'dummy'), True)

    def test_handler_get_fallback(self):
        self.app.setup()
        self.eq(self.app.handler.get('log', 'foo', 'bar'), 'bar')

    @test.raises(exc.FrameworkError)
    def test_register_invalid_handler_type(self):
        self.app.setup()
        class BadInterface:
            class IMeta:
                label = 'bad_interface'
        class BadHandler(TestHandler):
            class Meta:
                interface = BadInterface
        self.app.handler.register(BadHandler)


class DeprecatedHandlerTestCase(test.CementCoreTestCase):

    def setUp(self):
        super(DeprecatedHandlerTestCase, self).setUp()
        self.app = self.make_app()

    @test.raises(exc.FrameworkError)
    def test_get_invalid_handler(self):
        handler.get('output', 'bogus_handler')

    @test.raises(exc.InterfaceError)
    def test_register_invalid_handler(self):
        handler.register(BogusOutputHandler)

    @test.raises(exc.InterfaceError)
    def test_register_invalid_handler_no_meta(self):
        handler.register(BogusHandler3)

    @test.raises(exc.InterfaceError)
    def test_register_invalid_handler_no_Meta_label(self):
        handler.register(BogusHandler4)

    @test.raises(exc.FrameworkError)
    def test_register_duplicate_handler(self):
        from cement.ext import ext_dummy
        handler.register(ext_dummy.DummyOutputHandler)
        try:
            handler.register(DuplicateHandler)
        except exc.FrameworkError:
            raise

    @test.raises(exc.InterfaceError)
    def test_register_unproviding_handler(self):
        try:
            handler.register(BogusOutputHandler2)
        except exc.InterfaceError:
            del backend.__handlers__['output']
            raise

    def test_verify_handler(self):
        self.app.setup()
        self.ok(handler.registered('output', 'dummy'))
        self.eq(handler.registered('output', 'bogus_handler'), False)
        self.eq(handler.registered('bogus_type', 'bogus_handler'), False)

    @test.raises(exc.FrameworkError)
    def test_get_bogus_handler(self):
        handler.get('log', 'bogus')

    @test.raises(exc.FrameworkError)
    def test_get_bogus_handler_type(self):
        handler.get('bogus', 'bogus')

    def test_handler_defined(self):
        for handler_type in ['config', 'log', 'argument', 'plugin',
                             'extension', 'output', 'controller']:
            yield is_defined, handler_type

        # and check for bogus one too
        self.eq(handler.defined('bogus'), False)

    def test_handler_list(self):
        self.app.setup()
        handler_list = handler.list('config')
        res = ConfigParserConfigHandler in handler_list
        self.ok(res)

    @test.raises(exc.FrameworkError)
    def test_handler_list_bogus_type(self):
        self.app.setup()
        handler_list = handler.list('bogus')

    @test.raises(exc.FrameworkError)
    def test_register_invalid_handler_type(self):
        self.app.setup()
        class BadInterface:
            class IMeta:
                label = 'bad_interface'
        class BadHandler(TestHandler):
            class Meta:
                interface = BadInterface
        handler.register(BadHandler)

    def is_defined(handler_type):
        self.eq(handler.defined(handler_type), True)

    @test.raises(exc.InterfaceError)
    def test_bogus_interface_no_IMeta(self):
        handler.define(BogusInterface1)

    @test.raises(exc.InterfaceError)
    def test_bogus_interface_no_IMeta_label(self):
        handler.define(BogusInterface2)

    @test.raises(exc.FrameworkError)
    def test_define_duplicate_interface(self):
        handler.define(output.IOutput)
        handler.define(output.IOutput)

    def test_interface_with_no_validator(self):
        handler.define(TestInterface)
        handler.register(TestHandler)

    def test_handler_defined(self):
        handler.defined('output')

    def test_handler_not_defined(self):
        self.eq(handler.defined('bogus'), False)

    def test_handler_registered(self):
        self.app.setup()
        self.eq(handler.registered('output', 'dummy'), True)

    def test_handler_get_fallback(self):
        self.app.setup()
        self.eq(handler.get('log', 'foo', 'bar'), 'bar')

    def test_resolve(self):
        # just get some coverage
        handler.define(TestInterface)
        handler.resolve('test', TestHandler())
        handler.resolve('test', 'test')
        handler.resolve('test', TestHandler)

        self.reset_backend()
        self.app = self.make_app('test')
        handler.define(TestInterface)
        handler.resolve('test', TestHandler)
        handler.resolve('test', None, raise_error=False)
        try:
            handler.resolve('test', None)
        except Exception as e:
            pass
