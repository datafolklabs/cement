"""Tests for cement.core.setup."""

import os
import sys
from cement.core import foundation, exc, backend, config, extension, plugin
from cement.core import log, output, handler, hook, arg, controller
from cement.utils import test
from cement.utils.misc import init_defaults

def my_extended_func():
    return 'KAPLA'

class DeprecatedApp(foundation.CementApp):
    class Meta:
        label = 'deprecated'
        defaults = None

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
        self.app = self.make_app('my_app')

    def test_argv_is_none(self):
        app = self.make_app('myapp', argv=None)
        app.setup()
        self.eq(app.argv, list(sys.argv[1:]))

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
        from cement.ext import ext_nulloutput

        # forces CementApp._resolve_handler to register the handler
        from cement.ext import ext_json

        app = self.make_app('my-app-test',
            config_handler=ext_configparser.ConfigParserConfigHandler,
            log_handler=ext_logging.LoggingLogHandler(),
            arg_handler=ext_argparse.ArgParseArgumentHandler(),
            extension_handler=extension.CementExtensionHandler(),
            plugin_handler=ext_plugin.CementPluginHandler(),
            output_handler=ext_json.JsonOutputHandler(),
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

    def test_null_out(self):
        null = foundation.NullOut()
        null.write('nonsense')

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
        app = self.make_app('test', argv=['--json', '--yaml'])

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
        try:
            foundation.cement_signal_handler(signal.SIGTERM, 5)
        except exc.CaughtSignal as e:
            self.eq(e.signum, signal.SIGTERM)
            self.eq(e.frame, 5)
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
        app = self.make_app('myapp')
        app._resolve_handler('cache', None, raise_error=False)

    def test_config_files_is_none(self):
        app = self.make_app('myapp', config_files=None)
        app.setup()

        label = 'myapp'
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
        app = self.make_app('myapp', base_controller=BogusBaseController)
        app.setup()

    def test_pargs(self):
        app = self.make_app(argv=['--debug'])
        app.setup()
        app.run()
        self.eq(app.pargs.debug, True)

    def test_last_rendered(self):
        self.app.setup()
        output_text = self.app.render({'foo':'bar'})
        last_data, last_output = self.app.last_rendered
        self.eq({'foo':'bar'}, last_data)
        self.eq(output_text, last_output)

    def test_get_last_rendered(self):
        ### DEPRECATED - REMOVE AFTER THE FUNCTION IS REMOVED
        self.app.setup()
        output_text = self.app.render({'foo':'bar'})
        last_data, last_output = self.app.get_last_rendered()
        self.eq({'foo':'bar'}, last_data)
        self.eq(output_text, last_output)
