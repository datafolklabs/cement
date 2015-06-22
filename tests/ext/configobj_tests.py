"""Tests for cement.ext.ext_configobj."""

import os
import sys
from tempfile import mkstemp
from cement.core import handler, backend, log
from cement.utils import test
from cement.utils.misc import rando

if sys.version_info[0] < 3:
    import configobj
else:
    raise test.SkipTest(
        'ConfigObj does not support Python 3')  # pragma: no cover


APP = rando()[:12]

CONFIG = """
[my_section]
my_param = my_value
"""


class ConfigObjExtTestCase(test.CementTestCase):

    def setUp(self):
        _, self.tmppath = mkstemp()
        f = open(self.tmppath, 'w+')
        f.write(CONFIG)
        f.close()
        self.app = self.make_app(APP,
                                 extensions=['configobj'],
                                 config_handler='configobj',
                                 config_files=[self.tmppath],
                                 argv=[]
                                 )

    def tearDown(self):
        if os.path.exists(self.tmppath):
            os.remove(self.tmppath)

    def test_configobj(self):
        self.app.setup()

    def test_has_section(self):
        self.app.setup()
        self.ok(self.app.config.has_section('my_section'))

    def test_keys(self):
        self.app.setup()
        res = 'my_param' in self.app.config.keys('my_section')
        self.ok(res)

    def test_parse_file_bad_path(self):
        self.app._meta.config_files = ['./some_bogus_path']
        self.app.setup()

    def test_parse_file(self):
        self.app.setup()
        self.eq(self.app.config.get('my_section', 'my_param'), 'my_value')

        self.eq(self.app.config.get_section_dict('my_section'),
                {'my_param': 'my_value'})
