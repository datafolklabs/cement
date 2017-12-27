
from cement.core.cache import CacheHandlerBase, CacheHandler


### module tests

class TestCacheHandlerBase(object):
    def test_interface(self):
        assert CacheHandlerBase.Meta.interface == 'cache'


class TestCacheHandler(object):
    def test_subclassing(self):
        class MyCacheHandler(CacheHandler):
            class Meta:
                label = 'my_cache_handler'

            def get(self, *args, **kw):
                pass

            def set(self, *args, **kw):
                pass

            def delete(self, *args, **kw):
                pass

            def purge(self, *args, **kw):
                pass

        h = MyCacheHandler()
        assert h._meta.interface == 'cache'
        assert h._meta.label == 'my_cache_handler'

### app functionality and coverage tests
