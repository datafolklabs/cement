"""
Initialize the application for nose testing, must be loaded first before
other tests.
"""

from tempfile import mkdtemp

from helloworld.core.config import get_nose_config        
from helloworld.core.appmain import nose_main

# use an altername config for testing
config = get_nose_config(mkdtemp())

# run the initial main, which bootstraps the base application
nose_main([__file__, 'nosetests', '--quiet'], config)

def test_initialize():    
    # We put this here just to ensure nose picks up this file.
    pass