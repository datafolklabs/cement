"""Cement core controller module."""

import re
import textwrap
import argparse
from ..core import exc, interface, handler
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


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
        'config_section',
        'config_defaults',
        'stacked_on',
        'stacked_type',
    ]
    interface.validate(IController, obj, members, meta=meta)

    # also check _meta.arguments values
    errmsg = "Controller arguments must be a list of tuples.  I.e. " + \
             "[ (['-f', '--foo'], dict(action='store')), ]"

    if obj._meta.arguments is not None:
        if type(obj._meta.arguments) is not list:
            raise exc.InterfaceError(errmsg)
        for item in obj._meta.arguments:
            if type(item) is not tuple:
                raise exc.InterfaceError(errmsg)
            if type(item[0]) is not list:
                raise exc.InterfaceError(errmsg)
            if type(item[1]) is not dict:
                raise exc.InterfaceError(errmsg)

    if not obj._meta.label == 'base' and obj._meta.stacked_on is None:
        errmsg = "Controller `%s` is not stacked anywhere!" % \
                 obj.__class__.__name__
        raise exc.InterfaceError(errmsg)
    if not obj._meta.label == 'base' and \
            obj._meta.stacked_type not in ['nested', 'embedded']:
        raise exc.InterfaceError(
            "Controller '%s' " % obj._meta.label +
            "has an unknown stacked type of '%s'." %
            obj._meta.stacked_type
        )


class IController(interface.Interface):

    """
    This class defines the Controller Handler Interface.  Classes that
    implement this handler must provide the methods and attributes defined
    below.

    Implementations do *not* subclass from interfaces.

    Usage:

    .. code-block:: python

        from cement.core.handler import Handler
        from cement.core.controller import IController

        class MyController(handler):
            class Meta:
                interface = controller.IController
                ...
    """
    # pylint: disable=W0232, C0111, R0903
    class IMeta:

        """Interface meta-data."""

        #: The string identifier of the interface.
        label = 'controller'

        #: The interface validator function.
        validator = controller_validator

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
        :returns: ``None``

        """

    def _dispatch(self):
        """
        Reads the application object's data to dispatch a command from this
        controller.  For example, reading self.app.pargs to determine what
        command was passed, and then executing that command function.

        Note that Cement does *not* parse arguments when calling _dispatch()
        on a controller, as it expects the controller to handle parsing
        arguments (I.e. self.app.args.parse()).

        :returns: Returns the result of the executed controller function,
          or ``None`` if no controller function is called.

        """


