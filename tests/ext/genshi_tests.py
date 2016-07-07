"""Tests for cement.ext.ext_genshi."""

import sys
import random

from cement.core import exc, foundation, handler, backend, controller
from cement.utils import test

if sys.version_info[0] < 3:
    import configobj
else:
    raise test.SkipTest('Genshi does not support Python 3')  # pragma: no cover


class GenshiExtTestCase(test.CementExtTestCase):

    def setUp(self):
        super(GenshiExtTestCase, self).setUp()
        self.app = self.make_app('tests',
                                 extensions=['genshi'],
                                 output_handler='genshi',
                                 argv=[]
                                 )

    def test_genshi(self):
        self.app.setup()
        rando = random.random()
        res = self.app.render(dict(foo=rando), 'test_template.genshi')
        genshi_res = "foo equals %s\n" % rando
        self.eq(res, genshi_res)

    @test.raises(exc.FrameworkError)
    def test_genshi_bad_template(self):
        self.app.setup()
        res = self.app.render(dict(foo='bar'), 'bad_template2.genshi')

    @test.raises(exc.FrameworkError)
    def test_genshi_nonexistent_template(self):
        self.app.setup()
        res = self.app.render(dict(foo='bar'), 'missing_template.genshi')

    @test.raises(exc.FrameworkError)
    def test_genshi_none_template(self):
        self.app.setup()
        try:
            res = self.app.render(dict(foo='bar'), None)
        except exc.FrameworkError as e:
            self.eq(e.msg, "Invalid template path 'None'.")
            raise

    @test.raises(exc.FrameworkError)
    def test_genshi_bad_module(self):
        self.app.setup()
        self.app._meta.template_module = 'this_is_a_bogus_module'
        res = self.app.render(dict(foo='bar'), 'bad_template.genshi')
