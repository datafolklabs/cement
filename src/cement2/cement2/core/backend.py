"""Cement core backend module."""

import sys
import logging

from cement2.core import exc

def defaults(app_name=None):
    """
    Get a standard, default config.
    
    Required Arguments:
    
        app_name
            The name of the application.
            
    """
    # default backend configuration
    dcf = {}
    dcf['base'] = {}
    dcf['base']['app_name'] = app_name
    dcf['base']['config_files'] = []
    dcf['base']['config_source'] = ['defaults']
    dcf['base']['debug'] = False
    dcf['base']['plugins'] = []
    dcf['base']['plugin_config_dir'] = None
    
    # FIX ME: need to implement
    dcf['base']['plugin_bootstrap_module'] = '%s.bootstrap' % app_name
    dcf['base']['plugin_directory'] = '/usr/lib/%s/plugins' % app_name
    
    # FIX ME: Also, Should there be a [plugins] block?
    
    # default extensions
    dcf['base']['extensions'] = [  
        'cement2.ext.ext_cement_output',
        'cement2.ext.ext_cement_plugin',
        'cement2.ext.ext_configparser', 
        'cement2.ext.ext_logging', 
        'cement2.ext.ext_argparse',
        ]
    
    # default handlers
    dcf['base']['config_handler'] = 'configparser'
    dcf['base']['log_handler'] = 'logging'
    dcf['base']['arg_handler'] = 'argparse'
    dcf['base']['plugin_handler'] = 'cement'
    dcf['base']['extension_handler'] = 'cement'
    dcf['base']['output_handler'] = 'cement'
    dcf['base']['controller_handler'] = 'base'
    

    # default application configuration
    #dcf['log'] = {}
    #dcf['log']['file'] = None
    #dcf['log']['level'] = 'INFO'
    #dcf['log']['to_console'] = True
    #dcf['log']['rotate'] = False
    #dcf['log']['max_bytes'] = 512000
    #dcf['log']['max_files'] = 4
    #dcf['log']['file_formatter'] = None
    #dcf['log']['console_formatter'] = None
    #dcf['log']['clear_loggers'] = True
    return dcf

def minimal_logger(name, debug=False):
    """
    Setup just enough for cement to be able to do debug logging.
    """
                
    log = logging.getLogger(name)
    formatter = logging.Formatter(
                "%(asctime)s (%(levelname)s) %(name)s : %(message)s")
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.INFO)   
    log.setLevel(logging.INFO)
        
    # FIX ME: really don't want to hard check sys.argv like this but can't
    # figure any better way get logging started (only for debug) before the
    # app logging is setup.
    if '--debug' in sys.argv or debug:
        console.setLevel(logging.DEBUG)   
        log.setLevel(logging.DEBUG)
        
    log.addHandler(console)
    return log
        
# global handlers dict
handlers = {}

# global hooks dict
hooks = {}

# Save original stdout/stderr for supressing output.  This is actually reset
# in foundation.lay_cement before nullifying output, but we set it here
# just for a default.
SAVED_STDOUT = sys.stdout
SAVED_STDERR = sys.stderr
