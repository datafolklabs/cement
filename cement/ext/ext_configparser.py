"""

The ConfigParser Extension provides configuration handling based on
the standard :py:class:`ConfigParser`, and is the default configuration
handler used by Cement.

Requirements
------------

  * No external dependencies.


Configuration
-------------

This extension does not honor any application configuration settings.


Usage
-----

.. code-block:: python

    from cement import App

    with App() as app:
        app.run()

        # get a config setting
        app.config.get('myapp', 'foo')

        # set a config setting
        app.config.set('myapp', 'foo', 'bar2')

        # etc.
"""

import sys
from ..core import config
from ..utils.misc import minimal_logger

if sys.version_info[0] < 3:
    from ConfigParser import RawConfigParser  # pragma: no cover
else:
    from configparser import RawConfigParser  # pragma: no cover

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
        for section in list(dict_obj.keys()):
            if type(dict_obj[section]) == dict:
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

    def get(self, section, key):
        return RawConfigParser.get(self, section, key)

    def has_section(self, section):
        return RawConfigParser.has_section(self, section)

    def set(self, section, key, value):
        return RawConfigParser.set(self, section, key, value)

def load(app):
    app.handler.register(ConfigParserConfigHandler)
