"""
Cement core handler module.

"""

import re
from ..core import exc, meta
from ..core import backend
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class HandlerManager(object):
    """
    Manages the handler system to define, get, resolve, etc handlers with
    the Cement Framework.

    :param use_backend_globals: Whether to use backend globals (backward
        compatibility and deprecated).
    """

    def __init__(self, use_backend_globals=False):
        if use_backend_globals is True:
            self.__handlers__ = backend.__handlers__
        else:
            self.__handlers__ = {}

    def get(self, handler_type, handler_label, *args):
        """
        Get a handler object.

        :param handler_type: The type of handler (i.e. ``output``)
        :type handler_type: ``str``
        :param handler_label: The label of the handler (i.e. ``json``)
        :type handler_label: ``str``
        :param fallback:  A fallback value to return if handler_label doesn't
            exist.
        :returns: An uninstantiated handler object
        :raises: :class:`cement.core.exc.FrameworkError`

        Usage:

        .. code-block:: python

            output = app.handler.get('output', 'json')
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

        :param handler_type: The type of handler (i.e. ``output``)
        :returns: List of handlers that match ``hander_type``.
        :rtype: ``list``
        :raises: :class:`cement.core.exc.FrameworkError`

        Usage:

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

        :returns: List of handlers types (interface labels).
        :rtype: ``list``
        :raises: :class:`cement.core.exc.FrameworkError`

        Usage:

        .. code-block:: python

            app.handler.list_types()

        """
        return self.__handlers__.keys()

    def define(self, interface):
        """
        Define a handler based on the provided interface.  Defines a handler
        type based on ``<interface>.IMeta.label``.

        :param interface: The interface class that defines the interface to be
            implemented by handlers.
        :raises: :class:`cement.core.exc.InterfaceError`
        :raises: :class:`cement.core.exc.FrameworkError`

        Usage:

        .. code-block:: python

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

        if interface.IMeta.label in self.__handlers__:
            raise exc.FrameworkError("Handler type '%s' already defined!" %
                                     interface.IMeta.label)
        self.__handlers__[interface.IMeta.label] = {
            '__interface__': interface
        }

    def defined(self, handler_type):
        """
        Test whether ``handler_type`` is defined.

        :param handler_type: The name or ``handler_type`` of the handler (I.e.
            ``log``, ``config``, ``output``, etc).
        :returns: True if the handler type is defined, False otherwise.
        :rtype: ``boolean``

        Usage:

        .. code-block:: python

            app.handler.defined('log')

        """
        if handler_type in self.__handlers__:
            return True
        else:
            return False

    def register(self, handler_obj, force=False):
        """
        Register a handler object to a handler.  If the same object is already
        registered then no exception is raised, however if a different object
        attempts to be registered to the same name a ``FrameworkError`` is
        raised.

        :param handler_obj: The uninstantiated handler object to register.
        :param force: Whether to allow replacement if an existing
         handler of the same ``label`` is already registered.
        :raises: :class:`cement.core.exc.InterfaceError`
        :raises: :class:`cement.core.exc.FrameworkError`

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

        if handler_type not in self.__handlers__:
            raise exc.FrameworkError("Handler type '%s' doesn't exist." %
                                     handler_type)
        if obj._meta.label in self.__handlers__[handler_type] and \
                self.__handlers__[handler_type][obj._meta.label] != orig_obj:

            if force is True:
                LOG.debug(
                    "handlers['%s']['%s'] already exists" %
                    (handler_type, obj._meta.label) +
                    ", but `force==True`"
                )
            else:
                raise exc.FrameworkError(
                    "handlers['%s']['%s'] already exists" %
                    (handler_type, obj._meta.label)
                )

        interface = self.__handlers__[handler_type]['__interface__']
        if hasattr(interface.IMeta, 'validator'):
            interface.IMeta().validator(obj)
        else:
            LOG.debug("Interface '%s' does not have a validator() function!" %
                      interface)

        self.__handlers__[handler_type][obj._meta.label] = orig_obj

    def registered(self, handler_type, handler_label):
        """
        Check if a handler is registered.

        :param handler_type: The type of handler (interface label)
        :param handler_label: The label of the handler
        :returns: True if the handler is registered, False otherwise
        :rtype: ``boolean``

        Usage:

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
        the handler to load from self.__handlers__, or it can be an
        instantiated or non-instantiated handler class.

        :param handler_type: The type of handler (aka the interface label)
        :param handler_def: The handler as defined in CementApp.Meta.
        :type handler_def: str, uninstantiated object, or instantiated object
        :keyword raise_error: Whether or not to raise an exception if unable
            to resolve the handler.
        :type raise_error: boolean
        :keywork meta_defaults: Optional meta-data dictionary used as
         defaults to pass when instantiating uninstantiated handlers.  See
         ``CementApp.Meta.meta_defaults``.
        :returns: The instantiated handler object.

        Usage:

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
        in the ``[<config_section>]`` block.  These are defaults and do not
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
        must ``setup`` the handler object making it ready for the framework
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


def get(handler_type, handler_label, *args):
    """
    DEPRECATION WARNING: This function is deprecated as of Cement 2.7.x and
    will be removed in future versions of Cement.
    Use ``CementApp.handler.get()`` instead.

    ---

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

        from cement.core import handler
        output = handler.get('output', 'json')
        output.render(dict(foo='bar'))

    """
    # only log debug for now as this won't be removed until Cement 3.x and
    # we don't have access to CementApp.Meta.ignore_deprecation_warnings here
    LOG.debug(
        'Cement Deprecation Warning: `handler.get()` has been deprecated, '
        'and will be removed in future versions of Cement.  You should now '
        'use `CementApp.handler.get()` instead.'
    )

    if handler_type not in backend.__handlers__:
        raise exc.FrameworkError("handler type '%s' does not exist!" %
                                 handler_type)

    if handler_label in backend.__handlers__[handler_type]:
        return backend.__handlers__[handler_type][handler_label]
    elif len(args) > 0:
        return args[0]
    else:
        raise exc.FrameworkError("handlers['%s']['%s'] does not exist!" %
                                 (handler_type, handler_label))


def list(handler_type):
    """
    DEPRECATION WARNING: This function is deprecated as of Cement 2.7.x and
    will be removed in future versions of Cement.
    Use ``CementApp.handler.list()`` instead.

    ---

    Return a list of handlers for a given type.

    :param handler_type: The type of handler (i.e. 'output')
    :returns: List of handlers that match `type`.
    :rtype: ``list``
    :raises: cement.core.exc.FrameworkError

    """
    # only log debug for now as this won't be removed until Cement 3.x and
    # we don't have access to CementApp.Meta.ignore_deprecation_warnings here
    LOG.debug(
        'Cement Deprecation Warning: `handler.list()` has been deprecated, '
        'and will be removed in future versions of Cement.  You should now '
        'use `CementApp.handler.list()` instead.'
    )

    if handler_type not in backend.__handlers__:
        raise exc.FrameworkError("handler type '%s' does not exist!" %
                                 handler_type)

    res = []
    for label in backend.__handlers__[handler_type]:
        if label == '__interface__':
            continue
        res.append(backend.__handlers__[handler_type][label])
    return res


def define(interface):
    """
    DEPRECATION WARNING: This function is deprecated as of Cement 2.7.x and
    will be removed in future versions of Cement.
    Use ``CementApp.handler.define()`` instead.

    ---

    Define a handler based on the provided interface.  Defines a handler type
    based on <interface>.IMeta.label.

    :param interface: The interface class that defines the interface to be
        implemented by handlers.
    :raises: cement.core.exc.InterfaceError
    :raises: cement.core.exc.FrameworkError

    Usage:

    .. code-block:: python

        from cement.core import handler

        handler.define(IDatabaseHandler)

    """
    # only log debug for now as this won't be removed until Cement 3.x and
    # we don't have access to CementApp.Meta.ignore_deprecation_warnings here
    LOG.debug(
        'Cement Deprecation Warning: `handler.define()` has been deprecated, '
        'and will be removed in future versions of Cement.  You should now '
        'use `CementApp.handler.define()` instead.'
    )

    if not hasattr(interface, 'IMeta'):
        raise exc.InterfaceError("Invalid %s, " % interface +
                                 "missing 'IMeta' class.")
    if not hasattr(interface.IMeta, 'label'):
        raise exc.InterfaceError("Invalid %s, " % interface +
                                 "missing 'IMeta.label' class.")

    LOG.debug("defining handler type '%s' (%s)" %
              (interface.IMeta.label, interface.__name__))

    if interface.IMeta.label in backend.__handlers__:
        raise exc.FrameworkError("Handler type '%s' already defined!" %
                                 interface.IMeta.label)
    backend.__handlers__[interface.IMeta.label] = {'__interface__': interface}


def defined(handler_type):
    """
    DEPRECATION WARNING: This function is deprecated as of Cement 2.7.x and
    will be removed in future versions of Cement.
    Use ``CementApp.handler.defined()`` instead.

    ---

    Test whether a handler type is defined.

    :param handler_type: The name or 'type' of the handler (I.e. 'logging').
    :returns: True if the handler type is defined, False otherwise.
    :rtype: ``boolean``

    """
    # only log debug for now as this won't be removed until Cement 3.x and
    # we don't have access to CementApp.Meta.ignore_deprecation_warnings here
    LOG.debug(
        'Cement Deprecation Warning: `handler.defined()` has been deprecated, '
        'and will be removed in future versions of Cement.  You should now '
        'use `CementApp.handler.defined()` instead.'
    )

    if handler_type in backend.__handlers__:
        return True
    else:
        return False


def register(handler_obj, force=False):
    """
    DEPRECATION WARNING: This function is deprecated as of Cement 2.7.x and
    will be removed in future versions of Cement.
    Use ``CementApp.handler.register()`` instead.

    ---

    Register a handler object to a handler.  If the same object is already
    registered then no exception is raised, however if a different object
    attempts to be registered to the same name a FrameworkError is
    raised.

    :param handler_obj: The uninstantiated handler object to register.
    :param force: Whether to allow replacement if an existing
     handler of the same ``label`` is already registered.
    :raises: cement.core.exc.InterfaceError
    :raises: cement.core.exc.FrameworkError

    Usage:

    .. code-block:: python

        from cement.core import handler

        class MyDatabaseHandler(object):
            class Meta:
                interface = IDatabase
                label = 'mysql'

            def connect(self):
            ...

        handler.register(MyDatabaseHandler)

    """
    # only log debug for now as this won't be removed until Cement 3.x and
    # we don't have access to CementApp.Meta.ignore_deprecation_warnings here
    LOG.debug(
        'Cement Deprecation Warning: `handler.register()` has been '
        'deprecated, and will be removed in future versions of Cement.  You '
        'should now use `CementApp.handler.register()` instead.'
    )

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

    if handler_type not in backend.__handlers__:
        raise exc.FrameworkError("Handler type '%s' doesn't exist." %
                                 handler_type)
    if obj._meta.label in backend.__handlers__[handler_type] and \
            backend.__handlers__[handler_type][obj._meta.label] != obj:
        if force is True:
            LOG.debug(
                "handlers['%s']['%s'] already exists" %
                (handler_type, obj._meta.label) +
                ", but `force==True`"
            )
        else:
            raise exc.FrameworkError(
                "handlers['%s']['%s'] already exists" %
                (handler_type, obj._meta.label)
            )

    interface = backend.__handlers__[handler_type]['__interface__']
    if hasattr(interface.IMeta, 'validator'):
        interface.IMeta().validator(obj)
    else:
        LOG.debug("Interface '%s' does not have a validator() function!" %
                  interface)

    backend.__handlers__[handler_type][obj.Meta.label] = orig_obj


def registered(handler_type, handler_label):
    """
    DEPRECATION WARNING: This function is deprecated as of Cement 2.7.x and
    will be removed in future versions of Cement.
    Use ``CementApp.handler.registered()`` instead.

    ---

    Check if a handler is registered.

    :param handler_type: The type of handler (interface label)
    :param handler_label: The label of the handler
    :returns: True if the handler is registered, False otherwise
    :rtype: ``boolean``

    """
    # only log debug for now as this won't be removed until Cement 3.x and
    # we don't have access to CementApp.Meta.ignore_deprecation_warnings here
    LOG.debug(
        'Cement Deprecation Warning: `handler.registered()` has been '
        'deprecated, and will be removed in future versions of Cement.  You '
        'should now use `CementApp.handler.registered()` instead.'
    )

    if handler_type in backend.__handlers__ and \
       handler_label in backend.__handlers__[handler_type]:
        return True

    return False


def resolve(handler_type, handler_def, raise_error=True):
    """
    DEPRECATION WARNING: This function is deprecated as of Cement 2.7.x and
    will be removed in future versions of Cement.
    Use ``CementApp.handler.resolve()`` instead.

    ---

    Resolves the actual handler, as it can be either a string identifying
    the handler to load from backend.__handlers__, or it can be an
    instantiated or non-instantiated handler class.

    :param handler_type: The type of handler (aka the interface label)
    :param hander_def: The handler as defined in CementApp.Meta.
    :type handler_def: str, uninstantiated object, or instantiated object
    :param raise_error: Whether or not to raise an exception if unable
        to resolve the handler.
    :type raise_error: boolean
    :returns: The instantiated handler object.

    """
    # only log debug for now as this won't be removed until Cement 3.x and
    # we don't have access to CementApp.Meta.ignore_deprecation_warnings here
    LOG.debug(
        'Cement Deprecation Warning: `handler.resove()` has been '
        'deprecated, and will be removed in future versions of Cement.  You '
        'should now use `CementApp.handler.resolve()` instead.'
    )

    han = None
    if type(handler_def) == str:
        han = get(handler_type, handler_def)()
    elif hasattr(handler_def, '_meta'):
        if not registered(handler_type, handler_def._meta.label):
            register(handler_def.__class__)
        han = handler_def
    elif hasattr(handler_def, 'Meta'):
        han = handler_def()
        if not registered(handler_type, han._meta.label):
            register(handler_def)

    msg = "Unable to resolve handler '%s' of type '%s'" % \
          (handler_def, handler_type)
    if han is not None:
        return han
    elif han is None and raise_error:
        raise exc.FrameworkError(msg)
    elif han is None:
        LOG.debug(msg)
        return None
