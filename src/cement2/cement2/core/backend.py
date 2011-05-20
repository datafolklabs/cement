"""Cement core backend module."""

import sys
import logging

def default_config(app_name):
    """
    Get a standard, default config for app_name.
    
    Required Arguments:
    
        app_name
            The name of the application.
            
    """
    # default backend configuration
    dcf = {}
    dcf['base'] = {}
    dcf['base']['app_name'] = app_name
    dcf['base']['app_module'] = app_name
    dcf['base']['app_egg'] = app_name
    dcf['base']['config_files'] = []
    dcf['base']['config_source'] = ['default']
    dcf['base']['debug'] = False
    dcf['base']['extensions'] = []
    dcf['base']['plugins'] = []
    dcf['base']['plugin_config_dir'] = None
    dcf['base']['plugin_dir'] = '/usr/lib/%s/plugins' % app_name
    
    # default handlers
    dcf['base']['config_handler'] = 'configparser'
    dcf['base']['log_handler'] = 'logging'
    dcf['base']['plugin_handler'] = 'cement'
    dcf['base']['extension_handler'] = 'cement'
    dcf['base']['output_handler'] = 'cement'
    dcf['base']['option_handler'] = 'default'
    dcf['base']['command_handler'] = 'default'
    dcf['base']['hook_handler'] = 'default'
    dcf['base']['error_handler'] = 'default'

    # default application configuration
    dcf['log'] = {}
    dcf['log']['file'] = None
    dcf['log']['level'] = 'INFO'
    dcf['log']['to_console'] = True
    dcf['log']['max_bytes'] = None
    dcf['log']['max_files'] = 4
    dcf['log']['file_formatter'] = None
    dcf['log']['console_formatter'] = None
    dcf['log']['clear_loggers'] = True
    return dcf
    
def minimal_logger(name, debug=False):
    """
    Setup just enough for cement to be able to do debug logging.
    """
                
    log = logging.getLogger(name)
    formatter = logging.Formatter(
                "%(asctime)s (%(levelname)s) %(name)s : %(message)s")
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.INFO)   
    log.setLevel(logging.INFO)
        
    # FIX ME: really don't want to hard check sys.argv like this but can't
    # figure any better way get logging started (only for debug) before the
    # app logging is setup.
    if '--debug' in sys.argv or debug:
        console.setLevel(logging.DEBUG)   
        log.setLevel(logging.DEBUG)
        
    log.addHandler(console)
    return log
    
# global handlers dict
handlers = {}

# global hooks dict
hooks = {}

# Save original stdout/stderr for supressing output
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

buf_stdout = StdOutBuffer()
buf_stderr = StdErrBuffer()