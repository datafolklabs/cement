"""Cement basic plugin handler extension."""

import os
import sys
import glob
import imp
from cement2.core import backend, handler, plugin, util, exc

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

        # parse all app configs for plugins
        for section in self.config.sections():
            if not self.config.has_key(section, 'enable_plugin'):
                continue
            if util.is_true(self.config.get(section, 'enable_plugin')):
                self.enabled_plugins.append(section)

        # parse plugin config dir for enabled plugins, or return 
        if self.plugin_config_dir:
            if not os.path.exists(self.plugin_config_dir):
                Log.debug('plugin config dir %s does not exist.' % 
                          self.plugin_config_dir)
                return
        
        for config in glob.glob("%s/*.conf" % self.plugin_config_dir):
            Log.debug("loading plugin config from '%s'." % config)
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
        
        
    def _load_plugin_from_dir(self, plugin_name, plugin_dir):
        full_path = os.path.join(plugin_dir, "%s.py" % plugin_name)
        if not os.path.exists(full_path):
            Log.debug("plugin file '%s' does not exist." % full_path)
            return False
            
        Log.debug("attempting to load '%s' from '%s'" % (plugin_name, 
                                                         plugin_dir))
        
        # We don't catch this because it would make debugging a nightmare
        f, path, desc = imp.find_module(plugin_name, [plugin_dir])
        imp.load_module(plugin_name, f, path, desc)
        return True
            
    def _load_plugin_from_module(self, plugin_name, plugin_module):
        full_module = '%s.%s' % (plugin_module, plugin_name)
        Log.debug("attempting to load '%s' from '%s'" % (plugin_name, 
                                                         plugin_module))
        
        # We don't catch this because it would make debugging a nightmare
        __import__(full_module, globals(), locals(), [], -1)
        return True
            
    def load_plugin(self, plugin_name):
        Log.debug("loading application plugin '%s'" % plugin_name)
        plugin_dir = self.config.get('base', 'plugin_dir')
        plugin_module = self.config.get('base', 'plugin_bootstrap_module')
        
        # first attempt to load from plugin_dir, then from a bootstrap module
        
        if self._load_plugin_from_dir(plugin_name, plugin_dir):
            return True
        elif self._load_plugin_from_module(plugin_name, plugin_module):
            return True
        else:
            import traceback
            traceback.print_exc(file=sys.stdout)
            raise exc.CementConfigError(
                "Unable to import plugin '%s'." % plugin_name
                )
    
    def load_plugins(self, plugin_list):
        for plugin_name in plugin_list:
            self.load_plugin(plugin_name)
        
handler.register(CementPluginHandler)