
import pytest

from cement.core.foundation import TestApp
from cement.core.handler import Handler
from cement.core.exc import FrameworkError
from cement.core.extension import ExtensionHandlerBase, ExtensionHandler


### module tests

class TestExtensionHandlerBase(object):
    def test_interface(self):
        assert ExtensionHandlerBase.Meta.interface == 'extension'


class TestExtensionHandler(object):
    def test_subclassing(self):
        class MyExtensionHandler(ExtensionHandler):
            class Meta:
                label = 'my_extension_handler'

            def load_extension(self, *args, **kw):
                pass

            def load_extensions(self, *args, **kw):
                pass

        h = MyExtensionHandler()
        assert h._meta.interface == 'extension'
        assert h._meta.label == 'my_extension_handler'


### app functionality and coverage tests


class Bogus(Handler):

    class Meta:
        label = 'bogus'


class BogusExtensionHandler(ExtensionHandler):

    class Meta:
        interface = 'bogus'
        label = 'bogus'


def test_invalid_extension_handler():
    # the handler type bogus doesn't exist
    with pytest.raises(FrameworkError, match="Handler .* doesn't exist."):
        with TestApp() as app:
            app.handler.register(BogusExtensionHandler)


def test_load_extensions():
    with TestApp() as app:
        ext = ExtensionHandler()
        ext._setup(app)
        ext.load_extensions(['cement.ext.ext_configparser'])


def test_load_extensions_again():
    with TestApp() as app:
        ext = ExtensionHandler()
        ext._setup(app)
        ext.load_extensions(['cement.ext.ext_configparser'])
        ext.load_extensions(['cement.ext.ext_configparser'])


def test_load_bogus_extension():
    with pytest.raises(FrameworkError, match='No module named'):
        with TestApp() as app:
            ext = ExtensionHandler()
            ext._setup(app)
            ext.load_extensions(['bogus'])

def test_get_loaded_extensions():
    with TestApp() as app:
        ext = ExtensionHandler()
        ext._setup(app)

        assert 'cement.ext.ext_json' not in ext.get_loaded_extensions()

        ext.load_extensions(['json'])

        assert 'cement.ext.ext_json' in ext.get_loaded_extensions()
