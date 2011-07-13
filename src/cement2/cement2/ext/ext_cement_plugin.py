"""Cement basic plugin handler extension."""

from zope import interface

from cement2.core import backend, handler, plugin

Log = backend.minimal_logger(__name__)

class CementPluginHandler(object):
    __handler_type__ = 'plugin'
    __handler_label__ = 'cement'
    interface.implements(plugin.IPluginHandler)
    loaded_plugins = []
    
    def setup(self, config_obj):
        self.config = config_obj
        self.enabled_plugins = []
        
    def load_plugin(self, plugin_name):
        Log.debug("loading application plugin '%s'" % plugin_name)
        pass
    
    def load_plugins(self, plugin_list):
        pass
        
handler.register(CementPluginHandler)