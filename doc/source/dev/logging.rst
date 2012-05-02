Log Handling
============

Cement defines a logging interface called :ref:`ILog <cement2.core.log>`, 
as well as the default :ref:`LoggingLogHandler <cement2.ext.ext_logging>` 
that implements the interface.   This 
handler is built on top of the `Logging <http://docs.python.org/library/logging.html>`_ 
module which is included in the Python standard library.  

Please note that there may be other handler's that implement the ILog
interface.  The documentation below only references usage based on the 
interface and not the full capabilities of the implementation.

The following log handlers are included and maintained with Cement2:

    * :ref:`LoggingLogHandler <cement2.ext.ext_logging>`
    

Please reference the :ref:`ILog <cement2.core.config>` interface 
documentation for writing your own log handler.

Logging Messages
----------------

The following shows logging to each of the defined log levels.

.. code-block:: python

    from cement2.core import foundation
    app = foundation.CementApp('myapp')
    
    # First setup the application
    app.setup()
    
    # Run the application (even though it doesn't do much here)
    app.run()
    
    # Log a debug message
    app.log.debug('This is a debug message.')
    
    # Log an info message
    app.log.info('This is an info message.')
    
    # Log a warning message
    app.log.warn('This is a warning message.')
    
    # Log an error message
    app.log.error('This is an error message.')
    
    # Log an fatal error message
    app.log.fatal('This is a fatal message.')
    
    # Close the application
    app.close()


The above is displayed in order of 'severity' you can say.  If the log level
is set to 'INFO', you will receive all 'info' messages and above .. including
warning, error, and fatal.  However, you will not receive DEBUG level messages.
The same goes for a log level of 'WARN', where you will receive warning, error,
and fatal... but you will not receive INFO, or DEBUG level messages.

Changing Log Level
------------------

The log level defaults to INFO, based on the 'config_defaults' of the log 
handler.  You can override this via config_defaults:

.. code-block:: python

    from cement2.core import foundation, backend

    defaults = backend.defaults('myapp', 'log')
    defaults['log']['level'] = 'WARN'
    
    app = foundation.CementApp('myapp', config_defaults=defaults)
    app.setup()
    
This will also be overridden by the 'level' setting under a '[log]' section
in any of the applications configuration files that are parsed.

You should also note that Cement includes a '--debug' command line option by
default.  This triggers the log level to 'DEBUG' and is helpful for quickly
debugging issues:

.. code-block:: text

    $ python test.py --debug
    2011-08-26 18:00:31,993 (DEBUG) cement2.core.foundation : laying cement for the 'myapp' application
    2011-08-26 18:00:31,993 (DEBUG) cement2.core.hook : defining hook 'cement_init_hook'
    2011-08-26 18:00:31,993 (DEBUG) cement2.core.hook : defining hook 'cement_add_args_hook'
    2011-08-26 18:00:31,993 (DEBUG) cement2.core.hook : defining hook 'cement_validate_config_hook'
    2011-08-26 18:00:31,993 (DEBUG) cement2.core.handler : defining handler type 'extension' (IExtension)
    2011-08-26 18:00:31,993 (DEBUG) cement2.core.handler : defining handler type 'log' (ILog)
    2011-08-26 18:00:31,994 (DEBUG) cement2.core.handler : defining handler type 'config' (IConfig)
    2011-08-26 18:00:31,994 (DEBUG) cement2.core.handler : defining handler type 'plugin' (IPlugin)
    2011-08-26 18:00:31,994 (DEBUG) cement2.core.handler : defining handler type 'output' (IOutput)
    2011-08-26 18:00:31,994 (DEBUG) cement2.core.handler : defining handler type 'argument' (IArgument)
    2011-08-26 18:00:31,994 (DEBUG) cement2.core.handler : defining handler type 'controller' (IController)
    2011-08-26 18:00:31,994 (DEBUG) cement2.core.handler : registering handler '<class 'cement2.core.extension.CementExtensionHandler'>' into handlers['extension']['cement']
    2011-08-26 18:00:31,994 (DEBUG) cement2.core.foundation : now setting up the 'myapp' application
    2011-08-26 18:00:31,994 (DEBUG) cement2.core.foundation : setting up myapp.extension handler
    2011-08-26 18:00:31,995 (DEBUG) cement2.core.foundation : no config defaults from '<cement2.core.extension.CementExtensionHandler object at 0x1005827d0>'
    2011-08-26 18:00:31,995 (DEBUG) cement2.core.extension : loading the 'cement2.ext.ext_cement_output' framework extension
    2011-08-26 18:00:31,995 (DEBUG) cement2.core.handler : registering handler '<class 'cement2.ext.ext_cement_output.CementOutputHandler'>' into handlers['output']['cement']
    2011-08-26 18:00:31,995 (DEBUG) cement2.core.extension : loading the 'cement2.ext.ext_cement_plugin' framework extension
    2011-08-26 18:00:31,996 (DEBUG) cement2.core.handler : registering handler '<class 'cement2.ext.ext_cement_plugin.CementPluginHandler'>' into handlers['plugin']['cement']
    2011-08-26 18:00:31,996 (DEBUG) cement2.core.extension : loading the 'cement2.ext.ext_configparser' framework extension
    2011-08-26 18:00:31,999 (DEBUG) cement2.core.handler : registering handler 'cement2.ext.ext_configparser.ConfigParserConfigHandler' into handlers['config']['configparser']
    2011-08-26 18:00:31,999 (DEBUG) cement2.core.extension : loading the 'cement2.ext.ext_logging' framework extension
    2011-08-26 18:00:32,000 (DEBUG) cement2.core.handler : registering handler '<class 'cement2.ext.ext_logging.LoggingLogHandler'>' into handlers['log']['logging']
    2011-08-26 18:00:32,000 (DEBUG) cement2.core.extension : loading the 'cement2.ext.ext_argparse' framework extension
    2011-08-26 18:00:32,000 (DEBUG) cement2.core.handler : registering handler '<class 'cement2.ext.ext_argparse.ArgParseArgumentHandler'>' into handlers['argument']['argparse']
    2011-08-26 18:00:32,000 (DEBUG) cement2.core.foundation : setting up myapp.config handler
    2011-08-26 18:00:32,001 (DEBUG) cement2.core.foundation : validating required configuration parameters
    2011-08-26 18:00:32,001 (DEBUG) cement2.core.foundation : setting up myapp.log handler
    2011-08-26 18:00:32,001 (DEBUG) cement2.core.foundation : setting config defaults from '<cement2.ext.ext_logging.LoggingLogHandler object at 0x10040ffd0>'
    2011-08-26 18:00:32,002 (DEBUG) myapp : logging initialized for 'myapp' using LoggingLogHandler
    2011-08-26 18:00:32,002 (DEBUG) cement2.core.foundation : setting up myapp.plugin handler
    2011-08-26 18:00:32,002 (DEBUG) cement2.core.foundation : no config defaults from '<cement2.ext.ext_cement_plugin.CementPluginHandler object at 0x100590f50>'
    2011-08-26 18:00:32,002 (DEBUG) cement2.core.foundation : setting up myapp.arg handler
    2011-08-26 18:00:32,003 (DEBUG) cement2.core.foundation : no config defaults from 'ArgParseArgumentHandler(prog='test.py', usage=None, description=None, version=None, formatter_class=<class 'argparse.HelpFormatter'>, conflict_handler='error', add_help=True)'
    2011-08-26 18:00:32,004 (DEBUG) cement2.core.foundation : setting up myapp.output handler
    2011-08-26 18:00:32,004 (DEBUG) cement2.core.foundation : no config defaults from '<cement2.ext.ext_cement_output.CementOutputHandler object at 0x100599350>'
    2011-08-26 18:00:32,004 (DEBUG) cement2.core.foundation : setting up myapp.controller handler
    2011-08-26 18:00:32,004 (DEBUG) cement2.core.foundation : no controller could be found.
    2011-08-26 18:00:32,005 (INFO) myapp : This is my info message


You can see that debug logging is extremely verbose.  In the above you will 
note the message format is:

.. code-block:: text
    
    TIMESTAMP - LEVEL - MODULE - MESSAGE
    
The Cement framework only logs to DEBUG, where the MODULE is displayed as
'cement2.core.whatever'.  Note that Cement uses a minimal logger that is 
separate from the application log, therefore settings you change in your
application do not affect it.  

Logging to Console
------------------

The default log handler configuration enables logging to console.  For example:

.. code-block:: python

    from cement2.core import foundation
    app = foundation.CementApp('myapp')
    app.setup()
    app.run()
    app.log.info('This is my info message')
    app.close()

When running this script at command line you would get:

.. code-block:: text

    $ python test.py
    INFO: This is my info message
    
This can be disabled by setting 'to_console=False' in either the application
defaults, or in an application configuration file under the '[log]' section.

Logging to a File
-----------------

File logging is disabled by default, but is just one line to enable.  Simply
set the 'file' setting under the '[log]' config section either by application
defaults, or via a configuration file.

.. code-block:: python

    from cement2.core import foundation, backend

    defaults = backend.defaults('myapp', 'log')
    defaults['log']['file'] = 'my.log'

    app = foundation.CementApp('myapp', defaults=defaults)
    app.setup()
    app.run()
    app.log.info('This is my info message')
    app.close()

Running this we will see:

.. code-block:: text

    $ python test.py
    INFO: This is my info message
    
    $ cat my.log
    2011-08-26 17:50:16,306 (INFO) myapp : This is my info message
    

Notice that the logging is a bit more verbose when logged to a file.  One 
thing in particular to pay attention to is that the third column ('myapp') 
will always be the module where the log was called.  This is very helpful 
for debugging to know where execution is in your application at the point of
that log.  
