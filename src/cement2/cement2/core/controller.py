"""Cement core controller module."""

import re
import textwrap
import argparse
from cement2.core import backend, exc, interface, handler

Log = backend.minimal_logger(__name__)

def controller_validator(klass, obj):
    """
    Validates an handler implementation against the IController interface.
    
    """
    members = [
        'setup',
        'dispatch',
        ]
    meta = [
        'label',
        'interface',
        'description',
        'defaults',
        'arguments',
        ]
    interface.validate(IController, obj, members, meta=meta)
    
class IController(interface.Interface):
    """
    This class defines the Controller Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    Implementations do *not* subclass from interfaces.
    
    Usage:
    
    .. code-block:: python
    
        from cement2.core import controller
        
        class MyBaseController(object):
            class meta:
                interface = controller.IController
                label = 'my_base_controller'
            ...
            
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
            
            aliases
                List of aliases to this command.
             
        Usage:
        
        .. code-block:: python
        
            from cement2.core import controller
           
            class MyAppBaseController(controller.CementBaseController):
                class meta:
                    interface = controller.IController
                    label = 'base'
                    description = 'MyApp is awesome'
                    defaults = dict()
                    arguments = []
                  
                @controller.expose(hide=True, aliases=['run'])
                def default(self):
                    print("In MyAppBaseController.default()")
       
                @controller.expose()
                def my_command(self):
                    print("In MyAppBaseController.my_command()")
                   
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

class CementBaseController(object):
    """
    This is an implementation of the IControllerHandler interface, but as a
    base class that application controllers need to subclass from.  
    Registering it directly as a handler is useless.
    
    NOTE: This handler *requires* that the applications 'arg_handler' be
    argparse.  If using an alternative argument handler you will need to 
    write your own controller.
    
    Usage:
    
    .. code-block:: python
    
        from cement2.core import controller
           
        class MyAppBaseController(controller.CementBaseController):
            class meta:
                interface = controller.IController
                label = 'base'
                description = 'MyApp is awesome'
                defaults = dict()
                arguments = []
            ...
            
    """
    class meta:
        interface = IController
        label = None # provided in subclass
        defaults = {} # default config options
        arguments = [] # list of tuple (*args, *kwargs)
        stacked_on = None # controller name to merge commands/options into
        hide = False # whether to hide controller completely
        
    ignored = ['visible', 'hidden', 'exposed']
          
    def __init__(self):
        self.app = None
        self.command = 'default'
        self.config = None
        self.log = None
        self.pargs = None
        self.visible = {}
        self.hidden = {}
        self.exposed = {}
        self.arguments = []
        
    def setup(self, base_app):
        self.app = base_app
        self._collect()
        self._add_arguments_to_parser()
        
        # chop off a command argument if it matches an exposed command
        if len(self.app.argv) > 0 and not self.app.argv[0].startswith('-'):
            
            # translate dashes back to underscores
            cmd = re.sub('-', '_', self.app.argv[0])
            if cmd in self.exposed:
                self.command = cmd
                self.app.argv.pop(0)
            else:
                for label in self.exposed:
                    func = self.exposed[label]
                    if self.app.argv[0] in func['aliases']:
                        self.command = func['label']
                        self.app.argv.pop(0)
                        break
                        
        self.app.args.description = self.help_text
        self.app.args.usage = self.usage_text
        self.app.args.formatter_class=argparse.RawDescriptionHelpFormatter

        self.app._parse_args()
        
        # shortcuts
        self.config = self.app.config
        self.log = self.app.log
        self.pargs = self.app.pargs
                
    def dispatch(self):
        """
        Takes the remaining arguments from self.app.argv and parses for a
        command to dispatch, and if so... dispatches it.
        
        """
        if not self.command:
            Log.debug("no command to dispatch")
        elif self.command not in self.exposed:
            Log.debug("no function named %s" % self.command)
        else:    
            func = self.exposed[self.command]     
            Log.debug("dispatching command: %s.%s" % \
                      (func['controller'], func['label']))
            
            if func['controller'] == self.meta.label:
                getattr(self, func['label'])()
            else:
                controller = handler.get('controller', func['controller'])()
                getattr(controller, func['label'])()

    @expose(hide=True, help='default command')
    def default(self):
        raise NotImplementedError
    
    def _add_arguments_to_parser(self):
        """
        Run after _collect().  Add the collected arguments to the apps
        argument parser.
        
        """
        for _args,_kwargs in self.arguments:
            self.app.args.add_argument(*_args, **_kwargs)
            
    def _collect(self):
        """
        Collects all commands and arguments from this controller, and other
        availble controllers.
        """
        self.visible = {}
        self.hidden = {}
        self.exposed = {}
        self.arguments = []
    
        
        # collect our meta arguments
        Log.debug('collecting arguments from %s controller' % self.meta.label)
        for _args,_kwargs in self.meta.arguments:
            self.arguments.append((_args, _kwargs))
            
        # collect exposed commands from ourself
        Log.debug('collecting commands from %s controller' % self.meta.label)
        for member in dir(self):
            if member in self.ignored or member.startswith('_'):
                continue
                
            func = getattr(self, member)
            if hasattr(func, 'exposed'):
                func_dict = dict(
                    controller=self.meta.label,
                    label=func.label,
                    help=func.help,
                    aliases=func.aliases,
                    hide=func.hide,
                    )
                self.exposed[func.label] = func_dict
                if func.hide:
                    self.hidden[func.label] = func_dict
                else:
                    if not getattr(self.meta, 'hide', None):
                        self.visible[func.label] = func_dict
        
        # then handle stacked, and not stacked controllers
        for controller in handler.list('controller'):
            if controller.meta.label == self.meta.label:
                continue
                
            # expose other controllers as commands also (that aren't stacked
            # onto another controller)
            if not hasattr(controller.meta, 'stacked_on'):
                if getattr(controller.meta, 'label', None) == 'base':
                    continue
                    
                if not getattr(controller.meta, 'hide', None):
                    Log.debug('exposing %s controller' % controller.meta.label)
                    func_dict = dict(
                        controller=controller.meta.label,
                        label=controller.meta.label,
                        help=controller.meta.description,
                        aliases=[],
                        hide=False,
                        )
                    self.exposed[controller.meta.label] = func_dict
                    if not getattr(controller.meta, 'hide', None):
                        self.visible[controller.meta.label] = func_dict
                        
            elif controller.meta.stacked_on == self.meta.label:
                # Need to collect on the controller
                contr = controller()
                
                # This is a hack, but we don't want to run full setup() on
                # the stacked controllers.
                contr.app = self.app
                contr._collect()
                
                # add stacked arguments into ours
                Log.debug('collecting arguments from %s controller (stacked)' % \
                          controller.meta.label)
                for _args,_kwargs in contr.arguments:
                    self.arguments.append((_args, _kwargs))
                    
                # add stacked commands into ours
                Log.debug('collecting commands from %s controller (stacked)' % \
                          controller.meta.label)
                          
                
                func_dicts = contr.visible
                for label in func_dicts:
                    self.exposed[label] = func_dicts[label]
                    if func_dicts[label]['hide']:
                        if label in self.hidden:
                            raise exc.CementRuntimeError(
                                "Hidden command '%s' already exists." % label
                                )
                        self.hidden[label] = func_dicts[label]
                    else:
                        if not getattr(controller.meta, 'hide', False):
                            if label in self.visible:
                                raise exc.CementRuntimeError(
                                    "Command '%s' already exists." % label
                                    )
                            self.visible[label] = func_dicts[label]
          
    @property
    def usage_text(self):
        if self.meta.label == 'base':
            txt = "%s <CMD> -opt1 --opt2=VAL [arg1] [arg2] ..." % \
                self.app.args.prog
        else:
            txt = "%s %s <CMD> -opt1 --opt2=VAL [arg1] [arg2] ..." % \
                  (self.app.args.prog, self.meta.label)
        return txt
        
    @property
    def help_text(self):
        cmd_txt = ''
        
        # hack it up to keep commands in alphabetical order
        sorted_labels = []
        for label in self.visible.keys():
            old_label = label
            label = re.sub('_', '-', label)
            sorted_labels.append(label)
            self.visible[label] = self.visible[old_label]
            del self.visible[old_label]
        sorted_labels.sort()
        
        for label in sorted_labels:
            func = self.visible[label]
            if len(func['aliases']) > 0:
                cmd_txt = cmd_txt + "  %s (aliases: %s)\n" % \
                            (label, ', '.join(func['aliases']))
            else:
                cmd_txt = cmd_txt + "  %s\n" % label
            
            if func['help']:
                cmd_txt = cmd_txt + "    %s\n\n" % func['help']
            else:
                cmd_txt = cmd_txt + "\n"
    
        txt = '''%s

commands:

%s

        
        ''' % (self.meta.description, cmd_txt)
        
        return textwrap.dedent(txt)        
