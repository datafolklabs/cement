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