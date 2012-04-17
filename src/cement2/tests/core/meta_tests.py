"""Cement2 meta tests."""

import unittest
from nose.tools import eq_, raises
from cement2.core import backend, exc, meta
from cement2 import test_helper as _t

class TestMeta(meta.MetaMixin):
    class Meta:
        option_one = 'value one'
        option_two = 'value two'
    
    def __init__(self, **kw):
        super(TestMeta, self).__init__(**kw)
        self.option_three = kw.get('option_three', None)
        
class MetaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep()
        
    def test_passed_kwargs(self):
        t = TestMeta(option_two='some other value', option_three='value three')
        eq_(t._meta.option_one, 'value one')
        eq_(t._meta.option_two, 'some other value')
        eq_(hasattr(t._meta, 'option_three'), False)
        eq_(t.option_three, 'value three')
    
    