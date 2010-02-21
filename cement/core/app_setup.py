"""Cement methods to setup the framework for applications using it."""

import sys
from pkg_resources import get_distribution

from cement import namespaces, buf_stdout, buf_stderr, SAVED_STDOUT, SAVED_STDERR
from cement.core.configuration import CEMENT_API, set_config_opts_per_file
from cement.core.configuration import validate_config, get_default_config
from cement.core.plugin import load_all_plugins, get_enabled_plugins_per_files
from cement.core.namespace import CementNamespace, define_namespace, get_config
from cement.core.log import setup_logging, get_logger
from cement.core.hook import register_hook, define_hook, run_hooks
from cement.core.controller import expose

log = get_logger(__name__)    
                
def register_default_hooks():
    """
    Registers Cement framework hooks.
    
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
    
    """
    define_hook('options_hook')
    define_hook('post_options_hook')
    define_hook('validate_config_hook')
    define_hook('pre_plugins_hook')
    define_hook('post_plugins_hook')
    define_hook('bootstrap_application_hook')
    define_hook('bootstrap_plugins_hook')

def lay_cement(config=None, banner=None):
    """
    Primary method to setup an application for Cement.  
    
    Keyword arguments:
    
        config
            Dict containing application config.
    
        banner
            Optional text to display for --version
    
    
    Usage:
    
    .. code-block:: python
    
        from cement.core.configuration import get_default_config
        from cement.core.app_setup import lay_cement
        
        lay_cement(get_default_config())
        
    """    
    global namespaces
    
    if not banner:
        banner = "%s version %s" % (
            config['app_name'],
            get_distribution(config['app_egg_name']).version)
        
    register_default_hooks()
    
    namespace = CementNamespace(
        label='root',
        version=get_distribution(config['app_egg_name']).version,
        required_api=CEMENT_API,
        config=get_default_config(),
        banner=banner
        )
    define_namespace('root', namespace)
    namespaces['root'].config.update(config)
    
    root_mod = __import__("%s.controllers.root" % namespaces['root'].config['app_module'], 
                          globals(), locals(), ['root'], -1)
    namespaces['root'].controller = getattr(root_mod, 'RootController')
    
    for cf in namespaces['root'].config['config_files']:
        set_config_opts_per_file('root', 'root', cf)

    validate_config(namespaces['root'].config)
    get_enabled_plugins_per_files()
    
    # hardcoded hacks
    if '--quiet' in sys.argv:
        namespaces['root'].config['log_to_console'] = False
        sys.stdout = buf_stdout
        sys.stderr = buf_stderr
    if '--json' in sys.argv:
        sys.stdout = buf_stdout
        sys.stderr = buf_stderr
        namespaces['root'].config['output_engine'] = 'json'
        namespaces['root'].config['show_plugin_load'] = False
    # debug trumps everything
    if '--debug' in sys.argv:
        namespaces['root'].config['debug'] = True
        namespaces['root'].config['log_to_console'] = True
        sys.stdout = SAVED_STDOUT
        sys.stderr = SAVED_STDERR
        
    # Setup logging for console and file
    setup_logging(to_console=namespaces['root'].config['log_to_console'])
        
    boot = __import__("%s.bootstrap" % namespaces['root'].config['app_module'], 
                          globals(), locals(), ['root'], -1)
    
    # bootstrap application
    for res in run_hooks('bootstrap_application_hook'):
        pass
        
    load_all_plugins()
    
    # Looks dirty, but this creates json counter part commands that are hidden
    for nam in namespaces:
        commands = namespaces[nam].commands.copy()
        for command in commands:
            # Shorten it
            cmd = commands[command]
            controller = namespaces[cmd['controller_namespace']].controller
        
            # Run the command function
            func = cmd['original_func']
            name="%s_json" % cmd['func']
            json_func = expose(template='json', namespace=nam, is_hidden=True, 
                               name=name)(func)

            setattr(namespaces[cmd['controller_namespace']].controller, 
                    name, json_func) 
            
    # Allow plugins to add config validation for the global namespace
    for res in run_hooks('validate_config_hook', 
                         config=namespaces['root'].config):
        pass
    
    # Merge namespaces under root dict
    for nam in namespaces:
        if nam != 'root':
            namespaces['root'].config[nam] = get_config(nam)
