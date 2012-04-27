"""Tests for cement.core.backend."""

import unittest
from nose.tools import with_setup, ok_, eq_, raises
from cement2.core import backend
from cement2 import test_helper as _t

config = {}
config['base'] = {}

def compare_with_defaults(section, key):
    """
    Check that the default key value matches that of the known config above.
    """
    defaults = backend.defaults()
    ok_(section in defaults)
    ok_(key in defaults[section])
    eq_(defaults[section][key], config[section][key])
    
class BackendTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep()
        
    def test_verify_defaults(self):
        for section in list(config.keys()):
            for key in list(config[section].keys()):
                yield compare_with_defaults, section, key
    
    def test_minimal_logger(self):
        log = backend.minimal_logger(__name__)
        log = backend.minimal_logger(__name__, debug=True)
    
        # set logging back to non-debug
        backend.minimal_logger(__name__, debug=False)
        pass
