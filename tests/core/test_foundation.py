
import os
import sys
import re
import pytest
import json
import signal
from unittest.mock import Mock, MagicMock

from cement import App, Controller, ex
from cement.core.handler import Handler
from cement.core.exc import CaughtSignal, FrameworkError
from cement.core.foundation import TestApp
from cement.core.foundation import add_handler_override_options
from cement.core.foundation import handler_override
from cement.core.foundation import cement_signal_handler
from cement.utils.misc import minimal_logger, init_defaults
from cement.utils import test, fs, misc

def test_add_handler_override_options():
    class MyApp(TestApp):
        class Meta:
            extensions = ['json', 'yaml', 'mustache', 'tabulate']

    with MyApp() as app:
        # coverage for explicitly disabling handler_override_options
        app._meta.handler_override_options = None
        add_handler_override_options(app)

        # coverage for case where the interface doesn't exist
        app._meta.handler_override_options = {
            'bogus' : ( ['--bogus'], { 'help' : 'bogus handler' } ),
        }
        add_handler_override_options(app)

    # coverage for case where there is an output handler, but it's not
    # overridable (so no options to display in --help)
    class MyApp2(TestApp):
        class Meta:
            extensions = ['mustache']

    with MyApp2() as app:
        app.run()


def test_handler_override():
    class MyApp(TestApp):
        class Meta:
            argv = ['-o', 'json']
            extensions = ['json', 'yaml', 'mustache', 'tabulate']

    with MyApp() as app:
        app.run()

    # coverage
    app._meta.handler_override_options = None
    handler_override(app)


def test_cement_signal_handler():
    # coverage
    with pytest.raises(CaughtSignal):
        mframe = Mock()
        mframe.f_globals.values = MagicMock(return_value=[TestApp()])
        cement_signal_handler(1, mframe)
        mframe.f_globals.values.assert_called()


class TestFoundation(object):


    def test_basic(self):
        with TestApp() as app:
            assert re.match('app-.*', app._meta.label)
            app.run()


    def test_loaded(self):
        class MyApp(TestApp):
            class Meta:
                extensions = [
                    'alarm',
                    'colorlog',
                    'daemon',
                    'dummy',
                    'handlebars',
                    'jinja2',
                    'json',
                    'memcached',
                    'mustache',
                    'redis',
                    'smtp',
                    'tabulate',
                    'watchdog',
                    'yaml',
                ]

        with MyApp() as app:
            app.run()


    def test_argv(self):
        with TestApp(argv=None) as app:
            assert app.argv == list(sys.argv[1:])

        with TestApp(argv=['bogus', 'args']) as app:
            assert app.argv == ['bogus', 'args']


    def test_framework_logging(self):
        ### is true

        del os.environ['CEMENT_FRAMEWORK_LOGGING']

        with TestApp(framework_logging=True) as app:
            assert os.environ['CEMENT_FRAMEWORK_LOGGING'] == '1'

        ml = minimal_logger(__name__)
        assert ml.logging_is_enabled is True

        ### is false

        del os.environ['CEMENT_FRAMEWORK_LOGGING']

        with TestApp(framework_logging=False) as app:
            assert os.environ['CEMENT_FRAMEWORK_LOGGING'] == '0'

        ml = minimal_logger(__name__)
        assert ml.logging_is_enabled is False


    def test_bootstrap(self):
        with TestApp(bootstrap='tests.bootstrap') as app:
            assert app._loaded_bootstrap.__name__ == 'tests.bootstrap'

        ### reload

        app = TestApp(bootstrap='cement.utils.test')
        app._loaded_bootstrap = test
        app.setup()
        assert app._loaded_bootstrap.__name__ == 'cement.utils.test'


    def test_resolve_bad_handler(self):
        class Bogus(object):
            pass

        with pytest.raises(FrameworkError, match="Unable to resolve handler"):
            with TestApp() as app:
                app._resolve_handler('output', Bogus)


    def test_passed_handlers(self):
        # forces App._resolve_handler to register the handler by class
        from cement.core.extension import ExtensionHandler
        from cement.ext.ext_configparser import ConfigParserConfigHandler
        from cement.ext.ext_logging import LoggingLogHandler
        from cement.ext.ext_argparse import ArgparseArgumentHandler
        from cement.ext.ext_plugin import CementPluginHandler
        from cement.ext.ext_dummy import DummyMailHandler
        from cement.ext.ext_json import JsonOutputHandler

        class MyApp(TestApp):
            class Meta:
                config_handler = ConfigParserConfigHandler
                log_handler = LoggingLogHandler()
                arg_handler = ArgparseArgumentHandler()
                extension_handler = ExtensionHandler()
                plugin_handler = CementPluginHandler()
                output_handler = JsonOutputHandler()
                mail_handler = DummyMailHandler()
                argv = [ __file__, '--debug' ]

        with MyApp() as app:
            pass


    def test_debug(self):
        # default
        with TestApp() as app:
            assert app.debug is False

        # meta overricde
        with TestApp(argv=['--debug']) as app:
            assert app.debug is True

        # config defaults override
        defaults = init_defaults('my-app-test')
        defaults['my-app-test']['debug'] = True
        with TestApp('my-app-test', config_defaults=defaults) as app:
            assert app.debug is True


    def test_render(self, tmp):
        # defaults
        with TestApp() as app:
            app.render(dict(foo='bar'))

        # no output_handler... this is hackish, but there are
        # circumstances where app.output would be None.
        with TestApp(output_handler=None) as app:
            app.output = None
            app.render(dict(foo='bar'))

        # with output to file
        with TestApp(extensions=['json'], output_handler='json') as app:
            app.run()

            f = open(tmp.file, 'w')
            app.render(dict(foo='bar'), out=f)
            f.close()

            f = open(tmp.file, 'r')
            data = json.load(f)
            f.close()

            assert data == dict(foo='bar')

        # with bad output type
        msg = "Argument 'out' must be a 'file' like object"
        with pytest.raises(TypeError, match=msg):
            with TestApp() as app:
                app.run()
                app.render(dict(foo='bar'), out='bogus type')


    def test_label(self):
        # bad label
        with pytest.raises(FrameworkError):
            App(None)

        # bad chars
        with pytest.raises(FrameworkError, match="alpha-numeric"):
            App('some!bogus()label')



    def test_add_arg_shortcut(self):
        with TestApp() as app:
            app.add_arg('--foo', action='store')


    def test_reset_output_handler(self):

        with TestApp(extensions=['mustache'], output_handler='mustache') as app:
            app.run()
            app.output = None
            app._meta.output_handler = None
            app._setup_output_handler()


    def test_without_signals(self):
        with TestApp(catch_signals=None) as app:
            assert app._meta.catch_signals is None


    def test_extend(self):
        def my_extended_func():
            return 'KAPLA!'

        with TestApp() as app:
            app.extend('kapla', my_extended_func)
            assert app.kapla() == 'KAPLA!'

            # test for duplicates
            with pytest.raises(FrameworkError, match=".* already exists!"):
                app.extend('kapla', my_extended_func)


    def test_no_handler(self):
        # coverage
        with TestApp() as app:
            app._resolve_handler('cache', None, raise_error=False)


    def test_config_files_is_none(self):
        # verify the autogenerated config files list
        with TestApp('test-app', config_files=None) as app:
            user_home = fs.abspath(fs.HOME_DIR)
            files = [
                os.path.join('/', 'etc', app.label, '%s.conf' % app.label),
                os.path.join(user_home, '.%s.conf' % app.label),
                os.path.join(user_home, '.%s' % app.label, 'config'),
            ]
            for f in files:
                assert f in app._meta.config_files


    def test_base_controller_label(self):
        class BogusBaseController(Controller):
            class Meta:
                label = 'bad_base_controller_label'

        with pytest.raises(FrameworkError, match="must have a label of 'base'"):
            with TestApp(base_controller=BogusBaseController) as app:
                pass


    def test_pargs(self):
        with TestApp(argv=['--debug']) as app:
            app.run()
            assert app.pargs.debug is True


    def test_last_rendered(self):
        with TestApp() as app:
            output_text = app.render({'foo': 'bar'})
            assert app.last_rendered == ( {'foo': 'bar'}, output_text )


    def test_get_last_rendered(self):
        # DEPRECATED - REMOVE AFTER THE FUNCTION IS REMOVED
        with TestApp() as app:
            output_text = app.render({'foo': 'bar'})
            assert app.get_last_rendered() == ( {'foo': 'bar'}, output_text )


    def test_close_with_code(self):
        with pytest.raises(SystemExit) as e:
            with TestApp(exit_on_close=True) as app:
                app.run()
                app.close(114)
        assert e.value.code == 114

        ### test bad code
        with pytest.raises(AssertionError, match='Invalid exit status code'):
            with TestApp() as app:
                app.run()
                app.close('Not An Int')


    # def test_suppress_output_while_debug(self):
    #     # coverage?
    #     with TestApp(debug=True) as app:
    #         app._suppress_output()
    #
    #
    # def test_core_meta_override(self):
    #     # coverage?
    #     defaults = init_defaults('test-app')
    #     defaults['test-app']['mail_handler'] = 'dummy'
    #     with TestApp(config_defaults=defaults) as app:
    #         app.run()


    def test_define_hooks_via_meta(self):
        with TestApp(define_hooks=['my_custom_hook']) as app:
            assert app.hook.defined('my_custom_hook') is True


    def test_register_hooks_via_meta(self):
        def my_custom_hook_func():
            return 'OK'

        app = TestApp(define_hooks=['my_custom_hook'],
                      hooks=[('my_custom_hook', my_custom_hook_func)])
        with app:
            for res in app.hook.run('my_custom_hook'):
                assert res == "OK"


    def test_register_hooks_via_meta_retry(self):
        # hooks registered this way for non-framework hooks need to be retried
        # so we make sure it's actually being registered.
        def my_custom_hook_func():
            pass

        app = TestApp(extensions=['watchdog'],
                      hooks=[('watchdog_pre_start', my_custom_hook_func)])
        with app:
            assert len(app.hook.__hooks__['watchdog_pre_start']) == 1


    def test_define_handlers_via_meta(self):
        class MyTestHandler(Handler):
            class Meta:
                label = 'my_test_handler'
                interface = 'my_test_interface'

        with TestApp(define_handlers=[MyTestHandler]) as app:
            assert app.handler.defined('my_test_interface')


    def test_register_handlers_via_meta(self):
        class MyTestHandler(Handler):
            class Meta:
                label = 'my_test_handler'
                interface = 'my_test_interface'

        app = TestApp(define_handlers=[MyTestHandler],
                      handlers=[MyTestHandler])
        with app:
            assert app.handler.registered('my_test_interface', 'my_test_handler')


    def test_reload(self):
        class MyTestHandler(Handler):
            class Meta:
                label = 'my_test_handler'
                interface = 'my_test_interface'

        with TestApp() as app:
            app.hook.define('bogus_hook1')
            app.handler.define(MyTestHandler)
            app.extend('some_extra_member', dict())
            app.run()

            assert app.hook.defined('bogus_hook1') is True
            assert app.handler.defined('my_test_interface') is True

            app.reload()

            assert app.hook.defined('bogus_hook1') is False
            assert app.handler.defined('my_test_interface') is False

            app.run()


    def test_run_forever(self):
        class MyController(Controller):
            class Meta:
                label = 'base'

            @ex()
            def run_it(self):
                raise Exception("Fake some error")

        def handler(signum, frame):
            raise AssertionError('It ran forever!')

        app = TestApp(base_controller=MyController, argv=['run-it'])

        # set the signal handler and a 5-second alarm
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(5)

        with pytest.raises(AssertionError, match="It ran forever"):
            with app:
                app.run_forever()

        signal.alarm(0)


    def test_add_remove_template_directory(self, tmp):
        with TestApp() as app:
            app.add_template_dir(tmp.dir)
            assert tmp.dir in app._meta.template_dirs

            app.remove_template_dir(tmp.dir)
            assert tmp.dir not in app._meta.template_dirs


    def test_alternative_module_mapping(self):
        # coverage
        with TestApp(alternative_module_mapping=dict(time='time')) as app:
            app.__import__('time')
            app.__import__('sleep', from_module='time')


    def test_meta_defaults(self):
        DEBUG_FORMAT = "TEST DEBUG FORMAT - %s" % misc.rando
        META = {}
        META['log.logging'] = {}
        META['log.logging']['debug_format'] = DEBUG_FORMAT

        with TestApp(meta_defaults=META) as app:
            assert app.log._meta.debug_format == DEBUG_FORMAT
