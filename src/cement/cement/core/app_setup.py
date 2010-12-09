"""Cement methods to setup the framework for applications using it."""

import sys
import logging

from cement import namespaces
from cement import buf_stdout, buf_stderr, SAVED_STDOUT, SAVED_STDERR
from cement.core.exc import CementConfigError
from cement.core.configuration import set_config_opts_per_file
from cement.core.configuration import validate_config, get_default_config
from cement.core.plugin import load_all_plugins
from cement.core.namespace import CementNamespace, define_namespace, get_config
from cement.core.log import setup_logging, get_logger
from cement.core.hook import define_hook, run_hooks
from cement.core.handler import define_handler, register_handler
from cement.core.view import GenshiOutputHandler, JsonOutputHandler
      
def define_default_hooks():
    """
    Defines Cement framework hooks.
    
    Hook definitions:
    
        options_hook
            Used to add options to a namespaces options object
        
        post_options_hook
            Run after all options have been setup and merged
        
        validate_config_hook
            Run after config options are setup

        pre_plugins_hook
            Run just before all plugins are loaded (run once)

        post_plugins_hook
            Run just after all plugins are loaded (run once)
        
        post_bootstrap_hook
            Run just after the root bootstrap is loaded.
    
    """
    define_hook('options_hook')
    define_hook('post_options_hook')
    define_hook('validate_config_hook')
    define_hook('pre_plugins_hook')
    define_hook('post_plugins_hook')
    define_hook('post_bootstrap_hook')

def define_default_handler_types():
    """
    Defines Cement framework handlers.
    
    Handler Definitions:
    
        output
            Output handlers are responsible for rendering output as returned
            from controller functions.  This may be 'Genshi', 'json', 'yaml',
            'Jinja2', etc.
            
    """
    define_handler('output')

def register_default_handlers():
    """
    Register the default base level handlers required to run a Cement
    application.
    """
    register_handler('output', 'genshi', GenshiOutputHandler)
    register_handler('output', 'json', JsonOutputHandler)
    
def lay_cement(config, **kw):
    """
    Primary method to setup an application for Cement.  
    
    Required Arguments:
    
        config
            Dict containing application config.
    
    Optional Keyword Arguments:
    
        banner
            Optional text to display for --version
        
        args
            Args to use (default: sys.argv)... if passed, args overrides 
            sys.argv because optparse accesses sys.argv.
        
    Usage:
    
    .. code-block:: python
    
        from cement.core.configuration import get_default_config
        from cement.core.app_setup import lay_cement
        
        lay_cement(get_default_config())
        
    """    
    
    args = kw.get('args', None)
    banner = kw.get('banner', None)
    version = kw.get('version', None)
    
    if not version:
        from pkg_resources import get_distribution
        version = get_distribution(config['app_egg_name']).version
    
    # DEPRECATED: compat with 0.8.8
    if not args and kw.get('cli_args', None): 
        args = kw['cli_args']
    
    # a bit of a hack, but optparse and others use sys.argv
    if args:
        sys.argv = args
        
    try:
        assert config, "default config required!"
    except AssertionError, error:
        raise CementConfigError, error.message
     
    if not banner:
        banner = "%s version %s" % (
            config['app_name'],
            version)
        
    namespace = CementNamespace(
        label='root',
        version=version,
        config=get_default_config(),
        banner=banner,
        provider=config['app_module']
        )
    define_namespace('root', namespace)
    namespaces['root'].config.update(config)
    
    root_mod = __import__("%s.controllers.root" % \
                          namespaces['root'].config['app_module'], 
                          globals(), locals(), ['root'])
    namespaces['root'].controller = getattr(root_mod, 'RootController')
        
    for config_file in namespaces['root'].config['config_files']:
        set_config_opts_per_file('root', 'root', config_file)

    validate_config(namespaces['root'].config)
    
    # hardcoded hacks
    if '--quiet' in sys.argv:
        namespaces['root'].config['log_to_console'] = False
        sys.stdout = buf_stdout
        sys.stderr = buf_stderr
    if '--json' in sys.argv:
        sys.stdout = buf_stdout
        sys.stderr = buf_stderr
        namespaces['root'].config['output_handler_override'] = 'json'
        namespaces['root'].config['show_plugin_load'] = False
    # debug trumps everything
    if '--debug' in sys.argv:
        namespaces['root'].config['debug'] = True
        namespaces['root'].config['log_to_console'] = True
        sys.stdout = SAVED_STDOUT
        sys.stderr = SAVED_STDERR
        
    # Setup logging for console and file
    setup_logging(to_console=namespaces['root'].config['log_to_console'])
    log = get_logger(__name__)
    log.debug('logging initialized')
    log.debug('setup app per the following configs: %s' % \
              namespaces['root'].config['config_files'])
    define_default_hooks()
    define_default_handler_types()
    
    register_default_handlers()
    
    __import__("%s.bootstrap" % namespaces['root'].config['app_module'], 
               globals(), locals(), ['root'])
    
    for res in run_hooks('post_bootstrap_hook'):
        pass
    
    # load all plugins
    load_all_plugins()
    
    # Allow plugins to add config validation for the global namespace
    for res in run_hooks('validate_config_hook', 
                         config=namespaces['root'].config):
        pass
    
    # Merge namespaces under root dict
    for nam in namespaces:
        if nam != 'root':
            namespaces['root'].config[nam] = get_config(nam)
