
import sys

def get_defaults():
    # default backend configuration
    dcf = {}
    dcf['base'] = {}
    dcf['base']['app_name'] = None
    dcf['base']['app_module'] = None
    dcf['base']['app_egg'] = None
    dcf['base']['config_files'] = []
    dcf['base']['config_source'] = ['default']

    # default handlers
    dcf['base']['log_handler'] = 'default'
    dcf['base']['config_handler'] = 'configparser'
    dcf['base']['option_handler'] = 'default'
    dcf['base']['command_handler'] = 'default'
    dcf['base']['hook_handler'] = 'default'
    dcf['base']['plugin_handler'] = 'default'
    dcf['base']['error_handler'] = 'default'

    # default application configuration
    dcf['base']['debug'] = False
    dcf['base']['log_file'] = None
    dcf['base']['log_level'] = 'INFO'
    dcf['base']['log_to_console'] = True
    dcf['base']['log_max_bytes'] = None
    dcf['base']['log_max_files'] = 4
    dcf['base']['log_file_formatter'] = None
    dcf['base']['log_console_formatter'] = None
    dcf['base']['log_clear_loggers'] = True
    return dcf
    
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