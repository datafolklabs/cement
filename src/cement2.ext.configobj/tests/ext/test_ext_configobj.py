"""Tests for cement2.ext.ext_configobj."""

import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import handler, backend, log
from cement2 import test_helper as _t

if sys.version_info[0] >= 3:
    raise SkipTest('ConfigObj does not support Python 3') # pragma: no cover
    
import configobj

def import_configobj():
    from cement2.ext import ext_configobj
    handler.register(ext_configobj.ConfigObjConfigHandler)
    
def test_configobj():
    defaults = backend.defaults('myapp')
    defaults['base']['extensions'].append('cement2.ext.ext_configobj')
    defaults['base']['config_handler'] = 'configobj'
    
    app = _t.prep('myapp', defaults=defaults)
    #import_configobj()
    
    app.argv = []
    app.setup()    
    app.run()

def test_has_key():
    defaults = backend.defaults('myapp')
    defaults['base']['extensions'].append('cement2.ext.ext_configobj')
    defaults['base']['config_handler'] = 'configobj'

    app = _t.prep('myapp', defaults=defaults)
    import_configobj()
    
    app.argv = []    
    app.setup()    
    app.run()
    app.config.has_key('bogus_section', 'bogus_key')