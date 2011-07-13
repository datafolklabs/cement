"""Cement core application module."""

import sys

from cement2.core import backend, exc, handler, hook, log, config, plugin
from cement2.core import output, extension, arg

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
    
    if kw.get('defaults'):
        defaults = kw['defaults']
        del kw['defaults']
    else:
        defaults = backend.defaults()
        
    argv = kw.get('argv', sys.argv[1:])

    # basic logging setup first (mostly for debug/error)
    if '--debug' in argv:
        defaults['log']['level'] = 'DEBUG'
        defaults['base']['debug'] = True
    elif '--quiet' in argv:
        defaults['log']['to_console'] = False
        
        # a hack to suppress output
        sys.stdout = open('/dev/null', 'w+')
        sys.stderr = open('/dev/null', 'w+')

    elif '--json' in argv or '--yaml' in argv:
        # The framework doesn't provide --json/--yaml options but rather
        # extensions do.  That said, the --json/--yaml extensions are shipped
        # with our source so we can add a few hacks here.
        defaults['log']['to_console'] = False
        
        # a hack to suppress output
        sys.stdout = open('/dev/null', 'w+')
        sys.stderr = open('/dev/null', 'w+')
        
    # define framework hooks
    hook.define('cement_init_hook')
    hook.define('cement_add_args_hook')
    hook.define('cement_post_args_hook')
    hook.define('cement_validate_config_hook')
    hook.define('cement_pre_plugins_hook')
    hook.define('cement_post_plugins_hook')
    hook.define('cement_post_bootstrap_hook')
    
    for res in hook.run('cement_init_hook'):
        pass
        
    # define and register handlers    
    handler.define('log', log.ILogHandler)
    handler.define('config', config.IConfigHandler)
    handler.define('extension', extension.IExtensionHandler)
    handler.define('plugin', plugin.IPluginHandler)
    handler.define('output', output.IOutputHandler)
    handler.define('arg', arg.IArgumentHandler)
    #define_handler('command')
    #define_handler('hook')
    #define_handler('error')
    
    #handler.register(config.ConfigParserConfigHandler)
    #handler.register(log.LoggingLogHandler)
    handler.register(extension.CementExtensionHandler)
    handler.register(plugin.CementPluginHandler)
    #handler.register(output.CementOutputHandler)
    
    app = CementApp(name, defaults=defaults, argv=argv, *args, **kw)
    return app
    
class CementApp(object):
    def __init__(self, name, **kw):
        self.name = name
        self.defaults = kw.get('defaults', backend.defaults())
        self.defaults['base']['app_name'] = self.name
        self.argv = kw.get('argv', sys.argv[1:])
        
        # default all handlers to None
        self.extension = None
        self.config = None
        self.log = None
        self.plugin = None
        self.arg = None
        self.output = None
        
        # initialize handlers if passed in and set config to reflect
        if kw.get('config_handler', None):
            self.config = kw['config_handler']
            self.config.set('base', 'config_handler', 
                            self.config.__handler_label__)
        
        if kw.get('extension_handler', None):
            self.extension = kw['extension_handler']
            self.config.set('base', 'extension_handler', 
                            self.extension.__handler_label__)
                            
        if kw.get('log_handler', None):
            self.log = kw['log_handler']
            self.config.set('base', 'log_handler', 
                            self.log.__handler_label__)
                                    
        if kw.get('plugin_handler', None):
            self.plugin = kw['plugin_handler']
            self.config.set('base', 'plugin_handler', 
                            self.plugin.__handler_label__)
        
        if kw.get('arg_handler', None):
            self.arg = kw['arg_handler']
            self.config.set('base', 'arg_handler', self.arg.__handler_label__)
            
        if kw.get('output_handler', None):
            self.output = kw['output_handler']
            self.config.set('base', 'output_handler', 
                            self.output.__handler_label__)

    def setup(self):
        Log.debug("now setting up the '%s' application" % self.name)
        self._setup_extension_handler()
        self._setup_config_handler()
        self._validate_required_config()
        self.validate_config()
        self._setup_log_handler()
        self._setup_plugin_handler()
        self._setup_arg_handler()
        self._setup_output_handler()
        
    def run(self):
        self._parse_args()
        
    def _parse_args(self):
        self.arg.parse(self.argv)
        for member in dir(self.arg.result):
            if member.startswith('_'):
                continue
            for section in self.config.get_sections():
                if member in self.config.keys(section):
                    self.config.set(section, member, 
                                    getattr(self.arg.result, member))
        
        if self.config.get('base', 'output_handler') \
            != self.output.__handler_label__:                                  
            self.output = None
            self._setup_output_handler()
        
    def _setup_extension_handler(self):
        Log.debug("setting up %s.extension handler" % self.name) 
        if not self.extension:
            h = handler.get('extension', 
                            self.defaults['base']['extension_handler'])
            self.extension = h()
        self.extension.setup(self.defaults)
        self.extension.load_extensions(self.defaults['base']['extensions'])
        
    def _setup_config_handler(self):
        Log.debug("setting up %s.config handler" % self.name)
        if not self.config:
            h = handler.get('config', self.defaults['base']['config_handler'])
            self.config = h()

        self.config.setup(self.defaults)
        for _file in self.config.get('base', 'config_files'):
            self.config.parse_file(_file)

    def _setup_log_handler(self):
        Log.debug("setting up %s.log handler" % self.name)
        if not self.log:
            h = handler.get('log', self.config.get('base', 'log_handler'))
            self.log = h()
        self.log.setup(self.config)
           
    def _setup_plugin_handler(self):
        Log.debug("setting up %s.plugin handler" % self.name) 
        if not self.plugin:
            h = handler.get('plugin', 
                            self.config.get('base', 'plugin_handler'))
            self.plugin = h()
        self.plugin.setup(self.config)
        
    def _setup_output_handler(self):
        Log.debug("setting up %s.output handler" % self.name) 
        if not self.output:
            h = handler.get('output', 
                            self.config.get('base', 'output_handler'))
            self.output = h()
        self.output.setup(self.config)
         
    def _setup_arg_handler(self):
        Log.debug("setting up %s.arg handler" % self.name) 
        if not self.arg:
            h = handler.get('arg', self.config.get('base', 'arg_handler'))
            self.arg = h()
        self.arg.setup(self.config)
        self.arg.minimal_add_argument('--debug', dest='debug', 
            action='store_true', help='toggle debug output')
        self.arg.minimal_add_argument('--quiet', dest='suppress_output', 
            action='store_true', help='suppress all output')
        for arg_obj in hook.run('cement_add_args_hook', self.config, self.arg):
            pass
                 
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
        