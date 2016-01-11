"""Tests for cement.ext.ext_argcomplete."""

import os
from cement.ext import ext_argcomplete
from cement.ext.ext_argparse import ArgparseController, expose
from cement.utils import test
from cement.utils.misc import rando

APP = rando()[:12]

class MyBaseController(ArgparseController):
    class Meta:
        label = 'base'

    @expose()
    def default(self):
        pass

class ArgcompleteExtTestCase(test.CementExtTestCase):

    def setUp(self):
        super(ArgcompleteExtTestCase, self).setUp()
        self.app = self.make_app(APP, 
            argv=['default'],
            base_controller=MyBaseController,
            extensions=[
                'argparse',
                'argcomplete'
                ],
            )

    def test_argcomplete(self):
        # not really sure how to test this for reals... but let's atleast get
        # coverage
        with self.app as app:
            app.run()
