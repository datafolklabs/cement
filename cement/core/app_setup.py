"""Cement methods to setup the framework for applications using it."""
import sys, os
import re
from pkg_resources import get_distribution
from optparse import OptionParser, IndentedHelpFormatter

from cement import plugins as cement_plugins
from cement import hooks, namespaces
from cement.core.exc import *
from cement.core.configuration import *
from cement.core.plugin import load_all_plugins
from cement.core.namespace import CementNamespace, define_namespace
from cement.core.log import setup_logging, get_logger
from cement.core.opt import init_parser, get_options, Options
from cement.core.hook import define_hook, run_hooks
from cement.core.command import CementCommand


log = get_logger(__name__)
    
def register_default_hooks():
    # define default hooks
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
    global namespaces, log
    
    vb = version_banner    
    if not version_banner:
        vb = """%s version %s""" % (
            default_app_config['app_name'],
            get_distribution(default_app_config['app_egg_name']).version
            )
        
    namespace = CementNamespace(
        label = 'global',
        version = get_distribution(default_app_config['app_egg_name']).version,
        required_abi = CEMENT_ABI,
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
    setup_logging('cement')
    #log = get_logger(__name__)                             
    
    load_all_plugins()
    setup_logging('cement')
    setup_logging(namespaces['global'].config['app_module'])
    
    # allow plugins to add config validation
    for res in run_hooks('validate_config_hook', config=namespaces['global'].config):
        pass
    



        
        
