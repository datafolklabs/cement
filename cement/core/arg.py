"""
Cement core argument module.

"""

from ..core import backend, interface, handler

LOG = backend.minimal_logger(__name__)

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
    
        from cement.core import interface, arg

        class MyArgumentHandler(arg.CementArgumentHandler):
            class Meta:
                interface = arg.IArgument
                label = 'my_argument_handler'
                
    """
    # pylint: disable=W0232, C0111, R0903
    class IMeta:
        """Interface meta-data options."""

        label = 'argument'
        """The string identifier of the interface."""
        
        validator = argument_validator
        """Interface validator function."""
        
    # Must be provided by the implementation
    Meta = interface.Attribute('Handler Meta-data')
    parsed_args = interface.Attribute('Parsed args object')
    
    def _setup(app_obj):
        """
        The _setup function is called during application initialization and
        must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.
        
        :param app_obj: The application object
        :returns: None
        
        """
    
    def add_argument(*args, **kw):
        """
        Add arguments for parsing.  This should be -o/--option or positional.  
        
        :arg args: List of option arguments.  Generally something like 
            ['-h', '--help'].
        :keyword dest: The destination name (var).  Default: arg[0]'s string.
        :keyword help: The help text for --help output (for that argument).
        :keyword action: Must support: ['store', 'store_true', 'store_false', 
            'store_const']
        :keyword const: The value stored if action == 'store_const'.
        :keyword default: The default value.
        :returns: None
        
        """
        
    def parse(arg_list):
        """
        Parse the argument list (i.e. sys.argv).  Can return any object as
        long as it's members contain those of the added arguments.  For 
        example, if adding a '-v/--version' option that stores to the dest of
        'version', then the member must be callable as 'Object().version'.
        
        Must also set self.parsed_args to what is being returned.
        
        :param arg_list: A list of command line arguments.
        :returns: Callable object
        
        """

class CementArgumentHandler(handler.CementBaseHandler):
    """
    Base class that all Argument Handlers should sub-class from.
            
    """
    # pylint: disable=W0232,R0903
    class Meta:
        """Handler meta-data options."""
        
        label = None
        """The string identifier of the handler implementation."""
        
        interface = IArgument
        """The interface that this class implements."""
        
    def __init__(self, *args, **kw):
        super(CementArgumentHandler, self).__init__(*args, **kw)
        
    def _setup(self, app_obj):
        """
        See `IArgument._setup() <#cement.core.arg.IArgument._setup>`_.
        """
        self.app_obj = app_obj
