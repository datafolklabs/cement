
from cement.core.log import get_logger
from cement import helpers as _h

log = get_logger(__name__)
    
def register_plugin(config, options):
    """
    All plugins that are set as enabled will be imported, and this method
    will be called.  The module init method is expected to return the 
    following:
    
        plugin_config (dict)
        plugin_commands (dict)
        options (object)
        
    As a tuple:
    
        return (plugin_config, plugin_commands, options)
        
    """
    plugin_config = {
        'config_source' : ['defaults'],
        'myplugin_config_option' : True
        }
    plugin_commands = {
        'myplugin' : myplugin_method,
        'myplugin-help' : myplugin_method_help
        }
    
    # Cement allows you to expose command line options to the 
    # unified cli utility as well.   
    options.parser.add_option('--myoption', action ='store', 
        dest='myplugin_config_option', default=None, 
        help='example option for myplugin', metavar='VAR' 
        )
    return (plugin_config, plugin_commands, options)
        
            
def myplugin_method(config, cli_opts, cli_args):
    """
    This is an example method that is called when the following command is 
    run:
        
        <your_app_name> example
        
    
    All plugin commands receive the global config dict, as well as the 
    cli options that were passed at command line.
    
    Our plugin configuration comes back in the global config as:
    
        config['plugins']['myplugin']
        
    So, to access our 'example_config_option' we would reference:
    
        config['plugins']['myplugin']['example_config_options']
        
    
    Returns: True/False
    """
    if cli_opts.myplugin_config_option:
        print '--myoption passed with value %s' % cli_opts.myplugin_config_option
        
    print 'This is the myplugin...  myplugin_method()'
    log.debug('Loaded the myplugin plugin')
    return True


def myplugin_method_help(config, cli_opts, cli_args):
    """
    Help commands are hidden in the commands list, but can be called
    for any module command by adding it like this.
    """
    print 'help content for cement_example.plugins.myplugin.myplugin_method()' 
    