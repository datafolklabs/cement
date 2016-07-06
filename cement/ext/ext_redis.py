"""
The Redis Extension provides application caching and key/value store
support via Redis.

Requirements
------------

 * redis (``pip install redis``)

Configuration
-------------

This extension honors the following config settings
under a ``[cache.redis]`` section in any configuration file:

    * **expire_time** - The default time in second to expire items in the
      cache.  Default: 0 (does not expire).
    * **host** - Redis server.
    * **port** - Redis port.
    * **db** - Redis database number.


Configurations can be passed as defaults to a CementApp:

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.utils.misc import init_defaults

    defaults = init_defaults('myapp', 'cache.redis')
    defaults['cache.redis']['expire_time'] = 0
    defaults['cache.redis']['host'] = '127.0.0.1'
    defaults['cache.redis']['port'] = 6379
    defaults['cache.redis']['db'] = 0

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            config_defaults = defaults
            extensions = ['redis']
            cache_handler = 'redis'


Additionally, an application configuration file might have a section like
the following:

.. code-block:: text

    [myapp]

    # set the cache handler to use
    cache_handler = redis


    [cache.redis]

    # time in seconds that an item in the cache will expire
    expire_time = 300

    # Redis server
    host = 127.0.0.1

    # Redis port
    port = 6379

    # Redis database number
    db = 0


Usage
-----

.. code-block:: python

    from cement.core import foundation
    from cement.utils.misc import init_defaults

    defaults = init_defaults('myapp', 'redis')
    defaults['cache.redis']['expire_time'] = 300 # seconds
    defaults['cache.redis']['host'] = '127.0.0.1'
    defaults['cache.redis']['port'] = 6379
    defaults['cache.redis']['db'] = 0

    class MyApp(foundation.CementApp):
        class Meta:
            label = 'myapp'
            config_defaults = defaults
            extensions = ['redis']
            cache_handler = 'redis'

    with MyApp() as app:
        # Run the app
        app.run()

        # Set a cached value
        app.cache.set('my_key', 'my value')

        # Get a cached value
        app.cache.get('my_key')

        # Delete a cached value
        app.cache.delete('my_key')

        # Delete the entire cache
        app.cache.purge()

"""

import redis
from ..core import cache
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class RedisCacheHandler(cache.CementCacheHandler):

    """
    This class implements the :ref:`ICache <cement.core.cache>`
    interface.  It provides a caching interface using the
    `redis <http://github.com/andymccurdy/redis-py>`_ library.

    **Note** This extension has an external dependency on ``redis``.  You
    must include ``redis`` in your applications dependencies as Cement
    explicitly does *not* include external dependencies for optional
    extensions.
    """

    class Meta:

        """Handler meta-data."""

        interface = cache.ICache
        label = 'redis'
        config_defaults = dict(
            hosts='127.0.0.1',
            port=6379,
            db=0,
            expire_time=0,
        )

    def __init__(self, *args, **kw):
        super(RedisCacheHandler, self).__init__(*args, **kw)
        self.mc = None

    def _setup(self, *args, **kw):
        super(RedisCacheHandler, self)._setup(*args, **kw)
        self.r = redis.StrictRedis(
            host=self._config('host', default='127.0.0.1'),
            port=self._config('port', default=6379),
            db=self._config('db', default=0))

    def _config(self, key, default=None):
        """
        This is a simple wrapper, and is equivalent to:
        ``self.app.config.get('cache.redis', <key>)``.

        :param key: The key to get a config value from the 'cache.redis'
         config section.
        :returns: The value of the given key.

        """
        return self.app.config.get(self._meta.config_section, key)

    def get(self, key, fallback=None, **kw):
        """
        Get a value from the cache.  Additional keyword arguments are ignored.

        :param key: The key of the item in the cache to get.
        :param fallback: The value to return if the item is not found in the
         cache.
        :returns: The value of the item in the cache, or the `fallback` value.

        """
        LOG.debug("getting cache value using key '%s'" % key)
        res = self.r.get(key)
        if res is None:
            return fallback
        else:
            return res.decode('utf-8')

    def set(self, key, value, time=None, **kw):
        """
        Set a value in the cache for the given ``key``.  Additional
        keyword arguments are ignored.

        :param key: The key of the item in the cache to set.
        :param value: The value of the item to set.
        :param time: The expiration time (in seconds) to keep the item cached.
         Defaults to `expire_time` as defined in the applications
         configuration.
        :returns: ``None``

        """
        if time is None:
            time = int(self._config('expire_time'))

        if time == 0:
            self.r.set(key, value)
        else:
            self.r.setex(key, time, value)

    def delete(self, key, **kw):
        """
        Delete an item from the cache for the given ``key``.  Additional
        keyword arguments are ignored.

        :param key: The key to delete from the cache.
        :returns: ``None``

        """
        self.r.delete(key)

    def purge(self, **kw):
        """
        Purge the entire cache, all keys and values will be lost.  Any
        additional keyword arguments will be passed directly to the
        redis ``flush_all()`` function.

        :returns: ``None``

        """
        keys = self.r.keys('*')
        if keys:
            self.r.delete(*keys)


def load(app):
    app.handler.register(RedisCacheHandler)
