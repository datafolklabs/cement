
import sys

from tempfile import mkdtemp
from nose.tools import raises, with_setup

from cement_test.core.config import get_nose_config        
from cement_test.core.appmain import nose_main

sys.path.insert(0, '.')
# use an altername config for testing
config = get_nose_config(mkdtemp())

# run the initial main, which bootstraps the base application
nose_main([__file__, 'nosetests', '--quiet'], config)

def test_initialize():    
    """We put this here just to ensure nose picks up this file."""
    pass
