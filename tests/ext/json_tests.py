"""Tests for cement.ext.ext_json."""

import json
import sys
import unittest
from nose.tools import ok_, eq_, raises
from cement.core import handler, backend, hook
from cement.utils import test_helper as _t

_t.prep()
from cement.ext import ext_json

#def import_json():
#    from cement.ext import ext_json
#    handler.register(ext_json.JsonOutputHandler)
#    hook.register()(ext_json.cement_post_setup_hook)
#    hook.register()(ext_json.cement_pre_run_hook)
    
class JsonExtTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep('tests', 
            extensions=['json'],
            output_handler='json',
            argv=['--json']
            )
    
    def test_json(self):    
        self.app.setup()
        self.app.run()
        res = self.app.render(dict(foo='bar'))
        json_res = json.dumps(dict(foo='bar'))
        eq_(res, json_res)
