
import sys
from pytest import raises, skip
from unittest.mock import patch
from argparse import ArgumentError
from cement.core.foundation import TestApp
from cement.ext.ext_argparse import ArgparseArgumentHandler
from cement.ext.ext_argparse import ArgparseController, expose
from cement.ext.ext_argparse import _clean_label, _clean_func
from cement.core.exc import FrameworkError


if (sys.version_info[0] >= 3 and sys.version_info[1] >= 4):
    ARGPARSE_SUPPORTS_DEFAULTS = True
else:
    ARGPARSE_SUPPORTS_DEFAULTS = False


class Base(ArgparseController):

    class Meta:
        label = 'base'
        arguments = [
            (['--foo'], dict(dest='foo')),
        ]

    @expose(hide=True, help="this help doesn't get seen")
    def _default(self):
        return "Inside Base.default"

    @expose()
    def cmd1(self):
        return "Inside Base.cmd1"

    @expose()
    def command_with_dashes(self):
        return "Inside Base.command_with_dashes"


class Second(ArgparseController):

    class Meta:
        label = 'second'
        stacked_on = 'base'
        stacked_type = 'embedded'
        arguments = [
            (['--foo2'], dict(dest='foo2')),
        ]

    @expose(
        arguments=[
            (['--cmd2-foo'],
             dict(help='cmd2 sub-command only options', dest='cmd2_foo')),
        ]
    )
    def cmd2(self):
        if self.app.pargs.cmd2_foo:
            return "Inside Second.cmd2 : Foo > %s" % self.app.pargs.cmd2_foo
        else:
            return "Inside Second.cmd2"


class Third(ArgparseController):

    class Meta:
        label = 'third'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
            (['--foo3'], dict(dest='foo3')),
        ]

    @expose(hide=True)
    def _default(self):
        return "Inside Third.default"

    @expose()
    def cmd3(self):
        return "Inside Third.cmd3"


class Fourth(ArgparseController):

    class Meta:
        label = 'fourth'
        stacked_on = 'third'
        stacked_type = 'embedded'
        hide = True
        help = "this help doesn't get seen cause we're hiding"
        arguments = [
            (['--foo4'], dict(dest='foo4')),
        ]

    @expose()
    def cmd4(self):
        return "Inside Fourth.cmd4"


class Fifth(ArgparseController):

    class Meta:
        label = 'fifth'
        stacked_on = 'third'
        stacked_type = 'nested'
        hide = True
        help = "this help isn't seen... i'm hiding"
        arguments = [
            (['--foo5'], dict(dest='foo5')),
        ]

    @expose(hide=True)
    def _default(self):
        return "Inside Fifth.default"

    @expose()
    def cmd5(self):
        return "Inside Fifth.cmd5"


class Sixth(ArgparseController):

    class Meta:
        label = 'sixth'
        stacked_on = 'fifth'
        stacked_type = 'nested'
        arguments = [
            (['--foo6'], dict(dest='foo6')),
        ]

    @expose(hide=True)
    def _default(self):
        return "Inside Sixth.default"

    @expose()
    def cmd6(self):
        return "Inside Sixth.cmd6"


class Seventh(ArgparseController):

    class Meta:
        label = 'seventh'
        stacked_on = 'fourth'
        stacked_type = 'embedded'
        arguments = [
            (['--foo7'], dict(dest='foo7')),
        ]

    @expose()
    def cmd7(self):
        return "Inside Seventh.cmd7"


class Unstacked(ArgparseController):

    class Meta:
        label = 'unstacked'
        stacked_on = None
        arguments = [
            (['--foo6'], dict(dest='foo6')),
        ]


class BadStackType(ArgparseController):

    class Meta:
        label = 'bad_stack_type'
        stacked_on = 'base'
        stacked_type = 'bogus_stacked_type'
        arguments = [
            (['--foo6'], dict(dest='foo6')),
        ]


class DuplicateArguments(ArgparseController):

    class Meta:
        label = 'duplicate_arguments'
        arguments = [
            (['--foo'], dict(dest='foo')),
        ]


class ControllerCommandDuplicateArguments(ArgparseController):

    class Meta:
        label = 'controller_command_duplicate_arguments'

    @expose(
        arguments=[
            (['--foo'], dict(dest='foo')),
            (['--foo'], dict(dest='foo')),
        ]
    )
    def sub_command(self):
        pass


class AlternativeDefault(ArgparseController):

    class Meta:
        label = 'alternative_default'
        default_func = 'alternative_default'
        stacked_on = 'base'
        stacked_type = 'nested'

    @expose(hide=True)
    def alternative_default(self):
        return "Inside AlternativeDefault.alternative_default"


class BadAlternativeDefault(ArgparseController):

    class Meta:
        label = 'bad_alternative_default'
        default_func = 'bogus_default'
        stacked_on = 'base'
        stacked_type = 'nested'


class Aliases(ArgparseController):

    class Meta:
        label = 'aliases'
        aliases = ['aliases-controller', 'ac']
        stacked_on = 'base'
        stacked_type = 'nested'

    @expose(aliases=['aliases-cmd-1', 'ac1'])
    def aliases_cmd1(self):
        return "Inside Aliases.aliases_cmd1"


class ArgparseApp(TestApp):
    class Meta:
        argument_handler = ArgparseArgumentHandler
        handlers = [
            Sixth,
            Base,
            Second,
            Third,
            Fourth,
            Fifth,
            Seventh,
        ]


def test_clean_label():
    assert _clean_label('some_cmd_name') == 'some-cmd-name'


def test_clean_func():
    assert _clean_func('some-cmd-name') == 'some_cmd_name'
    assert _clean_func(None) is None


def test_base_default():
    if not ARGPARSE_SUPPORTS_DEFAULTS:
        skip('Argparse does not support default commands in Python < 3.4')

    with ArgparseApp() as app:
        res = app.run()
        assert res == "Inside Base.default"


def test_base_cmd1():
    with ArgparseApp(argv=['cmd1']) as app:
        res = app.run()
        assert res == "Inside Base.cmd1"


def test_base_command_with_dashes():
    with ArgparseApp(argv=['command-with-dashes']) as app:
        res = app.run()
        assert res == "Inside Base.command_with_dashes"


def test_controller_commands():
    with ArgparseApp(argv=['cmd2']) as app:
        res = app.run()
        assert res == "Inside Second.cmd2"

    with ArgparseApp(argv=['third', 'cmd3']) as app:
        res = app.run()
        assert res == "Inside Third.cmd3"

    with ArgparseApp(argv=['third', 'cmd4']) as app:
        res = app.run()
        assert res == "Inside Fourth.cmd4"

    with ArgparseApp(argv=['third', 'fifth', 'cmd5']) as app:
        res = app.run()
        assert res == "Inside Fifth.cmd5"

    with ArgparseApp(argv=['third', 'fifth', 'sixth', 'cmd6']) as app:
        res = app.run()
        assert res == "Inside Sixth.cmd6"

    with ArgparseApp(argv=['third', 'cmd7']) as app:
        res = app.run()
        assert res == "Inside Seventh.cmd7"


def test_base_cmd1_parsing():
    with ArgparseApp(argv=['--foo=bar', 'cmd1']) as app:
        res = app.run()
        assert res == "Inside Base.cmd1"
        assert app.pargs.foo == 'bar'


def test_second_cmd2():
    with ArgparseApp(argv=['--foo=bar', '--foo2=bar2', 'cmd2']) as app:
        res = app.run()
        assert res == "Inside Second.cmd2"
        assert app.pargs.foo == 'bar'
        assert app.pargs.foo2 == 'bar2'


def test_third_cmd3():
    argv = [
        '--foo=bar', '--foo2=bar2',
        'third', '--foo3=bar3', '--foo4=bar4', '--foo7=bar7', 'cmd3',
    ]

    with ArgparseApp(argv=argv) as app:
        res = app.run()
        assert res == "Inside Third.cmd3"
        assert app.pargs.foo == 'bar'
        assert app.pargs.foo2 == 'bar2'
        assert app.pargs.foo3 == 'bar3'
        assert app.pargs.foo4 == 'bar4'
        assert app.pargs.foo7 == 'bar7'


def test_fifth_cmd5():
    argv = [
        '--foo=bar', '--foo2=bar2',
        'third', '--foo3=bar3', '--foo4=bar4',
        'fifth', '--foo5=bar5', 'cmd5'
    ]

    with ArgparseApp(argv=argv) as app:
        res = app.run()
        assert res == "Inside Fifth.cmd5"
        assert app.pargs.foo == 'bar'
        assert app.pargs.foo2 == 'bar2'
        assert app.pargs.foo3 == 'bar3'
        assert app.pargs.foo4 == 'bar4'
        assert app.pargs.foo5 == 'bar5'


def test_sixth_cmd6():
    argv = [
        '--foo=bar', '--foo2=bar2',
        'third', '--foo3=bar3', '--foo4=bar4',
        'fifth', '--foo5=bar5', 'sixth', '--foo6=bar6', 'cmd6',
    ]

    with ArgparseApp(argv=argv) as app:
        res = app.run()
        assert res == "Inside Sixth.cmd6"
        assert app.pargs.foo == 'bar'
        assert app.pargs.foo2 == 'bar2'
        assert app.pargs.foo3 == 'bar3'
        assert app.pargs.foo4 == 'bar4'
        assert app.pargs.foo5 == 'bar5'
        assert app.pargs.foo6 == 'bar6'


def test_seventh_cmd7():
    argv = [
        '--foo=bar', '--foo2=bar2',
        'third', '--foo3=bar3', '--foo4=bar4', '--foo7=bar7', 'cmd7',
    ]

    with ArgparseApp(argv=argv) as app:
        res = app.run()
        assert res == "Inside Seventh.cmd7"
        assert app.pargs.foo == 'bar'
        assert app.pargs.foo2 == 'bar2'
        assert app.pargs.foo3 == 'bar3'
        assert app.pargs.foo4 == 'bar4'
        assert app.pargs.foo7 == 'bar7'


def test_collect():
    with ArgparseApp() as app:
        args = app.controller._collect_arguments()
        cmds = app.controller._collect_commands()
        args2, cmds2 = app.controller._collect()
        assert (args, cmds) == (args2, cmds2)


def test_controller_embedded_on_base():
    with ArgparseApp(argv=['cmd2']) as app:
        res = app.run()
        assert res == "Inside Second.cmd2"


def test_controller_command_arguments():
    with ArgparseApp(argv=['cmd2', '--cmd2-foo=bar2']) as app:
        res = app.run()
        assert res == "Inside Second.cmd2 : Foo > bar2"


def test_controller_default_nested_on_base():
    if not ARGPARSE_SUPPORTS_DEFAULTS:
        skip('Argparse does not support default commands in Python < 3.4')

    with ArgparseApp(argv=['third']) as app:
        res = app.run()
        assert res == "Inside Third.default"


def test_controller_command_nested_on_base():
    with ArgparseApp(argv=['third', 'cmd3']) as app:
        res = app.run()
        assert res == "Inside Third.cmd3"


def test_controller_doubled_embedded():
    with ArgparseApp(argv=['third', 'cmd4']) as app:
        res = app.run()
        assert res == "Inside Fourth.cmd4"


def test_controller_default_double_nested():
    if not ARGPARSE_SUPPORTS_DEFAULTS:
        skip('Argparse does not support default commands in Python < 3.4')

    with ArgparseApp(argv=['third', 'fifth']) as app:
        res = app.run()
        assert res == "Inside Fifth.default"


def test_controller_command_double_nested():
    with ArgparseApp(argv=['third', 'fifth', 'cmd5']) as app:
        res = app.run()
        assert res == "Inside Fifth.cmd5"


def test_alternative_default():
    if not ARGPARSE_SUPPORTS_DEFAULTS:
        skip('Argparse does not support default commands in Python < 3.4')

    class MyApp(ArgparseApp):
        class Meta:
            argv = ['alternative-default']
            handlers = [
                Base,
                AlternativeDefault,
            ]

    with MyApp() as app:
        res = app.run()
        assert res == "Inside AlternativeDefault.alternative_default"


def test_bad_alternative_default_command():
    if not ARGPARSE_SUPPORTS_DEFAULTS:
        skip('Argparse does not support default commands in Python < 3.4')

    class MyApp(ArgparseApp):
        class Meta:
            argv = ['bad-alternative-default']
            handlers = [
                Base,
                BadAlternativeDefault,
            ]

    with MyApp() as app:
        msg = "(.*)does not exist(.*)bogus_default(.*)"
        with raises(FrameworkError, match=msg):
            app.run()


def test_invalid_stacked_type():
    class MyApp(ArgparseApp):
        class Meta:
            argv = ['bad-alternative-default']
            handlers = [
                Base,
                BadStackType,
            ]

    with MyApp() as app:
        with raises(FrameworkError, match="(.*)Invalid stacked type(.*)"):
            app.run()


def test_duplicate_arguments():
    class MyApp(ArgparseApp):
        class Meta:
            argv = ['bad-alternative-default']
            handlers = [
                Base,
                DuplicateArguments,
            ]

    with MyApp() as app:
        with raises(ArgumentError, match="(.*)conflicting option string(.*)"):
            app.run()


def test_controller_command_duplicate_arguments():
    class MyApp(ArgparseApp):
        class Meta:
            argv = ['bad-alternative-default']
            handlers = [
                Base,
                ControllerCommandDuplicateArguments,
            ]

    with MyApp() as app:
        with raises(ArgumentError, match="(.*)conflicting option string(.*)"):
            app.run()


def test_aliases():
    class MyApp(ArgparseApp):
        class Meta:
            argv = ['bad-alternative-default']
            handlers = [
                Base,
                Aliases,
            ]

    with MyApp() as app:
        app._meta.argv = ['aliases', 'aliases-cmd1']
        res = app.run()
        assert res == "Inside Aliases.aliases_cmd1"

        app._meta.argv = ['aliases', 'aliases-cmd-1']
        app._setup_arg_handler()
        res = app.run()
        assert res == "Inside Aliases.aliases_cmd1"

        app._meta.argv = ['aliases-controller', 'aliases-cmd1']
        app._setup_arg_handler()
        res = app.run()
        assert res == "Inside Aliases.aliases_cmd1"

        app._meta.argv = ['ac', 'ac1']
        app._setup_arg_handler()
        res = app.run()
        assert res == "Inside Aliases.aliases_cmd1"


def test_unknown_arguments():
    class MyArgumentHandler(ArgparseArgumentHandler):
        class Meta:
            label = 'my_argument_handler'
            ignore_unknown_arguments = True

    class MyApp(TestApp):
        class Meta:
            argument_handler = MyArgumentHandler

    with MyApp(argv=['-T', 'some-other-argument']) as app:
        app.run()
        assert '-T' in app.args.unknown_args
        assert 'some-other-argument' in app.args.unknown_args


def test_get_exposed_commands():
    # coverage
    class MyController(ArgparseController):
        class Meta:
            label = 'base'

        @expose()
        def cmd1(self):
            pass

        @expose()
        def cmd2_two(self):
            pass

    with TestApp(handlers=[MyController]) as app:
        app.run()
        assert 'cmd1' in app.controller._get_exposed_commands()
        assert 'cmd2-two' in app.controller._get_exposed_commands()


def test_hide_help():
    class MyController(ArgparseController):
        class Meta:
            label = 'base'

        @expose(hide=True, help='should not be visible')
        def hidden(self):
            pass

    with patch('argparse._SubParsersAction.add_parser') as mock:
        with TestApp(handlers=[MyController]) as app:
            app.run()
            # help='should not be visible' should not
            # get sent to the parser if hide=True
            mock.assert_called_once_with('hidden')
