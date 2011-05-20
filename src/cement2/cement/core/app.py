"""Cement core application module."""

import sys

from cement.core.backend import default_config, minimal_logger
from cement.core import exc
from cement.core import handler, hook
from cement.core.log import ILogHandler, LoggingLogHandler
from cement.core.config import IConfigHandler, ConfigParserConfigHandler
from cement.core.plugin import IPluginHandler, CementPluginHandler

log = minimal_logger(__name__)

def lay_cement(app_name, *args, **kw):
    """
    Initialize the framework.

    Required Arguments:
    
        app_name
            The name of the application.
            
        
    Optional Keyword Arguments:

        defaults
            The default config dictionary, other wise use default_config().
            
        argv
            List of args to use.  Default: sys.argv.
    
    """
    
    defaults = kw.get('defaults', default_config())
    argv = kw.get('argv', sys.argv)
    
    # basic logging setup first (mostly for debug/error)
    if '--debug' in argv:
        kw['defaults']['log']['level'] = 'DEBUG'
        kw['defaults']['base']['debug'] = True
    
    # define framework hooks
    hook.define('cement_init_hook')
    hook.define('cement_post_options_hook')
    hook.define('cement_validate_config_hook')
    hook.define('cement_pre_plugins_hook')
    hook.define('cement_post_plugins_hook')
    hook.define('cement_post_bootstrap_hook')
    
    # define and register handlers    
    handler.define('log', ILogHandler)
    handler.define('config', IConfigHandler)
    handler.define('plugin', IPluginHandler)
    #define_handler('output')
    #define_handler('option')
    #define_handler('command')
    #define_handler('hook')
    #define_handler('error')
    
    handler.register(ConfigParserConfigHandler)
    handler.register(LoggingLogHandler)
    handler.register(CementPluginHandler)
    
    app = CementApp(app_name, *args, **kw)
    return app
    
class CementApp(object):
    def __init__(self, app_name, **kw):
        self.defaults = kw.get('defaults', default_config())
        if not self.defaults['base']['app_name']:
            self.defaults['base']['app_name'] = app_name

        # default all handlers to None
        self.config = None
        self.log = None
        self.plugin = None
        self.options = None
        self.commands = None
        
        # initialize handlers if passed in and set config to reflect
        if kw.get('config_handler', None):
            self.config = kw['config_handler']
            self.config.set('base', 'config_handler', 
                            self.config.__handler_label__)
        
        if kw.get('log', None):
            self.log = kw['log']
            self.config.set('base', 'log_handler', 
                            self.log.__handler_label__)
        
        if kw.get('plugin', None):
            self.plugin = kw['plugin']
            self.config.set('base', 'plugin_handler', 
                            self.plugin.__handler_label__)

    def run(self):
        self._setup_config_handler()
        self._validate_required_config()
        self._validate_config()
        self._setup_log_handler()
        self._setup_plugin_handler()
        
    def load_ext(self, ext_name):
        module = "cement.ext.ext_%s" % ext_name
        try:
            __import__(module)
        except ImportError, e:
            raise exc.CementRuntimeError, e.args[0]
        
    def _setup_config_handler(self):
        if not self.config:
            h = handler.get('config', self.defaults['base']['config_handler'])
            self.config = h(self.defaults)

        for _file in self.config.get('base', 'config_files'):
            self.config.parse_file(_file)

    def _setup_log_handler(self):
        if not self.log:
            h = handler.get('log', self.config.get('base', 'log_handler'))
            self.log = h(self.config)
        
    def _setup_plugin_handler(self):
        if not self.plugin:
            h = handler.get('plugin', 
                            self.config.get('base', 'plugin_handler'))
            self.plugin = h(self.config)
            
    def _validate_required_config(self):
        """
        Validate base config settings required by cement.
        """
        # need to shorten this a bit
        c = self.config

        if not c.has_key('base', 'app_name') or \
           not c.get('base', 'app_name'):
            raise exc.CementConfigError("config['app_name'] required.")
        if not c.has_key('base', 'app_module') or \
           not c.get('base', 'app_module'):
            c.set('base', 'app_module', c.get('base', 'app_name'))
        if not c.has_key('base', 'app_egg') or \
           not c.get('base', 'app_egg'):
            c.set('base', 'app_egg', c.get('base', 'app_name'))
        
        self.config = c
        
    def _validate_config(self):
        """
        Validate application config settings.
        """
        pass
        