"""Cement methods to setup the framework for applications using it."""
import os
from pkg_resources import get_distribution

from cement import plugins as cement_plugins
from cement.core.log import setup_logging
from cement.core.options import init_parser, parse_options
from cement.core.config import set_config_opts_per_file
from cement.core.options import set_config_opts_per_cli_opts
from cement.core.exc import CementConfigError, CementRuntimeError

CEMENT_ABI = "20091207"

class CementCommand(object):
    def __init__(self, config, cli_opts=None, cli_args=None, handlers=None):
        self.config = config
        self.cli_opts = cli_opts
        self.cli_args = cli_args
        self.handlers = handlers
    
    def help(self):
        """Display command help information."""
        print "No help information available."
    
    def run(self):
        """Run the command actions."""
        print "No actions have been defined for this command."
        

class CementPlugin(object):
    def __init__(self, config):
        self.version = None
        self.description = ""
        self.commands = {}
        self.handlers = {}
        self.config = {'config_source': ['defaults']}
        self.options = init_parser(config)
        

def get_abi_version():
    return CEMENT_ABI
    
    
def lay_cement(config, version_banner=None):
    """
    Primary method to setup an application for Cement.  
    
    Arguments:
    
    config => dict containing application config.
    version_banner => Option txt displayed for --version
    """
    dcf = {} # default config
    dcf['config_source'] = ['defaults']
    dcf['enabled_plugins'] = [] # no default plugins, add via the config file
    dcf['debug'] = False
    dcf['show_plugin_load'] = True

    dcf.update(config) # override the actual defaults
    config = dcf # take the new config with changes
    validate_config(config)
    
    if not version_banner:
        version_banner = get_distribution(config['app_egg_name']).version
        
    for cf in config['config_files']:
        config = set_config_opts_per_file(config, config['app_module'], cf)
        
    options = init_parser(config, version_banner)
    (config, commands, handlers, options) = load_all_plugins(config, options)
    (config, cli_opts, cli_args) = parse_options(config, options, commands)
    config = set_config_opts_per_cli_opts(config, cli_opts)
    setup_logging(config)
    return (config, cli_opts, cli_args, commands, handlers)


def ensure_abi_compat(module_name, required_abi):
    if int(required_abi) != int(CEMENT_ABI):
        raise CementRuntimeError, \
            "%s requires abi version %s which differs from cement(abi) %s." % \
                (module_name, required_abi, CEMENT_ABI)


def validate_config(config):
    """
    Validate that all required cement configuration options are set.
    """
    required_settings = [
        'config_source', 'config_files', 'debug', 'datadir',
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
            
            
def load_plugin(config, plugin):
    """
    Load a cement type plugin.  
    
    Arguments:
    
    config  => The existing config dict.
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
    except AttributeError, e:
        # we allow all apps to use cement plugins like their own.        
        try:
            plugins_module = __import__('cement.plugins', globals(), locals(),
                                        [plugin], 0)
            pluginobj = getattr(plugins_module, plugin)
        except AttributeError, e:
            raise CementConfigError, \
                'failed to load %s plugin: %s' % (plugin, e)    
    
    plugin_cls = pluginobj.register_plugin(config)
    
    ensure_abi_compat(plugin_cls.__module__, plugin_cls.required_abi)

    plugin_config_file = os.path.join(
        config['plugin_config_dir'], '%s.plugin' % plugin
        )
    plugin_cls.config = set_config_opts_per_file(plugin_cls.config, plugin, 
                                                 plugin_config_file)
    return plugin_cls
        
        
def load_all_plugins(config, options):
    """
    Attempt to load all enabled plugins.  Passes the existing config and 
    options object to each plugin and allows them to add/update each.
    """
    plugin_commands = {}
    plugin_handlers = {}
    for plugin in config['enabled_plugins']:
        plugin_cls = load_plugin(config, plugin)

        # add the plugin commands
        for key in plugin_cls.commands:
            if plugin_commands.has_key(key):
                raise CementRuntimeError, \
                    'Command conflict, %s command already exists!' % key
            plugin_commands[key] = plugin_cls.commands[key]

        # add the plugin handlers
        for key in plugin_cls.handlers:
            if plugin_handlers.has_key(key):
                raise CementRuntimeError, \
                    'Handler conflict, %s handler already exists!' % key
            plugin_handlers[key] = plugin_cls.handlers[key]

        # add the plugin 
        config['plugins'][plugin] = plugin_cls
        
        # add the plugin options
        for opt in plugin_cls.options.parser._get_all_options():
            if opt.get_opt_string() == '--help':
                pass
            else:
                options.parser.add_option(opt)
        
    return (config, plugin_commands, plugin_handlers, options)

    