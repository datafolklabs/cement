Quick Starting a New CLI Application
====================================

The following outlines how to create a new application built on The Cement
CLI Application Framework.


Installing Cement
-----------------

This section outlines how to install Cement.  By preference, we do so by way
of installing to a virtualenv.  This is not necessary if you have root access
on your system and want to install system wide.  That said, for development
purposes (i.e. building your application) you should be working out of a 
virtualenv.

Before installing Cement, setup your virtual environment:

.. code-block:: text

    $ virtualenv --no-site-packages ~/devel/env/helloworld
    
    $ source ~/devel/env/helloworld/bin/activate

    (helloworld) $
    
    
Your virtual environment is now active.  Anything you install will be 
installed to this location and not system wide.  To leave the environment, run
the following:

.. code-block:: text

    (helloworld) $ deactivate
    
    $
    

Stable
^^^^^^

Stable versions of Cement can be installed from the CheezeShop via 
easy_install:

.. code-block:: text

    $ easy_install Cement
    
    
Development
^^^^^^^^^^^

Development versions of Cement can be cloned from GitHub:

.. code-block:: text

    $ git clone git://github.com/derks/cement.git
    
    $ cd cement
    
    $ python setup.py install


The 'master' branch tracks development that is compatible with the stable
API.  However, development on the next major version which will break API
compatibility is tracked in the 'portland' branch.  The portland branch
can be checkout by:

.. code-block:: text

    $ git checkout --track -b portland origin/portland
    

Creating The HelloWorld Application
-----------------------------------

Now that the Cement Framework is installed, we can create our application
from templates via PasteScript (which is installed as a dependency when you
install Cement).  The following creates and installs a new CLI Application 
called HelloWorld:

.. code-block:: text

    $ paster cement-app helloworld
      
    $ cd helloworld
    
    $ python setup.py develop
    
    $ cp -a etc/helloworld.conf-dev ~/.helloworld.conf
    
    
**Note:** You need to look at ~/.helloworld.conf and edit any settings.  For
most cases, the only thing you might want to edit is the 'plugin_config_dir' 
path to point it to '/path/to/helloworld/etc/plugins.d'.  Note that your 
application by default searches for '/etc/helloworld/helloworld.conf' as well 
as '~/.helloworld.conf'.  

Now that helloworld is installed, lets see what it looks like:

.. code-block:: text

    $ helloworld --help
    loading example plugin
    Usage:   helloworld [COMMAND] --(OPTIONS)

    Commands:  
        cmd1, cmd2, example*

    
    Help?  try [COMMAND]-help

    Options:
        --version          show program's version number and exit
        -h, --help         show this help message and exit
        -R, --root-option  Example root option
        --json             render output as json (Cement CLI-API)
        --debug            toggle debug output
        --quiet            disable console logging
    

You will notice that your app is already loading an 'example' plugin.  Plugins
are enabled in a number of ways, but most generally by adding the plugin name 
to 'enabled_plugins' in your applications configuration, or by setting 
'enable_plugin=true' in each plugin's configuration (in the plugin_config_dir
plugins.d/plugin_name.conf) under '[plugin_name]'.

The included example plugin is a great starting point to learn how to build an
application on top of the Cement Framework.  The following files and 
directories should be explored:
 
 * ./helloworld/bootstrap/example.py
 * ./helloworld/controllers/example.py
 * ./helloworld/model/example.py
 * ./helloworld/templates/example/

It should be noted that the only difference between a plugin, and a built in
part of your application is that a plugin is optional, and only loaded if 
enabled via the configuration.  You can make the example plugin part of your 
application by adding the following to 'helloworld/bootstrap/root.py'

..code-block:: python
    
    from helloworld.bootstrap import example
    
    
All modules imported into the root bootstrap become a part of the application 
permanently (meaning its not loaded as an optional plugin).

Once you're ready to start coding, you can remove 'example' from the 
list of 'enabled_plugins' in your applications config. That said, it is 
recommended to keep the example plugin included with our application, as this 
also provides a starting point for developers wanting to build external plugins 
for your application (explained later on).

By default, the base application has a command named 'cmd1' created in the
controller and the options -R/--root-option, --debug, --quiet, --json which
are created in the bootstrap file.

The example plugin provides the 'example*' namespace, which has two commands
under it called 'ex1', and 'ex2' created in the controller, as well as the 
'-F/--foo' option created in the bootstrap file.  The controller also exposes 
a root command called 'cmd2'.
