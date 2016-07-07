"""Tests for cement.ext.ext_redis."""

import sys
import redis
from time import sleep
from random import random
from cement.core import handler
from cement.utils import test
from cement.utils.misc import init_defaults


class RedisExtTestCase(test.CementTestCase):

    def setUp(self):
        super(RedisExtTestCase, self).setUp()
        self.key = "cement-tests-random-key-%s" % random()
        defaults = init_defaults('tests', 'cache.redis')
        defaults['cache.redis']['host'] = '127.0.0.1'
        defaults['cache.redis']['port'] = 6379
        defaults['cache.redis']['db'] = 0
        self.app = self.make_app('tests',
                                 config_defaults=defaults,
                                 extensions=['redis'],
                                 cache_handler='redis',
                                 )
        self.app.setup()

    def tearDown(self):
        super(RedisExtTestCase, self).tearDown()
        self.app.cache.delete(self.key)

    def test_redis_set(self):
        self.app.cache.set(self.key, 1001)
        self.eq(int(self.app.cache.get(self.key)), 1001)

    def test_redis_get(self):
        # get empty value
        self.app.cache.delete(self.key)
        self.eq(self.app.cache.get(self.key), None)

        # get empty value with fallback
        self.eq(self.app.cache.get(self.key, 1234), 1234)

    def test_redis_delete(self):
        self.app.cache.delete(self.key)

    def test_redis_purge(self):
        self.app.cache.set(self.key, 1002)
        self.app.cache.purge()
        self.eq(self.app.cache.get(self.key), None)

    def test_memcache_expire(self):
        self.app.cache.set(self.key, 1003, time=2)
        sleep(3)
        self.eq(self.app.cache.get(self.key), None)
