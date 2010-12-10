"""Primary application classes."""

import sys

from cement.core.handler import define_handler, register_handler, get_handler
from cement.handlers.log import LoggingLogHandler

def lay_cement(config, **kw):
    """
    Initialize the framework.

    Required Arguments:
    
        config
            A config dictionary to work from.
        
    Optional Keyword Arguments:

        argv
            List of args to use.  Default: sys.argv.
    
    """
    
    argv = kw.get('argv', sys.argv)

    # basic logging setup first (mostly for debug/error)
    if '--debug' in argv:
        config['log_level'] = 'DEBUG'

    cement_log = LoggingLogHandler('cement')
    cement_log.setup_logging(
        level=config['log_level'],
        to_console=config['log_to_console'],
        clear_loggers=True,
        log_file=config['log_file'],
        max_bytes=config['log_max_bytes'],
        max_files=config['log_max_files'],
        file_formatter=config['log_file_formatter'],
        console_formatter=config['log_console_formatter'],
        )

    define_handler('log')
    define_handler('output')
    define_handler('option')
    define_handler('command')
    define_handler('hook')
    define_handler('plugin')
    
    register_handler('log', 'logging', LoggingLogHandler)

        
class CementApp(object):
    def __init__(self, config):
        self.config = config
        self._validate_required_config()
        lay_cement(config)
        
        self._validate_config()
        self._setup_logging()
    
    def _setup_logging(self):
        lh = get_handler('log', self.config['log_handler'])
        self.log = lh(self.config['app_module'])
        self.log.setup_logging(
            level=self.config['log_level'],
            to_console=self.config['log_to_console'],
            clear_loggers=True,
            log_file=self.config['log_file'],
            max_bytes=self.config['log_max_bytes'],
            max_files=self.config['log_max_files'],
            file_formatter=self.config['log_file_formatter'],
            console_formatter=self.config['log_console_formatter'],
            )
        
    def _validate_required_config(self):
        if not self.config.has_key('app_module') or \
           not self.config['app_module']:
            self.config['app_module'] = self.config['app_name']
            
        if not self.config.has_key('app_egg') or \
           not self.config['app_egg']:
            self.config['app_egg'] = self.config['app_name']

    def _validate_config(self):
        pass   