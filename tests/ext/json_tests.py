"""Tests for cement.ext.ext_json."""

import json
import sys
from cement.core import handler, backend, hook
from cement.utils import test

class JsonExtTestCase(test.CementExtTestCase):
    def setUp(self):
        self.app = self.make_app('tests', 
            extensions=['json'],
            output_handler='json',
            argv=['--json']
            )
    
    def test_json(self):    
        self.app.setup()
        self.app.run()
        res = self.app.render(dict(foo='bar'))
        json_res = json.dumps(dict(foo='bar'))
        self.eq(res, json_res)
