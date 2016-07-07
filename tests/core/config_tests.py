"""Tests for cement.core.config."""

import os
from cement.core import exc, config, backend
from cement.utils import test

CONFIG = """
[my_section]
my_param = my_value
"""


class BogusConfigHandler(config.CementConfigHandler):

    class Meta:
        label = 'bogus'


class ConfigTestCase(test.CementCoreTestCase):

    @test.raises(exc.InterfaceError)
    def test_invalid_config_handler(self):
            self.app.handler.register(BogusConfigHandler)

    @test.raises(NotImplementedError)
    def test_parse_file_not_implemented(self):
        c = config.CementConfigHandler()
        c._setup(self.app)
        c._parse_file(self.tmp_file)

    def test_has_key(self):
        self.app.setup()
        self.ok(self.app.config.has_section(self.app._meta.config_section))

    def test_config_override(self):
        defaults = dict()
        defaults['test'] = dict()
        defaults['test']['debug'] = False
        defaults['test']['foo'] = 'bar'

        # first test that it doesn't override the config with the default
        # setting of arguments_override_config=False
        self.app = self.make_app(
            config_defaults=defaults,
            argv=['--foo=not_bar'],
            arguments_override_config=False
        )
        self.app.setup()
        self.app.args.add_argument('--foo', action='store')
        self.app.run()
        self.eq(self.app.config.get('test', 'foo'), 'bar')

        # then make sure that it does
        self.app = self.make_app(
            config_defaults=defaults,
            argv=['--foo=not_bar'],
            arguments_override_config=True,
            meta_override=['foo'],
        )
        self.app.setup()
        self.app.args.add_argument('--foo', action='store')
        self.app.run()
        self.eq(self.app.config.get('test', 'foo'), 'not_bar')

        # one last test just for code coverage
        self.app = self.make_app(
            config_defaults=defaults,
            argv=['--debug'],
            arguments_override_config=True
        )
        self.app.setup()
        self.app.args.add_argument('--foo', action='store')
        self.app.run()
        self.eq(self.app.config.get('test', 'foo'), 'bar')

    def test_parse_file_bad_path(self):
        self.app._meta.config_files = ['./some_bogus_path']
        self.app.setup()

    def test_parse_file(self):
        f = open(self.tmp_file, 'w+')
        f.write(CONFIG)
        f.close()
        self.app._meta.config_files = [self.tmp_file]
        self.app.setup()
        self.eq(self.app.config.get('my_section', 'my_param'), 'my_value')
