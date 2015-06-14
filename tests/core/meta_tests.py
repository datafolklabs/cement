"""Cement meta tests."""

from cement.core import backend, exc, meta
from cement.utils import test


class TestMeta(meta.MetaMixin):

    class Meta:
        option_one = 'value one'
        option_two = 'value two'

    def __init__(self, **kw):
        super(TestMeta, self).__init__(**kw)
        self.option_three = kw.get('option_three', None)


class MetaTestCase(test.CementCoreTestCase):

    def test_passed_kwargs(self):
        t = TestMeta(option_two='some other value', option_three='value three')
        self.eq(t._meta.option_one, 'value one')
        self.eq(t._meta.option_two, 'some other value')
        self.eq(hasattr(t._meta, 'option_three'), False)
        self.eq(t.option_three, 'value three')
