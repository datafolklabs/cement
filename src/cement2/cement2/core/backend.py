"""Cement core backend module."""

import os
import sys
import logging

from cement2.core import exc

def defaults(app_name):
    """
    Get a standard, default config.
    
    Required Arguments:
    
        app_name
            The name of the application.  This is a single, alpha-numeric
            string (underscores allowed).
            
    Usage:
    
    .. code-block:: python
    
        from cement2.core import foundation, backend
        defaults = backend.defaults('myapp_name')
        app = foundation.lay_cement('myapp_name', defaults=defaults)
        
    """
    ok = ['_']
    for char in app_name:
        if char in ok:
            continue
            
        if not char.isalnum():
            raise exc.CementRuntimeError(
                "app_name must be alpha-numeric, or underscore."
                )
            
    # default backend configuration
    dcf = {}
    dcf['base'] = {}
    dcf['base']['app_name'] = app_name
    dcf['base']['config_files'] = [
        os.path.join('/', 'etc', app_name, '%s.conf' % app_name),
        os.path.join(os.environ['HOME'], '.%s.conf' % app_name),
        ]
    dcf['base']['config_source'] = ['defaults']
    dcf['base']['debug'] = False
    
    dcf['base']['plugins'] = []
    dcf['base']['plugin_config_dir'] = '/etc/%s/plugins.d' % app_name
    dcf['base']['plugin_bootstrap_module'] = '%s.bootstrap' % app_name
    dcf['base']['plugin_dir'] = '/usr/lib/%s/plugins' % app_name
    
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
