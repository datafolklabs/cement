"""Tests for cement.core.cache."""

from cement.core import exc, cache
from cement.utils import test


class MyCacheHandler(cache.CementCacheHandler):

    class Meta:
        label = 'my_cache_handler'

    def get(self, key, fallback=None):
        pass

    def set(self, key, value):
        pass

    def delete(self, key):
        pass

    def purge(self):
        pass


@test.attr('core')
class CacheTestCase(test.CementCoreTestCase):

    def setUp(self):
        super(CacheTestCase, self).setUp()
        self.app = self.make_app(cache_handler=MyCacheHandler)

    def test_base_handler(self):
        self.app.setup()
        self.app.cache.set('foo', 'bar')
        self.app.cache.get('foo')
        self.app.cache.delete('foo')
        self.app.cache.purge()
