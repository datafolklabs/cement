"""Tests for cement.core.config."""

import sys
from zope import interface
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, backend, config, handler

handler.define('config', config.IConfigHandler)
from cement2.ext.ext_configparser import ConfigParserConfigHandler

def startup():    
    handler.define('testconfig', config.IConfigHandler)

def teardown():
    if 'testconfig' in backend.handlers:
        del backend.handlers['testconfig']
    
    
class BogusConfigHandler(object):
    __handler_type__ = 'testconfig'
    __handler_label__ = 'bogus'
    interface.implements(config.IConfigHandler)
    pass
    
@with_setup(startup, teardown)    
@raises(exc.CementInterfaceError)
def test_invalid_config_handler():
    handler.register(BogusConfigHandler)
    
def test_has_key():
    myconfig = ConfigParserConfigHandler()
    myconfig.setup(backend.defaults())
    ok_(myconfig.has_key('base', 'config_handler'))
    eq_(myconfig.has_key('base', 'bogus_option'), False)
