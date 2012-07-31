"""Cement core backend module."""

import os
import sys
import logging

from ..core import exc

def defaults(*sections):
    """
    Returns a standard dictionary object to use for application defaults.
    If sections are given, it will create a nested dict for each section name.
    
    :arg sections: Section keys to create nested dictionaries for.
    :returns: Dictionary of nested dictionaries (sections)
    :rtype: dict
    
    .. code-block:: python
    
        from cement.core import foundation, backend
        
        defaults = backend.defaults('myapp', 'section2', 'section3')
        defaults['myapp']['debug'] = False
        defaults['section2']['foo'] = 'bar
        defaults['section3']['foo2'] = 'bar2'
        
        app = foundation.CementApp('myapp', config_defaults=defaults)
    
    """        
    defaults = dict()
    for section in sections:
        defaults[section] = dict()
    return defaults

def minimal_logger(name, debug=False):
    """
    Setup just enough for cement to be able to do debug logging.  This is the
    logger used by the Cement framework, which is setup and accessed before
    the application is functional (and more importantly before the 
    applications log handler is usable).
    
    :param name: The logging namespace.  This is generally '__name__' or 
        anything you want.
    :param debug: Toggle debug output. Default: False
    :type debug: boolean        
    :returns: Logger object

    .. code-block:: python
        
        from cement.core import backend
        LOG = backend.minimal_logger('cement')
        LOG.debug('This is a debug message')
        
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
# in foundation.CementApp.lay_cement() before nullifying output, but we set 
# it here just for a default.
SAVED_STDOUT = sys.stdout
SAVED_STDERR = sys.stderr
