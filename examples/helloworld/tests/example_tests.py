"""
The purpose of this module is to test application functionality.  It is here
as an example of how one might perform nose testing on an application built
on top of the Cement Framework.  It is not a fully comprehensive test, of the
application... and needs to be expanded as the application grows.

The initial file loaded by nose runs the application.  Additional calls are
then made via the 'simulate' function rather than needing to reload the 
application for every test.
"""

import os
from nose.tools import raises, with_setup, eq_, ok_

from cement import namespaces
from cement.core.namespace import get_config
from cement.core.testing import simulate
from cement.core.exc import CementRuntimeError

from helloworld.core.exc import HelloworldArgumentError

config = get_config()
    
def setup_func():
    """Setup operations before every test."""
    pass

def teardown_func():
    """Teardown operations after every test."""
    pass
    
@with_setup(setup_func, teardown_func)
def test_cmd1_output():  
    # Simulate returns the result dictionary, and the render output when
    # running the controller command.  This can be used to validate that the
    # command ran successfully.
    (res_dict, output_txt) =  simulate([__file__, 'cmd1'])
    
    # You can test that the rendered output is what we expected
    eq_(output_txt, 'bar')
    
    # You can test values in the result dictionary directly
    ok_(res_dict['foo'])
    
@raises(HelloworldArgumentError)
@with_setup(setup_func, teardown_func)
def test_default_cmd():
    # The default action is to raise an application error if an unknown 
    # command is called.  This is how we test that the exception is raised.
    simulate([__file__, 'default'])

@with_setup(setup_func, teardown_func)
def test_config_cli_options():
    # Using the test configuration file in ./config we can test config options
    # this way.  We are also using the example plugin for this test
    
    # First it is set by what is in the config file
    eq_(config['example']['foo'], 'some value')
    
    # Then overridden by cli_opts
    simulate([__file__, 'example', 'ex1', '--foo=bar'])
    
    # now we validate that the config option was set by the cli_opt --foo
    eq_(config['example']['foo'], 'bar')
