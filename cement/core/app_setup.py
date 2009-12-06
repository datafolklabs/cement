"""Cement methods to setup the framework for applications using it."""
import os
from pkg_resources import get_distribution

from cement.core.log import setup_logging
from cement.core.options import init_parser, parse_options
from cement.core.config import set_config_opts_per_file
from cement.core.options import set_config_opts_per_cli_opts
from cement.core.exc import CementConfigError

def lay_cement(config, version_banner=None):
    """
    Primary method to setup an application for Cement.  
    
    Arguments:
    
    config => dict containing application config.
    version_banner => Option txt displayed for --version
    """
    validate_config(config)
    
    if not version_banner:
        version_banner = get_distribution(config['app_module']).version
        
    config = set_config_opts_per_file(config, config['app_module'], 
                                      config['config_file'])
    options = init_parser(config, version_banner)
    (config, plugin_commands, options) = load_all_plugins(config, options)
    (config, cli_opts, cli_args) = parse_options(config, options, 
                                                 plugin_commands)
    config = set_config_opts_per_cli_opts(config, cli_opts)
    setup_logging(config)
    return (config, cli_opts, cli_args, plugin_commands)


def validate_config(config):
    """
    Validate that all required cement configuration options are set.
    """
    required_settings = [
        'config_source', 'config_file', 'debug', 'datadir',
        'enabled_plugins', 'plugin_config_dir', 'plugin_dir', 
        'plugins', 'app_module', 'app_name', 'tmpdir'
        ]
    for s in required_settings:
        if not config.has_key(s):
            raise CementConfigError, "config['%s'] value missing!" % s
    
    # create all directories if missing
    for d in [os.path.dirname(config['log_file']), config['datadir'], 
              config['plugin_config_dir'], config['plugin_dir'], 
              config['tmpdir']]:
        if not os.path.exists(d):
            os.makedirs(d)
            
            
def load_plugin(config, options, plugin):
    """
    Load a cement type plugin.  
    
    Arguments:
    
    config  => The existing config dict.
    options => A OptParse object.
    plugin  => Name of the plugin to load.
    """
    if config.has_key('show_plugin_load') and config['show_plugin_load']:
        print 'loading %s plugin' % plugin
    
    try: 
        app_module = __import__(config['app_module'])
    except ImportError, e:
        raise CementConfigError, e
            
    # try from 'app_module' first, then cement name space    
    try:
        plugins_module = __import__('%s.plugins' % config['app_module'],
                                globals(), locals(),
                                [plugin], 0)
        pluginobj = getattr(plugins_module, plugin)
    except ImportError, e:
        # we allow all apps to use cement plugins like their own.
        try:
            pluginobj = getattr(cement.plugins, plugin)
        except ImportError, e:
            raise CementConfigError, \
                'failed to load %s plugin: %s' % (plugin, e)    
    res = pluginobj.register_plugin(config, options)

    (p_config, p_commands, options) = res
    plugin_config_file = os.path.join(
        config['plugin_config_dir'], '%s.plugin' % plugin
        )
    p_config = set_config_opts_per_file(p_config, plugin, plugin_config_file)

    # update the config
    config['plugins'][plugin] = p_config
        
    return (config, p_commands, options)
    
        
def load_all_plugins(config, options):
    """
    Attempt to load all enabled plugins.  Passes the existing config and 
    options object to each plugin and allows them to add/update each.
    """
    plugin_commands = {}
    for plugin in config['enabled_plugins']:
        res = load_plugin(config, options, plugin)    
        (config, p_commands, options) = res
        
        plugin_commands.update(p_commands)   # add the plugin commands
        #config['plugins'][plugin] = p_config # add the plugin config
        
    return (config, plugin_commands, options)
