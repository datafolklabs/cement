"""Cement core extensions module."""

from zope import interface

from cement2.core import backend, exc

Log = backend.minimal_logger(__name__)

def extension_handler_invariant(obj):
    invalid = []
    members = [
        '__init__',
        '__handler_label__',
        '__handler_type__',
        'load_extension',
        'load_extensions',
        'loaded_extensions',
        ]
        
    for member in members:
        if not hasattr(obj, member):
            invalid.append(member)
    
    if invalid:
        raise exc.CementInterfaceError, \
            "Invalid or missing: %s in %s" % (invalid, obj)
    
class IExtensionHandler(interface.Interface):
    """
    This class defines the Extension Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    """
    # internal mechanism for handler registration
    __handler_type__ = interface.Attribute('Handler Type Identifier')
    __handler_label__ = interface.Attribute('Handler Label Identifier')
    loaded_extensions = interface.Attribute('List of loaded extensions')
    interface.invariant(extension_handler_invariant)
    
    def __init__(defaults, *args, **kw):
        """
        The __init__ function emplementation of Cement handlers acts as a 
        wrapper for initialization.  In general, the implementation simply
        needs to accept the defaults dict as its first argument.  If the 
        implementation subclasses from something else it will need to
        handle passing the proper args/keyword args to that classes __init__
        function, or you can easily just pass *args, **kw directly to it.
        
        Required Arguments:
        
            config
                The application default config dictionary.  This is *not* a 
                config object, but rather a dictionary which should be 
                obvious because the config handler implementation is what
                provides the application config object.
        
        
        Optional Arguments:
        
            *args
                Additional positional arguments.
                
            **kw
                Additional keyword arguments.
                
        Returns: n/a
        
        """
    
    def load_extension(self, ext_name):
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
    __handler_type__ = 'extension'
    __handler_label__ = 'cement'
    interface.implements(IExtensionHandler)
    loaded_extensions = []
    
    def __init__(self, config_obj, *args, **kw):
        self.config = config_obj
        self.enabled_extensions = []
        
    def load_extension(self, ext_name):
        module = "cement2.ext.ext_%s" % ext_name
        
        if ext_name in self.loaded_extensions:
            Log.debug("framework extension '%s' already loaded" % module)
            return 
            
        Log.debug("loading the '%s' framework extension" % module)
        try:
            __import__(module)
            self.loaded_extensions.append(module)
        except ImportError, e:
            raise exc.CementRuntimeError, e.args[0]
    
    def load_extensions(self, ext_list):
        for ext in ext_list:
            self.load_extension(ext)
        

    