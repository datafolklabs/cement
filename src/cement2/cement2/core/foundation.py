"""Cement core application module."""

import re
import os
import sys
import signal

from ..core import backend, exc, handler, hook, log, config, plugin
from ..core import output, extension, arg, controller, meta, cache
from ..lib import ext_configparser, ext_argparse, ext_logging
from ..lib import ext_nulloutput, ext_plugin

Log = backend.minimal_logger(__name__)    
    
class NullOut():
    def write(self, s):
        pass
        
def cement_signal_handler(signum, frame):
    """
    Catch a signal, run the cement_signal_hook, and then raise an exception 
    allowing the app to handle logic elsewhere.
    
    """      
    Log.debug('Caught signal %s' % signum)  
    
    for res in hook.run('cement_signal_hook', signum, frame):
        pass
        
    raise exc.CementSignalError(signum, frame)
                 
class CementApp(meta.MetaMixin):
    """
    The primary class to build applications from.
    
    Optional / Meta Arguments:
    
        label
            The name of the application.  This should be the common name as
            you would see and use at the command line.  For example 
            'helloworld', or 'my-awesome-app'.
            
            Default: None
    
        debug
            Toggles debug output.  By default, this setting is also overridden
            by the '[base] -> debug' config setting parsed in any
            of the application configuration files (where [base] is the 
            base configuration section of the application which is determined
            by Meta.config_section but defaults to Meta.label).
            
            Default: False
            
        argv
            A list of arguments to use for parsing command line arguments
            and options.
            
            Default: sys.argv
            
        config_section
            The base configuration section for the application.
            
            Default: None
            
            Note: Though Meta.config_section defaults to None, Cement will
            set this to the value of Meta.label (or in other words, the name
            of the application).
            
        config_defaults
            Default configuration dictionary.  Must be of type 'dict'.
            
            Default: None
            
        config_files
            List of config files to parse.  
            
            Default: None
            
        plugins
            A list of plugins to load.  This is generally considered bad 
            practice since plugins should be dynamically enabled/disabled
            via a plugin config file.  
            
            Default: []
        
        plugin_config_dir
            A directory path where plugin config files can be found.  Files
            must end in '.conf'.  By default, this setting is also overridden
            by the '[base] -> plugin_config_dir' config setting parsed in any
            of the application configuration files.
            
            Default: None
            
            Note: Though the meta default is None, Cement will set this to
            '/etc/<app_label>/plugins.d/' if not set during app.setup().
        
        plugin_dir
            A directory path where plugin code (modules) can be loaded from.
            By default, this setting is also overridden by the 
            '[base] -> plugin_dir' config setting parsed in any of the 
            application configuration files (where [base] is the 
            base configuration section of the application which is determined
            by Meta.config_section but defaults to Meta.label).
            
            Default: None
            
            Note: Though the meta default is None, Cement will set this to
            '/usr/lib/<app_label>/plugins/' if not set during app.setup()
        
        plugin_bootstrap
            A python package (dotted import path) where plugin code can be
            loaded from.  This is generally something like 'myapp.bootstrap'.
            
            Default: None
            
        catch_signals
            List of signals to catch, and raise exc.CementSignalError for.
            Can be set to None to disable signal handling.

            Default: [
                signal.SIGTERM, 
                signal.SIGINT
                ].
                
        signal_handler
            A function that is called to handle any caught signals. 
            
            Default: cement2.core.foundation.cement_signal_handler
            
        config_handler
            A handler class that implements the IConfig interface.  This can
            be a string (label of a registered handler), an uninstantiated
            class, or an instantiated class object.

            Default: cement2.lib.ext_configparser.ConfigParserConfigHandler
            
        extension_handler
            A handler class that implements the IExtension interface.  This can
            be a string (label of a registered handler), an uninstantiated
            class, or an instantiated class object.
            
            Default: cement2.core.extension.CementExtensionHandler
        
        log_handler
            A handler class that implements the ILog interface.  This can
            be a string (label of a registered handler), an uninstantiated
            class, or an instantiated class object.

            Default: cement2.lib.ext_logging.LoggingLogHandler
            
        plugin_handler
            A handler class that implements the IPlugin interface.  This can
            be a string (label of a registered handler), an uninstantiated
            class, or an instantiated class object.

            Default: cement2.lib.ext_plugin.CementPluginHandler
        
        argument_handler
            A handler class that implements the IArgument interface.  This can
            be a string (label of a registered handler), an uninstantiated
            class, or an instantiated class object.

            Default: cement2.lib.ext_argparse.ArgParseArgumentHandler
        
        output_handler
            A handler class that implements the IOutput interface.  This can
            be a string (label of a registered handler), an uninstantiated
            class, or an instantiated class object.

            Default: cement2.lib.ext_nulloutput.NullOutputHandler
            
        cache_handler
            A handler class that implements the ICache interface.  This can
            be a string (label of a registered handler), an uninstantiated
            class, or an instantiated class object.
            
            Default: None
            
        base_controller
            This is the base application controller.  If a controller is set,
            runtime operations are passed to the controller for command 
            dispatch and argument parsing when CementApp.run() is called.

            Default: None
        
        core_extensions
            List of Cement core extensions.  These are generally required by
            Cement and should only be modified if you know what you're 
            doing.  Use 'extensions' to add to this list, rather than 
            overriding core extensions.  That said if you want to prune down
            your application, you can remove core extensions if they are
            not necessary (for example if using your own log handler 
            extension you likely don't want/need LoggingLogHandler to be 
            registered).
            
            Default: [  
                'cement2.ext.ext_nulloutput',
                'cement2.ext.ext_plugin',
                'cement2.ext.ext_configparser', 
                'cement2.ext.ext_logging', 
                'cement2.ext.ext_argparse',
                ]
        
        extensions
            List of additional framework extensions to load.
            
            Default: []
        
        core_meta_override
            List of meta options that can/will be overridden by config options
            of the '[base]' config section (where [base] is the base 
            configuration section of the application which is determined by 
            Meta.config_section but defaults to Meta.label). These overrides 
            are required by the framework to function properly and should not 
            be used by end user (developers) unless you really know what 
            you're doing.  To add your own extended meta overrides please use 
            'meta_override'.
            
            Default: [
                'debug', 
                'plugin_config_dir', 
                'plugin_dir'
                ]
            
        meta_override
            List of meta options that can/will be overridden by config options
            of the '[base]' config section (where [base] is the 
            base configuration section of the application which is determined
            by Meta.config_section but defaults to Meta.label).
            
            Default: []
            
    
    Usage:
    
    The following is the simplest CementApp:
    
    .. code-block:: python
    
        from cement2.core import foundation
        try:
            app = foundation.CementApp('helloworld')
            app.setup()
            app.run()
        finally:
            app.close()
            
    A more advanced example looks like:
    
    .. code-block:: python
    
        from cement2.core import foundation, controller
        
        class MyController(controller.CementBaseController):
            class Meta:
                label = 'base'
                arguments = [
                    ( ['-f', '--foo'], dict(help='Notorious foo option') ),
                    ]
                config_defaults = dict(
                    debug=False,
                    some_config_param='some_value',
                    )
            
            @controller.expose(help='This is the default command', hide=True)
            def default(self):
                print('Hello World')
                    
        class MyApp(foundation.CementApp):
            class Meta:
                label = 'helloworld'
                extensions = [
                    'daemon',
                    'json',
                    ]
                base_controller = MyController
        
        try:
            app = MyApp()
            app.setup()
            app.run()
        finally:
            app.close()
                
    """
    class Meta:
        label = None
        debug = False
        config_files = None
        plugins = []
        plugin_config_dir = None
        plugin_bootstrap = None
        plugin_dir = None
        argv = sys.argv[1:]
        config_section = None
        config_defaults = None
        catch_signals = [signal.SIGTERM, signal.SIGINT]
        signal_handler = cement_signal_handler
        config_handler = ext_configparser.ConfigParserConfigHandler
        extension_handler = extension.CementExtensionHandler
        log_handler = ext_logging.LoggingLogHandler
        plugin_handler = ext_plugin.CementPluginHandler
        argument_handler = ext_argparse.ArgParseArgumentHandler
        output_handler = ext_nulloutput.NullOutputHandler
        cache_handler = None
        base_controller = None
        extensions = []        
        core_extensions = [  
            'cement2.ext.ext_nulloutput',
            'cement2.ext.ext_plugin',
            'cement2.ext.ext_configparser', 
            'cement2.ext.ext_logging', 
            'cement2.ext.ext_argparse',
            ]
        core_meta_override = [
            'debug', 
            'plugin_config_dir', 
            'plugin_dir'
            ]
        meta_override = []
            
    def __init__(self, label=None, **kw):                
        super(CementApp, self).__init__(**kw)
        
        # for convenience we translate this to _meta
        if label:
            self._meta.label = label
        self._validate_label()
        
        self.ext = None
        self.config = None
        self.log = None
        self.plugin = None
        self.args = None
        self.output = None
        self.controller = None
        self.cache = None
        
        # attributes
        self.argv = list(self._meta.argv)
        
        self._lay_cement()
        
    def extend(self, member_name, member_object):
        """
        Extend the CementApp() object with additional functions/classes such
        as 'app.my_custom_function()', etc.  It provides an interface for
        extensions to provide functionality that travel along with the 
        application object.
        
        Required Arguments:
        
            member_name
                The name to attach the object to.
                
            member_object
                The function or class object to attach to CementApp().
                
        """
        if hasattr(self, member_name):
            raise exc.CementRuntimeError("App member '%s' already exists!" % \
                                         member_name)
        Log.debug("extending appication with '.%s' (%s)" % \
                 (member_name, member_object))
        setattr(self, member_name, member_object)

    def _validate_label(self):
        if not self._meta.label:
            raise exc.CementRuntimeError("Application name missing.")
        
        # validate the name is ok
        ok = ['_', '-']
        for char in self._meta.label:
            if char in ok:
                continue
            
            if not char.isalnum():
                raise exc.CementRuntimeError(
                    "App label can only contain alpha-numeric, dashes, or underscores."
                    )
                    
    def setup(self):
        """
        This function wraps all '_setup' actons in one call.  It is called
        before self.run(), allowing the application to be _setup but not
        executed (possibly letting the developer perform other actions
        before full execution.).
        
        All handlers should be instantiated and callable after _setup() is
        complete.
        
        """
        Log.debug("now setting up the '%s' application" % self._meta.label)
        
        for res in hook.run('cement_pre_setup_hook', self):
            pass
        
        self._setup_signals()
        self._setup_extension_handler()
        self._setup_config_handler()
        self.validate_config()
        self._setup_cache_handler()
        self._setup_log_handler()
        self._setup_plugin_handler()
        self._setup_arg_handler()
        self._setup_output_handler()
        self._setup_controllers()

        for res in hook.run('cement_post_setup_hook', self):
            pass
             
    def run(self):
        """
        This function wraps everything together (after self._setup() is 
        called) to run the application.
        
        """
        for res in hook.run('cement_pre_run_hook', self):
            pass
        
        # If controller exists, then pass controll to it
        if self.controller:
            self.controller._dispatch()
        else:
            self._parse_args()

        for res in hook.run('cement_post_run_hook', self):
            pass

    def close(self):
        """
        Close the application.  This runs the cement_on_close_hook() allowing
        plugins/extensions/etc to 'cleanup' at the end of program execution.
        
        """
        Log.debug("closing the application")
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
        for res in hook.run('cement_pre_render_hook', self, data):
            if not type(res) is dict:
                Log.debug("pre_render_hook did not return a dict().")
            else:
                data = res
            
        if not self.output:
            Log.debug('render() called, but no output handler defined.')
            out_text = ''
        else:
            out_text = self.output.render(data, template)
            
        for res in hook.run('cement_post_render_hook', self, out_text):
            if not type(res) is str:
                Log.debug('post_render_hook did not return a str()')
            else:
                out_text = str(res)
        
        return out_text
        
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
        
    def _lay_cement(self):
        """
        Initialize the framework.
        """
        Log.debug("laying cement for the '%s' application" % \
                  self._meta.label)

        # hacks to suppress console output
        suppress_output = False
        if '--debug' in self._meta.argv:
            self._meta.debug = True
        else:
            for flag in ['--quiet', '--json', '--yaml']:
                if flag in self._meta.argv:
                    suppress_output = True
                    break

        if suppress_output:
            Log.debug('suppressing all console output per runtime config')
            backend.SAVED_STDOUT = sys.stdout
            backend.SAVED_STDERR = sys.stderr
            sys.stdout = NullOut()
            sys.stderr = NullOut()
            
        # start clean
        backend.hooks = {}
        backend.handlers = {}

        # define framework hooks
        hook.define('cement_pre_setup_hook')
        hook.define('cement_post_setup_hook')
        hook.define('cement_pre_run_hook')
        hook.define('cement_post_run_hook')
        hook.define('cement_on_close_hook')
        hook.define('cement_signal_hook')
        hook.define('cement_pre_render_hook')
        hook.define('cement_post_render_hook')
    
        # define and register handlers    
        handler.define(extension.IExtension)
        handler.define(log.ILog)
        handler.define(config.IConfig)
        handler.define(plugin.IPlugin)
        handler.define(output.IOutput)
        handler.define(arg.IArgument)
        handler.define(controller.IController)
        handler.define(cache.ICache)
        
        # extension handler is the only thing that can't be loaded... as, 
        # well, an extension.  ;)
        handler.register(extension.CementExtensionHandler)
            
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
            
    def _setup_signals(self):
        if not self._meta.catch_signals:
            Log.debug("catch_signals=None... not handling any signals")
            return
            
        for signum in self._meta.catch_signals:
            Log.debug("adding signal handler for signal %s" % signum)
            signal.signal(signum, self._meta.signal_handler)
    
    def _resolve_handler(self, handler_type, handler_def, raise_error=True):
        """
        Resolves the actual handler as it can be either a string identifying
        the handler to load from backend.handlers, or it can be an 
        instantiated or non-instantiated handler class.
        
        Returns: The instantiated handler object.
        
        """
        han = None
        if type(handler_def) == str:
            han = handler.get(handler_type, handler_def)()
        elif hasattr(handler_def, '_meta'):
            if not handler.registered(handler_type, handler_def._meta.label):
                handler.register(handler_def.__class__)
            han = handler_def
        elif hasattr(handler_def, 'Meta'):
            han = handler_def()
            if not handler.registered(handler_type, han._meta.label):
                handler.register(handler_def)
            
        msg = "Unable to resolve handler '%s' of type '%s'" % \
              (handler_def, handler_type)
        if han is not None:
            han._setup(self)
            return han
        elif han is None and raise_error:
            raise exc.CementRuntimeError(msg)
        elif han is None:
            Log.debug(msg)
        
    def _setup_extension_handler(self):
        Log.debug("setting up %s.extension handler" % self._meta.label) 
        self.ext = self._resolve_handler('extension', 
                                         self._meta.extension_handler)
        self.ext.load_extensions(self._meta.core_extensions)
        self.ext.load_extensions(self._meta.extensions)
        
    def _setup_config_handler(self):
        Log.debug("setting up %s.config handler" % self._meta.label)
        self.config = self._resolve_handler('config', 
                                            self._meta.config_handler)
        if self._meta.config_section is None:
            self._meta.config_section = self._meta.label
        self.config.add_section(self._meta.config_section)
        
        if hasattr(self._meta, 'defaults'):
            print('DEPRECATION WARNING: CementApp.Meta.defaults is ' + \
                  'deprecated.  Use CementApp.Meta.config_defaults instead.')
            self.config.merge(self._meta.defaults)
        if not self._meta.config_defaults is None:
            self.config.merge(self._meta.config_defaults)
        
        if self._meta.config_files is None:
            label = self._meta.label
            user_home = os.path.abspath(os.path.expanduser(os.environ['HOME']))
            self._meta.config_files = [
                os.path.join('/', 'etc', label, '%s.conf' % label),
                os.path.join(user_home, '.%s.conf' % label),
                ]
        for _file in self._meta.config_files:
            self.config.parse_file(_file)
        
        base_dict = self.config.get_section_dict(self._meta.config_section)
        for key in base_dict:
            if key in self._meta.core_meta_override or \
               key in self._meta.meta_override:
                setattr(self._meta, key, base_dict[key])
                                  
    def _setup_log_handler(self):
        Log.debug("setting up %s.log handler" % self._meta.label)
        self.log = self._resolve_handler('log', self._meta.log_handler)
           
    def _setup_plugin_handler(self):
        Log.debug("setting up %s.plugin handler" % self._meta.label) 
        
        # modify app defaults if not set
        if not self._meta.plugin_config_dir:
            self._meta.plugin_config_dir = '/etc/%s/plugins.d/' % self._meta.label
            
        if not self._meta.plugin_dir:
            self._meta.plugin_dir = '/usr/lib/%s/plugins' % self._meta.label

        self.plugin = self._resolve_handler('plugin', 
                                            self._meta.plugin_handler)
        self.plugin.load_plugins(self._meta.plugins)
        self.plugin.load_plugins(self.plugin.enabled_plugins)
        
    def _setup_output_handler(self):
        if self._meta.output_handler is None:
            Log.debug("no output handler defined, skipping.")
            return
            
        Log.debug("setting up %s.output handler" % self._meta.label) 
        self.output = self._resolve_handler('output', 
                                            self._meta.output_handler,
                                            raise_error=False)
         
    def _setup_cache_handler(self):
        if self._meta.cache_handler is None:
            Log.debug("no cache handler defined, skipping.")
            return
            
        Log.debug("setting up %s.cache handler" % self._meta.label) 
        self.cache = self._resolve_handler('cache', 
                                            self._meta.cache_handler,
                                            raise_error=False)
                                            
    def _setup_arg_handler(self):
        Log.debug("setting up %s.arg handler" % self._meta.label) 
        self.args = self._resolve_handler('argument', 
                                          self._meta.argument_handler)
        self.args.add_argument('--debug', dest='debug', 
            action='store_true', help='toggle debug output')
        self.args.add_argument('--quiet', dest='suppress_output', 
            action='store_true', help='suppress all output')
                 
    def _setup_controllers(self):
        Log.debug("setting up application controllers") 

        if self._meta.base_controller:
            self.controller = self._resolve_handler('controller', 
                                                    self._meta.base_controller) 
            self._meta.base_controller = self.controller
        elif self._meta.base_controller is None:
            if handler.registered('controller', 'base'):
                self.controller = self._resolve_handler('controller', 'base') 
                self._meta.base_controller = self.controller
                
        # Trump all with whats passed at the command line, and pop off the arg
        if len(self.argv) > 0:
            # translate dashes to underscore
            contr = re.sub('-', '_', self.argv[0])
                               
            h = handler.get('controller', contr, None)
            if h:
                self.controller = h()
                self.controller._setup(self)
                self.argv.pop(0)

        # if no handler can be found, that's ok
        if not self.controller:
            Log.debug("no controller could be found.")
    
    def validate_config(self):
        """
        Validate application config settings.
        """
        pass
        
        
def lay_cement(name, klass=CementApp, *args, **kw):
    """
    This function is deprecated.  Please use CementApp() directly.
    
    """
    print('DEPRECATION WARNING: lay_cement() is deprecated.  ' + \
          'Use foundation.CementApp() directly.')
    app = klass(name, *args, **kw)
    return app
