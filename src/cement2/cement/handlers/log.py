
import logging
from cement.core.exc import CementArgumentError

class CementLogHandler(object):
    """
    Create a standard object for logging.  
    
    Required Arguments:
    
        name
            The name of the logging namespaces.
    
    
    Usage:
            
    .. code-block:: python
    
        from cement.handlers.log import CementLogHandler
        log = CementLogHandler('cement')
        log.info('this is an info message')
        
        
    This class is largely unimplemented and needs to be subclassed from.
    
    """
    def __init__(self, name):
        self.all_levels = ['INFO', 'WARN', 'ERROR', 'DEBUG', 'FATAL']
        self.name = name
        self.backend = None
        
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
        raise NotImplementedError
        
    @property
    def level(self):
        """
        Return a string representation of the log level.
        """
        raise NotImplementedError
    
    def info(self, msg):
        """
        Log to the 'INFO' facility.
        
        Required Arguments:
        
            msg
                The message to log.
        
        """
        raise NotImplementedError
        
    def warn(self, msg):
        """
        Log to the 'WARN' facility.
        
        Required Arguments:
        
            msg
                The message to log.
        
        """
        raise NotImplementedError
    
    def error(self, msg):
        """
        Log to the 'ERROR' facility.
        
        Required Arguments:
        
            msg
                The message to log.
        
        """
        raise NotImplementedError
    
    def fatal(self, msg):
        """
        Log to the 'FATAL' facility.
        
        Required Arguments:
        
            msg
                The message to log.
        
        """
        raise NotImplementedError
    
    def debug(self, msg):
        """
        Log to the 'DEBUG' facility.
        
        Required Arguments:
        
            msg
                The message to log.
        
        """
        raise NotImplementedError
        
        
class LoggingLogHandler(CementLogHandler):
    def __init__(self, name):
        CementLogHandler.__init__(self, name)
        
        self.all_levels = ['INFO', 'WARN', 'ERROR', 'DEBUG', 'FATAL']
        self.name = name
        self.backend = logging.getLogger(self.name)
        
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
        
    @property
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
        