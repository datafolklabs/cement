"""Tests for cement2.ext.ext_yaml."""

import yaml
import unittest
from nose.tools import eq_, raises
from nose import SkipTest

from cement2.core import handler, hook
from cement2 import test_helper as _t

app = _t.prep()
from cement2.ext import ext_yaml

def import_yaml():
    from cement2.ext import ext_yaml
    handler.register(ext_yaml.YamlOutputHandler)
    hook.register()(ext_yaml.cement_post_setup_hook)
    hook.register()(ext_yaml.cement_pre_run_hook)
    
class YamlExtTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep('tests', 
            extensions=['yaml'],
            output_handler='yaml',
            argv=['--yaml']
            )
        import_yaml()
            
    def test_yaml(self):    
        self.app.setup()
        self.app.run()
        res = self.app.render(dict(foo='bar'))
        yaml_res = yaml.dump(dict(foo='bar'))
        eq_(res, yaml_res)
