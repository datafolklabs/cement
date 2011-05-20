"""Tests for cement.core.extension."""

import sys
from zope import interface
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, backend, extension, handler, output

def startup():    
    handler.define('test_extension', extension.IExtensionHandler)

def teardown():
    if 'test_extension' in backend.handlers:
        del backend.handlers['test_extension']
    
    
class BogusExtensionHandler(object):
    __handler_type__ = 'test_extension'
    __handler_label__ = 'bogus'
    interface.implements(extension.IExtensionHandler)
    pass
    
@raises(exc.CementInterfaceError)
@with_setup(startup, teardown)    
def test_invalid_extension_handler():
    handler.register(BogusExtensionHandler)

def test_load_extensions():
    handler.define('output', output.IOutputHandler)
    ext = extension.CementExtensionHandler(backend.defaults())
    ext.load_extensions(['example'])
    ext.load_extensions(['example'])
    del backend.handlers['output']

@raises(exc.CementRuntimeError)
def test_load_bogus_extension():
    ext = extension.CementExtensionHandler(backend.defaults())
    ext.load_extensions(['bogus'])
