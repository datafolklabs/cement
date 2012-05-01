Cache Handling
==============

Cement defines a cache interface called :ref:`ICache <cement2.core.cache>`, 
but does not implement caching by default.  The documentation below references 
usage based on the interface and not the full capabilities of any given 
implementation.

The following output handlers are included and maintained with Cement2:

    * :ref:`MemcachedCacheHandler <cement2.ext.ext_memcached>`

Please reference the :ref:`ICache <cement2.core.cache>` interface 
documentation for writing your own cache handler.

General Usage
-------------

For this example we use the Memcached extension.  This requires the pylibmc 
library to be installed, as well as a Memcached server running on localhost.

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