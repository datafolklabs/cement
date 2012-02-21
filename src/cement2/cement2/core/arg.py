"""
Cement core argument module.

"""

from cement2.core import backend, exc, interface, meta

Log = backend.minimal_logger(__name__)

def argument_validator(klass, obj):
    """Validates an handler implementation against the IArgument interface."""
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

        class MyArgumentHandler(object):
            class Meta:
                interface = arg.IArgument
                label = 'my_argument_handler'

            ...
                
    """
    class IMeta:
        label = 'argument'
        validator = argument_validator
    
    # Must be provided by the implementation
    Meta = interface.Attribute('Handler Meta-data')
    parsed_args = interface.Attribute('Parsed args object')
    
    def _setup(config_obj):
        """
        The _setup function is called during application initialization and
        must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.
        
        Required Arguments:
        
            config_obj
                The application configuration object.  This is a config object 
                that implements the :ref:`IConfig` <cement2.core.config>` 
                interface and not a config dictionary, though some config 
                handler implementations may also function like a dict 
                (i.e. configobj).
                
        Returns: n/a
        
        """
    
    def add_argument(self, *args, **kw):
        """
        Add arguments for parsing.  This should be -o/--option or positional.  
        
        Positional Arguments:
        
            args
                The option args.  Generally ['-h', '--help'].
                
        Optional Arguments
        
            dest
                The destination name (var).  Default: arg[0]'s string.
            
            help
                The help test for --help output.
            
            action
                Must be one of: ['store', 'store_true', 'store_false', 
                'store_const']
            
            const
                The value stored if action == 'store_const'.
                
            default
                The default value.
                
        
        Returns: n/a
        
        """
        
    def parse(self, args):
        """
        Parse the argument list (i.e. sys.argv).  Can return any object as
        long as it's members contain those of the added arguments.  For 
        example, if adding a '-v/--version' option that stores to the dest of
        'version', then the member must be callable as 'Object().version'.
        
        Must also set self.parsed_args to what is being returned.
        
        Required Arguments:
        
            args
                A list of command line arguments.
        
        Returns: Callable
        
        """

class CementArgumentHandler(meta.MetaMixin):
    class Meta:
        interface = IArgument
        
    def __init__(self, *args, **kw):
        super(CementArgumentHandler, self).__init__(*args, **kw)
        