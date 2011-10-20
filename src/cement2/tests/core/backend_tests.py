"""Tests for cement.core.backend."""

import os
import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import backend, exc

app_name = 'helloworld'
config = {}
config['base'] = {}
config['base']['app_name'] = app_name
config['base']['config_files'] = [
    os.path.join('/', 'etc', app_name, '%s.conf' % app_name),
    os.path.join(os.environ['HOME'], '.%s.conf' % app_name),
    ]
config['base']['config_source'] = ['defaults']
config['base']['debug'] = False
config['base']['plugins'] = []
config['base']['plugin_config_dir'] = '/etc/helloworld/plugins.d'
config['base']['plugin_bootstrap_module'] = '%s.bootstrap' % app_name
config['base']['plugin_dir'] = '/usr/lib/%s/plugins' % app_name
config['base']['config_handler'] = 'configparser'
config['base']['log_handler'] = 'logging'
config['base']['arg_handler'] = 'argparse'
config['base']['plugin_handler'] = 'cement'
config['base']['extension_handler'] = 'cement'
config['base']['output_handler'] = 'cement'
config['base']['extensions'] = [  
    'cement2.ext.ext_cement_output',
    'cement2.ext.ext_cement_plugin',
    'cement2.ext.ext_configparser', 
    'cement2.ext.ext_logging', 
    'cement2.ext.ext_argparse',
    ]
    
def startup():
    pass

def teardown():
    pass
    
@with_setup(startup, teardown)
def test_verify_defaults():
    for section in list(config.keys()):
        for key in list(config[section].keys()):
            yield compare_with_defaults, section, key
        
def compare_with_defaults(section, key):
    """
    Check that the default key value matches that of the known config above.
    """
    defaults = backend.defaults(app_name='helloworld')
    ok_(section in defaults)
    ok_(key in defaults[section])
    eq_(defaults[section][key], config[section][key])
    
@with_setup(startup, teardown)
def test_minimal_logger():
    log = backend.minimal_logger(__name__)
    log = backend.minimal_logger(__name__, debug=True)
    
    # set logging back to non-debug
    backend.minimal_logger(__name__, debug=False)
    pass

def test_appname_underscore():
    defaults = backend.defaults('my_app_name')
    
@raises(exc.CementRuntimeError)
def test_bad_appname_chars():
    defaults = backend.defaults('my-app-name')
    _eq(defaults['app_name'], 'my_app_name')
