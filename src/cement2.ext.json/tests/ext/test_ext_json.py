"""Tests for cement2.ext.ext_json."""

import json
import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import handler, backend, log
from cement2 import test_helper as _t

if sys.version_info[0] >= 3:
    raise SkipTest('jsonpickle does not support Python 3') # pragma: no cover
    
import jsonpickle
    
defaults = backend.defaults('myapp')
defaults['base']['extensions'].append('cement2.ext.ext_json')    
app = _t.prep('myapp', defaults=defaults)
app.setup()    

def import_json():
    from cement2.ext import ext_json
    handler.register(ext_json.JsonOutputHandler)
    
def test_json():    
    app.argv = ['--json']
    
    app.run()
    res = app.render(dict(foo='bar'))
    
    json_res = json.dumps(dict(foo='bar'))
    eq_(res, json_res)
