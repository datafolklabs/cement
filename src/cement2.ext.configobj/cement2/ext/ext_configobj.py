"""ConfigObj Framework Extension for Cement."""

import os
from zope import interface
from configobj import ConfigObj

from cement2.core import handler, config

class ConfigObjConfigHandler(ConfigObj):
    interface.implements(config.IConfigHandler)
    class meta:
        type = 'config'
        label = 'configobj'
        
    def __init__(self, *args, **kw):
        """
        This is an implementation of the IConfigHandler interface, which
        uses the ConfigObj library.  We subclass from ConfigObj, and
        pass *args, **kwargs directly to it.
        """
        super(ConfigObjConfigHandler, self).__init__(*args, **kw)
        
    def setup(self, defaults):
        """
        Take the default config dict and merge it into self.
        
        """
        self.merge(defaults)
    
    def get_sections(self):
        # ConfigObj sections is a list (not a function)
        return self.sections
            
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
        
    def has_section(self, section):
        if section in self.get_sections():
            return True
        else:
            return False
            
    def add_section(self, section):
        if not self.has_section(section):
            self[section] = dict()
            
handler.register(ConfigObjConfigHandler)