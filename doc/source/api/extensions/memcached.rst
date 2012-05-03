Memcached
=========

The Memcached Framework Extension enables applications built on cement to 
easily utilize a Memcached caching backend.

Configuration
-------------

The Memcached extension is configurable with the following config settings 
under the [cache.memcached] section of the application configuration.

    expire_time
        The default time in second to expire items in the cache.  The default
        value is 0 (does not expire).
        
    hosts
        List of Memcached servers.
    
The configurations can be passed as defaults:

.. code-block:: python
    
    from cement2.core import foundation, backend
    
    defaults = backend.defaults('myapp', 'cache.memcached')
    defaults['cache.memcached']['expire_time'] = 0
    defaults['cache.memcached']['hosts'] = ['127.0.0.1']
    
    app = foundation.CementApp('myapp', config_defaults=defaults)
    

Additionally, an application configuration file might have a section like the
following:

.. code-block:: text

    [cache.memcached]
    expire_time = 3600
    
    # comma seperated list of memcached servers
    hosts = 127.0.0.1, cache.example.com
        
Example Usage
-------------

.. code-block:: python
    
    from cement2.core import foundation

    try:    
        app = foundation.CementApp('myapp', extensions=['memcached'])
        app.setup()
        app.run()
        
        # Set a cached value
        app.cache.set('my_key', 'my value')
        
        # Get a cached value
        app.cache.get('my_key')
        
        # Delete a cached value
        app.cache.delete('my_key')
        
        # Delete the entire cache
        app.cache.purge()

    finally:
        app.close()


API Reference
-------------

.. _cement2.ext.ext_memcached:

:mod:`cement2.ext.ext_memcached`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: cement2.ext.ext_memcached
    :members:
    
.. _cement2.lib.ext_memcached:

:mod:`cement2.lib.ext_memcached`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: cement2.lib.ext_memcached
    :members:
    


