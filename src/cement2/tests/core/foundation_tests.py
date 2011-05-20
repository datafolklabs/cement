"""Tests for cement.core.setup."""

import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import foundation, exc, backend
    
def test_foundation():
    app = foundation.lay_cement('cement_nosetests')