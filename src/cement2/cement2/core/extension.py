"""Cement core extensions module."""

from ..core import backend, exc, interface, handler

Log = backend.minimal_logger(__name__)
    
def extension_validator(klass, obj):
    """
    Validates an handler implementation against the IExtension interface.
    
    """
    members = [
        '_setup',
        'load_extension',
        'load_extensions',
        'loaded_extensions',
        ]
    interface.validate(IExtension, obj, members)
    
class IExtension(interface.Interface):
    """
    This class defines the Extension Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    Implementations do *not* subclass from interfaces.
    
    Usage:
    
    .. code-block:: python
    
        from cement2.core import extension
        
        class MyExtensionHandler(object):
            class Meta:
                interface = extension.IExtension
                label = 'my_extension_handler'
            ...
            
    """
    
    # This is interface Meta-deta, not part of the implemention
    class IMeta:
        label = 'extension'
        validator = extension_validator
    
    # Must be provided by the implementation
    Meta = interface.Attribute('Handler Meta-data class')
    loaded_extensions = interface.Attribute('List of loaded extensions')
    
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
    
    def load_extension(self, ext_module):
        """
        Load an extension whose module is 'ext_module'.  For example, 
        'cement2.ext.ext_configobj'.
        
        Required Arguments:
        
            ext_module
                The name of the extension to load.
                
        """
        
    def load_extensions(self, ext_list):
        """
        Load all extensions from ext_list.
        
        Required Arguments:
        
            ext_list
                A list of extension modules to load.  For example, 
                ['cement2.ext.ext_configobj', 'cement2.ext.ext_logging'].
        
        """

class CementExtensionHandler(handler.CementBaseHandler):
    loaded_extensions = []
    
    class Meta:
        interface = IExtension
        label = 'cement'
        
    def __init__(self, **kw):
        """
        This is an implementation of the IExtentionHandler interface.  It handles
        loading framework extensions.
    
        """
        super(CementExtensionHandler, self).__init__(**kw)
        self.app = None
        self._loaded_extensions = []
        
    def _setup(self, app_obj):
        self.app = app_obj
    
    @property
    def loaded_extensions(self):
        return self._loaded_extensions
        
    def load_extension(self, ext_module):
        """
        Given an extension module name, load or in other-words 'import' the 
        extension.
        
        Required Arguments:
        
            ext_module
                The extension module name.  For example 
                'cement2.ext.ext_logging'.
                
        """
        # If its not a full module path then preppend our default path
        if ext_module.find('.') == -1:
            ext_module = 'cement2.ext.ext_%s' % ext_module
            
        if ext_module in self.loaded_extensions:
            Log.debug("framework extension '%s' already loaded" % ext_module)
            return 
            
        Log.debug("loading the '%s' framework extension" % ext_module)
        try:
            __import__(ext_module, globals(), locals(), [])                
            self.loaded_extensions.append(ext_module)
   
        except ImportError as e:
            raise exc.CementRuntimeError(e.args[0])
    
    def load_extensions(self, ext_list):
        """
        Given a list of extension modules, iterate over the list and pass
        individually to self.load_extension().
        
        Required Arguments:
        
            ext_list
                A list of extension modules.
                
        """
        for ext in ext_list:
            self.load_extension(ext)
