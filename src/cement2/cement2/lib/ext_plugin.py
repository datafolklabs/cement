"""Cement Plugin Framework Extension Library."""

import os
import sys
import glob
import imp
from cement2.core import backend, handler, plugin, util, exc

Log = backend.minimal_logger(__name__)

class CementPluginHandler(object):
    """
    This class is an internal implementation of the 
    :ref:`IPlugin <cement2.core.plugin>` interface. It does not take any 
    parameters on initialization.
    
    """
    
    # Listed here to satisfy the validator
    loaded_plugins = None
    enabled_plugins = None
    disabled_plugins = None
    
    class Meta:
        interface = plugin.IPlugin
        label = 'cement'
    
    def __init__(self):
       self.loaded_plugins = []
       self.enabled_plugins = []
       self.disabled_plugins = []
     
    def setup(self, config_obj):
        """
        Sets up the class for use by the framework, including parsing the
        application config, and plugin config files for enabled plugins
        signified by a 'enable_plugin' option under a config [section] and
        determining that plugins name by the [section] name.  Plugins whose
        config has enable_plugin=True are appended to the self.enabled_plugins
        list.  If the plugin is disabled, the plugin name is appended to the
        self.disabled_plugins list.
        
        Required Arguments:
        
            config_obj
                The application configuration object.  This is a config object 
                that implements the :ref:`IConfig <cement2.core.config>` 
                interface and not a config dictionary, though some config 
                handler implementations may also function like a dict 
                (i.e. configobj).
                
        Returns: n/a
        
        """
        
        self.config = config_obj
        self.plugin_config_dir = self.config.get('base', 'plugin_config_dir')
        config_handler = handler.get('config', self.config.get
                                    ('base', 'config_handler'))

        # parse all app configs for plugins
        for section in self.config.get_sections():
            if not self.config.has_key(section, 'enable_plugin'):
                continue
            if util.is_true(self.config.get(section, 'enable_plugin')):
                self.enabled_plugins.append(section)
            else:
                self.disabled_plugins.append(section)

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
            else:
                self.disabled_plugins.append(section)
        
    def _load_plugin_from_dir(self, plugin_name, plugin_dir):
        """
        Load a plugin from file within a plugin directory rather than a 
        python package within sys.path.
        
        Required Arguments:
        
            plugin_name
                The name of the plugin, also the name of the file with '.py'
                appended to the name.
            
            plugin_dir
                The filesystem directory path where to find the file.
                
        """
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
            
    def _load_plugin_from_module(self, plugin_name, base_package):
        """
        Load a plugin from a python module.  Returns True if no ImportError
        is encountered.
        
        Required Arguments:
        
            plugin_name
                The name of the plugin, also the name of the module to load
                from base_package.  I.e. 'myapp.bootstrap.myplugin'.
            
            base_package
                The base python package to load the plugin module from.  I.e.
                'myapp.bootstrap' or similar.
        
        Returns: Bool
        
        """
        full_module = '%s.%s' % (base_package, plugin_name)
        Log.debug("attempting to load '%s' from '%s'" % (plugin_name, 
                                                         base_package))
        
        # We don't catch this because it would make debugging a nightmare
        __import__(full_module, globals(), locals(), [], -1)
        return True
            
    def load_plugin(self, plugin_name):
        """
        Load a plugin whose name is 'plugin_name'.  First attempt to load
        from a plugin directory (plugin_dir), secondly attempt to load from a 
        bootstrap module (plugin_bootstrap_module) determined by self.config.
        
        Upon successful loading of a plugin, the plugin name is appended to
        the self.loaded_plugins list.
        
        Required Arguments:
        
            plugin_name
                The name of the plugin to load.
        
        """
        Log.debug("loading application plugin '%s'" % plugin_name)
        plugin_dir = self.config.get('base', 'plugin_dir')
        plugin_module = self.config.get('base', 'plugin_bootstrap_module')
        
        # first attempt to load from plugin_dir, then from a bootstrap module
        
        if self._load_plugin_from_dir(plugin_name, plugin_dir):
            self.loaded_plugins.append(plugin_name)
            return True
        elif self._load_plugin_from_module(plugin_name, plugin_module):
            self.loaded_plugins.append(plugin_name)
            return True
        
        # This doesn't seem likely to be triggerable because the second load
        # from module will raise an ImportError
        #else:
        #    import traceback
        #    traceback.print_exc(file=sys.stdout)
        #    raise exc.CementConfigError(
        #        "Unable to import plugin '%s'." % plugin_name
        #        )
    
    def load_plugins(self, plugin_list):
        """
        Load a list of plugins.  Each plugin name is passed to 
        self.load_plugin().
        
        Required Arguments:
            
            plugin_list
                A list of plugin names to load.
        
        """
        for plugin_name in plugin_list:
            self.load_plugin(plugin_name)
