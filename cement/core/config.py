"""Cement core config module."""

import os
from abc import ABC, abstractmethod, abstractproperty
from ..core.handler import Handler
from ..utils.fs import abspath
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class ConfigHandlerBase(Handler):

    """
    This class defines the Config Handler Interface.  Classes that
    implement this interface must provide the methods and attributes defined
    below.

    Usage:

    .. code-block:: python

        from cement.core.config import ConfigHandlerBase

        class MyConfigHandler(ConfigHandlerbase):
            class Meta:
                label = 'my_config'
            ...

    """

    class Meta:

        """Handler meta-data."""

        interface = 'config'
        """The string identifier of the interface."""

    @abstractmethod
    def parse_file(self, file_path):
        """
        Parse config file settings from file_path.  Returns True if the file
        existed, and was parsed successfully.  Returns False otherwise.

        :param file_path: The path to the config file to parse.
        :returns: True if the file was parsed, False otherwise.
        :rtype: ``boolean``

        """
        pass

    @abstractmethod
    def keys(self, section):
        """
        Return a list of configuration keys from `section`.

        :param section: The config [section] to pull keys from.
        :returns: A list of keys in `section`.
        :rtype: ``list``

        """
        pass

    @abstractmethod
    def get_sections(self):
        """
        Return a list of configuration sections.  These are designated by a
        [block] label in a config file.

        :returns: A list of config sections.
        :rtype: ``list``

        """
        pass

    @abstractmethod
    def get_section_dict(self, section):
        """
        Return a dict of configuration parameters for [section].

        :param section: The config [section] to generate a dict from (using
            that section keys).
        :returns: A dictionary of the config section.
        :rtype: ``dict``

        """
        pass

    @abstractmethod
    def add_section(self, section):
        """
        Add a new section if it doesn't exist.

        :param section: The [section] label to create.
        :returns: ``None``

        """
        pass

    @abstractmethod
    def get(self, section, key):
        """
        Return a configuration value based on [section][key].  The return
        value type is unknown.

        :param section: The [section] of the configuration to pull key value
            from.
        :param key: The configuration key to get the value from.
        :returns: The value of the `key` in `section`.
        :rtype: ``Unknown``

        """
        pass

    @abstractmethod
    def set(self, section, key, value):
        """
        Set a configuration value based at [section][key].

        :param section: The [section] of the configuration to pull key value
            from.
        :param key: The configuration key to set the value at.
        :param value: The value to set.
        :returns: ``None``

        """
        pass

    @abstractmethod
    def merge(self, dict_obj, override=True):
        """
        Merges a dict object into the configuration.

        :param dict_obj: The dictionary to merge into the config
        :param override: Boolean.  Whether to override existing values.
            Default: True
        :returns: ``None``
        """
        pass

    @abstractmethod
    def has_section(self, section):
        """
        Returns whether or not the section exists.

        :param section: The section to test for.
        :returns: ``boolean``

        """
        pass


class ConfigHandler(ConfigHandlerBase):

    """
    Config handler implementation.

    """

    @abstractmethod
    def _parse_file(self, file_path):
        """
        Parse a configuration file at `file_path` and store it.  This function
        must be provided by the handler implementation (that is sub-classing
        this).

        :param file_path: The file system path to the configuration file.
        :returns: True if file was read properly, False otherwise
        :rtype: ``boolean``

        """
        pass

    def parse_file(self, file_path):
        """
        Ensure we are using the absolute/expanded path to `file_path`, and
        then call `_parse_file` to parse config file settings from it,
        overwriting existing config settings.  If the file does not exist,
        returns False.

        Developers sub-classing from here should generally override
        `_parse_file` which handles just the parsing of the file and leaving
        this function to wrap any checks/logging/etc.

        :param file_path: The file system path to the configuration file.
        :returns: ``boolean``

        """
        file_path = abspath(file_path)
        if os.path.exists(file_path):
            LOG.debug("config file '%s' exists, loading settings..." %
                      file_path)
            return self._parse_file(file_path)
        else:
            LOG.debug("config file '%s' does not exist, skipping..." %
                      file_path)
            return False
