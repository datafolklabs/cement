"""Cement methods for handling config file parsing."""
import os
from configobj import ConfigObj, Section

from cement.core.exc import CementConfigError

CEMENT_API = "20091211"
    
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

        
def get_api_version():
    return CEMENT_API
    
def ensure_api_compat(module_name, required_api):
    if int(required_api) == int(CEMENT_API):
        pass
    else:
        raise CementRuntimeError, \
            "%s requires api version %s which differs from cement(api) %s." % \
                (module_name, required_api, CEMENT_API)
                
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

        # FIX ME: Is there an easier way to ensure true/false values are
        # actually True/False.  I think ConfigSpec, but don't have time right
        # now.
        for option in cnf[section]:
            if cnf[section][option] in \
                ['True', 'true', True, 'yes', 'Yes', '1']:
                namespaces[namespace].config[option] = True
                
            elif cnf[section][option] in \
                ['False', 'false', False, 'no', 'No', '0']:
                namespaces[namespace].config[option] = False
            
            elif type(cnf[section][option]) == Section:
                # this is another level of the same loop.  If the option is
                # actually a configobj.Section, we need to run the loop on 
                # that section.
                for sub_option in cnf[section][option]:
                    if cnf[section][option][sub_option] in \
                        ['True', 'true', True, 'yes', 'Yes', '1']:
                        namespaces[namespace].config[option][sub_option] = True
                
                    elif cnf[section][option][sub_option] in \
                        ['False', 'false', False, 'no', 'No', '0']:
                        namespaces[namespace].config[option][sub_option] = False
                    
                    elif type(cnf[section][option]) == Section:
                        # This is yet another level of the same loop.  Only
                        # willing to go 3 levels deep though.
                        for sub_sub_option in cnf[section][option][sub_option]:
                            if cnf[section][option][sub_option][sub_sub_option] in \
                                ['True', 'true', True, 'yes', 'Yes', '1']:
                                namespaces[namespace].config[option][sub_option][sub_sub_option] = True
                
                            elif cnf[section][option][sub_option][sub_sub_option] in \
                                ['False', 'false', False, 'no', 'No', '0']:
                                namespaces[namespace].config[option][sub_option][sub_sub_option] = False
                                
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
