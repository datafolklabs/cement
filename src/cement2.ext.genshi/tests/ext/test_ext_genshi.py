"""Tests for cement2.ext.ext_genshi."""

import sys
import random
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, foundation, handler, backend, controller
from cement2 import test_helper as _t

if sys.version_info[0] >= 3:
    raise SkipTest('Genshi does not support Python 3') # pragma: no cover
    
# create the application
defaults = backend.defaults('myapp')
defaults['base']['extensions'].append('genshi')
defaults['base']['output_handler'] = 'genshi'
defaults['genshi'] = dict(
    template_module='tests.templates'
    )
#app = foundation.lay_cement('myapp', defaults=defaults)
app = _t.prep('myapp', defaults=defaults)
app.setup()
app.argv = []
app.run()


def test_genshi():    
    rando = random.random()
    res = app.render(dict(foo=rando), 'test_template.txt')
    genshi_res = "foo equals %s" % rando
    eq_(res, genshi_res)

def test_genshi_bad_template():    
    res = app.render(dict(foo='bar'), 'bad_template.txt')

@raises(IOError)
def test_genshi_nonexistent_template():    
    res = app.render(dict(foo='bar'), 'missing_template.txt')
    
@raises(exc.CementRuntimeError)
def test_genshi_none_template():    
    try:
        res = app.render(dict(foo='bar'), None)
    except exc.CementRuntimeError as e:
        eq_(e.msg, "Invalid template 'None'.")
        raise

@raises(exc.CementRuntimeError)
def test_genshi_bad_module():
    app.config.set('genshi', 'template_module', 'this_is_a_bogus_module')
    res = app.render(dict(foo='bar'), 'bad_template.txt')