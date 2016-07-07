# -*- coding: utf-8 -*-
"""Tests for cement.ext.ext_jinja2."""

import sys
import random

from cement.core import exc, foundation, handler, backend, controller
from cement.utils import test


class Jinja2ExtTestCase(test.CementExtTestCase):

    def setUp(self):
        super(Jinja2ExtTestCase, self).setUp()
        self.app = self.make_app('tests',
                                 extensions=['jinja2'],
                                 output_handler='jinja2',
                                 argv=[]
                                 )

    def test_jinja2(self):
        self.app.setup()
        rando = random.random()
        res = self.app.render(dict(foo=rando), 'test_template.jinja2')
        jinja2_res = "foo equals %s\n" % rando
        self.eq(res, jinja2_res)

    @test.raises(exc.FrameworkError)
    def test_jinja2_bad_template(self):
        self.app.setup()
        res = self.app.render(dict(foo='bar'), 'bad_template2.jinja2')

    @test.raises(exc.FrameworkError)
    def test_jinja2_nonexistent_template(self):
        self.app.setup()
        res = self.app.render(dict(foo='bar'), 'missing_template.jinja2')

    @test.raises(exc.FrameworkError)
    def test_jinja2_none_template(self):
        self.app.setup()
        try:
            res = self.app.render(dict(foo='bar'), None)
        except exc.FrameworkError as e:
            self.eq(e.msg, "Invalid template path 'None'.")
            raise

    @test.raises(exc.FrameworkError)
    def test_jinja2_bad_module(self):
        self.app.setup()
        self.app._meta.template_module = 'this_is_a_bogus_module'
        res = self.app.render(dict(foo='bar'), 'bad_template.jinja2')
