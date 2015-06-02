"""
Cement core handler module.

"""

import re
import sys
from ..core import exc, meta
from ..utils.misc import minimal_logger, _inspect_app

LOG = minimal_logger(__name__)

if sys.version_info[0] < 3:
    builtins = __builtin__  # noqa
else:
    builtins = __builtins__  # noqa


class CementBaseHandler(meta.MetaMixin):

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
        A config [section] to merge config_defaults with.

        Note: Though Meta.config_section defaults to None, Cement will
        set this to the value of ``<interface_label>.<handler_label>`` if
        no section is set by the user/developer.
        """

        config_defaults = None
        """
        A config dictionary that is merged into the applications config
        in the [<config_section>] block.  These are defaults and do not
        override any existing defaults under that section.
        """

        overridable = False
        """
        Whether or not handler can be overridden by
        ``CementApp.Meta.handler_override_options``.  Will be listed as an
        available choice to override the specific handler (i.e.
        ``CementApp.Meta.output_handler``, etc).
        """

    def __init__(self, **kw):
        super(CementBaseHandler, self).__init__(**kw)
        self.app = None

    def _setup(self, app_obj):
        """
        The _setup function is called during application initialization and
        must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.

        :param app_obj: The application object.
        :returns: None

        """
        self.app = app_obj

        if self._meta.config_section is None:
            self._meta.config_section = "%s.%s" % \
                (self._meta.interface.IMeta.label, self._meta.label)

        if self._meta.config_defaults is not None:
            LOG.debug("merging config defaults from '%s' " % self +
                      "into section '%s'" % self._meta.config_section)
            dict_obj = dict()
            dict_obj[self._meta.config_section] = self._meta.config_defaults
            self.app.config.merge(dict_obj, override=False)


class _Dict(dict):
    """Dict with custom attributes."""


class Handlers(object):
    """Application-dependent handlers."""

    def __init__(self):
        self._handlers = {}

    def get(self, handler_type, handler_label=None, *args):
        """
        Get a handler object.

        Required Arguments:

        :param handler_type: The type of handler (i.e. 'output')
        :type handler_type: str
        :param handler_label: The label of the handler (i.e. 'json')
        :type handler_label: str
        :param fallback:  A fallback value to return if handler_label doesn't
            exist.
        :returns: An uninstantiated handler object
        :raises: cement.core.exc.FrameworkError

        Usage:

            from cement.core.foundation import CementApp
            app = CementApp('app')
            output = app.handler.get('output', 'json')
            output.render(dict(foo='bar'))

        """
        try:
            handlers = self._handlers[handler_type]
        except KeyError:
            raise exc.FrameworkError("handler type '%s' does not exist!" %
                                     handler_type)
        if handler_label is None:
            return handlers

        try:
            return handlers[handler_label]
        except KeyError:
            if len(args) > 0:
                return args[0]
            raise exc.FrameworkError("handlers['%s']['%s'] does not exist!" %
                                     (handler_type, handler_label))

    def define(self, interface):
        """
        Define a handler based on the provided interface.  Defines a handler
        type based on <interface>.IMeta.label.

        :param interface: The interface class that defines the interface to be
            implemented by handlers.
        :raises: cement.core.exc.InterfaceError
        :raises: cement.core.exc.FrameworkError

        Usage:

        .. code-block:: python

            from cement.core.foundation import CementApp

            app = CementApp('app')
            app.handler.define(IDatabaseHandler)

        """
        if not hasattr(interface, 'IMeta'):
            raise exc.InterfaceError("Invalid %s, " % interface +
                                     "missing 'IMeta' class.")
        if not hasattr(interface.IMeta, 'label'):
            raise exc.InterfaceError("Invalid %s, " % interface +
                                     "missing 'IMeta.label' class.")

        LOG.debug("defining handler type '%s' (%s)" %
                  (interface.IMeta.label, interface.__name__))

        if interface.IMeta.label in self._handlers:
            raise exc.FrameworkError("Handler type '%s' already defined!" %
                                     interface.IMeta.label)
        obj = self._handlers[interface.IMeta.label] = _Dict()
        obj._interface = interface

    def defined(self, handler_type):
        """
        Test whether a handler type is defined.

        :param handler_type: The name or 'type' of the handler
                             (I.e. 'logging').
        :returns: True if the handler type is defined, False otherwise.
        :rtype: boolean

        """
        return handler_type in self._handlers

    def register(self, handler_obj):
        """
        Register a handler object to a handler.  If the same object is already
        registered then no exception is raised, however if a different object
        attempts to be registered to the same name a FrameworkError is
        raised.

        :param handler_obj: The uninstantiated handler object to register.
        :raises: cement.core.exc.InterfaceError
        :raises: cement.core.exc.FrameworkError

        Usage:

        .. code-block:: python

            from cement.core.foundation import CementApp

            class MyDatabaseHandler(object):
                class Meta:
                    interface = IDatabase
                    label = 'mysql'

                def connect(self):
                ...

            app = CementApp('app')
            app.handler.register(MyDatabaseHandler)

        """

        orig_obj = handler_obj

        # for checks
        obj = orig_obj()

        if not hasattr(obj._meta, 'label') or not obj._meta.label:
            raise exc.InterfaceError("Invalid handler %s, " % orig_obj +
                                     "missing '_meta.label'.")
        if not hasattr(obj._meta, 'interface') or not obj._meta.interface:
            raise exc.InterfaceError("Invalid handler %s, " % orig_obj +
                                     "missing '_meta.interface'.")

        # translate dashes to underscores
        orig_obj.Meta.label = re.sub('-', '_', obj._meta.label)
        obj._meta.label = re.sub('-', '_', obj._meta.label)

        handler_type = obj._meta.interface.IMeta.label
        LOG.debug("registering handler '%s' into handlers['%s']['%s']" %
                  (orig_obj, handler_type, obj._meta.label))

        if handler_type not in self._handlers:
            raise exc.FrameworkError("Handler type '%s' doesn't exist." %
                                     handler_type)
        if obj._meta.label in self._handlers[handler_type] and \
                self._handlers[handler_type][obj._meta.label] != obj:
            raise exc.FrameworkError("handlers['%s']['%s'] already exists" %
                                     (handler_type, obj._meta.label))

        interface = self._handlers[handler_type]._interface
        if hasattr(interface.IMeta, 'validator'):
            interface.IMeta().validator(obj)
        else:
            LOG.debug("Interface '%s' does not have a validator() function!" %
                      interface)

        self._handlers[handler_type][obj.Meta.label] = orig_obj

    def registered(self, handler_type, handler_label):
        """
        Check if a handler is registered.

        :param handler_type: The type of handler (interface label)
        :param handler_label: The label of the handler
        :returns: True if the handler is registered, False otherwise
        :rtype: boolean

        """
        return (handler_type in self._handlers and
                handler_label in self._handlers[handler_type])

    def resolve(self, handler_type, handler_def, raise_error=True):
        """
        Resolves the actual handler, as it can be either a string identifying
        the handler to load from self._handlers, or it can be an
        instantiated or non-instantiated handler class.

        :param handler_type: The type of handler (aka the interface label)
        :param hander_def: The handler as defined in CementApp.Meta.
        :type handler_def: str, uninstantiated object, or instantiated object
        :param raise_error: Whether or not to raise an exception if unable
            to resolve the handler.
        :type raise_error: boolean
        :returns: The instantiated handler object.

        """
        han = None
        if type(handler_def) == str:
            han = self.get(handler_type, handler_def)()
        elif hasattr(handler_def, '_meta'):
            if not self.registered(handler_type, handler_def._meta.label):
                self.register(handler_def.__class__)
            han = handler_def
        elif hasattr(handler_def, 'Meta'):
            han = handler_def()
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


# Backwards compatibility
def get(handler_type, handler_label, *args):
    # TODO: deprecation warning
    app = _inspect_app(sys._getframe(1))
    return app.handlers.get(handler_type, handler_label, *args)


def list(handler_type):
    # TODO: deprecation warning
    app = _inspect_app(sys._getframe(1))
    return builtins['list'](app.handlers.get(handler_type).values())


def define(interface):
    # TODO: deprecation warning
    app = _inspect_app(sys._getframe(1))
    app.handlers.define(interface)


def defined(handler_type):
    # TODO: deprecation warning
    app = _inspect_app(sys._getframe(1))
    return app.handlers.defined(handler_type)


def register(handler_obj):
    # TODO: deprecation warning
    app = _inspect_app(sys._getframe(1))
    app.handlers.register(handler_obj)


def registered(handler_type, handler_label):
    # TODO: deprecation warning
    app = _inspect_app(sys._getframe(1))
    return app.handlers.registered(handler_type, handler_label)


def resolve(handler_type, handler_def, raise_error=True):
    # TODO: deprecation warning
    app = _inspect_app(sys._getframe(1))
    return app.handlers.resolve(handler_type, handler_def, raise_error)
