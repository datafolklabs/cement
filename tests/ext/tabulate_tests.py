"""Tests for cement.ext.ext_tabulate."""

import re
import random
from cement.utils import test


class TabulateExtTestCase(test.CementExtTestCase):

    def setUp(self):
        super(TabulateExtTestCase, self).setUp()
        self.app = self.make_app('tests',
                                 extensions=['tabulate'],
                                 output_handler='tabulate',
                                 argv=[]
                                 )

    def test_tabulate(self):
        self.app.setup()
        rando = random.random()
        res = self.app.render([['John', 'Doe']], headers=['FOO', 'BAR'])
        self.ok(res.find('FOO'))
