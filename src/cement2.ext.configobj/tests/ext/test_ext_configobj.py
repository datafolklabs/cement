"""Tests for cement2.ext.ext_configobj."""

import configobj
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import handler, backend, log
from cement2 import test_helper as _t

def test_configobj():
    defaults = backend.defaults('myapp')
    defaults['base']['extensions'].append('cement2.ext.ext_configobj')
    defaults['base']['config_handler'] = 'configobj'
    
    app = _t.prep('myapp', defaults=defaults)
    app.argv = []
    app.setup()    
    app.run()

def test_has_key():
    defaults = backend.defaults('myapp')
    defaults['base']['extensions'].append('cement2.ext.ext_configobj')
    defaults['base']['config_handler'] = 'configobj'
    
    app = _t.prep('myapp', defaults=defaults)
    app.argv = []
    app.setup()    
    app.run()
    app.config.has_key('bogus_section', 'bogus_key')