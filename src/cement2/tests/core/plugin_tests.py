"""Tests for cement.core.plugin."""

import os
import sys
import shutil
from tempfile import mkdtemp
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

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

PLUGIN = """

from cement2.core import handler, output

class TestOutputHandler(object):
    class Meta:
        interface = output.IOutput
        label = 'test_output_handler'
    
    def setup(self, config_obj):
        self.config = config_obj
    
    def render(self, data_dict, template=None):
        pass
        
handler.register(TestOutputHandler)

"""

def test_load_plugins_from_files():
    tmpdir = mkdtemp()
    f = open(os.path.join(tmpdir, 'myplugin.conf'), 'w')
    f.write(CONF)
    f.close()
    
    f = open(os.path.join(tmpdir, 'myplugin.py'), 'w')
    f.write(PLUGIN)
    f.close()
    
    defaults = backend.defaults('myapp')
    defaults['base']['plugin_config_dir'] = tmpdir
    defaults['base']['plugin_dir'] = tmpdir
    defaults['base']['plugin_bootstrap_module'] = None
    app = _t.prep('myapp', defaults=defaults)
    app.setup()
    
    try:
        han = handler.get('output', 'test_output_handler')
        eq_(han.Meta.label, 'test_output_handler')
    finally:
        shutil.rmtree(tmpdir)
        
def test_load_plugins_from_config():
    tmpdir = mkdtemp()
    f = open(os.path.join(tmpdir, 'myplugin.py'), 'w')
    f.write(PLUGIN)
    f.close()
    
    defaults = backend.defaults('myapp')
    defaults['base']['plugin_config_dir'] = tmpdir
    defaults['base']['plugin_dir'] = tmpdir
    defaults['base']['plugin_bootstrap_module'] = None
    defaults['myplugin'] = dict()
    defaults['myplugin']['enable_plugin'] = True
    defaults['myplugin2'] = dict()
    defaults['myplugin2']['enable_plugin'] = False
    app = _t.prep('myapp', defaults=defaults)
    app.setup()
    
    try:
        han = handler.get('output', 'test_output_handler')
        eq_(han.Meta.label, 'test_output_handler')
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
    
    res = 'myplugin' in app.config.get('base', 'plugins')        
    ok_(res)
    
def test_disabled_plugins_from_files():
    tmpdir = mkdtemp()
    f = open(os.path.join(tmpdir, 'myplugin.conf'), 'w')
    f.write(CONF2)
    f.close()
    
    f = open(os.path.join(tmpdir, 'myplugin.py'), 'w')
    f.write(PLUGIN)
    f.close()
    
    defaults = backend.defaults('myapp')
    defaults['base']['plugin_config_dir'] = tmpdir
    defaults['base']['plugin_dir'] = tmpdir
    defaults['base']['plugin_bootstrap_module'] = None
    app = _t.prep('myapp', defaults=defaults)
    app.setup()
    shutil.rmtree(tmpdir)
    
    res = 'test_output_handler' not in backend.handlers['output']
    ok_(res)

    res = 'myplugin2' not in app.config.get('base', 'plugins')        
    ok_(res)
    
def test_bogus_plugin_from_files():
    tmpdir = mkdtemp()
    f = open(os.path.join(tmpdir, 'myplugin.conf'), 'w')
    f.write(CONF3)
    f.close()
    
    defaults = backend.defaults('myapp')
    defaults['base']['plugin_config_dir'] = tmpdir
    defaults['base']['plugin_dir'] = tmpdir
    defaults['base']['plugin_bootstrap_module'] = None
    app = _t.prep('myapp', defaults=defaults)
    app.setup()
    shutil.rmtree(tmpdir)
    
    res = 'bogus_plugin' not in app.config.get('base', 'plugins')        
    ok_(res)

@raises(ImportError)
def test_bad_plugin_dir():
    tmpdir = mkdtemp()
    f = open(os.path.join(tmpdir, 'myplugin.conf'), 'w')
    f.write(CONF)
    f.close()
    
    defaults = backend.defaults('myapp')
    defaults['base']['plugin_config_dir'] = tmpdir
    defaults['base']['plugin_dir'] = './some/bogus/path'
    defaults['base']['plugin_bootstrap_module'] = None
    app = _t.prep('myapp', defaults=defaults)
    try:
        app.setup()
    except ImportError:
        raise
    finally:
        shutil.rmtree(tmpdir)
    
def test_load_plugin_from_module():
    # We mock this out by loading a cement ext, but it is essentially the
    # same type of code.
    tmpdir = mkdtemp()
    f = open(os.path.join(tmpdir, 'ext_optparse.conf'), 'w')
    f.write(CONF4)
    f.close()
    
    defaults = backend.defaults('myapp')
    defaults['base']['plugin_config_dir'] = tmpdir
    defaults['base']['plugin_dir'] = tmpdir
    defaults['base']['plugin_bootstrap_module'] = 'cement2.ext'
    app = _t.prep('myapp', defaults=defaults)
    app.setup()
    
    shutil.rmtree(tmpdir)
    
@raises(ImportError)
def test_load_bogus_plugin():
    app = _t.prep('myapp')
    app.setup()
    app.plugin.load_plugin('bogus_plugin')