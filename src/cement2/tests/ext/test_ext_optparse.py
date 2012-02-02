"""Tests for cement2.ext.ext_optparse."""

from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import handler, backend, log
from cement2 import test_helper as _t
_t.prep()

def test_optparse():
    defaults = backend.defaults('myapp')
    defaults['base']['arg_handler'] = 'optparse'
    defaults['base']['extensions'].append('optparse')
    
    app = _t.prep('myapp', defaults=defaults)
    app.argv = ['default']
    app.setup()    
    app.run()