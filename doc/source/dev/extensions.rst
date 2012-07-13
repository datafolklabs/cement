Framework Extensions
====================

Cement defines an extension interface called :ref:`IExtension <cement.core.extension>`, 
as well as the default :ref:`CementExtensionHandler <cement.core.extension>` 
that implements the interface.  Its purpose is to manage loading framework
extensions and making them usable by the application.  Extensions are similar
to :ref:`Application Plugins <cement.core.plugin>`, but at the framework level.

Please note that there may be other handler's that implement the IExtension
interface.  The documentation below only references usage based on the 
interface and not the full capabilities of the implementation.

The following extension handlers are included and maintained with Cement:

    * :ref:`CementExtensionHandler <cement.core.extension>`

Please reference the :ref:`IExtension <cement.core.extension>` interface 
documentation for writing your own extension handler.

Extension Configuration Settings
--------------------------------

The following Meta settings are honored under the CementApp:

    extension_handler
        A handler class that implements the IExtension interface.  This can
        be a string (label of a registered handler), an uninstantiated
        class, or an instantiated class object.
        Default: CementExtensionHandler.
        
    core_extensions
        List of Cement core extensions.  These are generally required by
        Cement and should only be modified if you know what you're 
        doing.  Use 'extensions' to add to this list, rather than 
        overriding core extensions.  That said if you want to prune down
        your application, you can remove core extensions if they are
        not necessary (for example if using your own log handler 
        extension you likely don't want/need LoggingLogHandler to be 
        registered).
    
    extensions
        List of additional framework extensions to load.
        Default: []
        
The following example shows how to alter these settings for your application:

.. code-block:: python

    from cement.core import foundation
    
    app = foundation.CementApp('myapp',
        extension_handler = MyExtensionHandler
        core_extensions = [
            'cement_output',
            'cement_plugin',
            'configparser', 
            'logging', 
            'argparse',
            ]
        extensions = ['myapp.ext.ext_something_fansy']
        )
        
    try:
        app.setup()
        app.run()
    finally:
        app.close()

Creating an Extension
---------------------

The extension system is a mechanism for dynamically loading code to extend
the functionality of the framework.  In general, this includes the 
registration of interfaces, handlers, and/or hooks.

The following is an example extension that provides an 
:ref:`Output Handler <cement.core.output>`.  We will assume this extension
is part of our 'myapp' application, so the extension module would be
'myapp.ext.ext_myapp_output' (or whatever you want to call it).

.. code-block:: python

    from cement.core import backend, handler, output

    Log = backend.minimal_logger(__name__)

    class MyAppOutputHandler(output.CementOutputHandler):
        class Meta:
            label = 'myapp_output'
                
        def render(self, data_dict, template=None):
            Log.debug("Rendering output via MyAppOutputHandler")
            for key in data_dict.keys():
                print "%s => %s" % (key, data_dict[key])

    def load():
        handler.register(MyAppOutputHandler)

Take note of two things.  One is, the 'Log' we are using is from 
cement.core.backend.minimal_logger(__name__).  Framework extensions do not 
use the application log handler, ever.  Use the minimal_logger(), and only
log to 'DEBUG' (recommended).

Secondly, in our extension file we need to define any interfaces, register
handlers and/or hooks if necessary.  In this example we only needed to 
register our output handler (which happens when the extension is loaded
by the application).

Last, notice that all 'bootstrapping' code goes in a load() function.  This is
where registration of handlers/hooks should happen.

You will notice that extensions are essentially the same as application 
plugins, however the difference is both when/how the code is loaded, as well as
the purpose of that code.  Framework extensions add functionality to the
framework for the application to utilize, where application plugins extend
the functionality of the application.

Loading an Extension
--------------------

Extensions are loaded when 'setup()' is called on an application.  Cement
automatically loads all extensions listed under the applications 
'core_extensions' and 'extensions' meta options.

To load the above example into our application, we just add it to the list
of extensions (not core extensions).  Lets assume the extension code lives
in 'myapp/ext/ext_something_fansy.py':

.. code-block:: python

    from cement.core import foundation

    app = foundation.CementApp('myapp',
        extensions = ['myapp.ext.ext_something_fansy']
        )
            
    try:        
        app.setup()
        app.run()
    finally:
        app.close()
    
Note that Cement provides a shortcut for Cement extensions.  For example, the
following:

.. code-block:: python

    app = foundation.CementApp('myapp', extensions=['json', 'daemon'])

Is equivalent to:

.. code-block:: python

    app = foundation.CementApp('myapp',
        extensions=[
            'cement.ext.ext_json', 
            'cement.ext.ext_daemon',
            ]
        )

For non-cement extensions you need to use the full python 'dotted' module 
path.