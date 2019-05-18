"""Misc utilities."""

import os
import sys
import logging
import hashlib
from textwrap import TextWrapper
from random import random


def rando(salt=None):
    """
    Generate a random MD5 hash for whatever purpose.  Useful for testing
    or any other time that something random is required.

    Args:
        salt (str): Optional ``salt``, if ``None`` then ``random.random()``
            is used.

    Returns:
        str: Random MD5 hash

    Example:

        .. code-block:: python

            from cement.utils.misc import rando

            rando('dAhn49amvnah3m')

    """

    if salt is None:
        salt = random()

    return hashlib.md5(str(salt).encode()).hexdigest()


class MinimalLogger(object):

    def __init__(self, namespace, debug, *args, **kw):
        self.namespace = namespace
        self.backend = logging.getLogger(namespace)
        formatter = logging.Formatter(
            "%(asctime)s (%(levelname)s) %(namespace)s : %(message)s"
        )
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        console.setLevel(logging.INFO)
        self.backend.setLevel(logging.INFO)

        # FIX ME: really don't want to hard check sys.argv like this but
        # can't figure any better way get logging started (only for debug)
        # before the app logging is setup.
        if '--debug' in sys.argv or debug:
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
        if 'CEMENT_FRAMEWORK_LOGGING' in os.environ.keys():
            if is_true(os.environ['CEMENT_FRAMEWORK_LOGGING']):
                res = True
            else:
                res = False
        else:
            res = True  # pragma: nocover

        return res

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
