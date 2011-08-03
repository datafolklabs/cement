"""Cement core controller module."""

from cement2.core import backend, exc, interface

Log = backend.minimal_logger(__name__)

def controller_validator(obj):
    members = [
        'setup',
        'dispatch',
        ]
    interface.validate(IController, obj, members)
    
class IController(interface.Interface):
    """
    This class defines the Controller Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    Implementations do *not* subclass from interfaces.
    
    """
    class imeta:
        label = 'controller'
        validator = controller_validator
    
    # Must be provided by the implementation
    meta = interface.Attribute('Handler meta-data')
    registered_controllers = interface.Attribute('List of registered controllers')
    
    def setup(base_app):
        """
        The setup function is after application initialization and after it
        is determined that this controller was requested via command line
        arguments.  Meaning, a controllers setup() function is only called
        right before it's dispatch() function is called to execute a command.
        Must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.
        
        Required Arguments:
        
            base_app
                The application object, after it has been setup() and run().
                
        Returns: n/a
        
        """
    
    def dispatch(self):
        """
        Reads the application object's data to dispatch a command from this
        controller.  For example, reading self.app.pargs to determine what
        command was passed, and then executing that command function.
                
        """

class expose(object):
    def __init__(self, hide=False, help='', aliases=[]):
        """
        Used to expose controller functions to be listed as commands, and to 
        decorate the function with meta data for the argument parser.
        
        Optional Argumnets:
        
            hide
                Whether the command should be visible
            
            help
                Help text.
            
            alias
                An alias to this command.
                
        """
        self.hide = hide
        self.help = help
        self.aliases = aliases

    def __call__(self, func):
        self.func = func
        self.func.label = self.func.__name__
        self.func.exposed = True
        self.func.hide = self.hide
        self.func.help = self.help
        self.func.aliases = self.aliases
        return self.func
        
class CementControllerHandler(object):
    """
    This is an implementation of the IControllerHandler interface, and also
    acts as a base class that application controllers can subclass from.
    
    """
    class meta:
        interface = IController
        label = None # provided in subclass
        options = []
        
    def __init__(self):
        pass
        
    def setup(self, base_app):
        self.app = base_app
        
        # shortcuts
        self.config = self.app.config
        self.log = self.app.log
        self.pargs = self.app.pargs
        
    def dispatch(self):
        pass
