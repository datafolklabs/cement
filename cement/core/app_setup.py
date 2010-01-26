"""Cement methods to setup the framework for applications using it."""

import sys
from pkg_resources import get_distribution

from cement import namespaces, buf_stdout, buf_stderr
from cement.core.configuration import CEMENT_API, set_config_opts_per_file
from cement.core.configuration import validate_config, get_default_config
from cement.core.plugin import load_all_plugins
from cement.core.namespace import CementNamespace, define_namespace
from cement.core.log import setup_logging, get_logger
from cement.core.hook import register_hook, define_hook, run_hooks
from cement.core.controller import expose

log = get_logger(__name__)    


        
def register_default_hooks():
    """
    Registers Cement framework hooks.
    
    Hook definitions:
    options_hook         -- Used to add options to a namespaces options object
    post_options_hook    -- Run after all options have been setup and merged
    validate_config_hook -- Run after config options are setup
    pre_plugins_hook     -- Run just before all plugins are loaded (run once)
    post_plugins_hook    -- Run just after all plugins are loaded (run once)
    
    """
    define_hook('options_hook')
    define_hook('post_options_hook')
    define_hook('validate_config_hook')
    define_hook('pre_plugins_hook')
    define_hook('post_plugins_hook')

def lay_cement(config=None, banner=None):
    """
    Primary method to setup an application for Cement.  
    
    Keyword arguments:
    config  -- Dict containing application config.
    banner  -- Optional text to display for --version
    """    
    global namespaces
    
    if not banner:
        banner = "%s version %s" % (
            config['app_name'],
            get_distribution(config['app_egg_name']).version)
        
    
    
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
    
    register_default_hooks()
    
    validate_config(namespaces['root'].config)
    
    for cf in namespaces['root'].config['config_files']:
        set_config_opts_per_file('root', 
                                 namespaces['root'].config['app_module'], 
                                 cf)

    # Add hardcoded options hacks... might move this to a hook or plugin later
    try:
        namespaces['root'].options.add_option('--json', action='store_true',
            dest='enable_json', default=None, 
            help='render command output as json (Cement CLI-API)'
            )
        namespaces['root'].options.add_option('--debug', action='store_true',
            dest='debug', default=None, help='toggle debug output'
            )
        namespaces['root'].options.add_option('--quiet', action='store_true',
            dest='quiet', default=None, help='disable console logging'
            )
    except optparse.OptionConflictError, e:
        pass
            
    # hardcoded options hacks... 
    if '--debug' in sys.argv:
        namespaces['root'].config['debug'] = True
    if '--quiet' in sys.argv:
        namespaces['root'].config['log_to_console'] = False
        sys.stdout = buf_stdout
        sys.stderr = buf_stderr
        
    # Setup logging for console and file
    if '--json' in sys.argv \
        or not namespaces['root'].config['log_to_console']:
        sys.stdout = buf_stdout
        sys.stderr = buf_stderr
        namespaces['root'].config['show_plugin_load'] = False
        setup_logging(to_console=False)
    else:
        setup_logging()
        
    load_all_plugins()
    
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

            setattr(namespaces[cmd['controller_namespace']].controller, name, json_func) 
            
    # Allow plugins to add config validation for the global namespace
    for res in run_hooks('validate_config_hook', 
                         config=namespaces['root'].config):
        pass
    

        
        
