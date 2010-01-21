"""
sayhi for the helloworld application.
"""

import os

from cement import namespaces
from cement.core.log import get_logger
from cement.core.opt import init_parser
from cement.core.hook import define_hook, register_hook
from cement.core.plugin import CementPlugin, register_plugin

log = get_logger(__name__)

VERSION = '0.1'
REQUIRED_CEMENT_API = '0.5-0.6:20100115'
BANNER = """
sayhi v%s (api:%s)
""" % (VERSION, REQUIRED_CEMENT_API)
 
@register_plugin() 
class sayhiPlugin(CementPlugin):
    #
    # Define hooks here, like so:
    #
    #   define_hook('sayhi_hook')
    
    def __init__(self):
        CementPlugin.__init__(self,
            label='sayhi',
            version=VERSION,
            description='sayhi plugin for helloworld',
            required_api=REQUIRED_CEMENT_API,
            banner=BANNER
            )
 
#      
# HOOKS: Usually defined in the main plugin file (here).  Functions
# that you decorate with @register_hook() will be run whenever/wherever 
# run_hooks('the_hook_name') is called.
#
@register_hook()
def options_hook(*args, **kwargs):
    """
    Register global options.
    """
    global_options = init_parser()
    global_options.add_option('--sayhi-global-option', action ='store_true', 
        dest='sayhi_global_option', default=None, help='example global option'
    ) 
    return ('global', global_options)
          
@register_hook()
def post_options_hook(cli_opts, cli_args, **kwargs):
    """Handle global options here."""
    pass
 
 
#          
# MODEL: For more complex applications, please consider following the MVC and
# moving your model class(es) to:
#
#   helloworld/model/sayhi.py
#
class sayhiModel(object):
    # define model class
    pass
 
    
#
# CONTROLLER: For more complex applications, please consider following the 
# MVC and moving your controller class(es) to:
#
#   helloworld/controllers/sayhi.py
#

from cement.core.controller import CementController, expose

class sayhiController(CementController):
    @expose()              
    def sayhi_command(self, opts, args):
        """Register global command."""
        print "sayhi global command run() method."
          
    @expose()            
    def sayhi_command_help(self, opts, args):
        print "sayhi global command help method."

    @expose('helloworld.templates.sayhi_command')              
    def sayhi_command2(self, opts, args):
        """Register global command, with Genshi templating."""
        foo = "Hello"
        bar = "World"
        return dict(foo=foo, bar=bar)

    @expose(namespace='sayhi')              
    def sayhi_sub_command(self, opts, args):
        """Register sub command for the sayhi namespace."""
        print "sayhi local command method."
