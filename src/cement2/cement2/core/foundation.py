"""Cement core application module."""

import sys

from cement2.core import backend, exc, handler, hook, log, config, plugin
from cement2.core import output, extension

Log = backend.minimal_logger(__name__)

def lay_cement(name, *args, **kw):
    """
    Initialize the framework.

    Required Arguments:
    
        name
            The name of the application.
            
        
    Optional Keyword Arguments:

        defaults
            The default config dictionary, other wise use backend.defaults().
            
        argv
            List of args to use.  Default: sys.argv.
    
    """
    Log.debug("laying cement for the '%s' application" % name)
    defaults = kw.get('defaults', backend.defaults())
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
    handler.define('log', log.ILogHandler)
    handler.define('config', config.IConfigHandler)
    handler.define('extension', extension.IExtensionHandler)
    handler.define('plugin', plugin.IPluginHandler)
    handler.define('output', output.IOutputHandler)
    #define_handler('option')
    #define_handler('command')
    #define_handler('hook')
    #define_handler('error')
    
    handler.register(config.ConfigParserConfigHandler)
    handler.register(log.LoggingLogHandler)
    handler.register(extension.CementExtensionHandler)
    handler.register(plugin.CementPluginHandler)
    handler.register(output.CementOutputHandler)
    
    app = CementApp(name, *args, **kw)
    return app
    
class CementApp(object):
    def __init__(self, name, **kw):
        self.name = name
        self.defaults = kw.get('defaults', backend.defaults())
        self.defaults['base']['app_name'] = self.name
        
        # default all handlers to None
        self.extension = None
        self.config = None
        self.log = None
        self.plugin = None
        self.options = None
        self.commands = None
        self.output = None
        
        # initialize handlers if passed in and set config to reflect
        if kw.get('extension_handler', None):
            self.extension = kw['extension_handler']
            self.config.set('base', 'extension_handler', 
                            self.extension.__handler_label__)

        if kw.get('config_handler', None):
            self.config = kw['config_handler']
            self.config.set('base', 'config_handler', 
                            self.config.__handler_label__)
        
        if kw.get('log_handler', None):
            self.log = kw['log_handler']
            self.config.set('base', 'log_handler', 
                            self.log.__handler_label__)
                                    
        if kw.get('plugin_handler', None):
            self.plugin = kw['plugin_handler']
            self.config.set('base', 'plugin_handler', 
                            self.plugin.__handler_label__)
        
        if kw.get('output_handler', None):
            self.output = kw['output_handler']
            self.config.set('base', 'output_handler', 
                            self.output.__handler_label__)

    def run(self):
        Log.debug("now running the '%s' application" % self.name)
        self._setup_extension_handler()
        self._setup_config_handler()
        self._validate_required_config()
        self.validate_config()
        self._setup_log_handler()
        self._setup_plugin_handler()
        self._setup_output_handler()
        
    def _setup_extension_handler(self):
        Log.debug("setting up %s.extension handler" % self.name) 
        if not self.extension:
            h = handler.get('extension', 
                            self.defaults['base']['extension_handler'])
            self.extension = h(self.defaults)
        self.extension.load_extensions(self.defaults['base']['extensions'])
        
    def _setup_config_handler(self):
        Log.debug("setting up %s.config handler" % self.name)
        if not self.config:
            h = handler.get('config', self.defaults['base']['config_handler'])
            self.config = h(self.defaults)

        for _file in self.config.get('base', 'config_files'):
            self.config.parse_file(_file)

    def _setup_log_handler(self):
        Log.debug("setting up %s.log handler" % self.name)
        if not self.log:
            h = handler.get('log', self.config.get('base', 'log_handler'))
            self.log = h(self.config)
           
    def _setup_plugin_handler(self):
        Log.debug("setting up %s.plugin handler" % self.name) 
        if not self.plugin:
            h = handler.get('plugin', 
                            self.config.get('base', 'plugin_handler'))
            self.plugin = h(self.config)
    
    def _setup_output_handler(self):
        Log.debug("setting up %s.output handler" % self.name) 
        if not self.output:
            h = handler.get('output', 
                            self.config.get('base', 'output_handler'))
            self.output = h(self.config)
                  
    def _validate_required_config(self):
        """
        Validate base config settings required by cement.
        """
        Log.debug("validating required configuration parameters")
        # FIX ME: do something here
        pass
        
    def validate_config(self):
        """
        Validate application config settings.
        """
        pass
        