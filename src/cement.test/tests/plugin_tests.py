"""The purpose of this module is to test plugin functionality."""

from nose.tools import raises, with_setup, eq_, ok_

from cement import namespaces
from cement.core.namespace import get_config
from cement.core.plugin import load_plugin
from cement.core.testing import simulate
from cement.core.exc import CementRuntimeError, CementConfigError

from cement_test.core.testing import setup_func, teardown_func

config = get_config()
    
@raises(CementRuntimeError)
@with_setup(setup_func, teardown_func)
def test_load_bogus_plugin():  
    load_plugin('some_bogus_plugin')

@raises(CementConfigError)
@with_setup(setup_func, teardown_func)
def test_load_plugin_with_bogus_provider():  
    load_plugin('some_bogus_provider.plugin.example')