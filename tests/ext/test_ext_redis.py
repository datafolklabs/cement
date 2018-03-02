
import os
from time import sleep
from cement.utils.test import TestApp
from cement.utils.misc import init_defaults


if 'REDIS_HOST' in os.environ.keys():
    redis_host = os.environ['REDIS_HOST']
else:
    redis_host = 'localhost'


defaults = init_defaults('cache.redis')
defaults['cache.redis']['host'] = redis_host
defaults['cache.redis']['port'] = 6379
defaults['cache.redis']['db'] = 0


class RedisApp(TestApp):
    class Meta:
        extensions = ['redis']
        cache_handler = 'redis'
        config_defaults = defaults


def test_redis_set(key):
    with RedisApp() as app:
        app.cache.set(key, 1001)
        assert int(app.cache.get(key)) == 1001


def test_redis_get(key):
    with RedisApp() as app:
        # get empty value
        app.cache.delete(key)
        assert app.cache.get(key) is None

        # get empty value with fallback
        assert app.cache.get(key, 1234) == 1234


def test_redis_delete(key):
    with RedisApp() as app:
        app.cache.set(key, 1001)
        assert int(app.cache.get(key)) == 1001
        app.cache.delete(key)
        assert app.cache.get(key) is None


def test_redis_purge(key):
    with RedisApp() as app:
        app.cache.set(key, 1002)
        app.cache.purge()
        assert app.cache.get(key) is None


def test_redis_expire(key):
    with RedisApp() as app:
        app.cache.set(key, 1003, time=2)
        sleep(3)
        assert app.cache.get(key) is None
