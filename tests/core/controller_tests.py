"""Tests for cement.core.controller."""

import re
from cement.core import exc, controller
from cement.utils import test
from cement.utils.misc import rando, init_defaults

APP = "app-%s" % rando()[:12]


class ControllerTestCase(test.CementCoreTestCase):
    pass
