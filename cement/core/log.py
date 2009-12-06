"""Cement methods to setup and configuring logging."""

import logging
from logging.handlers import RotatingFileHandler

def setup_logging(config):
    """
    Primary Cement method to setup logging.
    
    Arguments:
    
    config => dict containing the applications configurations.
    """
    # remove any previously setup handlers from other libraries
    for i in logging.getLogger().handlers:
        logging.getLogger().removeHandler(i)

    log = logging.getLogger(config['app_module'])
    
    if config.has_key('debug') and config['debug']:
        log_level = logging.DEBUG
        console_formatter = logging.Formatter(
            "%(asctime)s (%(levelname)s) %(name)s : %(message)s"
            )
    else:
        log_level = logging.INFO
        console_formatter = logging.Formatter("%(message)s")
            
    if config.has_key('log_file'):
        file_handler = RotatingFileHandler(
            config['log_file'], maxBytes=512000, backupCount=4
            )
        file_handler.setLevel(log_level)
        formatter = logging.Formatter(
            "%(asctime)s (%(levelname)s) %(name)s : %(message)s"
            )
        log.addHandler(file_handler)
        file_handler.setFormatter(formatter)
    
    console = logging.StreamHandler()
    console.setLevel(log_level)
    console.setFormatter(console_formatter)
    log.addHandler(console)
    log.setLevel(log_level)
    
def get_logger(name):
    """
    Used throughout the application to get a logger opject with a namespace
    of 'name' (should be passed as __name__).  
    
    Arguments:
    
    name => name of the module calling get_logger (use __name__).
    """
    return logging.getLogger(name)