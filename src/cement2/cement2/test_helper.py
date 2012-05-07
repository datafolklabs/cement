
import sys
from .core import backend, foundation, handler, hook

class TestApp(foundation.CementApp):
    class Meta:
        config_files = []
        
    def __init__(self, *args, **kw):
        super(TestApp, self).__init__(*args, **kw)
        from cement2.ext import ext_argparse
        from cement2.ext import ext_nulloutput
        from cement2.ext import ext_plugin
        from cement2.ext import ext_configparser
        from cement2.ext import ext_logging
        from cement2.ext import ext_optparse
        from cement2.ext import ext_daemon
        if not 'configparser' in backend.handlers['config']:
            handler.register(ext_configparser.ConfigParserConfigHandler)
        if not 'argparse' in backend.handlers['argument']:
            handler.register(ext_argparse.ArgParseArgumentHandler)
        if not 'null' in backend.handlers['output']:
            handler.register(ext_nulloutput.NullOutputHandler)
        if not 'cement' in backend.handlers['plugin']:
            handler.register(ext_plugin.CementPluginHandler)
        if not 'logging' in backend.handlers['log']:
            handler.register(ext_logging.LoggingLogHandler)
        if not 'optparse' in backend.handlers['argument']:
            handler.register(ext_optparse.OptParseArgumentHandler)
            
    def setup(self):
        super(TestApp, self).setup()

def reset_backend():
    for _handler in backend.handlers.copy():
        del backend.handlers[_handler]
    for _hook in backend.hooks.copy():
        del backend.hooks[_hook]

def prep(label='test', *args, **kw):
    reset_backend()
    dummy_app = TestApp(label, *args, **kw)
    return dummy_app

