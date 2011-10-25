"""Tests for cement.core.setup."""

import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import foundation, exc, backend, config, extension, plugin
from cement2.core import log, output, handler, hook, arg
from cement2 import test_helper as _t
    
class TestOutputHandler(object):
    file_suffix = None
    
    class meta:
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
    from cement2.ext import ext_cement_plugin
    from cement2.ext import ext_cement_output
    
    myconfig = ext_configparser.ConfigParserConfigHandler(defaults)
    myconfig.setup(defaults)
    app = _t.prep('test',
        config_handler=myconfig,
        log_handler=ext_logging.LoggingLogHandler(),
        arg_handler=ext_argparse.ArgParseArgumentHandler(),
        extension_handler=extension.CementExtensionHandler(),
        plugin_handler=ext_cement_plugin.CementPluginHandler(),
        output_handler=ext_cement_output.CementOutputHandler(),
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
    