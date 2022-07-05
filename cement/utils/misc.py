"""Misc utilities."""

import os
import sys
import logging
import hashlib
from textwrap import TextWrapper
from random import random
from ..core.deprecations import deprecate


def rando(salt=None):
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
        salt = random()

    # issue-626: Use sha256 for compatibility with Redhat/FIPS restricted
    # policies. Return only 32 chars for backward compat with previous md5
    return hashlib.sha256(str(salt).encode()).hexdigest()[:32]


class MinimalLogger(object):

    def __init__(self, namespace, debug, *args, **kw):
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

        self.backend.addHandler(console)

    def _get_logging_kwargs(self, namespace, **kw):
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
    def logging_is_enabled(self):
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

    def info(self, msg, namespace=None, **kw):
        if self.logging_is_enabled:
            kwargs = self._get_logging_kwargs(namespace, **kw)
            self.backend.info(msg, **kwargs)

    def warning(self, msg, namespace=None, **kw):
        if self.logging_is_enabled:
            kwargs = self._get_logging_kwargs(namespace, **kw)
            self.backend.warning(msg, **kwargs)

    def error(self, msg, namespace=None, **kw):
        if self.logging_is_enabled:
            kwargs = self._get_logging_kwargs(namespace, **kw)
            self.backend.error(msg, **kwargs)

    def fatal(self, msg, namespace=None, **kw):
        if self.logging_is_enabled:
            kwargs = self._get_logging_kwargs(namespace, **kw)
            self.backend.fatal(msg, **kwargs)

    def debug(self, msg, namespace=None, **kw):
        if self.logging_is_enabled:
            kwargs = self._get_logging_kwargs(namespace, **kw)
            self.backend.debug(msg, **kwargs)


def init_defaults(*sections):
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
    defaults = dict()
    for section in sections:
        defaults[section] = dict()
    return defaults


def minimal_logger(namespace, debug=False):
    """
    Setup just enough for cement to be able to do debug logging.  This is the
    logger used by the Cement framework, which is setup and accessed before
    the application is functional (and more importantly before the
    applications log handler is usable).

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


def is_true(item):
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


def wrap(text, width=77, indent='', long_words=False, hyphens=False):
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
