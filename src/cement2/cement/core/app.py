"""Primary application classes."""

import sys

from cement.core.backend import init_config
from cement.core.exc import CementConfigError
from cement.core.handler import define_handler, register_handler, get_handler
from cement.handlers.log import LoggingLogHandler
from cement.handlers.config import ConfigParserConfigHandler

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
    define_handler('config')
    define_handler('output')
    define_handler('option')
    define_handler('command')
    define_handler('hook')
    define_handler('plugin')
    define_handler('error')
    
    register_handler('log', 'logging', LoggingLogHandler)
    register_handler('config', 'configparser', ConfigParserConfigHandler)
    
class CementApp(object):
    def __init__(self, app_name, **kw):
        self.default_config = kw.get('default_config', init_config())
        self.default_config['app_name'] = app_name
        
        self.config = None
        self.log = None
        self.options = None
        self.commands = None
        
    def run(self):
        self._validate_required_config()
        self._setup_cement()
        self._setup_config()
        self._setup_logging()

    def _setup_cement(self):
        lay_cement(self.config)    
        
    def _setup_config(self):
        handler = get_handler('config', config['config_handler'])
        self.config = handler(self.default_config)
        
    def _setup_logging(self):
        # first redo logging for cement (in case the log_handler is diff)
        handler = get_handler('log', self.config['log_handler'])
        cement_log = handler('cement')
        cement_log.setup_logging(
            level=self.config['log_level'],
            to_console=self.config['log_to_console'],
            clear_loggers=self.config['log_clear_previous_loggers'],
            log_file=self.config['log_file'],
            max_bytes=self.config['log_max_bytes'],
            max_files=self.config['log_max_files'],
            file_formatter=self.config['log_file_formatter'],
            console_formatter=self.config['log_console_formatter'],
            )
        
        # then setup logging for the app    
        handler = get_handler('log', self.config['log_handler'])
        self.log = handler(self.config['app_module'])
        self.log.setup_logging(
            level=self.config['log_level'],
            to_console=self.config['log_to_console'],
            clear_loggers=self.config['log_clear_previous_loggers'],
            log_file=self.config['log_file'],
            max_bytes=self.config['log_max_bytes'],
            max_files=self.config['log_max_files'],
            file_formatter=self.config['log_file_formatter'],
            console_formatter=self.config['log_console_formatter'],
            )
        
    def _validate_required_config(self):
        # need to shorten this a bit
        c = self.config
        
        if not c.has_key('app_name') or not c['app_name']:
            raise CementConfigError("config['app_name'] required.")
        if not c.has_key('app_module') or not c['app_module']:
            c['app_module'] = c['app_name']
        if not c.has_key('app_egg') or not c['app_egg']:
            c['app_egg'] = c['app_name']
        
        self.config = c
        