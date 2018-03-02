"""
Cement core handler module.

"""

import re
from abc import ABC
from ..core import exc, meta
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class Handler(ABC, meta.MetaMixin):

    """Base handler class that all Cement Handlers should subclass from."""

    class Meta:

        """
        Handler meta-data (can also be passed as keyword arguments to the
        parent class).

        """

        label = None
        """The string identifier of this handler."""

        interface = None
        """The interface that this class implements."""

        config_section = None
        """
        A config section to merge config_defaults with.

        Note: Though ``App.Meta.config_section`` defaults to ``None``, Cement
        will set this to the value of ``<interface_label>.<handler_label>`` if
        no section is set by the user/developer.
        """

        config_defaults = None
        """
        A config dictionary that is merged into the applications config
        in the ``[<config_section>]`` block.  These are defaults and do not
        override any existing defaults under that section.
        """

        overridable = False
        """
        Whether or not handler can be overridden by
        ``App.Meta.handler_override_options``.  Will be listed as an
        available choice to override the specific handler (i.e.
        ``App.Meta.output_handler``, etc).
        """

    def __init__(self, **kw):
        super(Handler, self).__init__(**kw)
        try:
            assert self._meta.label, \
                "%s.Meta.label undefined." % self.__class__.__name__
            assert self._meta.interface, \
                "%s.Meta.interface undefined." % self.__class__.__name__
        except AssertionError as e:
            raise(exc.FrameworkError(e.args[0]))

        self.app = None

    def _setup(self, app):
        """
        Called during application initialization and must ``setup`` the handler
        object making it ready for the framework or the application to make
        further calls to it.

        Args:
            app (instance): The application object.

        """

        self.app = app

        if self._meta.config_section is None:
            self._meta.config_section = "%s.%s" % \
                (self._meta.interface, self._meta.label)

        if self._meta.config_defaults is not None:
            LOG.debug("merging config defaults from '%s' " % self +
                      "into section '%s'" % self._meta.config_section)
            dict_obj = dict()
            dict_obj[self._meta.config_section] = self._meta.config_defaults
            self.app.config.merge(dict_obj, override=False)

        self._validate()

    def _validate(self):
        """
        Perform any validation to ensure proper data, meta-data, etc.
        """
        pass


class HandlerManager(object):
    """
    Manages the handler system to define, get, resolve, etc handlers with
    the Cement Framework.

    """

    def __init__(self):
        self.__handlers__ = {}

    def get(self, handler_type, handler_label, *args):
        """
        Get a handler object.

        Args:
            handler_type (str): The type of handler (i.e. ``output``)
            handler_label (str): The label of the handler (i.e. ``json``)

        Keyword Args:
            fallback (Handler):  A fallback value to return if handler_label
                doesn't exist.

        Returns:
            Handler: An uninstantiated handler object

        Raises:
            cement.core.exc.FrameworkError: If the ``handler_type`` does not
                exist, or if the handler itself does not exist.

        Example:

            .. code-block:: python

                _handler = app.handler.get('output', 'json')
                output = _handler()
                output._setup(app)
                output.render(dict(foo='bar'))

        """
        if handler_type not in self.__handlers__:
            raise exc.FrameworkError("handler type '%s' does not exist!" %
                                     handler_type)

        if handler_label in self.__handlers__[handler_type]:
            return self.__handlers__[handler_type][handler_label]
        elif len(args) > 0:
            return args[0]
        else:
            raise exc.FrameworkError("handlers['%s']['%s'] does not exist!" %
                                     (handler_type, handler_label))

    def list(self, handler_type):
        """
        Return a list of handlers for a given ``handler_type``.

        Args:
            handler_type (str): The type of handler (i.e. ``output``)

        Returns:
            list: Handler labels (str) that match ``hander_type``.

        Raises:
            cement.core.exc.FrameworkError: If the ``handler_type`` does not
                exist.

        Example:

            .. code-block:: python

                app.handler.list('log')

        """
        if handler_type not in self.__handlers__:
            raise exc.FrameworkError("handler type '%s' does not exist!" %
                                     handler_type)

        res = []
        for label in self.__handlers__[handler_type]:
            if label == '__interface__':
                continue
            res.append(self.__handlers__[handler_type][label])
        return res

    def list_types(self):
        """
        Return a list of handler types (interface labels).

        Returns:
            list: Handler types (interface labels).

        Example:

            .. code-block:: python

                app.handler.list_types()

        """
        return self.__handlers__.keys()

    def define(self, handler):
        """
        Define an interface based on the provided handler.

        Args:
            handler (Handler): The handler that defines the interface
                implementation

        Raises:
            cement.core.exc.FrameworkError: If the handler type/interface is
                already defined

        Example:

            .. code-block:: python

                app.handler.define(DatabaseHandler)

        """

        LOG.debug("defining handler interface '%s' (%s)" %
                  (handler.Meta.interface, handler.__name__))

        if handler.Meta.interface in self.__handlers__:
            msg = "Handler interface '%s' already defined!" % \
                  handler.Meta.interface
            raise exc.FrameworkError(msg)
        self.__handlers__[handler.Meta.interface] = {
            '__interface__': handler
        }

    def defined(self, handler_type):
        """
        Test whether ``handler_type`` is defined.

        Args:
            handler_type (str): The label of the interface (I.e.
                ``log``, ``config``, ``output``, etc).

        Returns:
            bool: ``True`` if the handler type is defined, ``False`` otherwise

        Example:

            .. code-block:: python

                app.handler.defined('log')

        """
        if handler_type in self.__handlers__:
            return True
        else:
            return False

    def register(self, handler_class, force=False):
        """
        Register a handler class to an interface.  If the same object is
        already registered then no exception is raised, however if a different
        object attempts to be registered to the same name a ``FrameworkError``
        is raised.

        Args:
            handler_class (Handler): The uninstantiated handler class to
                register.

        Keyword Arguments:
            force (bool): Whether to allow replacement if an existing
            handler of the same ``label`` is already registered.

        Raises:
            cement.core.exc.InterfaceError: If the ``handler_class`` does not
                implement :class:`Handler`, or if ``handler_class`` does not
                properly sub-class it's interface.
            cement.core.exc.FrameworkError: If the
                ``handler_class.Meta.interface`` does not exist

        Usage:

        .. code-block:: python

            class MyDatabaseHandler(object):
                class Meta:
                    interface = IDatabase
                    label = 'mysql'

                def connect(self):
                    # ...

            app.handler.register(MyDatabaseHandler)

        """

        # for checks
        if not issubclass(handler_class, Handler):
            raise exc.InterfaceError("Class %s " % handler_class +
                                     "does not implement Handler")

        obj = handler_class()

        # translate dashes to underscores
        handler_class.Meta.label = re.sub('-', '_', obj._meta.label)
        obj._meta.label = re.sub('-', '_', obj._meta.label)

        interface = obj._meta.interface
        LOG.debug("registering handler '%s' into handlers['%s']['%s']" %
                  (handler_class, interface, obj._meta.label))

        if interface not in self.__handlers__:
            raise exc.FrameworkError("Handler interface '%s' doesn't exist." %
                                     interface)
        if obj._meta.label in self.__handlers__[interface] and \
                self.__handlers__[interface][obj._meta.label] != handler_class:

            if force is True:
                LOG.debug(
                    "handlers['%s']['%s'] already exists" %
                    (interface, obj._meta.label) +
                    ", but `force==True`"
                )
            else:
                raise exc.FrameworkError(
                    "handlers['%s']['%s'] already exists" %
                    (interface, obj._meta.label)
                )

        interface_class = self.__handlers__[interface]['__interface__']

        if not issubclass(handler_class, interface_class):
            raise exc.InterfaceError("Handler %s " % handler_class.__name__ +
                                     "does not sub-class %s" %
                                     interface_class.__name__)

        self.__handlers__[interface][obj._meta.label] = handler_class

    def registered(self, handler_type, handler_label):
        """
        Check if a handler is registered.

        Args:
            handler_type (str): The type of handler (interface label)
            handler_label (str): The label of the handler

        Returns:
            bool: ``True`` if the handler is registered, ``False`` otherwise

        Example:

            .. code-block:: python

                app.handler.registered('log', 'colorlog')

        """
        if handler_type in self.__handlers__ and \
           handler_label in self.__handlers__[handler_type]:
            return True

        return False

    def resolve(self, handler_type, handler_def, **kwargs):
        """
        Resolves the actual handler, as it can be either a string identifying
        the handler to load from ``self.__handlers__``, or it can be an
        instantiated or non-instantiated handler class.

        Args:
            handler_type (str): The type of handler (aka the interface label)
            handler_def(str,instance,Handler): The loose references of the
                handler, by label, instantiated object, or non-instantiated
                class.

        Keyword args:
            raise_error (bool): Whether or not to raise an exception if unable
                to resolve the handler.
            meta_defaults (dict): Optional meta-data dictionary used as
                defaults to pass when instantiating uninstantiated handlers.
                See ``App.Meta.meta_defaults``.

        Returns:
            instance: The instantiated handler object.

        Example:

            .. code-block:: python

                # via label (str)
                log = app.handler.resolve('log', 'colorlog')

                # via uninstantiated handler class
                log = app.handler.resolve('log', ColorLogHanddler)

                # via instantiated handler instance
                log = app.handler.resolve('log', ColorLogHandler())

        """
        raise_error = kwargs.get('raise_error', True)
        meta_defaults = kwargs.get('meta_defaults', {})
        han = None

        if type(handler_def) == str:
            han = self.get(handler_type, handler_def)(**meta_defaults)
        elif hasattr(handler_def, '_meta'):
            if not self.registered(handler_type, handler_def._meta.label):
                self.register(handler_def.__class__)
            han = handler_def
        elif hasattr(handler_def, 'Meta'):
            han = handler_def(**meta_defaults)
            if not self.registered(handler_type, han._meta.label):
                self.register(handler_def)

        msg = "Unable to resolve handler '%s' of type '%s'" % \
              (handler_def, handler_type)
        if han is not None:
            return han
        elif han is None and raise_error:
            raise exc.FrameworkError(msg)
        elif han is None:
            LOG.debug(msg)
            return None
