"""ConfigObj Framework Extension for Cement."""

import os
from configobj import ConfigObj

from cement2.core import handler, config, backend

Log = backend.minimal_logger(__name__)

class ConfigObjConfigHandler(ConfigObj):
    """
    This class implements the :ref:`IConfig <cement2.core.config>` 
    interface, and sub-classes from `configobj.ConfigObj <http://www.voidspace.org.uk/python/configobj.html>`_,
    which is an external library and not included with Python. Please 
    reference the configobj documentation for full usage of the class.

    Arguments and Keyword arguments are passed directly to ConfigObj
    on initialization.
    """
    class meta:
        interface = config.IConfig
        label = 'configobj'
        
    def __init__(self, *args, **kw):
        super(ConfigObjConfigHandler, self).__init__(*args, **kw)
        
    def setup(self, defaults):
        """
        Sets up the class for use by the framework, then calls self.merge() 
        with the passed defaults.  
        
        Required Arguments:
        
            defaults
                The application default config dictionary.  This is *not* a 
                config object, but rather a dictionary which should be 
                obvious because the config handler implementation is what
                provides the application config object.
                
        Returns: n/a
        
        """
        self.merge(defaults)
    
    def get_sections(self):
        """
        Return a list of [section] that exist in the configuration.
        
        """
        return self.sections
            
    def parse_file(self, file_path):
        """
        Parse config file settings from file_path, overwriting existing 
        config settings.  If the file does not exist, returns False.
        
        Required Arguments:
            
            file_path
                The file system path to the configuration file.
                
        
        Returns: Bool
        
        """
        if os.path.exists(file_path):
            _c = ConfigObj(file_path)
            self.merge(_c)
            return True
        else:
            Log.debug("file '%s' does not exist, skipping..." % \
                      file_path)
            return False
    
    def has_key(self, section, key):
        """
        Check if a configuration section has a given key.
        
        Required Arguments:
        
            section
                A configuration [section].
                
            key
                The key to check for under section.
        
        Returns: Bool
        
        """
        if self.has_section(section):
            return self[section].has_key(key)
        else:
            return False
     
    def keys(self, section):
        """
        Return a list of keys for a given section.
        
        Required Arguments:
        
            section 
                The configuration [section].
                
        """
        return self[section].keys()

    def get(self, section, key):
        """
        Get a value for a given key under section.
        
        Required Arguments:
        
            section
                The configuration [section].
        
            key
                The configuration key under the section.
        
        
        Returns: unknown (the value of the key)
        
        """
        return self[section][key]
    
    def set(self, section, key, value):
        """
        Set a configuration key value under [section].
        
        Required Arguments:
        
            section
                The configuration [section].
                
            key
                The configuration key under the section.
                
            value
                The value to set the key to.
        
                
        """
        self[section][key] = value
        
    def has_section(self, section):
        """
        Return True/False whether the configuration [section] exists.
        
        Required Arguments:
        
            section
                The section to check for.
        
        Returns: Bool        
        
        """
        if section in self.get_sections():
            return True
        else:
            return False
            
    def add_section(self, section):
        """
        Add a section to the configuration.
        
        Required Arguments:
        
            section
                The configuration [section] to add.
                
        """
        if not self.has_section(section):
            self[section] = dict()

handler.register(ConfigObjConfigHandler)