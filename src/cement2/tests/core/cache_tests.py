"""Tests for cement.core.cache."""

import unittest
from nose.tools import ok_, eq_, raises
from cement2.core import exc, cache, handler
from cement2 import test_helper as _t


class MyCacheHandler(cache.CementCacheHandler):
    class Meta:
        label = 'my_cache_handler'

class CacheTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep(cache_handler=MyCacheHandler)
    
    def test_base_handler(self):
        self.app.setup()
        count = 0
        
        try:
            self.app.cache.set('foo', 'bar')
        except NotImplementedError as e:
            count = count + 1
            
        try:
            self.app.cache.get('foo')
        except NotImplementedError as e:
            count = count + 1
        
        try:    
            self.app.cache.delete('foo')
        except NotImplementedError as e:
            count = count + 1
        
        try:    
            self.app.cache.purge()
        except NotImplementedError as e:
            count = count + 1
        
        eq_(count, 4)
            
        
        
    