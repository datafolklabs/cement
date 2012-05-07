"""Cement core plugins module."""

from ..core import backend, exc, interface, handler

Log = backend.minimal_logger(__name__)

def plugin_validator(klass, obj):
    """Validates an handler implementation against the IPlugin interface."""
    
    members = [
        '_setup',
        'load_plugin',
        'load_plugins',
        'loaded_plugins',
        'enabled_plugins',
        'disabled_plugins',
        ]
    interface.validate(IPlugin, obj, members)
    
class IPlugin(interface.Interface):
    """
    This class defines the Plugin Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    Implementations do *not* subclass from interfaces.
    
    Usage:
    
    .. code-block:: python
    
        from cement2.core import plugin
        
        class MyPluginHandler(object):
            class Meta:
                interface = plugin.IPlugin
                label = 'my_plugin_handler'
            ...
    
    """
    class IMeta:
        label = 'plugin'
        validator = plugin_validator
    
    # Must be provided by the implementation
    Meta = interface.Attribute('Handler Meta-data')
    loaded_plugins = interface.Attribute('List of loaded plugins')
    enabled_plugins = interface.Attribute('List of enabled plugins')
    disabled_plugins = interface.Attribute('List of disabled plugins')
    
    def _setup(app_obj):
        """
        The _setup function is called during application initialization and
        must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.
        
        Required Arguments:
        
            app_obj
                The application object. 
                                
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
        
class CementPluginHandler(handler.CementBaseHandler):
    """
    Base class that all Plugin Handlers should sub-class from.
    
    """
    
    class Meta:
        interface = IPlugin
        
    def __init__(self, *args, **kw):
        super(CementPluginHandler, self).__init__(*args, **kw)