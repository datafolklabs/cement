"""
Cement core interface module.
"""

from abc import ABC
from ..core import exc, meta
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class Interface(ABC, meta.MetaMixin):

    """Base interface class that all Cement Interfaces should subclass from."""

    class Meta:

        """
        Interface meta-data (can also be passed as keyword arguments to the
        parent class).

        """

        interface = NotImplemented
        """The string identifier of this interface."""

    def __init__(self, **kw):
        super(Interface, self).__init__(**kw)
        try:
            assert self._meta.interface, \
                "%s.Meta.interface undefined." % self.__class__.__name__
        except AssertionError as e:
            raise exc.InterfaceError(e.args[0])

    def _validate(self):
        """
        Perform any validation to ensure proper data, meta-data, etc.
        """
        pass


class InterfaceManager(object):
    """
    Manages the interface system to define, get, list interfaces with
    the Cement Framework.

    """

    def __init__(self, app):
        self.app = app
        self.__interfaces__ = {}

    def get(self, interface, fallback=None, **kwargs):
        """
        Get an interface class.

        Args:
            interface (str): The interface label (i.e. ``output``)
            fallback (Handler):  A fallback value to return if ``interface``
                doesn't exist.

        Returns:
            Interface: An uninstantiated interface class

        Raises:
            cement.core.exc.InterfaceError: If the ``interface`` does not
                exist.

        Example:

            .. code-block:: python

                i = app.interface.get('output')

        """

        if interface in self.__interfaces__.keys():
            return self.__interfaces__[interface]
        elif fallback is not None:
            return fallback
        else:
            raise exc.InterfaceError("interface '%s' does not exist!" %
                                     interface)

    def list(self):
        """
        Return a list of defined interfaces.

        Returns:
            list: Interface labels.

        Example:

            .. code-block:: python

                app.interface.list()

        """
        return list(self.__interfaces__.keys())

    def define(self, ibc):
        """
        Define an ``ibc`` (interface base class).

        Args:
            ibc (Interface): The abstract base class that defines the interface

        Raises:
            cement.core.exc.InterfaceError: If the interface label is already
            defined

        Example:

            .. code-block:: python

                app.interface.define(DatabaseInterface)

        """

        LOG.debug("defining interface '%s' (%s)" %
                  (ibc.Meta.interface, ibc.__name__))

        if ibc.Meta.interface in self.__interfaces__:
            msg = "interface '%s' already defined!" % ibc.Meta.interface
            raise exc.InterfaceError(msg)
        self.__interfaces__[ibc.Meta.interface] = ibc

    def defined(self, interface):
        """
        Test whether ``interface`` is defined.

        Args:
            interface (str): The label of the interface (I.e.
                ``log``, ``config``, ``output``, etc).

        Returns:
            bool: ``True`` if the interface is defined, ``False`` otherwise

        Example:

            .. code-block:: python

                app.interface.defined('log')

        """
        if interface in self.__interfaces__:
            return True
        else:
            return False
