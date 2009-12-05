
from cement.core.log import get_logger

log = get_logger(__name__)

def register_plugin(config, options):
    plugin_config = {
        'config_source' : ['defaults'],
        'myconfigoption' : 'Blah'
        }
    plugin_commands = {
        'simple' : simple_command
        }
    return (plugin_config, plugin_commands, options)

def simple_command(config, cli_opts=None, cli_args=None):
    print 'This is an example command from a plugin.'