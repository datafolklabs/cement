"""Tests for cement2.ext.ext_logging."""

import logging
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import handler, backend, log
from cement2 import test_helper as _t

def test_rotate():
    app = _t.prep('myapp')
    app.setup()    
    app.config.set('base', 'debug', True)
    app.config.set('log', 'file', '/dev/null')
    app.config.set('log', 'rotate', True)
    app.config.set('log', 'to_console', True)
    app.log.setup(app.config)
    
    
def test_bad_level():
    app = _t.prep('myapp')
    app.setup()
    app.config.set('log', 'file', '/dev/null')
    app.config.set('log', 'rotate', True)
    app.config.set('log', 'to_console', True)
    app.config.set('log', 'level', 'BOGUS')
    app.log.setup(app.config)