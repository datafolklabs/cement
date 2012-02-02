"""Cement2 meta tests."""

from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import backend, exc, meta
from cement2 import test_helper as _t
_t.prep()

class TestMeta(meta.MetaMixin):
    class Meta:
        option_one = 'value one'
        option_two = 'value two'
    
    def __init__(self, **kw):
        super(TestMeta, self).__init__(**kw)
        self.option_three = kw.get('option_three', None)
        
def test_passed_kwargs():
    t = TestMeta(option_two='some other value', option_three='value three')
    eq_(t._meta.option_one, 'value one')
    eq_(t._meta.option_two, 'some other value')
    eq_(hasattr(t._meta, 'option_three'), False)
    eq_(t.option_three, 'value three')
    
    