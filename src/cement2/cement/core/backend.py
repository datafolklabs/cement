
import sys

# global config dictionary
config = {}
config['app_name'] = None
config['app_module'] = None
config['app_egg'] = None
config['config_files'] = []
config['config_source'] = ['default']
config['debug'] = False
config['log_file'] = None
config['log_level'] = 'INFO'
config['log_to_console'] = True
config['log_max_bytes'] = None
config['log_max_files'] = 4
config['log_file_formatter'] = None
config['log_console_formatter'] = None
config['log_clear_previous_loggers'] = True
# default handlers
config['log_handler'] = 'default'
config['config_handler'] = 'default'
config['option_handler'] = 'default'
config['command_handler'] = 'default'
config['hook_handler'] = 'default'
config['plugin_handler'] = 'default'
config['error_handler'] = 'default'


def init_config():
    _config = config.copy()
    return _config
    
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