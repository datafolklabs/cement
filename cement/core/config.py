"""Cement methods for handling config file parsing."""
import os
from configobj import ConfigObj

from cement.core.exc import CementConfigError

def set_config_opts_per_file(config, section, config_file):
    """
    Parse config file options for into config dict.  Will do nothing if the 
    config file does not exist.
    
    Arguments:
    
    config => dict containing application configurations.
    section => section of the configuration file to read.
    config_file => The config file to parse.
    """
    if not config.has_key('config_source'):
        config['config_source'] = []
        
    if os.path.exists(config_file):
        config['config_source'].append(config_file)
        config['config_file'] = config_file
        cnf = ConfigObj(config_file)
        try:
            config.update(cnf[section])
        except KeyError:
            raise CementConfigError, \
                'missing section %s in %s.' % (section, config_file)

        for option in cnf[section]:
            if cnf[section][option] in ['True', 'true', True, 'yes', 
                                        'Yes', '1']:
                config[option] = True
            elif cnf[section][option] in ['False', 'false', False, 'no', 
                                          'No', '0']:
                config[option] = False

    return config