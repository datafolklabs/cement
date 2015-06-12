"""Tests for cement.ext.ext_yaml_configobj."""

import os
import sys
import yaml
from tempfile import mkstemp
from cement.core import handler, hook
from cement.utils import test

if sys.version_info[0] < 3:
    import configobj
else:
    raise test.SkipTest(
        'ConfigObj does not support Python 3')  # pragma: no cover


class YamlConfigObjExtTestCase(test.CementTestCase):
    CONFIG = '''
        section:
            subsection:
                list:
                    - item1
                    - item2
                    - item3
                    - item4
                key: value
            key1: ok1
            key2: ok2
    '''
    CONFIG_PARSED = dict(
        section=dict(
            subsection=dict(
                list=['item1', 'item2', 'item3', 'item4'],
                key='value'),
            key1='ok1',
            key2='ok2',
        ),
    )

    def setUp(self):
        _, self.tmppath = mkstemp()
        f = open(self.tmppath, 'w+')
        f.write(self.CONFIG)
        f.close()
        self.app = self.make_app('tests',
                                 extensions=['yaml_configobj'],
                                 config_handler='yaml_configobj',
                                 config_files=[self.tmppath],
                                 )

    def tearDown(self):
        if os.path.exists(self.tmppath):
            os.remove(self.tmppath)

    def test_has_section(self):
        self.app.setup()
        self.ok(self.app.config.has_section('section'))

    def test_keys(self):
        self.app.setup()
        res = 'subsection' in self.app.config.keys('section')
        self.ok(res)

    def test_parse_file_bad_path(self):
        self.app._meta.config_files = ['./some_bogus_path']
        self.app.setup()

    def test_parse_file(self):
        self.app.setup()
        self.eq(self.app.config.get('section', 'key1'), 'ok1')

        self.eq(self.app.config.get_section_dict('section'),
                self.CONFIG_PARSED['section'])
