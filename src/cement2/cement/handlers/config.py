
from cement.core.handler import CementConfigHandler
from configparser import SafeConfigParser

class ConfigParserConfigHandler(CementConfigHandler):
    def __init__(self, default_config, section):
        CementConfigHandler.__init__(self, default_config, section)
        self.backend = SafeConfigParser(self.default_config)
        self.backend.add_section(self.section)
        for key in self.default_config:
            self.backend.set(self.section, key, self.default_config[key])
            
    def parse_files(self):
        """
        Parse config file settings from self.default_config['config_files'].
        """
        self.backend.read(self.default_config['config_files'])
    
    def parse_file(self, file_path):
        """
        Parse config file settings from file_path.
        """
        raise NotImplementedError(
            "CementConfigHandler.parse_file() must be subclassed."
            )
    
    def __getitem__(self, key):
        return self.backend.get(self.section, key)
    
    def __setitem__(self, key, value):
        return self.backend.set(self.section, key, value)
