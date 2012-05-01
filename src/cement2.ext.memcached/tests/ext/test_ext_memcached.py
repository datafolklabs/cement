"""Tests for cement2.ext.ext_memcached."""

import pylibmc
import unittest
from time import sleep
from random import random
from nose.tools import eq_, raises
from cement2.core import handler
from cement2 import test_helper as _t

_t.prep()
from cement2.ext import ext_memcached

def import_memcached():
    from cement2.ext import ext_memcached
    handler.register(ext_memcached.MemcachedCacheHandler)
    
class MemcachedExtTestCase(unittest.TestCase):
    def setUp(self):
        self.key = "cement2-tests-random-key-%s" % random()
        self.app = _t.prep('tests', 
            extensions=['memcached'],
            cache_handler='memcached',
            )
        import_memcached()
        self.app.setup()
        
    def tearDown(self):
        self.app.cache.delete(self.key)
        
    def test_memcached_set(self):    
        self.app.cache.set(self.key, 1001)
        eq_(self.app.cache.get(self.key), 1001)
        
    def test_memcached_get(self):
        # get empty value
        self.app.cache.delete(self.key)
        eq_(self.app.cache.get(self.key), None)
        
        # get empty value with fallback
        eq_(self.app.cache.get(self.key, 1234), 1234)
        
    def test_memcached_delete(self):
        self.app.cache.delete(self.key)
        
    def test_memcached_purge(self):
        self.app.cache.set(self.key, 1002)
        self.app.cache.purge()
        eq_(self.app.cache.get(self.key), None)
        
    def test_memcache_expire(self):
        self.app.cache.set(self.key, 1003, time=2)
        sleep(3)
        eq_(self.app.cache.get(self.key), None)
        