"""Tests for cement.core.plugin."""

import os
import shutil
import unittest
from tempfile import mkdtemp
from nose.tools import with_setup, ok_, eq_, raises
from cement2.core import exc, backend, plugin, handler
from cement2 import test_helper as _t

CONF = """
[myplugin]
enable_plugin = true
foo = bar

"""

CONF2 = """
[myplugin]
enable_plugin = false
foo = bar
"""

CONF3 = """
[bogus_plugin]
foo = bar
"""

CONF4 = """
[ext_optparse]
enable_plugin = true
foo = bar
"""

CONF5 = ''

PLUGIN = """

from cement2.core import handler, output

class TestOutputHandler(output.CementOutputHandler):
    class Meta:
        interface = output.IOutput
        label = 'test_output_handler'
    
    def _setup(self, app_obj):
        self.app = app_obj
    
    def render(self, data_dict, template=None):
        pass
        
handler.register(TestOutputHandler)

"""

class PluginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep()

    def test_load_plugins_from_files(self):
        tmpdir = mkdtemp()
        f = open(os.path.join(tmpdir, 'myplugin.conf'), 'w')
        f.write(CONF)
        f.close()
    
        f = open(os.path.join(tmpdir, 'myplugin.py'), 'w')
        f.write(PLUGIN)
        f.close()
    
        app = _t.prep('myapp',
            config_files=[],
            plugin_config_dir=tmpdir,
            plugin_dir=tmpdir,
            plugin_bootstrap=None,
            )
        app.setup()

        try:
            han = handler.get('output', 'test_output_handler')()
            eq_(han._meta.label, 'test_output_handler')
        finally:
            shutil.rmtree(tmpdir)
        
    def test_load_plugins_from_config(self):
        tmpdir = mkdtemp()
        f = open(os.path.join(tmpdir, 'myplugin.py'), 'w')
        f.write(PLUGIN)
        f.close()
    
        defaults = backend.defaults()
        defaults['myplugin'] = dict()
        defaults['myplugin']['enable_plugin'] = True
        defaults['myplugin2'] = dict()
        defaults['myplugin2']['enable_plugin'] = False
        app = _t.prep('myapp', config_defaults=defaults,
            config_files=[],
            plugin_config_dir=tmpdir,
            plugin_dir=tmpdir,
            plugin_bootstrap=None,
            )
        app.setup()
    
        try:
            han = handler.get('output', 'test_output_handler')()
            eq_(han._meta.label, 'test_output_handler')
        finally:
            shutil.rmtree(tmpdir)
    
        # some more checks
        res = 'myplugin' in app.plugin.enabled_plugins
        ok_(res)
    
        res = 'myplugin' in app.plugin.loaded_plugins
        ok_(res)
        
        res = 'myplugin2' in app.plugin.disabled_plugins
        ok_(res)
    
        res = 'myplugin2' not in app.plugin.enabled_plugins
        ok_(res)
    
        res = 'myplugin2' not in app.plugin.loaded_plugins
        ok_(res)
    
    def test_disabled_plugins_from_files(self):
        tmpdir = mkdtemp()
        f = open(os.path.join(tmpdir, 'myplugin.conf'), 'w')
        f.write(CONF2)
        f.close()
    
        f = open(os.path.join(tmpdir, 'myplugin.py'), 'w')
        f.write(PLUGIN)
        f.close()
    
        app = _t.prep('myapp',
            config_files=[],
            plugin_config_dir=tmpdir,
            plugin_dir=tmpdir,
            plugin_bootstrap=None,
            )
        app.setup()
        shutil.rmtree(tmpdir)
    
        res = 'test_output_handler' not in backend.handlers['output']
        ok_(res)

        res = 'myplugin2' not in app.plugin.enabled_plugins
        ok_(res)
    
    def test_bogus_plugin_from_files(self):
        tmpdir = mkdtemp()
        f = open(os.path.join(tmpdir, 'myplugin.conf'), 'w')
        f.write(CONF3)
        f.close()
    
        # do this for coverage... empty config file
        f = open(os.path.join(tmpdir, 'bogus.conf'), 'w')
        f.write(CONF5)
        f.close()
        
        app = _t.prep('myapp',
            config_files=[],
            plugin_config_dir=tmpdir,
            plugin_dir=tmpdir,
            plugin_bootstrap=None,
            )
        app.setup()
        shutil.rmtree(tmpdir)
    
        res = 'bogus_plugin' not in app.plugin.enabled_plugins
        ok_(res)

    @raises(exc.CementRuntimeError)
    def test_bad_plugin_dir(self):
        tmpdir = mkdtemp()
        f = open(os.path.join(tmpdir, 'myplugin.conf'), 'w')
        f.write(CONF)
        f.close()

        app = _t.prep('myapp',
            config_files=[],
            plugin_config_dir=tmpdir,
            plugin_dir='./some/bogus/path',
            plugin_bootstrap=None,
            )
        try:
            app.setup()
        except ImportError as e:
            raise
        except exc.CementRuntimeError as e:
            raise 
        finally:
            shutil.rmtree(tmpdir)
    
    def test_load_plugin_from_module(self):
        # We mock this out by loading a cement ext, but it is essentially the
        # same type of code.
        tmpdir = mkdtemp()
        f = open(os.path.join(tmpdir, 'ext_optparse.conf'), 'w')
        f.write(CONF4)
        f.close()
    
        app = _t.prep('myapp',
            config_files=[],
            plugin_config_dir=tmpdir,
            plugin_dir=tmpdir,
            plugin_bootstrap='cement2.ext',
            )
        app.setup()
        
        res = 'ext_optparse' in app.plugin.enabled_plugins
        ok_(res)
        
        shutil.rmtree(tmpdir)
