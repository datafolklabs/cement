"""The purpose of this module is to test hook functionality."""

from nose.tools import raises, with_setup, eq_, ok_

from cement import hooks
from cement.core.hook import run_hooks, define_hook, register_hook
from cement.core.namespace import get_config
from cement.core.testing import simulate
from cement.core.exc import CementRuntimeError

from cement_test.core.testing import setup_func, teardown_func
from cement_test.core.exc import CementTestArgumentError, CementTestRuntimeError

config = get_config()
    
@with_setup(setup_func, teardown_func)
def test_my_example_hook():  
    ok_(hooks.has_key('my_example_hook'))
    
    hook_results = []
    
    for res in run_hooks('my_example_hook'):
        hook_results.append(res)
    
    # return results are the weight of the hook and should be in numerical
    # order
    res = hook_results = [-100, 0, 99]
    ok_(res)

@raises(CementRuntimeError)
@with_setup(setup_func, teardown_func)
def test_define_duplicate_hook():
    define_hook('my_example_hook')

@with_setup(setup_func, teardown_func)
@register_hook(name='bogus_hook_name')
def test_register_duplicate_hook():
    # this doesn't raise, just testing for coverage
    pass

@raises(CementRuntimeError)
@with_setup(setup_func, teardown_func)
def test_run_hook_that_does_not_exist():
    for res in run_hooks('bogus_hook'):
        pass

