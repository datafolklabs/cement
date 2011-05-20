"""ConfigObj Framework Extension for Cement."""

import os
from zope import interface
from configobj import ConfigObj
from cement.core import handler, config

class ConfigObjConfigHandler(ConfigObj):
    __handler_type__ = 'config'
    __handler_label__ = 'configobj'
    
    interface.implements(config.IConfigHandler)
    
    # We put this here because sections is a property in ConfigObj
    # and fails the invariant tests.
    sections = []
    
    def __init__(self, defaults, *args, **kw):
        """
        Take the default config dict and merge it into self.  Pass additional
        *args and **kw directly to ConfigObj.
        
        """
        ConfigObj.__init__(self, *args, **kw)
        self.merge(defaults)
        
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
        
handler.register(ConfigObjConfigHandler)