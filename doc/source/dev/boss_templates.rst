.. _boss:

Starting Projects from Boss Templates
=====================================

`The Boss Project <https://boss.readthedocs.io>`_ provides 'Baseline Open Source
Software' templates and development tools. It has similarities to PasteScript
with regards to templating, but far easier to extend.  The official template
repository includes a number of templates specifically for Cement, and are the
recommended means of start Cement based projects.

This is just a quick overview of creating Cement Apps, Plugins, and Extensions
with Boss.

Creating a Cement App
---------------------

.. code-block:: text

    $ boss create ./myapp -t boss:cement-app

    $ cd myapp

    $ virtualenv /path/to/myapp/env

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


Add the following to ``~/myapp.conf`` (or whereever your config file is):

.. code-block:: text

    [myapp]
    plugin_config_dir = /path/to/myapp/config/plugins.d
    plugin_dir = /path/to/myapp/plugins

    # Enable the plugin here, or in a plugins.d/myplugin.conf
    [myplugin]
    enable_plugin = 1


And it should be enabled when you run your app (though it doesn't do anything
out of the box).


Creating a Cement Extension
---------------------------

3rd party extensions are generally created within the app they are being
built with, but do not have to be.  In this case we are adding the extension
to an existing Cement project:

.. code-block:: text

    $ boss create ./myapp -t boss:cement-ext


At this point you would enable the extension in your app to utilize it.
