"""
myplugin for the helloworld application.
"""

import os

from cement.core.log import get_logger
from cement.core.app_setup import CementCommand, CementPlugin, register_hook, \
                                  register_command, register_plugin
from cement.core.options import init_parser

log = get_logger(__name__)

VERSION = '0.1'
REQUIRED_CEMENT_ABI = '20091211'
BANNER = """
myplugin v%s (abi:%s)
""" % (VERSION, REQUIRED_CEMENT_ABI)
 
@register_plugin() 
class mypluginPlugin(CementPlugin):
    def __init__(self):
        CementPlugin.__init__(self,
            label = 'myplugin',
            version = VERSION,
            description = 'myplugin Plugin for Applications using Cement Framework',
            required_abi = REQUIRED_CEMENT_ABI,
            version_banner=BANNER
            )
      
@register_hook()
def global_options_hook(*args, **kwargs):
    """
    Register global options.
    """
    global_options = init_parser()
    global_options.add_option('--myplugin-global-option', action ='store_true', 
        dest='myplugin_global_option', default=None, help='example global option'
    ) 
    return global_options
          
@register_command(name='myplugin-command')              
class mypluginCommand(CementCommand):
    """
    Register global commands.
    """
    def run(self):
        print "myplugin global command run() method."
                
    def help(self):
        print "myplugin global command help() method."


@register_command(name='myplugin_command', namespace='myplugin')              
class mypluginLocalCommand(CementCommand):
    """
    Register local commands.
    """
    def run(self):
        print "myplugin local command run() method."
                
    def help(self):
        print "myplugin local command help() method."
