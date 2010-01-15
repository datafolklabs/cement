"""Cement methods to setup the framework for applications using it."""

from pkg_resources import get_distribution

from cement import namespaces
from cement.core.configuration import CEMENT_API, set_config_opts_per_file
from cement.core.configuration import validate_config, get_default_config
from cement.core.plugin import load_all_plugins
from cement.core.namespace import CementNamespace, define_namespace
from cement.core.log import setup_logging, get_logger
from cement.core.hook import define_hook, run_hooks

log = get_logger(__name__)    

def register_default_hooks():
    """Register Cement framework hooks."""
    define_hook('options_hook')
    define_hook('post_options_hook')
    define_hook('validate_config_hook')
            
def lay_cement(default_app_config=None, version_banner=None):
    """
    Primary method to setup an application for Cement.  
    
    Arguments:
    
    config => dict containing application config.
    version_banner => Option txt displayed for --version
    """    
    vb = version_banner    
    if not version_banner:
        vb = """%s version %s""" % (
            default_app_config['app_name'],
            get_distribution(default_app_config['app_egg_name']).version
            )
        
    namespace = CementNamespace(
        label = 'global',
        version = get_distribution(default_app_config['app_egg_name']).version,
        required_api = CEMENT_API,
        config = get_default_config(),
        version_banner = vb,
        )
    define_namespace('global', namespace)
    namespaces['global'].config.update(default_app_config)
    
    register_default_hooks()
    
    validate_config(namespaces['global'].config)
    
    for cf in namespaces['global'].config['config_files']:
        set_config_opts_per_file('global', 
                                 namespaces['global'].config['app_module'], 
                                 cf)
    # initial logger
    setup_logging()
    load_all_plugins()
    
    # allow plugins to add config validation
    for res in run_hooks('validate_config_hook', 
                         config=namespaces['global'].config):
        pass
    



        
        
