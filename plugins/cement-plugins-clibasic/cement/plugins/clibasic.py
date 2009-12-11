"""
This is a simple plugin to add some basic functionality.
"""

import os
from pkg_resources import get_distribution

from cement import config
from cement.core.log import get_logger
from cement.core.app_setup import CementCommand, CementPlugin, register_hook, \
                                  register_command
from cement.core.options import init_parser

log = get_logger(__name__)

def register_plugin():
    return CLIBasicPlugin()

class CLIBasicPlugin(CementPlugin):
    def __init__(self):
        CementPlugin.__init__(self)
        self.version = '0.1'
        self.required_abi = '20091207'
        self.description = "Basic CLI Commands for Cement Applications"
        self.config = {
            'config_source': ['defaults']
            }
        self.commands = {
            'getconfig' : GetConfigCommand,
            'listplugins' : ListPluginsCommand
            }
        self.handlers = {}
        
@register_hook()
def global_option_hook(*args, **kwargs):
    """
    Pass back an OptParse object, options will be merged into the global
    options.
    """
    global_options = init_parser()
    global_options.parser.add_option('--debug', action ='store_true', 
        dest='debug', default=None, help='toggle debug output'
        ) 
    return global_options


@register_command(name='getconfig')
class GetConfigCommand(CementCommand):
    def run(self):
        if len(self.cli_args) == 2:
            config_key = self.cli_args[1]
            if config.has_key(config_key):
                print('')
                print('config[%s] => %s' % (config_key, config[config_key]))
                print('')
        else:
            for i in config:
                print("config[%s] => %s" % (i, config[i]))
                
    def help(self):
        print('')
        print('-' * 77) 
        print('')
        print('Print out entire config dict:')
        print('')
        print('    myapp getconfig')
        print('')
        print('Or specify a config key for just that value:')
        print('')
        print('    myapp getconfig enabled_plugins')
        print('')
        print('')


@register_command(name='listplugins')
class ListPluginsCommand(CementCommand):
    def run(self):
        print
        print "%-18s  %-7s  %-50s" % ('plugin', 'ver', 'description')
        print "%-18s  %-7s  %-50s" % ('-'*18, '-'*7, '-'*50)
        
        for plugin in config['plugins']:
            plugin_cls = config['plugins'][plugin]
            print "%-18s  %-7s  %-50s" % (
                plugin, plugin_cls.version, plugin_cls.description
                )
        print