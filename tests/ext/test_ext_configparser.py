
from pytest import raises

from cement.core.foundation import TestApp
from cement.core.exc import FrameworkError
from cement.ext.ext_configparser import ConfigParserConfigHandler


### module tests

class TestConfigParserConfigHandler(object):
    def test_subclassing(self):
        class MyConfigHandler(ConfigParserConfigHandler):
            class Meta:
                label = 'my_config_handler'


        h = MyConfigHandler()
        assert h._meta.interface == 'config'
        assert h._meta.label == 'my_config_handler'


### app functionality and coverage tests
