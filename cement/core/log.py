"""
Cement core log module.

"""

# from ..core import interface
from abc import abstractmethod
from ..core.handler import Handler


class LogHandlerBase(Handler):

    """
    This class defines the Log Handler Interface.  Classes that
    implement this handler must provide the methods and attributes defined
    below.

    Usage:

    .. code-block:: python

        from cement.core.log import LogHandlerBase

        class MyLogHandler(LogHandlerBase):
            class Meta:
                label = 'my_log'

    """

    class Meta:

        """Handler meta-data."""

        #: The string identifier of the interface.
        interface = 'log'

    @abstractmethod
    def set_level(self):
        """
        Set the log level.  Must except atleast one of:
            ``['INFO', 'WARNING', 'ERROR', 'DEBUG', or 'FATAL']``.

        """
        pass  # pragma: nocover

    @abstractmethod
    def get_level(self):
        """Return a string representation of the log level."""
        pass  # pragma: nocover

    @abstractmethod
    def info(self, msg):
        """
        Log to the ``INFO`` facility.

        Args:
            msg (str): The message to log.

        """
        pass  # pragma: nocover

    @abstractmethod
    def warning(self, msg):
        """
        Log to the ``WARNING`` facility.

        Args:
            msg (str): The message to log.

        """
        pass  # pragma: nocover

    @abstractmethod
    def error(self, msg):
        """
        Log to the ``ERROR`` facility.

        Args:
            msg (str): The message to log.

        """
        pass  # pragma: nocover

    @abstractmethod
    def fatal(self, msg):
        """
        Log to the ``FATAL`` facility.

        Args:
            msg (str): The message to log.

        """
        pass  # pragma: nocover

    @abstractmethod
    def debug(self, msg):
        """
        Log to the ``DEBUG`` facility.

        Args:
            msg (str): The message to log.

        """
        pass  # pragma: nocover


class LogHandler(LogHandlerBase):

    """
    Log handler implementation.

    """

    pass  # pragma: nocover
