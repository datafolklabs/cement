
import os
import sys
from zope import interface
from cement.handlers.log import LoggingLogHandler

if sys.version_info[0] < 3:
    from ConfigParser import RawConfigParser
else:
    from configparser import RawConfigParser
    
from cement.core.exc import CementInterfaceError

log = LoggingLogHandler(__name__)

def config_invariant(obj):
    invalid = []
    for member in ['keys', 'sections', 'get', 'set', 'parse_file']:
        if not hasattr(obj, member):
            invalid.append(member)
    
    if invalid:
        raise CementInterfaceError, \
            "Invalid or Missing: %s in %s" % (invalid, obj)
                    
class IConfigHandler(interface.Interface):
    """
    This class defines the Config Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    """
    default = interface.Attribute('Default Configuration Dictionary')
    interface.invariant(config_invariant)
    
    def parse_file(file_path):
        """
        Parse config file settings from file_path.
        
        Required Arguments:
        
            file_path
                The path to the config file to parse.
                
        """

    def keys(section):
        """
        Return a list of configuration keys from `section`.
        
        Required Arguments:
        
            section
                The config [section] to pull keys from.
                
        Returns: list
        """
            
    def sections():
        """
        Return a list of configuration sections.
        
        Returns: list
                
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

                        
class ConfigParserConfigHandler(RawConfigParser):
    interface.implements(IConfigHandler)
    
    def __init__(self, default_config):
        RawConfigParser.__init__(self, default_config)
        self.add_section('base')
        
        
    def parse_files(self):
        """
        Parse config file settings from self.default_config['config_files'].
        """
        for _file in self.get('base', 'config_files'):
            self.parse_file(_file)
    
    def parse_file(self, file_path):
        """
        Parse config file settings from file_path.
        """
        if not os.path.exists(file_path):
            log.debug('%s does not exist')
            return None
            
        self.read(file_path)
    
    def has_key(self, section, key):
        return self.has_option(section, key)
     
    def keys(self, section):
        return self.options(section)
