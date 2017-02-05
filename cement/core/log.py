"""
Cement core log module.

"""

# from ..core import interface
from abc import ABC, abstractmethod, abstractproperty
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
    def set_level():
        """
        Set the log level.  Must except atleast one of:
            ``['INFO', 'WARNING', 'ERROR', 'DEBUG', or 'FATAL']``.

        """
        pass

    @abstractmethod
    def get_level():
        """Return a string representation of the log level."""
        pass

    @abstractmethod
    def info(msg):
        """
        Log to the 'INFO' facility.

        :param msg: The message to log.

        """
        pass

    @abstractmethod
    def warning(self, msg):
        """
        Log to the 'WARNING' facility.

        :param msg: The message to log.

        """
        pass

    @abstractmethod
    def error(self, msg):
        """
        Log to the 'ERROR' facility.

        :param msg: The message to log.

        """
        pass

    @abstractmethod
    def fatal(self, msg):
        """
        Log to the 'FATAL' facility.

        :param msg: The message to log.

        """
        pass

    @abstractmethod
    def debug(self, msg):
        """
        Log to the 'DEBUG' facility.

        :param msg: The message to log.

        """
        pass

class LogHandler(LogHandlerBase):

    """
    Log handler implementation.

    """

    pass
