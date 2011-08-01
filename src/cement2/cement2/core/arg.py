"""Cement core argument module."""

from zope import interface
from cement2.core import backend, exc

Log = backend.minimal_logger(__name__)

def arg_handler_invariant(obj):
    members = [
        'setup',
        'parse',
        'result',
        ]
    backend.validate_invariants(obj, members)
    
class IArgumentHandler(interface.Interface):
    """
    This class defines the Argument Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    """
    meta = interface.Attribute('Handler meta-data')
    result = interface.Attribute('Parsed args object')
    interface.invariant(arg_handler_invariant)
    
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
    
    def minimal_add_argument(self, *args, **kw):
        """
        A minimal interface to adding an argument.  
        
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
                
        """
        
    def parse(self, args):
        """
        Parse the argument list (i.e. sys.argv).  Can return any object as
        long as it's members contain those of the added arguments.  For 
        example, if adding a '-v/--version' option that stores to the dest of
        'version', then the member must be callable as 'Object().version'.
        
        Required Arguments:
        
            args
                A list of command line arguments.
        
        Returns: Callable
        
        """
