"""Cement basic plugin handler extension."""

import os
import glob
from cement2.core import backend, handler, plugin, util

Log = backend.minimal_logger(__name__)

class CementPluginHandler(object):
    loaded_plugins = []
    enabled_plugins = []
    disabled_plugins = []
    
    class meta:
        interface = plugin.IPlugin
        label = 'cement'
    
    def setup(self, config_obj):
        self.config = config_obj
        self.plugin_config_dir = self.config.get('base', 'plugin_config_dir')
        config_handler = handler.get('config', self.config.get
                                    ('base', 'config_handler'))
        
        if not os.path.exists(self.plugin_config_dir):
            Log.debug('plugin config dir %s does not exist.' % 
                      self.plugin_config_dir)
            return
        
        # parse all app configs for plugins
        for config in glob.glob("%s/*.conf" % self.plugin_config_dir):
            pconfig = config_handler()
            pconfig.parse_file(config)
            plugin = pconfig.sections()[0]
            
            if not pconfig.has_key(plugin, 'enable_plugin'):
                continue

            if util.is_true(pconfig.get(plugin, 'enable_plugin')):
                self.enabled_plugins.append(plugin)
                self.config.add_section(plugin)
                
                # set the app config per the already parsed plugin config
                for key in pconfig.keys(plugin):
                    self.config.set(plugin, key, pconfig.get(plugin, key))
        
        
    def load_plugin(self, plugin_name):
        Log.debug("loading application plugin '%s'" % plugin_name)
        pass
    
    def load_plugins(self, plugin_list):
        print plugin_list
        pass
        
handler.register(CementPluginHandler)