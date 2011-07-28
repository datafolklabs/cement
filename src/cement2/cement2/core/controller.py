"""Cement core controller module."""

from zope import interface
from cement2.core import backend, exc

Log = backend.minimal_logger(__name__)

def controller_handler_invariant(obj):
    invalid = []
    members = [
        '__init__',
        '__handler_label__',
        '__handler_type__',
        'setup',
        'register',
        ]
        
    for member in members:
        if not hasattr(obj, member):
            invalid.append(member)
    
    if invalid:
        raise exc.CementInterfaceError, \
            "Invalid or missing: %s in %s" % (invalid, obj)
    
class IControllerHandler(interface.Interface):
    """
    This class defines the Controller Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    """
    # internal mechanism for handler registration
    __handler_type__ = interface.Attribute('Handler Type Identifier')
    __handler_label__ = interface.Attribute('Handler Label Identifier')
    registered_controllers = interface.Attribute('List of registered controllers')
    interface.invariant(controller_handler_invariant)
    
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
    
    def register(self, controller_obj):
        """
        Load an extension whose name is 'ext_name'.
        
        Required Arguments:
        
            ext
                The name of the extension to load.
                
        """
        
    def load_extensions(self, ext_list):
        """
        Load all extensions from ext_list.
        
        Required Arguments:
        
            ext_list
                A list of extension names to load.
        
        """

class CementExtensionHandler(object):
    """
    This is an implementation of the IExtentionHandler interface.  It handles
    loading framework extensions.
    
    """
    
    __handler_type__ = 'extension'
    __handler_label__ = 'cement'
    interface.implements(IExtensionHandler)
    loaded_extensions = []
    
    def __init__(self):
        self.defaults = {}
        self.enabled_extensions = []
        
    def setup(self, defaults):
        self.defaults = defaults
        
    def load_extension(self, ext_module):
        #module = "cement2.ext.ext_%s" % ext_name
        
        if ext_module in self.loaded_extensions:
            Log.debug("framework extension '%s' already loaded" % ext_module)
            return 
            
        Log.debug("loading the '%s' framework extension" % ext_module)
        try:
            __import__(ext_module)
            self.loaded_extensions.append(ext_module)
        except ImportError, e:
            raise exc.CementRuntimeError, e.args[0]
    
    def load_extensions(self, ext_list):
        for ext in ext_list:
            self.load_extension(ext)