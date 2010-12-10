
"""The purpose of this module is to test core functionality."""

import jsonpickle
from nose.tools import raises, with_setup, eq_, ok_

from cement import namespaces
from cement.core.namespace import get_config
from cement.core.testing import simulate
from cement.core.exc import CementArgumentError
from cement_test.core.testing import setup_func, teardown_func

config = get_config()

@with_setup(setup_func, teardown_func)
def test_json_output_handler():  
    # bit of a hack, but this is handled before the nose stuff... so, have to
    # redo it here to make it work
    orig = namespaces['root'].config['output_handler_override']
    namespaces['root'].config['output_handler_override'] = 'json'
    namespaces['root'].config['show_plugin_load'] = False
    
    (res, out_txt) = simulate([__file__, 'cmd1', '--json'])
    res_json = jsonpickle.decode(out_txt)
    eq_(res_json['items'][0], 'one')
    
    namespaces['root'].config['output_handler_override'] = orig
    
@raises(CementArgumentError)
@with_setup(setup_func, teardown_func)
def test_root_command_that_does_not_exist():  
    (res, out_txt) = simulate([__file__, 'non_existent'])
    
@with_setup(setup_func, teardown_func)
def test_example_namespace():  
    (res, out_txt) = simulate([__file__, 'example', 'cmd1'])
    

        
