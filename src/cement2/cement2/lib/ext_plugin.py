"""Cement Plugin Framework Extension Library."""

import os
import sys
import glob
import imp
from ..core import backend, handler, plugin, util, exc

Log = backend.minimal_logger(__name__)

### FIX ME: This is a redundant name... ?
class CementPluginHandler(plugin.CementPluginHandler):
    """
    This class is an internal implementation of the 
    :ref:`IPlugin <cement2.core.plugin>` interface. It does not take any 
    parameters on initialization.
    
    """
    
    class Meta:
        interface = plugin.IPlugin
        label = 'cement'
            
    def __init__(self):
        super(CementPluginHandler, self).__init__()
        self._loaded_plugins = []
        self._enabled_plugins = []
        self._disabled_plugins = []
     
    def _setup(self, app_obj):
        super(CementPluginHandler, self)._setup(app_obj)
        self.config_dir = util.abspath(self.app._meta.plugin_config_dir)
        self.bootstrap = self.app._meta.plugin_bootstrap
        self.load_dir = util.abspath(self.app._meta.plugin_dir)

        # grab a generic config handler object
        config_handler = handler.get('config', self.app.config._meta.label)

        # parse all app configs for plugins
        for section in self.app.config.get_sections():
            if not self.app.config.has_key(section, 'enable_plugin'):
                continue
            if util.is_true(self.app.config.get(section, 'enable_plugin')):
                self._enabled_plugins.append(section)
            else:
                self._disabled_plugins.append(section)

        # parse plugin config dir for enabled plugins, or return 
        if self.config_dir:
            if not os.path.exists(self.config_dir):
                Log.debug('plugin config dir %s does not exist.' % 
                          self.config_dir)
                return
        
        for config in glob.glob("%s/*.conf" % self.config_dir):
            config = os.path.abspath(os.path.expanduser(config))
            Log.debug("loading plugin config from '%s'." % config)
            pconfig = config_handler()
            pconfig._setup(self.app)
            pconfig.parse_file(config)

            if not pconfig.get_sections():
                Log.debug("config file '%s' has no sections." % config)
                continue
                
            plugin = pconfig.get_sections()[0]
            if not pconfig.has_key(plugin, 'enable_plugin'):
                continue

            if util.is_true(pconfig.get(plugin, 'enable_plugin')):
                self._enabled_plugins.append(plugin)
                self.app.config.add_section(plugin)
                
                # set the app config per the already parsed plugin config
                for key in pconfig.keys(plugin):
                    self.app.config.set(plugin, key, pconfig.get(plugin, key))
            else:
                self._disabled_plugins.append(section)
        
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
            
    def _load_plugin_from_bootstrap(self, plugin_name, base_package):
        """
        Load a plugin from a python package.  Returns True if no ImportError
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
        if base_package is None:
            Log.debug("plugin bootstrap module is set to None, unusable.")
            return False
            
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
        bootstrap module (plugin_bootstrap) determined by 
        self.app._meta.plugin_bootstrap.
        
        Upon successful loading of a plugin, the plugin name is appended to
        the self._loaded_plugins list.
        
        Required Arguments:
        
            plugin_name
                The name of the plugin to load.
        
        """
        Log.debug("loading application plugin '%s'" % plugin_name)

        # first attempt to load from plugin_dir, then from a bootstrap module
        
        if self._load_plugin_from_dir(plugin_name, self.load_dir):
            self._loaded_plugins.append(plugin_name)
            return True
        elif self._load_plugin_from_bootstrap(plugin_name, self.bootstrap):
            self._loaded_plugins.append(plugin_name)
            return True
        else:
            raise exc.CementRuntimeError("Unable to load plugin '%s'." % 
                                         plugin_name)
    
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

    @property
    def loaded_plugins(self):
        return self._loaded_plugins
    
    @property
    def enabled_plugins(self):
        return self._enabled_plugins

    @property
    def disabled_plugins(self):
        return self._disabled_plugins