"""Cement core config module."""

import os
import sys
from zope import interface

if sys.version_info[0] < 3:
    from ConfigParser import RawConfigParser
else:
    from configparser import RawConfigParser

from cement2.core import backend, exc

Log = backend.minimal_logger(__name__)

def config_handler_invariant(obj):
    invalid = []
    members = [
        '__init__',
        '__handler_label__',
        '__handler_type__',
        'setup',
        'keys', 
        'has_key',
        'sections', 
        'get', 
        'set', 
        'parse_file', 
        'merge',
        ]
        
    for member in members:
        if not hasattr(obj, member):
            invalid.append(member)
    
    if invalid:
        raise exc.CementInterfaceError, \
            "Invalid or missing: %s in %s" % (invalid, obj)
    
class IConfigHandler(interface.Interface):
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
    
    """
    # internal mechanism for handler registration
    __handler_type__ = interface.Attribute('Handler Type Identifier')
    __handler_label__ = interface.Attribute('Handler Label Identifier')
    interface.invariant(config_handler_invariant)
            
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
    
    def setup(self, defaults, *args, **kw):
        """
        Take the default config dict and merge it into self.
        
        """
        RawConfigParser.__init__(self, *args, **kw)
        self.merge(defaults)
        
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
            Log.debug("config file '%s' does not exist, skipping..." % \
                      file_path)
            return False
     
    def keys(self, section):
        return self.options(section)

    def has_key(self, section, key):
        if key in self.options(section):
            return True
        else:
            return False
            