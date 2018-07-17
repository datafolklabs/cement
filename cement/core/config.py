"""Cement core config module."""

import os
from abc import abstractmethod
from ..core.interface import Interface
from ..core.handler import Handler
from ..utils.fs import abspath
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class ConfigInterface(Interface):

    """
    This class defines the Config Interface.  Handlers that implement this
    interface must provide the methods and attributes defined below. In
    general, most implementations should sub-class from the provided
    :class:`ConfigHandler` base class as a starting point.
    """

    class Meta:

        """Handler meta-data."""

        #: The string identifier of the interface.
        interface = 'config'

    @abstractmethod
    def parse_file(self, file_path):
        """
        Parse config file settings from ``file_path``.  Returns True if the
        file existed, and was parsed successfully.  Returns False otherwise.

        Args:
            file_path (str): The path to the config file to parse.

        Returns:
            bool: ``True`` if the file was parsed, ``False`` otherwise.

        """
        pass    # pragma: nocover

    @abstractmethod
    def keys(self, section):
        """
        Return a list of configuration keys from ``section``.

        Args:
            section (list): The config section to pull keys from.

        Returns:
            list: A list of keys in ``section``.

        """
        pass    # pragma: nocover

    @abstractmethod
    def get_sections(self):
        """
        Return a list of configuration sections.

        Returns:
            list: A list of config sections.

        """
        pass    # pragma: nocover

    @abstractmethod
    def get_dict(self):
        """
        Return a dict of the entire configuration.

        Returns:
            dict: A dictionary of the entire config.

        """

    @abstractmethod
    def get_section_dict(self, section):
        """
        Return a dict of configuration parameters for ``section``.

        Args:
            section (str): The config section to generate a dict from (using
                that sections' keys).

        Returns:
            dict: A dictionary of the config section.

        """
        pass    # pragma: nocover

    @abstractmethod
    def add_section(self, section):
        """
        Add a new section if it doesn't already exist.

        Args:
            section: The section label to create.

        Returns:
            None

        """
        pass    # pragma: nocover

    @abstractmethod
    def get(self, section, key):
        """
        Return a configuration value based on ``section.key``.  Must honor
        environment variables if they exist to override the config... for
        example ``config['myapp']['foo']['bar']`` must be overridable by the
        environment variable ``MYAPP_FOO_BAR``.... Note that ``MYAPP_`` must
        prefix all vars, therefore ``config['redis']['foo']`` would be
        overridable by ``MYAPP_REDIS_FOO`` ... but
        ``config['myapp']['foo']['bar']`` would not have a double prefix of
        ``MYAPP_MYAPP_FOO_BAR``.

        Args:
            section (str): The section of the configuration to pull key values
                from.
            key (str): The configuration key to get the value for.

        Returns:
            unknown: The value of the ``key`` in ``section``.

        """
        pass    # pragma: nocover

    @abstractmethod
    def set(self, section, key, value):
        """
        Set a configuration value based at ``section.key``.

        Args:
            section (str): The ``section`` of the configuration to pull key
                value from.
            key (str): The configuration key to set the value at.
            value: The value to set.

        Returns:
            None

        """
        pass    # pragma: nocover

    @abstractmethod
    def merge(self, dict_obj, override=True):
        """
        Merges a dict object into the configuration.

        Args:
            dict_obj (dict): The dictionary to merge into the config
            override (bool): Whether to override existing values or not.

        Returns:
            None

        """
        pass    # pragma: nocover

    @abstractmethod
    def has_section(self, section):
        """
        Returns whether or not the section exists.

        Args:
            section (str): The section to test for.

        Returns:
            bool: ``True`` if the configuration section exists, ``False``
                otherwise.

        """
        pass    # pragma: nocover


class ConfigHandler(ConfigInterface, Handler):

    """
    Config handler implementation.

    """

    @abstractmethod
    def _parse_file(self, file_path):
        """
        Parse a configuration file at ``file_path`` and store it.  This
        function must be provided by the handler implementation (that is
        sub-classing this).

        Args:
            file_path (str): The file system path to the configuration file.

        Returns:
            bool: ``True`` if file was read properly, ``False`` otherwise

        """
        pass    # pragma: nocover

    def parse_file(self, file_path):
        """
        Ensure we are using the absolute/expanded path to ``file_path``, and
        then call ``self._parse_file`` to parse config file settings from it,
        overwriting existing config settings.

        Developers sub-classing from here should generally override
        ``_parse_file`` which handles just the parsing of the file and leaving
        this function to wrap any checks/logging/etc.

        Args:
            file_path (str): The file system path to the configuration file.

        Returns:
            bool: ``True`` if the given ``file_path`` was parsed, and ``False``
                otherwise.

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
