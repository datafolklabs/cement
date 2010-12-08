"""The purpose of this module is to test bootstrapping functionality."""

from nose.tools import raises, with_setup, eq_, ok_

from cement import namespaces
from cement.core.namespace import get_config
from cement.core.testing import simulate

from cement_test.core.testing import setup_func, teardown_func

config = get_config()
    
@with_setup(setup_func, teardown_func)
def test_import_install_plugin():  
    # example plugin is imported in root bootstrap, so it should have
    # a place in global namespaces
    ok_(namespaces.has_key('example'))
