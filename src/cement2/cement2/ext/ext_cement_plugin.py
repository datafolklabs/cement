"""Cement basic plugin handler extension."""

from cement2.core import backend, handler, plugin

Log = backend.minimal_logger(__name__)

class CementPluginHandler(object):
    loaded_plugins = []
    
    class meta:
        interface = plugin.IPlugin
        label = 'cement'
    
    def setup(self, config_obj):
        self.config = config_obj
        self.enabled_plugins = []
        
    def load_plugin(self, plugin_name):
        Log.debug("loading application plugin '%s'" % plugin_name)
        pass
    
    def load_plugins(self, plugin_list):
        pass
        
handler.register(CementPluginHandler)