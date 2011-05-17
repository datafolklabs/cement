"""ConfigObj Framework Extension for Cement."""

import os
from zope import interface
from configobj import ConfigObj
from cement.core.handler import register_handler
from cement.core.config import IConfigHandler
#from cement.core.log import get_logger

#log = get_logger(__name__)

class ConfigObjConfigHandler(ConfigObj):
    __handler_type__ = 'config'
    __handler_label__ = 'configobj'
    
    interface.implements(IConfigHandler)
    
    # We put this here because sections is a property in ConfigObj
    # and fails the invariant tests.
    sections = []
    
    def __cement_init__(self, config):
        """
        Take the default config dict and merge it into self.
        
        """
        self.merge(config)
        
    def parse_file(self, file_path):
        """
        Parse config file settings from file_path, overwriting existing 
        config settings.
        """
        if os.path.exists(file_path):
            _c = ConfigObj(file_path)
            self.merge(_c)
            return True
        else:
            #log.debug("file '%s' does not exist, skipping..." % \
            #          file_path)
            return False
    
    def has_key(self, section, key):
        return self[section].has_key(key)
     
    def keys(self, section):
        return self[section].keys()

    def get(self, section, key):
        return self[section][key]
    
    def set(self, section, key, value):
        self[section][key] = value
        
register_handler(ConfigObjConfigHandler)