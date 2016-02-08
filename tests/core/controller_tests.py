"""Tests for cement.core.controller."""

import re
from cement.core import exc, controller
from cement.utils import test
from cement.utils.misc import rando, init_defaults

APP = "app-%s" % rando()[:12]


class TestController(controller.CementBaseController):

    class Meta:
        label = 'base'
        arguments = [
            (['-f', '--foo'], dict(help='foo option'))
        ]
        usage = 'My Custom Usage TXT'
        epilog = "This is the epilog"

    @controller.expose(hide=True)
    def default(self):
        pass

    @controller.expose()
    def some_command(self):
        pass


class TestWithPositionalController(controller.CementBaseController):

    class Meta:
        label = 'base'
        arguments = [
            (['foo'], dict(help='foo option', nargs='?'))
        ]

    @controller.expose(hide=True)
    def default(self):
        self.app.render(dict(foo=self.app.pargs.foo))


class Embedded(controller.CementBaseController):

    class Meta:
        label = 'embedded_controller'
        stacked_on = 'base'
        stacked_type = 'embedded'
        arguments = [(['-t'], dict())]

    @controller.expose(aliases=['emcmd1'], help='This is my help txt')
    def embedded_cmd1(self):
        pass


class Nested(controller.CementBaseController):

    class Meta:
        label = 'nested_controller'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [(['-t'], dict())]

    @controller.expose()
    def nested_cmd1(self):
        pass


class AliasesOnly(controller.CementBaseController):

    class Meta:
        label = 'aliases_only_controller'
        stacked_on = 'base'
        stacked_type = 'nested'
        aliases = ['this_is_ao_controller']
        aliases_only = True

    @controller.expose(aliases=['ao_cmd1'], aliases_only=True)
    def aliases_only_cmd1(self):
        pass

    @controller.expose(aliases=['ao_cmd2', 'ao2'], aliases_only=True)
    def aliases_only_cmd2(self):
        pass


class DuplicateCommand(controller.CementBaseController):

    class Meta:
        label = 'duplicate_command'
        stacked_on = 'base'
        stacked_type = 'embedded'

    @controller.expose()
    def default(self):
        pass


class DuplicateAlias(controller.CementBaseController):

    class Meta:
        label = 'duplicate_command'
        stacked_on = 'base'
        stacked_type = 'embedded'

    @controller.expose(aliases=['default'])
    def cmd(self):
        pass


class Bad(controller.CementBaseController):

    class Meta:
        label = 'bad_controller'
        arguments = []


class BadStackedType(controller.CementBaseController):

    class Meta:
        label = 'bad_stacked_type'
        stacked_on = 'base'
        stacked_type = 'bogus'
        arguments = []


class ArgumentConflict(controller.CementBaseController):

    class Meta:
        label = 'embedded'
        stacked_on = 'base'
        stacked_type = 'embedded'
        arguments = [(['-f', '--foo'], dict())]


class Unstacked(controller.CementBaseController):

    class Meta:
        label = 'unstacked'
        stacked_on = None
        arguments = [
            (['--foo6'], dict(dest='foo6')),
        ]


class BadStackType(controller.CementBaseController):

    class Meta:
        label = 'bad_stack_type'
        stacked_on = 'base'
        stacked_type = 'bogus_stacked_type'
        arguments = [
            (['--foo6'], dict(dest='foo6')),
        ]


class ControllerTestCase(test.CementCoreTestCase):

    def test_default(self):
        app = self.make_app(base_controller=TestController)
        app.setup()
        app.run()

    def test_epilog(self):
        app = self.make_app(base_controller=TestController)
        app.setup()
        app.run()
        self.eq(app.args.epilog, 'This is the epilog')

    def test_txt_defined_base_controller(self):
        self.app.handler.register(TestController)
        self.app.setup()

    @test.raises(exc.InterfaceError)
    def test_invalid_arguments_1(self):
        Bad.Meta.arguments = ['this is invalid']
        self.app.handler.register(Bad)

    @test.raises(exc.InterfaceError)
    def test_invalid_arguments_2(self):
        Bad.Meta.arguments = [('this is also invalid', dict())]
        self.app.handler.register(Bad)

    @test.raises(exc.InterfaceError)
    def test_invalid_arguments_3(self):
        Bad.Meta.arguments = [(['-f'], 'and this is invalid')]
        self.app.handler.register(Bad)

    @test.raises(exc.InterfaceError)
    def test_invalid_arguments_4(self):
        Bad.Meta.arguments = 'totally jacked'
        self.app.handler.register(Bad)

    def test_embedded_controller(self):
        app = self.make_app(argv=['embedded-cmd1'])
        app.handler.register(TestController)
        app.handler.register(Embedded)
        app.setup()
        app.run()

        check = 'embedded-cmd1' in app.controller._visible_commands
        self.ok(check)

        # also check for the alias here
        check = 'emcmd1' in app.controller._dispatch_map
        self.ok(check)

    def test_nested_controller(self):
        app = self.make_app(argv=['nested-controller'])
        app.handler.register(TestController)
        app.handler.register(Nested)
        app.setup()
        app.run()

        check = 'nested-controller' in app.controller._visible_commands
        self.ok(check)

        self.eq(app.controller._dispatch_command['func_name'], '_dispatch')

    def test_aliases_only_controller(self):
        app = self.make_app(argv=['aliases-only-controller'])
        app.handler.register(TestController)
        app.handler.register(AliasesOnly)
        app.setup()
        app.run()

    @test.raises(exc.FrameworkError)
    def test_bad_stacked_type(self):
        app = self.make_app()
        app.handler.register(TestController)
        app.handler.register(BadStackedType)
        app.setup()
        app.run()

    @test.raises(exc.FrameworkError)
    def test_duplicate_command(self):
        app = self.make_app()
        app.handler.register(TestController)
        app.handler.register(DuplicateCommand)
        app.setup()
        app.run()

    @test.raises(exc.FrameworkError)
    def test_duplicate_alias(self):
        app = self.make_app()
        app.handler.register(TestController)
        app.handler.register(DuplicateAlias)
        app.setup()
        app.run()

    def test_usage_txt(self):
        app = self.make_app()
        app.handler.register(TestController)
        app.setup()
        self.eq(app.controller._usage_text, 'My Custom Usage TXT')

    @test.raises(exc.FrameworkError)
    def test_argument_conflict(self):
        try:
            app = self.make_app(base_controller=TestController)
            app.handler.register(ArgumentConflict)
            app.setup()
            app.run()
        except NameError as e:
            # This is a hack due to a Travis-CI Bug:
            # https://github.com/travis-ci/travis-ci/issues/998
            if e.args[0] == "global name 'ngettext' is not defined":
                bug = "https://github.com/travis-ci/travis-ci/issues/998"
                raise test.SkipTest("Travis-CI Bug: %s" % bug)
            else:
                raise

    def test_default_command_with_positional(self):
        app = self.make_app(base_controller=TestWithPositionalController,
                            argv=['mypositional'])
        app.setup()
        app.run()
        self.eq(app.get_last_rendered()[0]['foo'], 'mypositional')

    def test_load_extensions_from_config_list(self):
        defaults = init_defaults(APP)
        defaults[APP]['extensions'] = ['json', 'yaml']

        app = self.make_app(
            label=APP,
            extensions=[],
            config_defaults=defaults,
        )
        app.setup()
        app.run()

        res = 'cement.ext.ext_json' in app.ext._loaded_extensions
        self.ok(res)

        res = 'cement.ext.ext_yaml' in app.ext._loaded_extensions
        self.ok(res)

    def test_load_extensions_from_config_str(self):
        defaults = init_defaults(APP)
        defaults[APP]['extensions'] = 'json, yaml'

        app = self.make_app(
            label=APP,
            extensions=[],
            config_defaults=defaults,
        )
        app.setup()
        app.run()

        res = 'cement.ext.ext_json' in app.ext._loaded_extensions
        self.ok(res)

        res = 'cement.ext.ext_yaml' in app.ext._loaded_extensions
        self.ok(res)

    @test.raises(exc.InterfaceError)
    def test_invalid_stacked_on(self):
        self.reset_backend()
        try:
            self.app = self.make_app(APP,
                                     handlers=[
                                         TestController,
                                         Unstacked,
                                     ],
                                     )
            with self.app as app:
                res = app.run()
        except exc.InterfaceError as e:
            self.ok(re.match("(.*)is not stacked anywhere!(.*)", e.msg))
            raise

    @test.raises(exc.InterfaceError)
    def test_invalid_stacked_type(self):
        self.reset_backend()
        try:
            self.app = self.make_app(APP,
                                     handlers=[
                                         TestController,
                                         BadStackType,
                                     ],
                                     )
            with self.app as app:
                res = app.run()
        except exc.InterfaceError as e:
            self.ok(re.match("(.*)has an unknown stacked type(.*)", e.msg))
            raise

    def test_usage_text(self):
        self.reset_backend()
        self.app = self.make_app(APP,
                                 handlers=[
                                     TestController,
                                 ],
                                 )
        with self.app as app:
            self.app.controller._meta.usage = None
            usage = app.controller._usage_text
            self.ok(usage.startswith('%s (sub-commands ...)' %
                                     self.app._meta.label))

    def test_help_text(self):
        self.reset_backend()
        self.app = self.make_app(APP,
                                 handlers=[
                                     TestController,
                                     AliasesOnly,
                                 ],
                                 )
        with self.app as app:
            app.run()
            help = app.controller._help_text
            # self.ok(usage.startswith('%s (sub-commands ...)' % \
            #         self.app._meta.label))
