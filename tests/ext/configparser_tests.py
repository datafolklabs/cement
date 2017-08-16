
from cement.utils import test
from cement.utils.misc import rando

APP = rando()[:12]

CONFIG = """
[my_section]
my_param = my_value
"""

@test.attr('core')
class ConfigParserConfigHandlerTestCase(test.CementExtTestCase):

    def setUp(self):
        super(ConfigParserConfigHandlerTestCase, self).setUp()
        f = open(self.tmp_file, 'w+')
        f.write(CONFIG)
        f.close()
        self.app = self.make_app(
            APP,
            extensions=['configparser'],
            config_handler='configparser',
            config_files=[self.tmp_file],
            argv=[]
        )

    def test_configparser(self):
        self.app.setup()

    def test_get_dict(self):
        self.app.setup()
        self.ok(isinstance(self.app.config.get_dict(), dict))

    def test_get_dict_deep(self):
        self.app.setup()
        self.ok(isinstance(self.app.config.get_dict(), dict))
        self.eq(
            self.app.config.get_dict()["my_section"],
            dict(my_param="my_value"),
        )

    def test_override(self):
        # test arguments_override_config
        self.app = self.make_app(
            APP,
            argv=['--my_param=not_my_value'],
            arguments_override_config=True,
            config_handler='configparser',
            config_files=[self.tmp_file],
            extensions=['configparser'],
            meta_override=['my_param'],
        )
        self.app.setup()
        self.app.args.add_argument('--my_param', action='store')
        self.app.run()
        self.eq(self.app.config.get('my_section', 'my_param'), 'not_my_value')
