import os
import yaml
from unittest.mock import patch
from cement.utils.test import TestApp
from cement.utils import fs


CONFIG_PARSED = dict(
    section=dict(
        subsection=dict(
            list=['item1', 'item2', 'item3', 'item4'],
            key='value'),
        key1='ok1',
        key2='ok2',
    ),
)

CONFIG = fs.join(os.path.dirname(__file__), '..',
                 'data', 'config', 'config.yml')


class YamlApp(TestApp):
    class Meta:
        extensions = ['yaml']
        output_handler = 'yaml'
        config_handler = 'yaml'
        config_files = [CONFIG]
        argv = ['-o', 'yaml']
        meta_defaults = {'output.yaml': {'overridable': True}}


def test_yaml():
    with YamlApp() as app:
        app.run()
        res = app.render(dict(foo='bar'))
        yaml_res = yaml.dump(dict(foo='bar'))
        assert res == yaml_res


def test_has_section():
    with YamlApp() as app:
        assert app.config.has_section('section')


def test_keys():
    with YamlApp() as app:
        assert 'subsection' in app.config.keys('section')


def test_parse_file_bad_path():
    with patch('cement.ext.ext_yaml.YamlConfigHandler._parse_file') as pf:
        with YamlApp(config_files=['./some_bogus_path']):
            assert not pf.called


def test_parse_file():
    with YamlApp() as app:
        assert app.config.get('section', 'key1') == 'ok1'
        assert app.config.get_section_dict('section') == \
            CONFIG_PARSED['section']


def test_get_dict():
    with YamlApp() as app:
        _config = app.config.get_dict()
        assert _config['log.logging']['level'] == 'INFO'
