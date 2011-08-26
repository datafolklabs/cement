Configuration Handling
======================

Cement provides a configuration interface called 'IConfig', as well as a
default config handler that implements that interface.  

By default, Cement loads the cement2.ext.ext_configparser framework extension
which provides the ConfigParserConfigHandler implementation of IConfig.  This 
handler is built on top of `ConfigParser <http://docs.python.org/library/configparser.html>`_ 
which is included in the Python standard library.  Therefor, this class will
work much like ConfigParser but with any added functions necessary to
meet the requirements of the IConfig interface.

Please note that there are other handler's that implement the IConfig 
interface.  The documentation below only references usage based on the 
interface and not the full capabilities of the implementation.

The following config handlers are included and maintained with Cement2, though
may need to be installed via an external extension:

    * ConfigParserConfigHandler (default)
    * ConfigObjConfigHandler
    
    
Configuration Ordering
----------------------

An applications configuration is made up of a number of things, including
default settings, handler defaults, config file settings, etc.  The following
is the order in which configurations are discoverred:

    * Loaded from backend.defaults()
    * Extended by any handler defaults (not overridden)
    * Overridden by a defaults dict passed to foundation.lay_cement()
    * Overridden by the configuration files
    * Overridden by command line options that match the same key name


Application Default Settings
----------------------------

Cement requires a number of basic default settings in order to operate.  These
settings are found under the 'base' section of the config, and overridden by
a '[base]' block from a configuration file.

You do not need to override these values, and the default dictionary is used 
if no other defaults are passed when creating an application.  For example,
the following:

.. code-block:: python

    from cement2.core import foundation
    app = foundation.lay_cement('myapp')

Is equivalent to:

.. code-block:: python

    from cement2.core import foundation, backend
    defaults = backend.defaults()
    app = foundation.lay_cement('myapp', defaults=defaults)
    

That said, you can override default settings or add your own defaults like
so:

.. code-block:: python

    from cement2.core import foundation, backend
    
    defaults = backend.defaults()
    defaults['base']['debug'] = True
    defaults['base']['foo'] = 'bar'
    
    app = foundation.lay_cement('myapp', defaults=defaults)

It is important to note that the default settings, which is a dict, is parsed
by the config handler and loaded into it's own configuration mechanism.  
Meaning, though some config handlers (i.e. ConfigObj) might also be accessible
like a dict, not all do (i.e. ConfigParser).  Please see the documentation
for the config handler you use for their full usage.   

Accessing Configuration Settings
--------------------------------

After application creation, you can access the config handler via the 
'config' object.  For example:

.. code-block:: python

    from cement2.core import foundation
    app = foundation.lay_cement('myapp')
    
    # First setup the application
    app.setup()
    
    # Get settings
    app.config.get('base', 'debug')
    
    # Set settings
    app.config.set('base', 'debug', True)
    
    # Get sections (configuration [blocks])
    app.config.get_sections()
    
    # Add a section
    app.config.add_section('my_config_section')
    
    # Test if a section exists
    app.config.has_section('my_config_section')
    
    # Get configuration keys for the 'base' section
    app.config.keys('base')
    
    # Test if a key exist
    app.config.has_key('base', 'debug')

    # Merge a dict of settings into the config
    other_config = dict()
    other_config['base'] = dict()
    other_config['base']['foo'] = 'not bar'
    app.config.merge(other_config)
    
    
Parsing Config Files
--------------------

Most applications benefit from allowing their users to customize runtime via
a configuration file.  This can be done by:

.. code-block:: python

    from cement2.core import foundation
    app = foundation.lay_cement('myapp')
    
    # First setup the application
    app.setup()
    
    # Parse a configuration file
    app.config.parse_file('/path/to/some/file.conf')
    
    
Overriding Configurations with Command Line Options
---------------------------------------------------

Config settings are automatically overridden if a passed command line option
matches the name.  Note that this happens in *all* sections:

.. code-block:: python

    from cement2.core import foundation
    
    defaults = backend.defaults()
    defaults['base']['foo'] = 'bar'
    app = foundation.lay_cement('myapp')
    
    # First setup the application
    app.setup()
    
    # Add arguments
    app.args.add_argument('--foo', action='store', dest='foo')
    
    # Run the application (this parsed command line, among other things)
    app.run()

At the command line, running the application and passing the '--foo=some_value'
option will override the 'foo' setting under the 'base' (or any other) section.



Customizing Configuration Handlers
----------------------------------

Some config handlers might allow customizations, or accept additional 
arguments that you might want to pass and take advantage of.  Please note that
this is based on the handler implementation, and not the IConfig interface.

For example:

.. code-block:: python

    from cement2.core import foundation
    from myapp.config import MyConfigHandler
    
    myconfig = MyConfigHandler(some_keywork='some_value')
    
    # do something else with config_handler
    

Note that, at this point the config handler is instantiated, but it is not 
setup for use by the framework, meaning that some functions might not work
as expected.  Cement calls 'setup()' on all handlers when app.setup() is 
called.  Now you just need to pass the handler when creating a new 
application.

.. code-block:: python
    
    app = foundation.lay_cement('myapp', config_handler=myconfig)
    
