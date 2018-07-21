
from pytest import raises

from cement.core.foundation import TestApp
from cement.core.interface import Interface
from cement.core.exc import InterfaceError
from cement.core.output import OutputInterface


# module tests

class TestInterface(object):
    def test_subclassing(self):
        class MyInterface(Interface):
            class Meta:
                interface = 'test'


class TestInterfaceManager(object):
    pass


# app functionality and coverage tests


def test_missing_interface_label():
    class BadInterface(Interface):
        class Meta:
            interface = None

    with raises(InterfaceError, match=".*Meta.interface undefined"):
        BadInterface()


def test_get_invalid_interface():
    with raises(InterfaceError, match='.*bogus_interface.* does not exist'):
        with TestApp() as app:
            app.interface.get('bogus_interface')


def test_define_duplicate_interface():
    class DuplicateInterface(OutputInterface):
        pass

    with raises(InterfaceError, match='.*output.* already defined'):
        with TestApp(interfaces=[OutputInterface]):
            pass


def test_interface_defined():
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


def test_interface_list():
    with TestApp() as app:
        assert 'config' in app.interface.list()


def test_interface_get_fallback():
    with TestApp() as app:
        assert app.interface.get('bogus', 'foo') == 'foo'
