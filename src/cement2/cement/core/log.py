
import logging
from zope import interface

from cement.core.exc import CementArgumentError, CementInterfaceError
        
def config_invariant(obj):
    invalid = []
    members = [
        '__init__', 
        '__handler_label__',
        '__handler_type__',
        'clear_loggers',
        'setup_console_log',
        'setup_file_log',
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
        raise CementInterfaceError, \
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
    interface.invariant(config_invariant)
    
    def __init__(config_obj, **kw):
        """
        The __init__ function emplementation of Cement handlers acts as a 
        wrapper for initialization.  In general, the implementation simply
        need to accept the config obj as its first argument.  If the 
        implementation subclasses from something else it will need to
        handle passing the proper args/keyword args to that classes __init__
        function, or you can easily just pass *args, **kw directly to it.
        
        Required Arguments:
        
            config_obj
                The application configuration object after it has been parsed
                and processed.  This is *not* a defaults dictionary, though
                some config handler implementations may work as a dict.
        
        
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
    
    def __init__(self, config_obj, **kw):
        """
        Setup the logging facility.
        
        Required Arguments:
        
            config
                The application configuration object.
        
        
        Optional Arguments:
        
            clear_loggers
                Boolean.  Whether to clear existing loggers.
                
        """
        self.config = config_obj
        self.name = self.config.get('base', 'app_name')
        self.max_bytes = self.config.get('log', 'max_bytes')
        self.max_files = self.config.get('log', 'max_files')
        self.backend = logging.getLogger(self.name)
        self.all_levels = ['INFO', 'WARN', 'ERROR', 'DEBUG', 'FATAL']
        
        # set the level (config first, **kw overrides, INFO default)
        level = kw.get('level', self.config.get('log', 'level')).upper()
        if level not in self.all_levels:
            level = 'INFO'

        # the king trumps all
        if self.config.get('base', 'debug') in [True, 'True', 'true', '1', 1]:
            level = 'DEBUG'
            
        self.backend.setLevel(getattr(logging, level))
        
        # clear loggers?
        if kw.get('clear_loggers', None):
            self.clear_loggers
            
        # console
        if kw.get('to_console', self.config.get('log', 'to_console')):
            self.setup_console_log()
        
        # file
        if kw.get('file', self.config.get('log', 'file')):
            self.setup_file_log()
            
        self.debug("logging initialized for '%s' using LoggingLogHandler" % \
                   self.name)
                   
    def clear_loggers(self):
        for i in logging.getLogger(self.name).handlers:
            logging.getLogger(self.name).removeHandler(i)
            self.backend = logging.getLogger(self.name)
    
    def setup_console_log(self, formatter=None):
        console = logging.StreamHandler()
        if formatter:
            console.setFormatter(formatter)
        elif self.level() == logging.getLevelName(logging.DEBUG):
            console.setFormatter(logging.Formatter(
                "%(asctime)s (%(levelname)s) %(name)s : %(message)s"))
        else: 
            console.setFormatter(
                logging.Formatter("%(levelname)s: %(message)s")
                )
        console.setLevel(getattr(logging, self.level()))   
        self.backend.addHandler(console)
    
    def setup_file_log(self, formatter=None):
        if self.max_bytes:
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                log_file, 
                maxBytes=int(self.max_bytes), 
                backupCount=int(self.max_files),
                )
        else:
            from logging import FileHandler
            file_handler = FileHandler(log_file)
        
        if formatter:
            console.setFormatter(formatter)
        else:
            file_handler.setFormatter(logging.Formatter(
                "%(asctime)s (%(levelname)s) %(name)s : %(message)s"))
        file_handler.setLevel(getattr(logging, self.level())) 
        self.backend.addHandler(file_handler)

        
    def setup_logging(self, level='INFO', **kw):
        """
        Setup the logging facility.  Should only be called during initial
        framework or application initialization.
        
        Required Arguments:
        
            level
                The level to log at 'INFO', 'WARN', 'ERROR', 'DEBUG', 'FATAL'.
        
        Optional Keyword Arguments:
        
            clear_loggers
                Whether to clear existing loggers.
                
            to_console
                Whether to log to the console. Boolean (default: True).  Uses
                logging.StreamHandler()
            
            log_file
                The log file to log to.  If no file is passed, file logging
                is disabled.  Uses logging.FileHandler
                
            file_formatter
                A logging 'formatter' object to pass to 'setFormatter()' for
                the file logger.
            
            console_formatter
                A logging 'formatter' object to pass to 'setFormatter()' for
                the console logger.
              
            max_bytes
                Maximum number of bytes per log file (if log_file is passed).
                Uses logging.RotatingFileHandler() if passed.  Default: None.
            
            max_files
                If log_file and max_bytes are passed, this sets the max number
                of log files to keep.  Default: 4.
                
        """
        
        if level not in self.all_levels:
            raise CementArgumentError("Unknown log level '%s'." % level)
        
        log_level = getattr(logging, level.upper())
                
        clear_loggers = kw.get('clear_loggers', True)
        to_console = kw.get('to_console', True)
        log_file = kw.get('log_file', None)
        file_formatter = kw.get('file_formatter', None)
        console_formatter = kw.get('console_formatter', None)
        max_bytes = kw.get('max_bytes', None)     
        max_files = kw.get('max_files', 4)
        
        # Remove any previously log handlers for this name
        if clear_loggers:
            for i in logging.getLogger(self.name).handlers:
                logging.getLogger(self.name).removeHandler(i)
            self.backend = logging.getLogger(self.name)
            
        self.backend.setLevel(log_level)
        
        # Console formatter    
        if to_console:
            console = logging.StreamHandler()
            if console_formatter:
                console.setFormatter(console_formatter)
            elif log_level == logging.DEBUG:
                console.setFormatter(logging.Formatter(
                    "%(asctime)s (%(levelname)s) %(name)s : %(message)s"))
            else: 
                console.setFormatter(
                    logging.Formatter("%(levelname)s: %(message)s")
                    )
            console.setLevel(log_level)   
            self.backend.addHandler(console)
        
        # File formatter
        if log_file:
            if max_bytes:
                from logging.handlers import RotatingFileHandler
                file_handler = RotatingFileHandler(
                    log_file, 
                    maxBytes=int(max_bytes), 
                    backupCount=int(max_files),
                    )
            else:
                from logging import FileHandler
                file_handler = FileHandler(log_file)
            
            if file_formatter:
                console.setFormatter(console_formatter)
            else:
                file_handler.setFormatter(logging.Formatter(
                    "%(asctime)s (%(levelname)s) %(name)s : %(message)s"))
            file_handler.setLevel(log_level)   
            self.backend.addHandler(file_handler)
        self.debug("logging initialized for '%s' using LoggingLogHandler" % \
                   self.name)
    
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
        
