"""Tests for cement.core.backend."""

import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement.core import backend
config = {}
config['base'] = {}
config['base']['app_name'] = None
config['base']['app_module'] = None
config['base']['app_egg'] = None
config['base']['config_files'] = []
config['base']['config_source'] = ['default']
config['base']['debug'] = False
config['base']['log_handler'] = 'logging'
config['base']['config_handler'] = 'configparser'
config['base']['option_handler'] = 'default'
config['base']['command_handler'] = 'default'
config['base']['hook_handler'] = 'default'
config['base']['plugin_handler'] = 'default'
config['base']['error_handler'] = 'default'
config['log'] = {}
config['log']['file'] = None
config['log']['level'] = 'INFO'
config['log']['to_console'] = True
config['log']['max_bytes'] = None
config['log']['max_files'] = 4
config['log']['file_formatter'] = None
config['log']['console_formatter'] = None
config['log']['clear_loggers'] = True
    
def startup():
    pass

def teardown():
    pass
    
@with_setup(startup, teardown)
def test_verify_default_config():
    for section in config.keys():
        for key in config[section].keys():
            yield compare_with_default_config, section, key
        
def compare_with_default_config(section, key):
    """
    Check that the default key value matches that of the known config above.
    """
    defaults = backend.default_config()
    ok_(defaults.has_key(section))
    ok_(defaults[section].has_key(key))
    eq_(defaults[section][key], config[section][key])
    
@with_setup(startup, teardown)
def test_minimal_logger():
    log = backend.minimal_logger(__name__)
    log = backend.minimal_logger(__name__, debug=True)
    
    # set logging back to non-debug
    backend.minimal_logger(__name__, debug=False)
    pass
    
@with_setup(startup, teardown)
def test_output_buffer():
    out = backend.StdOutBuffer()
    out.write('test')
    eq_(out.buffer, 'test')
    
    err = backend.StdErrBuffer()
    err.write('test')
    eq_(err.buffer, 'test')