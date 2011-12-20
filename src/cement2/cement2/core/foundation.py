"""Cement core application module."""

import re
import sys
import signal

from cement2.core import backend, exc, handler, hook, log, config, plugin
from cement2.core import output, extension, arg, controller

Log = backend.minimal_logger(__name__)    
    
class NullOut():
    def write(self, s):
        pass
        
def cement_signal_handler(signum, frame):
    """
    Catch a signal, and then raise an exception allowing the app to handle
    logic elsewhere.
    
    """      
    Log.debug('Caught signal %s' % signum)  
    raise exc.CementSignalError(signum, frame)
        
class CementApp(object):
    """
    The CementApp is the primary application class used and returned by
    lay_cement().
    
    Required Arguments:
    
        name
            The name of the application.
            
    Optional Arguments:
    
        argv
            A list of arguments to use.  Default: sys.argv
            
        defaults
            Default configuration dictionary.
            
        catch_signals
            List of signals to catch, and raise exc.CementSignalError for.
            Default: [signals.SIGTERM, signals.SIGINT]
                
        config_handler
            An instantiated config handler object.
            
        extension_handler
            An instantiated extension handler object.
        
        log_handler
            An instantiated log handler object.
            
        plugin_handler
            An instantiated plugin handler object.
        
        arg_handler
            An instantiated argument handler object.
        
        output_handler
            An instantiated output handler object.
            
    """
    def __init__(self, name, **kw):                
        self.name = name
        if not self.name:
            raise exc.CementRuntimeError("Application name missing.")
        
        self.defaults = kw.get('defaults', backend.defaults(self.name))
        self.defaults['base']['app_name'] = self.name
        self.argv = kw.get('argv', sys.argv[1:])
        self.catch_signals = kw.get('catch_signals', 
                                    [signal.SIGTERM, signal.SIGINT])
                                    
        # default all handlers to None
        self.ext = None
        self.config = None
        self.log = None
        self.plugin = None
        self.args = None
        self.output = None
        self.controller = None
        
        # initialize handlers if passed in and set config to reflect
        if kw.get('config_handler', None):
            self.config = kw['config_handler']
            self.config.set('base', 'config_handler', self.config.Meta.label)
        
        if kw.get('extension_handler', None):
            self.ext = kw['extension_handler']
            self.config.set('base', 'extension_handler', 
                            self.ext.Meta.label)
                            
        if kw.get('log_handler', None):
            self.log = kw['log_handler']
            self.config.set('base', 'log_handler', self.log.Meta.label)
                                    
        if kw.get('plugin_handler', None):
            self.plugin = kw['plugin_handler']
            self.config.set('base', 'plugin_handler', self.plugin.Meta.label)
        
        if kw.get('arg_handler', None):
            self.args = kw['arg_handler']
            self.config.set('base', 'arg_handler', self.args.Meta.label)
            
        if kw.get('output_handler', None):
            self.output = kw['output_handler']
            self.config.set('base', 'output_handler', 
                            self.output.Meta.label)

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
        
        for res in hook.run('cement_pre_setup_hook', self):
            pass
        
        self._setup_signals()
        self._setup_extension_handler()
        self._setup_config_handler()
        self._validate_required_config()
        self.validate_config()
        self._setup_log_handler()
        self._setup_plugin_handler()
        self._setup_arg_handler()
        self._setup_output_handler()
        self._setup_controller_handler()

        for res in hook.run('cement_post_setup_hook', self):
            pass
             
    def run(self):
        """
        This function wraps everything together (after self.setup() is 
        called) to run the application.
        
        """
        for res in hook.run('cement_pre_run_hook', self):
            pass
        
        # If controller exists, then pass controll to it
        if self.controller:
            self.controller.dispatch()
        else:
            self._parse_args()

        for res in hook.run('cement_post_run_hook', self):
            pass

    def close(self):
        """
        Close the application.  This runs the cement_on_close_hook() allowing
        plugins/extensions/etc to 'cleanup' at the end of program execution.
        
        """
        for res in hook.run('cement_on_close_hook', self):
            pass
            
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
            
    @property
    def pargs(self):
        """
        A shortcut for self.args.parsed_args.
        """
        return self.args.parsed_args
     
    def add_arg(self, *args, **kw):
        """
        A shortcut for self.args.add_argument.
        
        """   
        self.args.add_argument(*args, **kw)
        
    def _set_handler_defaults(self, handler_obj):
        """
        Set config defaults per handler defaults if the config key is not 
        already set.  The configurations are set under a [section] whose
        name is that of the handlers interface type/label.  The exception
        is for handlers of type 'controllers', by which case the label of the
        controller is used.
        
        Required Arguments:
        
            handler_obj
                An instantiated handler object.
                
        """
        if not hasattr(handler_obj.Meta, 'defaults'):
            Log.debug("no config defaults from '%s'" % handler_obj)
            return 
        
        Log.debug("setting config defaults from '%s'" % handler_obj)
        
        dict_obj = dict()
        handler_type = handler_obj.Meta.interface.IMeta.label
        
        if handler_type == 'controller':
            # If its stacked, then add the defaults to the parent config
            if getattr(handler_obj.Meta, 'stacked_on', None):
                key = handler_obj.Meta.stacked_on
            else:
                key = handler_obj.Meta.label
        else:
            key = handler_type
            
        dict_obj[key] = handler_obj.Meta.defaults
        self.config.merge(dict_obj, override=False)
            
    def _parse_args(self):
        self.args.parse(self.argv)
        
        for member in dir(self.args.parsed_args):
            if member and member.startswith('_'):
                continue
            
            # don't override config values for options that weren't passed
            # or in otherwords are None
            elif getattr(self.args.parsed_args, member) is None:
                continue
                
            for section in self.config.get_sections():
                if member in self.config.keys(section):
                    self.config.set(section, member, 
                                    getattr(self.args.parsed_args, member))
        
        # If the output handler was changed after parsing args, then
        # we need to set it up again.
        if self.output:
            if self.config.get('base', 'output_handler') \
                != self.output.Meta.label:
                self.output = None
                self._setup_output_handler()
        else:
            self._setup_output_handler()
            
    def _setup_signals(self):
        for signum in self.catch_signals:
            Log.debug("adding signal handler for signal %s" % signum)
            signal.signal(signum, cement_signal_handler)
    
    def _setup_extension_handler(self):
        Log.debug("setting up %s.extension handler" % self.name) 
        if not self.ext:
            h = handler.get('extension', 
                            self.defaults['base']['extension_handler'])
            self.ext = h()
        self._set_handler_defaults(self.ext)
        self.ext.setup(self.defaults)
        self.ext.load_extensions(self.defaults['base']['extensions'])
        
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
        self.config.set('base', 'plugins', self.plugin.enabled_plugins)
        self.plugin.load_plugins(self.config.get('base', 'plugins'))
        
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
        if not self.args:
            h = handler.get('argument', 
                            self.config.get('base', 'arg_handler'))
            self.args = h()
        self._set_handler_defaults(self.args)
        self.args.setup(self.config)
        self.args.add_argument('--debug', dest='debug', 
            action='store_true', help='toggle debug output')
        self.args.add_argument('--quiet', dest='suppress_output', 
            action='store_true', help='suppress all output')
                 
    def _setup_controller_handler(self):
        Log.debug("setting up %s.controller handler" % self.name) 

        # set handler defaults for all controllers
        for contr in handler.list('controller'):
            self._set_handler_defaults(contr)
            
        # Use self.controller first(it was passed in)
        if not self.controller:
            # Only use the config'd controller if no self.controller
            h = handler.get('controller', 
                            self.config.get('base', 'controller_handler'), 
                            None)
            if h:
                self.controller = h()
                
        # Trump all with whats passed at the command line, and pop off the
        # arg
        if len(self.argv) > 0:
            # translate dashes to underscore
            contr = re.sub('-', '_', self.argv[0])
            
            h = handler.get('controller', contr, None)
            if h:
                self.controller = h()
                self.argv.pop(0)
                
        # if no handler can be found, that's ok
        if self.controller:
            self.controller.setup(self)
        else:
            Log.debug("no controller could be found.")
    
    def _validate_required_config(self):
        """
        Validate base config settings required by cement.
        """
        Log.debug("validating required configuration parameters")
        
    def validate_config(self):
        """
        Validate application config settings.
        """
        pass
        
        
def lay_cement(name, klass=CementApp, *args, **kw):
    """
    Initialize the framework.  All *args, and **kwargs are passed to the 
    klass() object.

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
    
    if kw.get('defaults', None):
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
    hook.define('cement_pre_setup_hook')
    hook.define('cement_post_setup_hook')
    hook.define('cement_pre_run_hook')
    hook.define('cement_post_run_hook')
    hook.define('cement_on_close_hook')
    
    # define and register handlers    
    handler.define(extension.IExtension)
    handler.define(log.ILog)
    handler.define(config.IConfig)
    handler.define(plugin.IPlugin)
    handler.define(output.IOutput)
    handler.define(arg.IArgument)
    handler.define(controller.IController)
    
    # extension handler is the only thing that can't be loaded... as, well, an
    # extension.  ;)
    handler.register(extension.CementExtensionHandler)
    
    app = klass(name, defaults=defaults, *args, **kw)
    return app
