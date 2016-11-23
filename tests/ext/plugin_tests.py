"""Tests for cement.ext.ext_plugin."""

import os
from cement.utils import test
from cement.core.exc import FrameworkError
from cement.ext.ext_plugin import CementPluginHandler
from nose.plugins.attrib import attr

@attr('plugin')
class PluginExtTestCase(test.CementExtTestCase):

    def setUp(self):
        super(PluginExtTestCase, self).setUp()
        self.app = self.make_app('tests',
                        argv=[],
                        plugin_dir='./tests/__data__/plugins',
                        plugin_config_dir='./tests/__data__/config/plugins.d'
                        )

    def test_plugins(self):
        # real simple tests here just to ensure different kinds of plugins 
        # are loading
        with self.app as app:
            app.run()
            self.ok(app.plugin1_loaded)

            ### FIX ME: Fails because relative imports are broken with 
            ### importlib (which deprecated imp)
            self.ok(app.plugin2_loaded)
