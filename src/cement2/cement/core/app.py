"""Primary application classes."""

import sys

from cement.core.backend import get_defaults
from cement.core.exc import CementConfigError
from cement.core.handler import define_handler, register_handler, get_handler
from cement.handlers.log import CementLogHandler, LoggingLogHandler
from cement.handlers.config import IConfigHandler, ConfigParserConfigHandler
from cement.handlers.config import ConfigObjConfigHandler

def lay_cement(app_name, *args, **kw):
    """
    Initialize the framework.

    Required Arguments:
    
        app_name
            The name of the application.
            
        
    Optional Keyword Arguments:

        defaults
            The default config dictionary (other wise use get_defaults)
            
        argv
            List of args to use.  Default: sys.argv.
    
    """
    
    defaults = kw.get('defaults', get_defaults())
    argv = kw.get('argv', sys.argv)
    
    # basic logging setup first (mostly for debug/error)
    if '--debug' in argv:
        defaults['base']['log_level'] = 'DEBUG'
    
    cement_log = LoggingLogHandler('cement')
    cement_log.setup_logging(
        level=defaults['base']['log_level'],
        to_console=defaults['base']['log_to_console'],
        clear_loggers=defaults['base']['log_clear_loggers'],
        log_file=defaults['base']['log_file'],
        max_bytes=defaults['base']['log_max_bytes'],
        max_files=defaults['base']['log_max_files'],
        file_formatter=defaults['base']['log_file_formatter'],
        console_formatter=defaults['base']['log_console_formatter'],
        )

    define_handler('log', CementLogHandler)
    define_handler('config', IConfigHandler)
    #define_handler('output')
    #define_handler('option')
    #define_handler('command')
    #define_handler('hook')
    #define_handler('plugin')
    #define_handler('error')
    
    #register_handler(LoggingLogHandler)
    register_handler(ConfigParserConfigHandler)
    #register_handler(ConfigObjConfigHandler)
    
    app = CementApp(app_name, *args, **kw)
    return app
    
class CementApp(object):
    def __init__(self, app_name, **kw):
        self.defaults = kw.get('defaults', get_defaults())
        if not self.defaults['base']['app_name']:
            self.defaults['base']['app_name'] = app_name

        # initialize handlers if passed in
        self.config = kw.get('config', None)
        self.log = kw.get('log', None)
        self.options = None
        self.commands = None
        
    def run(self):
        self._setup_config()
        self._validate_required_config()
        self._validate_config()
        #self._setup_logging()

    def _setup_config(self):
        if not self.config:
            h = get_handler('config', self.defaults['base']['config_handler'])
            self.config = h()
        
        self.config.merge(self.defaults)
        for _file in self.config.get('base', 'config_files'):
            self.config.parse_file(_file)
        
    def _setup_logging(self):
        # first redo logging for cement (in case the log_handler is diff)
        handler = get_handler('log', self.config.get('base', 'log_handler'))
        cement_log = handler('cement')
        cement_log.setup_logging(
            level=self.config.get('base', 'log_level'),
            to_console=self.config.get('base', 'log_to_console'),
            clear_loggers=self.config.get('base', 'log_clear_loggers'),
            log_file=self.config.get('base', 'log_file'),
            max_bytes=self.config.get('base', 'log_max_bytes'),
            max_files=self.config.get('base', 'log_max_files'),
            file_formatter=self.config.get('base', 'log_file_formatter'),
            console_formatter=self.config.get('base', 'log_console_formatter'),
            )
        
        # then setup logging for the app    
        handler = get_handler('log', self.config.get('base', 'log_handler'))
        self.log = handler(self.config.get('base', 'app_module'))
        self.log.setup_logging(
            level=self.config.get('base', 'log_level'),
            to_console=self.config.get('base', 'log_to_console'),
            clear_loggers=self.config.get('base', 'log_clear_loggers'),
            log_file=self.config.get('base', 'log_file'),
            max_bytes=self.config.get('base', 'log_max_bytes'),
            max_files=self.config.get('base', 'log_max_files'),
            file_formatter=self.config.get('base', 'log_file_formatter'),
            console_formatter=self.config.get('base', 'log_console_formatter'),
            )
        
    def _validate_required_config(self):
        """
        Validate base config settings required by cement.
        """
        # need to shorten this a bit
        c = self.config

        if not c.has_key('base', 'app_name') or \
           not c.get('base', 'app_name'):
            raise CementConfigError("config['app_name'] required.")
        if not c.has_key('base', 'app_module') or \
           not c.get('base', 'app_module'):
            c.set('base', 'app_module', c.get('base', 'app_name'))
        if not c.has_key('base', 'app_egg') or \
           not c.get('base', 'app_egg'):
            c.set('base', 'app_egg', c.get('base', 'app_name'))
        
        self.config = c
        
    def _validate_config(self):
        """
        Validate application config settings.
        """
        pass
        