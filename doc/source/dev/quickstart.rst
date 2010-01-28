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

.. code-block:: console

    $ virtualenv --no-site-packages ~/devel/env/helloworld
    
    $ source ~/devel/env/helloworld/bin/activate

    (helloworld) $
    
    
Your virtual environment is now active.  Anything you install will be 
installed to this location and not system wide.  To leave the environment, run
the following:

.. code-block:: console

    (helloworld) $ deactivate
    
    $
    

Stable
^^^^^^

Stable versions of Cement can be installed from the CheezeShop via 
easy_install:

.. code-block:: console

    $ easy_install Cement
    
    
Development
^^^^^^^^^^^

Development versions of Cement can be cloned from GitHub:

.. code-block:: console

    $ git clone git://github.com/derks/cement.git
    
    $ cd cement
    
    $ python setup.py install



Creating The HelloWorld Application
-----------------------------------

Now that the Cement Framework is installed, we can create our application
from templates via PasteScript (which is installed as a dependency when you
install Cement).  You can see the Cement plugins when you access the paster
utility:

.. code-block:: console

    $ paster --help
    Usage: paster [paster_options] COMMAND [command_options]

    Options:
      --version         show program's version number and exit
      --plugin=PLUGINS  Add a plugin to the list of commands (plugins are Egg
                        specs; will also require() the Egg)
      -h, --help        Show this help message

    Commands:
      create         Create the file layout for a Python distribution
      help           Display help
      make-config    Install a package and create a fresh config file/directory
      points         Show information about entry points
      post           Run a request for the described application
      request        Run a request for the described application
      serve          Serve the described application
      setup-app      Setup an application, given a config file

    Cement:
      cement-app     Create a new CLI Application using the Cement Framework.
      cement-helper  Create a helper for an application using the Cement Framework.
      cement-plugin  Create a plugin for an application using the Cement Framework.
      

The following creates and installs a new CLI Application called HelloWorld:

.. code-block:: console

    $ paster cement-app helloworld
      
    $ cd helloworld
    
    $ python setup.py develop
    
    $ sudo ln -s `pwd`/etc/helloworld /etc/helloworld
    
    
**Note:** We symlink ./etc/helloworld to /etc proper.  This isn't required, but
you will get a warning and will not be able to read your primary configuration 
file.  Alternatively, you can copy the config to ~/.helloworld.conf which
is parsed after the global config (if you don't have root/sudo access).

Now that helloworld is installed, lets see what it looks like:

.. code-block:: console

    $ helloworld --help
    loading example plugin
    Usage:   helloworld [COMMAND] --(OPTIONS)

    Commands:  
        ex2, ex1

    
    Help?  try [COMMAND]-help

    Options:
        --version          show program's version number and exit
        -h, --help         show this help message and exit
        --json             render output as json (Cement CLI-API) [EXPERIMENTAL]
        --debug            toggle debug output
        --quiet            disable console logging
        -G, --root-option  Example root option
    
You will notice that your app is already loading an 'example' plugin.  The
included example plugin is a great starting point to learn how to build an
application on top of the Cement Framework.  The following files and 
directories should be explored:
 
 * ./helloworld/plugins/example.py
 * ./helloworld/controllers/example.py
 * ./helloworld/model/example.py
 * ./helloworld/templates/example

Once you're ready to start on a real plugin, you can remove 'example' from the 
list of 'enabled_plugins' in your applications config file 
'/etc/helloworld/helloworld.conf'.  That said, it is recommended to keep an 
example plugin included with our application, as this also provides a starting 
point for developers wanting to build external plugins for your application 
(explained later on).

The example plugin provides the 'ex1', and 'ex2' example commands, as well as
the '--root-option' which are all exposed from the example plugin, into the 
'root' namespace (more on namespaces later).

The other options are built into the Cement Framework by default, and provide
obvious functionality.

    