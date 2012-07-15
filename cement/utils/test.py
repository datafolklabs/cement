"""Cement testing utilities."""

import unittest
from ..core import backend, foundation

# shortcuts
from nose.tools import ok_ as ok
from nose.tools import eq_ as eq
from nose.tools import raises
from nose import SkipTest

class TestApp(foundation.CementApp):
    """
    Basic CementApp for generic testing.
    
    """
    class Meta:
        label = 'test'
        config_files = []
        argv = []

class CementTestCase(unittest.TestCase):
    """
    A sub-class of unittest.TestCase.  Provides useful shortcuts including 
    the following:
    
        self.ok
            A shortcut to assert()
        
        self.eq
            A shortcut to assertEquals()
        
        """
        
    def __init__(self, *args, **kw):
        super(CementTestCase, self).__init__(*args, **kw)
        self.ok = ok
        self.eq = eq
    
    def setUp(self):
        """
        Sets up self.app with a generic TestApp().  Also resets the backend
        hooks and handlers so that everytime an app is created it is setup
        clean each time.
        
        """
        self.app = self.make_app()
        
    def make_app(self, *args, **kw):
        """
        Create a generic app using TestApp.  Arguments and Keyword Arguments
        are passed to the app.
        
        """
        self.reset_backend()
        return TestApp(*args, **kw)
        
    def reset_backend(self):
        """
        Remove all registered hooks and handlers from the backend.
        
        """
        for _handler in backend.handlers.copy():
            del backend.handlers[_handler]
        for _hook in backend.hooks.copy():
            del backend.hooks[_hook]    
            