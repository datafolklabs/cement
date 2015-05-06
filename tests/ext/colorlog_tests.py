"""Tests for cement.ext.ext_colorlog."""

from cement.ext import ext_colorlog
from cement.utils import test
from cement.utils.misc import rando

APP = rando()[:12]

class ColorLogExtTestCase(test.CementExtTestCase):
    def setUp(self):
        self.app = self.make_app(APP, 
                        extensions=['colorlog'], 
                        log_handler='colorlog',
                        )

    def test_colorlog(self):
        self.app.setup()
        self.app.run()
        self.app.close()