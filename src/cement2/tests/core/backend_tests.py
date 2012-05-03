"""Tests for cement.core.backend."""

import unittest
from nose.tools import with_setup, ok_, eq_, raises
from cement2.core import backend
from cement2 import test_helper as _t

class BackendTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep()

    def test_defaults(self):
        defaults = backend.defaults('myapp', 'section2', 'section3')
        defaults['myapp']['debug'] = True
        defaults['section2']['foo'] = 'bar'
        self.app = _t.prep('myapp', config_defaults=defaults)
        self.app.setup()
        eq_(self.app.config.get('myapp', 'debug'), True)
        ok_(self.app.config.get_section_dict('section2'))
        
    def test_minimal_logger(self):
        log = backend.minimal_logger(__name__)
        log = backend.minimal_logger(__name__, debug=True)
    
        # set logging back to non-debug
        backend.minimal_logger(__name__, debug=False)
        pass
