"""Cement core application module."""

import sys

from cement2.core import backend, exc, handler, hook, log, config, plugin
from cement2.core import output, extension, arg

Log = backend.minimal_logger(__name__)    
    
class NullOut():
    def write(self, s):
        pass
        
class CementApp(object):
    def __init__(self, name, **kw):
        self.name = name
        self.defaults = kw.get('defaults', backend.defaults(self.name))
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
            self.config.set('base', 'config_handler', self.config.meta.label)
        
        if kw.get('extension_handler', None):
            self.extension = kw['extension_handler']
            self.config.set('base', 'extension_handler', 
                            self.extension.meta.label)
                            
        if kw.get('log_handler', None):
            self.log = kw['log_handler']
            self.config.set('base', 'log_handler', self.log.meta.label)
                                    
        if kw.get('plugin_handler', None):
            self.plugin = kw['plugin_handler']
            self.config.set('base', 'plugin_handler', self.plugin.meta.label)
        
        if kw.get('arg_handler', None):
            self.arg = kw['arg_handler']
            self.config.set('base', 'arg_handler', self.arg.meta.label)
            
        if kw.get('output_handler', None):
            self.output = kw['output_handler']
            self.config.set('base', 'output_handler', 
                            self.output.meta.label)

    def setup(self):
        """
        This function wraps all 'setup' actons in one call.  It is called
        before self.run(), allowing the application to be setup but not
        executed (possibly letting the developer perform other actions
        before full execution.).
        
        All handlers should be instantiated and callable after setup() is
        complete.
        
        """
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
        """
        This function wraps everything together (after self.setup() is 
        called) to run the application.
        
        """
        self._parse_args()
        
    def render(self, data, template=None):
        """
        This is a simple wrapper around self.output.render() which simply
        returns an empty string if no self.output handler is defined.
        
        Required Arguments:
        
            data
                The data dictionary to render.
                
        Optional Arguments:
        
            template
                The template to render to.  Default: None (some output 
                handlers do not use templates).
                
        """
        if not self.output:
            Log.debug('render() called, but no output handler defined.')
            return ''
        else:
            return self.output.render(data, template)
            
    def _set_handler_defaults(self, handler_obj):
        """
        Set config defaults per handler defaults if the config key is not 
        already set.
        
        Required Arguments:
        
            handler_obj
                An instantiated handler object.
                
        """
        
        if hasattr(handler_obj.meta, 'defaults'):
            Log.debug("setting config defaults from handlers['%s']['%s']" % \
                     (handler_obj.meta.type, handler_obj.meta.label)) 
            for key in handler_obj.meta.defaults:
                if not self.config.has_section(handler_obj.meta.type):
                    self.config.add_section(handler_obj.meta.type)
                if not self.config.has_key(handler_obj.meta.type, key):
                    self.config.set(handler_obj.meta.type, key,
                                    handler_obj.meta.defaults[key])
        else:
            Log.debug("no config defaults from handlers['%s']['%s']" % \
                     (handler_obj.meta.type, handler_obj.meta.label))                        
                     
    def _parse_args(self):
        self.arg.parse(self.argv)
        for member in dir(self.arg.result):
            # ignore None values
            if member is None:
                continue
                
            if member.startswith('_'):
                continue
            for section in self.config.get_sections():
                if member in self.config.keys(section):
                    self.config.set(section, member, 
                                    getattr(self.arg.result, member))
        
        # If the output handler was changed after parsing args, then
        # we need to set it up again.
        if self.output:
            if self.config.get('base', 'output_handler') \
                != self.output.meta.label:
                self.output = None
                self._setup_output_handler()
        else:
            self._setup_output_handler()
            
    def _setup_extension_handler(self):
        Log.debug("setting up %s.extension handler" % self.name) 
        if not self.extension:
            h = handler.get('extension', 
                            self.defaults['base']['extension_handler'])
            self.extension = h()
        self._set_handler_defaults(self.extension)
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
        self._set_handler_defaults(self.log)
        self.log.setup(self.config)
           
    def _setup_plugin_handler(self):
        Log.debug("setting up %s.plugin handler" % self.name) 
        if not self.plugin:
            h = handler.get('plugin', 
                            self.config.get('base', 'plugin_handler'))
            self.plugin = h()
        self._set_handler_defaults(self.plugin)
        self.plugin.setup(self.config)
        
    def _setup_output_handler(self):
        Log.debug("setting up %s.output handler" % self.name) 
        if not self.output:
            if not self.config.get('base', 'output_handler'):
                return
            h = handler.get('output', 
                            self.config.get('base', 'output_handler'))
            self.output = h()
        self._set_handler_defaults(self.output)
        self.output.setup(self.config)
         
    def _setup_arg_handler(self):
        Log.debug("setting up %s.arg handler" % self.name) 
        if not self.arg:
            h = handler.get('arg', self.config.get('base', 'arg_handler'))
            self.arg = h()
        self._set_handler_defaults(self.arg)
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
        
        
def lay_cement(name, klass=CementApp, *args, **kw):
    """
    Initialize the framework.

    Required Arguments:
    
        name
            The name of the application.
            
        
    Optional Keyword Arguments:

        klass
            The 'CementApp' class to instantiate and return.
            
        defaults
            The default config dictionary, other wise use backend.defaults().
            
        argv
            List of command line arguments.  Default: sys.argv.
            
    """
    Log.debug("laying cement for the '%s' application" % name)
    
    if kw.get('defaults'):
        defaults = kw['defaults']
        del kw['defaults']
    else:
        defaults = backend.defaults(name)
        
    argv = kw.get('argv', sys.argv[1:])

    # basic logging setup first (mostly for debug/error)
    suppress_output = False
    if '--debug' in argv:
        defaults['base']['debug'] = True
    elif '--quiet' in argv:
        suppress_output = True
        
    elif '--json' in argv or '--yaml' in argv:
        # The framework doesn't provide --json/--yaml options but rather
        # extensions do.  That said, the --json/--yaml extensions are shipped
        # with our source so we can add a few hacks here.
        suppress_output = True
        
    # a hack to suppress output
    if suppress_output:
        backend.SAVED_STDOUT = sys.stdout
        backend.SAVED_STDERR = sys.stderr
        sys.stdout = NullOut()
        sys.stderr = NullOut()
        
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
    
    # extension handler is the only thing that can't be loaded... as, well, an
    # extension.  ;)
    handler.register(extension.CementExtensionHandler)
    
    app = klass(name, defaults=defaults, *args, **kw)
    return app
