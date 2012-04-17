"""Tests for cement2.ext.ext_optparse."""

import unittest
from nose.tools import eq_, raises
from cement2.core import handler, backend, log
from cement2 import test_helper as _t

class OptParseExtTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep()
        
    def test_optparse(self):    
        app = _t.prep('myapp', 
            extensions=['optparse'],
            arg_handler='optparse',
            argv=['my-command']
            )
        app.setup()    