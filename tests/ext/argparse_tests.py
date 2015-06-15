"""Tests for cement.ext.ext_argparse."""

import os
from cement.ext.ext_argparse import ArgparseArgumentHandler
from cement.ext.ext_argparse import ArgparseController, expose
from cement.utils import test
from cement.utils.misc import rando, init_defaults
from cement.core import handler

APP = rando()[:12]

class Base(ArgparseController):
    class Meta:
        label = 'base'

    @expose(hide=True, help="this help doesn't get seen")
    def default(self):
        return "Inside Base.default"

class Second(ArgparseController):
    class Meta:
        label = 'second'
        stacked_on = 'base'
        stacked_type = 'embedded'

    @expose()
    def cmd2(self):
        return "Inside Second.cmd2"

class Third(ArgparseController):
    class Meta:
        label = 'third'
        stacked_on = 'base'
        stacked_type = 'nested'

    @expose(hide=True)
    def default(self):
        return "Inside Third.default"

    @expose()
    def cmd3(self):
        return "Inside Third.cmd3"

class Fourth(ArgparseController):
    class Meta:
        label = 'fourth'
        stacked_on = 'third'
        stacked_type = 'embedded'
        hide = True
        help = "this help doesn't get seen cause we're hiding"

    @expose()
    def cmd4(self):
        return "Inside Fourth.cmd4"

class Fifth(ArgparseController):
    class Meta:
        label = 'fifth'
        stacked_on = 'third'
        stacked_type = 'nested'

    @expose(hide=True)
    def default(self):
        return "Inside Fifth.default"
        
    @expose()
    def cmd5(self):
        return "Inside Fifth.cmd5"


class ArgparseExtTestCase(test.CementExtTestCase):

    def setUp(self):
        super(ArgparseExtTestCase, self).setUp()
        self.app = self.make_app(APP,
            argument_handler=ArgparseArgumentHandler,
            handlers=[
                Base,
                Second,
                Third,
                Fourth,
                Fifth,
                ],
            )

    def test_base_controller_default(self):
        with self.app as app:
            res = app.run()
            self.eq(res, "Inside Base.default")

    def test_controller_embedded_on_base(self):
        self.app._meta.argv = ['cmd2']
        with self.app as app:
            res = app.run()
            self.eq(res, "Inside Second.cmd2")

    def test_controller_nested_on_base(self):
        self.app._meta.argv = ['third']
        with self.app as app:
            res = app.run()
            self.eq(res, "Inside Third.default")

    def test_controller_doubled_embedded(self):
        self.app._meta.argv = ['third', 'cmd4']
        with self.app as app:
            res = app.run()
            self.eq(res, "Inside Fourth.cmd4")
            
    def test_controller_double_nested(self):
        self.app._meta.argv = ['third', 'fifth']
        with self.app as app:
            res = app.run()
            self.eq(res, "Inside Fifth.default")

        self.setUp()

        self.app._meta.argv = ['third', 'fifth', 'cmd5']
        with self.app as app:
            res = app.run()
            self.eq(res, "Inside Fifth.cmd5")