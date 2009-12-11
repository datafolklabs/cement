"""Cement methods for handling config file parsing."""
import os
from configobj import ConfigObj

from cement.core.exc import CementConfigError

def get_default_config():
    dcf = {}
    dcf['config_source'] = ['defaults']
    dcf['enabled_plugins'] = []
    dcf['debug'] = False
    dcf['show_plugin_load'] = True
    return dcf
# global config dictionary
config = get_default_config()

# global hooks dictionary
hooks = {}

# commands dictionary
commands = {'global' : {}}

# OptParse options object *we set this up later
options = None

def set_config_opts_per_file(tmpconfig, section, config_file):
    """
    Parse config file options for into config dict.  Will do nothing if the 
    config file does not exist.
    
    Arguments:
    
    config => dict containing configurations.
    section => section of the configuration file to read.
    config_file => The config file to parse.
    """
    if not tmpconfig.has_key('config_source'):
        tmpconfig['config_source'] = []
        
    if os.path.exists(config_file):
        tmpconfig['config_source'].append(config_file)
        tmpconfig['config_file'] = config_file
        cnf = ConfigObj(config_file)
        try:
            tmpconfig.update(cnf[section])
        except KeyError:
            raise CementConfigError, \
                'missing section %s in %s.' % (section, config_file)

        for option in cnf[section]:
            if cnf[section][option] in ['True', 'true', True, 'yes', 
                                        'Yes', '1']:
                tmpconfig[option] = True
            elif cnf[section][option] in ['False', 'false', False, 'no', 
                                          'No', '0']:
                tmpconfig[option] = False
    return tmpconfig


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