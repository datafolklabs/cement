
import os
import sys
from zope.interface import Interface, implements

if sys.version_info[0] < 3:
    from ConfigParser import RawConfigParser
else:
    from configparser import RawConfigParser
    
class CementConfigHandler(Interface):
    def __init__(self, default_config):
        self.default_config = default_config
        
    def parse_files(self):
        """
        Parse all config files in self.default_config['config_files'].
        """
        for _file in self.default_config['config_files']:
            self.parse_file(_file)
    
    def parse_file(self, file_path):
        """
        Parse config file settings from file_path.
        """
        pass

    def has_key(self, section, key):
        pass
    
    def keys(self, section):
        pass
    
    def has_section(self, section):    
        pass
            
    def sections(self):
        pass
           
    def get(self, section, key):
        pass
            
    def set(self, section, key):
        pass
                        
class ConfigParserConfigHandler(RawConfigParser):
    implements(CementConfigHandler)
    
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
