"""Tests for cement.ext.ext_configobj."""

import sys
from tempfile import mkstemp
from cement.core import handler, backend, log
from cement.utils import test

if sys.version_info[0] < 3:
    import configobj
else:
    raise test.SkipTest('ConfigObj does not support Python 3') # pragma: no cover


CONFIG = """
[my_section]
my_param = my_value
"""

class ConfigObjExtTestCase(test.CementTestCase):
    def setUp(self):
        self.app = self.make_app('myapp',
            extensions=['configobj'],
            config_handler='configobj',
            argv=[]
            )

    def test_configobj(self):
        self.app.setup()

    def test_keys(self):
        _, tmppath = mkstemp()
        f = open(tmppath, 'w+')
        f.write(CONFIG)
        f.close()
        self.app._meta.config_files = [tmppath]
        self.app.setup()
        res = 'my_param' in self.app.config.keys('my_section')
        self.ok(res)

    def test_parse_file_bad_path(self):
        self.app._meta.config_files = ['./some_bogus_path']
        self.app.setup()

    def test_parse_file(self):
        _, tmppath = mkstemp()
        f = open(tmppath, 'w+')
        f.write(CONFIG)
        f.close()
        self.app._meta.config_files = [tmppath]
        self.app.setup()
        self.eq(self.app.config.get('my_section', 'my_param'), 'my_value')

        self.eq(self.app.config.get_section_dict('my_section'),
                {'my_param': 'my_value'})
