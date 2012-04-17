"""Tests for cement2.ext.ext_json."""

import json
import sys
import unittest
from nose.tools import ok_, eq_, raises
from nose import SkipTest
from cement2.core import handler, backend, hook
from cement2 import test_helper as _t

if sys.version_info[0] < 3:
    import jsonpickle
else:
    raise SkipTest('jsonpickle does not support Python 3') # pragma: no cover

_t.prep()
from cement2.ext import ext_json

def import_json():
    from cement2.ext import ext_json
    handler.register(ext_json.JsonOutputHandler)
    hook.register()(ext_json.cement_post_setup_hook)
    hook.register()(ext_json.cement_pre_run_hook)
    
class JsonExtTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep('tests', 
            extensions=['json'],
            output_handler='json',
            argv=['--json']
            )
        import_json()
    
    def test_json(self):    
        self.app.setup()
        self.app.run()
        res = self.app.render(dict(foo='bar'))
        json_res = json.dumps(dict(foo='bar'))
        eq_(res, json_res)
