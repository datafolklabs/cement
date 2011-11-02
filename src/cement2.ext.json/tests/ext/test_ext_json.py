"""Tests for cement2.ext.ext_json."""

import json
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import handler, backend, log
from cement2 import test_helper as _t

def test_json():
    defaults = backend.defaults('myapp')
    defaults['base']['extensions'].append('cement2.ext.ext_json')
    
    app = _t.prep('myapp', defaults=defaults)
    app.argv = ['--json']
    app.setup()    
    app.run()
    res = app.render(dict(foo='bar'))
    
    json_res = json.dumps(dict(foo='bar'))
    eq_(res, json_res)