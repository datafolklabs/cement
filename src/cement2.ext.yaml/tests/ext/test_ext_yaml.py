"""Tests for cement2.ext.ext_yaml."""

import yaml
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import handler, backend, log
from cement2 import test_helper as _t

def test_yaml():
    defaults = backend.defaults('myapp')
    defaults['base']['extensions'].append('cement2.ext.ext_yaml')
    
    app = _t.prep('myapp', defaults=defaults)
    app.argv = ['--yaml']
    app.setup()    
    app.run()
    res = app.render(dict(foo='bar'))
    
    yaml_res = yaml.dump(dict(foo='bar'))
    eq_(res, yaml_res)