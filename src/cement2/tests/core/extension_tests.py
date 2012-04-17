"""Tests for cement.core.extension."""

import unittest
from nose.tools import raises
from cement2.core import exc, backend, extension, handler, output, interface
from cement2 import test_helper as _t

class IBogus(interface.Interface):
    class IMeta:
        label = 'bogus'
        
class BogusExtensionHandler(extension.CementExtensionHandler):
    class Meta:
        interface = IBogus
        label = 'bogus'

class ExtensionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep()
        
    @raises(exc.CementRuntimeError)
    def test_invalid_extension_handler(self):
        # the handler type bogus doesn't exist
        handler.register(BogusExtensionHandler)

    def test_load_extensions(self):
        ext = extension.CementExtensionHandler()
        ext._setup(self.app)
        ext.load_extensions(['cement2.ext.ext_configparser'])

    def test_load_extensions_again(self):
        ext = extension.CementExtensionHandler()
        ext._setup(self.app)
        ext.load_extensions(['cement2.ext.ext_configparser'])
        ext.load_extensions(['cement2.ext.ext_configparser'])
    
    @raises(exc.CementRuntimeError)
    def test_load_bogus_extension(self):
        ext = extension.CementExtensionHandler()
        ext._setup(self.app)
        ext.load_extensions(['bogus'])
