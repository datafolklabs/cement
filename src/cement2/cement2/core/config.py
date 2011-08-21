"""Cement core config module."""

from cement2.core import exc, backend, interface

def config_validator(klass, obj):
    members = [
        'setup',
        'keys', 
        'has_key',
        'get_sections', 
        'get', 
        'set', 
        'parse_file', 
        'merge',
        'add_section',
        'has_section',
        ]
    interface.validate(IConfig, obj, members)
    
class IConfig(interface.Interface):
    """
    This class defines the Config Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    All implementations must provide sane 'default' functionality when 
    instantiated with no arguments.  Meaning, it can and should accept 
    optional parameters that alter how it functions, but can not require
    any parameters.  When the framework first initializes handlers it does
    not pass anything too them, though a handler can be instantiated first
    (with or without parameters) and then passed to 'lay_cement()' already
    instantiated.
    
    Implementations do *not* subclass from interfaces.
    
    """
    class imeta:
        label = 'config'
        validator = config_validator
    
    # Must be provided by the implementation
    meta = interface.Attribute('Handler meta-data')
            
    def setup(defaults):
        """
        The setup function is called during application initialization and
        must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.
        
        Required Arguments:
        
            defaults
                The application default config dictionary.  This is *not* a 
                config object, but rather a dictionary which should be 
                obvious because the config handler implementation is what
                provides the application config object.
                
        Returns: n/a
        
        """

    def parse_file(file_path):
        """
        Parse config file settings from file_path.  Returns True if the file
        existed, and was parsed successfully.  Returns False otherwise.
        
        Required Arguments:
        
            file_path
                The path to the config file to parse.
                
        Returns: boolean
        
        """

    def keys(section):
        """
        Return a list of configuration keys from `section`.
        
        Required Arguments:
        
            section
                The config [section] to pull keys from.
                
        Returns: list
        
        """
            
    def get_sections():
        """
        Return a list of configuration sections.
        
        Returns: list
                
        """
          
    def add_section():
        """
        Add a new section if it doesn't exist.
        
        Returns: None
        
        """ 
        
    def get(section, key):
        """
        Return a configuration value based on [section][key].  The return
        value type is unknown.
        
        Required Arguments:
        
            section
                The [section] of the configuration to pull key value from.
            
            key
                The configuration key to get the value from.
                
        Returns: unknown
        
        """
            
    def set(section, key, value):
        """
        Set a configuration value based at [section][key].
        
        Required Arguments:
        
            section
                The [section] of the configuration to pull key value from.
        
            key
                The configuration key to set the value at.
            
            value
                The value to set.
        
        """

    def merge(dict_obj):
        """
        Merges a dict object into the configuration.
        """
    
    def has_section(section):
        """
        Returns whether or not the section exists.
        
        Returns: bool
        
        """
        
                        
