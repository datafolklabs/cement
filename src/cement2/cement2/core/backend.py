"""Cement core backend module."""

import os
import sys
import logging

from cement2.core import exc

def defaults():
    """
    Get a standard, default config dictionary for the [base] section.
    
    Usage:
    
    .. code-block:: python
    
        from cement2.core import backend, foundation
        
        defaults = backend.defaults()
        defaults['base']['debug'] = False
        defaults['base']['some_param'] = 'some_value'
        
        app = foundation.CementApp('myapp', defaults=defaults)
        
    """        
    dcf = {}
    dcf['base'] = {}
    dcf['base']['debug'] = False  
    
    # FIX ME: This should go under a [plugin] block handled by the plugin
    # handler  
    #dcf['base']['plugin_config_dir'] = '/etc/%s/plugins.d' % label
    #dcf['base']['plugin_bootstrap_module'] = '%s.bootstrap' % label
    #dcf['base']['plugin_dir'] = '/usr/lib/%s/plugins' % label

    # default extensions
    #dcf['base']['extensions'] = [  
    #    'cement2.ext.ext_nulloutput',
    #    'cement2.ext.ext_plugin',
    #    'cement2.ext.ext_configparser', 
    #    'cement2.ext.ext_logging', 
    #    'cement2.ext.ext_argparse',
    #    ]
    
    # default handlers
    #dcf['base']['config_handler'] = 'configparser'
    #dcf['base']['log_handler'] = 'logging'
    #dcf['base']['arg_handler'] = 'argparse'
    #dcf['base']['plugin_handler'] = 'cement'
    #dcf['base']['extension_handler'] = 'cement'
    #dcf['base']['output_handler'] = 'null'
    #dcf['base']['controller_handler'] = 'base'
    
    return dcf

def minimal_logger(name, debug=False):
    """
    Setup just enough for cement to be able to do debug logging.  This is the
    logger used by the Cement framework, which is setup and accessed before
    the application is functional (and more importantly before the 
    applications log handler is usable).
    
    Usage:
    
    .. code-block:: python
    
        from cement2.core import backend
        Log = backend.minimal_logger('cement')
        Log.debug('This is a debug message')
        
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
