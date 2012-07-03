Cache Handling
==============

Cement defines a cache interface called :ref:`ICache <cement.core.cache>`, 
but does not implement caching by default.  The documentation below references 
usage based on the interface and not the full capabilities of any given 
implementation.

The following output handlers are included and maintained with Cement:

    * None

Please reference the :ref:`ICache <cement.core.cache>` interface 
documentation for writing your own cache handler.

General Usage
-------------

For this example we use the Memcached extension.  This requires the pylibmc 
library to be installed, as well as a Memcached server running on localhost.
You can find more information on this extension here:

    * http://github.com/cement/cement.ext.memcache
    
Example:

.. code-block:: python

    from cement.core import foundation

    app = foundation.CementApp('myapp', extensions=['memcached'])
    
    try:        
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
