"""
This is a bare minimum Cement plugin.  See ./examples/CementExamplePlugin
for a more verbose and commented plugin example.
"""

from pkg_resources import get_distribution

from cement.core.log import get_logger
from cement.core.app_setup import CementCommand, CementPlugin
from cement.core.options import init_parser

log = get_logger(__name__)

def register_plugin(global_config):
    return SimplePlugin(global_config)

class SimplePlugin(CementPlugin):
    def __init__(self, global_config):
        CementPlugin.__init__(self, global_config)
        self.version = get_distribution('cement_example').version
        self.required_abi = '20091207'
        self.description = "Example Simple Plugin for Cement Applications"
        self.config = {
            'config_source': ['defaults']
            }
        self.commands = {
            'simple' : SimpleCommand,
            }
        self.handlers = {}
        self.options = init_parser(global_config)
  
        
class SimpleCommand(CementCommand):
    def run(self):
        print "This is cement_example.plugins.simple.SimpleCommand().run()"
    
    def help(self):
        print "This is the help for cement_example.plugins.simple.SimpleCommand().run()"