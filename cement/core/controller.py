"""Cement core controller module."""

import re
import textwrap
import argparse
from ..core import backend, exc, interface, handler

LOG = backend.minimal_logger(__name__)

def controller_validator(klass, obj):
    """
    Validates a handler implementation against the IController interface.
    
    """
    members = [
        '_setup',
        '_dispatch',
        ]
    meta = [
        'label',
        'interface',
        'description',
        'config_section',
        'config_defaults',
        'arguments',
        'usage',
        'epilog',
        'stacked_on',
        'hide',
        ]
    interface.validate(IController, obj, members, meta=meta)
    
    # also check _meta.arguments values
    errmsg = "Controller arguments must be a list of tuples.  I.e. " + \
             "[ (['-f', '--foo'], dict(action='store')), ]"
    try:
        for _args,_kwargs in obj._meta.arguments:
            if not type(_args) is list:
                raise exc.InterfaceError(errmsg)
            if not type(_kwargs) is dict:
                raise exc.InterfaceError(errmsg)
    except ValueError:
        raise exc.InterfaceError(errmsg)
            
class IController(interface.Interface):
    """
    This class defines the Controller Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    Implementations do *not* subclass from interfaces.
    
    Usage:
    
    .. code-block:: python
    
        from cement.core import controller
        
        class MyBaseController(controller.CementBaseController):
            class Meta:
                interface = controller.IController
                ...            
    """
    # pylint: disable=W0232, C0111, R0903
    class IMeta:
        """Interface meta-data."""
        
        label = 'controller'
        """The string identifier of the interface."""
        
        validator = controller_validator
        """The interface validator function."""
    
    # Must be provided by the implementation
    Meta = interface.Attribute('Handler meta-data')
    
    def _setup(app_obj):
        """
        The _setup function is after application initialization and after it
        is determined that this controller was requested via command line
        arguments.  Meaning, a controllers _setup() function is only called
        right before it's _dispatch() function is called to execute a command.
        Must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.
        
        :param app_obj: The application object.
        :returns: None
        
        """
    
    def _dispatch(self):
        """
        Reads the application object's data to dispatch a command from this
        controller.  For example, reading self.app.pargs to determine what
        command was passed, and then executing that command function.
        
        Note that Cement does *not* parse arguments when calling _dispatch()
        on a controller, as it expects the controller to handle parsing 
        arguments (I.e. self.app.args.parse()).
         
        :returns: None       
        
        """

class expose(object):
    """
    Used to expose controller functions to be listed as commands, and to 
    decorate the function with Meta data for the argument parser.
    
    :param hide: Whether the command should be visible.
    :type hide: boolean
    :param help: Help text to display for that command.
    :type help: str
    :param aliases: Aliases to this command.
    :type aliases: list
         
    Usage:
    
    .. code-block:: python
    
        from cement.core.controller import CementBaseController, expose
       
        class MyAppBaseController(CementBaseController):
            class Meta:
                label = 'base'
                
            @expose(hide=True, aliases=['run'])
            def default(self):
                print("In MyAppBaseController.default()")
   
            @expose()
            def my_command(self):
                print("In MyAppBaseController.my_command()")
               
    """
    def __init__(self, hide=False, help='', aliases=[]):
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

class CementBaseController(handler.CementBaseHandler):
    """
    This is an implementation of the 
    `IControllerHandler <#cement.core.controller.IController>`_ interface, but 
    as a base class that application controllers `should` subclass from.  
    Registering it directly as a handler is useless.
    
    NOTE: This handler **requires** that the applications 'arg_handler' be
    argparse.  If using an alternative argument handler you will need to 
    write your own controller base class.
    
    Usage:
    
    .. code-block:: python
    
        from cement.core import controller
           
        class MyAppBaseController(controller.CementBaseController):
            class Meta:
                label = 'base'
                description = 'MyApp is awesome'
                config_defaults = dict()
                arguments = []
                epilog = "This is the text at the bottom of --help."
                # ...
                
        class MyStackedController(controller.CementBaseController):
            class Meta:
                label = 'second_controller'
                aliases = ['sec', 'secondary']
                stacked_on = 'base'
                # ...
                
    """
    class Meta:
        """
        Controller meta-data (can be passed as keyword arguments to the parent 
        class).
        
        """
        
        interface = IController
        """The interface this class implements."""
        
        label = 'base'
        """The string identifier for the controller."""
        
        aliases = []
        """
        A list of aliases for the controller.  Will be treated like
        command/function aliases for non-stacked controllers.  For example:
        'myapp <controller_label> --help' is the same as 
        'myapp <controller_alias> --help'.
        """
            
        description = None
        """The description shown at the top of '--help'.  Default: None"""
        
        config_section = None
        """
        A config [section] to merge config_defaults into.  Cement will default 
        to controller.<label> if None is set.
        """
        
        config_defaults = {} 
        """
        Configuration defaults (type: dict) that are merged into the 
        applications config object for the config_section mentioned above.
        """
        
        arguments = []
        """
        Arguments to pass to the argument_handler.  The format is a list
        of tuples whos items are a ( list, dict ).  Meaning:
            
        ``[ ( ['-f', '--foo'], dict(dest='foo', help='foo option') ), ]``
        
        This is equivelant to manually adding each argument to the argument
        parser as in the following example:
        
        ``parser.add_argument(['-f', '--foo'], help='foo option', dest='foo')``
        
        """

        stacked_on = None
        """
        A label of another controller to 'stack' commands/arguments on top of.
        """
        
        hide = False
        """Whether or not to hide the controller entirely."""
        
        epilog = None
        """
        The text that is displayed at the bottom when '--help' is passed.
        """
        
        usage = None
        """
        The text that is displayed at the top when '--help' is passed.  
        Although the default is `None`, Cement will set this to a generic
        usage based on the `prog`, `controller` name, etc if nothing else is
        passed.
        """
        
        argument_formatter = argparse.RawDescriptionHelpFormatter
        """
        The argument formatter class to use to display --help output.
        """
        
    ### FIX ME: What is this used for???
    ignored = ['visible', 'hidden', 'exposed']
          
    def __init__(self, *args, **kw):
        super(CementBaseController, self).__init__(*args, **kw)
        
        self.app = None
        self.command = 'default'
        self.config = None
        self.log = None
        self.pargs = None
        self.visible = {}
        self.hidden = {}
        self.exposed = {}
        self._arguments = []
        
    def _setup(self, app_obj):
        """
        See `IController._setup() <#cement.core.cache.IController._setup>`_.
        """
        super(CementBaseController, self)._setup(app_obj)

        if self._meta.description is None:
            self._meta.description = "%s Controller" % \
                self._meta.label.capitalize()
        
        # shortcuts
        self.config = self.app.config
        self.log = self.app.log
        self.pargs = self.app.pargs
        self.render = self.app.render
        self._collect()
        
             
    def _parse_args(self):
        """
        Parses command line arguments and determine a command to dispatch.
        
        """
        # chop off a command argument if it matches an exposed command
        if len(self.app.argv) > 0 and not self.app.argv[0].startswith('-'):
            
            # translate dashes back to underscores
            cmd = re.sub('-', '_', self.app.argv[0])
            if cmd in self.exposed:
                self.command = cmd
                self.app.argv.pop(0)
            else:
                # FIX ME: This seems inefficient.  Would be better to have an
                # alias map... with key: controller_label.func_name
                for label,func in self.exposed.items():
                    if self.app.argv[0] in func['aliases']:
                        self.command = func['label']
                        self.app.argv.pop(0)
                        break
                        
        self.app.args.description = self._help_text
        self.app.args.usage = self._usage_text
        self.app.args.formatter_class=self._meta.argument_formatter

        self.app._parse_args()
        self.pargs = self.app.pargs
        
    def _dispatch(self):
        """
        Takes the remaining arguments from self.app.argv and parses for a
        command to dispatch, and if so... dispatches it.
        
        """
        self._add_arguments_to_parser()
        self._parse_args()
                       
        if not self.command:
            LOG.debug("no command to dispatch")
        else:    
            func = self.exposed[self.command]     
            LOG.debug("dispatching command: %s.%s" % \
                      (func['controller'], func['label']))

            if func['controller'] == self._meta.label:
                getattr(self, func['label'])()
            else:
                controller = handler.get('controller', func['controller'])()
                controller._setup(self.app)
                getattr(controller, func['label'])()

    @expose(hide=True, help='default command')
    def default(self):
        """
        This is the default action if no arguments (sub-commands) are passed
        at command line.
        
        :raises: NotImplementedError
        
        """
        raise NotImplementedError
    
    def _add_arguments_to_parser(self):
        """
        Run after _collect().  Add the collected arguments to the apps
        argument parser.
        
        """
        for _args,_kwargs in self._arguments:
            self.app.args.add_argument(*_args, **_kwargs)
        
    def _collect_from_self(self):
        """
        Collect arguments from this controller.
        
        :raises: cement.core.exc.FrameworkError
            
        """
        # collect our Meta arguments
        for _args,_kwargs in self._meta.arguments:
            if (_args, _kwargs) not in self._arguments:
                self._arguments.append((_args, _kwargs))
           
        # epilog only good for non-stacked controllers
        if hasattr(self._meta, 'epilog'):
            if  not hasattr(self._meta, 'stacked_on') or \
                not self._meta.stacked_on:
                self.app.args.epilog = self._meta.epilog
             
        # collect exposed commands from ourself
        for member in dir(self):
            if member in self.ignored or member.startswith('_'):
                continue
                
            func = getattr(self, member)
            if hasattr(func, 'exposed'):
                func_dict = dict(
                    controller=self._meta.label,
                    label=func.label,
                    help=func.help,
                    aliases=func.aliases,
                    hide=func.hide,
                    )

                if func_dict['label'] == self._meta.label:
                    raise exc.FrameworkError(
                        "Controller command '%s' " % func_dict['label'] + \
                        "matches controller label.  Use 'default' instead."
                        )
                
                self.exposed[func.label] = func_dict
                    
                if func.hide:
                    self.hidden[func.label] = func_dict
                else:
                    if not getattr(self._meta, 'hide', None):
                        self.visible[func.label] = func_dict
                        
    def _collect_from_non_stacked_controller(self, controller):
        """
        Collect arguments from non-stacked controllers.
        
        :param controller: The controller to collect arguments from.
        :type controller: Uninstantiated controller class
                
        """
        contr = controller()
        LOG.debug('exposing %s controller' % contr._meta.label)
                
        func_dict = dict(
            controller=contr._meta.label,
            label=contr._meta.label,
            help=contr._meta.description,
            aliases=contr._meta.aliases, # for display only
            hide=False,
            )
            
        # expose the controller label as a sub command
        self.exposed[contr._meta.label] = func_dict
        if not getattr(contr._meta, 'hide', None):
            self.visible[contr._meta.label] = func_dict
                                        
    def _collect_from_stacked_controller(self, controller):     
        """
        Collect arguments from stacked controllers.
        
        :param controller: The controller to collect arguments from.
        :type controller: Uninstantiated controller class
        :raises: cement.core.exc.FrameworkError
                
        """           
        contr = controller()
        contr._setup(self.app)
        contr._collect()
        
        # add stacked arguments into ours
        for _args,_kwargs in contr._arguments:
            if (_args, _kwargs) not in self._arguments:
                self._arguments.append((_args, _kwargs))
            
        # add stacked commands into ours              

        # determine hidden vs. visible commands
        func_dicts = contr.exposed
        for label in func_dicts:
            if label in self.exposed:  
                if label == 'default':
                    LOG.debug(
                        "ignoring duplicate command '%s' " % label + \
                        "found in '%s' " % contr._meta.label + \
                        "controller."
                        )
                    continue
                else:
                    raise exc.FrameworkError(
                        "Duplicate command '%s' " % label + \
                        "found in '%s' " % contr._meta.label + \
                        "controller."
                        )
            if func_dicts[label]['hide']:
                self.hidden[label] = func_dicts[label]
            elif not getattr(contr._meta, 'hide', False):
                self.visible[label] = func_dicts[label]
            self.exposed[label] = func_dicts[label]

    def _collect_from_controllers(self):
        """Collect arguments from all controllers."""
        
        for controller in handler.list('controller'):
            contr = controller()
            if contr._meta.label == self._meta.label:
                continue
                
            # expose other controllers as commands also
            if not hasattr(contr._meta, 'stacked_on') \
               or contr._meta.stacked_on is None:
                # only show non-stacked controllers under base
                if self._meta.label == 'base':
                    self._collect_from_non_stacked_controller(controller)         
            elif contr._meta.stacked_on == self._meta.label:
                self._collect_from_stacked_controller(controller)

    def _collect(self):
        """
        Collects all commands and arguments from this controller, and other
        availble controllers.
        
        :raises: cement.core.exc.FrameworkError
            
        """
        
        LOG.debug("collecting arguments and commands from '%s' controller" % \
                  self)
                  
        self.visible = {}
        self.hidden = {}
        self.exposed = {}
        self._arguments = []
        
        self._collect_from_self()
        self._collect_from_controllers()
        self._check_for_duplicates_on_aliases()
        
    def _check_for_duplicates_on_aliases(self):
        known_aliases = {}
        for label in self.exposed:
            func = self.exposed[label]
            for alias in func['aliases']:
                if alias in known_aliases:
                    raise exc.FrameworkError(
                        "Alias '%s' " % alias + \
                        "from the '%s' controller " % func['controller'] + \
                        "collides with an alias of the same name " + \
                        "in the '%s' controller." % known_aliases[alias]['controller']
                        )
                elif alias in self.exposed.keys():
                    raise exc.FrameworkError(
                        "Alias '%s' " % alias + \
                        "from the '%s' controller " % func['controller'] + \
                        "collides with a command of the same name in the " + \
                        "'%s' " % self.exposed[alias]['controller'] + \
                        "controller."
                        )
                known_aliases[alias] = func
                        
    @property
    def _usage_text(self):
        """Returns the usage text displayed when '--help' is passed."""
        
        if self._meta.usage is not None:
            return self._meta.usage
            
        if self == self.app._meta.base_controller:
            txt = "%s <CMD> -opt1 --opt2=VAL [arg1] [arg2] ..." % \
                self.app.args.prog
        else:
            txt = "%s %s <CMD> -opt1 --opt2=VAL [arg1] [arg2] ..." % \
                  (self.app.args.prog, self._meta.label)
        return txt
        
    @property
    def _help_text(self):
        """Returns the help text displayed when '--help' is passed."""
        
        cmd_txt = ''
        
        # hack it up to keep commands in alphabetical order
        sorted_labels = []
        for label in list(self.visible.keys()):
            old_label = label
            label = re.sub('_', '-', label)
            sorted_labels.append(label)
            
            if label != old_label:
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
    
        if len(cmd_txt) > 0:
            txt = '''%s

commands:

%s

        
        ''' % (self._meta.description, cmd_txt)
        else:
            txt = self._meta.description
        
        return textwrap.dedent(txt)        
