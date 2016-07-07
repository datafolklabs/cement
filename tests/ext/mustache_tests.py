"""Tests for cement.ext.ext_mustache."""

import sys
import random

from cement.core import exc, foundation, handler, backend, controller
from cement.utils import test


class MustacheExtTestCase(test.CementExtTestCase):

    def setUp(self):
        super(MustacheExtTestCase, self).setUp()
        self.app = self.make_app('tests',
                                 extensions=['mustache'],
                                 output_handler='mustache',
                                 argv=[]
                                 )

    def test_mustache(self):
        self.app.setup()
        rando = random.random()
        res = self.app.render(dict(foo=rando), 'test_template.mustache')
        mustache_res = "foo equals %s\n" % rando
        self.eq(res, mustache_res)

    def test_mustache_partials(self):
        self.app.setup()
        rando = random.random()
        res = self.app.render(dict(foo=rando), 'test_base_template.mustache')
        mustache_res = "Inside partial > foo equals %s\n" % rando
        self.eq(res, mustache_res)

    @test.raises(exc.FrameworkError)
    def test_mustache_bad_template(self):
        self.app.setup()
        res = self.app.render(dict(foo='bar'), 'bad_template2.mustache')

    @test.raises(exc.FrameworkError)
    def test_mustache_nonexistent_template(self):
        self.app.setup()
        res = self.app.render(dict(foo='bar'), 'missing_template.mustache')

    @test.raises(exc.FrameworkError)
    def test_mustache_none_template(self):
        self.app.setup()
        try:
            res = self.app.render(dict(foo='bar'), None)
        except exc.FrameworkError as e:
            self.eq(e.msg, "Invalid template path 'None'.")
            raise

    @test.raises(exc.FrameworkError)
    def test_mustache_bad_module(self):
        self.app.setup()
        self.app._meta.template_module = 'this_is_a_bogus_module'
        res = self.app.render(dict(foo='bar'), 'bad_template.mustache')
