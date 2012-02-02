"""Tests for cement2.ext.ext_logging."""
        
import os
import logging
from tempfile import mkstemp
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import handler, backend, log
from cement2 import test_helper as _t
_t.prep()

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
    app.config.set('log', 'level', 'BOGUS')
    
    han = handler.get('log', 'logging')
    Log = han()
    Log.setup(app.config)

    eq_(Log.level(), 'INFO')

def test_clear_loggers():
    app = _t.prep('myapp')
    app.setup()
    
    han = handler.get('log', 'logging')
    Log = han()
    Log.clear_loggers()

def test_rotate():
    app = _t.prep('myapp')
    app.setup()
    
    han = handler.get('log', 'logging')
    Log = han(rotate=True, file=mkstemp()[1])
    Log.setup(app.config)

def test_missing_log_dir():
    _, tmp_path = mkstemp()
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
        
    defaults = backend.defaults('myapp')
    defaults['log'] = dict()
    defaults['log']['file'] = os.path.join(tmp_path, 'myapp.log')
    app = _t.prep('myapp', defaults=defaults)
    app.setup()
        