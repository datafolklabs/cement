"""
Cement redis extension module.
"""

import redis
from ..core import cache
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class RedisCacheHandler(cache.CacheHandler):

    """
    This class implements the :ref:`Cache <cement.core.cache>` Handler
    interface.  It provides a caching interface using the
    `redis <http://github.com/andymccurdy/redis-py>`_ library.

    **Note** This extension has an external dependency on ``redis``.  You
    must include ``redis`` in your applications dependencies as Cement
    explicitly does *not* include external dependencies for optional
    extensions.
    """

    class Meta:

        """Handler meta-data."""

        label = 'redis'
        config_defaults = dict(
            host='127.0.0.1',
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

        Args:
            key (str): The key to get a config value from the ``cache.redis``
                config section.

        Returns:
            unknown: The value of the given key.

        """
        return self.app.config.get(self._meta.config_section, key)

    def get(self, key, fallback=None, **kw):
        """
        Get a value from the cache.  Additional keyword arguments are ignored.

        Args:
            key (str): The key of the item in the cache to get.

        Keyword Args:
            fallback: The value to return if the item is not found in the
                cache.

        Returns:
            unknown: The value of the item in the cache, or the ``fallback``
            value.

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

        Args:
            key (str): The key of the item in the cache to set.
            value: The value of the item to set.
            time (int): The expiration time (in seconds) to keep the item
                cached. Defaults to ``expire_time`` as defined in the
                applications configuration.

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

        Args:
            key (str): The key to delete from the cache.

        """
        self.r.delete(key)

    def purge(self, **kw):
        """
        Purge the entire cache, all keys and values will be lost.  Any
        additional keyword arguments will be passed directly to the
        redis ``flush_all()`` function.

        """
        keys = self.r.keys('*')
        if keys:
            self.r.delete(*keys)


def load(app):
    app.handler.register(RedisCacheHandler)
