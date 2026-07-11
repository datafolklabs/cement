"""Misc utilities."""

import hashlib
import logging
import os
import sys
from random import random
from textwrap import TextWrapper
from typing import Any

from ..core.deprecations import deprecate


def rando(salt: str | None = None) -> str:
    """
    Generate a random hash for whatever purpose.  Useful for testing
    or any other time that something random is required.

    Args:
        salt (str): Optional ``salt``, if ``None`` then ``random.random()``
            is used.

    Returns:
        str: Random hash

    Example:

        .. code-block:: python

            from cement.utils.misc import rando

            rando('dAhn49amvnah3m')

    """

    if salt is None:
        salt = str(random())

    # issue-626: Use sha256 for compatibility with Redhat/FIPS restricted
    # policies. Return only 32 chars for backward compat with previous md5
    return hashlib.sha256(salt.encode()).hexdigest()[:32]


def init_defaults(*sections: str) -> dict[str, Any]:
    """
    Returns a standard dictionary object to use for application defaults.
    If sections are given, it will create a nested dict for each section name.
    This is sometimes more useful, or cleaner than creating an entire dict set
    (often used in testing).

    Args:
        sections: Section keys to create nested dictionaries for.

    Returns:
        dict: Dictionary of nested dictionaries (sections)

    Example:

        .. code-block:: python

            from cement import App, init_defaults

            defaults = init_defaults('myapp', 'section2', 'section3')
            defaults['myapp']['debug'] = False
            defaults['section2']['foo'] = 'bar
            defaults['section3']['foo2'] = 'bar2'

            app = App('myapp', config_defaults=defaults)

    """
    defaults: dict[str, Any] = dict()
    for section in sections:
        defaults[section] = dict()
    return defaults


def is_true(item: Any) -> bool:
    """
    Given a value, determine if it is one of
    ``[True, 'true', 'yes', 'y', 'on', '1', 1,]`` (note: strings are converted
    to lowercase before comparison).

    Args:
        item: The item to convert to a boolean.

    Returns:
        bool: ``True`` if ``item`` equates to a true-ish value, ``False``
            otherwise

    """
    tstrings = ['true', 'yes', 'y', 'on', '1']
    if isinstance(item, str) and item.lower() in tstrings:
        return True
    elif isinstance(item, bool) and item is True:
        return True
    elif isinstance(item, int) and item == 1:
        return True
    else:
        return False


def wrap(text: str,
         width: int = 77,
         indent: str = '',
         long_words: bool = False,
         hyphens: bool = False) -> str:
    """
    Wrap text for cleaner output (this is a simple wrapper around
    ``textwrap.TextWrapper`` in the standard library).

    Args:
        text (str): The text to wrap

    Keyword Arguments:
        width (int): The max width of a line before breaking
        indent (str): String to prefix subsequent lines after breaking
        long_words (bool): Whether or not to break on long words
        hyphens (bool): Whether or not to break on hyphens

    Returns:
        str: The wrapped string

    """

    types = [str]
    if type(text) not in types:
        raise TypeError("Argument `text` must be one of [str, unicode].")

    wrapper = TextWrapper(subsequent_indent=indent, width=width,
                          break_long_words=long_words,
                          break_on_hyphens=hyphens)
    return wrapper.fill(text)


class _SafeFileHandler(logging.FileHandler):
    """
    A ``logging.FileHandler`` that never lets a file I/O failure reach the
    host application.

    Framework logging (see :func:`minimal_logger`) is a silent development
    aid enabled via ``CEMENT_FRAMEWORK_LOG_FILE``.  A misconfigured or
    unwritable path -- a directory, an existing read-only file, a disk that
    fills up mid-run, a path removed while running -- must not crash the
    application or spam its stderr.  Any error raised while opening or
    writing the log file is swallowed.
    """

    def emit(self, record: logging.LogRecord) -> None:
        try:
            super().emit(record)
        except Exception:  # noqa: BLE001 - dev aid must never crash the app
            self.handleError(record)

    def handleError(self, record: logging.LogRecord) -> None:  # noqa: N802
        # name mirrors logging.Handler.handleError (framework override)
        pass


class MinimalLogger:

    def __init__(self,
                 namespace: str,
                 debug: bool,
                 *args: Any,
                 **kw: Any) -> None:
        self.namespace = namespace
        self.backend = logging.getLogger(namespace)
        self._debug = debug
        formatter = logging.Formatter(
            "%(asctime)s (%(levelname)s) %(namespace)s : %(message)s"
        )
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        console.setLevel(logging.INFO)
        self.backend.setLevel(logging.INFO)

        _enabled = False
        if is_true(os.environ.get('CEMENT_LOG', 0)) or debug is True:
            _enabled = True
        elif '--debug' in sys.argv:
            deprecate('3.0.8-2')
            _enabled = True
        elif is_true(os.environ.get('CEMENT_FRAMEWORK_LOGGING', 0)):
            deprecate('3.0.8-1')
            _enabled = True

        if _enabled is True:
            # framework and extensions only log to debug
            console.setLevel(logging.DEBUG)
            self.backend.setLevel(logging.DEBUG)

        # Idempotency guard: `logging.getLogger(namespace)` returns the
        # same backend logger instance for a given namespace, so a
        # second `minimal_logger(ns)` call would otherwise stack a
        # duplicate StreamHandler on the shared backend (every
        # subsequent log emit would print twice). Only attach when
        # the backend has no handlers yet.
        if not self.backend.handlers:
            self.backend.addHandler(console)

        # issue-593: Optionally also route framework/extension debug
        # output to a file when CEMENT_FRAMEWORK_LOG_FILE is set. This is
        # purely additive: the emit methods still gate on
        # `logging_is_enabled`, so nothing is written unless framework
        # logging is enabled via an existing switch (CEMENT_LOG /
        # debug=True / --debug / CEMENT_FRAMEWORK_LOGGING). The handler
        # level and formatter mirror the console handler.
        log_file = os.environ.get('CEMENT_FRAMEWORK_LOG_FILE', None)
        if log_file:
            path = os.path.abspath(os.path.expanduser(log_file))
            # Idempotency guard mirroring the StreamHandler one above: a
            # repeated minimal_logger() call for the same namespace + path
            # must not stack a duplicate FileHandler (double-writes).
            already_attached = any(
                isinstance(h, logging.FileHandler)
                and h.baseFilename == path
                for h in self.backend.handlers
            )
            # Attach when the target directory exists and is writable. Any
            # failure that slips past this check -- the path is itself a
            # directory, an existing but unwritable file, a disk that later
            # fills up, etc. -- is contained by _SafeFileHandler, which never
            # lets a logging failure crash the host app or spam its stderr
            # (framework logging is a silent development aid).
            parent = os.path.dirname(path)
            if (not already_attached
                    and os.path.isdir(parent)
                    and os.access(parent, os.W_OK)):
                # delay=True defers opening (and creating) the file until the
                # first record is actually emitted. Combined with the
                # `logging_is_enabled` gate on every emit method, this means
                # no empty log file is created unless framework logging is
                # enabled AND something is actually logged.
                file_handler = _SafeFileHandler(path, delay=True)
                file_handler.setFormatter(formatter)
                file_handler.setLevel(console.level)
                self.backend.addHandler(file_handler)

    def _get_logging_kwargs(self,
                            namespace: str | None,
                            **kw: Any) -> dict[Any, Any]:
        if not namespace:
            namespace = self.namespace

        if 'extra' in kw.keys() and 'namespace' in kw['extra'].keys():
            pass
        elif 'extra' in kw.keys() and 'namespace' not in kw['extra'].keys():
            kw['extra']['namespace'] = namespace
        else:
            kw['extra'] = dict(namespace=namespace)

        return kw

    @property
    def logging_is_enabled(self) -> bool:
        enabled = False
        if '--debug' in sys.argv or self._debug:
            deprecate('3.0.8-2')
            val = os.environ.get('CEMENT_LOG_DEPRECATED_DEBUG_OPTION', 0)
            if is_true(val):
                enabled = True
        elif is_true(os.environ.get('CEMENT_LOG', 0)):
            enabled = True
        elif is_true(os.environ.get('CEMENT_FRAMEWORK_LOGGING', 0)):
            deprecate('3.0.8-1')
            enabled = True

        return enabled

    def info(self,
             msg: str,
             namespace: str | None = None,
             **kw: Any) -> None:
        if self.logging_is_enabled:
            kwargs = self._get_logging_kwargs(namespace, **kw)
            self.backend.info(msg, **kwargs)

    def warning(self,
                msg: str,
                namespace: str | None = None,
                **kw: Any) -> None:
        if self.logging_is_enabled:
            kwargs = self._get_logging_kwargs(namespace, **kw)
            self.backend.warning(msg, **kwargs)

    def error(self,
              msg: str,
              namespace: str | None = None,
              **kw: Any) -> None:
        if self.logging_is_enabled:
            kwargs = self._get_logging_kwargs(namespace, **kw)
            self.backend.error(msg, **kwargs)

    def fatal(self,
              msg: str,
              namespace: str | None = None,
              **kw: Any) -> None:
        if self.logging_is_enabled:
            kwargs = self._get_logging_kwargs(namespace, **kw)
            self.backend.fatal(msg, **kwargs)

    def debug(self,
              msg: str,
              namespace: str | None = None,
              **kw: Any) -> None:
        if self.logging_is_enabled:
            kwargs = self._get_logging_kwargs(namespace, **kw)
            self.backend.debug(msg, **kwargs)


def minimal_logger(namespace: str, debug: bool = False) -> MinimalLogger:
    """
    Setup just enough for cement to be able to do debug logging.  This is the
    logger used by the Cement framework, which is setup and accessed before
    the application is functional (and more importantly before the
    applications log handler is usable).

    Framework logging is toggled by the usual switches (``CEMENT_LOG``,
    ``debug=True``, ``--debug``, or the deprecated
    ``CEMENT_FRAMEWORK_LOGGING``).  When framework logging is enabled, setting
    the ``CEMENT_FRAMEWORK_LOG_FILE`` environment variable to a path *also*
    writes that output to the given file (in addition to the console).
    Setting the variable alone does not enable logging, and an
    unwritable/invalid path is ignored rather than raising.

    Args:
        namespace (str): The logging namespace.  This is generally
            ``__name__`` or anything you want.

    Keyword Args:
        debug (bool): Toggle debug output.

    Returns:
        object: A Logger object

    Example:

        .. code-block:: python

            from cement.utils.misc import minimal_logger
            LOG = minimal_logger('cement')
            LOG.debug('This is a debug message')

    """
    return MinimalLogger(namespace, debug)
