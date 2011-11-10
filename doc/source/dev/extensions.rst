Framework Extensions
====================

Cement defines an extension interface called :ref:`IExtension <cement2.core.extension>`, 
as well as the default :ref:`CementExtensionHandler <cement2.core.extension>` 
that implements the interface.  Its purpose is to manage loading framework
extensions and making them usable by the application.  Extensions are similar
to :ref:`Application Plugins <cement2.core.plugin>`, but at the framework level.

Please note that there may be other handler's that implement the IExtension
interface.  The documentation below only references usage based on the 
interface and not the full capabilities of the implementation.

The following extension handlers are included and maintained with Cement2:

    * :ref:`CementExtensionHandler <cement2.core.extension>`

Please reference the :ref:`IExtension <cement2.core.extension>` interface 
documentation for writing your own extension handler.

Extension Configuration Settings
--------------------------------

The following configuration settings under the 'base' section alter extension
handling:

extension_handler
^^^^^^^^^^^^^^^^^

The label of the extension handler to use.


extensions
^^^^^^^^^^

A list of extension modules to load.  


The following example shows how to alter these settings for your application:

.. code-block:: python

    from cement2.core import foundation, backend
    
    defaults = backend.defaults('myapp')
    defaults['base']['extension_handler'] = 'my_extension_handler'
    defaults['base']['extensions'] = [  
        'cement2.ext.ext_cement_output',
        'cement2.ext.ext_cement_plugin',
        'cement2.ext.ext_configparser', 
        'cement2.ext.ext_logging', 
        'cement2.ext.ext_argparse',
        ]
    
    app = foundation.lay_cement('myapp', defaults=defaults)
    app.setup()
    app.run()
    app.close()
    
You can also always use the default 'extensions' list, but add any additional
extensions to it:

.. code-block:: python

    ...
    defaults['base']['extensions'].append('myapp.ext.ext_example')
    ...

Creating an Extension
---------------------

The extension system is a mechanism for dynamically loading code to extend
the functionality of the framework.  In general, this includes the 
registration of interfaces, handlers, and/or hooks.

The following is an example extension that provides an 
:ref:`Output Handler <cement2.core.output>`.  We will assume this extension
is part of our 'myapp' application, so the extension module would be
'myapp.ext.ext_myapp_output' (or whatever you want to call it).

.. code-block:: python

    from cement2.core import backend, handler, output

    Log = backend.minimal_logger(__name__)

    class MyAppOutputHandler(object):
        class meta:
            interface = output.IOutput
            label = 'myapp_output'
        
        def __init__(self):
            self.config = None
            
        def setup(self, config_obj):
            self.config = config_obj
        
        def render(self, data_dict, template=None):
            Log.debug("Rendering output via MyAppOutputHandler")
            for key in data_dict.keys():
                print "%s => %s" % (key, data_dict[key])

    handler.register(MyAppOutputHandler)

Take note of two things.  One is, the 'Log' we are using is from 
cement2.core.backend.minimal_logger(__name__).  Framework extensions do not 
use the application log handler, every.  Using the minimal_logger() and only
log to 'DEBUG'.

Secondly, in our extension file we need to define any interfaces, register
handlers and/or hooks if necessary.  In this example we only needed to 
register our output handler (which happens when the extension is loaded
by the application).

You will notice that extensions are essentially the same as application 
plugins, however the difference is both when the code is loaded, as well as
the purpose of that code.  Framework extensions add functionality to the
framework for the application to utilize, where application plugins extend
the functionality of the application.

Loading an Extension
--------------------

Extensions are loaded when 'setup()' is called on an application.  Cement
automatically loads all extensions listed under the applications 
'base' -> 'extensions' configuration setting, as show in the example above.

To load the above example into our application, we just add it to the list
of extensions:

.. code-block:: python

    from cement2.core import foundation, backend
    
    defaults = backend.defaults('myapp')
    defaults['base']['extension_handler'] = 'my_extension_handler'
    defaults['base']['extensions'] = [  
        'cement2.ext.ext_cement_plugin',
        'cement2.ext.ext_configparser', 
        'cement2.ext.ext_logging', 
        'cement2.ext.ext_argparse',
        'myapp.ext.ext_output',
        ]
    
    app = foundation.lay_cement('myapp', defaults=defaults)
    app.setup()
    app.run()
    app.close()
    
To cleanup unecessary code, we also removed the default handler 
'cement2.ext.ext_cement_output'.  This isn't always necessary, or desired.
Depending on the handler, there may still be a need for it to be loaded even
if you aren't using it directly.


