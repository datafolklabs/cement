
from pytest import raises

from cement.core.foundation import TestApp
from cement.core.handler import Handler
from cement.core.meta import MetaMixin
from cement.core.exc import FrameworkError, InterfaceError
from cement.ext.ext_configparser import ConfigParserConfigHandler
from cement.ext.ext_dummy import DummyOutputHandler


# module tests

class TestHandler(object):
    def test_subclassing(self):
        class MyHandler(Handler):
            class Meta:
                label = 'my_handler'
                interface = 'test'

        h = MyHandler()
        assert h._meta.interface == 'test'
        assert h._meta.label == 'my_handler'


class TestHandlerManager(object):
    pass


# app functionality and coverage tests


def test_get_invalid_handler():
    with raises(FrameworkError, match='.*bogus_handler.* does not exist'):
        with TestApp() as app:
            app.handler.get('output', 'bogus_handler')


def test_register_invalid_handlers():
    class BogusHandlerNoMeta(MetaMixin):
        pass

    class BogusHandlerNoMetaInterface(MetaMixin):
        class Meta:
            # interface = Bogus
            label = 'bogus_handler'

    class BogusHandlerNoMetaLabel(MetaMixin):
        class Meta:
            interface = 'output'
            # label = 'bogus4'

    with TestApp() as app:
        msg = 'Class .*BogusHandlerNoMeta.* does not implement Handler'
        with raises(InterfaceError, match=msg):
            app.handler.register(BogusHandlerNoMeta)

        msg = 'Class .*BogusHandlerNoMetaInterface.* does not implement ' + \
              'Handler'
        with raises(InterfaceError, match=msg):
            app.handler.register(BogusHandlerNoMetaInterface)

        msg = 'Class .*BogusHandlerNoMetaLabel.* does not implement Handler'
        with raises(InterfaceError, match=msg):
            app.handler.register(BogusHandlerNoMetaLabel)

    # coverage

    class MyHandler(DummyOutputHandler):
        class Meta:
            label = None

    msg = 'MyHandler.Meta.label undefined.'
    with raises(FrameworkError, match=msg):
        MyHandler()


def test_handler_does_not_subclass():
    class MyHandler(DummyOutputHandler):
        class Meta:
            label = 'does-not-subclass-argument-handler'
            interface = 'argument'

    with TestApp() as app:
        msg = 'Handler MyHandler does not sub-class ArgumentInterface'
        with raises(InterfaceError, match=msg):
            app.handler.register(MyHandler)


def test_register_duplicate_handler():
    class DuplicateHandler(DummyOutputHandler):
        pass

    with TestApp() as app:
        app.handler.register(DummyOutputHandler)

        with raises(FrameworkError, match='.*dummy.* already exists'):
            app.handler.register(DuplicateHandler)


def test_register_force():
    class DuplicateHandler(DummyOutputHandler):
        pass

    with TestApp() as app:
        # register once, verify
        app.handler.register(DummyOutputHandler)
        assert app.handler.get('output', 'dummy')

        # register again with force, and verify we get new class back
        app.handler.register(DuplicateHandler, force=True)
        assert app.handler.get('output', 'dummy') == DuplicateHandler


def test_register_unproviding_handler():
    class BogusHandler(MetaMixin):
        class Meta:
            interface = 'output'
            label = 'bogus_handler'

    with TestApp() as app:
        msg = '.*BogusHandler.* does not implement Handler'
        with raises(InterfaceError, match=msg):
            app.handler.register(BogusHandler)


def test_verify_handler():
    with TestApp() as app:
        assert app.handler.registered('output', 'dummy') is True
        assert app.handler.registered('output', 'bogus_handler') is False
        assert app.handler.registered('bogus_interface', 'bogus_handler') \
            is False


def test_get_bogus_handler():
    with TestApp() as app:
        with raises(FrameworkError, match='.*log.*bogus.* does not exist!'):
            app.handler.get('log', 'bogus')


def test_get_bogus_handler_interface():
    with TestApp() as app:
        with raises(FrameworkError, match='Interface .* does not exist!'):
            app.handler.get('bogus', 'bogus')


def test_handler_defined():
    with TestApp() as app:
        interfaces = [
            'config',
            'log',
            'argument',
            'plugin',
            'extension',
            'output',
            'template',
            'controller'
        ]
        for handler_interface in interfaces:
            assert app.interface.defined(handler_interface) is True

        # and check for bogus one too
        assert app.interface.defined('bogus') is False


def test_handler_list():
    with TestApp() as app:
        assert ConfigParserConfigHandler in app.handler.list('config')


def test_handler_registered():
    with TestApp() as app:
        assert app.handler.registered('output', 'dummy') is True


def test_handler_get_fallback():
    with TestApp() as app:
        assert app.handler.get('log', 'foo', 'bar') == 'bar'


def test_register_invalid_handler_interfaces():
    class BadHandler(Handler):
        class Meta:
            label = 'bad'
            interface = 'bad_interface_not_defined'

    with TestApp() as app:
        with raises(InterfaceError, match='interface .* doesn\'t exist.'):
            app.handler.register(BadHandler)


def test_setup():
    with TestApp() as app:
        han = app.handler.get('output', 'dummy')
        assert not hasattr(han, '_meta')

        han = app.handler.get('output', 'dummy', setup=True)
        assert hasattr(han, '_meta')


def test_validate():
    class MyHandler(DummyOutputHandler):
        class Meta:
            label = 'my_handler'

        def _validate(self):
            raise Exception('it validated')

    with raises(Exception, match='it validated'):
        with TestApp(handlers=[MyHandler], output_handler='my_handler') as app:
            app.run()


def test_list_bogus_interface():
    with raises(InterfaceError, match='Interface .* does not exist.'):
        with TestApp() as app:
            app.handler.list('bogus')
