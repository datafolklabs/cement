
import os
import sys
from pytest import raises

from cement import init_defaults
from cement.core.foundation import TestApp
from cement.core.exc import FrameworkError
from cement.core.plugin import PluginInterface, PluginHandler


# module tests

class TestPluginInterface(object):
    def test_interface(self):
        assert PluginInterface.Meta.interface == 'plugin'


class TestPluginHandler(object):
    def test_subclassing(self):

        class MyPluginHandler(PluginHandler):

            class Meta:
                label = 'my_plugin_handler'

            def load_plugin(plugin_name):
                pass

            def load_plugins(self, plugins):
                pass

            def get_loaded_plugins(self):
                pass

            def get_enabled_plugins(self):
                pass

            def get_disabled_plugins(self):
                pass

        h = MyPluginHandler()
        assert h._meta.interface == 'plugin'
        assert h._meta.label == 'my_plugin_handler'


# app functionality and coverage tests

CONF1 = """
[plugin.myplugin]
enabled = true
foo = bar

"""

CONF2 = """
[plugin.myplugin]
enabled = false
foo = bar
"""

CONF3 = """
[plugin.bogus_plugin]
foo = bar
"""

CONF4 = """
[plugin.ext_json]
enabled = true
foo = bar
"""

CONF5 = ''

PLUGIN = """

from cement.core.output import OutputHandler

class MyOutputHandler(OutputHandler):
    class Meta:
        label = 'my_output_handler'

    def render(self, data_dict, template=None):
        pass

def load(app):
    app.handler.register(MyOutputHandler)

"""


def test_load_plugins_from_files(tmp):

    f = open(os.path.join(tmp.dir, 'myplugin.conf'), 'w')
    f.write(CONF1)
    f.close()

    f = open(os.path.join(tmp.dir, 'myplugin.py'), 'w')
    f.write(PLUGIN)
    f.close()

    class MyApp(TestApp):
        class Meta:
            plugin_config_dir = tmp.dir
            plugin_dir = tmp.dir
            plugin_bootstrap = None

    with MyApp() as app:
        han = app.handler.get('output', 'my_output_handler')()
        assert han._meta.label, 'my_output_handler'


def test_load_order_presedence_one(tmp):
    # app config defines it as enabled, but the plugin config has it
    # disabled... app trumps the config
    defaults = init_defaults('plugin.myplugin')
    defaults['plugin.myplugin']['enabled'] = True

    f = open(os.path.join(tmp.dir, 'myplugin.conf'), 'w')
    f.write(CONF2)
    f.close()

    f = open(os.path.join(tmp.dir, 'myplugin.py'), 'w')
    f.write(PLUGIN)
    f.close()

    class MyApp(TestApp):
        class Meta:
            config_defaults = defaults
            plugin_config_dir = tmp.dir
            plugin_dir = tmp.dir
            plugin_bootstrap = None

    with MyApp() as app:
        assert 'myplugin' in app.plugin._enabled_plugins
        assert 'myplugin' not in app.plugin._disabled_plugins


def test_load_order_presedence_two(tmp):
    # opposite of previous test... the app config defines it as disabled, even
    # though the plugin config has it enabled... app trumps the config
    defaults = init_defaults('plugin.myplugin')
    defaults['plugin.myplugin']['enabled'] = False

    f = open(os.path.join(tmp.dir, 'myplugin.conf'), 'w')
    f.write(CONF1)
    f.close()

    f = open(os.path.join(tmp.dir, 'myplugin.py'), 'w')
    f.write(PLUGIN)
    f.close()

    class MyApp(TestApp):
        class Meta:
            config_defaults = defaults
            plugin_config_dir = tmp.dir
            plugin_dir = tmp.dir
            plugin_bootstrap = None

    with MyApp() as app:
        assert 'myplugin' in app.plugin._disabled_plugins
        assert 'myplugin' not in app.plugin._enabled_plugins


def test_load_order_presedence_three(tmp):
    # multiple plugin configs, first plugin conf defines it as disabled,
    # but last read should make it enabled.
    defaults = init_defaults('plugin.myplugin')

    f = open(os.path.join(tmp.dir, 'a.conf'), 'w')
    f.write(CONF2)  # disabled config
    f.close()

    f = open(os.path.join(tmp.dir, 'b.conf'), 'w')
    f.write(CONF1)  # enabled config
    f.close()

    f = open(os.path.join(tmp.dir, 'myplugin.py'), 'w')
    f.write(PLUGIN)
    f.close()

    class MyApp(TestApp):
        class Meta:
            config_defaults = defaults
            plugin_config_dir = tmp.dir
            plugin_dir = tmp.dir
            plugin_bootstrap = None

    with MyApp() as app:
        assert 'myplugin' in app.plugin._enabled_plugins
        assert 'myplugin' not in app.plugin._disabled_plugins


def test_load_order_presedence_four(tmp):
    # multiple plugin configs, first plugin conf defines it as enabled,
    # but last read should make it disabled.
    defaults = init_defaults('plugin.myplugin')

    f = open(os.path.join(tmp.dir, 'a.conf'), 'w')
    f.write(CONF1)  # enabled config
    f.close()

    f = open(os.path.join(tmp.dir, 'b.conf'), 'w')
    f.write(CONF2)  # disabled config
    f.close()

    f = open(os.path.join(tmp.dir, 'myplugin.py'), 'w')
    f.write(PLUGIN)
    f.close()

    class MyApp(TestApp):
        class Meta:
            config_defaults = defaults
            plugin_config_dir = tmp.dir
            plugin_dir = tmp.dir
            plugin_bootstrap = None

    with MyApp() as app:
        assert 'myplugin' in app.plugin._disabled_plugins
        assert 'myplugin' not in app.plugin._enabled_plugins


def test_load_order_presedence_five(tmp):
    # Multiple plugin configs, enable -> disabled -> enable
    defaults = init_defaults('plugin.myplugin')

    f = open(os.path.join(tmp.dir, 'a.conf'), 'w')
    f.write(CONF1)  # enabled config
    f.close()

    f = open(os.path.join(tmp.dir, 'b.conf'), 'w')
    f.write(CONF2)  # disabled config
    f.close()

    f = open(os.path.join(tmp.dir, 'c.conf'), 'w')
    f.write(CONF1)  # enabled config
    f.close()

    f = open(os.path.join(tmp.dir, 'd.conf'), 'w')
    f.write(CONF2)  # disabled config
    f.close()

    f = open(os.path.join(tmp.dir, 'e.conf'), 'w')
    f.write(CONF1)  # enabled config
    f.close()

    f = open(os.path.join(tmp.dir, 'myplugin.py'), 'w')
    f.write(PLUGIN)
    f.close()

    class MyApp(TestApp):
        class Meta:
            config_defaults = defaults
            plugin_config_dir = tmp.dir
            plugin_dir = tmp.dir
            plugin_bootstrap = None

    with MyApp() as app:
        assert 'myplugin' in app.plugin._enabled_plugins
        assert 'myplugin' not in app.plugin._disabled_plugins


def test_load_plugins_from_config(tmp):
    f = open(os.path.join(tmp.dir, 'myplugin.py'), 'w')
    f.write(PLUGIN)
    f.close()

    defaults = init_defaults('plugin.myplugin', 'plugin.myplugin2')
    defaults['plugin.myplugin']['enabled'] = True
    defaults['plugin.myplugin2']['enabled'] = False

    class MyApp(TestApp):
        class Meta:
            config_defaults = defaults
            plugin_config_dir = tmp.dir
            plugin_dir = tmp.dir
            plugin_bootstrap = None

    with MyApp() as app:
        han = app.handler.get('output', 'my_output_handler')()
        assert han._meta.label == 'my_output_handler'

        # some more checks for coverage

        assert 'myplugin' in app.plugin.get_enabled_plugins()
        assert 'myplugin' in app.plugin.get_loaded_plugins()
        assert 'myplugin2' in app.plugin.get_disabled_plugins()
        assert 'myplugin2' not in app.plugin.get_enabled_plugins()
        assert 'myplugin2' not in app.plugin.get_loaded_plugins()


def test_disabled_plugins_from_files(tmp):
    f = open(os.path.join(tmp.dir, 'myplugin.conf'), 'w')
    f.write(CONF2)
    f.close()

    f = open(os.path.join(tmp.dir, 'myplugin.py'), 'w')
    f.write(PLUGIN)
    f.close()

    class MyApp(TestApp):
        class Meta:
            plugin_config_dir = tmp.dir
            plugin_dir = tmp.dir
            plugin_bootstrap = None

    with MyApp() as app:
        assert 'my_output_handler' not in app.handler.__handlers__['output']
        assert 'myplugin2' not in app.plugin.get_enabled_plugins()


def test_bogus_plugin_from_files(tmp):
    f = open(os.path.join(tmp.dir, 'myplugin.conf'), 'w')
    f.write(CONF3)
    f.close()

    # do this for coverage... empty config file
    f = open(os.path.join(tmp.dir, 'bogus.conf'), 'w')
    f.write(CONF5)
    f.close()

    class MyApp(TestApp):
        class Meta:
            plugin_config_dir = tmp.dir
            plugin_dir = tmp.dir
            plugin_bootstrap = None

    with MyApp() as app:
        assert 'bogus_plugin' not in app.plugin.get_enabled_plugins()


def test_bad_plugin_dir(tmp):
    f = open(os.path.join(tmp.dir, 'myplugin.conf'), 'w')
    f.write(CONF1)
    f.close()

    class MyApp(TestApp):
        class Meta:
            plugin_config_dir = tmp.dir
            plugin_dir = './some/bogus/path'
            plugin_bootstrap = None

    with raises(FrameworkError, match="Unable to load plugin 'myplugin'."):
        with MyApp():
            pass


def test_load_plugin_from_module(tmp):
    # We mock this out by loading a cement ext, but it is essentially the
    # same type of code.
    if 'cement.ext.ext_json' in sys.modules:
        del sys.modules['cement.ext.ext_json']

    f = open(os.path.join(tmp.dir, 'ext_json.conf'), 'w')
    f.write(CONF4)
    f.close()

    class MyApp(TestApp):
        class Meta:
            plugin_config_dir = tmp.dir
            plugin_dir = tmp.dir
            plugin_bootstrap = 'cement.ext'

    with MyApp() as app:
        assert 'ext_json' in app.plugin.get_enabled_plugins()
