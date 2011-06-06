"""Tests for cement.core.setup."""

import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import foundation, exc, backend, config, extension, plugin
from cement2.core import log, output, handler
from cement2.ext.ext_configparser import ConfigParserConfigHandler

if not handler.defined('config'):
    handler.define('config', config.IConfigHandler)
if not handler.defined('log'):
    handler.define('log', log.ILogHandler)
from cement2.ext.ext_logging import LoggingLogHandler
from cement2.ext.ext_configparser import ConfigParserConfigHandler

def startup():
    pass
    
def teardown():
    if backend.handlers.has_key('log'):
        del backend.handlers['log']
    if backend.handlers.has_key('config'):
        del backend.handlers['config']
            
    for hook in backend.hooks.copy():
        if hook.startswith('cement'):
            del backend.hooks[hook]
    backend.handlers = {}
    
@with_setup(startup, teardown)
def test_foundation_default():
    if backend.handlers.has_key('log'):
        del backend.handlers['log']
    if backend.handlers.has_key('config'):
        del backend.handlers['config']
    app = foundation.lay_cement('cement_nosetests')
    handler.register(ConfigParserConfigHandler)
    handler.register(LoggingLogHandler)
    app.run()
    
def test_foundation_passed_handlers():
    defaults = backend.defaults('cement_nosetests')
    defaults['base']['config_files'] = '/dev/null'
    myconfig = ConfigParserConfigHandler(defaults)
    myconfig.setup(defaults)
    app = foundation.lay_cement('cement_nosetests',
        config_handler=myconfig,
        log_handler=LoggingLogHandler(),
        extension_handler=extension.CementExtensionHandler(),
        plugin_handler=plugin.CementPluginHandler(),
        output_handler=output.CementOutputHandler(),
        argv=[__file__, '--debug']
        )
    
    app.run()