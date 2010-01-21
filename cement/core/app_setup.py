"""Cement methods to setup the framework for applications using it."""

import sys
from pkg_resources import get_distribution

from cement import namespaces
from cement.core.configuration import CEMENT_API, set_config_opts_per_file
from cement.core.configuration import validate_config, get_default_config
from cement.core.plugin import load_all_plugins
from cement.core.namespace import CementNamespace, define_namespace
from cement.core.log import setup_logging, get_logger
from cement.core.hook import register_hook, define_hook, run_hooks

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
    if not banner:
        banner = "%s version %s" % (
            config['app_name'],
            get_distribution(config['app_egg_name']).version)
        
    namespace = CementNamespace(
        label='global',
        version=get_distribution(config['app_egg_name']).version,
        required_api=CEMENT_API,
        config=get_default_config(),
        banner=banner,
        )
    define_namespace('global', namespace)
    namespaces['global'].config.update(config)
    
    register_default_hooks()
    
    validate_config(namespaces['global'].config)
    
    for cf in namespaces['global'].config['config_files']:
        set_config_opts_per_file('global', 
                                 namespaces['global'].config['app_module'], 
                                 cf)

    # Add the --json option (hack)
    try:
        namespaces['global'].options.add_option('--json', action='store_true',
            dest='enable_json', default=None, help='Display command output as json.'
            )
    except optparse.OptionConflictError, e:
        pass
            
    # Setup logging for console and file
    if '--json' in sys.argv \
        or not namespaces['global'].config['log_to_console']:
        namespaces['global'].config['show_plugin_load'] = False
        setup_logging(to_console=False)
    else:
        setup_logging()
        
    load_all_plugins()
    
    # Allow plugins to add config validation for the global namespace
    for res in run_hooks('validate_config_hook', 
                         config=namespaces['global'].config):
        pass
    

        
        
