"""Cement core plugins module."""

from zope import interface

from cement2.core import backend, exc

Log = backend.minimal_logger(__name__)

def plugin_handler_invariant(obj):
    members = [
        'setup',
        'load_plugin',
        'load_plugins',
        'loaded_plugins',
        ]
    backend.validate_invariants(obj, members)
    
class IPluginHandler(interface.Interface):
    """
    This class defines the Plugin Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    """
    meta = interface.Attribute('Handler meta-data')
    loaded_plugins = interface.Attribute('List of loaded plugins')
    interface.invariant(plugin_handler_invariant)
    
    def setup(config_obj):
        """
        The setup function is called during application initialization and
        must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.
        
        Required Arguments:
        
            config_obj
                The application configuration object.  This is a config object 
                that implements the IConfigHandler interface and not a config 
                dictionary, though some config handler implementations may 
                also function like a dict (i.e. configobj).
                
        Returns: n/a
        
        """
    
    def load_plugin(self, plugin_name):
        """
        Load a plugin whose name is 'plugin_name'.
        
        Required Arguments:
        
            plugin_name
                The name of the plugin to load.
                
        """
        
    def load_plugins(self, plugin_list):
        """
        Load all plugins from plugin_list.
        
        Required Arguments:
        
            plugin_list
                A list of plugin names to load.
        
        """

        

    
    
    
    
    
    
        