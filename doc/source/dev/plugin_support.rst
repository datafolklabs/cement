Plugin Support
==============

Plugins are made possible by namespaces, therefore you should read and 
be familiar with the Namespaces section of the documentation.  There
is no difference between internal controller/model/bootstrap/etc code and 
plugin code.  The difference is that plugins are optional and only loaded if
'enable_plugin=true' in the plugins configuration.  Internal code is 
bootstrapped and imported directly by 'helloworld/bootstrap/root.py' so that
it is always loaded by your application.  

The Cement Framework automatically builds plugin support into your application.
Plugins can be either internal, or external.  Internal plugins are shipped
with your application and are more or less a convenient way of maintaining
optional code within your application.  External plugins are either for
third parties to build new features into your application, or perhaps for you
yourself to build extended support maybe under a different license, or in 
order to not interfere with your stable application.

Because users can override the default application configuration in their
home dir ~/.yourapp.conf, they can optionally enable/disable plugins catered 
to their actual needs of the application.  Plugins are a great way for them 
to add functionality that the system administrator might not want to enable 
globally.


A Look at an Internal Plugin
----------------------------

An internal plugin would consist of the following files:

    * ./yourapp/bootstrap/yourplugin.py
    * ./yourapp/controllers/yourplugin.py
    * ./yourapp/model/yourplugin.py
    * ./yourapp/templates/yourplugin/
    * ./yourapp/etc/yourapp/plugins.d/yourplugin.conf

As you can see, plugins have the same layout as the standard application which
utilizes a Model, View, Controller design as well as a bootstrap file.  For 
that reason we aren't going to cover much in this section because the plugin
code is exactly the same as your application.  The only difference is that
you do not import the plugin's 'bootstrap' file into the root bootstrap like
you do with the rest of your application, but rather enable the plugin in the
yourplugin.conf within plugins.d.

      
External Plugins
----------------

External plugins are the same as internal plugins, however they are created
outside of the main applications source tree.  To make this process as easy as 
possible, we created a Paster plugin allowing you to create plugins for
applications built on cement.  Therefore, if your applications name is
helloworld, the following creates an external plugin for helloworld:

.. code-block:: python

    $ paster cement-plugin helloworld myplugin
    
    $ cd helloworld-plugins-myplugin
    
    $ python setup.py develop
    

Once the plugin is installed you simply need to enable it.  An external plugin
functions by way of pkg_resources and shared library paths.  Meaning, even
though the code is outside the main applications source tree the code is still
installed under the applications library path in site-packages.  Take a look
at the files created by Paster and you will see that the tree is almost
the exact same as the main applications source tree.
    

Enabling Internal/External Plugins
----------------------------------

Plugins are enabled by first installing them, and then creating a plugin.conf
within your applications plugins.d directory (set by plugin_config_dir).
Plugin code is only loaded when 'enable_plugin=yes'.

**/etc/yourapp/plugins.d/yourplugin.conf**    
    
.. code-block:: text

    [yourplugin]
    enable_plugin = true
    some_option = some value
    foo = bar

    
    
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
another application.

Using the 'clibasic' plugin from The Rosendale Project as an example, the 
following outlines how to load it as part of your application.

**/etc/yourapp/plugins.d/clibasic.conf**    
    
.. code-block:: text

    [clibasic]
    enable_plugin = true
    provider = rosendale
    

The plugin will be loaded from the rosendale namespace, but will function as
if it were built specifically for your application.  Yes, we know... this is
pretty awesome... you're right.
