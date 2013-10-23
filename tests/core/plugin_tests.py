"""Tests for cement.core.plugin."""

import os
import sys
import shutil
from tempfile import mkdtemp
from cement.core import exc, backend, plugin, handler
from cement.utils import test
from cement.utils.misc import init_defaults

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
[ext_json]
enable_plugin = true
foo = bar
"""

CONF5 = ''

PLUGIN = """

from cement.core import handler, output

class TestOutputHandler(output.CementOutputHandler):
    class Meta:
        interface = output.IOutput
        label = 'test_output_handler'
    
    def _setup(self, app_obj):
        self.app = app_obj
    
    def render(self, data_dict, template=None):
        pass
        
def load():
    handler.register(TestOutputHandler)

"""

class PluginTestCase(test.CementCoreTestCase):
    def setUp(self):
        self.app = self.make_app()

    def test_load_plugins_from_files(self):
        tmpdir = mkdtemp()
        f = open(os.path.join(tmpdir, 'myplugin.conf'), 'w')
        f.write(CONF)
        f.close()
    
        f = open(os.path.join(tmpdir, 'myplugin.py'), 'w')
        f.write(PLUGIN)
        f.close()
    
        app = self.make_app('myapp',
            config_files=[],
            plugin_config_dir=tmpdir,
            plugin_dir=tmpdir,
            plugin_bootstrap=None,
            )
        app.setup()

        try:
            han = handler.get('output', 'test_output_handler')()
            self.eq(han._meta.label, 'test_output_handler')
        finally:
            shutil.rmtree(tmpdir)
        
    def test_load_plugins_from_config(self):
        tmpdir = mkdtemp()
        f = open(os.path.join(tmpdir, 'myplugin.py'), 'w')
        f.write(PLUGIN)
        f.close()
    
        defaults = init_defaults()
        defaults['myplugin'] = dict()
        defaults['myplugin']['enable_plugin'] = True
        defaults['myplugin2'] = dict()
        defaults['myplugin2']['enable_plugin'] = False
        app = self.make_app('myapp', config_defaults=defaults,
            config_files=[],
            plugin_config_dir=tmpdir,
            plugin_dir=tmpdir,
            plugin_bootstrap=None,
            )
        app.setup()
    
        try:
            han = handler.get('output', 'test_output_handler')()
            self.eq(han._meta.label, 'test_output_handler')
        finally:
            shutil.rmtree(tmpdir)
    
        # some more checks
        res = 'myplugin' in app.plugin.get_enabled_plugins()
        self.ok(res)
    
        res = 'myplugin' in app.plugin.get_loaded_plugins()
        self.ok(res)
        
        res = 'myplugin2' in app.plugin.get_disabled_plugins()
        self.ok(res)
    
        res = 'myplugin2' not in app.plugin.get_enabled_plugins()
        self.ok(res)
    
        res = 'myplugin2' not in app.plugin.get_loaded_plugins()
        self.ok(res)
    
    def test_disabled_plugins_from_files(self):
        tmpdir = mkdtemp()
        f = open(os.path.join(tmpdir, 'myplugin.conf'), 'w')
        f.write(CONF2)
        f.close()
    
        f = open(os.path.join(tmpdir, 'myplugin.py'), 'w')
        f.write(PLUGIN)
        f.close()
    
        app = self.make_app('myapp',
            config_files=[],
            plugin_config_dir=tmpdir,
            plugin_dir=tmpdir,
            plugin_bootstrap=None,
            )
        app.setup()
        shutil.rmtree(tmpdir)
    
        res = 'test_output_handler' not in backend.__handlers__['output']
        self.ok(res)

        res = 'myplugin2' not in app.plugin.get_enabled_plugins()
        self.ok(res)
    
    def test_bogus_plugin_from_files(self):
        tmpdir = mkdtemp()
        f = open(os.path.join(tmpdir, 'myplugin.conf'), 'w')
        f.write(CONF3)
        f.close()
    
        # do this for coverage... empty config file
        f = open(os.path.join(tmpdir, 'bogus.conf'), 'w')
        f.write(CONF5)
        f.close()
        
        app = self.make_app('myapp',
            config_files=[],
            plugin_config_dir=tmpdir,
            plugin_dir=tmpdir,
            plugin_bootstrap=None,
            )
        app.setup()
        shutil.rmtree(tmpdir)
    
        res = 'bogus_plugin' not in app.plugin.get_enabled_plugins()
        self.ok(res)

    @test.raises(exc.FrameworkError)
    def test_bad_plugin_dir(self):
        tmpdir = mkdtemp()
        f = open(os.path.join(tmpdir, 'myplugin.conf'), 'w')
        f.write(CONF)
        f.close()

        app = self.make_app('myapp',
            config_files=[],
            plugin_config_dir=tmpdir,
            plugin_dir='./some/bogus/path',
            plugin_bootstrap=None,
            )
        try:
            app.setup()
        except ImportError as e:
            raise
        except exc.FrameworkError as e:
            raise 
        finally:
            shutil.rmtree(tmpdir)
    
    def test_load_plugin_from_module(self):
        # We mock this out by loading a cement ext, but it is essentially the
        # same type of code.
        tmpdir = mkdtemp()
        del sys.modules['cement.ext.ext_json']
        f = open(os.path.join(tmpdir, 'ext_json.conf'), 'w')
        f.write(CONF4)
        f.close()
    
        app = self.make_app('myapp',
            config_files=[],
            plugin_config_dir=tmpdir,
            plugin_dir=tmpdir,
            plugin_bootstrap='cement.ext',
            )
        app.setup()
        
        res = 'ext_json' in app.plugin.get_enabled_plugins()
        self.ok(res)
        
        shutil.rmtree(tmpdir)

