"""Tests for cement.core.setup."""

import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import foundation, exc, backend, config, extension, plugin
from cement2.core import log, output

def startup():
    pass

def teardown():
    for hook in backend.hooks.copy():
        if hook.startswith('cement'):
            del backend.hooks[hook]
    backend.handlers = {}
    
@with_setup(startup, teardown)
def test_foundation_default():
    app = foundation.lay_cement('cement_nosetests')
    app.run()
    
def test_foundation_passed_handlers():
    defaults = backend.defaults('cement_nosetests')
    defaults['base']['config_files'] = '/dev/null'
    myconfig = config.ConfigParserConfigHandler(defaults)
    app = foundation.lay_cement('cement_nosetests',
        config_handler=myconfig,
        log_handler=log.LoggingLogHandler(myconfig),
        extension_handler=extension.CementExtensionHandler(myconfig),
        plugin_handler=plugin.CementPluginHandler(myconfig),
        output_handler=output.CementOutputHandler(myconfig),
        argv=[__file__, '--debug']
        )
    
    app.run()