"""Tests for cement2.ext.ext_yaml."""

import yaml
from cement.core import handler, hook
from cement.utils import test

class YamlExtTestCase(test.CementTestCase):
    def setUp(self):
        self.app = self.make_app('tests',
            extensions=['yaml'],
            output_handler='yaml',
            argv=['--yaml']
            )

    def test_yaml(self):
        self.app.setup()
        self.app.run()
        res = self.app.render(dict(foo='bar'))
        yaml_res = yaml.dump(dict(foo='bar'))
        self.eq(res, yaml_res)
