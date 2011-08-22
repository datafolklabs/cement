"""Cement core controller module."""

from cement2.core import backend, exc, interface

Log = backend.minimal_logger(__name__)

def controller_validator(klass, obj):
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
        arguments = [] # list of tuple (*args, *kwargs)
    
    ignored = []
        
    def __init__(self):
        pass
        
    def setup(self, base_app):
        self.app = base_app
        self.command = 'default'
        
        if len(self.app.argv) > 0:
            if self.app.argv[0] in self.visible_commands:
                self.command = self.app.argv.pop(0)
        
        # setup controller args
        for _args,_kwargs in self.meta.arguments:
            self.app.args.add_argument(_args, **_kwargs)
        
        self.app._parse_args()
        
        # shortcuts
        self.config = self.app.config
        self.log = self.app.log
        self.pargs = self.app.pargs
            
    def dispatch(self):
        if not self.command:
            Log.debug("no command to dispatch")
        elif not hasattr(self, self.command):
            Log.debug("no function named %s" % self.command)
            
        Log.debug("dispatching command: %s" % self.command)
        func = getattr(self, self.command)
        func()
    
    @expose(hide=True, help='default command', aliases=['run'])
    def default(self):
        raise NotImplementedError

    ignored = ['visible_commands', 'hidden_commands', 'exposed_commands']
    
    @property
    def visible_commands(self):
        visible = []
        for member in dir(self):
            if member in self.ignored or member.startswith('_'):
                continue

            if hasattr(getattr(self, member), 'exposed'):
                visible.append(member)
        return visible
    
    @property
    def hidden_commands(self):
        hidden = []
        for member in dir(self):
            if member in self.ignored or member.startswith('_'):
                continue

            if hasattr(getattr(self, member), 'exposed') \
                and getattr(self, member).hide == True:
                hidden.append(member)
        return hidden
        
    @property
    def exposed_commands(self):
        exposed = []
        for member in dir(self):
            if member in self.ignored or member.startswith('_'):
                continue

            if hasattr(getattr(self, member), 'exposed'):
                exposed.append(member)
        return exposed