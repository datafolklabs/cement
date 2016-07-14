"""Tests for cement.ext.ext_handlebars."""

import sys
import random
from cement.core import exc, foundation, handler, backend, controller
from cement.utils import test
from nose.plugins.attrib import attr

class HandlebarsTestApp(test.TestApp):
    class Meta:
        extensions = ['handlebars']
        output_handler = 'handlebars'
        template_module = 'tests.templates'
        template_dirs = []
        handlebars_helpers = {}
        handlebars_partials = ['test_partial_template.handlebars']
        
@attr('ext_handlebars')        
class HandlebarsExtTestCase(test.CementExtTestCase):
    app_class = HandlebarsTestApp

    def test_handlebars(self):
        self.app.setup()
        rando = random.random()
        res = self.app.render(dict(foo=rando), 'test_template.handlebars')
        handlebars_res = "foo equals %s\n" % rando
        self.eq(res, handlebars_res)

    def test_handlebars_partials(self):
        # FIX ME: Not sure what's going on here
        self.app.setup()

        rando = random.random()
        res = self.app.render(dict(foo=rando), 'test_base_template.handlebars')
        handlebars_res = "Inside partial > foo equals %s\n" % rando
        self.eq(res, handlebars_res)

    @test.raises(exc.FrameworkError)
    def test_handlebars_bad_template(self):
        self.app.setup()
        res = self.app.render(dict(foo='bar'), 'bad_template2.handlebars')

    @test.raises(exc.FrameworkError)
    def test_handlebars_nonexistent_template(self):
        self.app.setup()
        res = self.app.render(dict(foo='bar'), 'missing_template.handlebars')

    @test.raises(exc.FrameworkError)
    def test_handlebars_none_template(self):
        self.app.setup()
        try:
            res = self.app.render(dict(foo='bar'), None)
        except exc.FrameworkError as e:
            self.eq(e.msg, "Invalid template path 'None'.")
            raise

    @test.raises(exc.FrameworkError)
    def test_handlebars_bad_module(self):
        self.app.setup()
        self.app._meta.template_module = 'this_is_a_bogus_module'
        res = self.app.render(dict(foo='bar'), 'bad_template.handlebars')
