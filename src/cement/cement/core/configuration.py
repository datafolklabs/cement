"""Cement methods for handling config file parsing."""

import os
import sys
from configobj import ConfigObj, Section

from cement.core.exc import CementConfigError

SAVED_STDOUT = sys.stdout
SAVED_STDERR = sys.stderr

class StdOutBuffer(object):
    buffer = ''
    def write(self, text):
        self.buffer += text
        
class StdErrBuffer(object):
    buffer = ''
    def write(self, text):
        self.buffer += text

# These will only be used if --quiet or --json are passed
buf_stdout = StdOutBuffer()
buf_stderr = StdErrBuffer()

def get_default_config():
    """Get a default config dict."""
    dcf = ConfigObj()
    dcf['config_source'] = ['defaults']
    dcf['config_files'] = []
    dcf['enabled_plugins'] = []
    dcf['debug'] = False
    dcf['show_plugin_load'] = True
    dcf['output_engine'] = 'genshi' # deprecated
    dcf['output_handler'] = 'genshi'
    dcf['output_handler_override'] = None
    dcf['logging_config_file'] = None
    return dcf

def get_default_namespace_config():
    """Get a default plugin config dict."""
    dcf = ConfigObj()
    dcf['config_source'] = ['defaults']
    dcf['merge_root_options'] = True
    return dcf

# global hooks dictionary
hooks = {}

# global namespace dict
namespaces = {}

# global handlers dict
handlers = {}
        
def get_api_version():
    """Get the Cement API Version."""
    #return CEMENT_API
    print "The use of CEMENT_API is deprecated as of 0.8.9."
    return None
    
def ensure_api_compat(module_name, required_api):
    """
    Ensure the application is compatible with this version of Cement.
    
    Required Arguments:
    
        module_name
            Name of the applications module.
            
        required_api
            The Cement API version required by the application.
        
    """
    print "WARNING: The use of CEMENT_API is deprecated as of 0.8.9.  Called from %s" % module_name
    return True
         
def t_f_pass(value):
    """
    A quick hack for making true/false type values actually True/False in
    python.
    
    Required arguments:
    
        value
            The presumed 'true' or 'false' value.
    
    
    Returns:
    
        boolean
            True/False based on logic of the operation.
    
    """
    try:
        if str(value.lower()) in ['true', True]:
            return True
        if str(value.lower()) in ['false', False]:
            return False
        else:
            return value
    except:
        return value
        
        
def set_config_opts_per_file(namespace, section, config_file):
    """
    Parse config file options for into config dict.  Will do nothing if the 
    config file does not exist.
    
    Required arguments:
    
        namespace
            The namespace to set config options for
            
        section
            Section of the configuration file to read.
            
        config_file
            The config file to parse.
    
    """
    config = namespaces[namespace].config

    if not config.has_key('config_source'):
        config['config_source'] = []
        
    if os.path.exists(config_file):
        try:
            cnf = ConfigObj(config_file)
            config.update(cnf[section])
            config['config_source'].append(config_file)
        except IOError, error:
            # the file is not readable, so remove it from config_files
            if config_file in config['config_files']:
                config['config_files'].remove(config_file)
                namespaces[namespace].config = config
            return 
        except KeyError, error:
            # FIX ME: can't log here...  
            # log.debug('missing section %s in %s.' % (section, config_file))
            return
        
        
        # FIX ME: Is there an easier way to ensure true/false values are
        # actually True/False.  I think ConfigSpec, but don't have time right
        # now.
        #
        # But since we are parsing config before our plugins load then how
        # do you have a config spec for the app and plugin?  UPDATE: i think
        # with the new bootstrap layout a spec could be possible.
        #
        # Regardless... the point of this nonsense below is to ensure
        # true false values equate to True/False in python.  We go 3 levels
        # deep into:
        #
        # [section]
        # [[section2]]
        # [[section3]]
        #
        sec1 = cnf[section]
        for opt1 in sec1:
            if not type(sec1[opt1]) == Section:
                config[opt1] = t_f_pass(sec1[opt1])
                try:
                    if sec1[opt1].startswith('~'):
                        config[opt1] = os.path.expanduser(sec1[opt1])
                except AttributeError:
                    pass
            else:
                # This is another level of the same loop.  If the option is
                # actually a configobj.Section, we need to run the loop on 
                # that section.
                sec2 = sec1[opt1]
                for opt2 in sec2:
                    if not type(sec2[opt2]) == Section:
                        config[opt1][opt2] = t_f_pass(sec2[opt2])                   
                        if opt2.startswith('~'):
                            config[opt1][opt2] = os.path.expanduser(sec2[opt2])
                    else:
                        # This is yet another level of the same loop.  Only
                        # willing to go 3 levels deep though.
                        sec3 = sec2[opt2]
                        for opt3 in sec3:
                            if not type(sec3[opt3]) == Section:
                                config[opt1][opt2][opt3] = t_f_pass(sec3[opt3])
                                if opt3.startswith('~'):
                                    config[opt1][opt2][opt3] = os.path.expanduser(sec3[opt3])
                        
        # overwrite the namespace config
        namespaces[namespace].config = config
                                
def set_config_opts_per_cli_opts(namespace, cli_opts):
    """
    Determine if any config optons were passed via cli options, and if so
    override the config option.  Overwrites the global 
    namespaces['namespace'].config dict.
    
    Required arguments:
    
        namespace
            The namespace of whose config to modify.

        cli_opts
            The cli_opts as parsed from OptParse.
    
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
    Validate that all required cement configuration options are set.  Also
    creates any common directories based on config settings if they do not 
    exist.
    
    Required arguments:
    
        config
            The config dict to validate.
    
    
    Possible Exceptions:
    
        CementConfigError
            Raised on invalid configuration.
    
    """
    required_settings = [
        'config_source', 'config_files', 'debug', 'datadir',
        'enabled_plugins', 'plugin_config_dir', 'app_module', 'app_name', 
        'tmpdir', 'output_handler'
        ]
    for s in required_settings:
        if not config.has_key(s):
            raise CementConfigError, "config['%s'] value missing!" % s
    
    # create all directories if missing
    for d in [os.path.dirname(config['log_file']), config['datadir'], 
              config['plugin_config_dir'], config['tmpdir']]:
        if not os.path.exists(d):
            os.makedirs(d)
