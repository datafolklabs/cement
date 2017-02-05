"""Cement core extensions module."""

import sys
from abc import ABC, abstractmethod, abstractproperty
from ..core import exc
from ..core.handler import Handler
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class ExtensionHandlerBase(Handler):

    """
    This class defines the Extension Handler Interface.  Classes that
    implement this handler must provide the methods and attributes defined
    below.

    Usage:

    .. code-block:: python

        from cement.core.extension import ExtensionHandlerBase

        class MyExtensionHandler(ExtensionHandlerBase):
            class Meta:
                interface = extension.IExtension
                label = 'my_extension_handler'
            ...

    """

    class Meta:

        """Handler meta-data."""

        #: The string identifier of the interface.
        interface = 'extension'

    @abstractmethod
    def load_extension(self, ext_module):
        """
        Load an extension whose module is 'ext_module'.  For example,
        'cement.ext.ext_json'.

        :param ext_module: The name of the extension to load.
        :type ext_module: ``str``

        """
        pass

    @abstractmethod
    def load_extensions(self, ext_list):
        """
        Load all extensions from ext_list.

        :param ext_list: A list of extension modules to load.  For example:
            ``['cement.ext.ext_json', 'cement.ext.ext_logging']``

        :type ext_list: ``list``

        """
        pass


class ExtensionHandler(ExtensionHandlerBase):

    class Meta:

        """
        Handler meta-data (can be passed as keyword arguments to the parent
        class).
        """

        label = 'cement'
        """The string identifier of the handler."""

    def __init__(self, **kw):
        """
        This handler defines the Extention Interface, which handles
        loading framework extensions.  All extension  handlers should
        sub-class from here, or ensure that their implementation meets the
        requirements of this base class.

        """
        super().__init__(**kw)
        self.app = None
        self._loaded_extensions = []

    def get_loaded_extensions(self):
        """Returns a list of loaded extensions."""
        return self._loaded_extensions

    def load_extension(self, ext_module):
        """
        Given an extension module name, load or in other-words 'import' the
        extension.

        :param ext_module: The extension module name.  For example:
            'cement.ext.ext_logging'.
        :type ext_module: ``str``
        :raises: cement.core.exc.FrameworkError

        """
        # If its not a full module path then preppend our default path
        if ext_module.find('.') == -1:
            ext_module = 'cement.ext.ext_%s' % ext_module

        if ext_module in self._loaded_extensions:
            LOG.debug("framework extension '%s' already loaded" % ext_module)
            return

        LOG.debug("loading the '%s' framework extension" % ext_module)
        try:
            if ext_module not in sys.modules:
                __import__(ext_module, globals(), locals(), [], 0)

            if hasattr(sys.modules[ext_module], 'load'):
                sys.modules[ext_module].load(self.app)

            if ext_module not in self._loaded_extensions:
                self._loaded_extensions.append(ext_module)

        except ImportError as e:
            raise exc.FrameworkError(e.args[0])

    def load_extensions(self, ext_list):
        """
        Given a list of extension modules, iterate over the list and pass
        individually to self.load_extension().

        :param ext_list: A list of extension modules.
        :type ext_list: ``list``

        """
        for ext in ext_list:
            self.load_extension(ext)
