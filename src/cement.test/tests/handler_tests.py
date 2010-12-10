"""The purpose of this module is to test handler functionality."""

from nose.tools import raises, with_setup, eq_, ok_

from cement import namespaces
from cement.core.namespace import get_config
from cement.core.testing import simulate
from cement.core.handler import get_handler, define_handler, register_handler
from cement.core.exc import CementRuntimeError

from cement_test.core.testing import setup_func, teardown_func

config = get_config()
    
@with_setup(setup_func, teardown_func)
def test_get_handler():  
    get_handler('output', 'json')

@raises(CementRuntimeError)
@with_setup(setup_func, teardown_func)
def test_get_handler_bad():  
    get_handler('output', 'bogus handler name')

@raises(CementRuntimeError)
@with_setup(setup_func, teardown_func)
def test_define_duplicate_handler():  
    define_handler('output')

@raises(CementRuntimeError)
@with_setup(setup_func, teardown_func)
def test_register_to_bogus_handler():  
    register_handler('bogus_handler', 'bogus', None)

@raises(CementRuntimeError)
@with_setup(setup_func, teardown_func)
def test_register_duplicate_handler():  
    register_handler('output', 'json', None)