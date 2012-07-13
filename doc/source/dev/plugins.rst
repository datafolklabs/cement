Application Plugins
===================

Cement defines a plugin interface called :ref:`IPlugin <cement.core.plugin>`, 
as well as the default :ref:`CementPluginHandler <cement.ext.ext_plugin>` 
that implements the interface.  

Please note that there may be other handler's that implement the IPlugin
interface.  The documentation below only references usage based on the 
interface and not the full capabilities of the implementation.

The following output handlers are included and maintained with Cement:

    * :ref:`CementPluginHandler <cement.ext.ext_plugin>`

Please reference the :ref:`IPlugin <cement.core.plugin>` interface 
documentation for writing your own plugin handler.

Plugin Configuration Settings
-----------------------------

There are a few settings related to how plugins are loaded under the 
applications Meta options.  These are:

**plugin_config_dir**

The directory where plugin config files live.  This is usually something
like '/etc/myapp/plugins.d' or similar.  When the application runs, the
plugin handler will parse all config files in this directory looking for
enabled plugins.  Any plugins that are enabled will then be loaded.

**plugin_dir**

This is simply an external location where plugins can be loaded from.  This is
usually something like '/var/lib/myapp/plugins' or similar.  Plugins here must
be a single file.

**plugin_bootstrap**

For internal plugins, or plugins that tie into the actual python namespace
as the application.  For example, via Setuptools you can define 
'myapp/bootstrap' as namespace package.  Meaning that multiple sources can
install files to 'myapp/bootstrap' and still be called as 
'myapp.bootstrap.whatever' within the application.  

This is useful for plugins that go beyond a single file... where the plugins
'bootstrap' module is loaded when the plugin is loaded.  The bootstrap module
is expected to load anything else it needs from other files.

Creating a Plugin
-----------------

A plugin is essentially just an extension of a Cement application, that is 
loaded from an internal or external source location.  It is really just an 
mechanism for dynamically loading code (whether the plugin is enabled or not).
It can contain any code that would normally be part of your application, but 
should be thought of as 'optional' features, where the core application does 
not rely on that code to operate.  

The following is an example plugin (single file) that provides a number of
options and commands via an application controller:

*myplugin.py*

.. code-block:: python

    from cement.core import handler, controller

    class MyPluginController(controller.CementBaseController):
        class Meta:
            label = 'myplugin'
            description = 'This is my plugin controller.'
            stacked_on = 'base'
            config_defaults = dict(foo='bar')
            arguments = [
                (['--foo'], dict(action='store', help='the infamous foo option')),
                ]

        @controller.expose(help="This is my command.")
        def mycommand(self):
            print 'in MyPlugin.mycommand()'
        
    def load():
        handler.register(MyPluginController)


As you can see, this is very similar to an application that has a base 
controller, however as you'll note we do not create an application object
via foundation.CementApp() like we do in our application.  This code/file
would then be saved to a location defined by your applications configuration
that determines where plugins are loaded from (See the next section).

Notice that all 'bootstrapping' code goes in a load() function.  This is
where registration of handlers/hooks should happen.

A plugin also has a configuration file that will be found in the 
'plugin_config_dir' as defined by your applications configuration.  The 
following is an example plugin configuration file:

*myplugin.conf*

.. code-block:: text

    [myplugin]
    enable_plugin = true
    foo = bar
    


Loading a Plugin
----------------

Plugins are looked for first in the 'plugin_dir', and if not found then 
Cement attempts to load them from the 'plugin_bootstrap'.  The following
application shows how to configure an application to load plugins:

.. code-block:: python

    import sys
    from cement.core import backend, foundation
    
    app = foundation.CementApp('myapp', 
            plugin_config_dir='/etc/myapp/plugins.d/plugins.d',
            plugin_dir='/usr/lib/myapp/plugins',
            plugin_bootstrap='myapp.bootstrap',
            )
    try:
        app.setup()
        app.run()
    finally:
        app.close()
    
    
We modified the default settings for 'plugin_config_dir' and 'plugin_dir'.  
Note that the default config setting for 'plugin_bootstrap' would be 
'myapp.bootstrap', but we put it here anyway for clarity.

Running this application will do nothing particularly special, however by 
adding a plugin config dir setting to '/etc/myapp/plugins.d' and a plugin dir 
setting to '/usr/lib/myapp/plugins' we can dynamically extend the 
functionality of our app.  Take the following for example:

*/etc/myapp/plugins.d/myplugin.conf*

.. code-block:: text

    [myplugin]
    enable_plugin = true
    some_option = some value

*/usr/lib/myapp/plugins/myplugin.py*

.. code-block:: python

    from cement.core import handler, controller

    class MyPluginController(controller.CementBaseController):
        class Meta:
            label = 'myplugin'
            description = 'This is my plugin controller.'
            stacked_on = 'base'
    
            config_defaults = dict(some_option='some_value')

            arguments = [
                (['--some-option'], dict(action='store')),
                ]

        @controller.expose(help="This is my command.")
        def my_plugin_command(self):
            print 'in MyPlugin.my_plugin_command()'
    
    def load():
        handler.register(MyPluginController)


Running our application we can see:

.. code-block:: text

    $ python test.py --help
    usage: test.py <CMD> -opt1 --opt2=VAL [arg1] [arg2] ...

    HelloWorld does amazing things!

    commands:

      command1
        this command does relatively nothing useful.

      my_plugin_command
        This is my command.

    optional arguments:
      -h, --help            show this help message and exit
      --debug               toggle debug output
      --quiet               suppress all output
      --foo FOO             the notorious foo option
      -C                    the big C option
      --some-option SOME_OPTION
     
We can see that the 'my_plugin_command' and the '--some-option' option were
provided by our plugin.  Note that the 'plugin_dir' and 'plugin_config_dir'
are also configurable by the applications 'base' configuration.  For example:

*/etc/myapp/myapp.conf*

.. code-block:: text

    [myapp]
    plugin_dir = /usr/lib/myapp/plugins
    plugin_config_dir = /etc/myapp/plugins.d

The 'plugin_bootstrap' setting is however only configurable within the
application itself.