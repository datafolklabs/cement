Quick Starting a New CLI Application
====================================

The following outlines how to create a new application built on The Cement
CLI Application Framework.  Throughout this documentation we reference an
application called 'helloworld'.  For almost all cases, you can replace
helloworld with the package name of your application.

    
Raw Commands For The Impatient
------------------------------

This is for development.  Please note that in production you will likely be
installing system wide (with root access), and that you only need 'cement' in
production (not cement.devtools).

.. code-block:: text

    ### install
    
    $ virtualenv --no-site-packages ~/env/helloworld
    
    $ source ~/env/helloworld/bin/activate
    
    $ easy_install cement.devtools
    
    
    ### create app
    
    $ paster cement-app helloworld
    
    $ cd helloworld
    
    $ python setup.py develop
    
    
    ### setup local (user) config
    
    $ cp -a ./etc/helloworld.conf-dev ~/.helloworld.conf
    
    $ vi ~/.helloworld.conf
    
    $ helloworld --help
    
    
    ### create an external plugin
    
    $ mkdir plugins
    
    $ cd plugins
    
    $ paster cement-plugin helloworld myplugin
    
    $ cd helloworld.myplugin
    
    $ python setup.py develop
    
    $ cp -a ./etc/plugins.d/myplugin.conf ~/path/to/plugin_config_dir
    
    $ helloworld --help
    
    
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
easy_install (devtools installs cement as a dependency):

.. code-block:: text

    $ easy_install cement.devtools
    
    
Development
^^^^^^^^^^^

Development versions of Cement can be cloned from GitHub:

.. code-block:: text

    $ git clone git://github.com/derks/cement.git
    
    # install cement core framework
    $ cd cement/src/cement
    $ python setup.py install
    
    # install devtools
    $ cd ../cement.devtools
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
called HelloWorld, and copies a 'development' config file to your home 
directory path.  Note that the -dev config is geared towards 'local' file
paths for your user where as the other config is geared towards a system wide
production install:

.. code-block:: text

    $ paster cement-app helloworld
      
    $ cd helloworld
    
    $ python setup.py develop
    
    $ cp -a etc/helloworld.conf-dev ~/.helloworld.conf
    
    
**Note:** You need to look at ~/.helloworld.conf and edit any settings.  For
most cases, the only thing you might want to edit is the 'plugin_config_dir' 
path to point it to '/path/to/helloworld/etc/plugins.d'.  Your application by 
default searches for configs in the following order:

    * /etc/helloworld/helloworld.conf
    * ~/.helloworld/etc/helloworld.conf
    * ~/.helloworld.conf 

The second is a hard set location based on the 'prefix' in your applications
'helloworld/core/config.py' and is not often relied on.  Now that helloworld 
is installed, lets see what it looks like:

.. code-block:: text

    $ helloworld --help
    loading example plugin
    Usage:   helloworld [COMMAND] --(OPTIONS)

    Commands:  
        get-started, cmd1, cmd2, example*

    
    Help?  try [COMMAND]-help

    Options:
        --version          show program's version number and exit
        -h, --help         show this help message and exit
        -R, --root-option  Example root option
        --json             render output as json (Cement CLI-API)
        --debug            toggle debug output
        --quiet            disable console logging
    

Go ahead and run the get-started command:

.. code-block:: text

    $ helloworld get-started


It is more or less the same information you are reading here, however it is
also a functional command that is rendered by Genshi and a template.  We've 
put it there to show how commands are created and rendered.  Go ahead and
take a look at the following files to see where and how that command is setup:

    * helloworld/controllers/root.py
    * helloworld/templates/root/get-started.txt
    
    
You will also notice that your app is already loading an 'example' plugin.  
Plugins are enabled under their [plugin] config either in your main 
application configuration file, or in the plugins.d/<plugin_name>.conf file for 
that plugin.  An example plugin config looks like:

.. code-block:: text

    [example]
    enable_plugin = true
    provider = helloworld


The 'provider' is the package that provides it and can be omitted for plugins
that are a part of your application.  However, you can load plugins from any
other application that is built on Cement by adding them as the provider.  
The plugin has to be written in a 'generic' fashion of course.  For more 
information on shared plugins check our The Rosendale Project which provides
plugins explicitly for re-usability in other applications built on Cement.  

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

.. code-block:: python
    
    from helloworld.bootstrap import example
    
    
All modules imported into the root bootstrap become a part of the application 
permanently (meaning its not loaded as an optional plugin).  You then want to
move the plugins configuration from a separate plugin config to your primary
applications configuration and remove 'enable_plugin' setting.

Once you're ready to start coding, you can disable the 'example' plugin by
setting 'enable_plugin=false' in plugins.d/example.conf. That said, it is 
recommended to keep the example plugin included with our application, as this 
also provides a starting point for developers wanting to build external plugins 
for your application (explained later on).

By default, the base application has a command named 'cmd1' created in the
controller and the options -R/--root-option, --debug, --quiet, --json which
are created in the bootstrap file.  You can remove these from the bootstrap
file so that they don't show up under '--help', however please note that
--debug, --quiet, and --json are hard coded in the Cement framework and will
still function if the user passes them at command line.

The example plugin provides the 'example*' namespace, which has two commands
under it called 'ex1', and 'ex2' created in the controller, as well as the 
'-F/--foo' option created in the bootstrap file.  The controller also exposes 
a root command called 'cmd2'.
