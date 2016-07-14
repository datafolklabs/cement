"""Tests for cement.core.setup."""

import os
import sys
import json
import signal
from time import sleep
from cement.core import foundation, exc, backend, config, extension, plugin
from cement.core.handler import CementBaseHandler
from cement.core.controller import CementBaseController, expose
from cement.core import log, output, hook, arg, controller
from cement.core.interface import Interface
from cement.utils import test
from cement.core.exc import CaughtSignal
from cement.utils.misc import init_defaults, rando, minimal_logger
from nose.plugins.attrib import attr

APP = rando()[:12]


def my_extended_func():
    return 'KAPLA'


class DeprecatedApp(foundation.CementApp):

    class Meta:
        label = 'deprecated'
        defaults = None


class HookTestException(Exception):
    pass


class MyTestInterface(Interface):

    class IMeta:
        label = 'my_test_interface'


class MyTestHandler(CementBaseHandler):

    class Meta:
        label = 'my_test_handler'
        interface = MyTestInterface


class TestOutputHandler(output.CementOutputHandler):
    file_suffix = None

    class Meta:
        interface = output.IOutput
        label = 'test_output_handler'

    def _setup(self, config_obj):
        self.config = config_obj

    def render(self, data_dict, template=None):
        return None


class BogusBaseController(controller.CementBaseController):

    class Meta:
        label = 'bad_base_controller_label'


def my_hook_one(app):
    return 1


def my_hook_two(app):
    return 2


def my_hook_three(app):
    return 3


class FoundationTestCase(test.CementCoreTestCase):

    def setUp(self):
        super(FoundationTestCase, self).setUp()
        self.app = self.make_app('my_app')

    def test_argv_is_none(self):
        app = self.make_app(APP, argv=None)
        app.setup()
        self.eq(app.argv, list(sys.argv[1:]))

    def test_framework_logging_is_true(self):
        del os.environ['CEMENT_FRAMEWORK_LOGGING']

        app = self.make_app(APP, argv=None, framework_logging=True)
        app.setup()
        self.eq(os.environ['CEMENT_FRAMEWORK_LOGGING'], '1')

        ml = minimal_logger(__name__)
        self.eq(ml.logging_is_enabled, True)

    def test_framework_logging_is_false(self):
        del os.environ['CEMENT_FRAMEWORK_LOGGING']

        app = self.make_app(APP, argv=None, framework_logging=False)
        app.setup()
        self.eq(os.environ['CEMENT_FRAMEWORK_LOGGING'], '0')

        ml = minimal_logger(__name__)
        self.eq(ml.logging_is_enabled, False)

        # coverage... should default to True if no key in os.environ
        del os.environ['CEMENT_FRAMEWORK_LOGGING']
        self.eq(ml.logging_is_enabled, True)

    def test_bootstrap(self):
        app = self.make_app('my_app', bootstrap='tests.bootstrap')
        app.setup()
        self.eq(app._loaded_bootstrap.__name__, 'tests.bootstrap')

    def test_reload_bootstrap(self):
        app = self.make_app('my_app', bootstrap='cement.utils.test')
        app._loaded_bootstrap = test
        app.setup()
        self.eq(app._loaded_bootstrap.__name__, 'cement.utils.test')

    def test_argv(self):
        app = self.make_app('my_app', argv=['bogus', 'args'])
        self.eq(app.argv, ['bogus', 'args'])

    @test.raises(exc.FrameworkError)
    def test_resolve_handler_bad_handler(self):
        class Bogus(object):
            pass

        try:
            self.app._resolve_handler('output', Bogus)
        except exc.FrameworkError as e:
            self.ok(e.msg.find('resolve'))
            raise

    def test_default(self):
        self.app.setup()
        self.app.run()

    def test_passed_handlers(self):
        from cement.ext import ext_configparser
        from cement.ext import ext_logging
        from cement.ext import ext_argparse
        from cement.ext import ext_plugin
        from cement.ext import ext_dummy

        # forces CementApp._resolve_handler to register the handler
        from cement.ext import ext_json

        app = self.make_app('my-app-test',
            config_handler=ext_configparser.ConfigParserConfigHandler,
            log_handler=ext_logging.LoggingLogHandler(),
            arg_handler=ext_argparse.ArgParseArgumentHandler(),
            extension_handler=extension.CementExtensionHandler(),
            plugin_handler=ext_plugin.CementPluginHandler(),
            output_handler=ext_json.JsonOutputHandler(),
            mail_handler=ext_dummy.DummyMailHandler(),
            argv=[__file__, '--debug']
            )

        app.setup()

    def test_debug(self):
        app = self.make_app('my-app-test', argv=[__file__])
        app.setup()
        self.eq(app.debug, False)

        self.reset_backend()
        app = self.make_app('my-app-test', argv=[__file__, '--debug'])
        app.setup()
        self.eq(app.debug, True)

        self.reset_backend()
        defaults = init_defaults('my-app-test')
        defaults['my-app-test']['debug'] = True
        app = self.make_app('my-app-test', argv=[__file__],
                            config_defaults=defaults)
        app.setup()
        self.eq(app.debug, True)

    def test_render(self):
        # Render with default
        self.app.setup()
        self.app.render(dict(foo='bar'))

        # Render with no output_handler... this is hackish, but there are
        # circumstances where app.output would be None.
        app = self.make_app('test', output_handler=None)
        app.setup()
        app.output = None
        app.render(dict(foo='bar'))

    def test_render_out_to_file(self):
        self.app = self.make_app(APP, extensions=['json'],
                                 output_handler='json')
        self.app.setup()
        self.app.run()

        f = open(self.tmp_file, 'w')
        self.app.render(dict(foo='bar'), out=f)
        f.close()

        f = open(self.tmp_file, 'r')
        data = json.load(f)
        f.close()

        self.eq(data, dict(foo='bar'))

    @test.raises(TypeError)
    def test_render_bad_out(self):
        self.app.setup()
        self.app.run()

        try:
            self.app.render(dict(foo='bar'), out='bogus type')
        except TypeError as e:
            self.eq(e.args[0], "Argument 'out' must be a 'file' like object")
            raise

    @test.raises(exc.FrameworkError)
    def test_bad_label(self):
        try:
            app = foundation.CementApp(None)
        except exc.FrameworkError as e:
            # FIX ME: verify error msg
            raise

    @test.raises(exc.FrameworkError)
    def test_bad_label_chars(self):
        try:
            app = foundation.CementApp('some!bogus()label')
        except exc.FrameworkError as e:
            self.ok(e.msg.find('alpha-numeric'))
            raise

    def test_add_arg_shortcut(self):
        self.app.setup()
        self.app.add_arg('--foo', action='store')

    def test_reset_output_handler(self):
        app = self.make_app('test', argv=[], output_handler=TestOutputHandler)
        app.setup()
        app.run()

        app.output = None

        app._meta.output_handler = None
        app._setup_output_handler()

    def test_lay_cement(self):
        app = self.make_app('test', argv=['--quiet'])

    def test_none_member(self):
        class Test(object):
            var = None

        self.app.setup()
        self.app.args.parsed_args = Test()
        try:
            self.app._parse_args()
        except SystemExit:
            pass

    @test.raises(exc.CaughtSignal)
    def test_cement_signal_handler(self):
        import signal
        import types
        global app
        app = self.make_app('test')
        frame = sys._getframe(0)
        try:
            foundation.cement_signal_handler(signal.SIGTERM, frame)
        except exc.CaughtSignal as e:
            self.eq(e.signum, signal.SIGTERM)
            self.ok(isinstance(e.frame, types.FrameType))
            raise

    def test_cement_without_signals(self):
        app = self.make_app('test', catch_signals=None)
        app.setup()

    def test_extend(self):
        self.app.extend('kapla', my_extended_func)
        self.eq(self.app.kapla(), 'KAPLA')

    @test.raises(exc.FrameworkError)
    def test_extended_duplicate(self):
        self.app.extend('config', my_extended_func)

    def test_no_handler(self):
        app = self.make_app(APP)
        app._resolve_handler('cache', None, raise_error=False)

    def test_config_files_is_none(self):
        app = self.make_app(APP, config_files=None)
        app.setup()

        label = APP
        user_home = os.path.abspath(os.path.expanduser(os.environ['HOME']))
        files = [
            os.path.join('/', 'etc', label, '%s.conf' % label),
            os.path.join(user_home, '.%s.conf' % label),
            os.path.join(user_home, '.%s' % label, 'config'),
        ]
        for f in files:
            res = f in app._meta.config_files
            self.ok(res)

    @test.raises(exc.FrameworkError)
    def test_base_controller_label(self):
        app = self.make_app(APP, base_controller=BogusBaseController)
        app.setup()

    def test_pargs(self):
        app = self.make_app(argv=['--debug'])
        app.setup()
        app.run()
        self.eq(app.pargs.debug, True)

    def test_last_rendered(self):
        self.app.setup()
        output_text = self.app.render({'foo': 'bar'})
        last_data, last_output = self.app.last_rendered
        self.eq({'foo': 'bar'}, last_data)
        self.eq(output_text, last_output)

    def test_get_last_rendered(self):
        # DEPRECATED - REMOVE AFTER THE FUNCTION IS REMOVED
        self.app.setup()
        output_text = self.app.render({'foo': 'bar'})
        last_data, last_output = self.app.get_last_rendered()
        self.eq({'foo': 'bar'}, last_data)
        self.eq(output_text, last_output)

    def test_with_operator(self):
        with self.app_class() as app:
            app.run()

    @test.raises(SystemExit)
    def test_close_with_code(self):
        app = self.make_app(APP, exit_on_close=True)
        app.setup()
        app.run()
        try:
            app.close(114)
        except SystemExit as e:
            self.eq(e.code, 114)
            raise

    @test.raises(AssertionError)
    def test_close_with_bad_code(self):
        self.app.setup()
        self.app.run()
        try:
            self.app.close('Not An Int')
        except AssertionError as e:
            self.eq(e.args[0], "Invalid exit status code (must be integer)")
            raise

    def test_handler_override_options(self):
        app = self.make_app(APP,
                            argv=['-o', 'json'],
                            extensions=['yaml', 'json'],
                            )
        app.setup()
        app.run()
        self.eq(app._meta.output_handler, 'json')

    def test_handler_override_options_is_none(self):
        app = self.make_app(APP,
                            core_handler_override_options=None,
                            handler_override_options=None
                            )
        app.setup()
        app.run()

    def test_handler_override_invalid_interface(self):
        app = self.make_app(APP,
                            handler_override_options=dict(
                                bogus_interface=(['-f'], ['--foo'], {}),
                            )
                            )
        app.setup()
        app.run()

    def test_handler_override_options_not_passed(self):
        app = self.make_app(APP,
                            extensions=['yaml', 'json'],
                            )
        app.setup()
        app.run()

    def test_suppress_output_while_debug(self):
        app = self.make_app(APP, debug=True)
        app.setup()
        app._suppress_output()

    def test_core_meta_override(self):
        defaults = init_defaults(APP)
        defaults[APP]['mail_handler'] = 'dummy'
        app = self.make_app(APP, debug=True, config_defaults=defaults)
        app.setup()
        app.run()

    def test_define_hooks_meta(self):
        app = self.make_app(APP, define_hooks=['my_custom_hook'])
        app.setup()
        self.ok(hook.defined('my_custom_hook'))

    @test.raises(HookTestException)
    def test_register_hooks_meta(self):
        def my_custom_hook_func():
            raise HookTestException('OK')

        app = self.make_app(APP,
                            define_hooks=['my_custom_hook'],
                            hooks=[('my_custom_hook', my_custom_hook_func)])

        app.setup()

        for res in hook.run('my_custom_hook'):
            pass

    def test_register_hooks_meta_retry(self):
        # hooks registered this way for non-framework hooks need to be retried
        # so we make sure it's actually being registered.
        def my_custom_hook_func():
            raise HookTestException('OK')

        app = self.make_app(APP, 
            extensions=['watchdog'],
            hooks=[
                ('watchdog_pre_start', my_custom_hook_func)
            ]
        )
        app.setup()
        self.eq(len(app.hook.__hooks__['watchdog_pre_start']), 1)

    def test_define_handlers_meta(self):
        app = self.make_app(APP, define_handlers=[MyTestInterface])
        app.setup()
        self.ok(app.handler.defined('my_test_interface'))

    def test_register_handlers_meta(self):
        app = self.make_app(APP,
                            define_handlers=[MyTestInterface],
                            handlers=[MyTestHandler],
                            )
        app.setup()
        self.ok(app.handler.registered('my_test_interface', 
                                       'my_test_handler'))

    def test_disable_backend_globals(self):
        app = self.make_app(APP, 
            use_backend_globals=False,
            define_handlers=[MyTestInterface],
            handlers=[MyTestHandler],
            define_hooks=['my_hook'],
            )
        app.setup()
        self.ok(app.handler.registered('my_test_interface', 
                                       'my_test_handler'))
        self.ok(app.hook.defined('my_hook'))

    def test_reload(self):
        with self.app as app:
            app.hook.define('bogus_hook1')
            app.handler.define(MyTestInterface)
            app.extend('some_extra_member', dict())
            app.run()
            self.ok(app.hook.defined('bogus_hook1'))
            self.ok(app.handler.defined('my_test_interface'))
            app.reload()
            self.eq(app.hook.defined('bogus_hook1'), False)
            self.eq(app.handler.defined('my_test_interface'), False)
            app.run()

    @test.raises(AssertionError)
    def test_run_forever(self):
        class Controller(CementBaseController):
            class Meta:
                label = 'base'

            @expose()
            def runit(self):
                raise Exception("Fake some error")

        app = self.make_app(base_controller=Controller, argv=['runit'])

        def handler(signum, frame):
            raise AssertionError('It ran forever!')

        # set the signal handler and a 5-second alarm
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(5)

        try:
            # this will run indefinitely
            with app as app:
                app.run_forever()
        except AssertionError as e:
            self.eq(e.args[0], 'It ran forever!')
            raise
        finally:
            signal.alarm(0) 

    def test_add_template_directory(self):
        self.app.setup()
        
        self.app.add_template_dir(self.tmp_dir)
        res = self.tmp_dir in self.app._meta.template_dirs
        self.ok(res)

    def test_remove_template_directory(self):
        self.app.setup()

        self.app.add_template_dir(self.tmp_dir)
        res = self.tmp_dir in self.app._meta.template_dirs
        self.ok(res)

        self.app.remove_template_dir(self.tmp_dir)
        res = self.tmp_dir not in self.app._meta.template_dirs
        self.ok(res)

    def test_alternative_module_mapping(self):
        # just to have something for coverage
        app = self.make_app(alternative_module_mapping=dict(time='time'))
        app.setup()

        app.__import__('time')
        app.__import__('sleep', from_module='time')

    def test_meta_defaults(self):
        DEBUG_FORMAT = "TEST DEBUG FORMAT - %s" % self.rando
        META = {}
        META['log.logging'] = {}
        META['log.logging']['debug_format'] = DEBUG_FORMAT
        app = self.make_app(meta_defaults=META)
        app.setup()
        self.eq(app.log._meta.debug_format, DEBUG_FORMAT)

