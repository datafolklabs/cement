"""
This is a simple plugin to add some basic functionality.
"""
from cement.core.log import get_logger

log = get_logger(__name__)

def register_plugin(config, options):
    plugin_config = {
        'config_source' : ['defaults'],
        }
    plugin_commands = {
        'getconfig' : getconfig_command,
        'getconfig-help' : getconfig_help,
        }
    return (plugin_config, plugin_commands, options)

def getconfig_command(config, cli_opts=None, cli_args=None):
    if len(cli_args) == 2:
        config_key = cli_args[1]
        if config.has_key(config_key):
            print('')
            print('config[%s] => %s' % (config_key, config[config_key]))
            print('')
    else:
        for i in config:
            print("config[%s] => %s" % (i, config[i]))

def getconfig_help(config, cli_opts=None, cli_args=None):
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