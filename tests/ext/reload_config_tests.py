"""Tests for cement.ext.ext_reload_config."""

import platform
from cement.utils import test

system = platform.system()
if not system in ['Linux']:
    raise test.SkipTest('ext_reload_config not supported on %s' % system)

import os
import shutil
import signal
from time import sleep
from cement.utils.misc import rando
from cement.ext import ext_reload_config

APP = rando()[:12]

CONFIG1 = """
[%s]
foo = bar1
""" % APP

CONFIG2 = """
[%s]
foo = bar2
""" % APP

PLUGIN_CONFIG1 = """
[bogus]
enable_plugin = false
"""


def bogus_hook_func(app):
    pass


class ReloadConfigExtTestCase(test.CementExtTestCase):

    def setUp(self):
        super(ReloadConfigExtTestCase, self).setUp()

        f = open(self.tmp_file, 'w')
        f.write(CONFIG1)
        f.close()

        f = open(os.path.join(self.tmp_dir, 'bogus.conf'), 'w')
        f.write(PLUGIN_CONFIG1)
        f.close()

        self.app = self.make_app(APP,
                                 extensions=['reload_config'],
                                 config_files=[self.tmp_file],
                                 plugin_config_dirs=[self.tmp_dir],
                                 )

    def test_reload_config(self):
        self.app.setup()
        self.app.hook.register('pre_reload_config', bogus_hook_func)
        self.app.hook.register('post_reload_config', bogus_hook_func)
        self.app.run()
        self.eq(self.app.config.get(APP, 'foo'), 'bar1')

        f = open(self.tmp_file, 'w')
        f.write(CONFIG2)
        f.close()

        sleep(1)

        try:
            self.eq(self.app.config.get(APP, 'foo'), 'bar2')
        finally:
            self.app.close()

    def test_no_plugin_dir(self):
        # coverage.. remove the plugin config dir
        shutil.rmtree(self.tmp_dir)
        self.app.setup()
        self.app.run()
        self.app.close()

    def test_signal_handling(self):
        self.app.setup()
        self.app.hook.register('pre_reload_config', bogus_hook_func)
        self.app.hook.register('post_reload_config', bogus_hook_func)
        self.app.run()

        sleep(1)
        try:
            ext_reload_config.signal_handler(self.app, signal.SIGINT, None)
        finally:
            self.app.close()
