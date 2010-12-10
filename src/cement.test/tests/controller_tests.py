"""The purpose of this module is to test controller functionality."""

from nose.tools import raises, with_setup, eq_, ok_

from cement import namespaces
from cement.core.namespace import get_config
from cement.core.controller import expose, CementController
from cement.core.controller import run_controller_command
from cement.core.testing import simulate
from cement.core.exc import CementRuntimeError, CementArgumentError

from cement_test.core.testing import setup_func, teardown_func
from cement_test.core.exc import CementTestArgumentError

config = get_config()
    
@raises(CementRuntimeError)
@with_setup(setup_func, teardown_func)
def test_bogus_output_handler():  
    simulate([__file__, 'bogus-cmd1'])

@with_setup(setup_func, teardown_func)
def test_error_handler():  
    (res, out) = run_controller_command('root', 'error', errors=[('label', 'msg')])
    eq_(res, dict(errors=[('label', 'msg')]))

@raises(CementTestArgumentError)
@with_setup(setup_func, teardown_func)
def test_default_cmd():      
    (res, out) = simulate([__file__, 'default'])

        
@raises(CementArgumentError)
@with_setup(setup_func, teardown_func)
def test_bogus_cmd():  
    simulate([__file__, 'bogus-cmd-does-not-exist'])
    
@with_setup(setup_func, teardown_func)
def test_controller_class():
    # FIXME: passing bogus cause cli_opts is actually an object, but we just
    # want to test that self.cli_opts is getting assigned
    c = CementController(cli_opts='bogus', cli_args=['a', 'b'])
    assert c.cli_opts == 'bogus', "self.cli_opts is not getting set."
    assert 'a' in c.cli_args, "self.cli_opts is not getting set."

# test for coverage
@with_setup(setup_func, teardown_func)
def test_root_cmd1_help():
    simulate([__file__, 'cmd1-help', '--debug'])
    
@with_setup(setup_func, teardown_func)
def test_get_started():
    simulate([__file__, 'get-started'])
    
@with_setup(setup_func, teardown_func)
def test_example_cmd1():
    simulate([__file__, 'example', 'cmd1'])
    
@with_setup(setup_func, teardown_func)
def test_example2_cmd1():
    simulate([__file__, 'example2', 'cmd1'])
    
@with_setup(setup_func, teardown_func)
def test_example3_cmd1():
    simulate([__file__, 'example3', 'cmd1'])

@with_setup(setup_func, teardown_func)
def test_example4_cmd1():
    simulate([__file__, 'example4', 'cmd1'])
