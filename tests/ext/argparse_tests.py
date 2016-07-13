"""Tests for cement.ext.ext_argparse."""

import os
import sys
import re
from argparse import ArgumentError
from cement.ext.ext_argparse import ArgparseArgumentHandler
from cement.ext.ext_argparse import ArgparseController, expose
from cement.ext.ext_argparse import _clean_label, _clean_func
from cement.utils import test
from cement.utils.misc import rando, init_defaults
from cement.core import handler
from cement.core.exc import InterfaceError, FrameworkError

APP = rando()[:12]

if (sys.version_info[0] > 3 and sys.version_info[1] >= 4):
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
    def default(self):
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
    def default(self):
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
    def default(self):
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
    def default(self):
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


class ArgparseExtTestCase(test.CementExtTestCase):

    def setUp(self):
        super(ArgparseExtTestCase, self).setUp()
        self.app = self.make_app(APP,
                                 argument_handler=ArgparseArgumentHandler,
                                 handlers=[
                                     Sixth,
                                     Base,
                                     Second,
                                     Third,
                                     Fourth,
                                     Fifth,
                                     Seventh,
                                 ],
                                 )

    def test_clean_label(self):
        self.eq(_clean_label('some_cmd_name'), 'some-cmd-name')

    def test_clean_func(self):
        self.eq(_clean_func('some-cmd-name'), 'some_cmd_name')

    def test_base_default(self):
        if not ARGPARSE_SUPPORTS_DEFAULTS:
            raise test.SkipTest(
                'Argparse does not support default commands in Python < 3.4'
            )

        with self.app as app:
            res = app.run()
            self.eq(res, "Inside Base.default")

    def test_base_cmd1(self):
        with self.app as app:
            app._meta.argv = ['cmd1']
            res = app.run()
            self.eq(res, "Inside Base.cmd1")

    def test_base_command_with_dashes(self):
        with self.app as app:
            app._meta.argv = ['command-with-dashes']
            res = app.run()
            self.eq(res, "Inside Base.command_with_dashes")

    def test_controller_commands(self):
        with self.app as app:
            app._meta.argv = ['cmd2']
            res = app.run()
            self.eq(res, "Inside Second.cmd2")
        self.tearDown()
        
        self.setUp()
        with self.app as app:
            app._meta.argv = ['third', 'cmd3']
            res = app.run()
            self.eq(res, "Inside Third.cmd3")
        self.tearDown()

        self.setUp()
        with self.app as app:
            app._meta.argv = ['third', 'cmd4']
            res = app.run()
            self.eq(res, "Inside Fourth.cmd4")
        self.tearDown()

        self.setUp()
        with self.app as app:
            app._meta.argv = ['third', 'fifth', 'cmd5']
            res = app.run()
            self.eq(res, "Inside Fifth.cmd5")
        self.tearDown()

        self.setUp()
        with self.app as app:
            app._meta.argv = ['third', 'fifth', 'sixth', 'cmd6']
            res = app.run()
            self.eq(res, "Inside Sixth.cmd6")
        self.tearDown()

        self.setUp()
        with self.app as app:
            app._meta.argv = ['third', 'cmd7']
            res = app.run()
            self.eq(res, "Inside Seventh.cmd7")
        self.tearDown()
        
    def test_base_cmd1_parsing(self):
        with self.app as app:
            app._meta.argv = ['--foo=bar', 'cmd1']
            res = app.run()
            self.eq(res, "Inside Base.cmd1")
            self.eq(app.pargs.foo, 'bar')

    def test_second_cmd2(self):
        with self.app as app:
            app._meta.argv = ['--foo=bar', '--foo2=bar2', 'cmd2']
            res = app.run()
            self.eq(res, "Inside Second.cmd2")
            self.eq(app.pargs.foo, 'bar')
            self.eq(app.pargs.foo2, 'bar2')

    def test_third_cmd3(self):
        with self.app as app:
            app._meta.argv = [
                '--foo=bar', '--foo2=bar2',
                'third', '--foo3=bar3', '--foo4=bar4', '--foo7=bar7', 'cmd3',
            ]
            res = app.run()
            self.eq(res, "Inside Third.cmd3")
            self.eq(app.pargs.foo, 'bar')
            self.eq(app.pargs.foo2, 'bar2')
            self.eq(app.pargs.foo3, 'bar3')
            self.eq(app.pargs.foo4, 'bar4')
            self.eq(app.pargs.foo7, 'bar7')

    def test_fifth_cmd5(self):
        with self.app as app:
            app._meta.argv = [
                '--foo=bar', '--foo2=bar2',
                'third', '--foo3=bar3', '--foo4=bar4',
                'fifth', '--foo5=bar5', 'cmd5'
            ]
            res = app.run()
            self.eq(res, "Inside Fifth.cmd5")
            self.eq(app.pargs.foo, 'bar')
            self.eq(app.pargs.foo2, 'bar2')
            self.eq(app.pargs.foo3, 'bar3')
            self.eq(app.pargs.foo4, 'bar4')
            self.eq(app.pargs.foo5, 'bar5')

    def test_sixth_cmd6(self):
        with self.app as app:
            app._meta.argv = [
                '--foo=bar', '--foo2=bar2',
                'third', '--foo3=bar3', '--foo4=bar4',
                'fifth', '--foo5=bar5', 'sixth', '--foo6=bar6', 'cmd6',
            ]
            res = app.run()
            self.eq(res, "Inside Sixth.cmd6")
            self.eq(app.pargs.foo, 'bar')
            self.eq(app.pargs.foo2, 'bar2')
            self.eq(app.pargs.foo3, 'bar3')
            self.eq(app.pargs.foo4, 'bar4')
            self.eq(app.pargs.foo5, 'bar5')
            self.eq(app.pargs.foo6, 'bar6')

    def test_seventh_cmd7(self):
        with self.app as app:
            app._meta.argv = [
                '--foo=bar', '--foo2=bar2',
                'third', '--foo3=bar3', '--foo4=bar4', '--foo7=bar7', 'cmd7',
            ]
            res = app.run()
            self.eq(res, "Inside Seventh.cmd7")
            self.eq(app.pargs.foo, 'bar')
            self.eq(app.pargs.foo2, 'bar2')
            self.eq(app.pargs.foo3, 'bar3')
            self.eq(app.pargs.foo4, 'bar4')
            self.eq(app.pargs.foo7, 'bar7')

    def test_collect(self):
        with self.app as app:
            args = self.app.controller._collect_arguments()
            cmds = self.app.controller._collect_commands()
            args2, cmds2 = self.app.controller._collect()
            self.eq((args, cmds), (args2, cmds2))

    def test_controller_embedded_on_base(self):
        self.app._meta.argv = ['cmd2']
        with self.app as app:
            res = app.run()
            self.eq(res, "Inside Second.cmd2")

    def test_controller_command_arguments(self):
        self.app._meta.argv = ['cmd2', '--cmd2-foo=bar2']
        with self.app as app:
            res = app.run()
            self.eq(res, "Inside Second.cmd2 : Foo > bar2")

    def test_controller_default_nested_on_base(self):
        if not ARGPARSE_SUPPORTS_DEFAULTS:
            raise test.SkipTest(
                'Argparse does not support default commands in Python < 3.4'
            )

        self.app._meta.argv = ['third']
        with self.app as app:
            res = app.run()
            self.eq(res, "Inside Third.default")

    def test_controller_command_nested_on_base(self):
        self.app._meta.argv = ['third', 'cmd3']
        with self.app as app:
            res = app.run()
            self.eq(res, "Inside Third.cmd3")

    def test_controller_doubled_embedded(self):
        self.app._meta.argv = ['third', 'cmd4']
        with self.app as app:
            res = app.run()
            self.eq(res, "Inside Fourth.cmd4")

    def test_controller_default_double_nested(self):
        if not ARGPARSE_SUPPORTS_DEFAULTS:
            raise test.SkipTest(
                'Argparse does not support default commands in Python < 3.4'
            )
        self.app._meta.argv = ['third', 'fifth']
        with self.app as app:
            res = app.run()
            self.eq(res, "Inside Fifth.default")

    def test_controller_command_double_nested(self):
        self.app._meta.argv = ['third', 'fifth', 'cmd5']
        with self.app as app:
            res = app.run()
            self.eq(res, "Inside Fifth.cmd5")

    def test_alternative_default(self):
        if not ARGPARSE_SUPPORTS_DEFAULTS:
            raise test.SkipTest(
                'Argparse does not support default commands in Python < 3.4'
            )

        self.reset_backend()
        self.app = self.make_app(APP,
                                 argv=['alternative_default'],
                                 argument_handler=ArgparseArgumentHandler,
                                 handlers=[
                                     Base,
                                     AlternativeDefault,
                                 ],
                                 )
        with self.app as app:
            res = app.run()
            self.eq(res,
                    "Inside AlternativeDefault.alternative_default")

    @test.raises(FrameworkError)
    def test_bad_alternative_default_command(self):
        if not ARGPARSE_SUPPORTS_DEFAULTS:
            raise test.SkipTest(
                'Argparse does not support default commands in Python < 3.4'
            )

        self.reset_backend()
        self.app = self.make_app(APP,
                                 argv=['bad_alternative_default'],
                                 argument_handler=ArgparseArgumentHandler,
                                 handlers=[
                                     Base,
                                     BadAlternativeDefault,
                                 ],
                                 )
        try:
            with self.app as app:
                res = app.run()

        except FrameworkError as e:
            res = re.match("(.*)does not exist(.*)bogus_default(.*)",
                           e.__str__())
            self.ok(res)
            raise

    @test.raises(InterfaceError)
    def test_invalid_stacked_on(self):
        self.reset_backend()
        try:
            self.app = self.make_app(APP,
                                     argument_handler=ArgparseArgumentHandler,
                                     handlers=[
                                         Base,
                                         Unstacked,
                                     ],
                                     )
            with self.app as app:
                res = app.run()
        except InterfaceError as e:
            self.ok(re.match("(.*)is not stacked anywhere!(.*)", e.msg))
            raise

    @test.raises(InterfaceError)
    def test_invalid_stacked_type(self):
        self.reset_backend()
        try:
            self.app = self.make_app(APP,
                                     argument_handler=ArgparseArgumentHandler,
                                     handlers=[
                                         Base,
                                         BadStackType,
                                     ],
                                     )
            with self.app as app:
                res = app.run()
        except InterfaceError as e:
            self.ok(re.match("(.*)has an unknown stacked type(.*)", e.msg))
            raise

    @test.raises(ArgumentError)
    def test_duplicate_arguments(self):
        self.reset_backend()
        try:
            self.app = self.make_app(APP,
                                     argument_handler=ArgparseArgumentHandler,
                                     handlers=[
                                         Base,
                                         DuplicateArguments,
                                     ],
                                     )
            with self.app as app:
                res = app.run()
        except ArgumentError as e:
            self.ok(re.match("(.*)conflicting option string(.*)",
                             e.__str__()))
            raise

    @test.raises(ArgumentError)
    def test_controller_command_duplicate_arguments(self):
        self.reset_backend()
        try:
            self.app = self.make_app(APP,
                                     argument_handler=ArgparseArgumentHandler,
                                     handlers=[
                                         Base,
                                         ControllerCommandDuplicateArguments,
                                     ],
                                     )
            with self.app as app:
                res = app.run()
        except ArgumentError as e:
            self.ok(re.match("(.*)conflicting option string(.*)",
                             e.__str__()))
            raise

    def test_aliases(self):
        if sys.version_info[0] < 3:
            raise test.SkipTest(
                'Argparse does not support aliases in Python < 3'
            )
        self.reset_backend()

        self.app = self.make_app(APP,
                                 argument_handler=ArgparseArgumentHandler,
                                 handlers=[
                                     Base,
                                     Aliases,
                                 ],
                                 )
        with self.app as app:
            app._meta.argv = ['aliases', 'aliases-cmd1']
            res = app.run()
            self.eq(res, "Inside Aliases.aliases_cmd1")

            app._meta.argv = ['aliases', 'aliases-cmd-1']
            app._setup_arg_handler()
            res = app.run()
            self.eq(res, "Inside Aliases.aliases_cmd1")

            app._meta.argv = ['aliases-controller', 'aliases-cmd1']
            app._setup_arg_handler()
            res = app.run()
            self.eq(res, "Inside Aliases.aliases_cmd1")

            app._meta.argv = ['ac', 'ac1']
            app._setup_arg_handler()
            res = app.run()
            self.eq(res, "Inside Aliases.aliases_cmd1")

    def test_unknown_arguments(self):
        self.reset_backend()

        class MyArgumentHandler(ArgparseArgumentHandler):
            class Meta:
                label = 'my_argument_handler'
                ignore_unknown_arguments = True
        self.app = self.make_app(APP,
                                 argument_handler=MyArgumentHandler,
                                 )
        with self.app as app:
            app._meta.argv = ['-l', 'some-other-argument']
            app.run()
            res = '-l' in app.args.unknown_args
            self.ok(res)
            res = 'some-other-argument' in app.args.unknown_args
            self.ok(res)
