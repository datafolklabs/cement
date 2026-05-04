"""Cement core controller module."""

from abc import abstractmethod
from typing import Any

from ..core.handler import Handler
from ..core.interface import Interface
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class ControllerInterface(Interface):

    """
    This class defines the Controller Interface.  Handlers that implement this
    interface must provide the methods and attributes defined below. In
    general, most implementations should sub-class from the provided
    :class:`ControllerHandler` base class as a starting point.
    """

    class Meta(Interface.Meta):

        """Interface meta-data."""

        #: The string identifier of the interface.
        interface = 'controller'

    # D-09: `_dispatch` returns whatever the user's command function returns
    # so the type contract is intentionally wide. The Wave 3 UP007 cascade
    # left a redundant `| None` member on this annotation; dropped in the
    # Wave 5 tightening pass since the wide type already covers None.
    @abstractmethod
    def _dispatch(self) -> Any:
        """
        Reads the application object's data to dispatch a command from this
        controller.  For example, reading ``self.app.pargs`` to determine what
        command was passed, and then executing that command function.

        Note that Cement does *not* parse arguments when calling
        ``_dispatch()`` on a controller, as it expects the controller to
        handle parsing arguments (I.e. ``self.app.args.parse()``).

        Returns:
            unknown: The result of the executed controller function, or
            ``None`` if no controller function is called.

        """
        pass    # pragma: nocover  # abstract method


class ControllerHandler(ControllerInterface, Handler):
    """Controller handler implementation."""
    class Meta(Handler.Meta):
        pass    # pragma: nocover  # abstract method
