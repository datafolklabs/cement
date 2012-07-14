"""Tests for cement.core.cache."""

from cement.core import exc, cache, handler
from cement.utils import test

class MyCacheHandler(cache.CementCacheHandler):
    class Meta:
        label = 'my_cache_handler'

class CacheTestCase(test.CementTestCase):
    def setUp(self):
        super(CacheTestCase, self).setUp()
        self.app = self.make_app(cache_handler=MyCacheHandler)
    
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
        
        self.eq(count, 4)
            
        
        
    
