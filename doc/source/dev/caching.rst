Caching
=======

Cement defines a cache interface called :ref:`ICache <cement.core.cache>`,
but does not implement caching by default.  The documentation below references
usage based on the interface and not the full capabilities of any given
implementation.

The following cache handlers are included and maintained with Cement:

    * :ref:`MemcachedCacheHandler <cement.ext.ext_memcached>`


Please reference the :ref:`ICache <cement.core.cache>` interface
documentation for writing your own cache handler.

General Usage
-------------

For this example we use the Memcached extension, which requires the
``pylibmc`` library to be installed, as well as a Memcached server running on
localhost.

Example:

**/path/to/myapp.conf**

.. code-block:: text

    [myapp]
    extensions = memcached

    [cache.memcached]
    # comma separated list of hosts to use
    hosts = 127.0.0.1

    # time in milliseconds
    expire_time = 300

**myapp.py**

.. code-block:: python

    from cement.core.foundation import CementApp

    with CementApp('myapp') as app:
        # run the application
        app.run()

        # set a cached value
        app.cache.set('my_key', 'my value')

        # get a cached value
        app.cache.get('my_key')

        # delete a cached value
        app.cache.delete('my_key')

        # delete the entire cache
        app.cache.purge()

