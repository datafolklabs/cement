"""The purpose of this module is to test command functionality."""

from nose.tools import raises, with_setup, eq_, ok_

from cement import namespaces
from cement.core.namespace import get_config
from cement.core.command import run_command
from cement.core.testing import simulate
from cement.core.exc import CementRuntimeError, CementArgumentError

from cement_test.core.testing import setup_func, teardown_func

config = get_config()
    
@raises(CementArgumentError)
@with_setup(setup_func, teardown_func)
def test_run_command_namespace():  
    # raises cause example is a namespace
    run_command('example')
  
@raises(CementArgumentError)
@with_setup(setup_func, teardown_func)
def test_run_command_namespace_help():  
    # raises cause example is a namespace
    run_command('example-help')
      
@with_setup(setup_func, teardown_func)
def test_run_command():  
    # raises cause example is a namespace
    run_command('cmd1')

@raises(CementArgumentError)
@with_setup(setup_func, teardown_func)
def test_run_unknown_command():  
    # raises cause blah doesn't exist
    run_command('blah')