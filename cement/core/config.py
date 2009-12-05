
import os
from configobj import ConfigObj

from cement.core.exc import CementConfigError

def set_config_opts_per_file(config_opts, section, file):
    """
    Parse config file options for config optios.  Will do nothing if the 
    config file does not exist.
    """
    if not config_opts.has_key('config_source'):
        config_opts['config_source'] = []
        
    if os.path.exists(file):
        config_opts['config_source'].append(file)
        config_opts['config_file'] = file
        config = ConfigObj(file)
        try:
            config_opts.update(config[section])
        except KeyError, e:
            raise CementConfigError, \
                'missing section %s in %s.' % (section, file)

        for option in config[section]:
            if config[section][option] in ['True', 'true', True, 'yes', 'Yes', '1']:
                config_opts[option] = True
            elif config[section][option] in ['False', 'false', False, 'no', 'No', '0']:
                config_opts[option] = False

    return config_opts