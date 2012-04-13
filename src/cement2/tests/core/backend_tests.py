"""Tests for cement.core.backend."""

import os
import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import backend, exc
from cement2 import test_helper as _t
_t.prep()

label = 'helloworld'
config = {}
config['base'] = {}
config['base']['label'] = label
config['base']['config_files'] = [
    os.path.join('/', 'etc', label, '%s.conf' % label),
    os.path.join(os.environ['HOME'], '.%s.conf' % label),
    ]
config['base']['config_source'] = ['defaults']
config['base']['debug'] = False
config['base']['plugins'] = []
config['base']['plugin_config_dir'] = '/etc/helloworld/plugins.d'
config['base']['plugin_bootstrap_module'] = '%s.bootstrap' % label
config['base']['plugin_dir'] = '/usr/lib/%s/plugins' % label
config['base']['config_handler'] = 'configparser'
config['base']['log_handler'] = 'logging'
config['base']['arg_handler'] = 'argparse'
config['base']['plugin_handler'] = 'cement'
config['base']['extension_handler'] = 'cement'
config['base']['output_handler'] = 'null'
config['base']['extensions'] = [  
    'cement2.ext.ext_nulloutput',
    'cement2.ext.ext_plugin',
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
    defaults = backend.defaults(label='helloworld')
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
    defaults = backend.defaults('my_label')
    
@raises(exc.CementRuntimeError)
def test_bad_appname_chars():
    defaults = backend.defaults('my-app-name')
    _eq(defaults['label'], 'my_label')
