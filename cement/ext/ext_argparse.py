"""
The Argparse Extension provides argument handling based on
:py:class:`argparse.ArgumentParser`, and is the default argument handler
used by :class:`cement.core.foundation.CementApp`.  In addition, this
extension also provides :class:`ArgparseController` that enables rapid
development via application controllers based on Argparse.

Requirements
------------

 * Python 2.7+, Python 3+
 * Some features of :class:`ArgparseController` are only available in Python
   3 including controller and function/command ``aliases`` (Python 3+) and
   controller default functions/command (Python 3.4+).


Configuration
-------------

This extension does not have any application configuration settings.


Usage
-----

The following is an example application using both the
:class:`ArgparseArgumentHandler` and :class:`ArgparseController`.  Note that
the default ``arg_handler`` is already set to
:class:`ArgparseArgumentHandler`` by :class:`CementApp`.

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.ext.ext_argparse import ArgparseController, expose


    class BaseController(ArgparseController):
        class Meta:
            label = 'base'
            arguments = [
                (['--base-foo'], dict(help='base foo option')),
            ]

        @expose(hide=True)
        def default(self):
            # Note: Default commands are only available in Python 3.4+
            print('Inside BaseController.default')

            if self.app.pargs.base_foo:
                # do something with self.app.pargs.base_foo
                print('Base Foo > %s' % self.app.pargs.base_foo)

        @expose(
            arguments=[
                (['--command1-opt'],
                 dict(help='option under command1', action='store_true'))
            ],
            aliases=['cmd1'],
            help='command1 is a sub-command under myapp base controller',
        )
        def command1(self):
            print('Inside BaseController.command1')

            if self.app.pargs.command1_opt:
                # do something with self.app.pargs.command1_opt
                pass


    class EmbeddedController(ArgparseController):
        class Meta:
            label = 'embedded_controller'
            stacked_on = 'base'
            stacked_type = 'embedded'

        @expose(help="command2 embedded under base controller")
        def command2(self):
            print('Inside EmbeddedController.command2')


    class NestedController(ArgparseController):
        class Meta:
            label = 'nested_controller'
            stacked_on = 'base'
            stacked_type = 'nested'
            arguments = [
                (['--nested-opt'],
                 dict(help='option under nested-controller')),
            ]

        @expose(help="command3 under nested-controller")
        def command3(self):
            print('Inside NestedController.command3')


    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            handlers = [
                BaseController,
                EmbeddedController,
                NestedController
            ]


    with MyApp() as app:
        app.run()


The above looks like:

.. code-block:: console

    $ python myapp.py --help
    usage: myapp.py [-h] [--debug] [--quiet] [--base-foo BASE_FOO]
                    {nested-controller,command1,cmd1,default,command2} ...

    optional arguments:
      -h, --help            show this help message and exit
      --debug               toggle debug output
      --quiet               suppress all output
      --base-foo BASE_FOO   base foo option

    sub-commands:
      {nested-controller,command1,cmd1,default,command2}
        nested-controller   nested-controller controller
        command1 (cmd1)     command1 is a sub-command under base controller
        command2            command2 embedded under base controller


    $ python myapp.py --base-foo bar
    Inside BaseController.default
    Base Foo > bar


    $ python myapp.py command1 --help
    usage: myapp.py command1 [-h] [--command1-opt]

    optional arguments:
      -h, --help      show this help message and exit
      --command1-opt  option under command1


    $ python myapp.py command1
    Inside BaseController.command1


    $ python myapp.py command2
    Inside EmbeddedController.command2


    $ python myapp.py nested-controller --help
    usage: myapp.py nested-controller [-h] [--nested-opt] {command3} ...

    optional arguments:
      -h, --help            show this help message and exit
      --nested-opt          option under nested-controller

    sub-commands:
      {command3}
        command3            command3 under nested-controller


    $ python myapp.py nested-controller command3
    Inside NestedController.command3

"""

import re
import sys
from argparse import ArgumentParser, SUPPRESS
from ..core.handler import CementBaseHandler
from ..core.arg import CementArgumentHandler, IArgument
from ..core.controller import IController
from ..core.exc import FrameworkError
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


def _clean_label(label):
    return re.sub('_', '-', label)


def _clean_func(func):
    return re.sub('-', '_', func)


class ArgparseArgumentHandler(ArgumentParser, CementArgumentHandler):

    """
    This class implements the :class:`cement.core.arg.IArgument`
    interface, and sub-classes from :py:class:`argparse.ArgumentParser`.
    Please reference the argparse documentation for full usage of the
    class.

    Arguments and Keyword arguments are passed directly to ArgumentParser
    on initialization.
    """

    class Meta:

        """Handler meta-data."""

        interface = IArgument
        """The interface that this class implements."""

        label = 'argparse'
        """The string identifier of the handler."""

        ignore_unknown_arguments = False
        """
        Whether or not to ignore any arguments passed that are not defined.
        Default behavoir by Argparse is to raise an "unknown argument"
        exception by Argparse.

        This affectively triggers the difference between using ``parse_args``
        and ``parse_known_args``.  Unknown arguments will be accessible as
        ``unknown_args``.
        """

    def __init__(self, *args, **kw):
        super(ArgparseArgumentHandler, self).__init__(*args, **kw)
        self.config = None
        self.unknown_args = None
        self.parsed_args = None

    def parse(self, arg_list):
        """
        Parse a list of arguments, and return them as an object.  Meaning an
        argument name of 'foo' will be stored as parsed_args.foo.

        :param arg_list: A list of arguments (generally sys.argv) to be
         parsed.
        :returns: object whose members are the arguments parsed.

        """
        if self._meta.ignore_unknown_arguments is True:
            args, unknown = self.parse_known_args(arg_list)
            self.parsed_args = args
            self.unknown_args = unknown
        else:
            args = self.parse_args(arg_list)
            self.parsed_args = args
        return self.parsed_args

    def add_argument(self, *args, **kw):
        """
        Add an argument to the parser.  Arguments and keyword arguments are
        passed directly to ``ArgumentParser.add_argument()``.
        See the :py:class:`argparse.ArgumentParser` documentation for help.
        """
        super(ArgparseArgumentHandler, self).add_argument(*args, **kw)


# FIXME: Backward compat name, will remove in Cement 3.x
class ArgParseArgumentHandler(ArgparseArgumentHandler):
    pass


class expose(object):

    """
    Used to expose functions to be listed as sub-commands under the
    controller namespace.  It also decorates the function with meta-data for
    the argument parser.

    :param hide: Whether the command should be visible.
    :type hide: ``boolean``
    :param arguments: List of tuples that define arguments to add to this
     commands sub-parser.
    :keyword parser_options: Additional options to pass to Argparse.
    :type parser_options: ``dict``

    Usage:

    .. code-block:: python

        from cement.ext.ext_argparse import ArgparseController, expose

        class Base(ArgparseController):
            class Meta:
                label = 'base'

            # Note: Default functions only work in Python > 3.4
            @expose(hide=True)
            def default(self):
                print("In Base.default()")

            @expose(
                help='this is the help message for my_command',
                aliases=['my_cmd'], # only available in Python 3+
                arguments=[
                    (['-f', '--foo'],
                     dict(help='foo option', action='store', dest='foo')),
                ]
            )
            def my_command(self):
                print("In Base.my_command()")

    """
    # pylint: disable=W0622

    def __init__(self, hide=False, arguments=[], **parser_options):
        self.hide = hide

        # FIX ME: Not Implemented
        self.arguments = arguments
        self.parser_options = parser_options

    def __call__(self, func):
        metadict = {}
        metadict['label'] = _clean_label(func.__name__)
        metadict['func_name'] = func.__name__
        metadict['exposed'] = True
        metadict['hide'] = self.hide
        metadict['arguments'] = self.arguments
        metadict['parser_options'] = self.parser_options
        metadict['controller'] = None  # added by the controller
        func.__cement_meta__ = metadict
        return func

# FIX ME: Should be refactored into separate BaseController and Controller
# classes in Cement 3, but that would break the interface spec in 2.x


class ArgparseController(CementBaseHandler):

    """
    This is an implementation of the
    :class:`cement.core.controller.IController` interface, but as a base class
    that application controllers should subclass from.  Registering it
    directly as a handler is useless.

    NOTE: This handler **requires** that the applications ``arg_handler`` be
    ``argparse``.  If using an alternative argument handler you will need to
    write your own controller base class or modify this one.

    NOTE: This is a re-implementation of
    :class:`cement.core.controller.CementBaseController`.
    In the future, this class will eventually replace it as the default.

    Usage:

    .. code-block:: python

        from cement.ext.ext_argparse import ArgparseController

        class Base(ArgparseController):
            class Meta:
                label = 'base'
                description = 'description at the top of --help'
                epilog = "the text at the bottom of --help."
                arguments = [
                    (['-f', '--foo'], dict(help='my foo option', dest='foo')),
                ]

        class Second(ArgparseController):
            class Meta:
                label = 'second'
                stacked_on = 'base'
                stacked_type = 'embedded'
                arguments = [
                    (['--foo2'], dict(help='my foo2 option', dest='foo2')),
                ]

    """

    class Meta:

        """
        Controller meta-data (can be passed as keyword arguments to the parent
        class).

        """

        # The interface this class implements.
        interface = IController

        #: The string identifier for the controller.
        label = 'base'

        #: A list of aliases for the controller/sub-parser.  **Only available
        #: in Python > 3**.
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
        #: ``[ ( ['-f', '--foo'], dict(help='foo option', dest='foo') ), ]``
        #:
        #: This is equivelant to manually adding each argument to the argument
        #: parser as in the following example:
        #:
        #: ``add_argument('-f', '--foo', help='foo option', dest='foo')``
        arguments = []

        #: A label of another controller to 'stack' commands/arguments on top
        #: of.
        stacked_on = 'base'

        #: Whether to embed commands and arguments within the parent
        #: controller's namespace, or to nest this controller under the parent
        #: controller (making it a sub-command).  Must be one of
        #: ``['embedded', 'nested']``.
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

        #: The text that is displayed at the bottom when ``--help`` is passed.
        epilog = None

        #: The text that is displayed at the top when ``--help`` is passed.
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
        #: Python > 3.4.  Previous versions of Python/Argparse will throw the
        #: exception ``error: too few arguments``.
        default_func = 'default'

    def __init__(self, *args, **kw):
        super(ArgparseController, self).__init__(*args, **kw)
        self.app = None
        self._parser = None

        if self._meta.label == 'base':
            self._sub_parser_parents = dict()
            self._sub_parsers = dict()
            self._controllers = []
            self._controllers_map = {}

        if self._meta.help is None:
            self._meta.help = '%s controller' % _clean_label(self._meta.label)

    def _setup(self, app):
        """
        See `IController._setup() <#cement.core.cache.IController._setup>`_.
        """
        super(ArgparseController, self)._setup(app)
        self.app = app

    def _setup_controllers(self):
        # need a list to maintain order
        resolved_controllers = []

        # need a dict to do key/label based lookup
        resolved_controllers_map = {}

        # list to maintain which controllers we haven't resolved yet
        unresolved_controllers = []
        for contr in self.app.handler.list('controller'):
            # don't include self/base
            if contr == self.__class__:
                continue

            contr = contr()
            contr._setup(self.app)
            unresolved_controllers.append(contr)

        # treat self/base separately
        resolved_controllers.append(self)
        resolved_controllers_map['base'] = self

        # all this crazy shit is to resolve controllers in the order that they
        # are nested/embedded, otherwise argparse does weird things

        LOG.debug('resolving controller nesting/embedding order')

        current_parent = self._meta.label
        while unresolved_controllers:
            LOG.debug('unresolved controllers > %s' % unresolved_controllers)
            LOG.debug('current parent > %s' % current_parent)

            # handle all controllers nested on parent
            current_children = []
            resolved_child_controllers = []
            for contr in list(unresolved_controllers):
                # if stacked_on is the current parent, we want to process
                # its children in this run first
                if contr._meta.stacked_on == current_parent:
                    current_children.append(contr)
                    if contr._meta.stacked_type == 'embedded':
                        resolved_child_controllers.append(contr)
                    else:
                        resolved_child_controllers.insert(0, contr)
                    unresolved_controllers.remove(contr)
                    LOG.debug('resolved controller %s %s on %s' %
                              (contr, contr._meta.stacked_type,
                               current_parent))

                # if not, fall back on whether the stacked_on parent is
                # already resolved
                elif contr._meta.stacked_on in resolved_controllers_map.keys():
                    resolved_controllers.append(contr)
                    resolved_controllers_map[contr._meta.label] = contr
                    unresolved_controllers.remove(contr)
                    LOG.debug('resolved controller %s %s on %s' %
                              (contr, contr._meta.stacked_type,
                               contr._meta.stacked_on))

            resolved_controllers.extend(resolved_child_controllers)
            for contr in resolved_child_controllers:
                resolved_controllers_map[contr._meta.label] = contr

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
                        LOG.debug('resolved controller %s %s on %s' %
                                  (contr, contr._meta.stacked_type,
                                   child_contr._meta.label))

            resolved_controllers.extend(resolved_child_controllers)
            for contr in resolved_child_controllers:
                resolved_controllers_map[contr._meta.label] = contr

            # re-iterate with the next in line as the parent (handles multiple
            # level nesting)
            if unresolved_controllers:
                current_parent = unresolved_controllers[0]._meta.label

        self._controllers = resolved_controllers
        self._controllers_map = resolved_controllers_map

    def _process_parsed_arguments(self):
        pass

    def _get_subparser_options(self, contr):
        kwargs = contr._meta.subparser_options.copy()

        if 'title' not in kwargs.keys():
            kwargs['title'] = contr._meta.title

        kwargs['dest'] = 'command'

        return kwargs

    def _get_parser_options(self, contr):
        kwargs = contr._meta.parser_options.copy()

        if sys.version_info[0] >= 3:
            if 'aliases' not in kwargs.keys():              # pragma: nocover
                kwargs['aliases'] = contr._meta.aliases     # pragma: nocover

        if 'description' not in kwargs.keys():
            kwargs['description'] = contr._meta.description
        if 'usage' not in kwargs.keys():
            kwargs['usage'] = contr._meta.usage
        if 'epilog' not in kwargs.keys():
            kwargs['epilog'] = contr._meta.epilog
        if 'help' not in kwargs.keys():
            kwargs['help'] = contr._meta.help

        if contr._meta.hide is True:
            if 'help' in kwargs.keys():
                del kwargs['help']
        else:
            kwargs['help'] = contr._meta.help

        return kwargs

    def _get_command_parser_options(self, command):
        kwargs = command['parser_options'].copy()

        contr = command['controller']

        hide_it = False
        if command['hide'] is True:
            hide_it = True

        # only hide commands from embedded controllers if the controller is
        # hidden
        elif contr._meta.stacked_type == 'embedded' \
                and contr._meta.hide is True:
            hide_it = True

        if hide_it is True:
            if 'help' in kwargs:
                del kwargs['help']

        return kwargs

    def _setup_parsers(self):
        # this should only be run by the base controller
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
        # parsers['base'] = ArgumentParser()
        # sub1 = parsers['base'].add_subparsers(title='sub-commands')
        # sub1.add_parser('johnny')
        # parsers['base'].parse_args()

        kwargs = self._get_subparser_options(self)
        sub = self.app.args.add_subparsers(**kwargs)
        parents['base'] = sub
        base_parser_options = self._get_parser_options(self)
        for key, val in base_parser_options.items():
            setattr(self.app.args, key, val)

        # handle base controller separately
        parsers['base'].add_argument(self._controller_option,
                                     action='store',
                                     default='base',
                                     nargs='?',
                                     help=SUPPRESS,
                                     dest='__controller_namespace__',
                                     )
        self._parser = parsers['base']

        # and if only base controller registered... go ahead and return
        if len(self.app.handler.list('controller')) <= 1:
            return    # pragma: nocover

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
                    _clean_label(label),
                    **kwargs
                )

                contr._parser = parsers[label]

                # we need to add subparsers to this parser so we can
                # attach commands and other nested controllers to it
                kwargs = self._get_subparser_options(contr)
                parents[label] = parsers[label].add_subparsers(**kwargs)

                # add an invisible controller option so we can figure out what
                # to call later in self._dispatch
                parsers[label].add_argument(self._controller_option,
                                            action='store',
                                            default=contr._meta.label,
                                            help=SUPPRESS,
                                            dest='__controller_namespace__',
                                            )

            elif stacked_type == 'embedded':
                # if it's embedded, then just set it to use the same as the
                # controller its stacked on
                parents[label] = parents[stacked_on]
                parsers[label] = parsers[stacked_on]

    def _get_parser_by_controller(self, controller):
        if controller._meta.stacked_type == 'embedded':
            parser = self._get_parser(controller._meta.stacked_on)
        else:
            parser = self._get_parser(controller._meta.label)

        return parser

    def _get_parser_parent_by_controller(self, controller):
        if controller._meta.stacked_type == 'embedded':
            parent = self._get_parser_parent(controller._meta.stacked_on)
        else:
            parent = self._get_parser_parent(controller._meta.label)

        return parent

    def _get_parser_parent(self, label):
        return self._sub_parser_parents[label]

    def _get_parser(self, label):
        return self._sub_parsers[label]

    def _process_arguments(self, controller):
        label = controller._meta.label

        LOG.debug("processing arguments for '%s' " % label +
                  "controller namespace")

        parser = self._get_parser_by_controller(controller)
        arguments = controller._collect_arguments()
        for arg, kw in arguments:
            LOG.debug('adding argument (args=%s, kwargs=%s)' % (arg, kw))
            parser.add_argument(*arg, **kw)

    def _process_commands(self, controller):
        label = controller._meta.label
        LOG.debug("processing commands for '%s' " % label +
                  "controller namespace")

        commands = controller._collect_commands()
        for command in commands:
            kwargs = self._get_command_parser_options(command)

            func_name = command['func_name']
            LOG.debug("adding command '%s' " % command['label'] +
                      "(controller=%s, func=%s)" %
                      (controller._meta.label, func_name))

            cmd_parent = self._get_parser_parent_by_controller(controller)
            command_parser = cmd_parent.add_parser(command['label'], **kwargs)

            # add an invisible dispatch option so we can figure out what to
            # call later in self._dispatch
            default_contr_func = "%s.%s" % (command['controller']._meta.label,
                                            command['func_name'])
            command_parser.add_argument(self._dispatch_option,
                                        action='store',
                                        default=default_contr_func,
                                        help=SUPPRESS,
                                        dest='__dispatch__',
                                        )

            # add additional arguments to the sub-command namespace
            LOG.debug("processing arguments for '%s' " % command['label'] +
                      "command namespace")
            for arg, kw in command['arguments']:
                LOG.debug('adding argument (args=%s, kwargs=%s)' %
                          (arg, kw))
                command_parser.add_argument(*arg, **kw)

    def _collect(self):
        arguments = self._collect_arguments()
        commands = self._collect_commands()
        return (arguments, commands)

    def _collect_arguments(self):
        LOG.debug("collecting arguments from %s " % self +
                  "(stacked_on='%s', stacked_type='%s')" %
                  (self._meta.stacked_on, self._meta.stacked_type))
        return self._meta.arguments

    def _collect_commands(self):
        LOG.debug("collecting commands from %s " % self +
                  "(stacked_on='%s', stacked_type='%s')" %
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

    def _pre_argument_parsing(self):
        """
        Called on every controller just before arguments are parsed.
        Provides an alternative means of adding arguments to the controller,
        giving more control than using ``Meta.arguments``.

        .. code-block:: python

            class Base(ArgparseController):
                class Meta:
                    label = 'base'

                def _pre_argument_parsing(self):
                    p = self._parser
                    p.add_argument('-f', '--foo',
                                   help='my foo option',
                                   dest='foo')

                def _post_argument_parsing(self):
                    if self.app.pargs.foo:
                        print('Got Foo Option Before Controller Dispatch')

        """
        pass

    def _post_argument_parsing(self):
        """
        Called on every controller just after arguments are parsed (assuming
        that the parser hasn't thrown an exception).  Provides an alternative
        means of handling passed arguments.  Note that, this function is
        called on every controller, regardless of what namespace and
        sub-command is eventually going to be called.  Therefore, every
        controller can handle their arguments if the user passed them.

        For example:

        .. code-block:: console

            $ myapp --foo bar some-controller --foo2 bar2 some-command


        In the above, the ``base`` controller (or a nested controller) would
        handle ``--foo``, while ``some-controller`` would handle ``foo2``
        before ``some-command`` is executed.

        .. code-block:: python

            class Base(ArgparseController):
                class Meta:
                    label = 'base'

                    arguments = [
                        (['-f', '--foo'],
                         dict(help='my foo option', dest=foo)),
                    ]

                def _post_argument_parsing(self):
                    if self.app.pargs.foo:
                        print('Got Foo Option Before Controller Dispatch')

        Note that ``self._parser`` within a controller is that individual
        controllers ``sub-parser``, and is not the root parser ``app.args``
        (unless you are the ``base`` controller, in which case
        ``self._parser`` is synonymous with ``app.args``).

        """
        pass

    def _dispatch(self):
        LOG.debug("controller dispatch passed off to %s" % self)
        self._setup_controllers()
        self._setup_parsers()

        for contr in self._controllers:
            self._process_arguments(contr)
            self._process_commands(contr)

        for contr in self._controllers:
            contr._pre_argument_parsing()

        self.app._parse_args()

        for contr in self._controllers:
            contr._post_argument_parsing()
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

            # We never get here on Python < 3 as Argparse would have already
            # complained about too few arguments
            contr_label = self.app.pargs\
                              .__controller_namespace__     # pragma: nocover
            contr = self._controllers_map[contr_label]      # pragma: nocover
            func_name = _clean_func(                # pragma: nocover
                contr._meta.default_func        # pragma: nocover
            )                               # pragma: nocover

        if contr_label == 'base':
            contr = self
        else:
            contr = self._controllers_map[contr_label]

        if hasattr(contr, func_name):
            func = getattr(contr, func_name)
            return func()
        else:
            # only time that we'd get here is if Controller.Meta.default_func
            # is pointing to something that doesn't exist
            #
            # We never get here on Python < 3 as Argparse would have already
            # complained about too few arguments
            raise FrameworkError(                           # pragma: nocover
                "Controller function does not exist %s.%s()" % \
                (contr.__class__.__name__, func_name))      # pragma: nocover


def load(app):
    app.handler.register(ArgparseArgumentHandler)
