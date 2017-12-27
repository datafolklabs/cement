
from cement.core.meta import Meta, MetaMixin

class TestMeta(object):
    def test_meta(self):
        m = Meta(key='value')
        assert hasattr(m, 'key')
        assert m.key == 'value'


class TestMetaMixin(object):
    def test_metamixin(self):
        class SomeClass(MetaMixin):
            class Meta:
                k1 = 'v1'
                k2 = 'v2'

        sc = SomeClass(k2='not-v2')
        assert hasattr(sc, '_meta')
        assert sc._meta.k1 == 'v1'
        assert sc._meta.k2 == 'not-v2'
