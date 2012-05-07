"""Cement core config module."""

from ..core import exc, backend, interface, handler

def config_validator(klass, obj):
    """Validates a handler implementation against the IConfig interface."""
    members = [
        '_setup',
        'keys', 
        'has_key',
        'get_sections', 
        'get_section_dict',
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
    (with or without parameters) and then passed to 'CementApp()' already
    instantiated.
    
    Implementations do *not* subclass from interfaces.
    
    Usage:
    
    .. code-block:: python
    
        from cement2.core import config
        
        class MyConfigHandler(config.CementConfigHandler):
            class Meta:
                interface = config.IConfig
                label = 'my_config_handler'
            ...
            
    """
    class IMeta:
        label = 'config'
        validator = config_validator
    
    # Must be provided by the implementation
    Meta = interface.Attribute('Handler Meta-data')
            
    def _setup(app_obj):
        """
        The _setup function is called during application initialization and
        must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.
        
        Required Arguments:
        
            app_obj
                The application object. 
                                
        Returns: n/a
        
        """

    def parse_file(file_path):
        """
        Parse config file settings from file_path.  Returns True if the file
        existed, and was parsed successfully.  Returns False otherwise.
        
        Required Arguments:
        
            file_path
                The path to the config file to parse.
                
        Return: boolean
        
        """

    def keys(section):
        """
        Return a list of configuration keys from `section`.
        
        Required Arguments:
        
            section
                The config [section] to pull keys from.
                
        Return: list
        
        """
            
    def get_sections():
        """
        Return a list of configuration sections.  These are designated by a
        [block] label in a config file.
        
        Return: list
                
        """
        
    def get_section_dict(section):
        """
        Return a dict of configuration parameters for [section].
        
        Required Arguments:
        
            section
                The config [section] to generate a dict from (using that 
                sections keys).
                
        Return: dict
                
        """
          
    def add_section(section):
        """
        Add a new section if it doesn't exist.
        
        Required Arguments:
        
            section
                The [section] label to create.
                
        Return: None
        
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
                
        Return: unknown
        
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
        
        Return: None
        """

    def merge(dict_obj, override=True):
        """
        Merges a dict object into the configuration.
        
        Required Arguments:
        
            dict_obj
                The dict to merge into the config
                
        Optional Arguments:
        
            override 
                Whether to override existing values.  Default: True
                
        Return: None
        """
    
    def has_section(section):
        """
        Returns whether or not the section exists.
        
        Return: bool
        
        """
        
class CementConfigHandler(handler.CementBaseHandler):
    """
    Base class that all Config Handlers should sub-class from.
    
    """
    class Meta:
        interface = IConfig
        
    def __init__(self, *args, **kw):
        super(CementConfigHandler, self).__init__(*args, **kw)              
