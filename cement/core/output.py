"""Cement core output module."""

from abc import abstractmethod
from ..core.handler import Handler
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class OutputHandlerBase(Handler):

    """
    This class defines the Output Handler Interface.  Classes that
    implement this interface must provide the methods and attributes defined
    below.

    Usage:

        .. code-block:: python

            from cement.core.output import OutputHandlerBase

            class MyOutputHandler(OutputHandlerBase):
                class Meta:
                    label = 'my_output_handler'
                ...

    """

    class Meta:

        """Handler meta-data."""

        #: The string identifier of the interface
        interface = 'output'

    @abstractmethod
    def render(self, data, *args, **kwargs):
        """
        Render the ``data`` dict into output in some fashion.  This function
        must accept both ``*args`` and ``**kwargs`` to allow an application to
        mix output handlers that support different features.

        Args:
            data (dict): The dictionary whose data we need to render into
                output.

        Returns:
            str, None: The rendered output string, or ``None`` if no output is
            rendered

        """
        pass


class OutputHandler(OutputHandlerBase):

    """Output handler implementation."""

    pass
