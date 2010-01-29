
Namespaces and Plugin Support
=============================

The Cement Framework establishes a global 'namespaces' dictionary that stores
information for each namespace (and/or plugin).  Namespaces are primarily 
used by the plugin system to establish plugin namespaces, however there is
also a 'root' namespace for the base application. Each namespace has the 
following members:


.. _namespaces-ref:

Namespaces
----------

All namespaces have the following members, that are available under the 
global *namespaces['namespace']* dictionary:

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


In general, namespaces are created when you register a plugin, but can be
manually defined as well.


Accessing Namespaces
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from cement import namespaces
    
    my_namespace = namespaces['my_namespace']
    my_namespace.config
    


Plugin Support
==============

Plugins are simply another form of namespaces, therefore you should read and 
be familiar with the :ref:`namespaces-ref` section of the documentation.

The Cement Framework automatically builds plugin support into your application.
Plugins can be either internal, or external.  Internal plugins are shipped
with your application and are more or less a convenient way of maintaining
separate namespaces within your application.  External plugins are either for
third parties to build new features into your application, or perhaps for you
yourself to build extended support maybe under a different license, or in 
order to not interfere with your stable application.

Because users can override the default application configuration in their
home dir ~/.yourapp.conf, they can optionally enable/disable plugins catered 
to their actual needs of the application.  Plugins are a great way for them 
to add functionality that the system administrator might not want to enable 
globally.  In short, making all pieces of your application pluggable also
makes your application more versatile.  That said, the logic doesn't work if
any of the plugins actually rely on each other to function.

Much of the documentation references internal plugins within your application,
however it should be noted that building your application with plugins is
not necessary by any means.  If all commands and options are for the 'root'
namespace, there really isn't much need for internal plugins within your
application.  That said, as applications get more complex it is helpful to
separate controllers/models/options/commands/etc into a separate namespace
which is created by registering a plugin.


A Look at an Internal Plugin
----------------------------

An internal plugin would consist of the following files:

 * ./yourapp/controllers/yourplugin.py
 * ./yourapp/model/yourplugin.py
 * ./yourapp/templates/yourplugin/
 * ./yourapp/plugins/yourplugin.py
 * ./yourapp/etc/yourapp/plugins.d/yourplugin.conf

As you can see, plugins has the same layout as the standard application which
utilizes a Model, View, Controller design.  Lets take a look at an example 
plugin for an application called 'helloworld'.

.. code-block:: python

    import sys, os
    import logging

    from cement import namespaces
    from cement.core.log import get_logger
    from cement.core.opt import init_parser
    from cement.core.hook import define_hook, register_hook
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
                controller = 'ExampleController',
                )
        
            self.config['example_option'] = False
        
            self.options.add_option('-E', '--example', action='store',
                dest='example_option', default=None, help='Example Plugin Option'
                )

This is the example plugin, which does a number of things when it is loaded.
First, because this is an internal plugin we want it to maintain the same
VERSION, and BANNER from our main application.  The BANNER is displayed when
you execute:

.. code-block:: text

    $ helloworld example --version
    
    
In this case, 'example' is actually a namespace and not a command because the
name of the plugin/namespace is 'example'.  The 'root' namespace commands and 
options are accessible under:

.. code-block:: text

    $ helloworld --help
    
    
Your plugin's commands and options are available under either the plugins 
'example' namespace, or optionally they can also be exposed to the 'root'
namespace.  That said, commands and options that are exposed under the 
plugins 'example' namespace are available under:

.. code-block:: text
    
    $ helloworld example --help
    
Having separate namespaces allows you to keep related commands separate from
the rest of the application.  The other import piece of a plugin is the 
controller definition.  When you register a plugin, you specify the name of
the controller class as a 'string'.  The reason is because when the controller
is loaded it will most likely try to expose commands to the plugins namespace
which it can't do until the namespace is fully defined.  The @register_plugin
decorator does just that.  It first defines the namespace, and then 
instantiates the controller name to be the actual controller object.

You can optionally define configuration settings in self.config, or add
ConfigObj options to self.options.  Both are scoped only within the plugins
namespace and do not affect the 'root' or any other namespaces.
      
External Plugins
----------------

External plugins are the same as internal plugins, however they are created
outside of the main applications source.  To make this process as easy as 
possible, we created a Paster plugin allowing you to create plugins for
applications built on cement.  Therefore, if your applications name is
helloworld, the following creates an external plugin for helloworld:

.. code-block:: python

    $ paster cement-plugin helloworld myplugin
    
    $ cd helloworld-plugins-myplugin
    
    $ python setup.py develop
    

Once the plugin is installed you simply need to enable it.    

Enabling Internal/External Plugins
----------------------------------

Plugins are enabled by first installing them, and then adding the plugin
name to the *enabled_plugins* setting in your applications configuration
file.  

.. code-block:: text

    enabled_plugins = example, myplugin,
    
    
Shared Plugin Support
---------------------

Another form of plugin, is a shared plugin from another application.  For 
example, you can have a parent (company wide) application that has shared 
functionality and re-usable code.  Those plugins, from and for a completely
different application, can be loaded into your application to extend 
functionality.  

A perfect example of using shared plugins is via The Rosendale Project.  This
project is specifically geared toward building shared plugins for applications
that are built on the Cement Framework.  Where internal, and external plugins
are built specifically for your application, shared plugins are loaded from
another application.  Loading shared plugins is slightly different, but are
also added to your plugins configuration file:

.. code-block:: text

    enabled_plugins = example, myplugin, rosendale.plugins.clibasic,
    

                