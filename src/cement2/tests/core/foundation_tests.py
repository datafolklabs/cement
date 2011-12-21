"""Tests for cement.core.setup."""

import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import foundation, exc, backend, config, extension, plugin
from cement2.core import log, output, handler, hook, arg, controller
from cement2 import test_helper as _t
       
class TestOutputHandler(object):
    file_suffix = None
    
    class Meta:
        interface = output.IOutput
        label = 'test_output_handler'
        
    def setup(self, config_obj):
        self.config = config_obj
        
    def render(self, data_dict, template=None):
        return None
            
def test_default():
    app = _t.prep('test')
    app.setup()
    try:
        app.run()
    except BaseException:
        pass
    
def test_passed_handlers():
    defaults = backend.defaults('test')
    defaults['base']['config_files'] = '/dev/null'
    
    from cement2.ext import ext_configparser
    from cement2.ext import ext_logging
    from cement2.ext import ext_argparse
    from cement2.ext import ext_plugin
    from cement2.ext import ext_nulloutput
    
    myconfig = ext_configparser.ConfigParserConfigHandler(defaults)
    myconfig.setup(defaults)
    app = _t.prep('test',
        config_handler=myconfig,
        log_handler=ext_logging.LoggingLogHandler(),
        arg_handler=ext_argparse.ArgParseArgumentHandler(),
        extension_handler=extension.CementExtensionHandler(),
        plugin_handler=ext_plugin.CementPluginHandler(),
        output_handler=ext_nulloutput.NullOutputHandler(),
        argv=[__file__, '--debug']
        )
    app.setup()

def test_null_out():
    null = foundation.NullOut()
    null.write('nonsense')

def test_render():
    # Render with default
    app = _t.prep('test')
    app.setup()
    app.render(dict(foo='bar'))

    # Render with no output_handler... this is hackish, but there are 
    # circumstances where app.output would be None.
    app = _t.prep('test', output_handler=None)
    app.setup()
    app.output = None
    app.render(dict(foo='bar'))

@raises(exc.CementRuntimeError)
def test_bad_app_name():
    app = foundation.CementApp(None)

def test_add_arg_shortcut():
    app = _t.prep('test')
    app.setup()
    app.add_arg('--foo', action='store')
    
def test_reset_output_handler():
    app = _t.prep('test')
    app.argv = []
    app.setup()
    app.output = TestOutputHandler()
    app.run()
    
    app.output = None
    app.run()
    
    app.config.set('base', 'output_handler', None)
    app._setup_output_handler()
    app.run()

def test_controller_handler():
    app = _t.prep('test')
    handler.register(controller.CementBaseController)
    
    app.setup()
    app.controller = None
    app.config.set('base', 'controller_handler', 'base')
    app._setup_controller_handler()
    
    app = _t.prep('test')
    handler.register(controller.CementBaseController)
    
    app.argv = ['base', 'default']
    app.controller = controller.CementBaseController()
    app.setup()
    try:
        app.run()
    except NotImplementedError:
        pass

def test_lay_cement():
    _t.reset_backend()
    defaults = backend.defaults('test')
    argv = ['--quiet']
    app = foundation.lay_cement('test', defaults=defaults, argv=argv)
    
    _t.reset_backend()
    defaults = backend.defaults('test')
    argv = ['--json', '--yaml']
    app = foundation.lay_cement('test', defaults=defaults, argv=argv)
    
def my_hook_one(app):
    return 1
        
def my_hook_two(app):
    return 2

def my_hook_three(app):
    return 3
    
def test_framework_hooks():
    app = _t.prep()
    
    hook_tuple = (0, my_hook_one.__name__, my_hook_one)    
    hook_tuple_two = (99, my_hook_two.__name__, my_hook_two)    
    hook_tuple_three = (-99, my_hook_three.__name__, my_hook_three)    
    backend.hooks['cement_pre_setup_hook'].append(hook_tuple)
    backend.hooks['cement_pre_setup_hook'].append(hook_tuple_two)
    backend.hooks['cement_pre_setup_hook'].append(hook_tuple_three)
    backend.hooks['cement_post_setup_hook'].append(hook_tuple)
    backend.hooks['cement_pre_run_hook'].append(hook_tuple)
    backend.hooks['cement_post_run_hook'].append(hook_tuple)
    app.setup()

    # check weight ordering
    eq_(backend.hooks['cement_pre_setup_hook'][0][1], 'my_hook_three')
    eq_(backend.hooks['cement_pre_setup_hook'][1][1], 'my_hook_one')
    eq_(backend.hooks['cement_pre_setup_hook'][2][1], 'my_hook_two')
    
def test_none_member():
    class Test(object):
        var = None
    
    app = _t.prep()
    app.setup()    
    app.args.parsed_args = Test()
    try:
        app._parse_args()
    except SystemExit:
        pass
    
@raises(exc.CementSignalError)
def test_cement_signal_handler():
    import signal
    try:
        foundation.cement_signal_handler(signal.SIGTERM, 5)
    except exc.CementSignalError as e:
        eq_(e.signum, signal.SIGTERM)
        eq_(e.frame, 5)
        raise
    