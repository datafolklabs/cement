"""Cement methods for handling config file parsing."""
import os
from configobj import ConfigObj

from cement.core.options import init_parser
from cement.core.exc import CementConfigError

class CementNamespace(object):
    def __init__(self, label, version, required_abi, **kw):
        self.label = label
        self.version = version
        self.required_abi = required_abi
        self.description = kw.get('description', '')
        self.commands = kw.get('commands', {})
        self.config = kw.get('config', {'config_source': ['defaults']})
        
        if not kw.get('version_banner'):
            vb = "%s version %s" % (self.label, self.version)
        else:
            vb = kw.get('version_banner')
        self.options = kw.get('options', init_parser(version_banner=vb))
            
def define_namespace(namespace, namespace_obj):
    """
    Define a namespace for commands, options, configuration, etc.  
    
    Arguments:
    
    namespace => label of the namespace
    namespace_obj => CementNamespace object
    """
    if namespaces.has_key(namespace):
        raise CementRuntimeError, "Namespace '%s' already defined!" % namespace
    namespaces[namespace] = namespace_obj
    
def get_default_config():
    dcf = {}
    dcf['config_source'] = ['defaults']
    dcf['enabled_plugins'] = []
    dcf['debug'] = False
    dcf['show_plugin_load'] = True
    dcf['merge_global_options'] = False
    return dcf

# global hooks dictionary
hooks = {}

# setup namespace dict
namespaces = {}

def set_config_opts_per_file(namespace, section, config_file):
    """
    Parse config file options for into config dict.  Will do nothing if the 
    config file does not exist.
    
    Arguments:
    
    config => dict containing configurations.
    section => section of the configuration file to read.
    config_file => The config file to parse.
    """
    
    if not namespaces[namespace].config.has_key('config_source'):
        namespaces[namespace].config['config_source'] = []
        
    if os.path.exists(config_file):
        namespaces[namespace].config['config_source'].append(config_file)
        namespaces[namespace].config['config_file'] = config_file
        cnf = ConfigObj(config_file)
        try:
            namespaces[namespace].config.update(cnf[section])
        except KeyError:
            raise CementConfigError, \
                'missing section %s in %s.' % (section, config_file)

        for option in cnf[section]:
            if cnf[section][option] in ['True', 'true', True, 'yes', 
                                        'Yes', '1']:
                namespaces[namespace].config[option] = True
            elif cnf[section][option] in ['False', 'false', False, 'no', 
                                          'No', '0']:
                namespaces[namespace].config[option] = False


def set_config_opts_per_cli_opts(namespace, cli_opts):
    """
    Determine if any config optons were passed via cli options, and if so
    override the config option.
    
    Returns the updated config dict.
    """
    for opt in namespaces[namespace].config:
        try:
            val = getattr(cli_opts, opt)
            if val:
                namespaces[namespace].config[opt] = val
        except AttributeError:
            pass
            
def validate_config(config):
    """
    Validate that all required cement configuration options are set.
    """
    required_settings = [
        'config_source', 'config_files', 'debug', 'datadir',
        'enabled_plugins', 'plugin_config_dir', 'plugin_dir', 
        'plugins', 'app_module', 'app_name', 'tmpdir', 'merge_global_options'
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