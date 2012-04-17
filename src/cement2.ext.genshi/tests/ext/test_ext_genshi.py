"""Tests for cement2.ext.ext_genshi."""

import sys
import random
import unittest
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, foundation, handler, backend, controller
from cement2 import test_helper as _t

if sys.version_info[0] >= 3:
    raise SkipTest('Genshi does not support Python 3') # pragma: no cover
    
app = _t.prep()
from cement2.ext import ext_genshi

def import_genshi():
    from cement2.ext import ext_genshi
    handler.register(ext_genshi.GenshiOutputHandler)
    
class GenshiExtTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep('tests', 
            extensions=['genshi'],
            output_handler='genshi',
            argv=[]
            )
        import_genshi()
        
    def test_genshi(self):    
        self.app.setup()
        rando = random.random()
        res = self.app.render(dict(foo=rando), 'test_template.txt')
        genshi_res = "foo equals %s" % rando
        eq_(res, genshi_res)

    def test_genshi_bad_template(self):    
        self.app.setup()
        res = self.app.render(dict(foo='bar'), 'bad_template.txt')

    @raises(IOError)
    def test_genshi_nonexistent_template(self):    
        self.app.setup()
        res = self.app.render(dict(foo='bar'), 'missing_template.txt')
    
    @raises(exc.CementRuntimeError)
    def test_genshi_none_template(self):    
        self.app.setup()
        try:
            res = self.app.render(dict(foo='bar'), None)
        except exc.CementRuntimeError as e:
            eq_(e.msg, "Invalid template 'None'.")
            raise

    @raises(exc.CementRuntimeError)
    def test_genshi_bad_module(self):
        self.app.setup()
        self.app.output._meta.template_module = 'this_is_a_bogus_module'
        res = self.app.render(dict(foo='bar'), 'bad_template.txt')