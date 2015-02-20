"""ArgParse Framework Extension"""

import re
import argparse
from argparse import ArgumentParser
from ..core import backend, arg, handler
from ..core.controller import IController
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


def argparse_action(controller, command, func_name):
    class CustomAction(argparse.Action):
        def __init__(self, option_strings, dest, nargs=None, **kwargs):
            super(CustomAction, self).__init__(option_strings, dest, **kwargs)

        def __call__(self, parser, namespace, values, option_string=None):
            # this is wierd, but this func gets called before the
            # app can set self._parsed_args (which the controllers use as
            # app.pargs generally
            if namespace.command == command:
                controller.app._parsed_args = namespace
                func = getattr(controller, func_name)
                func()
            setattr(namespace, self.dest, values)

    return CustomAction


class ArgParseArgumentHandler(arg.CementArgumentHandler, ArgumentParser):

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
        super(ArgParseArgumentHandler, self).__init__(*args, **kw)
        self.config = None

    def parse(self, arg_list):
        """
        Parse a list of arguments, and return them as an object.  Meaning an
        argument name of 'foo' will be stored as parsed_args.foo.

        :param arg_list: A list of arguments (generally sys.argv) to be
         parsed.
        :returns: object whose members are the arguments parsed.

        """
        return self.parse_args(arg_list)

    def add_argument(self, *args, **kw):
        """
        Add an argument to the parser.  Arguments and keyword arguments are
        passed directly to ArgumentParser.add_argument().

        """
        return super(ArgumentParser, self).add_argument(*args, **kw)


class expose(object):

    """
    Used to expose controller functions to be listed as commands, and to
    decorate the function with Meta data for the argument parser.

    :param help: Help text to display for that command.
    :type help: str
    :param hide: Whether the command should be visible.
    :type hide: boolean
    :param aliases: Aliases to this command.
    :param aliases_only: Whether to only display the aliases (not the label).
     This is useful for situations where you have obscure function names
     which you do not want displayed.  Effecively, if there are aliases and
     `aliases_only` is True, then aliases[0] will appear as the actual
     command/function label.
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
    # pylint: disable=W0622

    def __init__(self, help='', hide=False, aliases=[], aliases_only=False):
        self.hide = hide
        self.help = help
        self.aliases = aliases
        self.aliases_only = aliases_only

    def __call__(self, func):
        metadict = {}
        metadict['label'] = re.sub('_', '-', func.__name__)
        metadict['func_name'] = func.__name__
        metadict['exposed'] = True
        metadict['hide'] = self.hide
        metadict['help'] = self.help
        metadict['aliases'] = self.aliases
        metadict['aliases_only'] = self.aliases_only
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

        #: A list of aliases for the controller/sub-parser.
        # aliases = []

        # aliases_only = False
        # """
        # When set to True, the controller label will not be displayed at
        # command line, only the aliases will.  Effectively, aliases[0] will
        # appear as the label.  This feature is useful for the situation Where
        # you might want two controllers to have the same label when stacked
        # on top of separate controllers.  For example, 'myapp users list' and
        # 'myapp servers list' where 'list' is a stacked controller, not a
        # function.
        # """

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

        # #: Description for the sub-parser group in help output.
        # description = None

        # #: The title for the sub-parser group in help output.
        # title = 'sub-commands'

        #: Text for the controller/sub-parser group in help output (for
        #: nested stacked controllers only).
        # help = None

        # #: Whether or not to hide the controller entirely.
        # hide = False

        # epilog = None
        # """
        # The text that is displayed at the bottom when '--help' is passed.
        # """

        # usage = None
        # """
        # The text that is displayed at the top when '--help' is passed.
        # Although the default is `None`, Cement will set this to a generic
        # usage based on the `prog`, `controller` name, etc if nothing else is
        # passed.
        # """

        # argument_formatter = argparse.RawDescriptionHelpFormatter
        # """
        # The argument formatter class to use to display --help output.
        # """

        # action = argparse_action
        # """
        # The action function to set for controller/command actions.
        # """

        #: Keyword arguments passed when ``ArgumentParser.add_subparsers()``
        #: is called to create this controller namespace.
        subparser_options = {}

        #: Keyword arguments passed when ``ArgumentParser.add_parser()`` is
        #: called to create this controller sub-parser.
        parser_options = {}

        #: The action that will be added to ``parser_options`` to handle
        #: controller and sub-command mapping.
        parser_action = argparse_action

        #: Keyword arguments passed when ``ArgumentParser.add_argument()`` is
        #: called to add arguments.
        argument_options = {}

    def __init__(self, *args, **kw):
        super(ArgparseController, self).__init__(*args, **kw)
        self.app = None
        self._sub_parser_parents = dict()
        self._sub_parsers = dict()
        self._controllers = []
        self._nesting_parents = []

    def _setup(self, app):
        """
        See `IController._setup() <#cement.core.cache.IController._setup>`_.
        """
        super(ArgparseController, self)._setup(app)
        self.app = app

    def _setup_controllers(self):
        self._controllers = []
        self._nesting_parents = []

        # treat base/self separately
        self._controllers.append(self)

        for contr in handler.list('controller'):
            # ignore self
            if contr == self.__class__:
                continue

            contr = contr()
            contr._setup(self.app)
            if contr._meta.stacked_on not in self._nesting_parents:
                self._nesting_parents.append(contr._meta.stacked_on)
            self._controllers.append(contr)

    def _get_subparser_kwargs(self, contr):
        kwargs = contr._meta.subparser_options.copy()
        if 'title' not in kwargs.keys():
            kwargs['title'] = 'sub-commands'
        if 'dest' not in kwargs.keys():
            kwargs['dest'] = 'command'
        kwargs['action'] = 'store_true'
        #if 'action' not in kwargs.keys():
        #    kwargs['action'] = contr._meta.parser_action(
        #                            contr,
        #                            contr._meta.label,
        #                            'default',
        #                            )
        return kwargs

    def _setup_parsers(self):
        # this should only be run by the base controller
        if not self._meta.label == 'base':
            raise FrameworkError('Private function _setup_parsers() called'
                                 'from non-base controller')

        dest = 'command'

        # parents are sub-parser namespaces (that we can add subparsers to)
        # where-as parsers are the actual root parser and sub-parsers to
        # add arguments to
        parents = self._sub_parser_parents
        parsers = self._sub_parsers

        parsers['base'] = self.app.args

        # only base controller registered
        if len(handler.list('controller')) <= 1:
            return True


        kwargs = self._get_subparser_kwargs(self)
        print kwargs
        # handle base controller separately
        sub = self.app.args.add_subparsers(**kwargs)
        parents['base'] = sub

        # This is odd... but there is a circular dependency on stacked
        # controllers.  We don't know what order we are handling them, and we
        # need to ensure all parsers are setup (before a stacked controller
        # can access it's parser)

        tmp_controllers = list(self._controllers)
        while tmp_controllers:
            for contr in self._controllers:
                label = contr._meta.label
                stacked_on = contr._meta.stacked_on
                stacked_type = contr._meta.stacked_type

                # kwargs = {}
                # if not contr._meta.hide == True:
                #     kwargs['help'] = contr._meta.help
                #     self._meta.subparser_options['help'] =
                # kwargs['title'] = contr._meta.title
                # kwargs['aliases'] = contr._meta.aliases
                # kwargs['descripton'] = contr._meta.description

                # if the controller this one is stacked on is not setup yet
                # we need to skip it and then come back to it
                if stacked_on not in parents.keys():
                    continue

                # if the controller is nested, we need to create a new parser
                # parent using the one that it is stacked on, as well as as a
                # new parser
                if stacked_type == 'nested':
                    parsers[label] = parents[stacked_on].add_parser(
                                        label,
                                        **contr._meta.parser_options
                                        )

                    # if other controllers are nested on this one we need to
                    # setup additional subparsers in this namespace
                    #if label in self._nesting_parents:
                    kwargs = self._get_subparser_kwargs(contr)
                    parents[label] = parsers[label].add_subparsers(**kwargs)

                # if it's embedded, then just set the use the same as the
                # controller its stacked on
                elif stacked_type == 'embedded':
                    parents[label] = parents[stacked_on]
                    parsers[label] = parsers[stacked_on]

                if contr in tmp_controllers:
                    tmp_controllers.remove(contr)

    def _get_parser(self, parser):
        return self._sub_parsers[parser]

    def _process_arguments(self, parser, arguments):
        parser = self._get_parser(parser)
        for arg, kw in arguments:
            try:
                parser.add_argument(*arg, **kw)
            except argparse.ArgumentError as e:
                raise exc.FrameworkError(e.__str__())

    def _process_commands(self, parser, commands):
        parser = self._get_parser(parser)
        for command in commands:
            kwargs = {}
            if not command['hide'] == True:
                kwargs['help'] = command['help']
            kwargs['aliases'] = command['aliases']

            contr = command['controller']
            cmd_parent = self._sub_parser_parents[contr._meta.label]
            command_parser = cmd_parent.add_parser(command['label'], **kwargs)

            # create a default command for the controller
            command_parser.add_argument('run',
                action=contr._meta.parser_action(
                    command['controller'],
                    command['label'],
                    command['func_name'],
                    ),
                nargs='?',
                help=argparse.SUPPRESS,
                )

    def _collect(self):
        self.app.log.debug("collecting arguments/commands for %s" % self)
        arguments = self._meta.arguments
        commands = []

        for member in dir(self.__class__):
            if member.startswith('_'):
                continue
            elif hasattr(getattr(self, member), '__cement_meta__'):
                func = getattr(self.__class__, member).__cement_meta__
                func['controller'] = self
                commands.append(func)

        return (arguments, commands)

    def _dispatch(self):
        self.app.log.debug("controller dispatch passed off to %s" % self)
        self._setup_controllers()
        self._setup_parsers()

        for contr in self._controllers:
            arguments, commands = contr._collect()
            self._process_arguments(contr._meta.stacked_on, arguments)
            self._process_commands(contr._meta.stacked_on, commands)

        #self.app.args.parse_args()

def load(app):
    handler.register(ArgParseArgumentHandler)
