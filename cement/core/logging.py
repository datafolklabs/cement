#!/usr/bin/env python
#
# This file is a part of the Cement package.  Please see the
# README and LICENSE files includes with this software.
#

import sys,os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(config):
    # remove any previously setup handlers from other libraries
    for i in logging.getLogger().handlers:
        logging.getLogger().removeHandler(i)
    
    log = logging.getLogger(config['app_name'])

    config['debug']
    if config['debug']:
        log_level = logging.DEBUG
        console_formatter = logging.Formatter(
            "%(asctime)s (%(levelname)s) %(name)s : %(message)s"
            )
    else:
        log_level = logging.INFO
        console_formatter = logging.Formatter(
            "(%(levelname)s) : %(message)s"
            )
            
    if config['log_file']:
        file = logging.handlers.RotatingFileHandler(
            config['log_file'], maxBytes=512000, backupCount=4
            )
        file.setLevel(log_level)
        formatter = logging.Formatter(
            "%(asctime)s (%(levelname)s) %(name)s : %(message)s"
            )
        log.addHandler(file)
        file.setFormatter(formatter)
    
    console = logging.StreamHandler()
    console.setLevel(log_level)
    console.setFormatter(console_formatter)
    log.addHandler(console)
    log.setLevel(log_level)
    
def get_logger(name):
    return logging.getLogger(name)