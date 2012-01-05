"""Tests for cement2.ext.ext_genshi."""

from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import handler, backend, log
from cement2 import test_helper as _t

    
defaults = backend.defaults('myapp')
defaults['base']['extensions'].append('cement2.ext.ext_genshi')    
defaults['base']['output_handler'] = 'genshi'
app = _t.prep('myapp', defaults=defaults)
app.setup()    

def test_genshi():    
    app.argv = ['default']
    
    app.run()
    res = app.render(dict(foo='bar'))
    genshi_res = "foo equals bar"
    eq_(res, genshi_res)
