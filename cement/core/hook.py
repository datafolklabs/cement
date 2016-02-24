"""Cement core hooks module."""

import operator
import types
from ..core import exc, backend
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class HookManager(object):
    """
    Manages the hook system to define, get, run, etc hooks within the
    the Cement Framework and applications Built on Cement (tm).

    :param use_backend_globals: Whether to use backend globals (backward
        compatibility and deprecated).
    """

    def __init__(self, use_backend_globals=False):
        if use_backend_globals is True:
            self.__hooks__ = backend.__hooks__
        else:
            self.__hooks__ = {}

    def define(self, name):
        """
        Define a hook namespace that the application and plugins can register
        hooks in.

        :param name: The name of the hook, stored as hooks['name']
        :raises: cement.core.exc.FrameworkError

        Usage:

        .. code-block:: python

            from cement.core.foundation import CementApp

            with CementApp('myapp') as app:
                app.hook.define('my_hook_name')

        """
        LOG.debug("defining hook '%s'" % name)
        if name in self.__hooks__:
            raise exc.FrameworkError("Hook name '%s' already defined!" % name)
        self.__hooks__[name] = []

    def defined(self, hook_name):
        """
        Test whether a hook name is defined.

        :param hook_name: The name of the hook.
            I.e. ``my_hook_does_awesome_things``.
        :returns: True if the hook is defined, False otherwise.
        :rtype: ``boolean``

        Usage:

        .. code-block:: python

            from cement.core.foundation import CementApp

            with CementApp('myapp') as app:
                app.hook.defined('some_hook_name'):
                    # do something about it
                    pass


        """
        if hook_name in self.__hooks__:
            return True
        else:
            return False

    def register(self, name, func, weight=0):
        """
        Register a function to a hook.  The function will be called, in order
        of weight, when the hook is run.

        :param name: The name of the hook to register too.
            I.e. ``pre_setup``, ``post_run``, etc.
        :param func:    The function to register to the hook.  This is an
            *un-instantiated*, non-instance method, simple function.
        :param weight:  The weight in which to order the hook function.
        :type weight: ``int``

        Usage:

        .. code-block:: python

            from cement.core.foundation import CementApp

            def my_hook_func(app):
                # do something with app?
                return True

            with CementApp('myapp') as app:
                app.hook.define('my_hook_name')
                app.hook.register('my_hook_name', my_hook_func)

        """
        if name not in self.__hooks__:
            LOG.debug("hook name '%s' is not defined! ignoring..." % name)
            return False

        LOG.debug("registering hook '%s' from %s into hooks['%s']" %
                  (func.__name__, func.__module__, name))

        # Hooks are as follows: (weight, name, func)
        self.__hooks__[name].append((int(weight), func.__name__, func))

    def run(self, name, *args, **kwargs):
        """
        Run all defined hooks in the namespace.  Yields the result of each
        hook function run.

        :param name: The name of the hook function.
        :param args: Additional arguments to be passed to the hook functions.
        :param kwargs: Additional keyword arguments to be passed to the hook
            functions.
        :raises: FrameworkError

        Usage:

        .. code-block:: python

            from cement.core.foundation import CementApp

            def my_hook_func(app):
                # do something with app?
                return True

            with CementApp('myapp') as app:
                app.hook.define('my_hook_name')
                app.hook.register('my_hook_name', my_hook_func)
                for res in app.hook.run('my_hook_name', self):
                    # do something with the result?
                    pass

        """
        if name not in self.__hooks__:
            raise exc.FrameworkError("Hook name '%s' is not defined!" % name)

        # Will order based on weight (the first item in the tuple)
        self.__hooks__[name].sort(key=operator.itemgetter(0))
        for hook in self.__hooks__[name]:
            LOG.debug("running hook '%s' (%s) from %s" %
                      (name, hook[2], hook[2].__module__))
            res = hook[2](*args, **kwargs)

            # Check if result is a nested generator - needed to support e.g.
            # asyncio
            if isinstance(res, types.GeneratorType):
                for _res in res:
                    yield _res
            else:
                yield res


# the following is only used for backward compat with < 2.7.x!

def define(name):
    """
    DEPRECATION WARNING: This function is deprecated as of Cement 2.7.x and
    will be removed in future versions of Cement.
    Use ``CementApp.hook.define()`` instead.

    ---

    Define a hook namespace that plugins can register hooks in.

    :param name: The name of the hook, stored as hooks['name']
    :raises: cement.core.exc.FrameworkError

    Usage:

    .. code-block:: python

        from cement.core import hook

        hook.define('myhookname_hook')

    """
    # only log debug for now as this won't be removed until Cement 3.x and
    # we don't have access to CementApp.Meta.ignore_deprecation_warnings here
    LOG.debug(
        'Cement Deprecation Warning: `hook.define()` has been deprecated, '
        'and will be removed in future versions of Cement.  You should now '
        'use `CementApp.hook.define()` instead.'
    )
    LOG.debug("defining hook '%s'" % name)
    if name in backend.__hooks__:
        raise exc.FrameworkError("Hook name '%s' already defined!" % name)
    backend.__hooks__[name] = []


def defined(hook_name):
    """
    DEPRECATION WARNING: This function is deprecated as of Cement 2.7.x and
    will be removed in future versions of Cement.
    Use ``CementApp.hook.defined()`` instead.

    ---

    Test whether a hook name is defined.

    :param hook_name: The name of the hook.
        I.e. ``my_hook_does_awesome_things``.
    :returns: True if the hook is defined, False otherwise.
    :rtype: ``boolean``

    """
    # only log debug for now as this won't be removed until Cement 3.x and
    # we don't have access to CementApp.Meta.ignore_deprecation_warnings here
    LOG.debug(
        'Cement Deprecation Warning: `hook.defined()` has been deprecated, '
        'and will be removed in future versions of Cement.  You should now '
        'use `CementApp.hook.defined()` instead.'
    )
    if hook_name in backend.__hooks__:
        return True
    else:
        return False


def register(name, func, weight=0):
    """
    DEPRECATION WARNING: This function is deprecated as of Cement 2.7.x and
    will be removed in future versions of Cement.
    Use ``CementApp.hook.register()`` instead.

    ---

    Register a function to a hook.  The function will be called, in order of
    weight, when the hook is run.

    :param name: The name of the hook to register too.  I.e. ``pre_setup``,
        ``post_run``, etc.
    :param func:    The function to register to the hook.  This is an
        *un-instantiated*, non-instance method, simple function.
    :param weight:  The weight in which to order the hook function.
    :type weight: ``int``

    Usage:

    .. code-block:: python

        from cement.core import hook

        def my_hook(*args, **kwargs):
            # do something here
            res = 'Something to return'
            return res

        hook.register('post_setup', my_hook)

    """
    # only log debug for now as this won't be removed until Cement 3.x and
    # we don't have access to CementApp.Meta.ignore_deprecation_warnings here
    LOG.debug(
        'Cement Deprecation Warning: `hook.register()` has been deprecated, '
        'and will be removed in future versions of Cement.  You should now '
        'use `CementApp.hook.register()` instead.'
    )
    if name not in backend.__hooks__:
        LOG.debug("hook name '%s' is not defined! ignoring..." % name)
        return False

    LOG.debug("registering hook '%s' from %s into hooks['%s']" %
              (func.__name__, func.__module__, name))

    # Hooks are as follows: (weight, name, func)
    backend.__hooks__[name].append((int(weight), func.__name__, func))


def run(name, *args, **kwargs):
    """
    DEPRECATION WARNING: This function is deprecated as of Cement 2.7.x and
    will be removed in future versions of Cement.
    Use ``CementApp.hook.run()`` instead.

    ---

    Run all defined hooks in the namespace.  Yields the result of each hook
    function run.

    :param name: The name of the hook function.
    :param args: Additional arguments to be passed to the hook functions.
    :param kwargs: Additional keyword arguments to be passed to the hook
        functions.
    :raises: FrameworkError

    Usage:

    .. code-block:: python

        from cement.core import hook

        for result in hook.run('hook_name'):
            # do something with result from each hook function
            ...
    """
    # only log debug for now as this won't be removed until Cement 3.x and
    # we don't have access to CementApp.Meta.ignore_deprecation_warnings here
    LOG.debug(
        'Cement Deprecation Warning: `hook.run()` has been deprecated, '
        'and will be removed in future versions of Cement.  You should now '
        'use `CementApp.hook.run()` instead.'
    )
    if name not in backend.__hooks__:
        raise exc.FrameworkError("Hook name '%s' is not defined!" % name)

    # Will order based on weight (the first item in the tuple)
    backend.__hooks__[name].sort(key=operator.itemgetter(0))
    for hook in backend.__hooks__[name]:
        LOG.debug("running hook '%s' (%s) from %s" %
                  (name, hook[2], hook[2].__module__))
        res = hook[2](*args, **kwargs)

        # Check if result is a nested generator - needed to support e.g.
        # asyncio
        if isinstance(res, types.GeneratorType):
            for _res in res:
                yield _res
        else:
            yield res
