Log Handling
============

Cement defines a logging interface called :ref:`ILog <cement.core.log>`,
as well as the default :ref:`LoggingLogHandler <cement.ext.ext_logging>`
that implements the interface.   This
handler is built on top of the `Logging <http://docs.python.org/library/logging.html>`_
module which is included in the Python standard library.

Please note that there may be other handler's that implement the ILog
interface.  The documentation below only references usage based on the
interface and not the full capabilities of the implementation.

The following log handlers are included and maintained with Cement:

    * :ref:`LoggingLogHandler <cement.ext.ext_logging>`
    * :ref:`ColorLogHandler <cement.ext.ext_colorlog>`


Please reference the :ref:`ILog <cement.core.config>` interface
documentation for writing your own log handler.

Logging Messages
----------------

The following shows logging to each of the defined log levels.

.. code-block:: python

    from cement.core import foundation
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
    app.log.warning('This is a warning message.')

    # Log an error message
    app.log.error('This is an error message.')

    # Log an fatal error message
    app.log.fatal('This is a fatal message.')

    # Close the application
    app.close()


The above is displayed in order of 'severity' you can say.  If the log level
is set to 'INFO', you will receive all 'info' messages and above .. including
warning, error, and fatal.  However, you will not receive DEBUG level messages.
The same goes for a log level of 'WARNING', where you will receive warning, 
error, and fatal... but you will not receive INFO, or DEBUG level messages.

Changing Log Level
------------------

The log level defaults to INFO, based on the 'config_defaults' of the log
handler.  You can override this via config_defaults:

.. code-block:: python

    from cement.core import foundation, backend
    from cement.utils.misc import init_defaults

    defaults = init_defaults('myapp', 'log.logging')
    defaults['log.logging']['level'] = 'WARNING'

    app = foundation.CementApp('myapp', config_defaults=defaults)
    app.setup()

This will also be overridden by the 'level' setting under a '[log.logging]'
section in any of the applications configuration files that are parsed.

You should also note that Cement includes a '--debug' command line option by
default.  This triggers the log level to 'DEBUG' and is helpful for quickly
debugging issues:

.. code-block:: text

    $ python test.py --debug
    2012-07-13 02:19:42,270 (DEBUG) cement.core.foundation : laying cement for the 'myapp' application
    2012-07-13 02:19:42,270 (DEBUG) cement.core.hook : defining hook 'pre_setup'
    2012-07-13 02:19:42,270 (DEBUG) cement.core.hook : defining hook 'post_setup'
    2012-07-13 02:19:42,270 (DEBUG) cement.core.hook : defining hook 'pre_run'
    2012-07-13 02:19:42,270 (DEBUG) cement.core.hook : defining hook 'post_run'
    2012-07-13 02:19:42,271 (DEBUG) cement.core.hook : defining hook 'pre_close'
    2012-07-13 02:19:42,271 (DEBUG) cement.core.hook : defining hook 'post_close'
    2012-07-13 02:19:42,271 (DEBUG) cement.core.hook : defining hook 'signal'
    2012-07-13 02:19:42,271 (DEBUG) cement.core.hook : defining hook 'pre_render'
    2012-07-13 02:19:42,271 (DEBUG) cement.core.hook : defining hook 'post_render'
    2012-07-13 02:19:42,271 (DEBUG) cement.core.handler : defining handler type 'extension' (IExtension)
    2012-07-13 02:19:42,271 (DEBUG) cement.core.handler : defining handler type 'log' (ILog)
    2012-07-13 02:19:42,271 (DEBUG) cement.core.handler : defining handler type 'config' (IConfig)
    2012-07-13 02:19:42,271 (DEBUG) cement.core.handler : defining handler type 'plugin' (IPlugin)
    2012-07-13 02:19:42,272 (DEBUG) cement.core.handler : defining handler type 'output' (IOutput)
    2012-07-13 02:19:42,272 (DEBUG) cement.core.handler : defining handler type 'argument' (IArgument)
    2012-07-13 02:19:42,272 (DEBUG) cement.core.handler : defining handler type 'controller' (IController)
    2012-07-13 02:19:42,272 (DEBUG) cement.core.handler : defining handler type 'cache' (ICache)
    2012-07-13 02:19:42,272 (DEBUG) cement.core.handler : registering handler '<class 'cement.core.extension.CementExtensionHandler'>' into handlers['extension']['cement']
    2012-07-13 02:19:42,272 (DEBUG) cement.core.foundation : now setting up the 'myapp' application
    2012-07-13 02:19:42,272 (DEBUG) cement.core.foundation : adding signal handler for signal 15
    2012-07-13 02:19:42,273 (DEBUG) cement.core.foundation : adding signal handler for signal 2
    2012-07-13 02:19:42,273 (DEBUG) cement.core.foundation : setting up myapp.extension handler
    2012-07-13 02:19:42,273 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_dummy' framework extension
    2012-07-13 02:19:42,273 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_dummy.DummyOutputHandler'>' into handlers['output']['null']
    2012-07-13 02:19:42,273 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_plugin' framework extension
    2012-07-13 02:19:42,273 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_plugin.CementPluginHandler'>' into handlers['plugin']['cement']
    2012-07-13 02:19:42,273 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_configparser' framework extension
    2012-07-13 02:19:42,274 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_configparser.ConfigParserConfigHandler'>' into handlers['config']['configparser']
    2012-07-13 02:19:42,274 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_logging' framework extension
    2012-07-13 02:19:42,274 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_logging.LoggingLogHandler'>' into handlers['log']['logging']
    2012-07-13 02:19:42,274 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_argparse' framework extension
    2012-07-13 02:19:42,276 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_argparse.ArgParseArgumentHandler'>' into handlers['argument']['argparse']
    2012-07-13 02:19:42,276 (DEBUG) cement.core.foundation : setting up myapp.config handler
    2012-07-13 02:19:42,276 (DEBUG) cement.ext.ext_configparser : config file '/etc/myapp/myapp.conf' does not exist, skipping...
    2012-07-13 02:19:42,277 (DEBUG) cement.core.foundation : no cache handler defined, skipping.
    2012-07-13 02:19:42,277 (DEBUG) cement.core.foundation : setting up myapp.log handler
    2012-07-13 02:19:42,277 (DEBUG) cement.core.handler : merging config defaults from '<cement.ext.ext_logging.LoggingLogHandler object at 0x100588dd0>'
    2012-07-13 02:19:42,277 (DEBUG) myapp : logging initialized for 'myapp' using LoggingLogHandler
    2012-07-13 02:19:42,278 (DEBUG) cement.core.foundation : setting up myapp.plugin handler
    2012-07-13 02:19:42,278 (DEBUG) cement.ext.ext_plugin : plugin config dir /etc/myapp/plugins.d does not exist.
    2012-07-13 02:19:42,278 (DEBUG) cement.core.foundation : setting up myapp.arg handler
    2012-07-13 02:19:42,279 (DEBUG) cement.core.foundation : setting up myapp.output handler
    2012-07-13 02:19:42,279 (DEBUG) cement.core.foundation : setting up application controllers
    2012-07-13 02:19:42,279 (DEBUG) cement.core.foundation : no controller could be found.
    2012-07-13 02:19:42,280 (DEBUG) cement.core.foundation : closing the application

You can see that debug logging is extremely verbose.  In the above you will
note the message format is:

.. code-block:: text

    TIMESTAMP - LEVEL - MODULE - MESSAGE

The Cement framework only logs to DEBUG, where the MODULE is displayed as
'cement.core.whatever'.  Note that Cement uses a minimal logger that is
separate from the application log, therefore settings you change in your
application do not affect it.

Logging to Console
------------------

The default log handler configuration enables logging to console.  For example:

.. code-block:: python

    from cement.core import foundation
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
defaults, or in an application configuration file under the '[log.logging]'
section.

Logging to a File
-----------------

File logging is disabled by default, but is just one line to enable.  Simply
set the 'file' setting under the '[log.logging]' config section either by application
defaults, or via a configuration file.

.. code-block:: python

    from cement.core import foundation, backend
    from cement.utils.misc import init_defaults

    defaults = init_defaults('myapp', 'log.logging')
    defaults['log.logging']['file'] = 'my.log'

    app = foundation.CementApp('myapp', config_defaults=defaults)
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


Notice that the logging is a bit more verbose when logged to a file.


Tips on Debugging
-----------------

Note: The following is specific to the default
:ref:`LoggingLogHandler <cement.ext.ext_logging>` only, and is not
an implementation of the ILog interface.

Logging to 'app.log.debug()' is pretty straight forward, however adding an
additional parameter for the 'namespace' can greatly increase insight into
where that log is happening.  The 'namespace' defaults to the application name
which you will see in every log like this:

.. code-block:: text

    2012-07-30 18:05:11,357 (DEBUG) myapp : This is my message

For debugging, it might be more useful to change this to __name__:

.. code-block:: python

    app.log.debug('This is my info message', __name__)

Which looks like:

.. code-block:: text

    2012-07-30 18:05:11,357 (DEBUG) myapp.somepackage.test : This is my message

Or even more verbose, the __file__ and a line number of the log:

.. code-block:: python

    app.log.debug('This is my info message', '%s,L2734' % __file__)

Which looks like:

.. code-block:: text

    2012-07-30 18:05:11,357 (DEBUG) myapp/somepackage/test.py,L2345 : This is my message

You can override this with anything... it doesn't have to be just for
debugging.
