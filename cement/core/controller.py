"""Cement core controller module."""

import re
import textwrap
import argparse
from abc import abstractmethod
from ..core import exc
from ..core.handler import Handler
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class ControllerHandlerBase(Handler):

    """
    This class defines the Controller Handler Interface.  Classes that
    implement this interface must provide the methods and attributes defined
    below.

    Usage:

    .. code-block:: python

        from cement.core.controller import ControllerHandlerBase

        class MyController(ControllerHandlerBase):
            class Meta:
                label = 'my_controller'
                ...
    """

    class Meta:

        """Interface meta-data."""

        #: The string identifier of the interface.
        interface = 'controller'

    @abstractmethod
    def _dispatch(self):
        """
        Reads the application object's data to dispatch a command from this
        controller.  For example, reading ``self.app.pargs`` to determine what
        command was pass    # pragma: nocovered, and then executing that command function.

        Note that Cement does *not* parse arguments when calling ``_dispatch()``
        on a controller, as it expects the controller to handle parsing
        arguments (I.e. ``self.app.args.parse()``).

        Returns:
            unknown: The result of the executed controller function, or ``None``
            if no controller function is called.

        """
        pass    # pragma: nocover


class ControllerHandler(ControllerHandlerBase):
    """Controller handler implementation."""
    pass    # pragma: nocover
