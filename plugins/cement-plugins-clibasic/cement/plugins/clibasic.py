"""
This is a simple plugin to add some basic functionality.
"""

import os
from pkg_resources import get_distribution

from cement.core.log import get_logger
from cement.core.app_setup import CementCommand, CementPlugin
from cement.core.options import init_parser

log = get_logger(__name__)

def register_plugin(global_config):
    return CLIBasicPlugin(global_config)

class CLIBasicPlugin(CementPlugin):
    def __init__(self, global_config):
        CementPlugin.__init__(self, global_config)
        self.version = get_distribution('cement').version
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
        self.options = init_parser(global_config)
        self.options.parser.add_option('--debug', action ='store_true', 
            dest='debug', default=None, help='toggle debug output'
            ) 
        
        
class GetConfigCommand(CementCommand):
    def run(self):
        if len(self.cli_args) == 2:
            config_key = self.cli_args[1]
            if self.config.has_key(config_key):
                print('')
                print('config[%s] => %s' % (config_key, self.config[config_key]))
                print('')
        else:
            for i in self.config:
                print("config[%s] => %s" % (i, self.config[i]))
                
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


class ListPluginsCommand(CementCommand):
    def run(self):
        print
        print "%-18s  %-7s  %-50s" % ('plugin', 'ver', 'description')
        print "%-18s  %-7s  %-50s" % ('-'*18, '-'*7, '-'*50)
        
        for plugin in self.config['plugins']:
            plugin_cls = self.config['plugins'][plugin]
            print "%-18s  %-7s  %-50s" % (
                plugin, plugin_cls.version, plugin_cls.description
                )
        print