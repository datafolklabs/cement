"""Cement methods to setup and configuring logging."""

import logging

from cement import namespaces

def setup_logging_for_plugin_provider(provider):
    """
    Setup the logging handlers for a plugin providers module name space.
    
    Required Arguments:
    
        provider
            The name of the application (module) providing the shared plugin.
    
    """
    config = namespaces['root'].config
    provider_log = logging.getLogger(provider)
    cement_log = logging.getLogger('cement')
    
    for handler in logging.getLogger('cement').handlers:
        provider_log.addHandler(handler)
    provider_log.level = cement_log.level
    
def setup_logging(clear_loggers=True, level=None, to_console=True):
    """
    Primary Cement method to setup logging.
    
    Keyword arguments:
        
        clear_loggers
            Boolean, whether to clean exiting loggers (default: True)
            
        level
            The log level (info, warn, error, debug, fatal), (default: None)
            
        to_console
            Boolean, whether or not to log to console
    
    
    Usage:
    
    .. code-block:: python
    
        from cement.core.log import setup_logging
        setup_logging()
        
    """
    config = namespaces['root'].config
    all_levels = ['INFO', 'WARN', 'ERROR', 'DEBUG', 'FATAL']
    
    # Remove any previously setup handlers from other libraries
    if clear_loggers:
        for i in logging.getLogger().handlers:
            logging.getLogger().removeHandler(i)
        for i in logging.getLogger(config['app_module']).handlers:
            logging.getLogger(config['app_module']).removeHandler(i)
        for i in logging.getLogger('cement').handlers:
            logging.getLogger('cement').removeHandler(i)
            
    app_log = logging.getLogger(config['app_module'])
    cement_log = logging.getLogger('cement')
    
    # Log level
    if config.has_key('debug') and config['debug']:
        level = 'DEBUG'
    elif level and level.upper() in all_levels:
        level = level
    elif config.has_key('log_level'):
        level = config['log_level']
    else:
        level = 'INFO'

    log_level = getattr(logging, level.upper())
    app_log.setLevel(log_level)
    cement_log.setLevel(log_level)
    
    # Console formatter    
    if to_console:
        console = logging.StreamHandler()
        if log_level == logging.DEBUG:
            console.setFormatter(logging.Formatter(
                "%(asctime)s (%(levelname)s) %(name)s : %(message)s"))
        else: 
            console.setFormatter(
                logging.Formatter("%(levelname)s: %(message)s")
                )
        console.setLevel(log_level)   
        app_log.addHandler(console)    
        cement_log.addHandler(console)
    
    # File formatter
    if config.has_key('log_file'):
        if config.has_key('log_max_bytes'):
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                config['log_file'], maxBytes=int(config['log_max_bytes']), 
                backupCount=int(config['log_max_files'])
                )
        else:
            from logging import FileHandler
            file_handler = FileHandler(config['log_file'])
            
        file_handler.setFormatter( 
            logging.Formatter("%(asctime)s (%(levelname)s) %(name)s : %(message)s")
            )
        file_handler.setLevel(log_level)   
        app_log.addHandler(file_handler)
        cement_log.addHandler(file_handler)
        
def get_logger(name):
    """
    Used throughout the application to get a logger opject with a namespace
    of 'name' (should be passed as __name__).  
    
    Arguments:
    
        name
            Name of the module calling get_logger (use __name__).
    
    Usage:
    
    .. code-block:: python
    
        from cement.core.log import get_logger
        log = get_logger(__name__)
        
    """
    return logging.getLogger(name)
    