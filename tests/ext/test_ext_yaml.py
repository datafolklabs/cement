
import yaml
from cement.utils.test import *


# CONFIG = '''
#     section:
#         subsection:
#             list:
#                 - item1
#                 - item2
#                 - item3
#                 - item4
#             key: value
#         key1: ok1
#         key2: ok2
# '''

CONFIG_PARSED = dict(
    section=dict(
        subsection=dict(
            list=['item1', 'item2', 'item3', 'item4'],
            key='value'),
        key1='ok1',
        key2='ok2',
    ),
)

CONFIG = fs.join(os.path.dirname(__file__), '..', 'data', 'config', 'config.yml')

class YamlApp(TestApp):
    class Meta:
        extensions = ['yaml']
        output_handler = 'yaml'
        config_handler = 'yaml'
        config_files = [CONFIG]
        argv = ['-o', 'yaml']


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
    with YamlApp(config_files=['./some_bogus_path']) as app:
        pass


def test_parse_file():
    with YamlApp() as app:
        assert app.config.get('section', 'key1') == 'ok1'
        assert app.config.get_section_dict('section') == \
               CONFIG_PARSED['section']


def test_handler_override_options_is_none():
    class MyApp(YamlApp):
        class Meta:
            core_handler_override_options = {}
            handler_override_options = {}
            argv = []

    with MyApp() as app:
        app.run()
        app.render(dict(foo='bar'))

def test_get_dict():
    with YamlApp() as app:
        _config = app.config.get_dict()
        assert _config['log.logging']['level'] == 'INFO'
