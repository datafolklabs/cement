"""ConfigParser framework extension."""

import os
import sys
from zope import interface

if sys.version_info[0] < 3:
    from ConfigParser import RawConfigParser
else:
    from configparser import RawConfigParser

from cement2.core import backend, handler
from cement2.core.config import IConfigHandler

Log = backend.minimal_logger(__name__)

class ConfigParserConfigHandler(RawConfigParser):
    """
    This class is an implementation of the IConfigHandler interface.  It
    handles configuration file parsing and the like using the standard
    ConfigParser library.
    
    """
    interface.implements(IConfigHandler)
    class meta:
        type = 'config'
        label = 'configparser'
        
    def setup(self, defaults, *args, **kw):
        """
        Take the default config dict and merge it into self.
        
        """
        RawConfigParser.__init__(self, *args, **kw)
        self.merge(defaults)
        
    def merge(self, dict_obj):
        """
        Merge a dictionary into our config.
        
        """
        for section in dict_obj.keys():
            if type(dict_obj[section]) == dict:
                if not section in self.sections():
                    self.add_section(section)
                
                for key in dict_obj[section].keys():
                    self.set(section, key, dict_obj[section][key])
                # we don't support nested config blocks, so no need to go 
                # further down to more nested dicts.
                
    def parse_file(self, file_path):
        """
        Parse config file settings from file_path, overwriting existing 
        config settings.
        """
        if os.path.exists(file_path):
            self.read(file_path)
            return True
        else:
            Log.debug("config file '%s' does not exist, skipping..." % \
                      file_path)
            return False
     
    def keys(self, section):
        """
        Return a list of keys within 'section'.
        
        Required Arguments:
        
            section
                The config section (I.e. [block_section]).
        
        Returns: list
        
        """
        return self.options(section)

    def has_key(self, section, key):
        """
        Return whether or not a 'section' has the given 'key'.
        
        Required Arguments:
        
            section
                The section of the configuration. I.e. [block_section].
            
            key
                The key within 'section'.
        
        Returns: bool
        
        """
        if key in self.options(section):
            return True
        else:
            return False
     
    def get_sections(self):
        return self.sections()
            
handler.register(ConfigParserConfigHandler)
