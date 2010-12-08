"""The purpose of this module is to test namespace functionality."""

from nose.tools import raises, with_setup, eq_, ok_

from cement import namespaces
from cement.core.namespace import get_config, get_namespace, define_namespace
from cement.core.namespace import CementNamespace
from cement.core.testing import simulate
from cement.core.handler import get_handler, define_handler, register_handler
from cement.core.exc import CementRuntimeError

from cement_test.core.testing import setup_func, teardown_func

config = get_config()
    
@with_setup(setup_func, teardown_func)
def test_get_handler():  
    root = get_namespace('root')

@raises(CementRuntimeError)
@with_setup(setup_func, teardown_func)
def test_get_bogus_handler():  
    root = get_namespace('bogus_namespace')

@raises(CementRuntimeError)
@with_setup(setup_func, teardown_func)
def test_get_bogus_config():  
    _cnf = get_config('bogus_namespace')

@raises(CementRuntimeError)
@with_setup(setup_func, teardown_func)
def test_define_duplicate_namespace():  
    bogus = CementNamespace(
        label='root', 
        controller='RootController',
        version='1.0', 
        required_api='xxxx', 
        provider='cement_test')
    define_namespace('root', bogus)

@raises(CementRuntimeError)
@with_setup(setup_func, teardown_func)
def test_define_broken_namespace():  
    bogus = CementNamespace(
        label='root', 
        controller='RootController')