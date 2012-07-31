Starting Projects from Boss Templates
=====================================

The `Boss Project <http://boss.rtfd.org>`_ provides 'Baseline Open Source 
Software' templates and development tools. It has similarities to PasteScript 
with regards to templating, but far easier to extend.  The official template 
repository includes a number of templates specifically for Cement.

This is just a quick overview of creating Cement Apps, Plugins, and Extensions
with Boss.

Creating a Cement App
---------------------

.. code-block:: text

    $ boss create ./myapp -t boss:cement-app
    
    $ cd myapp
    
    $ virtualenv --no-site-packages /path/to/myapp/env
    
    $ source /path/to/myapp/env/bin/activate
    
    $ pip install -r requirements.txt
    
    $ python setup.py develop
    
    $ myapp --help

    $ pip install nose coverage
    
    $ python setup.py nosetests
    

Creating a Cement Plugin
------------------------

.. code-block:: text

    $ source /path/to/myapp/env/bin/activate
    
    $ cd /path/to/myapp
    
    $ mkdir plugins
    
    $ boss create ./plugins/myplugin -t boss:cement-plugin
    
    $ cd plugins
    
Add the following to ~/myapp.conf (or whereever your config file is):

.. code-block:: text

    [myapp]
    plugin_dir = /path/to/myapp/plugins
    
    [myplugin]
    enable_plugin = 1
    
And it should be enabled when you run your app (though it doesn't do anything
out of the box).


Creating a Cement Extension
---------------------------

.. code-block:: text

    $ virtualenv --no-site-packages /path/to/cement.ext.myext
    
    $ source /path/to/cement.ext.myext/env/bin/activate
        
    $ boss create ./cement.ext.myext -t boss:cement-ext
    
    $ cd ./cement.ext.myext 
    
    $ pip install -r requirements.txt
    
    $ python setup.py develop
    
At this point you would enable the extension in your app to utilize it.