"""
The module handles the integration with PasteScript enabling the following
plugins to the 'paste' command line utility:

    cement-app
        Generates a base application built on Cement.
        
    cement-plugin
        Generates an external plugin for an application built on Cement.
        
    cement-helper
        Generates an external helper for an application built on Cement.
        
Usage:

.. code-block::

    $ paster cement-app helloworld
    
    $ paster cement-plugin helloworld myplugin
    
    $ paster cement-helper helloworld myhelper
    
"""
__import__('pkg_resources').declare_namespace(__name__)