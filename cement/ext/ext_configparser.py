"""
Cement configparser extension module.
"""

import os
import re
from ..core import config
from ..utils.misc import minimal_logger
from configparser import RawConfigParser

LOG = minimal_logger(__name__)


class ConfigParserConfigHandler(config.ConfigHandler, RawConfigParser):

    """
    This class is an implementation of the :ref:`Config <cement.core.config>`
    interface.  It handles configuration file parsing and the like by
    sub-classing from the standard `ConfigParser
    <http://docs.python.org/library/configparser.html>`_
    library.  Please see the ConfigParser documentation for full usage of the
    class.

    Additional arguments and keyword arguments are passed directly to
    RawConfigParser on initialization.
    """
    class Meta:

        """Handler meta-data."""

        label = 'configparser'
        """The string identifier of this handler."""

    def merge(self, dict_obj, override=True):
        """
        Merge a dictionary into our config.  If override is True then
        existing config values are overridden by those passed in.

        Args:
            dict_obj (dict): A dictionary of configuration keys/values to merge
                into our existing config (self).

        Keyword Args:
            override (bool):  Whether or not to override existing values in the
                config.

        """
        assert isinstance(dict_obj, dict), "Dictionary object required."

        for section in list(dict_obj.keys()):
            if type(dict_obj[section]) is dict:
                if section not in self.get_sections():
                    self.add_section(section)

                for key in list(dict_obj[section].keys()):
                    if override:
                        self.set(section, key, dict_obj[section][key])
                    else:
                        # only set it if the key doesn't exist
                        if key not in self.keys(section):
                            self.set(section, key, dict_obj[section][key])

                # we don't support nested config blocks, so no need to go
                # further down to more nested dicts.

    def _parse_file(self, file_path):
        """
        Parse a configuration file at ``file_path`` and store it.

        Args:
            file_path (str): The file system path to the configuration file.

        Returns:
            bool: ``True`` if file was read properly, ``False`` otherwise

        """
        self.read(file_path)

        # FIX ME: Should check that file was read properly, however if not it
        # will likely raise an exception anyhow.
        return True

    def keys(self, section):
        """
        Return a list of keys within ``section``.

        Args:
            section (str): The config section

        Returns:
            list: List of keys in the ``section``.

        """
        return self.options(section)

    def get_dict(self):
        """
        Return a dict of the entire configuration.

        Returns:
            dict: A dictionary of the entire config.
        """
        _config = {}
        for section in self.get_sections():
            _config[section] = self.get_section_dict(section)
        return _config

    def get_sections(self):
        """
        Return a list of configuration sections.

        Returns:
            list: List of sections

        """
        return self.sections()

    def get_section_dict(self, section):
        """
        Return a dict representation of a section.

        Args:
            section: The section of the configuration.

        Returns:
            dict: Dictionary reprisentation of the config section.

        """
        dict_obj = dict()
        for key in self.keys(section):
            dict_obj[key] = self.get(section, key)
        return dict_obj

    def add_section(self, section):
        """
        Adds a block section to the config.

        Args:
            section (str): The section to add.

        """
        return RawConfigParser.add_section(self, section)

    def _get_env_var(self, section, key):
        if section == self.app._meta.config_section:
            env_var = "%s_%s" % (self.app._meta.config_section, key)
        else:
            env_var = "%s_%s_%s" % (
                self.app._meta.config_section, section, key)

        env_var = env_var.upper()
        env_var = re.sub('[^0-9a-zA-Z_]+', '_', env_var)
        return env_var

    def get(self, section, key, **kwargs):
        env_var = self._get_env_var(section, key)

        if env_var in os.environ.keys():
            return os.environ[env_var]
        else:
            return RawConfigParser.get(self, section, key, **kwargs)

    def has_section(self, section):
        return RawConfigParser.has_section(self, section)

    def set(self, section, key, value):
        return RawConfigParser.set(self, section, key, value)


def load(app):
    app.handler.register(ConfigParserConfigHandler)
