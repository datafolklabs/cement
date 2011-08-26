"""
.. _logging-extension:

Logging Framework Extension
---------------------------

"""

import logging
from cement2.core import exc, util, handler, log
        
class LoggingLogHandler(object):  
    class meta:
        interface = log.ILog
        label = 'logging'
        
        # These are the default config values, overridden by any '[log]' 
        # section in parsed config files.
        defaults = dict(
            file=None,
            level='INFO',
            to_console=True,
            rotate=False,
            max_bytes=512000,
            max_files=4,
            clear_loggers=True,
            )
    
    levels = ['INFO', 'WARN', 'ERROR', 'DEBUG', 'FATAL']

    def __init__(self, **kw):
        """
        This is an implementation of the ILogHandler interface, and sets up 
        the logging facility using the standard 'logging' module.

        Optional Arguments:
        
            config
                The application configuration object.
                
            namespace
                The logging namespace.  Default: application name.
                
            backend
                The logging backend.  Default: logging.getLogger().
            
            file
                The log file path. Default: None.
                
            to_console
                Whether to log to the console.  Default: True.
            
            rotate
                Whether to rotate the log file.  Default: False.
            
            max_bytes
                The number of bytes at which to rotate the log file.
                Default: 512000.
            
            max_files
                The max number of files to keep when rotation the log file.
                Default: 4
                
            file_formatter
                The logging formatter to use for the log file.
                
            console_formatter
                The logging formatter to use for the console output.
                
            debug_formatter
                The logging formatter to use for debug output.
                
            clear_loggers
                Whether or not to clear previous loggers first.  
                Default: False.
               
            level
                The level to log at.  Must be one of ['INFO', 'WARN', 'ERROR', 
                'DEBUG', 'FATAL'].  Default: INFO.
        
        
        Configuration Options
        
        The following configuration options are recognized in this class:
        
            base.app_name
            base.debug
            log.file
            log.to_console
            log.rotate
            log.max_bytes
            log.max_files
            log.clear_loggers
        
        A sample config section (in any config file) might look like:
        
        .. code-block::text
        
            [log]
            file = /path/to/config/file
            level = info
            to_console = true
            rotate = true
            max_bytes = 512000
            max_files = 4
            
        """  
        self.config = kw.get('config', None)
        self.namespace = kw.get('namespace', None)
        self.backend = kw.get('backend', None)
        self.file = kw.get('file', None)
        self.to_console = kw.get('to_console', None)
        self.rotate = kw.get('rotate', None)
        self.max_bytes = kw.get('max_bytes', None)
        self.max_files = kw.get('max_files', None)
        self.file_formatter = kw.get('file_formatter', None)
        self.console_formatter = kw.get('console_formatter', None)
        self.debug_formatter = kw.get('debug_formatter', None)
        self._clear_loggers = kw.get('clear_loggers', None)
        self._level = kw.get('level', None)
        
    def setup(self, config_obj):
        self.config = config_obj
        
        # first handle anything passed to __init__, fall back on config.
        if self.namespace is None:
            self.namespace = self.config.get('base', 'app_name')
        if self.backend is None:
            self.backend = logging.getLogger(self.namespace)
        if self.file is None:
            self.file = self.config.get('log', 'file')
        if self.to_console is None:
            self.to_console = self.config.get('log', 'to_console')
        if self.rotate is None:
            self.rotate = self.config.get('log', 'rotate')
        if self.max_bytes is None:
            self.max_bytes = self.config.get('log', 'max_bytes')
        if self.max_files is None:
            self.max_files = self.config.get('log', 'max_files')
        if self.file_formatter is None:
            format_str = "%(asctime)s (%(levelname)s) %(name)s : %(message)s"
            self.file_formatter = logging.Formatter(format_str)
        if self.console_formatter is None:
            format_str = "%(levelname)s: %(message)s"
            self.console_formatter = logging.Formatter(format_str)
        if self.debug_formatter is None:
            format_str = "%(asctime)s (%(levelname)s) %(name)s : %(message)s"
            self.debug_formatter = logging.Formatter(format_str)
        if self._clear_loggers is None:
            self._clear_loggers = self.config.get('log', 'clear_loggers')
        if self._level is None:
            self._level = self.config.get('log', 'level').upper()
            if self._level not in self.levels:
                self._level = 'INFO'

        # the king trumps all
        if util.is_true(self.config.get('base', 'debug')):
            self._level = 'DEBUG'
            
        self.set_level(self._level)
        
        # clear loggers?
        if util.is_true(self._clear_loggers):
            self.clear_loggers()
            
        # console
        if util.is_true(self.to_console):
            self._setup_console_log()
        
        # file
        if self.file:
            self._setup_file_log()
            
        self.debug("logging initialized for '%s' using LoggingLogHandler" % \
                   self.namespace)
                 
    def set_level(self, level):
        if level not in self.levels:
            level = 'INFO'
        level = getattr(logging, level.upper())
        
        self.backend.setLevel(level)  
        
        for handler in logging.getLogger(self.namespace).handlers:
            handler.setLevel(level)
            
    def clear_loggers(self):
        if not self.namespace:
            # setup() probably wasn't run
            return
            
        for i in logging.getLogger(self.namespace).handlers:
            logging.getLogger(self.namespace).removeHandler(i)
            self.backend = logging.getLogger(self.namespace)
    
    def _setup_console_log(self):
        console_handler = logging.StreamHandler()
        if self.level() == logging.getLevelName(logging.DEBUG):
            console_handler.setFormatter(self.debug_formatter)
        else:
            console_handler.setFormatter(self.console_formatter)
            
        console_handler.setLevel(getattr(logging, self.level()))   
        self.backend.addHandler(console_handler)
    
    def _setup_file_log(self):
        if self.rotate:
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                self.file, 
                maxBytes=int(self.max_bytes), 
                backupCount=int(self.max_files),
                )
        else:
            from logging import FileHandler
            file_handler = FileHandler(self.file)
        
        if self.level() == logging.getLevelName(logging.DEBUG):
            file_handler.setFormatter(self.debug_formatter)
        else:
            file_handler.setFormatter(self.file_formatter)
            
        file_handler.setLevel(getattr(logging, self.level())) 
        self.backend.addHandler(file_handler)
        
    def level(self):
        return logging.getLevelName(self.backend.level)
    
    def info(self, msg):
        self.backend.info(msg)
        
    def warn(self, msg):
        self.backend.warn(msg)
    
    def error(self, msg):
        self.backend.error(msg)
    
    def fatal(self, msg):
        self.backend.fatal(msg)
    
    def debug(self, msg):
        self.backend.debug(msg)
        
handler.register(LoggingLogHandler)
