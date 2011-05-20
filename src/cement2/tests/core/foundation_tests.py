"""Tests for cement.core.setup."""

import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import foundation, exc, backend, config
    
def test_foundation_default():
    app = foundation.lay_cement('cement_nosetests')
    
def test_foundation_passed_handlers():
    app = foundation.lay_cement('cement_nosetests',
        config_handler=config.ConfigParserConfigHandler(backend.defaults),
        
        )