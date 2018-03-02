
from cement.ext.ext_plugin import CementPluginHandler


# module tests

class TestCementPluginHandler(object):
    def test_subclassing(self):
        class MyPluginHandler(CementPluginHandler):
            class Meta:
                label = 'my_plugin_handler'

        h = MyPluginHandler()
        assert h._meta.interface == 'plugin'
        assert h._meta.label == 'my_plugin_handler'


# app functionality and coverage tests
