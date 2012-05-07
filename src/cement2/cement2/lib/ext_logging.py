"""Logging Framework Extension Library."""

import os
import logging
from ..core import exc, util, log
        
class LoggingLogHandler(log.CementLogHandler):  
    """
    This class is an implementation of the :ref:`ILog <cement2.core.log>` 
    interface, and sets up the logging facility using the standard Python
    `logging <http://docs.python.org/library/logging.html>`_ module. 
    
    Optional Arguments / Meta:
        
        namespace
            The logging namespace.  Default: application name.
        
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
    
        <app_label>.debug
        
        log.file
        
        log.to_console
        
        log.rotate
        
        log.max_bytes
        
        log.max_files
    
    
    A sample config section (in any config file) might look like:
    
    .. code-block::text
    
        [<app_label>]
        debug = True
        
        [log]
        file = /path/to/config/file
        level = info
        to_console = true
        rotate = true
        max_bytes = 512000
        max_files = 4
        
    """
    class Meta:
        interface = log.ILog
        label = 'logging'
        namespace = None
        file_format = "%(asctime)s (%(levelname)s) %(name)s : %(message)s"
        console_format = "%(levelname)s: %(message)s"
        debug_format = "%(asctime)s (%(levelname)s) %(name)s : %(message)s"
        clear_loggers = True

        # These are the default config values, overridden by any '[log]' 
        # section in parsed config files.
        config_section = 'log'
        config_defaults = dict(
            file=None,
            level='INFO',
            to_console=True,
            rotate=False,
            max_bytes=512000,
            max_files=4,
            )
    
            
    levels = ['INFO', 'WARN', 'ERROR', 'DEBUG', 'FATAL']

    def __init__(self, *args, **kw):
        super(LoggingLogHandler, self).__init__(*args, **kw)
        self.app = None
        
    def _setup(self, app_obj):
        super(LoggingLogHandler, self)._setup(app_obj)
        self._meta._merge(self.app.config.get_section_dict('log'))
        
        if self._meta.namespace is None:
            self._meta.namespace = self.app._meta.label

        self.backend = logging.getLogger(self._meta.namespace)
        
        # the king trumps all
        if util.is_true(self.app._meta.debug):
            self._meta.level = 'DEBUG'
            
        self.set_level(self._meta.level)
        
        # clear loggers?
        if util.is_true(self._meta.clear_loggers):
            self.clear_loggers()
            
        # console
        if util.is_true(self._meta.to_console):
            self._setup_console_log()
        
        # file
        if self._meta.file:
            self._setup_file_log()
            
        self.debug("logging initialized for '%s' using LoggingLogHandler" % \
                   self._meta.namespace)
                 
    def set_level(self, level):
        """
        Set the log level.  Must be one of the log levels configured in 
        self.levels which are ['INFO', 'WARN', 'ERROR', 'DEBUG', 'FATAL'].
        
        """
        if level not in self.levels:
            level = 'INFO'
        level = getattr(logging, level.upper())
        
        self.backend.setLevel(level)  
        
        for handler in logging.getLogger(self._meta.namespace).handlers:
            handler.setLevel(level)
            
    def clear_loggers(self):
        """
        Clear any previously configured logging namespaces.
        
        """
        if not self._meta.namespace:
            # _setup() probably wasn't run
            return
            
        for i in logging.getLogger(self._meta.namespace).handlers:
            logging.getLogger(self._meta.namespace).removeHandler(i)
            self.backend = logging.getLogger(self._meta.namespace)
    
    def _setup_console_log(self):
        """
        Add a console log handler.
        
        """
        console_handler = logging.StreamHandler()
        if self.level() == logging.getLevelName(logging.DEBUG):
            format = logging.Formatter(self._meta.debug_format)
        else:
            format = logging.Formatter(self._meta.console_format)
        console_handler.setFormatter(format)    
        console_handler.setLevel(getattr(logging, self.level()))   
        self.backend.addHandler(console_handler)
    
    def _setup_file_log(self):
        """
        Add a file log handler.
        
        """
        file = os.path.abspath(os.path.expanduser(self._meta.file))
        log_dir = os.path.dirname(file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        if self._meta.rotate:
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                file, 
                maxBytes=int(self._meta.max_bytes), 
                backupCount=int(self._meta.max_files),
                )
        else:
            from logging import FileHandler
            file_handler = FileHandler(file)
        
        if self.level() == logging.getLevelName(logging.DEBUG):
            format = logging.Formatter(self._meta.debug_format)
        else:
            format = logging.Formatter(self._meta.file_format)
        file_handler.setFormatter(format)   
        file_handler.setLevel(getattr(logging, self.level())) 
        self.backend.addHandler(file_handler)
        
    def level(self):
        """
        Returns the current log level.
        
        """
        return logging.getLevelName(self.backend.level)
    
    def info(self, msg):
        """
        Log to the INFO facility.
        
        Required Arguments:
        
            msg
                The message the log.
        
        """
        self.backend.info(msg)
        
    def warn(self, msg):
        """
        Log to the WARN facility.
        
        Required Arguments:
        
            msg
                The message the log.
        
        """
        self.backend.warn(msg)
    
    def error(self, msg):
        """
        Log to the ERROR facility.
        
        Required Arguments:
        
            msg
                The message the log.
        
        """
        self.backend.error(msg)
    
    def fatal(self, msg):
        """
        Log to the FATAL (aka CRITICAL) facility.
        
        Required Arguments:
        
            msg
                The message the log.
        
        """
        self.backend.fatal(msg)
    
    def debug(self, msg):
        """
        Log to the DEBUG facility.
        
        Required Arguments:
        
            msg
                The message the log.
        
        """
        self.backend.debug(msg)