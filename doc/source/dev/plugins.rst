.. _application_plugins:

Application Plugins
===================

Cement defines a plugin interface called :ref:`IPlugin <cement.core.plugin>`,
as well as the default :ref:`CementPluginHandler <cement.ext.ext_plugin>`
that implements the interface.

Please note that there may be other handlers that implement the ``IPlugin``
interface.  The documentation below only references usage based on the
interface and not the full capabilities of the implementation.

The following plugin handlers are included and maintained with Cement:

    * :ref:`CementPluginHandler <cement.ext.ext_plugin>`

Please reference the :ref:`IPlugin <cement.core.plugin>` interface
documentation for writing your own plugin handler.

Plugin Configuration Settings
-----------------------------

There are a few settings related to how plugins are loaded under an
applications meta options.  These are:

plugins = ``[]``
    A list of plugins to load.  This is generally considered bad
    practice since plugins should be dynamically enabled/disabled
    via a plugin config file.


plugin_config_dirs = ``None``
    A list of directory paths where plugin config files can be found.
    Files must end in ``.conf`` (or the extension defined by
    ``CementApp.Meta.config_extension``), or they will be ignored.

    Note: Though ``CementApp.Meta.plugin_config_dirs`` is ``None``, Cement
    will set this to a default list based on ``CementApp.Meta.label``.  This
    will equate to:

    .. code-block:: python

        ['/etc/<app_label>/plugins.d', '~/.<app_label>/plugin.d']


    Files are loaded in order, and have precedence in that order.  Therefore,
    the last configuration loaded has precedence (and overwrites settings
    loaded from previous configuration files).

plugin_config_dir = ``None``
    A directory path where plugin config files can be found.  Files must end 
    in ``.conf`` (or the extension defined by
    ``CementApp.Meta.config_extension``), or they will be ignored.  By 
    default, this setting is also overridden by the 
    ``[<app_label>] -> plugin_config_dir`` config setting parsed in any
    of the application configuration files.

    If set, this item will be **appended** to
    ``CementApp.Meta.plugin_config_dirs`` so that it's settings will have
    presedence over other configuration files.

    In general, this setting should not be defined by the developer, as it
    is primarily used to allow the end-user to define a
    ``plugin_config_dir`` without completely trumping the hard-coded list
    of default ``plugin_config_dirs`` defined by the app/developer.

plugin_bootstrap = ``None``
    A python package (dotted import path) where plugin code can be
    loaded from.  This is generally something like ``myapp.plugins``
    where a plugin file would live at ``myapp/plugins/myplugin.py`` or 
    ``myapp/plugins/myplugin/__init__.py``.
    This provides a facility for applications that have builtin plugins that
    ship with the applications source code and live in the same Python module.

    Note: Though the meta default is ``None``, Cement will set this to
    ``<app_label>.plugins`` if not set.

plugin_dirs = ``None``
    A list of directory paths where plugin code (modules) can be loaded
    from.

    Note: Though ``CementApp.Meta.plugin_dirs`` is None, Cement will set this
    to a default list based on ``CementApp.Meta.label`` if not set.  This will
    equate to:

    .. code-block:: python

        ['~/.<app_label>/plugins', '/usr/lib/<app_label>/plugins']


    Modules are attempted to be loaded in order, and will stop loading
    once a plugin is successfully loaded from a directory.  Therefore
    this is the oposite of configuration file loading, in that here the first
    has precedence.

plugin_dir = ``None``
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

Creating a Plugin
-----------------

A plugin is essentially an extension of a Cement application, that is loaded
from an internal or external source location.  It is a mechanism for
dynamically loading code (whether the plugin is enabled or not).
It can contain any code that would normally be part of your application, but
should be thought of as optional features, where the core application does
not rely on that code to operate.

The following is an example plugin (single file) that provides a number of
options and commands via an application controller:

*myplugin.py*

.. code-block:: python

    from cement.core.controller import CementBaseController, expose

    class MyPluginController(CementBaseController):
        class Meta:
            label = 'myplugin'
            description = 'this is my controller description'
            stacked_on = 'base'

            config_defaults = dict(
                foo='bar',
                )

            arguments = [
                (['--foo'],
                 dict(action='store', help='the infamous foo option')),
                ]

        @expose(help="this is my command description")
        def mycommand(self):
            print 'in MyPlugin.mycommand()'

    def load(app):
        app.handler.register(MyPluginController)


As you can see, this is very similar to an application that has a base
controller, however as you'll note we do not create an application object
via ``foundation.CementApp()`` like we do in our application.  This code/file
would then be saved to a location defined by your applications configuration
that determines where plugins are loaded from (see the next section).

Notice that all 'bootstrapping' code goes in a ``load()`` function.  This is
where registration of handlers/hooks should happen.  For convenience, and
certain edge cases, the `app` object is passed here in its current state
at the time that ``load()`` is called.  You do not need to do anything with
the ``app`` object, but you can.

A plugin also has a configuration file that will be Cement will attempt to
find in one of the directories listed in ``CementApp.Meta.plugin_config_dirs``
as defined by your application's configuration.  The following is an example
plugin configuration file:

*myplugin.conf*

.. code-block:: text

    [myplugin]
    enable_plugin = true
    foo = bar



Loading a Plugin
----------------

Plugin modules are looked for first in one of the defined ``plugin_dirs``, and
if not found then Cement attempts to load them from the ``plugin_bootstrap``.
The following application shows how to configure an application to load
plugins.  Take note that these are the **default settings** and will work the
same if not defined:

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.core.controller import CementBaseController, expose

    class MyBaseController(CementBaseController):
        class Meta:
            label = 'base'
            description = 'MyApp Does Amazing Things'

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            base_controller = MyBaseController
            plugin_bootstrap='myapp.bootstrap',
            plugin_config_dirs=[
                '/etc/myapp/plugins.d',
                '~/.myapp/plugins.d',
                ]
            plugin_dirs=[
                '/usr/lib/myapp/plugins',
                '~/.myapp/plugins',
                ]


    def main():
        with MyApp() as app:
            app.run()

    if __name__ == '__main__':
        main()


We modified the default settings for ``plugin_config_dirs`` and
``plugin_dirs``.  These are the default settings under ``Cementapp``, however
we have put them here for clarity.

Running this application will do nothing particularly special, however the
following demonstrates what happens when we add a simple plugin that provides
an application controller:

*/etc/myapp/plugins.d/myplugin.conf*

.. code-block:: text

    [myplugin]
    enable_plugin = true
    some_option = some value

*/usr/lib/myapp/plugins/myplugin.py*

.. code-block:: python

    from cement.core.controller import CementBaseController, expose
    from cement.utils.misc import init_defaults

    defaults = init_defaults('myplugin')

    class MyPluginController(CementBaseController):
        class Meta:
            label = 'myplugin'
            description = 'this is my plugin description'
            stacked_on = 'base'
            config_defaults = defaults
            arguments = [
                (['--some-option'], dict(action='store')),
                ]

        @expose(help="this is my command description")
        def my_plugin_command(self):
            print 'In MyPlugin.my_plugin_command()'

    def load(app):
        app.handler.register(MyPluginController)


Running our application with the plugin disabled, we see:

.. code-block:: text

    $ python myapp.py --help
    usage: myapp.py (sub-commands ...) [options ...] {arguments ...}

    MyApp Does Amazing Things

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output


But if we enable the plugin, we get something a little different:

.. code-block:: text

    $ python myapp.py --help
    usage: myapp.py (sub-commands ...) [options ...] {arguments ...}

    MyApp Does Amazing Things

    commands:

      my-plugin-command
        this is my command description

    optional arguments:
      -h, --help            show this help message and exit
      --debug               toggle debug output
      --quiet               suppress all output
      --some-option SOME_OPTION

We can see that the ``my-plugin-command`` and the ``--some-option`` option
were provided by our plugin, which has been 'stacked' on top of the base
controller.

User Defined Plugin Configuration and Module Directories
--------------------------------------------------------

Most applications will want to provide the ability for the end-user to define
where plugin configurations and modules live.  This is possible by setting the
``plugin_config_dir`` and ``plugin_dir`` settings in any of the applications
configuration files.  Note that these paths will be **added** to the built-in
``plugin_config_dirs`` and ``plugin_dirs`` settings respectively, rather than
completely overwriting them.  Therefore, your application can maintain it's
default list of plugin configuration and module paths while also allowing
users to define their own.

*/etc/myapp/myapp.conf*

.. code-block:: text

    [myapp]
    plugin_dir = /usr/lib/myapp/plugins
    plugin_config_dir = /etc/myapp/plugins.d

The ``plugin_bootstrap`` setting is however only configurable within the
application itself.

What Can Go Into a Plugin?
--------------------------

The above example shows how to add an optional application controller via a
plugin, however a plugin can contain anything you want.  This could be as
simple as adding a hook that does something magical.  For example:

.. code-block:: python

    from cement.core import hook

    def my_magical_hook(app):
        # do something magical
        print('Something Magical is Happening!')

    def load(app):
        hook.register('post_setup', my_magical_hook)


And with the plugin enabled, we get this when we run the same app defined
above:

.. code-block:: text

    $ python myapp.py
    Something Magical is Happening!


The primary detail is that Cement calls the `load()` function of a plugin...
after that, you can do anything you like.


Single File Plugins vs. Plugin Directories
------------------------------------------

As of Cement 2.9.x, plugins can be either a single file (i.e ``myplugin.py``)
or a python module directory (i.e. ``myplugin/__init__.py``).  Both will be
loaded and executed the exact same way.

One caveat however, is that the submodules referenced from within a plugin 
directory must be relative path.  For example:

**myplugin/__init__.py**

.. code-block:: python

    from .controllers import MyPluginController

    def load(app):
        app.handler.register(MyPluginController)

**myplugin/controllers.py**

.. code-block:: python

    from cement.core.controller import CementBaseController, expose

    class MyPluginController(CementBaseController):
        class Meta:
            label = 'myplugin'
            stacked_on = 'base'
            stacked_type = 'embedded'

        @expose()
        def my_command(self):
            print('Inside MyPluginController.my_command()')


Loading Templates From Plugin Directories
-----------------------------------------

A common use case for complex applications is to use an output handler the
uses templates, such as Mustache, Genshi, Jinja2, etc.  In order for a plugin
to use it's own template files it's templates directory first needs to be 
added to the list of template directories to be parsed.  In the future, this
will be more streamlined however currently the following is the recommeded
way:

**myplugin/__init__.py**

.. code-block:: python

    def add_template_dir(app):
        path = os.path.join(os.path.basename(self.__file__, 'templates')
        app.add_template_dir(path)

    def load(app):
        app.hook.register('post_setup', add_template_dir)


The above will append the directory ``/path/to/myplugin/templates`` to the 
list of template directories that the applications output handler with search
for template files.

