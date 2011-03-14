
import os
import sys
from zope import interface
from cement.handlers.log import LoggingLogHandler

if sys.version_info[0] < 3:
    from ConfigParser import RawConfigParser
    DICT_TYPE = dict
else:
    from configparser import RawConfigParser
    DICT_TYPE = collections.OrderedDict
    
from cement.core.backend import handlers
from cement.core.exc import CementInterfaceError
from cement.core.handler import validate_handler_registration

log = LoggingLogHandler(__name__)

def config_invariant(obj):
    invalid = []
    members = [
        'keys', 
        'has_key',
        'sections', 
        'get', 
        'set', 
        'parse_file', 
        'merge',
        '__handler_label__',
        '__handler_type__',
        ]
        
    for member in members:
        if not hasattr(obj, member):
            invalid.append(member)
    
    if invalid:
        raise CementInterfaceError, \
            "Invalid or missing: %s in %s" % (invalid, obj)
    
class IConfigHandler(interface.Interface):
    """
    This class defines the Config Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    """
    # internal mechanism for handler registration
    __handler_type__ = interface.Attribute('Handler Type Identifier')
    __handler_label__ = interface.Attribute('Handler Label Identifier')
    interface.invariant(config_invariant)
    
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

    def merge(dict_obj):
        """
        Merges a dict object into the configuration.
        """
                        
class ConfigParserConfigHandler(RawConfigParser):
    __handler_label__ = 'configparser'
    __handler_type__ = 'config'
    interface.implements(IConfigHandler)
    
    def __init__(self, defaults={}, dict_type=DICT_TYPE, allow_no_value=False):
        RawConfigParser.__init__(self, defaults, dict_type, allow_no_value)

    def merge(self, dict_obj):
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
            log.debug("file '%s' does not exist, skipping..." % \
                      file_path)
            return False
     
    def keys(self, section):
        return self.options(section)

    def has_key(self, section, key):
        if key in self.options(section):
            return True
        else:
            return False
            
from configobj import ConfigObj
class ConfigObjConfigHandler(ConfigObj):
    __handler_type__ = 'config'
    __handler_label__ = 'configobj'
    interface.implements(IConfigHandler)
    sections = []
    
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
            log.debug("file '%s' does not exist, skipping..." % \
                      file_path)
            return False
    
    def has_key(self, section, key):
        return self[section].has_key(key)
     
    def keys(self, section):
        return self[section].keys()

    def get(self, section, key):
        return self[section][key]
    
    def set(self, section, key, value):
        self[section][key] = value
        
