"""Tests for cement.core.extension."""

import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, backend, extension, handler, output, interface
from cement2 import test_helper as _t

class IBogus(interface.Interface):
    class imeta:
        label = 'bogus'
        
class BogusExtensionHandler(object):
    class meta:
        interface = IBogus
        label = 'bogus'
    
@raises(exc.CementRuntimeError)
def test_invalid_extension_handler():
    # the handler type test_extension doesn't exist
    handler.register(BogusExtensionHandler)

def test_load_extensions():
    _t.reset_backend()
    handler.define(output.IOutput)
    ext = extension.CementExtensionHandler()
    ext.setup(backend.defaults('nosetests'))
    ext.load_extensions(['cement2.ext.ext_configparser'])

def test_load_extensions_again():
    _t.reset_backend()
    handler.define(output.IOutput)
    ext = extension.CementExtensionHandler()
    ext.setup(backend.defaults('nosetests'))
    ext.load_extensions(['cement2.ext.ext_configparser'])
    ext.load_extensions(['cement2.ext.ext_configparser'])
    
@raises(exc.CementRuntimeError)
def test_load_bogus_extension():
    ext = extension.CementExtensionHandler()
    ext.setup(backend.defaults('nosetests'))
    ext.load_extensions(['bogus'])
