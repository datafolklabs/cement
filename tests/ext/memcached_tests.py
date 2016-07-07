"""Tests for cement.ext.ext_memcached."""

import sys
import pylibmc
from time import sleep
from random import random
from cement.core import handler
from cement.utils import test
from cement.utils.misc import init_defaults


class MemcachedExtTestCase(test.CementTestCase):

    def setUp(self):
        super(MemcachedExtTestCase, self).setUp()
        self.key = "cement-tests-random-key-%s" % random()
        defaults = init_defaults('tests', 'cache.memcached')
        defaults['cache.memcached']['hosts'] = '127.0.0.1, localhost'
        self.app = self.make_app('tests',
                                 config_defaults=defaults,
                                 extensions=['memcached'],
                                 cache_handler='memcached',
                                 )
        self.app.setup()

    def tearDown(self):
        super(MemcachedExtTestCase, self).tearDown()
        self.app.cache.delete(self.key)

    def test_memcache_list_type_config(self):
        defaults = init_defaults('tests', 'cache.memcached')
        defaults['cache.memcached']['hosts'] = ['127.0.0.1', 'localhost']
        self.app = self.make_app('tests',
                                 config_defaults=defaults,
                                 extensions=['memcached'],
                                 cache_handler='memcached',
                                 )
        self.app.setup()
        self.eq(self.app.config.get('cache.memcached', 'hosts'),
                ['127.0.0.1', 'localhost'])

    def test_memcache_str_type_config(self):
        defaults = init_defaults('tests', 'cache.memcached')
        defaults['cache.memcached']['hosts'] = '127.0.0.1, localhost'
        self.app = self.make_app('tests',
                                 config_defaults=defaults,
                                 extensions=['memcached'],
                                 cache_handler='memcached',
                                 )
        self.app.setup()
        self.eq(self.app.config.get('cache.memcached', 'hosts'),
                ['127.0.0.1', 'localhost'])

    def test_memcached_set(self):
        self.app.cache.set(self.key, 1001)
        self.eq(self.app.cache.get(self.key), 1001)

    def test_memcached_get(self):
        # get empty value
        self.app.cache.delete(self.key)
        self.eq(self.app.cache.get(self.key), None)

        # get empty value with fallback
        self.eq(self.app.cache.get(self.key, 1234), 1234)

    def test_memcached_delete(self):
        self.app.cache.delete(self.key)

    def test_memcached_purge(self):
        self.app.cache.set(self.key, 1002)
        self.app.cache.purge()
        self.eq(self.app.cache.get(self.key), None)

    def test_memcache_expire(self):
        self.app.cache.set(self.key, 1003, time=2)
        sleep(3)
        self.eq(self.app.cache.get(self.key), None)
