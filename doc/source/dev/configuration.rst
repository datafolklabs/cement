Configuration Handling
======================

Cement defines a configuration interface called
:ref:`IConfig <cement.core.config>`, as well as the default
:ref:`ConfigParserConfigHandler <cement.ext.ext_configparser>` that implements
the interface.  This handler is built on top of `ConfigParser
<http://docs.python.org/library/configparser.html>`_ which is included in the
Python standard library.  Therefor, this class will work much like
ConfigParser but with any added functions necessary to meet the requirements
of the ``IConfig`` interface.

Please note that there are other handlers that implement the ``IConfig``
interface.  The documentation below only references usage based on the
interface and not the full capabilities of the implementation.

The following config handlers are included and maintained with Cement:

    * :ref:`ConfigParserConfigHandler <cement.ext.ext_configparser>` (default)
    * :ref:`ConfigObjConfigHandler <cement.ext.ext_configobj>`
    * :ref:`JsonConfigHandler <cement.ext.ext_json>`
    * :ref:`JsonConfigObjConfigHandler <cement.ext.ext_json_configobj>`
    * :ref:`YamlConfigHandler <cement.ext.ext_yaml>`
    * :ref:`YamlConfigObjHandler <cement.ext.ext_yaml_configobj>`


Please reference the :ref:`IConfig <cement.core.config>` interface
documentation for writing your own config handler.

Configuration Ordering
----------------------

An applications configuration is made up of a number of things, including
default settings, handler defaults, config file settings, etc.  The following
is the order in which configurations are discovered and loaded:

    * Defaults defined in ``CementApp.Meta.config_defaults`` or passed as
      ``config_defaults`` keyword to ``CementApp``
    * Extended by ``CementBaseHandler.Meta.config_defaults`` (not overridden)
    * Overridden by configuration files defined in
      ``CementApp.Meta.config_files`` in the order they are listed/loaded
      (last has precedence)
    * Overridden by command line options that match the same key name (only
      if ``CementApp.Meta.arguments_override_config == True`` or if the
      argument name is listed in ``CementApp.Meta.override_arguments``)


Application Default Settings
----------------------------

Cement does not require default config settings in order to operate.  That
said, these settings are found under the ``app_label`` application section
of the configuration, and overridden by a ``[<app_label>]`` block from a
configuration file.

A default dictionary is used if no other defaults are passed when creating an
application.  For example, the following:

.. code-block:: python

    from cement.core import foundation
    app = foundation.CementApp('myapp')

Is equivalent to:

.. code-block:: python

    from cement.core import foundation
    from cement.utils.misc import init_defaults

    defaults = init_defaults('myapp')
    app = foundation.CementApp('myapp', config_defaults=defaults)


That said, you can override default settings or add your own defaults like
so:

.. code-block:: python

    from cement.core import foundation
    from cement.utils.misc import init_defaults

    defaults = init_defaults('myapp', 'section1','section2')
    defaults['section1']['foo'] = 'bar'
    defaults['section2']['foo2'] = 'bar2'

    app = foundation.CementApp('myapp', config_defaults=defaults)


It is important to note that the default settings, which is a dict, is parsed
by the config handler and loaded into it's own configuration mechanism.
Meaning, though some config handlers (i.e. ``ConfigObjConfigHandler``) might
also be accessible like a dict, not all do (i.e.
``ConfigParserConfigHandler``).  Please see the documentation for the config
handler you use for their full usage when accessing the ``app.config`` object.

Built-in Defaults
-----------------

The following are not required to exist in the config defaults, however if
they do, Cement will honor them (overriding or appending to built-in
defaults).

    debug = ``False``
        Toggles debug output.  By default, this setting is also overridden
        by the ``[<app_label>] -> debug`` config setting parsed in any
        of the application configuration files.

    ignore_deprecation_warnings = ``False``
        Disable deprecation warnings from being logged by Cement.

    extensions = ``None``
        List of additional framework extensions to load.  Any extensions
        defined here will be appended to the application's defined extensions.

    plugin_config_dir = ``None``
        A directory path where plugin config files can be found.  Files
        must end in ``.conf``.  By default, this setting is also overridden
        by the ``[<app_label>] -> plugin_config_dir`` config setting parsed in
        any of the application configuration files.

        If set, this item will be **appended** to
        ``CementApp.Meta.plugin_config_dirs`` so that it's settings will have
        presedence over other config files.

        In general, this setting should not be defined by the developer, as it
        is primarily used to allow the end-user to define a
        ``plugin_config_dir`` without completely trumping the hard-coded list
        of default ``plugin_config_dirs`` defined by the app/developer.

    plugin_dir = ``None``
        A directory path where plugin code (modules) can be loaded from.
        By default, this setting is also overridden by the
        ``[<app_label>] -> plugin_dir`` config setting parsed in any of the
        application configuration files.

        If set, this item will be **prepended** to
        ``CementApp.Meta.plugin_dirs`` so that a user's defined ``plugin_dir``
        has precedence over other ``plugin_dirs``.

        In general, this setting should not be defined by the developer, as it
        is primarily used to allow the end-user to define a
        ``plugin_dir`` without completely trumping the hard-coded list
        of default ``plugin_dirs`` defined by the app/developer.

    template_dir = ``None``
        A directory path where template files can be loaded from.  By default,
        this setting is also overridden by the
        ``[<app_label>] -> template_dir`` config setting parsed in any of the
        application configuration files.

        If set, this item will be appended to
        ``CementApp.Meta.template_dirs``.

        In general, this setting should not be defined by the developer, as it
        is primarily used to allow the end-user to define a ``template_dir``
        without completely trumping the hard-coded list of default
        ``template_dirs`` defined by the app/developer.


Application Configuration Defaults vs Handler Configuration Defaults
--------------------------------------------------------------------

There may be slight confusion between the ``CementApp.Meta.config_defaults``
and the ``CementBaseHandler.Meta.config_defaults`` options.  They both are
very similar, however the application level configuration defaults are
intended to be used to set defaults for multiple sections.  Therefore, the
``CementApp.Meta.config_defaults`` option is a ``dict`` with nested
``dict``'s under it.  Each key of the top level ``dict`` relates to a config
``[section]`` and the nested ``dict`` are the settings for that ``[section]``.

The ``CementBaseHandler.Meta.config_defaults`` only partain to a single
``[section]`` and therefor is only a single level ``dict``, whose settings are
applied to the ``CementBaseHandler.Meta.config_section`` of the application's
configuration.

Accessing Configuration Settings
--------------------------------

After application creation and setup, you can access the config handler via
the ``app.config`` object.  For example:

.. code-block:: python

    from cement.core import foundation
    app = foundation.CementApp('myapp')

    # First setup the application
    app.setup()

    # Get settings
    app.config.get('myapp', 'debug')

    # Set settings
    app.config.set('myapp', 'debug', True)

    # Get sections (configuration [blocks])
    app.config.get_sections()

    # Add a section
    app.config.add_section('my_config_section')

    # Test if a section exists
    app.config.has_section('my_config_section')

    # Get configuration keys for the 'myapp' section
    app.config.keys('myapp')

    # Test if a key exist
    if 'debug' in app.config.keys('myapp')

    # Merge a dict of settings into the config
    other_config = dict()
    other_config['myapp'] = dict()
    other_config['myapp']['foo'] = 'not bar'
    app.config.merge(other_config)


Parsing Config Files
--------------------

Most applications benefit from allowing their users to customize runtime via
a configuration file.  This can be done by:

.. code-block:: python

    from cement.core import foundation
    app = foundation.CementApp('myapp')

    # First setup the application
    app.setup()

    # Parse a configuration file
    app.config.parse_file('/path/to/some/file.conf')

Note that Cement automatically parses any config files listed in the
``CementApp.Meta.config_files`` list.  For example:

.. code-block:: python

    from cement.core import foundation, backend

    app = foundation.CementApp('myapp',
            config_files = [
                '/path/to/config1',
                '/path/to/config2'
                ],
            )


If no ``config_files`` meta is provided, Cement will set the defaults to the
following common and sane defaults:

    * ``/etc/<app_label>/<app_label>.conf``
    * ``~/.<app_label>.conf``
    * ``~/.<app_label>/config``


Overriding Configurations with Command Line Options
---------------------------------------------------

Config settings can **optionally** overridden by a passed command line
option if the option name matches a configuration key.  Note that this will
happen in *all* config sections if enabled:

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.utils.misc import init_defaults

    defaults = init_defaults('myapp')
    defaults['myapp']['foo'] = 'bar'

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            config_defaults = defaults
            arguments_override_config = True

    with MyApp() as app:
        app.args.add_argument('--foo', action='store', dest='foo')
        app.run()



With ``arguments_override_config`` enabled, running the above application and
passing the ``--foo=some_value`` option will override the ``foo`` setting
under a ``[myapp]`` configuration section as well as any other section that
has a matching ``foo`` key.


Configuration Options Versus Meta Options
-----------------------------------------

As you will see extensively throughout the Cement code is the use of Meta
options.  There can be some confusion between the use of Meta options, and
application configuration options.  The following explains the two:

**Configuration Options**

Configuration options are application specific.  There are config defaults
defined by the application developer, that can be (and are intended to be)
overridden by user defined settings in a configuration file.

Cement does not rely on the application configuration, though it can honor
configuration settings.  For example, ``CementApp`` honors the ``debug``
config option which is documented, but it doesn't rely on it existing either.

The key things to note about configuration options are:

    * They give the end user flexibility in how the application operates.
    * Anything that you want users to be able to customize via a config file.
      For example, the path to a log file or the location of a database
      server. These are things that you do not want hard-coded into your
      app, but rather might want sane defaults for.

**Meta Options**

Meta options are used on the backend by developers to alter how classes
operate.  For example, the ``CementApp`` class has a meta option of
``log_handler``.  The default log handler is ``LoggingLogHandler``, however
because this is built on an interface definition, Cement can use any other log
handler the same way without issue as long as that log handler abides by the
interface definition.  Meta options make this change seamless and allows the
handler to alter functionality, rather than having to change code in the top
level class itself.

The key thing to note about Meta options are:

    * They give the developer flexibility in how the code operates.
    * End users should not have access to modify Meta options via a config
      file or similar 'dynamic' configuration (unless those specific options
      are listed in ``CementApp.Meta.core_meta_override`` or
      ``CementApp.Meta.meta_override`` (for example, the ``debug`` setting
      under ``[<app_label>]`` overrides ``CementApp.Meta.debug`` by default.
    * Meta options are used to alter how classes work, however are considered
      'hard-coded' settings.  If the developer chooses to alter a Meta option,
      it is for the life of that release.
    * Meta options should have a sane default, and be clearly documented.
