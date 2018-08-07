import os
from time import sleep
from cement.utils.test import TestApp
from cement.utils.misc import init_defaults

if 'MEMCACHED_HOST' in os.environ.keys():
    memcached_host = os.environ['MEMCACHED_HOST']
else:
    memcached_host = 'localhost'


defaults = init_defaults('cache.memcached')
defaults['cache.memcached']['hosts'] = [
    memcached_host,
    memcached_host
]


class MemcachedApp(TestApp):
    class Meta:
        extensions = ['memcached']
        cache_handler = 'memcached'
        config_defaults = defaults


def test_memcache_list_type_config():
    with MemcachedApp() as app:
        assert app.config.get('cache.memcached', 'hosts') == \
            [memcached_host, memcached_host]


def test_memcache_str_type_config():
    defaults = init_defaults('tests', 'cache.memcached')
    defaults['cache.memcached']['hosts'] = "%s,%s" % (memcached_host,
                                                      memcached_host)
    with MemcachedApp(config_defaults=defaults) as app:
        assert app.config.get('cache.memcached', 'hosts') == \
            [memcached_host, memcached_host]


def test_memcached_set(key):
    with MemcachedApp() as app:
        app.cache.set(key, 1001)
        assert app.cache.get(key) == 1001
        app.cache.delete(key)


def test_memcached_get(key):
    with MemcachedApp() as app:
        # get empty value
        app.cache.delete(key)
        assert app.cache.get(key) is None

        # get empty value with fallback
        assert app.cache.get(key, 1234) == 1234


def test_memcached_delete(key):
    with MemcachedApp() as app:
        # When deleting a key that doesn't exist
        app.cache.delete(key)

        # When deleting a key that does exist
        app.cache.set(key, 4321)
        app.cache.delete(key)
        assert app.cache.get(key) is None


def test_memcached_purge(key):
    with MemcachedApp() as app:
        app.cache.set(key, 1002)
        app.cache.purge()
        assert app.cache.get(key) is None


def test_memcache_expire(key):
    with MemcachedApp() as app:
        app.cache.set(key, 1003, time=2)
        sleep(3)
        assert app.cache.get(key) is None
