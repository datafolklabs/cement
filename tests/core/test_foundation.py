
import os
import sys
import re
import pytest
import json
import signal
import platform
from unittest.mock import Mock, MagicMock

from cement import App, Controller, ex
from cement.core.interface import Interface
from cement.core.handler import Handler
from cement.core.exc import CaughtSignal, FrameworkError
from cement.core.foundation import TestApp
from cement.core.foundation import add_handler_override_options
from cement.core.foundation import handler_override
from cement.core.foundation import cement_signal_handler
from cement.utils.misc import minimal_logger, init_defaults
from cement.utils import test, fs, misc


def pre_render_hook(app, data):
    return data


def test_add_handler_override_options_none():
    # coverage for explicitly disabling handler_override_options
    class MyApp(TestApp):
        class Meta:
            extensions = ['json', 'yaml', 'mustache', 'tabulate']

    with MyApp() as app:
        app.args.add_argument = Mock()
        app._meta.handler_override_options = None
        add_handler_override_options(app)
        assert not app.args.add_argument.called


def test_add_handler_override_options_no_interface():
    # coverage for case where the interface doesn't exist
    class MyApp(TestApp):
        class Meta:
            extensions = ['json', 'yaml', 'mustache', 'tabulate']

    with MyApp() as app:
        app._meta.handler_override_options = {
            'bogus': (['--bogus'], {'help': 'bogus handler'}),
        }
        add_handler_override_options(app)
        app.run()
        assert 'bogus_handler_override' not in app.pargs


def test_add_handler_override_options_no_override():
    # coverage for case where there is an output handler, but it's not
    # overridable (so no options to display in --help)
    class MyApp2(TestApp):
        class Meta:
            extensions = ['mustache']

    with MyApp2() as app:
        app._meta.handler_override_options = {
            'output': (['--bogus'], {'help': 'bogus handler'}),
        }
        add_handler_override_options(app)
        app.run()
        assert 'output_handler_override' not in app.pargs


def test_handler_override():
    class MetaStub(object):
        def __init__(self):
            self.handler_override_options = None

    class AppStub(object):
        def __init__(self, meta):
            self._meta = meta

    meta = MetaStub()
    meta_attrs_pre = dir(meta)

    app = AppStub(meta)
    handler_override(app)

    meta_attrs_post = dir(meta)
    assert meta_attrs_pre == meta_attrs_post


def test_cement_signal_handler():
    # coverage
    with pytest.raises(CaughtSignal):
        mframe = Mock()
        mframe.f_globals.values = MagicMock(return_value=[TestApp()])
        cement_signal_handler(1, mframe)
        mframe.f_globals.values.assert_called()


def test_basic():
    with TestApp() as app:
        assert re.match('app-.*', app._meta.label)
        app.run()


def test_loaded_extensions():
    if platform.system().lower() in ['windows']:
        ext_list = [
            'colorlog',
            'dummy',
            'jinja2',
            'json',
            'mustache',
            'smtp',
            'tabulate',
            'watchdog',
            'yaml',
        ]
    else:
        ext_list = [
            'alarm',
            'colorlog',
            'daemon',
            'dummy',
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

    class MyApp(TestApp):
        class Meta:
            extensions = ext_list

    with MyApp() as app:
        for ext in ext_list:
            assert 'cement.ext.ext_%s' % ext in app.ext._loaded_extensions


def test_argv():
    with TestApp(argv=None) as app:
        assert app.argv == list(sys.argv[1:])

    with TestApp(argv=['bogus', 'args']) as app:
        assert app.argv == ['bogus', 'args']


def test_framework_logging():
    # is true

    env_vars = [
        'CEMENT_LOG_DEPRECATED_DEBUG_OPTION',
        'CEMENT_LOG',
        'CEMENT_FRAMEWORK_LOGGING'
    ]
    for var in env_vars:
        if var in os.environ.keys():
            del os.environ[var]

    os.environ['CEMENT_LOG'] = '1'

    with TestApp(framework_logging=True) as app:
        assert app._meta.framework_logging is True

    ml = minimal_logger(__name__)
    assert ml.logging_is_enabled is True

    # is false

    orig_argv = sys.argv
    sys.argv = ['--debug']
    for var in env_vars:
        if var in os.environ.keys():
            del os.environ[var]
    os.environ['CEMENT_LOG'] = '0'

    with TestApp() as app:
        assert app._meta.framework_logging is False

    ml = minimal_logger(__name__)
    assert ml.logging_is_enabled is False
    sys.argv = orig_argv


def test_framework_logging_deprecated_debug_option():
    # is true

    env_vars = [
        'CEMENT_LOG_DEPRECATED_DEBUG_OPTION',
        'CEMENT_LOG',
        'CEMENT_FRAMEWORK_LOGGING'
    ]
    for var in env_vars:
        if var in os.environ.keys():
            del os.environ[var]

    orig_argv = sys.argv
    sys.argv = ['--debug']
    with TestApp(framework_logging=True):
        assert os.environ['CEMENT_LOG_DEPRECATED_DEBUG_OPTION'] == '1'

    ml = minimal_logger(__name__)
    assert ml.logging_is_enabled is True

    # is false

    for var in env_vars:
        if var in os.environ.keys():
            del os.environ[var]

    ml = minimal_logger(__name__)
    assert ml.logging_is_enabled is False
    sys.argv = orig_argv


def test_deprecated_cement_framework_logging_env_var():
    # is true

    os.environ['CEMENT_FRAMEWORK_LOGGING'] = '1'

    with TestApp() as app:
        assert app._meta.framework_logging is True

    ml = minimal_logger(__name__)
    assert ml.logging_is_enabled is True

    # is false

    os.environ['CEMENT_FRAMEWORK_LOGGING'] = '0'

    ml = minimal_logger(__name__)
    assert ml.logging_is_enabled is False


def test_bootstrap():
    with TestApp(bootstrap='tests.bootstrap') as app:
        assert app._loaded_bootstrap.__name__ == 'tests.bootstrap'

    # reload

    app = TestApp(bootstrap='cement.utils.test')
    app._loaded_bootstrap = test
    app.setup()
    assert app._loaded_bootstrap.__name__ == 'cement.utils.test'


def test_resolve_bad_handler():
    class Bogus(object):
        pass

    with pytest.raises(FrameworkError, match="Unable to resolve handler"):
        with TestApp() as app:
            app._resolve_handler('output', Bogus)


def test_passed_handlers():
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
            argv = [__file__, '--debug']

    with MyApp() as app:
        assert isinstance(app.log, LoggingLogHandler)
        assert isinstance(app.plugin, CementPluginHandler)
        assert isinstance(app.args, ArgparseArgumentHandler)
        assert isinstance(app.config, ConfigParserConfigHandler)
        assert isinstance(app.ext, ExtensionHandler)
        assert isinstance(app.mail, DummyMailHandler)
        assert isinstance(app.output, JsonOutputHandler)


def test_debug():
    # default
    with TestApp() as app:
        assert app.debug is False

    # meta overricde
    with TestApp(argv=['--debug']) as app:
        assert app.debug is True

    # alternative options
    argv = ['--not-debug']
    with TestApp(debug_argument_options=['--not-debug']) as app:
        assert app.debug is False
    with TestApp(debug_argument_options=['--not-debug'], argv=argv) as app:
        assert app.debug is True

    # config defaults override
    defaults = init_defaults('my-app-test')
    defaults['my-app-test']['debug'] = True
    with TestApp('my-app-test', config_defaults=defaults) as app:
        assert app.debug is True


def test_render(tmp):
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


def test_label():
    # bad label
    with pytest.raises(FrameworkError):
        App(None)

    # bad chars
    with pytest.raises(FrameworkError, match="alpha-numeric"):
        App('some!bogus()label')


def test_add_arg_shortcut():
    with TestApp() as app:
        app.add_arg('--foo', action='store')
        app.run()
        assert 'foo' in app.pargs


def test_reset_output_handler():
    class ThisApp(TestApp):
        class Meta:
            extensions = ['mustache']
            output_handler = 'mustache'

    with ThisApp() as app:
        app.run()
        app.output = None
        app._meta.output_handler = None
        app._setup_output_handler()
        assert app.output is None


def test_without_signals():
    with TestApp(catch_signals=None) as app:
        assert app._meta.catch_signals is None


def test_extend():
    def my_extended_func():
        return 'KAPLA!'

    with TestApp() as app:
        app.extend('kapla', my_extended_func)
        assert app.kapla() == 'KAPLA!'

        # test for duplicates
        with pytest.raises(FrameworkError, match=".* already exists!"):
            app.extend('kapla', my_extended_func)


def test_no_handler():
    # coverage
    with TestApp() as app:
        retval = app._resolve_handler('cache', None, raise_error=False)
        assert retval is None


def test_config_files_is_none():
    # verify the autogenerated config files list... create a unique
    # test app here since testapp removes all the config path settings
    class ThisApp(App):
        class Meta:
            argv = []
            exit_on_close = False

    with ThisApp('test-app', config_files=None) as app:
        user_home = fs.abspath(fs.HOME_DIR)
        if platform.system().lower() in ['windows']:
            files = [
                os.path.join('C:\\', 'etc', app.label, '%s.conf' % app.label),
                os.path.join(user_home, '.%s.conf' % app.label),
                os.path.join(user_home, '.%s' % app.label, 'config',
                             '%s.conf' % app.label),
            ]
        else:
            files = [
                os.path.join('/', 'etc', app.label, '%s.conf' % app.label),
                os.path.join(user_home, '.%s.conf' % app.label),
                os.path.join(user_home, '.%s' % app.label, 'config',
                             '%s.conf' % app.label),
            ]
        for f in files:
            assert f in app._meta.config_files


def test_pargs():
    with TestApp(argv=['--debug']) as app:
        app.run()
        assert app.pargs.debug is True


def test_last_rendered():
    with TestApp() as app:
        output_text = app.render({'foo': 'bar'})
        assert app.last_rendered == ({'foo': 'bar'}, output_text)


def test_close_with_code():
    with pytest.raises(SystemExit) as e:
        with TestApp(exit_on_close=True) as app:
            app.run()
            app.close(114)
    assert e.value.code == 114

    # test bad code
    with pytest.raises(AssertionError, match='Invalid exit status code'):
        with TestApp() as app:
            app.run()
            app.close('Not An Int')


def test_core_meta_override():
    defaults = init_defaults('test-app')
    defaults['test-app']['mail_handler'] = 'smtp'
    defaults['test-app']['extensions'] = 'smtp'
    with TestApp(label='test-app', config_defaults=defaults) as app:
        app.run()
        assert app._meta.mail_handler == 'smtp'


def test_load_extensions_via_config(rando):
    label = "app-%s" % rando
    defaults = init_defaults(label)

    # singular item
    defaults[label]['extensions'] = 'json'
    with TestApp(label=label, config_defaults=defaults) as app:
        app.run()
        assert 'json' in app._meta.extensions

    # comma separated str list
    defaults[label]['extensions'] = 'json,yaml'
    with TestApp(label=label, config_defaults=defaults) as app:
        app.run()
        assert 'json' in app._meta.extensions
        assert 'yaml' in app._meta.extensions

    # list
    defaults[label]['extensions'] = ['jinja2', 'tabulate']
    with TestApp(label=label, config_defaults=defaults) as app:
        app.run()
        assert 'jinja2' in app._meta.extensions
        assert 'tabulate' in app._meta.extensions


def test_define_hooks_via_meta():
    with TestApp(define_hooks=['my_custom_hook']) as app:
        assert app.hook.defined('my_custom_hook') is True


def test_register_hooks_via_meta():
    def my_custom_hook_func():
        return 'OK'

    app = TestApp(define_hooks=['my_custom_hook'],
                  hooks=[('my_custom_hook', my_custom_hook_func)])
    with app:
        for res in app.hook.run('my_custom_hook'):
            assert res == "OK"


def test_register_hooks_via_meta_retry():
    # hooks registered this way for non-framework hooks need to be retried
    # so we make sure it's actually being registered.
    def my_custom_hook_func():
        pass

    app = TestApp(extensions=['watchdog'],
                  hooks=[('watchdog_pre_start', my_custom_hook_func)])
    with app:
        assert len(app.hook.__hooks__['watchdog_pre_start']) == 1


def test_interfaces_via_meta():
    class MyTestInterface(Interface):
        class Meta:
            interface = 'my_test_interface'

    with TestApp(interfaces=[MyTestInterface]) as app:
        assert app.interface.defined('my_test_interface')


def test_register_handlers_via_meta():
    class MyTestInterface(Interface):
        class Meta:
            interface = 'my_test_interface'

    class MyTestHandler(MyTestInterface, Handler):
        class Meta:
            label = 'my_test_handler'

    app = TestApp(interfaces=[MyTestInterface],
                  handlers=[MyTestHandler])
    with app:
        assert app.handler.registered(
            'my_test_interface', 'my_test_handler')


def test_reload():
    class MyTestInterface(Interface):
        class Meta:
            interface = 'my_test_interface'

    with TestApp() as app:
        app.hook.define('bogus_hook1')
        app.interface.define(MyTestInterface)
        app.extend('some_extra_member', dict())
        app.run()

        assert app.hook.defined('bogus_hook1') is True
        assert app.interface.defined('my_test_interface') is True

        app.reload()

        assert app.hook.defined('bogus_hook1') is False
        assert app.interface.defined('my_test_interface') is False

        app.run()


def test_run_forever():
    if platform.system().lower() in ['windows']:
        pytest.skip('Unable to test run_forever on Windows')

    class MyController(Controller):
        class Meta:
            label = 'base'

        @ex()
        def run_it(self):
            raise Exception("Fake some error")

    def handler(signum, frame):
        raise AssertionError('It ran forever!')

    app = TestApp(handlers=[MyController], argv=['run-it'])

    # set the signal handler and a 5-second alarm
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(5)

    with pytest.raises(AssertionError, match="It ran forever"):
        with app:
            app.run_forever()

    signal.alarm(0)


def test_add_remove_template_directory(tmp):
    with TestApp() as app:
        app.add_template_dir(tmp.dir)
        assert tmp.dir in app._meta.template_dirs

        app.remove_template_dir(tmp.dir)
        assert tmp.dir not in app._meta.template_dirs


def test_alternative_module_mapping():
    with TestApp(alternative_module_mapping=dict(time='math')) as app:
        app.__import__('time')
        app.__import__('sqrt', from_module='time')

        with pytest.raises(AttributeError):
            app.__import__('sleep', from_module='time')


def test_meta_defaults():
    DEBUG_FORMAT = "TEST DEBUG FORMAT - %s" % misc.rando
    META = {}
    META['log.logging'] = {}
    META['log.logging']['debug_format'] = DEBUG_FORMAT

    with TestApp(meta_defaults=META) as app:
        assert app.log._meta.debug_format == DEBUG_FORMAT


def test_template_dir_in_template_dirs(tmp):
    with TestApp(template_dir=tmp.dir) as app:
        app.run()
        assert tmp.dir in app._meta.template_dirs


# coverage

def test_pre_render_hook():
    bogus_hook = Mock(wraps=pre_render_hook)
    bogus_hook.__name__ = 'bogus_hook'
    bogus_hook.__module__ = 'bogus_hooks'

    with TestApp() as app:
        app.hook.register('pre_render', bogus_hook)
        app.run()
        app.render({})
        assert bogus_hook.called


def test_quiet():
    stdout_ref = sys.stdout
    stderr_ref = sys.stderr
    try:
        with TestApp(argv=['--quiet']) as app:
            app.run()
            app.render({})  # coverage
            assert app.quiet is True
            assert stdout_ref is not sys.stdout

        sys.stdout = stdout_ref
        sys.stderr = stderr_ref
        with TestApp(argv=['--quiet', '--debug']) as app:
            app.run()
            assert stdout_ref is sys.stdout

        sys.stdout = stdout_ref
        sys.stderr = stderr_ref
        with TestApp(argv=['--quiet'], debug=True) as app:
            app.run()
            assert stdout_ref is sys.stdout

        sys.stdout = stdout_ref
        sys.stderr = stderr_ref
    except Exception:
        sys.stdout = stdout_ref
        sys.stderr = stderr_ref
        raise


def test_issue_653():
    with pytest.raises(SystemExit):
        with App('myapp', argv=[], exit_on_close=True) as app:
            app.run()
    with pytest.raises(SystemExit):
        with App('myapp', argv=["--quiet"], exit_on_close=True) as app:
            app.run()
    with App('myapp', argv=[]) as app:
        print(app._meta.exit_on_close)
        app.run()
    with App('myapp', argv=["--quiet"]) as app:
        app.run()


def test_none_template_handler():
    with TestApp(template_handler=None) as app:
        app.run()
        assert not hasattr(app, 'template')


def test_core_system_config_dirs(tmp, rando):
    class ThisTestApp(TestApp):
        class Meta:
            label = rando
            core_system_config_dirs = [tmp.dir]

    conf = """
    [%s]
    foo = %s
    """ % (rando, rando)
    with open(os.path.join(tmp.dir, 'test.conf'), 'w') as f:
        f.write(conf)

    with ThisTestApp() as app:
        app.run()
        assert tmp.dir in app._meta.config_dirs
        assert app.config.get(app._meta.label, 'foo') == rando


def test_core_user_config_dirs(tmp, rando):
    class ThisTestApp(TestApp):
        class Meta:
            label = rando
            core_user_config_dirs = [tmp.dir]

    conf = """
    [%s]
    foo = %s
    """ % (rando, rando)
    with open(os.path.join(tmp.dir, 'test.conf'), 'w') as f:
        f.write(conf)

    with ThisTestApp() as app:
        app.run()
        assert tmp.dir in app._meta.config_dirs
        assert app.config.get(app._meta.label, 'foo') == rando


def test_config_dirs(tmp, rando):
    class ThisTestApp(TestApp):
        class Meta:
            label = rando
            config_dirs = [tmp.dir]

    conf = """
    [%s]
    foo = %s
    """ % (rando, rando)
    with open(os.path.join(tmp.dir, 'test.conf'), 'w') as f:
        f.write(conf)

    with ThisTestApp() as app:
        app.run()
        assert tmp.dir in app._meta.config_dirs
        assert app.config.get(app._meta.label, 'foo') == rando


def test_core_system_template_dirs(tmp, rando):
    class ThisTestApp(TestApp):
        class Meta:
            label = rando
            core_system_template_dirs = [tmp.dir]

    with ThisTestApp() as app:
        app.run()
        assert tmp.dir in app._meta.template_dirs


def test_core_user_template_dirs(tmp, rando):
    class ThisTestApp(TestApp):
        class Meta:
            label = rando
            core_user_template_dirs = [tmp.dir]

    with ThisTestApp() as app:
        app.run()
        assert tmp.dir in app._meta.template_dirs


def test_template_dirs(tmp, rando):
    class ThisTestApp(TestApp):
        class Meta:
            label = rando
            template_dirs = [tmp.dir]

    with ThisTestApp() as app:
        app.run()
        assert tmp.dir in app._meta.template_dirs


def test_core_system_plugin_dirs(tmp, rando):
    class ThisTestApp(TestApp):
        class Meta:
            label = rando
            core_system_plugin_dirs = [tmp.dir]

    with ThisTestApp() as app:
        app.run()
        assert tmp.dir in app._meta.plugin_dirs


def test_core_user_plugin_dirs(tmp, rando):
    class ThisTestApp(TestApp):
        class Meta:
            label = rando
            core_user_plugin_dirs = [tmp.dir]

    with ThisTestApp() as app:
        app.run()
        assert tmp.dir in app._meta.plugin_dirs


def test_plugin_dirs(tmp, rando):
    class ThisTestApp(TestApp):
        class Meta:
            label = rando
            plugin_dirs = [tmp.dir]

    with ThisTestApp() as app:
        app.run()
        assert tmp.dir in app._meta.plugin_dirs
