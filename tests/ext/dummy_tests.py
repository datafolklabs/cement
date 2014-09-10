"""Tests for cement.ext.ext_dummy."""

from cement.utils import test
from cement.utils.misc import rando

APP = "app-%s" % rando()[:12]


class DummyOutputHandlerTestCase(test.CementTestCase):
    pass

class DummyMailHandlerTestCase(test.CementTestCase):
    pass
