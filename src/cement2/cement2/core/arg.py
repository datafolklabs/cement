"""
Cement core argument module.

"""

from ..core import backend, exc, interface, handler

Log = backend.minimal_logger(__name__)

def argument_validator(klass, obj):
    """Validates a handler implementation against the IArgument interface."""
    members = [
        '_setup',
        'parse',
        'parsed_args',
        'add_argument',
        ]
    interface.validate(IArgument, obj, members)
    
class IArgument(interface.Interface):
    """
    This class defines the Argument Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.  Implementations do *not* subclass from interfaces.
    
    Example:
    
    .. code-block:: python
    
        from cement2.core import interface, arg

        class MyArgumentHandler(arg.CementArgumentHandler):
            class Meta:
                interface = arg.IArgument
                label = 'my_argument_handler'
                
    """
    class IMeta:
        label = 'argument'
        validator = argument_validator
    
    # Must be provided by the implementation
    Meta = interface.Attribute('Handler Meta-data')
    parsed_args = interface.Attribute('Parsed args object')
    
    def _setup(app_obj):
        """
        The _setup function is called during application initialization and
        must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.
        
        Required Arguments:
        
            app_obj
                The application object.
                
        Return: None
        
        """
    
    def add_argument(self, *args, **kw):
        """
        Add arguments for parsing.  This should be -o/--option or positional.  
        
        Positional Arguments:
        
            args
                List of option arguments.  Generally something like 
                ['-h', '--help'].
                
        Optional Arguments
        
            dest
                The destination name (var).  Default: arg[0]'s string.
            
            help
                The help text for --help output (for that argument).
            
            action
                Must support: ['store', 'store_true', 'store_false', 
                'store_const']
            
            const
                The value stored if action == 'store_const'.
                
            default
                The default value.
                
        
        Return: None
        
        """
        
    def parse(self, arg_list):
        """
        Parse the argument list (i.e. sys.argv).  Can return any object as
        long as it's members contain those of the added arguments.  For 
        example, if adding a '-v/--version' option that stores to the dest of
        'version', then the member must be callable as 'Object().version'.
        
        Must also set self.parsed_args to what is being returned.
        
        Required Arguments:
        
            arg_list
                A list of command line arguments.
        
        Return: Callable
        
        """

class CementArgumentHandler(handler.CementBaseHandler):
    """
    Base class that all Argument Handlers should sub-class from.
    
    """
    class Meta:
        label = None
        interface = IArgument
        
    def __init__(self, *args, **kw):
        super(CementArgumentHandler, self).__init__(*args, **kw)
        