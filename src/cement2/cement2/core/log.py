"""Cement core log module."""

import logging
from zope import interface

from cement2.core import exc, util
        
def log_handler_invariant(obj):
    invalid = []
    members = [
        '__init__', 
        '__handler_label__',
        '__handler_type__',
        'clear_loggers',
        'setup_console_log',
        'setup_file_log',
        'setup_logging',
        'set_level',
        'level',
        'info', 
        'warn',
        'error', 
        'fatal', 
        'debug', 
        ]
        
    for member in members:
        if not hasattr(obj, member):
            invalid.append(member)
    
    if invalid:
        raise exc.CementInterfaceError, \
            "Invalid or missing: %s in %s" % (invalid, obj)
            
class ILogHandler(interface.Interface):
    """
    This class defines the Log Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
        
    """
    # internal mechanism for handler registration
    __handler_type__ = interface.Attribute('Handler Type Identifier')
    __handler_label__ = interface.Attribute('Handler Label Identifier')
    interface.invariant(log_handler_invariant)
    
    def __init__(config_obj, *args, **kw):
        """
        The __init__ function emplementation of Cement handlers acts as a 
        wrapper for initialization.  In general, the implementation simply
        needs to accept the config obj as its first argument.  If the 
        implementation subclasses from something else it will need to
        handle passing the proper args/keyword args to that classes __init__
        function, or you can easily just pass *args, **kw directly to it.
        
        Required Arguments:
        
            config_obj
                The application configuration object after it has been parsed
                and processed.  This is *not* a dictionary, though some config 
                handler implementations may work as a dict.
        
        
        Optional Arguments:
        
            *args
                Additional positional arguments.
                
            **kw
                Additional keyword arguments.
                
        Returns: n/a
        
        """
        
    def clear_loggers():
        """
        Clear all existing loggers.
        
        """
        
    def setup_console_log():
        """
        Setup logging to the console.
        
        """
        
    def setup_file_log():
        """
        Setup logging to a file.
        
        """
    
    def setup_logging():
        """
        Setup logging per the application config.  This should be a sane
        default logging config.
        
        """
        
    def set_level(self):
        """
        Set the log level.  Must except one of: 'INFO', 'WARN', 'ERROR', 
        'DEBUG', or 'FATAL'.
        
        """
        
    def level(self):
        """
        Return a string representation of the log level.
        """
    
    def info(self, msg):
        """
        Log to the 'INFO' facility.
        
        Required Arguments:
        
            msg
                The message to log.
        
        """
        
    def warn(self, msg):
        """
        Log to the 'WARN' facility.
        
        Required Arguments:
        
            msg
                The message to log.
        
        """
    
    def error(self, msg):
        """
        Log to the 'ERROR' facility.
        
        Required Arguments:
        
            msg
                The message to log.
        
        """
    
    def fatal(self, msg):
        """
        Log to the 'FATAL' facility.
        
        Required Arguments:
        
            msg
                The message to log.
        
        """
    
    def debug(self, msg):
        """
        Log to the 'DEBUG' facility.
        
        Required Arguments:
        
            msg
                The message to log.
        
        """
        
        
class LoggingLogHandler(object):
    __handler_type__ = 'log'
    __handler_label__ = 'logging'
    interface.implements(ILogHandler)
    levels = ['INFO', 'WARN', 'ERROR', 'DEBUG', 'FATAL']
    
    def __init__(self, config_obj, **kw):
        """
        This is an implementation of the ILogHandler interface, and sets up 
        the logging facility using the standard 'logging' module.
        
        Required Arguments:
        
            config_obj
                The application configuration object.
        

        Optional Keyword Arguments:
        
            namespace
                The logging namespace.
                
                
        The following configuration options are recognized:
        
            base.app_name
            base.debug
            log.file
            log.to_console
            log.max_bytes
            log.max_files
            log.level
            log.file_formatter
            log.console_formatter
            log.clear_loggers
            
        FIX ME: need to refactor this class a bit ... all options should be
        able to be sent via **kw... and documented here.
        
        """
        self.config = config_obj
        
        if kw.get('namespace', None):
            self.namespace = kw['namespace']
        else:
            self.namespace = self.config.get('base', 'app_name')
            
        self.backend = logging.getLogger(self.namespace)
        
    def setup_logging(self):
        # set the level (config first, **kw overrides, INFO default)
        level = self.config.get('log', 'level').upper()
        if level not in self.levels:
            level = 'INFO'

        # the king trumps all
        if util.is_true(self.config.get('base', 'debug')):
            level = 'DEBUG'
            
        self.set_level(level)
        
        # clear loggers?
        if util.is_true(self.config.get('log', 'clear_loggers')):
            self.clear_loggers()
            
        # console
        if util.is_true(self.config.get('log', 'to_console')):
            self.setup_console_log()
        
        # file
        if self.config.get('log', 'file'):
            if self.config.get('log', 'max_bytes'):
                self.setup_file_log(
                    self.config.get('log', 'file'),
                    rotate=True,
                    max_bytes=self.config.get('log', 'max_bytes'),
                    max_files=self.config.get('log', 'max_files'),
                    )
            else:
                self.setup_file_log(self.config.get('log', 'file'))
            
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
        for i in logging.getLogger(self.namespace).handlers:
            logging.getLogger(self.namespace).removeHandler(i)
            self.backend = logging.getLogger(self.namespace)
    
    def setup_console_log(self, formatter=None):
        console = logging.StreamHandler()
        if formatter:
            console.setFormatter(formatter)
        elif self.level() == logging.getLevelName(logging.DEBUG):
            format_str = "%(asctime)s (%(levelname)s) %(name)s : %(message)s"
        else:
            format_str = "%(levelname)s: %(message)s"
            
        console.setFormatter(logging.Formatter(format_str))
        console.setLevel(getattr(logging, self.level()))   
        self.backend.addHandler(console)
    
    def setup_file_log(self, path, **kw):
        """
        Setup a file log.
        
        Required Arguments:
        
            path
                The path to the log file.
                
        Optional Keyword Arguments:
        
            rotate
                bool.  Whether to rotate the log file.
                
            max_bytes
                int: Number of bytes to rotate file at.  Default: 512000.
            
            max_files
                int: Number of files to keep when rotating.  Default: 4.
                
            formatter
                object: A logging 'formatter' object.  Default format is:
                "%(asctime)s (%(levelname)s) %(name)s : %(message)s"
                
        """
        if kw.get('rotate', None):
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                path, 
                maxBytes=int(kw.get('max_bytes', 512000)), 
                backupCount=int(kw.get('max_files', 4)),
                )
        else:
            from logging import FileHandler
            file_handler = FileHandler(path)
        
        format_str = "%(asctime)s (%(levelname)s) %(name)s : %(message)s"
        file_handler.setFormatter(logging.Formatter(format_str))
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
        
