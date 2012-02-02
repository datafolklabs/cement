"""Tests for cement.core.config."""

from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, backend, config, handler
from cement2 import test_helper as _t
_t.prep()

from cement2.lib.ext_configparser import ConfigParserConfigHandler

class BogusConfigHandler(config.CementConfigHandler):
    class Meta:
        interface = config.IConfig
        label = 'bogus'
    
@raises(exc.CementInterfaceError)
def test_invalid_config_handler():
    _t.prep()
    handler.register(BogusConfigHandler)
    
def test_has_key():
    _t.prep()
    myconfig = ConfigParserConfigHandler()
    myconfig.setup(backend.defaults('helloworld'))
    ok_(myconfig.has_key('base', 'config_handler'))
    eq_(myconfig.has_key('base', 'bogus_option'), False)
