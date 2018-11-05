"""
Cement plugin extension module.
"""

import os
import sys
import imp
import re
from ..core import plugin, exc
from ..utils.misc import is_true, minimal_logger
from ..utils.fs import abspath

LOG = minimal_logger(__name__)

# FIX ME: This is a redundant name... ?


class CementPluginHandler(plugin.PluginHandler):

    """
    This class is an internal implementation of the
    :ref:`IPlugin <cement.core.plugin>` interface. It does not take any
    parameters on initialization.

    """

    class Meta:

        """Handler meta-data."""

        label = 'cement'
        """The string identifier for this class."""

    def __init__(self):
        super().__init__()
        self._loaded_plugins = []
        self._enabled_plugins = []
        self._disabled_plugins = []

    def _setup(self, app_obj):
        super()._setup(app_obj)
        self._enabled_plugins = []
        self._disabled_plugins = []
        self.bootstrap = self.app._meta.plugin_module
        self.load_dirs = self.app._meta.plugin_dirs

        # parse all app configs for plugins. Note: these are already
        # loaded from files when app.config was setup.  The application
        # configuration OVERRIDES plugin configs.
        for section in self.app.config.get_sections():
            if not section.startswith('plugin.'):
                continue
            plugin_section = section
            plugin = re.sub('^plugin.', '', section)

            if 'enabled' not in self.app.config.keys(plugin_section):
                continue
            if is_true(self.app.config.get(plugin_section, 'enabled')):
                LOG.debug("enabling plugin '%s' per application config" %
                          plugin)
                if plugin not in self._enabled_plugins:
                    self._enabled_plugins.append(plugin)  # pragma: nocover
                if plugin in self._disabled_plugins:
                    self._disabled_plugins.remove(plugin)  # pragma: nocover
            else:
                LOG.debug("disabling plugin '%s' per application config" %
                          plugin)
                if plugin not in self._disabled_plugins:
                    self._disabled_plugins.append(plugin)  # pragma: nocover
                if plugin in self._enabled_plugins:
                    self._enabled_plugins.remove(plugin)  # pragma: nocover

    def _load_plugin_from_dir(self, plugin_name, plugin_dir):
        """
        Load a plugin from a directory path rather than a python package
        within sys.path.  This would either be ``myplugin.py`` or
        ``myplugin/__init__.py`` within the given ``plugin_dir``.

        Args:
            plugin_name (str): The name of the plugin.
            plugin_dir (str): The filesystem directory path where the plugin
                exists.

        """

        # FIX ME: `imp` is deprecated in Python 3.4 and will be  going away
        # so we need to update forward compatibility for ``importlib``.
        #
        # See: https://github.com/datafolklabs/cement/issues/386

        LOG.debug("attempting to load '%s' from '%s'" % (plugin_name,
                                                         plugin_dir))

        if not os.path.exists(plugin_dir):
            LOG.debug("plugin directory '%s' does not exist." % plugin_dir)
            return False

        try:
            f, path, desc = imp.find_module(plugin_name, [plugin_dir])
        except ImportError:
            LOG.debug("plugin '%s' does not exist in '%s'." %
                      (plugin_name, plugin_dir))
            return False

        # We don't catch this because it would make debugging a
        # nightmare
        mod = imp.load_module(plugin_name, f, path, desc)
        if mod and hasattr(mod, 'load'):
            mod.load(self.app)
        return True

    def _load_plugin_from_bootstrap(self, plugin_name, base_package):
        """
        Load a plugin from a python package.  Returns True if no ImportError
        is encountered.

        Args:
            plugin_name (str): The name of the plugin, also the name of the
                module to load from base_package. I.e.
                ``myapp.bootstrap.myplugin``
            base_package: The base python package to load the plugin module
                from.  I.e. ``myapp.bootstrap`` or similar.

        Returns:
            bool: ``True`` is the plugin was loaded, ``False`` otherwise

        Raises:
            :py:class:`ImportError`: If the plugin can not be imported

        """

        full_module = '%s.%s' % (base_package, plugin_name)

        # If the base package doesn't exist, we return False rather than
        # bombing out.
        if base_package not in sys.modules:
            try:
                __import__(base_package, globals(), locals(), [], 0)
            except ImportError:
                LOG.debug("unable to import plugin bootstrap module '%s'."
                          % base_package)
                return False

        LOG.debug("attempting to load '%s' from '%s'" % (plugin_name,
                                                         base_package))
        # We don't catch this because it would make debugging a nightmare
        # FIXME: not sure how to test/cover this
        if full_module not in sys.modules:
            __import__(full_module,
                       globals(), locals(), [], 0)  # pragma: nocover

        if hasattr(sys.modules[full_module], 'load'):
            sys.modules[full_module].load(self.app)

        return True

    def load_plugin(self, plugin_name):
        """
        Load a plugin whose name is ``plugin_name``.  First attempt to load
        from a plugin directory (plugin_dir), secondly attempt to load from a
        Python module determined by ``App.Meta.plugin_module``.

        Upon successful loading of a plugin, the plugin name is appended to
        the ``self._loaded_plugins list``.

        Args:
            plugin_name (str): The name of the plugin to load.

        Raises:
            cement.core.exc.FrameworkError: If the plugin can not be loaded

        """
        LOG.debug("loading application plugin '%s'" % plugin_name)

        # first attempt to load from plugin_dirs
        for load_dir in self.load_dirs:
            load_dir = abspath(load_dir)

            if self._load_plugin_from_dir(plugin_name, load_dir):
                self._loaded_plugins.append(plugin_name)
                break

        # then from a bootstrap module
        if plugin_name not in self._loaded_plugins:
            if self._load_plugin_from_bootstrap(plugin_name, self.bootstrap):
                self._loaded_plugins.append(plugin_name)

        # otherwise it's a bust
        if plugin_name not in self._loaded_plugins:
            raise exc.FrameworkError("Unable to load plugin '%s'." %
                                     plugin_name)

    def load_plugins(self, plugin_list):
        """
        Load a list of plugins.  Each plugin name is passed to
        ``self.load_plugin()``.

        Args:
            plugin_list (list): A list of plugin names to load.

        """
        for plugin_name in plugin_list:
            self.load_plugin(plugin_name)

    def get_loaded_plugins(self):
        """List of plugins that have been loaded."""
        return self._loaded_plugins

    def get_enabled_plugins(self):
        """List of plugins that are enabled (not necessary loaded yet)."""
        return self._enabled_plugins

    def get_disabled_plugins(self):
        """List of disabled plugins"""
        return self._disabled_plugins


def load(app):
    app.handler.register(CementPluginHandler)
