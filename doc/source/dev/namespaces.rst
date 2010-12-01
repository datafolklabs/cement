
Namespaces
==========

The Cement Framework establishes a global 'namespaces' dictionary that stores
information for each namespace (and/or plugin).  A Cement namespace should
not be confused with a Python namespace.  We use namespaces in reference to
where commands, configurations, command line options/arguments, etc are 
accessible from.

All namespaces have the following members, that are available under the 
global *namespaces['namespace']* dictionary:

    config
        A ConfigObj object, also accessible as a dict.  For the 'root' namespace
        which is the base application itself, this holds all the critical
        configurations for your application.  The 'root' namespace config
        is generated from a default set, and then overridden by config files
        in either /etc/yourapp/yourapp.conf (global) or ~/.yourapp.conf (per 
        user).  For namespace specific configs, the configuration is generated 
        from a default set and then overridden by the plugin config file at
        /etc/yourapp/plugins.d/yourplugin.conf or from a [namespace] block
        from the main applications configuration file.
    
    label
        The name of the namespace (single word).  For complex namespaces, or 
        those that are better fit for two words, you must use an underscore
        '_'.  All python modules/files, config files, and config blocks 
        '[you_namespace]' must also use underscores.  That said, Cement will
        display this namespaces *with* dashes in the --help output and will
        be called as 'your-namespace' which is more proper for command line
        access.
        
    version
        The version of the applicaton ('root') or of the plugin.  If not 
        specified this version will be inherited from the root namespace.
    
    description
        A brief summary of the plugin or namespace.
    
    commands
        A dictionary of commands exposed into this namespace.  This is
        different than commands exposed by the namespaces controller.  
        Controllers from any namespace can expose commands into other 
        namespaces, which will be added to the commands dictionary of the 
        destination namespace (yes, it's confusing).
        
    controller
        The CementController object for the namespace.  Set as a string
        when initializing a namespace, but is instantiated as the object
        when the namespace is registered.
    
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


Namespaces are generally used to breakup your applicaton into smaller parts.
For example, if you have 50 commands under the root namespace and all show
up under 'myapp --help' you're users are going to hate you.  Namespaces allow
you to breaking up commands into smaller, related sections.

**./helloworld/bootstap/example.py**:

.. code-block:: python

    from cement.core.hook import define_hook
    from cement.core.namespace import CementNamespace, register_namespace

    define_hook('my_example_hook')

    # Setup the 'example' namespace object
    example = CementNamespace('example', controller='ExampleController')

    # Example namespace default configurations, overwritten by the [example] 
    # section of the applications config file(s).  Once registered, this dict is
    # accessible as:
    #
    #   from cement.core.namespace import get_config
    #   example_config = get_config('example')
    #
    # Or simply as:
    #
    #   root_config = get_config()
    #   root_config['example']
    #
    example.config['foo'] = 'bar'

    # Example namespace options.  These options show up under:
    #
    #   $ {{package}} example --help
    #
    example.options.add_option('-F', '--foo', action='store',
        dest='foo', default=None, help='Example Foo Option'
        )

    # Officialize and register the namespace
    register_namespace(example)


Namespaces are always defined and registered in an associated bootstrap file, 
as in the above example we registered the 'example' namespace from the file
'helloworld/bootstrap/example.py'.


Accessing Namespaces
^^^^^^^^^^^^^^^^^^^^

Accessing the namespaces dictionary directly is not recommended from outside
the Cement Framework code.  That said, there might be a sitation you would 
want to and well, we can't stop you can we?

.. code-block:: python

    from cement import namespaces
    
    my_namespace = namespaces['my_namespace']
    my_namespace.config
    my_namespace.commands
    my_namespace.version


