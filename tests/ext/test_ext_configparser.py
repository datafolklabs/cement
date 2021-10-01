
import os
from cement.core.foundation import TestApp
from cement.ext.ext_configparser import ConfigParserConfigHandler


# module tests

class TestConfigParserConfigHandler(object):
    def test_subclassing(self):
        class MyConfigHandler(ConfigParserConfigHandler):
            class Meta:
                label = 'my_config_handler'

        h = MyConfigHandler()
        assert h._meta.interface == 'config'
        assert h._meta.label == 'my_config_handler'


# app functionality and coverage tests

def test_get_dict():
    with TestApp() as app:
        assert isinstance(app.config.get_dict(), dict)
        _config = app.config.get_dict()
        assert _config['log.logging']['level'] == 'INFO'


def test_env_var_override():
    with TestApp(config_section='testapp') as app:
        app.config.set('testapp', 'foo', 'bar')

        env_var = "TESTAPP_FOO"
        assert app.config.get('testapp', 'foo') == 'bar'
        section_dict = app.config.get_section_dict('testapp')
        assert section_dict['foo'] == 'bar'

        os.environ[env_var] = 'not-bar'
        assert app.config.get('testapp', 'foo') == 'not-bar'
        section_dict = app.config.get_section_dict('testapp')
        assert section_dict['foo'] == 'not-bar'

        # do again but in another config namespace

        app.config.add_section('dummy')
        app.config.set('dummy', 'foo', 'bar')

        env_var = "TESTAPP_DUMMY_FOO"
        assert app.config.get('dummy', 'foo') == 'bar'
        section_dict = app.config.get_section_dict('dummy')
        assert section_dict['foo'] == 'bar'

        os.environ[env_var] = 'dummy-not-bar'
        assert app.config.get('dummy', 'foo') == 'dummy-not-bar'
        section_dict = app.config.get_section_dict('dummy')
        assert section_dict['foo'] == 'dummy-not-bar'

        # issue/590 - don't sub underscores

        app.config.set('testapp', '__foo__', 'bar')
        env_var = "TESTAPP___FOO__"

        os.environ[env_var] = 'not-bar'
        assert app.config.get('testapp', '__foo__') == 'not-bar'
        section_dict = app.config.get_section_dict('testapp')
        assert section_dict['__foo__'] == 'not-bar'


def test_get_boolean():
    with TestApp(config_section='testapp') as app:
        app.config.set('testapp', 'foobool', 'true')
        assert app.config['testapp'].getboolean('foobool') is True

        app.config.set('testapp', 'foobool', 'no')
        assert app.config['testapp'].getboolean('foobool') is False

        os.environ['TESTAPP_FOOBOOL'] = '1'
        assert app.config['testapp'].getboolean('foobool') is True
