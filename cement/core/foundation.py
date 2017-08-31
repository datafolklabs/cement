"""Cement core foundation module."""

import os
import sys
import signal
import platform
from time import sleep
from ..core import backend, exc, log, config, plugin
from ..core import output, extension, arg, controller, meta, cache, mail
from ..core.handler import HandlerManager
from ..core.hook import HookManager
from ..utils.misc import is_true, minimal_logger
from ..utils import fs

# The `imp` module is deprecated in favor of `importlib` in 3.4, but it
# wasn't introduced until 3.1.  Finally, reload is a builtin on Python < 3
pyver = sys.version_info
if pyver[0] >= 3 and pyver[1] >= 4:                # pragma: nocover  # noqa
    from importlib import reload as reload_module  # pragma: nocover  # noqa
elif pyver[0] >= 3:                                # pragma: nocover  # noqa
    from imp import reload as reload_module        # pragma: nocover  # noqa
else:                                              # pragma: nocover  # noqa
    reload_module = reload                         # pragma: nocover  # noqa


LOG = minimal_logger(__name__)
if platform.system() == 'Windows':
    SIGNALS = [signal.SIGTERM, signal.SIGINT]   # pragma: nocover
else:
    SIGNALS = [signal.SIGTERM, signal.SIGINT, signal.SIGHUP]


def add_handler_override_options(app):
    """
    This is a ``post_setup`` hook that adds the handler override options to
    the argument parser

    :param app: The application object.

    """
    if app._meta.handler_override_options is None:
        return

    for i in app._meta.handler_override_options:
        if i not in app.handler.list_types():
            LOG.debug("interface '%s'" % i +
                      " is not defined, can not override handlers")
            continue

        if len(app.handler.list(i)) > 1:
            handlers = []
            for h in app.handler.list(i):
                handlers.append(h())

            choices = [x._meta.label
                       for x in handlers
                       if x._meta.overridable is True]

            # don't display the option if no handlers are overridable
            if not len(choices) > 0:
                LOG.debug("no handlers are overridable within the " +
                          "%s interface" % i)
                continue

            # override things that we need to control
            argument_kw = app._meta.handler_override_options[i][1]
            argument_kw['dest'] = '%s_handler_override' % i
            argument_kw['action'] = 'store'
            argument_kw['choices'] = choices

            app.args.add_argument(
                *app._meta.handler_override_options[i][0],
                **app._meta.handler_override_options[i][1]
            )


def handler_override(app):
    """
    This is a ``post_argument_parsing`` hook that overrides a configured
    handler if defined in ``CementApp.Meta.handler_override_options`` and
    the option is passed at command line with a valid handler label.

    :param app: The application object.

    """
    if app._meta.handler_override_options is None:
        return

    for i in app._meta.handler_override_options.keys():
        if not hasattr(app.pargs, '%s_handler_override' % i):
            continue
        elif getattr(app.pargs, '%s_handler_override' % i) is None:
            continue
        else:
            # get the argument value from command line
            argument = getattr(app.pargs, '%s_handler_override' % i)
            setattr(app._meta, '%s_handler' % i, argument)

            # and then re-setup the handler
            getattr(app, '_setup_%s_handler' % i)()


def cement_signal_handler(signum, frame):
    """
    Catch a signal, run the 'signal' hook, and then raise an exception
    allowing the app to handle logic elsewhere.

    :param signum: The signal number
    :param frame: The signal frame.
    :raises: cement.core.exc.CaughtSignal

    """
    LOG.debug('Caught signal %s' % signum)

    # FIXME: Maybe this isn't ideal... purhaps make
    # CementApp.Meta.signal_handler a decorator that take the app object
    # and wraps/returns the actually signal handler?
    for f_global in frame.f_globals.values():
        if isinstance(f_global, CementApp):
            app = f_global
            for res in app.hook.run('signal', app, signum, frame):
                pass  # pragma: nocover
    raise exc.CaughtSignal(signum, frame)


class CementApp(meta.MetaMixin):

    """
    The primary class to build applications from.

    Usage:

    The following is the simplest CementApp:

    .. code-block:: python

        from cement.core.foundation import CementApp

        with CementApp('helloworld') as app:
            app.run()


    Alternatively, the above could be written as:

    .. code-block:: python

        from cement.core.foundation import CementApp

        app = foundation.CementApp('helloworld')
        app.setup()
        app.run()
        app.close()


    A more advanced example looks like:

    .. code-block:: python

        from cement.core.foundation import CementApp
        from cement.core.controller import CementBaseController, expose

        class MyController(CementBaseController):
            class Meta:
                label = 'base'
                arguments = [
                    ( ['-f', '--foo'], dict(help='Notorious foo option') ),
                    ]
                config_defaults = dict(
                    debug=False,
                    some_config_param='some_value',
                    )

            @expose(help='This is the default command', hide=True)
            def default(self):
                print('Hello World')

        class MyApp(CementApp):
            class Meta:
                label = 'helloworld'
                extensions = ['daemon','json',]
                base_controller = MyController

        with MyApp() as app:
            app.run()

    """
    class Meta:

        """
        Application meta-data (can also be passed as keyword arguments to the
        parent class).
        """

        label = None
        """
        The name of the application.  This should be the common name as you
        would see and use at the command line.  For example 'helloworld', or
        'my-awesome-app'.
        """

        debug = False
        """
        Used internally, and should not be used by developers.  This is set
        to `True` if `--debug` is passed at command line."""

        exit_on_close = False
        """
        Whether or not to call ``sys.exit()`` when ``close()`` is called.
        The default is ``False``, however if ``True`` then the app will call
        ``sys.exit(X)`` where ``X`` is ``self.exit_code``.
        """

        config_extension = '.conf'
        """
        Extension used to identify application and plugin configuration files.
        """

        config_files = None
        """
        List of config files to parse.

        Note: Though Meta.config_section defaults to None, Cement will
        set this to a default list based on Meta.label (or in other words,
        the name of the application).  This will equate to:

        .. code-block:: python

            ['/etc/<app_label>/<app_label>.conf',
             '~/.<app_label>.conf',
             '~/.<app_label>/config']


        Files are loaded in order, and have precedence in order.  Therefore,
        the last configuration loaded has precedence (and overwrites settings
        loaded from previous configuration files).

        Note that ``.conf`` is the default config file extension, defined by
        ``CementApp.Meta.config_extension``.
        """

        config_dirs = None
        """
        List of config directories to search config files.

        For each direcory cement will load all files that ends
        with ``.conf``.

        .. code-block:: python

            ['/etc/<app_label>/<app_label>/conf.d',
             '~/.<app_label>/conf.d']

        Directories and files inside are loaded in order, and have precedence
        in order.  Therefore, the last configuration loaded has precedence
        (and overwrites settings loaded from previous configuration files).

        These configuration will be overriden by configuration from
        ``CementApp.Meta.config_files``.

        Note that ``.conf`` is the default config file extension, defined by
        ``CementApp.Meta.config_extension``.
        """

        plugins = []
        """
        A list of plugins to load.  This is generally considered bad
        practice since plugins should be dynamically enabled/disabled
        via a plugin config file.
        """

        plugin_config_dirs = None
        """
        A list of directory paths where plugin config files can be found.
        Files must end in ``.conf`` (or the extension defined by
        ``CementApp.Meta.config_extension``) or they will be ignored.

        Note: Though ``CementApp.Meta.plugin_config_dirs`` is ``None``, Cement
        will set this to a default list based on ``CementApp.Meta.label``.
        This will equate to:

        .. code-block:: python

            ['/etc/<app_label>/plugins.d', '~/.<app_label>/plugin.d']


        Files are loaded in order, and have precedence in that order.
        Therefore, the last configuration loaded has precedence (and
        overwrites settings loaded from previous configuration files).
        """

        plugin_config_dir = None
        """
        A directory path where plugin config files can be found.  Files must
        end in ``.conf`` (or the extension defined by
        ``CementApp.Meta.config_extension``) or they will be ignored.  By
        default, this setting is also overridden by the
        ``[<app_label>] -> plugin_config_dir`` config setting parsed in
        any of the application configuration files.

        If set, this item will be **appended** to
        ``CementApp.Meta.plugin_config_dirs`` so that it's settings will have
        presedence over other configuration files.

        In general, this setting should not be defined by the developer, as it
        is primarily used to allow the end-user to define a
        ``plugin_config_dir`` without completely trumping the hard-coded list
        of default ``plugin_config_dirs`` defined by the app/developer.
        """

        plugin_bootstrap = None
        """
        A python package (dotted import path) where plugin code can be
        loaded from.  This is generally something like ``myapp.plugins``
        where a plugin file would live at ``myapp/plugins/myplugin.py``.
        This provides a facility for applications that have builtin plugins
        that ship with the applications source code and live in the same
        Python module.

        Note: Though the meta default is ``None``, Cement will set this to
        ``<app_label>.plugins`` if not set.
        """

        plugin_dirs = None
        """
        A list of directory paths where plugin code (modules) can be loaded
        from.

        Note: Though ``CementApp.Meta.plugin_dirs`` is None, Cement will set
        this to a default list based on ``CementApp.Meta.label`` if not set.
        This will equate to:

        .. code-block:: python

            ['~/.<app_label>/plugins', '/usr/lib/<app_label>/plugins']


        Modules are attempted to be loaded in order, and will stop loading
        once a plugin is successfully loaded from a directory.  Therefore
        this is the oposite of configuration file loading, in that here the
        first has precedence.
        """

        plugin_dir = None
        """
        A directory path where plugin code (modules) can be loaded from.
        By default, this setting is also overridden by the
        ``[<app_label>] -> plugin_dir`` config setting parsed in any of the
        application configuration files.

        If set, this item will be **prepended** to ``Meta.plugin_dirs`` so
        that a users defined ``plugin_dir`` has precedence over others.

        In general, this setting should not be defined by the developer, as it
        is primarily used to allow the end-user to define a
        ``plugin_dir`` without completely trumping the hard-coded list
        of default ``plugin_dirs`` defined by the app/developer.
        """

        argv = None
        """
        A list of arguments to use for parsing command line arguments
        and options.

        Note: Though Meta.argv defaults to None, Cement will set this to
        ``list(sys.argv[1:])`` if no argv is set in Meta during setup().
        """

        arguments_override_config = False
        """
        A boolean to toggle whether command line arguments should
        override configuration values if the argument name matches the
        config key.  I.e. --foo=bar would override config['myapp']['foo'].

        This is different from ``override_arguments`` in that if
        ``arguments_override_config`` is ``True``, then all arguments will
        override (you don't have to list them all).
        """

        override_arguments = ['debug']
        """
        List of arguments that override their configuration counter-part.
        For example, if ``--debug`` is passed (and it's config value is
        ``debug``) then the ``debug`` key of all configuration sections will
        be overridden by the value of the command line option (``True`` in
        this example).

        This is different from ``arguments_override_config`` in that this is
        a selective list of specific arguments to override the config with
        (and not all arguments that match the config).  This list will take
        affect whether ``arguments_override_config`` is ``True`` or ``False``.
        """

        core_handler_override_options = dict(
            output=(['-o'], dict(help='output handler')),
        )
        """
        Similar to ``CementApp.Meta.handler_override_options`` but these are
        the core defaults required by Cement.  This dictionary can be
        overridden by ``CementApp.Meta.handler_override_options`` (when they
        are merged together).
        """

        handler_override_options = {}
        """
        Dictionary of handler override options that will be added to the
        argument parser, and allow the end-user to override handlers.  Useful
        for interfaces that have multiple uses within the same application
        (for example: Output Handler (json, yaml, etc) or maybe a Cloud
        Provider Handler (rackspace, digitalocean, amazon, etc).

        This dictionary will merge with
        ``CementApp.Meta.core_handler_override_options`` but this one has
        precedence.

        Dictionary Format:

        .. code-block:: text

            <interface_name> = (option_arguments, help_text)


        See ``CementApp.Meta.core_handler_override_options`` for an example
        of what this should look like.

        Note, if set to ``None`` then no options will be defined, and the
        ``CementApp.Meta.core_meta_override_options`` will be ignore (not
        recommended as some extensions rely on this feature).
        """

        config_section = None
        """
        The base configuration section for the application.

        Note: Though Meta.config_section defaults to None, Cement will
        set this to the value of Meta.label (or in other words, the name
        of the application).
        """

        config_defaults = None
        """Default configuration dictionary.  Must be of type 'dict'."""

        meta_defaults = {}
        """
        Default metadata dictionary used to pass high level options from the
        application down to handlers at the point they are registered by the
        framework **if the handler has not already been instantiated**.

        For example, if requiring the ``json`` extension, you might want to
        override ``JsonOutputHandler.Meta.json_module`` with ``ujson`` by
        doing the following

        .. code-block:: python

            from cement.core.foundation import CementApp
            from cement.utils.misc import init_defaults

            META = init_defaults('output.json')
            META['output.json']['json_module'] = 'ujson'

            class MyApp(CementApp):
                class Meta:
                    label = 'myapp'
                    extensions = ['json']
                    meta_defaults = META

        """

        catch_signals = SIGNALS
        """
        List of signals to catch, and raise exc.CaughtSignal for.
        Can be set to None to disable signal handling.
        """

        signal_handler = cement_signal_handler
        """A function that is called to handle any caught signals."""

        config_handler = 'configparser'
        """
        A handler class that implements the IConfig interface.
        """

        mail_handler = 'dummy'
        """
        A handler class that implements the IMail interface.
        """

        extension_handler = 'cement'
        """
        A handler class that implements the IExtension interface.
        """

        log_handler = 'logging'
        """
        A handler class that implements the ILog interface.
        """

        plugin_handler = 'cement'
        """
        A handler class that implements the IPlugin interface.
        """

        argument_handler = 'argparse'
        """
        A handler class that implements the IArgument interface.
        """

        output_handler = 'dummy'
        """
        A handler class that implements the IOutput interface.
        """

        cache_handler = None
        """
        A handler class that implements the ICache interface.
        """

        base_controller = None
        """
        This is the base application controller.  If a controller is set,
        runtime operations are passed to the controller for command
        dispatch and argument parsing when CementApp.run() is called.

        Note that cement will automatically set the `base_controller` to a
        registered controller whose label is 'base' (only if `base_controller`
        is not currently set).
        """

        extensions = []
        """List of additional framework extensions to load."""

        bootstrap = None
        """
        A bootstrapping module to load after app creation, and before
        app.setup() is called.  This is useful for larger applications
        that need to offload their bootstrapping code such as registering
        hooks/handlers/etc to another file.

        This must be a dotted python module path.
        I.e. 'myapp.bootstrap' (myapp/bootstrap.py).  Cement will then
        import the module, and if the module has a 'load()' function, that
        will also be called.  Essentially, this is the same as an
        extension or plugin, but as a facility for the application itself
        to bootstrap 'hardcoded' application code.  It is also called
        before plugins are loaded.
        """

        core_extensions = [
            'cement.ext.ext_dummy',
            'cement.ext.ext_smtp',
            'cement.ext.ext_plugin',
            'cement.ext.ext_configparser',
            'cement.ext.ext_logging',
            'cement.ext.ext_argparse',
        ]
        """
        List of Cement core extensions.  These are generally required by
        Cement and should only be modified if you know what you're
        doing.  Use 'extensions' to add to this list, rather than
        overriding core extensions.  That said if you want to prune down
        your application, you can remove core extensions if they are
        not necessary (for example if using your own log handler
        extension you likely don't want/need LoggingLogHandler to be
        registered).
        """

        core_meta_override = [
            'debug',
            'plugin_config_dir',
            'plugin_dir',
            'ignore_deprecation_warnings',
            'template_dir',
            'mail_handler',
            'cache_handler',
            'log_handler',
            'output_handler',
        ]
        """
        List of meta options that can/will be overridden by config options
        of the '[base]' config section (where [base] is the base
        configuration section of the application which is determined by
        Meta.config_section but defaults to Meta.label). These overrides
        are required by the framework to function properly and should not
        be used by end user (developers) unless you really know what
        you're doing.  To add your own extended meta overrides please use
        'meta_override'.
        """

        meta_override = []
        """
        List of meta options that can/will be overridden by config options
        of the '[base]' config section (where [base] is the
        base configuration section of the application which is determined
        by Meta.config_section but defaults to Meta.label).
        """

        ignore_deprecation_warnings = False
        """Disable deprecation warnings from being logged by Cement."""

        template_module = None
        """
        A python package (dotted import path) where template files can be
        loaded from.  This is generally something like ``myapp.templates``
        where a plugin file would live at ``myapp/templates/mytemplate.txt``.
        Templates are first loaded from ``CementApp.Meta.template_dirs``, and
        and secondly from ``CementApp.Meta.template_module``.  The
        ``template_dirs`` setting has presedence.
        """

        template_dirs = None
        """
        A list of directory paths where template files can be loaded
        from.

        Note: Though ``CementApp.Meta.template_dirs`` defaults to ``None``,
        Cement will set this to a default list based on
        ``CementApp.Meta.label``.  This will equate to:

        .. code-block:: python

            ['~/.<app_label>/templates', '/usr/lib/<app_label>/templates']


        Templates are attempted to be loaded in order, and will stop loading
        once a template is successfully loaded from a directory.
        """

        template_dir = None
        """
        A directory path where template files can be loaded from.  By default,
        this setting is also overridden by the
        ``[<app_label>] -> template_dir`` config setting parsed in any of the
        application configuration files .

        If set, this item will be **prepended** to
        ``CementApp.Meta.template_dirs`` (giving it precedence over other
        ``template_dirs``.
        """

        framework_logging = True
        """
        Whether or not to enable Cement framework logging.  This is separate
        from the application log, and is generally used for debugging issues
        with the framework and/or extensions primarily in development.

        This option is overridden by the environment variable
        `CEMENT_FRAMEWORK_LOGGING`.  Therefore, if in production you do not
        want the Cement framework log enabled, you can set this option to
        ``False`` but override it in your environment by doing something like
        ``export CEMENT_FRAMEWORK_LOGGING=1`` in your shell whenever you need
        it enabled.
        """

        define_hooks = []
        """
        List of hook definitions (label).  Will be passed to
        ``self.hook.define(<hook_label>)``.  Must be a list of strings.

        I.e. ``['my_custom_hook', 'some_other_hook']``
        """

        hooks = []
        """
        List of hooks to register when the app is created.  Will be passed to
        ``self.hook.register(<hook_label>, <hook_func>)``.  Must be a list of
        tuples in the form of ``(<hook_label>, <hook_func>)``.

        I.e. ``[('post_argument_parsing', my_hook_func)]``.
        """

        define_handlers = []
        """
        List of interfaces classes to define handlers.  Must be a list of
        uninstantiated interface classes.

        I.e. ``['MyCustomInterface', 'SomeOtherInterface']``
        """

        handlers = []
        """
        List of handler classes to register.  Will be passed to
        ``handler.register(<handler_class>)``.  Must be a list of
        uninstantiated handler classes.

        I.e. ``[MyCustomHandler, SomeOtherHandler]``
        """

        use_backend_globals = True
        """
        This is a backward compatibility feature.  Cement 2.x.x
        relies on several global variables hidden in ``cement.core.backend``
        used for things like storing hooks and handlers.  Future versions of
        Cement will no longer use this mechanism, however in order to maintain
        backward compatibility this is still the default.  By disabling this
        feature allows multiple instances of CementApp to be created
        from within the same runtime space without clobbering eachothers
        hooks/handers/etc.

        Be warned that use of third-party extensions might break as they were
        built using backend globals, and probably have no idea this feature
        has changed or exists.
        """

        alternative_module_mapping = {}
        """
        EXPERIMENTAL FEATURE: This is an experimental feature added in Cement
        2.9.x and may or may not be removed in future versions of Cement.

        Dictionary of alternative, **drop-in** replacement modules to use
        selectively throughout the application, framework, or
        extensions.  Developers can optionally use the
        ``CementApp.__import__()`` method to import simple modules, and if
        that module exists in this mapping it will import the alternative
        library in it's place.

        This is a low-level feature, and may not produce the results you are
        expecting.  It's purpose is to allow the developer to replace specific
        modules at a high level.  Example: For an application wanting to use
        ``ujson`` in place of ``json``, the developer could set the following:

        .. code-block:: python

            alternative_module_mapping = {
                'json' : 'ujson',
            }

        In the app, you would then load ``json`` as:

        .. code-block:: python

            _json = app.__import__('json')
            _json.dumps(data)


        Obviously, the replacement module **must be** a drop-in replace and
        function the same.
        """

    def __init__(self, label=None, **kw):
        super(CementApp, self).__init__(**kw)

        # disable framework logging?
        if 'CEMENT_FRAMEWORK_LOGGING' not in os.environ.keys():
            if self._meta.framework_logging is True:
                os.environ['CEMENT_FRAMEWORK_LOGGING'] = '1'
            else:
                os.environ['CEMENT_FRAMEWORK_LOGGING'] = '0'

        # for convenience we translate this to _meta
        if label:
            self._meta.label = label
        self._validate_label()
        self._loaded_bootstrap = None
        self._parsed_args = None
        self._last_rendered = None
        self._extended_members = []
        self.__saved_stdout__ = None
        self.__saved_stderr__ = None
        self.__retry_hooks__ = []
        self.handler = None
        self.hook = None

        self.exit_code = 0

        self.ext = None
        self.config = None
        self.log = None
        self.plugin = None
        self.args = None
        self.output = None
        self.controller = None
        self.cache = None
        self.mail = None

        # setup argv... this has to happen before lay_cement()
        if self._meta.argv is None:
            self._meta.argv = list(sys.argv[1:])

        # hack for command line --debug
        if '--debug' in self.argv:
            self._meta.debug = True

        # setup the cement framework
        self._lay_cement()

    @property
    def debug(self):
        """
        Returns boolean based on whether ``--debug`` was passed at command
        line or set via the application's configuration file.

        :returns: boolean
        """
        return self._meta.debug

    @property
    def argv(self):
        """The arguments list that will be used when self.run() is called."""
        return self._meta.argv

    def extend(self, member_name, member_object):
        """
        Extend the CementApp() object with additional functions/classes such
        as 'app.my_custom_function()', etc.  It provides an interface for
        extensions to provide functionality that travel along with the
        application object.

        :param member_name: The name to attach the object to.
        :type member_name: ``str``
        :param member_object: The function or class object to attach to
            CementApp().
        :raises: cement.core.exc.FrameworkError

        """
        if hasattr(self, member_name):
            raise exc.FrameworkError("App member '%s' already exists!" %
                                     member_name)
        LOG.debug("extending appication with '.%s' (%s)" %
                  (member_name, member_object))
        setattr(self, member_name, member_object)
        if member_name not in self._extended_members:
            self._extended_members.append(member_name)

    def _validate_label(self):
        if not self._meta.label:
            raise exc.FrameworkError("Application name missing.")

        # validate the name is ok
        ok = ['_', '-']
        for char in self._meta.label:
            if char in ok:
                continue

            if not char.isalnum():
                raise exc.FrameworkError(
                    "App label can only contain alpha-numeric, dashes, " +
                    "or underscores."
                )

    def setup(self):
        """
        This function wraps all '_setup' actons in one call.  It is called
        before self.run(), allowing the application to be _setup but not
        executed (possibly letting the developer perform other actions
        before full execution.).

        All handlers should be instantiated and callable after setup is
        complete.

        """
        LOG.debug("now setting up the '%s' application" % self._meta.label)

        if self._meta.bootstrap is not None:
            LOG.debug("importing bootstrap code from %s" %
                      self._meta.bootstrap)

            if self._meta.bootstrap not in sys.modules \
                    or self._loaded_bootstrap is None:
                __import__(self._meta.bootstrap, globals(), locals(), [], 0)
                if hasattr(sys.modules[self._meta.bootstrap], 'load'):
                    sys.modules[self._meta.bootstrap].load(self)

                self._loaded_bootstrap = sys.modules[self._meta.bootstrap]
            else:
                reload_module(self._loaded_bootstrap)

        for res in self.hook.run('pre_setup', self):
            pass

        self._setup_extension_handler()
        self._setup_signals()
        self._setup_config_handler()
        self._setup_mail_handler()
        self._setup_cache_handler()
        self._setup_log_handler()
        self._setup_plugin_handler()
        self._setup_arg_handler()
        self._setup_output_handler()
        self._setup_controllers()

        for hook_spec in self.__retry_hooks__:
            self.hook.register(*hook_spec)

        for res in self.hook.run('post_setup', self):
            pass

    def run(self):
        """
        This function wraps everything together (after self._setup() is
        called) to run the application.

        :returns: Returns the result of the executed controller function if
          a base controller is set and a controller function is called,
          otherwise ``None`` if no controller dispatched or no controller
          function was called.

        """
        return_val = None

        LOG.debug('running pre_run hook')
        for res in self.hook.run('pre_run', self):
            pass

        # If controller exists, then dispatch it
        if self.controller:
            return_val = self.controller._dispatch()
        else:
            self._parse_args()

        LOG.debug('running post_run hook')
        for res in self.hook.run('post_run', self):
            pass

        return return_val

    def run_forever(self, interval=1, tb=True):
        """
        This function wraps ``run()`` with an endless while loop.  If any
        exception is encountered it will be logged and then the application
        will be reloaded.

        :param interval: The number of seconds to sleep before reloading the
            the appliction.
        :param tb: Whether or not to print traceback if exception occurs.
        :returns: It should never return.
        """

        if tb is True:
            import traceback

        while True:
            LOG.debug('inside run_forever() eternal loop')
            try:
                self.run()
            except Exception as e:
                self.log.fatal('Caught Exception: %s' % e)

                if tb is True:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    traceback.print_exception(
                        exc_type, exc_value, exc_traceback, limit=2,
                        file=sys.stdout
                    )
            sleep(interval)
            self.reload()

    def reload(self):
        """
        This function is useful for reloading a running applications, for
        example to reload configuration settings, etc.

        :returns: ``None``
        """
        LOG.debug('reloading the %s application' % self._meta.label)
        self._unlay_cement()
        self._lay_cement()
        self.setup()

    def _unlay_cement(self):
        for member in self._extended_members:
            delattr(self, member)
        self._extended_members = []
        self.handler.__handlers__ = {}
        self.hook.__hooks__ = {}

    def close(self, code=None):
        """
        Close the application.  This runs the ``pre_close`` and ``post_close``
        hooks allowing plugins/extensions/etc to cleanup at the end of
        program execution.

        :param code: An exit code to exit with (``int``), if ``None`` is
          passed then exit with whatever ``self.exit_code`` is currently set
          to.  Note: ``sys.exit()`` will only be called if
          ``CementApp.Meta.exit_on_close==True``.
        """
        for res in self.hook.run('pre_close', self):
            pass

        LOG.debug("closing the %s application" % self._meta.label)

        # in theory, this should happen last-last... but at that point `self`
        # would be kind of busted after _unlay_cement() is run.
        for res in self.hook.run('post_close', self):
            pass

        self._unlay_cement()

        if code is not None:
            assert type(code) == int, \
                "Invalid exit status code (must be integer)"
            self.exit_code = code

        if self._meta.exit_on_close is True:
            sys.exit(self.exit_code)

    def render(self, data, template=None, out=sys.stdout, **kw):
        """
        This is a simple wrapper around self.output.render() which simply
        returns an empty string if no self.output handler is defined.

        :param data: The data dictionary to render.
        :param template: The template to render to.  Default: None (some
            output handlers do not use templates).
        :param out: A file like object (sys.stdout, or actual file).  Set to
         ``None`` is no output is desired (just render and return).
         Default: sys.stdout

        """
        for res in self.hook.run('pre_render', self, data):
            if not type(res) is dict:
                LOG.debug("pre_render hook did not return a dict().")
            else:
                data = res

        kw['template'] = template

        if self.output is None:
            LOG.debug('render() called, but no output handler defined.')
            out_text = ''
        else:
            out_text = self.output.render(data, **kw)

        for res in self.hook.run('post_render', self, out_text):
            if not type(res) is str:
                LOG.debug('post_render hook did not return a str()')
            else:
                out_text = str(res)

        if out is not None and not hasattr(out, 'write'):
            raise TypeError("Argument 'out' must be a 'file' like object")
        elif out is not None and out_text is None:
            LOG.debug('render() called but output text is None')
        elif out:
            out.write(out_text)

        self._last_rendered = (data, out_text)
        return out_text

    def get_last_rendered(self):
        """
        DEPRECATION WARNING: This function is deprecated as of Cement 2.1.3
        in favor of the `self.last_rendered` property, and will be removed in
        future versions of Cement.

        Return the (data, output_text) tuple of the last time self.render()
        was called.

        :returns: tuple (data, output_text)

        """
        if not is_true(self._meta.ignore_deprecation_warnings):
            self.log.warning("Cement Deprecation Warning: " +
                             "CementApp.get_last_rendered() has been " +
                             "deprecated, and will be removed in future " +
                             "versions of Cement.  You should use the " +
                             "CementApp.last_rendered property instead.")
        return self._last_rendered

    @property
    def last_rendered(self):
        """
        Return the (data, output_text) tuple of the last time self.render() was
        called.

        :returns: tuple (data, output_text)

        """
        return self._last_rendered

    @property
    def pargs(self):
        """
        Returns the `parsed_args` object as returned by self.args.parse().
        """
        return self._parsed_args

    def add_arg(self, *args, **kw):
        """A shortcut for self.args.add_argument."""
        self.args.add_argument(*args, **kw)

    def _suppress_output(self):
        if self._meta.debug is True:
            LOG.debug('not suppressing console output because of debug mode')
            return

        LOG.debug('suppressing all console output')
        self.__saved_stdout__ = sys.stdout
        self.__saved_stderr__ = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def _unsuppress_output(self):
        LOG.debug('unsuppressing all console output')
        sys.stdout = self.__saved_stdout__
        sys.stderr = self.__saved_stderr__

    def _lay_cement(self):
        """Initialize the framework."""
        LOG.debug("laying cement for the '%s' application" %
                  self._meta.label)

        if '--debug' in self._meta.argv:
            self._meta.debug = True
        elif '--quiet' in self._meta.argv:
            self._suppress_output()

        # Forward/Backward compat, see Issue #311
        if self._meta.use_backend_globals is True:
            backend.__hooks__ = {}
            backend.__handlers__ = {}
            self.handler = HandlerManager(use_backend_globals=True)
            self.hook = HookManager(use_backend_globals=True)
        else:
            self.handler = HandlerManager(use_backend_globals=False)
            self.hook = HookManager(use_backend_globals=False)

        # define framework hooks
        self.hook.define('pre_setup')
        self.hook.define('post_setup')
        self.hook.define('pre_run')
        self.hook.define('post_run')
        self.hook.define('pre_argument_parsing')
        self.hook.define('post_argument_parsing')
        self.hook.define('pre_close')
        self.hook.define('post_close')
        self.hook.define('signal')
        self.hook.define('pre_render')
        self.hook.define('post_render')

        # define application hooks from meta
        for label in self._meta.define_hooks:
            self.hook.define(label)

        # register some built-in framework hooks
        self.hook.register('post_setup', add_handler_override_options,
                           weight=-99)
        self.hook.register('post_argument_parsing',
                           handler_override, weight=-99)

        # register application hooks from meta.  the hooks listed in
        # CementApp.Meta.hooks are registered here, so obviously can not be
        # for any hooks other than the builtin framework hooks that we just
        # defined here (above).  Anything that we couldn't register here
        # will be retried after setup
        self.__retry_hooks__ = []
        for hook_spec in self._meta.hooks:
            if not self.hook.defined(hook_spec[0]):
                LOG.debug('hook %s not defined, will retry after setup' %
                          hook_spec[0])
                self.__retry_hooks__.append(hook_spec)
            else:
                self.hook.register(*hook_spec)

        # define and register handlers
        self.handler.define(extension.IExtension)
        self.handler.define(log.ILog)
        self.handler.define(config.IConfig)
        self.handler.define(mail.IMail)
        self.handler.define(plugin.IPlugin)
        self.handler.define(output.IOutput)
        self.handler.define(arg.IArgument)
        self.handler.define(controller.IController)
        self.handler.define(cache.ICache)

        # define application handlers
        for interface_class in self._meta.define_handlers:
            self.handler.define(interface_class)

        # extension handler is the only thing that can't be loaded... as,
        # well, an extension.  ;)
        self.handler.register(extension.CementExtensionHandler)

        # register application handlers
        for handler_class in self._meta.handlers:
            self.handler.register(handler_class)

    def _parse_args(self):
        for res in self.hook.run('pre_argument_parsing', self):
            pass

        self._parsed_args = self.args.parse(self.argv)

        if self._meta.arguments_override_config is True:
            for member in dir(self._parsed_args):
                if member and member.startswith('_'):
                    continue

                # don't override config values for options that weren't passed
                # or in otherwords are None
                elif getattr(self._parsed_args, member) is None:
                    continue

                for section in self.config.get_sections():
                    if member in self.config.keys(section):
                        self.config.set(section, member,
                                        getattr(self._parsed_args, member))

        for member in self._meta.override_arguments:
            for section in self.config.get_sections():
                if member in self.config.keys(section):
                    self.config.set(section, member,
                                    getattr(self._parsed_args, member))

        for res in self.hook.run('post_argument_parsing', self):
            pass

    def catch_signal(self, signum):
        """
        Add ``signum`` to the list of signals to catch and handle by Cement.

        :param signum: The signal number to catch.  See Python ``signal``
          library.
        """

        LOG.debug("adding signal handler %s for signal %s" % (
            self._meta.signal_handler, signum)
        )
        signal.signal(signum, self._meta.signal_handler)

    def _setup_signals(self):
        if self._meta.catch_signals is None:
            LOG.debug("catch_signals=None... not handling any signals")
            return

        for signum in self._meta.catch_signals:
            self.catch_signal(signum)

    def _resolve_handler(self, handler_type, handler_def, raise_error=True):
        meta_defaults = {}
        if type(handler_def) == str:
            _meta_label = "%s.%s" % (handler_type, handler_def)
            meta_defaults = self._meta.meta_defaults.get(_meta_label, {})
        elif hasattr(handler_def, 'Meta'):
            _meta_label = "%s.%s" % (handler_type, handler_def.Meta.label)
            meta_defaults = self._meta.meta_defaults.get(_meta_label, {})

        han = self.handler.resolve(handler_type, handler_def,
                                   raise_error=raise_error,
                                   meta_defaults=meta_defaults)
        if han is not None:
            han._setup(self)
            return han

    def _setup_extension_handler(self):
        LOG.debug("setting up %s.extension handler" % self._meta.label)
        self.ext = self._resolve_handler('extension',
                                         self._meta.extension_handler)
        self.ext.load_extensions(self._meta.core_extensions)
        self.ext.load_extensions(self._meta.extensions)

    def _setup_config_handler(self):
        LOG.debug("setting up %s.config handler" % self._meta.label)
        self.config = self._resolve_handler('config',
                                            self._meta.config_handler)
        if self._meta.config_section is None:
            self._meta.config_section = self._meta.label
        self.config.add_section(self._meta.config_section)

        if self._meta.config_defaults is not None:
            self.config.merge(self._meta.config_defaults)

        ext = self._meta.config_extension
        label = self._meta.label

        if self._meta.config_files is None:
            self._meta.config_files = [
                os.path.join('/', 'etc', label, '%s%s' % (label, ext)),
                os.path.join(fs.HOME_DIR, '.%s%s' % (label, ext)),
                os.path.join(fs.HOME_DIR, '.%s' % label, 'config'),
            ]

        if self._meta.config_dirs is None:
            self._meta.config_dirs = [
                os.path.join('/', 'etc', label, 'conf.d'),
                os.path.join(fs.HOME_DIR, '.%s' % label, 'conf.d'),
            ]

        for _dir in self._meta.config_dirs:
            if not os.path.isdir(_dir):
                continue
            for f in os.listdir(_dir):
                if f.endswith(ext):
                    self.config.parse_file(os.path.join(_dir, f))

        for _file in self._meta.config_files:
            self.config.parse_file(_file)

        self.validate_config()

        # hack for --debug
        if '--debug' in self.argv or self._meta.debug is True:
            self.config.set(self._meta.config_section, 'debug', True)

        # override select Meta via config
        base_dict = self.config.get_section_dict(self._meta.config_section)

        for key in base_dict:
            if key in self._meta.core_meta_override or \
                    key in self._meta.meta_override:
                # kind of a hack for core_meta_override
                if key in ['debug']:
                    setattr(self._meta, key, is_true(base_dict[key]))
                else:
                    setattr(self._meta, key, base_dict[key])

        # load extensions from configuraton file
        if 'extensions' in self.config.keys(self._meta.config_section):
            exts = self.config.get(self._meta.label, 'extensions')

            # convert a comma-separated string to a list
            if type(exts) is str:
                ext_list = exts.split(',')

                # clean up extra space if they had it inbetween commas
                ext_list = [x.strip() for x in ext_list]

                # set the new extensions value in the config
                self.config.set(self._meta.label, 'extensions', ext_list)

            # otherwise, if it's a list (ConfigObj?)
            elif type(exts) is list:
                ext_list = exts

            for ext in ext_list:
                # load the extension
                self.ext.load_extension(ext)

                # add to meta data
                self._meta.extensions.append(ext)

    def _setup_mail_handler(self):
        LOG.debug("setting up %s.mail handler" % self._meta.label)
        self.mail = self._resolve_handler('mail',
                                          self._meta.mail_handler)

    def _setup_log_handler(self):
        LOG.debug("setting up %s.log handler" % self._meta.label)
        self.log = self._resolve_handler('log', self._meta.log_handler)

    def _setup_plugin_handler(self):
        LOG.debug("setting up %s.plugin handler" % self._meta.label)
        label = self._meta.label

        # plugin config dirs
        if self._meta.plugin_config_dirs is None:
            self._meta.plugin_config_dirs = [
                '/etc/%s/plugins.d/' % self._meta.label,
                os.path.join(fs.HOME_DIR, '.%s' % label, 'plugins.d'),
            ]
        config_dir = self._meta.plugin_config_dir
        if config_dir is not None:
            if config_dir not in self._meta.plugin_config_dirs:
                # append so that this config has precedence
                self._meta.plugin_config_dirs.append(config_dir)

        # plugin dirs
        if self._meta.plugin_dirs is None:
            self._meta.plugin_dirs = [
                os.path.join(fs.HOME_DIR, '.%s' % label, 'plugins'),
                '/usr/lib/%s/plugins' % self._meta.label,
            ]
        plugin_dir = self._meta.plugin_dir
        if plugin_dir is not None:
            if plugin_dir not in self._meta.plugin_dirs:
                # insert so that this dir has precedence
                self._meta.plugin_dirs.insert(0, plugin_dir)

        # plugin bootstrap
        if self._meta.plugin_bootstrap is None:
            self._meta.plugin_bootstrap = '%s.plugins' % self._meta.label

        self.plugin = self._resolve_handler('plugin',
                                            self._meta.plugin_handler)
        self.plugin.load_plugins(self._meta.plugins)
        self.plugin.load_plugins(self.plugin.get_enabled_plugins())

    def _setup_output_handler(self):
        if self._meta.output_handler is None:
            LOG.debug("no output handler defined, skipping.")
            return

        label = self._meta.label
        LOG.debug("setting up %s.output handler" % self._meta.label)
        self.output = self._resolve_handler('output',
                                            self._meta.output_handler,
                                            raise_error=False)
        # template module
        if self._meta.template_module is None:
            self._meta.template_module = '%s.templates' % label

        # template dirs
        if self._meta.template_dirs is None:
            self._meta.template_dirs = []
            paths = [
                os.path.join(fs.HOME_DIR, '.%s' % label, 'templates'),
                '/usr/lib/%s/templates' % label,
            ]
            for path in paths:
                self.add_template_dir(path)

        template_dir = self._meta.template_dir
        if template_dir is not None:
            if template_dir not in self._meta.template_dirs:
                # insert so that this dir has precedence
                self._meta.template_dirs.insert(0, template_dir)

    def _setup_cache_handler(self):
        if self._meta.cache_handler is None:
            LOG.debug("no cache handler defined, skipping.")
            return

        LOG.debug("setting up %s.cache handler" % self._meta.label)
        self.cache = self._resolve_handler('cache',
                                           self._meta.cache_handler,
                                           raise_error=False)

    def _setup_arg_handler(self):
        LOG.debug("setting up %s.arg handler" % self._meta.label)
        self.args = self._resolve_handler('argument',
                                          self._meta.argument_handler)
        self.args.prog = self._meta.label

        self.args.add_argument('--debug', dest='debug',
                               action='store_true',
                               help='toggle debug output')
        self.args.add_argument('--quiet', dest='suppress_output',
                               action='store_true',
                               help='suppress all output')

        # merge handler override meta data
        if self._meta.handler_override_options is not None:
            # fucking long names... fuck.  anyway, merge the core handler
            # override options with developer defined options
            core = self._meta.core_handler_override_options.copy()
            dev = self._meta.handler_override_options.copy()
            core.update(dev)

            self._meta.handler_override_options = core

    def _setup_controllers(self):
        LOG.debug("setting up application controllers")

        if self._meta.base_controller is not None:
            cntr = self._resolve_handler('controller',
                                         self._meta.base_controller)
            self.controller = cntr
            self._meta.base_controller = self.controller
        elif self._meta.base_controller is None:
            if self.handler.registered('controller', 'base'):
                self.controller = self._resolve_handler('controller', 'base')
                self._meta.base_controller = self.controller

        # This is necessary for some backend usage
        if self._meta.base_controller is not None:
            if self._meta.base_controller._meta.label != 'base':
                raise exc.FrameworkError("Base controllers must have " +
                                         "a label of 'base'.")

    def validate_config(self):
        """
        Validate application config settings.

        Usage:

        .. code-block:: python

            import os
            from cement.core import foundation

            class MyApp(foundation.CementApp):
                class Meta:
                    label = 'myapp'

                def validate_config(self):
                    super(MyApp, self).validate_config()

                    # test that the log file directory exist, if not create it
                    logdir = os.path.dirname(self.config.get('log', 'file'))

                    if not os.path.exists(logdir):
                        os.makedirs(logdir)

        """
        pass

    def add_template_dir(self, path):
        """
        Append a directory path to the list of template directories to parse
        for templates.

        :param path: Directory path that contains template files.

        Usage:

        .. code-block:: python

            app.add_template_dir('/path/to/my/templates')

        """
        path = fs.abspath(path)
        if path not in self._meta.template_dirs:
            self._meta.template_dirs.append(path)

    def remove_template_dir(self, path):
        """
        Remove a directory path from the list of template directories to parse
        for templates.

        :param path: Directory path that contains template files.

        Usage:

        .. code-block:: python

            app.remove_template_dir('/path/to/my/templates')

        """
        path = fs.abspath(path)
        if path in self._meta.template_dirs:
            self._meta.template_dirs.remove(path)

    def __import__(self, obj, from_module=None):
        # EXPERIMENTAL == UNDOCUMENTED
        mapping = self._meta.alternative_module_mapping

        if from_module is not None:
            _from = mapping.get(from_module, from_module)
            _loaded = __import__(_from, globals(), locals(), [obj], 0)
            return getattr(_loaded, obj)
        else:
            obj = mapping.get(obj, obj)
            _loaded = __import__(obj, globals(), locals(), [], 0)

        return _loaded

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # only close the app if there are no unhandled exceptions
        if exc_type is None:
            self.close()
