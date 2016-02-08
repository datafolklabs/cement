"""Tests for cement.core.extension."""

from cement.core import exc, backend, extension, output, interface
from cement.utils import test


class IBogus(interface.Interface):

    class IMeta:
        label = 'bogus'


class BogusExtensionHandler(extension.CementExtensionHandler):

    class Meta:
        interface = IBogus
        label = 'bogus'


class ExtensionTestCase(test.CementCoreTestCase):

    @test.raises(exc.FrameworkError)
    def test_invalid_extension_handler(self):
        # the handler type bogus doesn't exist
        self.app.handler.register(BogusExtensionHandler)

    def test_load_extensions(self):
        ext = extension.CementExtensionHandler()
        ext._setup(self.app)
        ext.load_extensions(['cement.ext.ext_configparser'])

    def test_load_extensions_again(self):
        ext = extension.CementExtensionHandler()
        ext._setup(self.app)
        ext.load_extensions(['cement.ext.ext_configparser'])
        ext.load_extensions(['cement.ext.ext_configparser'])

    @test.raises(exc.FrameworkError)
    def test_load_bogus_extension(self):
        ext = extension.CementExtensionHandler()
        ext._setup(self.app)
        ext.load_extensions(['bogus'])

    def test_get_loaded_extensions(self):
        ext = extension.CementExtensionHandler()
        ext._setup(self.app)

        res = 'cement.ext.ext_json' not in ext.get_loaded_extensions()
        self.ok(res)

        ext.load_extensions(['json'])

        res = 'cement.ext.ext_json' in ext.get_loaded_extensions()
        self.ok(res)
