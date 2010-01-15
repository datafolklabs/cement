"""This is an example plugin for helloworld."""

"""
This is a simple plugin to add some basic functionality.
"""

import sys, os
import logging

from cement import namespaces
from cement.core.log import get_logger
from cement.core.opt import init_parser
from cement.core.hook import define_hook, register_hook
from cement.core.plugin import CementPlugin, register_plugin

from helloworld.appmain import VERSION, BANNER

log = get_logger(__name__)

REQUIRED_CEMENT_API = '0.5-0.6:20100115'
        
@register_plugin() 
class ExamplePlugin(CementPlugin):
    define_hook('my_example_hook')
    
    def __init__(self):
        CementPlugin.__init__(self,
            label = 'example',
            version = VERSION,
            description = 'Example plugin for helloworld',
            required_api = REQUIRED_CEMENT_API,
            version_banner=BANNER,
            )
        
        # plugin configurations can be setup this way
        self.config['example_option'] = False
        
        # plugin cli options can be setup this way.  Generally, cli options
        # are used to set config options... so if you probably want to
        # add your options to both.
        self.options.add_option('-E', '--example', action='store',
            dest='example_option', default=None, help='Example Plugin Option'
            )
           
           
# We import the controller here because the register_plugin() decorator
# must get loaded first:
from helloworld.controllers.example import ExampleController


#      
# HOOKS: Usually defined in the main plugin file (here).  Functions
# that you decorate with @register_hook() will be run whenever/wherever 
# run_hooks('the_hook_name') is called.
#
        
@register_hook()
def options_hook(*args, **kwargs):
    """
    Use this hook to add options to other namespaces.  An OptParse object is 
    expected on return, and any options will be merged into the global options.  
    Global options can also be used as local options by setting the config 
    option 'merge_global_options = true' in the plugin config.
    """
    global_options = init_parser()
    global_options.add_option('-G', '--global-option', action ='store_true', 
        dest='global_option', default=None, help='Example Global option'
    ) 
    
    # return the namespace and the global options to add.
    return ('global', global_options)

@register_hook()
def options_hook(*args, **kwargs):
    """
    We can also use the options hook to tie into other plugins, or even our
    own.  This is an alternateway of adding options for your [or other] 
    plugins.
    """
    my_options = init_parser()
    my_options.add_option('--new-local', action ='store', 
        dest='newlocal_option', default=None, help='Example Local option'
    ) 
    
    # return the namespace and the global options to add.
    return ('example', my_options)


@register_hook()
def post_options_hook(*args, **kwargs):
    """
    Use this hook if any operations need to be performed if a global
    option is passed.  Notice that we set a global option of -G in our
    global_options_hook above.  Here we can access that value from the 
    global namespace configuration.
    """
    cnf = namespaces['global'].config 
    if cnf.has_key('global_option'):
        print "global_option => %s", cnf['global_option']  
        # then do something with it  
        
@register_hook()
def my_example_hook(*args, **kwargs):
    """This is an example hook, that I define in my plugin config above."""
    return "I'm in my_example_hook"
    