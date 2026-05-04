"""Cement core exceptions module."""

from typing import Any


class FrameworkError(Exception):

    """
    General framework (non-application) related errors.

    Args:
        msg (str): The error message

    """

    def __init__(self, msg: str) -> None:
        Exception.__init__(self)
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class InterfaceError(FrameworkError):

    """Interface related errors."""
    pass


class CaughtSignal(FrameworkError):  # noqa: N818 - public exception name; adding Error suffix would break 3.0.x API

    """
    Raised when a defined signal is caught.  For more information regarding
    signals, reference the
    `signal <http://docs.python.org/library/signal.html>`_ library.

    Args:
        signum (int): The signal number
        frame: The signal frame object

    """

    def __init__(self, signum: int, frame: Any) -> None:
        msg = f'Caught signal {signum}'
        super().__init__(msg)
        self.signum = signum
        self.frame = frame
