"""ConfigParser Framework Extension Library."""
        
import os
import sys
if sys.version_info[0] < 3:
    from ConfigParser import RawConfigParser # pragma: no cover
else:
    from configparser import RawConfigParser # pragma: no cover

from ..core import backend, config

Log = backend.minimal_logger(__name__)

class ConfigParserConfigHandler(config.CementConfigHandler, RawConfigParser):
    """
    This class is an implementation of the :ref:`IConfig <cement2.core.config>` 
    interface.  It handles configuration file parsing and the like by 
    sub-classing from the standard `ConfigParser <http://docs.python.org/library/configparser.html>`_ 
    library.  Please see the ConfigParser documentation for full usage of the
    class.
    
    Additional arguments and keyword arguments are passed directly to 
    RawConfigParser on initialization.
    """
    class Meta:
        interface = config.IConfig
        label = 'configparser'
    
    def __init__(self, *args, **kw):
        # ConfigParser is not a new style object, so you can't call super()
        # super(ConfigParserConfigHandler, self).__init__(*args, **kw)
        RawConfigParser.__init__(self, *args, **kw)
        super(ConfigParserConfigHandler, self).__init__(*args, **kw)
        self.app = None
        
    def merge(self, dict_obj, override=True):
        """
        Merge a dictionary into our config.  If override is True then 
        existing config values are overridden by those passed in.
        
        Required Arguments:
        
            dict_obj
                A dictionary of configuration keys/values to merge into our
                existing config (self).
            
        Optional Arguments:
        
            override
                Whether or not to override existing values in the config.
                Defaults: True.
                
        
        Returns: None
        
        """
        for section in list(dict_obj.keys()):
            if type(dict_obj[section]) == dict:
                if not section in self.get_sections():
                    self.add_section(section)
                
                for key in list(dict_obj[section].keys()):
                    if override:
                        self.set(section, key, dict_obj[section][key])
                    else:
                        # only set it if the key doesn't exist
                        if not self.has_key(section, key):
                            self.set(section, key, dict_obj[section][key])
                            
                # we don't support nested config blocks, so no need to go 
                # further down to more nested dicts.
                
    def parse_file(self, file_path):
        """
        Parse config file settings from file_path, overwriting existing 
        config settings.  If the file does not exist, returns False.
        
        Required Arguments:
            
            file_path
                The file system path to the configuration file.
                
        
        Returns: Bool
        
        """
        file_path = os.path.abspath(os.path.expanduser(file_path))
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
        """
        Return a list of configuration sections or [blocks].
        
        Returns: list
        
        """
        return self.sections()
    
    def get_section_dict(self, section):
        """
        Return a dict representation of a section.
        
        Required Arguments:
        
            section:
                The section of the configuration.  I.e. [block_section]
                
        """
        dict_obj = dict()
        for key in self.keys(section):
            dict_obj[key] = self.get(section, key)
        return dict_obj
        