"""The purpose of this module is to test view functionality."""

from nose.tools import raises, with_setup, eq_, ok_

from cement import namespaces
from cement.core.namespace import get_config
from cement.core.controller import expose
from cement.core.testing import simulate
from cement.core.exc import CementRuntimeError

from cement_test.core.testing import setup_func, teardown_func

config = get_config()
    
@with_setup(setup_func, teardown_func)
def test_genshi():  
    orig = namespaces['root'].config['output_handler_override']
    namespaces['root'].config['output_handler_override'] = 'genshi'
    
    (res, out) = simulate([__file__, 'cmd1'])
    eq_(out, 'one two three ')
    namespaces['root'].config['output_handler_override'] = orig

@with_setup(setup_func, teardown_func)
def test_output_file():  
    (res, out) = simulate([__file__, 'send-to-file'])

@with_setup(setup_func, teardown_func)
def test_log_to_console():  
    namespaces['root'].config['log_to_console'] = True
    (res, out) = simulate([__file__, 'cmd1'])
    namespaces['root'].config['log_to_console'] = False
