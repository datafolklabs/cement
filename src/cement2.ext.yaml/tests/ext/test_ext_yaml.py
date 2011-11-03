"""Tests for cement2.ext.ext_yaml."""

import yaml
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import handler, backend, log
from cement2 import test_helper as _t

    
defaults = backend.defaults('myapp')
defaults['base']['extensions'].append('cement2.ext.ext_yaml')    
app = _t.prep('myapp', defaults=defaults)
app.setup()    

def import_yaml():
    from cement2.ext import ext_yaml
    handler.register(ext_yaml.JsonOutputHandler)
    
def test_yaml():    
    app.argv = ['--yaml']
    
    app.run()
    res = app.render(dict(foo='bar'))
    
    yaml_res = yaml.dump(dict(foo='bar'))
    eq_(res, yaml_res)
