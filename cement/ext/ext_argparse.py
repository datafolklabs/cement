"""Argparse Framework Extension"""

import re
import argparse
import sys
from argparse import ArgumentParser
from ..core import backend, arg, handler, hook
from ..core.controller import IController
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)

def _clean_command_label(label):
    return re.sub('_', '-', label)

def _clean_command_func(func):
    return re.sub('-', '_', func)

class ArgparseArgumentHandler(arg.CementArgumentHandler, ArgumentParser):

    """
    This class implements the :ref:`IArgument <cement.core.arg>`
    interface, and sub-classes from `argparse.ArgumentParser
    <http://docs.python.org/dev/library/argparse.html>`_.
    Please reference the argparse documentation for full usage of the
    class.

    Arguments and Keyword arguments are passed directly to ArgumentParser
    on initialization.
    """

    class Meta:

        """Handler meta-data."""

        interface = arg.IArgument
        """The interface that this class implements."""

        label = 'argparse'
        """The string identifier of the handler."""

    def __init__(self, *args, **kw):
        super(ArgparseArgumentHandler, self).__init__(*args, **kw)
        self.config = None

    def parse(self, arg_list):
        """
        Parse a list of arguments, and return them as an object.  Meaning an
        argument name of 'foo' will be stored as parsed_args.foo.

        :param arg_list: A list of arguments (generally sys.argv) to be
         parsed.
        :returns: object whose members are the arguments parsed.

        """
        args = self.parse_args(arg_list)
        return args

    def add_argument(self, *args, **kw):
        """
        Add an argument to the parser.  Arguments and keyword arguments are
        passed directly to ArgumentParser.add_argument().

        """
        return super(ArgumentParser, self).add_argument(*args, **kw)


# FIXME: Backward compat name, will remove in Cement 3.x
class ArgParseArgumentHandler(ArgparseArgumentHandler):
    pass


class expose(object):

    """
    Used to expose controller functions to be listed as commands, and to
    decorate the function with Meta data for the argument parser.

    :param hide: Whether the command should be visible.
    :type hide: boolean
    :param arguments: List of tuples that define arguments to add to this 
     command sub-parser.
    :keyword parser_options: Additional options to pass to Argparse.
    :type parser_options: dict

    Usage:

    .. code-block:: python

        from cement.core.controller import CementBaseController, expose

        class MyAppBaseController(CementBaseController):
            class Meta:
                label = 'base'

            # Note: Default functions only work on Python 3.4+
            @expose(hide=True)
            def default(self):
                print("In MyAppBaseController.default()")

            @expose(
                help='this is the help message for my_command',
                aliases=['my_cmd'], # only available in Python 3+
                arguments=[
                    (['-f', '--foo'], 
                     dict(help='foo option', action='store', dest='foo')),
                ]
            )
            def my_command(self):
                print("In MyAppBaseController.my_command()")

    """
    # pylint: disable=W0622

    def __init__(self, hide=False, arguments=[], **parser_options):
        self.hide = hide

        ### FIX ME: Not Implemented
        self.arguments = arguments
        self.parser_options = parser_options

    def __call__(self, func):
        metadict = {}
        metadict['label'] = _clean_command_label(func.__name__)
        metadict['func_name'] = func.__name__
        metadict['exposed'] = True
        metadict['hide'] = self.hide
        metadict['arguments'] = self.arguments
        metadict['parser_options'] = self.parser_options
        metadict['controller'] = None  # added by the controller
        func.__cement_meta__ = metadict
        return func

class ArgparseController(handler.CementBaseHandler):
    """
    This is an implementation of the
    `IControllerHandler <#cement.core.controller.IController>`_ interface, but
    as a base class that application controllers `should` subclass from.
    Registering it directly as a handler is useless.

    NOTE: This handler **requires** that the applications 'arg_handler' be
    argparse.  If using an alternative argument handler you will need to
    write your own controller base class or modify this one.

    NOTE: This is a re-implementation of CementBaseController.  In the future,
    this class will eventually replace CementBaseController.

    Usage:

    .. code-block:: python

        from cement.ext.ext_argparse import ArgparseController

        class MyAppBaseController(ArgparseController):
            class Meta:
                label = 'base'
                description = 'MyApp is awesome'
                config_defaults = dict()
                arguments = []
                epilog = "This is the text at the bottom of --help."
                # ...

        class MyStackedController(ArgparseController):
            class Meta:
                label = 'second_controller'
                aliases = ['sec', 'secondary']
                stacked_on = 'base'
                stacked_type = 'embedded'
                # ...

    """

    class Meta:

        """
        Controller meta-data (can be passed as keyword arguments to the parent
        class).

        """

        #: The interface this class implements.
        interface = IController

        #: The string identifier for the controller.
        label = 'base'

        #: A list of aliases for the controller/sub-parser.  **Only available
        #: in Python 3+.
        aliases = []

        #: A config [section] to merge config_defaults into.  Cement will
        #: default to controller.<label> if None is set.
        config_section = None

        #: Configuration defaults (type: dict) that are merged into the
        #: applications config object for the config_section mentioned above.
        config_defaults = {}

        #: Arguments to pass to the argument_handler.  The format is a list
        #: of tuples whos items are a ( list, dict ).  Meaning:
        #:
        #: ``[ ( ['-f', '--foo'], dict(dest='foo', help='foo option') ), ]``
        #:
        #: This is equivelant to manually adding each argument to the argument
        #: parser as in the following example:
        #:
        #: ``parser.add_argument('-f', '--foo',
        #:                       help='foo option', dest='foo')``
        arguments = []

        #: A label of another controller to 'stack' commands/arguments on top
        #: of.
        stacked_on = 'base'

        #: Whether to `embed` commands and arguments within the parent
        #: controller or to simply ``nest`` the controller under the parent
        #: controller (making it a sub-sub-command).  Must be one of
        #: ``['embedded', 'nested']`` only if ``stacked_on`` is not ``None``.
        stacked_type = 'embedded'

        #: Description for the sub-parser group in help output.
        description = None

        #: The title for the sub-parser group in help output.
        title = 'sub-commands'

        #: Text for the controller/sub-parser group in help output (for
        #: nested stacked controllers only).
        help = None

        #: Whether or not to hide the controller entirely.
        hide = False

        #: The text that is displayed at the bottom when '--help' is passed. 
        epilog = None

        #: The text that is displayed at the top when '--help' is passed.
        #: Defaults to Argparse standard usage.
        usage = None

        #: Additional keyword arguments passed when 
        #: ``ArgumentParser.add_subparsers()`` is called to create this 
        #: controller namespace.  WARNING: This could break things, use at 
        #: your own risk.  Useful if you need additional features from 
        #: Argparse that is not built into the controller Meta-data.
        subparser_options = {}

        #: Additional keyword arguments passed when 
        #: ``ArgumentParser.add_parser()`` is called to create this 
        #: controller sub-parser.  WARNING: This could break things, use at 
        #: your own risk.  Useful if you need additional features from 
        #: Argparse that is not built into the controller Meta-data.
        parser_options = {}

        #: Function to call if no sub-command is passed.  Note that this can
        #: **not** start with an ``_`` due to backward compatibility 
        #: restraints in how Cement discovers and maps commands.
        #:
        #: Note: Currently, default function/sub-command only functions on 
        #: Python 3.4+.  Previous versions of Python/Argparse will throw the 
        #: exception ``error: too few arguments``.
        default_func = 'default'
        

    def __init__(self, *args, **kw):
        super(ArgparseController, self).__init__(*args, **kw)
        self.app = None
        self._sub_parser_parents = dict()
        self._sub_parsers = dict()
        self._controllers = []
        self._controllers_map = {}

        if self._meta.help is None:
            self._meta.help = '%s controller' % self._meta.label

    def _setup(self, app):
        """
        See `IController._setup() <#cement.core.cache.IController._setup>`_.
        """
        super(ArgparseController, self)._setup(app)
        self.app = app

    def _setup_controllers(self):
        # note this is only called on base controller, so self == 'base'

        resolved_controllers = []
        unresolved_controllers = []
        for contr in handler.list('controller'):
            # don't include self
            if contr == self.__class__:
                continue

            contr = contr()
            contr._setup(self.app)
            unresolved_controllers.append(contr)

        # treat base/self separately
        resolved_controllers.append(self)

        # all this crazy shit is to resolve controllers in the order that they
        # are nested/embedded, otherwise argparse does weird things

        LOG.debug('resolving controller nesting/embedding order')

        current_parent = self._meta.label
        while unresolved_controllers:
            # handle all controllers nested on parent
            current_children = []
            resolved_child_controllers = []
            for contr in list(unresolved_controllers):
                if contr._meta.stacked_on == current_parent:
                    current_children.append(contr)
                    if contr._meta.stacked_type == 'embedded':
                        resolved_child_controllers.append(contr)
                    else:
                        resolved_child_controllers.insert(0, contr)
                    unresolved_controllers.remove(contr)
                    LOG.debug('resolve controller %s' % contr)

            resolved_controllers.extend(resolved_child_controllers)

            # then, for all those controllers... handler all controllers 
            # nested on them
            resolved_child_controllers = []
            for child_contr in current_children:
                for contr in list(unresolved_controllers):
                    if contr._meta.stacked_on == child_contr._meta.label:
                        if contr._meta.stacked_type == 'embedded':
                            resolved_child_controllers.append(contr)
                        else:
                            
                            resolved_child_controllers.insert(0, contr)

                        unresolved_controllers.remove(contr)
                        LOG.debug('resolve controller %s' % contr)

            resolved_controllers.extend(resolved_child_controllers)
            # re-iterate with the next in line as the parent (handles multiple
            # level nesting)
            if unresolved_controllers:
                current_parent = unresolved_controllers[0]._meta.label

        
        self._controllers = resolved_controllers

        # so that we can look up by controller label in self._dispatch
        for contr in resolved_controllers:
            self._controllers_map[contr._meta.label] = contr

    def _process_parsed_arguments(self):
        pass

    def _get_subparser_options(self, contr):
        kwargs = contr._meta.subparser_options.copy()

        if 'title' not in kwargs.keys():
            kwargs['title'] = contr._meta.title

        kwargs['dest'] = '__subparser__'

        return kwargs

    def _get_parser_options(self, contr):
        kwargs = contr._meta.parser_options.copy()

        if sys.version_info[0] > 3:
            if 'aliases' not in kwargs.keys():
                kwargs['aliases'] = contr._meta.aliases

        if 'description' not in kwargs.keys():
            kwargs['description'] = contr._meta.description
        if 'usage' not in kwargs.keys():
            kwargs['usage'] = contr._meta.usage
        if 'epilog' not in kwargs.keys():
            kwargs['epilog'] = contr._meta.epilog

        if contr._meta.hide == True:
            if 'help' in kwargs.keys():
                del kwargs['help']
        else:
            kwargs['help'] = contr._meta.help

        return kwargs

    def _get_command_parser_options(self, command):
        kwargs = command['parser_options'].copy()

        contr = command['controller']

        hide_it = False
        if command['hide'] == True:
            hide_it = True

        # only hide commands from embedded controllers if the controller is
        # hidden
        elif contr._meta.stacked_type == 'embedded' \
            and contr._meta.hide == True:
            hide_it = True
        
        if hide_it == True:
            if 'help' in kwargs:
                del kwargs['help']

        return kwargs

    def _setup_parsers(self):
        # this should only be run by the base controller
        if not self._meta.label == 'base':
            raise FrameworkError('Private function _setup_parsers() called'
                                 'from non-base controller')

        from cement.utils.misc import rando
        
        _rando = rando()[:12]
        self._dispatch_option = '--dispatch-%s' % _rando
        self._controller_option = '--controller-namespace-%s' % _rando


        # parents are sub-parser namespaces (that we can add subparsers to)
        # where-as parsers are the actual root parser and sub-parsers to
        # add arguments to
        parents = self._sub_parser_parents
        parsers = self._sub_parsers
        parsers['base'] = self.app.args

        # handle base controller separately
        parsers['base'].add_argument(self._controller_option,
            action='store',
            default='base',
            nargs='?',
            help=argparse.SUPPRESS,
            dest='__controller_namespace__',
            )

        kwargs = self._get_subparser_options(self)
        sub = self.app.args.add_subparsers(**kwargs)
        parents['base'] = sub
        base_parser_options = self._get_parser_options(self)
        for key,val in base_parser_options.items():
            setattr(self.app.args, key, val)

        # and if only base controller registered... go ahead and return
        if len(handler.list('controller')) <= 1:
            return

        # note that the order of self._controllers was already organized by
        # stacking/embedding order in self._setup_controllers ... order is
        # important here otherwise argparse does wierd things
        for contr in self._controllers:
            label = contr._meta.label
            stacked_on = contr._meta.stacked_on
            stacked_type = contr._meta.stacked_type

            if stacked_type == 'nested':
                # if the controller is nested, we need to create a new parser
                # parent using the one that it is stacked on, as well as as a
                # new parser
                kwargs = self._get_parser_options(contr)
                parsers[label] = parents[stacked_on].add_parser(
                                    label,
                                    **kwargs
                                    )

                # we also need to add subparsers to this parser so we can
                # attach commands and other nested controllers to it
                kwargs = self._get_subparser_options(contr)
                parents[label] = parsers[label].add_subparsers(**kwargs)

                # add an invisible controller option so we can figure out what 
                # to call later in self._dispatch
                parsers[label].add_argument(self._controller_option,
                    action='store',
                    default=contr._meta.label,
                    help=argparse.SUPPRESS,
                    dest='__controller_namespace__',
                    )

            elif stacked_type == 'embedded':
                # if it's embedded, then just set it to use the same as the
                # controller its stacked on
                parents[label] = parents[stacked_on]
                parsers[label] = parsers[stacked_on]

    def _get_parser_by_controller(self, controller):
        if controller._meta.stacked_on:
            if controller._meta.stacked_type == 'embedded':
                parser = self._get_parser(controller._meta.stacked_on)
            else:
                parser = self._get_parser(controller._meta.label)
        else:
            parser = self._get_parser(controller._meta.label)

        return parser

    def _get_parser_parent_by_controller(self, controller):
        if controller._meta.stacked_on:
            if controller._meta.stacked_type == 'embedded':
                parent = self._get_parser_parent(controller._meta.stacked_on)
            else:
                parent = self._get_parser_parent(controller._meta.label)
        else:
            parent = self._get_parser_parent(controller._meta.label)

        return parent

    def _get_parser_parent(self, label):
        return self._sub_parser_parents[label]

    def _get_parser(self, label):
        return self._sub_parsers[label]

    def _process_arguments(self, controller):
        label = controller._meta.label

        LOG.debug("processing arguments for '%s' " % label + \
                           "controller namespace")

        parser = self._get_parser_by_controller(controller)
        arguments = controller._collect_arguments()
        for arg, kw in arguments:
            try:
                LOG.debug('adding argument (args=%s, kwargs=%s)' % \
                                  (arg, kw))
                parser.add_argument(*arg, **kw)
            except argparse.ArgumentError as e:
                raise exc.FrameworkError(e.__str__())

    def _process_commands(self, controller):
        label = controller._meta.label
        LOG.debug("processing commands for '%s' " % label + \
                           "controller namespace")
        parser = self._get_parser_by_controller(controller)

        commands = controller._collect_commands()
        for command in commands:
            kwargs = self._get_command_parser_options(command)

            func_name = command['func_name']
            LOG.debug("adding command '%s' " % command['label'] + \
                      "(controller=%s, func=%s)" % \
                      (controller._meta.label, func_name))

            cmd_parent = self._get_parser_parent_by_controller(controller)
            command_parser = cmd_parent.add_parser(command['label'], **kwargs)

            # add an invisible dispatch option so we can figure out what to 
            # call later in self._dispatch
            command_parser.add_argument(self._dispatch_option,
                action='store',
                default="%s.%s" % (command['controller']._meta.label, 
                                   command['func_name']),
                help=argparse.SUPPRESS,
                dest='__dispatch__',
                )
        
            # add additional arguments to the sub-command namespace
            LOG.debug("processing arguments for '%s' " % command['label'] + \
                      "command namespace")
            for arg, kw in command['arguments']:
                try:
                    LOG.debug('adding argument (args=%s, kwargs=%s)' % \
                                      (arg, kw))
                    command_parser.add_argument(*arg, **kw)
                except argparse.ArgumentError as e:
                    raise exc.FrameworkError(e.__str__())

    def _collect(self):
        arguments = self._collect_arguments()
        commands = self._collect_commands()
        return (arguments, commands)

    def _collect_arguments(self):
        LOG.debug("collecting arguments from %s " % self +
                  "(stacked_on='%s', stacked_type='%s')" % \
                  (self._meta.stacked_on, self._meta.stacked_type))
        return self._meta.arguments

    def _collect_commands(self):
        LOG.debug("collecting commands from %s " % self +
                  "(stacked_on='%s', stacked_type='%s')" % \
                  (self._meta.stacked_on, self._meta.stacked_type))
        
        commands = []
        for member in dir(self.__class__):
            if member.startswith('_'):
                continue
            elif hasattr(getattr(self, member), '__cement_meta__'):
                func = getattr(self.__class__, member).__cement_meta__
                func['controller'] = self
                commands.append(func)

        return commands

    def _dispatch(self):
        LOG.debug("controller dispatch passed off to %s" % self)
        self._setup_controllers()
        self._setup_parsers()

        for contr in self._controllers:
            self._process_arguments(contr)
            self._process_commands(contr)

        self.app._parse_args()

        for contr in self._controllers:
            contr._process_parsed_arguments()
        
        if hasattr(self.app.pargs, '__dispatch__'):
            # if __dispatch__ is set that means that we have hit a sub-command
            # of a controller.
            contr_label = self.app.pargs.__dispatch__.split('.')[0]
            func_name = self.app.pargs.__dispatch__.split('.')[1]
        else:
            # if no __dispatch__ is set then that means we have hit a 
            # controller with not sub-command (argparse doesn't support 
            # default sub-command yet... so we rely on 
            # __controller_namespace__ and it's default func
            contr_label = self.app.pargs.__controller_namespace__
            func_name = _clean_command_func(contr._meta.default_func)

        if contr_label == 'base':
            contr = self
        else:
            contr = self._controllers_map[contr_label]

        if hasattr(contr, func_name):
            func = getattr(contr, func_name)
            return func()
        else:
            self.app.log.fatal(
                "Controller function does not exist " + \
                "%s.%s()" % (contr.__class__, func_name))
            return None

def load(app):
    handler.register(ArgparseArgumentHandler)
