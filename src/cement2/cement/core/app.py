"""Primary application classes."""

import sys

from cement.handlers.log import CementLogHandler
from cement.core.handler import define_handler, register_handler

def lay_cement(config, **kw):
    """
    Initialize the framework.
    
    Optional Keyword Arguments:
    
        argv
            List of args to use.  Default: sys.argv.
        
    """
        
    argv = kw.get('argv', sys.argv)
    
    # basic logging setup first (mostly for debug/error)
    if '--debug' in argv:
        config['log_level'] = 'DEBUG'

    cement_log = CementLogHandler('cement')
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
    register_handler('log', 'logging', CementLogHandler)
        
class CementApp(object):
    def __init__(self, config):
        self.config = config
        self._validate_required_config()
        lay_cement(config)
        
        self._validate_config()
        
        # setup logging for the app
        self.log = CementLogHandler(self.config['app_module'])
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