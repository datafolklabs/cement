Namespaces
==========

The Cement Framework establishes a global 'namespaces' dictionary that stores
information for each namespace (and/or plugin).  Namespaces are primarily 
used by the plugin system to establish plugin namespaces, however there is
also a 'root' namespace for the base application. Each namespace has the 
following members:

    config
        A dictionary of configuration parameters.  For the 'root' namespace
        which is the base application itself, this holds all the critical
        configurations for your applicaton.  The 'root' namespace config
        is generated from a default set, and then overridden by config files
        in either /etc/yourapp/yourapp.conf (global) or ~/.yourapp.conf (per 
        user).  For plugins, the configuration is generated from a default
        set and then overridden by the plugin config file at
        /etc/yourapp/plugins.d/yourplugin.conf.
    
    label
        The name of the namespace (single word).
        
    version
        The version of the applicaton ('root') or of the plugin.  In general,
        internal plugins (those part of the core application) will probably
        want to inherite the version of the application from 
        pkg_resources.get_distribution('YouApp').version.
    
    description
        A brief summary of the plugin or namespace.
    
    commands
        A dictionary of commands exposed into this namespace.  This is
        different than commands exposed by the namespaces controller.  
        Controllers from any namespace can expose commands into other 
        namespaces, which will be added to the commands dict of the destination
        namespace.
        
    controller
        The CementController object for the namespace.  Set as a string
        when initializing a plugin, but is instantiated as the object
        after the plugin loads (and the namespace is created).
    
    options
        An OptParse object used to set options that are local to this 
        namespace only.  For example, for a subcommand 'cmd2' of the 'example'
        namespace, the option '--my-opt' would only appear under
        'myapp example cmd2 --my-opt' but would not be available under
        'myapp cmd1 --my-opt'.
        
    is_hidden
        Boolean, determines whether or not to display the namespace in the 
        output of 'myapp --help'.  By default, if the namespace does not 
        have any visible/exposed commands, the namespace will not display.


In general, namespaces are created when you register a plugin.  For example:

.. code-block:: python

    from cement import namespaces
    from cement.core.log import get_logger
    from cement.core.plugin import CementPlugin, register_plugin

    from helloworld.appmain import VERSION, BANNER

    log = get_logger(__name__)

    REQUIRED_CEMENT_API = '0.5-0.6:20100115'
        
    @register_plugin() 
    class ExamplePlugin(CementPlugin):
        def __init__(self):
            CementPlugin.__init__(self,
                label='example',
                version=VERSION,
                description='Example plugin for helloworld',
                required_api=REQUIRED_CEMENT_API,
                banner=BANNER,
                controller = 'ExampleController', # from helloworld.controllers.example
                )
        
            self.config['example_option'] = False
    
            self.options.add_option('-E', '--example', action='store',
                dest='example_option', default=None, help='Example Plugin Option'
                )        
                
You would then add 'example' to the enabled_plugins of your applications
configuration file.  Upon loading, this plugin is registered and the global
namespaces['example'] is created (which is a CementPlugin/CementNamespace 
object).
                
                